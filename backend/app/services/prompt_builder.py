from app.models.conversation import ConversationContext
from app.rag_engine.citations import CitationFormatter
from app.events.types import PromptEvent
from app.diagnostics.event_bus import event_bus
import time
from datetime import datetime, timezone, timedelta

class PromptBuilder:
    def __init__(self):
        self.citation_formatter = CitationFormatter()
        
    def build(self, context: ConversationContext) -> str:
        start_time = time.time()
        
        ist_tz = timezone(timedelta(hours=5, minutes=30))
        current_time = datetime.now(ist_tz).strftime("%Y-%m-%d %I:%M:%S %p IST")
        # Base System Prompt
        sys_prompt = f"You are an advanced enterprise AI assistant. The current date and time is {current_time}."
        
        context.system_prompt = sys_prompt
        
        # Build Final Prompt with Sources (Recency Bias optimization)
        final_prompt = context.user_query
        
        formatted_sources = ""
        if context.final_sources:
            formatted_sources = self.citation_formatter.format_sources(context.final_sources)
            final_prompt = f"Context Information:\n{formatted_sources}\n\nBased on the context information above, answer the following query: {context.user_query}\nIf the answer is not in the context, say you don't know."
            
        context.final_prompt = final_prompt
        
        # Rough token estimation for events
        sys_tokens = len(sys_prompt.split())
        ctx_tokens = len(formatted_sources.split())
        hist_tokens = sum(len(m.content.split()) for m in context.history)
        final_tokens = len(context.final_prompt.split())
        
        event_bus.emit(PromptEvent(
            session_id=context.session_id,
            stage="prompt_building",
            system_prompt_tokens=sys_tokens,
            context_tokens=ctx_tokens,
            history_tokens=hist_tokens,
            final_prompt_tokens=final_tokens,
            latency_ms=round((time.time() - start_time) * 1000)
        ))
        
        return sys_prompt

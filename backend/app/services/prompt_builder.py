from app.models.conversation import ConversationContext
from app.rag_engine.citations import CitationFormatter
from app.events.types import PromptEvent
from app.diagnostics.event_bus import event_bus
import time

class PromptBuilder:
    def __init__(self):
        self.citation_formatter = CitationFormatter()
        
    def build(self, context: ConversationContext) -> str:
        start_time = time.time()
        
        # Base System Prompt
        sys_prompt = "You are an advanced enterprise AI assistant."
        
        # Add Sources
        formatted_sources = ""
        if context.final_sources:
            sys_prompt += "\n\nYou must answer the user's query using the following context sources. If the answer is not in the sources, say you don't know.\n\n"
            formatted_sources = self.citation_formatter.format_sources(context.final_sources)
            sys_prompt += formatted_sources
            
        context.system_prompt = sys_prompt
        
        # We assume history is passed separately to LLM, so final_prompt is just the user query.
        # However, if we need to wrap everything into one, we would do it here.
        # But typically we pass a list of messages. We will build the `system` message.
        
        context.final_prompt = context.user_query
        
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

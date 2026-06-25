import json
import time
from typing import AsyncGenerator
from app.models.conversation import ConversationContext
from app.providers.providers import ProviderFactory
from app.events.types import GenerationEvent
from app.diagnostics.event_bus import event_bus

class ChatService:
    def __init__(self):
        self.llm_provider = ProviderFactory.get_llm_provider()
        
    async def generate_stream(self, context: ConversationContext) -> AsyncGenerator[str, None]:
        # Construct messages payload
        messages = [{"role": "system", "content": context.system_prompt}]
        for msg in context.history:
            messages.append({"role": msg.role, "content": msg.content})
            
        messages.append({"role": "user", "content": context.final_prompt})
        
        try:
            stream = self.llm_provider.generate_stream(
                messages=messages,
                model=context.model
            )
            
            async for chunk in stream:
                if chunk["type"] == "metrics":
                    # Emit generation event
                    metrics = chunk["metrics"]
                    mech = metrics.get("transformer_mechanics", {})
                    
                    event_bus.emit(GenerationEvent(
                        session_id=context.session_id,
                        stage="generation",
                        model=context.model,
                        total_tokens=metrics.get("total_tokens", 0),
                        tokens_per_sec=metrics.get("tokens_per_sec", 0.0),
                        perplexity=mech.get("perplexity"),
                        avg_entropy=mech.get("avg_entropy"),
                        kv_cache_mb=mech.get("kv_cache_mb"),
                        attention_flops=mech.get("attention_flops"),
                        sequence_length=mech.get("sequence_length", 0),
                        latency_ms=metrics.get("latency_ms")
                    ))
                    
                    context.telemetry["generation_metrics"] = metrics
                    
                    yield f'data: {json.dumps(chunk)}\n\n'
                else:
                    yield f'data: {json.dumps(chunk)}\n\n'
                    
        except Exception as e:
            error_msg = f"Error during streaming: {str(e)}"
            context.failures.append(error_msg)
            yield f'data: {json.dumps({"type": "content", "content": error_msg})}\n\n'

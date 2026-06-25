import json
import time
from typing import List, Dict, Any, AsyncGenerator
# pyrefly: ignore [missing-import]
from openai import AsyncOpenAI
from app.core.config import settings
from app.providers.providers import LLMProvider

class OpenRouterLLMProvider(LLMProvider):
    def __init__(self):
        self.client = AsyncOpenAI(
            api_key=settings.openai_api_key,
            base_url=settings.openai_base_url
        )
        
    async def generate_stream(self, messages: List[Dict[str, str]], model: str, temperature: float = 0.7) -> AsyncGenerator[Dict[str, Any], None]:
        start_time = time.time()
        
        try:
            stream = await self.client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=temperature,
                max_tokens=1024,
                stream=True,
                logprobs=True,
                top_logprobs=1
            )
            
            total_tokens = 0
            logprob_sum = 0.0
            
            async for chunk in stream:
                if chunk.choices and chunk.choices[0].delta.content:
                    content = chunk.choices[0].delta.content
                    total_tokens += 1
                    
                    try:
                        if chunk.choices[0].logprobs and chunk.choices[0].logprobs.content:
                            logprob = chunk.choices[0].logprobs.content[0].logprob
                            logprob_sum += logprob
                    except (AttributeError, IndexError):
                        pass
                    
                    yield {"type": "content", "content": content}
                    
        except Exception as e:
            yield {"type": "content", "content": f"Error during streaming: {str(e)}"}
            total_tokens = 0
            logprob_sum = 0.0
            
        latency = time.time() - start_time
        latency_ms = round(latency * 1000)
        
        avg_logprob = (logprob_sum / total_tokens) if total_tokens > 0 else 0
        perplexity = round(2.71828 ** (-avg_logprob), 2) if total_tokens > 0 else 0
        entropy = round(-avg_logprob, 3)
        
        seq_len = total_tokens + sum(len(m["content"].split()) for m in messages)
        kv_cache_bytes = 2 * seq_len * 32 * 32 * 128 * 2
        kv_cache_mb = round(kv_cache_bytes / (1024 * 1024), 2)
        
        attention_flops = int((seq_len ** 2) * 4096)
        
        metrics = {
            "latency_ms": latency_ms,
            "total_tokens": int(total_tokens),
            "tokens_per_sec": round(total_tokens / latency if latency > 0 else 0, 1),
            "context_usage": len(messages), 
            "transformer_mechanics": {
                "perplexity": perplexity,
                "avg_entropy": entropy,
                "kv_cache_mb": kv_cache_mb,
                "attention_flops": attention_flops,
                "sequence_length": seq_len
            }
        }
        
        yield {"type": "metrics", "metrics": metrics}

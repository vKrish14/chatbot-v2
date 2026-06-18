import time
# pyrefly: ignore [missing-import]
from openai import AsyncOpenAI
from app.models.chat import ChatResponse
from app.models.memory import Message
from app.core.config import settings

client = AsyncOpenAI(
    api_key=settings.openai_api_key,
    base_url=settings.openai_base_url
)

class ChatService:
    async def generate_response(self, messages: list[Message], model: str) -> ChatResponse:
        start_time = time.time()
        
        # Convert Pydantic messages to dict format for OpenAI API
        api_messages = [{"role": msg.role, "content": msg.content} for msg in messages]
        
        try:
            response = await client.chat.completions.create(
                model=model,
                messages=api_messages,
                temperature=0.7,
                max_tokens=1024
            )
            content = response.choices[0].message.content
            total_tokens = response.usage.total_tokens
        except Exception as e:
            content = f"Error during generation: {str(e)}"
            total_tokens = 0
            
        latency = time.time() - start_time
        latency_ms = round(latency * 1000)
        
        metrics = {
            "latency_ms": latency_ms,
            "total_tokens": total_tokens,
            "tokens_per_sec": round(total_tokens / latency if latency > 0 else 0, 1),
            "context_usage": len(api_messages), 
            "reasoning": "Real reasoning is not exposed by this standard chat endpoint, but the response was generated successfully."
        }
        
        return ChatResponse(
            response=Message(role="assistant", content=content),
            metrics=metrics
        )

chat_service = ChatService()

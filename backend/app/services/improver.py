import time
# pyrefly: ignore [missing-import]
from openai import AsyncOpenAI
from app.models.prompt import PromptImproveResponse
from app.core.config import settings

client = AsyncOpenAI(
    api_key=settings.openai_api_key,
    base_url=settings.openai_base_url
)

class PromptImproverService:
    async def improve_prompt(self, original_prompt: str) -> PromptImproveResponse:
        start_time = time.time()
        
        try:
            response = await client.chat.completions.create(
                model="google/gemma-4-31b-it:free",  # free model for prompt improvement
                messages=[
                    {"role": "system", "content": "You are an expert prompt engineer. Your task is to rewrite the user's prompt to be much more detailed, clear, and structured for an LLM to understand. Output ONLY the improved prompt, with no additional commentary."},
                    {"role": "user", "content": original_prompt}
                ],
                temperature=0.4,
                max_tokens=500
            )
            improved_prompt = response.choices[0].message.content.strip()
        except Exception as e:
            # Fallback to original if API fails
            improved_prompt = f"{original_prompt} (Error improving: {str(e)})"
            
        latency = time.time() - start_time
        
        return PromptImproveResponse(
            original_prompt=original_prompt,
            improved_prompt=improved_prompt,
            improvement_metrics={
                "latency_ms": round(latency * 1000, 2),
                "tokens_added": len(improved_prompt.split()) - len(original_prompt.split())
            }
        )

prompt_improver = PromptImproverService()

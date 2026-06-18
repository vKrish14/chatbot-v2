from pydantic import BaseModel

class PromptImproveRequest(BaseModel):
    original_prompt: str
    
class PromptImproveResponse(BaseModel):
    original_prompt: str
    improved_prompt: str
    improvement_metrics: dict

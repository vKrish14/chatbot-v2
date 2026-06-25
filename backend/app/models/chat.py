from pydantic import BaseModel
from typing import List, Optional
from app.models.memory import Message

class ChatRequest(BaseModel):
    messages: List[Message]
    model: str
    temperature: float = 0.7
    search_strategy: str = "similarity"
    top_k: int = 4
    similarity_threshold: float = 0.5

class ChatResponse(BaseModel):
    response: Message
    metrics: dict

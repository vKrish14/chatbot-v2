from pydantic import BaseModel
from typing import List, Optional
from app.models.memory import Message

class ChatRequest(BaseModel):
    messages: List[Message]
    model: str
    temperature: float = 0.7

class ChatResponse(BaseModel):
    response: Message
    metrics: dict

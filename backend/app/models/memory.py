from pydantic import BaseModel
from typing import List, Optional

class Message(BaseModel):
    role: str
    content: str

class MemoryStats(BaseModel):
    total_messages: int
    context_window: int
    retained_messages: int
    estimated_tokens: int

class MemoryProcessRequest(BaseModel):
    session_id: str
    messages: List[Message]
    context_window: int = 10

class MemoryProcessResponse(BaseModel):
    processed_messages: List[Message]
    stats: MemoryStats

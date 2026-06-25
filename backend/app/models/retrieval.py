from pydantic import BaseModel, Field
from typing import List, Optional
from .conversation import Source

class RetrievalRequest(BaseModel):
    query: str
    session_id: str
    strategy: str = "similarity" # similarity, mmr, hybrid
    top_k: int = 4
    threshold: float = 0.5

class RetrievalResponse(BaseModel):
    sources: List[Source]
    strategy_used: str
    latency_ms: float

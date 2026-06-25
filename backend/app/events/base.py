from pydantic import BaseModel, Field
from datetime import datetime
from uuid import uuid4
from typing import Optional, Dict, Any

class BaseEvent(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    timestamp: float = Field(default_factory=lambda: datetime.now().timestamp())
    session_id: str
    stage: str
    latency_ms: Optional[float] = None
    success: bool = True
    error: Optional[str] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)

from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from .memory import Message
from uuid import uuid4

class Source(BaseModel):
    document_id: str
    document_name: str
    chunk_id: str
    content: str
    similarity: float
    page: Optional[int] = None
    section: Optional[str] = None
    url: Optional[str] = None  # for web sources

class ConversationContext(BaseModel):
    session_id: str = Field(default_factory=lambda: str(uuid4()))
    user_query: str = ""
    history: List[Message] = Field(default_factory=list)
    retrieved_chunks: List[Source] = Field(default_factory=list)
    web_results: List[Source] = Field(default_factory=list)
    final_sources: List[Source] = Field(default_factory=list)
    
    # Built prompts
    system_prompt: str = ""
    final_prompt: str = ""
    
    # State tracking
    failures: List[str] = Field(default_factory=list)
    telemetry: Dict[str, Any] = Field(default_factory=dict)
    diagnostics: Dict[str, Any] = Field(default_factory=dict)
    
    # Pipeline configuration for this request
    pipeline_type: str = "chat"
    model: str = "default"
    search_strategy: str = "similarity"
    top_k: int = 4
    similarity_threshold: float = 0.5

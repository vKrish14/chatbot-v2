from pydantic import BaseModel, Field
from typing import Dict, Any, Optional
from datetime import datetime
import uuid

class DocumentMetadata(BaseModel):
    filename: str
    session_id: str = "default"
    document_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    upload_timestamp: float = Field(default_factory=lambda: datetime.now().timestamp())
    file_type: str
    page_count: Optional[int] = 0
    chunk_count: Optional[int] = 0
    embedded: bool = False
    embedding_model: Optional[str] = None

class DocumentChunk(BaseModel):
    chunk_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    document_id: str
    content: str
    metadata: Dict[str, Any] = Field(default_factory=dict)

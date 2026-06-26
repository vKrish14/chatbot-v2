from typing import List, Dict, Any, Optional
from .base import BaseEvent

class PipelineEvent(BaseEvent):
    query: str
    pipeline_type: str  # chat, rag, web
    total_latency_ms: Optional[float] = None

class RetrieverEvent(BaseEvent):
    strategy: str  # similarity, mmr, hybrid
    top_k: int
    chunks_retrieved: int
    avg_similarity: Optional[float] = None
    threshold: Optional[float] = None
    sources: Optional[List[Dict[str, Any]]] = None

class EmbeddingEvent(BaseEvent):
    model: str
    tokens: int
    vector_dimension: int

class PromptEvent(BaseEvent):
    system_prompt_tokens: int
    context_tokens: int
    history_tokens: int
    final_prompt_tokens: int

class GenerationEvent(BaseEvent):
    model: str
    total_tokens: int
    tokens_per_sec: float
    perplexity: Optional[float] = None
    avg_entropy: Optional[float] = None
    kv_cache_mb: Optional[float] = None
    attention_flops: Optional[int] = None
    sequence_length: int

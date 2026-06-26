from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from app.models.document import DocumentChunk
from app.models.conversation import Source

class LLMProvider(ABC):
    @abstractmethod
    async def generate_stream(self, messages: List[Dict[str, str]], model: str, temperature: float = 0.7):
        pass

class EmbeddingProvider(ABC):
    @abstractmethod
    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        pass
    
    @abstractmethod
    def embed_query(self, text: str) -> List[float]:
        pass
    
    @property
    @abstractmethod
    def dimension(self) -> int:
        pass

class VectorStoreProvider(ABC):
    @abstractmethod
    def add_chunks(self, chunks: List[DocumentChunk]):
        pass
    
    @abstractmethod
    def search(self, query_embedding: List[float], top_k: int = 4, threshold: float = 0.0, session_id: str = "default") -> List[Source]:
        pass

class WebSearchProvider(ABC):
    @abstractmethod
    def search(self, query: str, top_k: int = 4) -> List[Source]:
        pass

class ProviderFactory:
    _llm_provider = None
    _embedding_provider = None
    _vectorstore_provider = None
    _websearch_provider = None
    
    @classmethod
    def get_llm_provider(cls) -> LLMProvider:
        if not cls._llm_provider:
            from .llm.openrouter import OpenRouterLLMProvider
            cls._llm_provider = OpenRouterLLMProvider()
        return cls._llm_provider
    
    @classmethod
    def get_embedding_provider(cls) -> EmbeddingProvider:
        if not cls._embedding_provider:
            from .embeddings.sentence_transformers import SentenceTransformersProvider
            cls._embedding_provider = SentenceTransformersProvider()
        return cls._embedding_provider
        
    @classmethod
    def get_vectorstore_provider(cls) -> VectorStoreProvider:
        if not cls._vectorstore_provider:
            from .vectorstore.chroma import ChromaDBProvider
            cls._vectorstore_provider = ChromaDBProvider()
        return cls._vectorstore_provider
        
    @classmethod
    def get_websearch_provider(cls) -> WebSearchProvider:
        if not cls._websearch_provider:
            from .search.web_search_provider import DuckDuckGoProvider
            cls._websearch_provider = DuckDuckGoProvider()
        return cls._websearch_provider

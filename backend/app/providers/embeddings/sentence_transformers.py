from typing import List
# pyrefly: ignore [missing-import]
from langchain_community.embeddings import HuggingFaceEmbeddings
from app.providers.providers import EmbeddingProvider

class SentenceTransformersProvider(EmbeddingProvider):
    def __init__(self, model_name: str = "BAAI/bge-small-en-v1.5"):
        # Utilizing Langchain's HuggingFaceEmbeddings wrapper
        self.embeddings = HuggingFaceEmbeddings(
            model_name=model_name,
            model_kwargs={'device': 'cpu'},  # Default to CPU for broad compatibility
            encode_kwargs={'normalize_embeddings': True}
        )
        self._model_name = model_name
        # BGE small generates 384 dimensional vectors
        self._dimension = 384 

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        return self.embeddings.embed_documents(texts)
    
    def embed_query(self, text: str) -> List[float]:
        return self.embeddings.embed_query(text)
    
    @property
    def dimension(self) -> int:
        return self._dimension

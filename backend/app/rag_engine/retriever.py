from typing import List
from app.providers.providers import ProviderFactory
from app.models.conversation import Source

class Retriever:
    def __init__(self):
        self.vector_store = ProviderFactory.get_vectorstore_provider()
        self.embedding_provider = ProviderFactory.get_embedding_provider()
        
    def retrieve(self, query: str, strategy: str = "similarity", top_k: int = 4, threshold: float = 0.0, session_id: str = "default") -> List[Source]:
        # 1. Embed query
        query_embedding = self.embedding_provider.embed_query(query)
        
        # 2. Search
        # We only support similarity for now in Chroma basic wrapper, but we would implement MMR here if needed.
        sources = self.vector_store.search(
            query_embedding=query_embedding,
            top_k=top_k,
            threshold=threshold,
            session_id=session_id
        )
        
        return sources

from typing import List
from app.models.conversation import Source

class Ranker:
    def rank(self, query: str, sources: List[Source], top_k: int) -> List[Source]:
        # Lightweight ranking stage.
        # For now, it just sorts by similarity and returns top_k.
        # In the future, a CrossEncoder or Cohere Rerank could be inserted here.
        sorted_sources = sorted(sources, key=lambda x: x.similarity, reverse=True)
        return sorted_sources[:top_k]

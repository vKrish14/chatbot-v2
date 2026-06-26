import uuid
from typing import List
from duckduckgo_search import DDGS
from app.providers.providers import WebSearchProvider
from app.models.conversation import Source

class DuckDuckGoProvider(WebSearchProvider):
    def __init__(self):
        pass

    def search(self, query: str, top_k: int = 4) -> List[Source]:
        try:
            with DDGS() as ddgs:
                results = list(ddgs.text(query, max_results=top_k))
            
            sources = []
            for res in results:
                sources.append(Source(
                    document_id=str(uuid.uuid4()),
                    document_name=res.get("title", "Web Result"),
                    chunk_id=str(uuid.uuid4()),
                    content=res.get("body", ""),
                    similarity=0.0,
                    url=res.get("href", "")
                ))
            return sources
        except Exception as e:
            print(f"Error during web search: {e}")
            return []

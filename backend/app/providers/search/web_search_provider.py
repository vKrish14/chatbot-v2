import uuid
from typing import List
# pyrefly: ignore [missing-import]
from langchain_community.tools import DuckDuckGoSearchResults
from app.providers.providers import WebSearchProvider
from app.models.conversation import Source

class DuckDuckGoProvider(WebSearchProvider):
    def __init__(self):
        self.search_tool = DuckDuckGoSearchResults(num_results=4)

    def search(self, query: str, top_k: int = 4) -> List[Source]:
        try:
            # DuckDuckGoSearchResults returns a string format which we need to parse
            # Alternatively use DuckDuckGoSearchRun or API wrappers for JSON.
            # Using basic wrapper and parsing logic.
            from langchain_community.utilities import DuckDuckGoSearchAPIWrapper
            wrapper = DuckDuckGoSearchAPIWrapper(max_results=top_k)
            results = wrapper.results(query, max_results=top_k)
            
            sources = []
            for res in results:
                sources.append(Source(
                    document_id=str(uuid.uuid4()),
                    document_name=res.get("title", "Web Result"),
                    chunk_id=str(uuid.uuid4()),
                    content=res.get("snippet", ""),
                    similarity=0.0, # Web results don't have vector similarity
                    url=res.get("link", "")
                ))
            return sources
        except Exception as e:
            print(f"Error during web search: {e}")
            return []

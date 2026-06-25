from typing import List
from app.models.conversation import Source

class CitationFormatter:
    def format_sources(self, sources: List[Source]) -> str:
        if not sources:
            return ""
            
        formatted = "### Context Sources:\n"
        for i, source in enumerate(sources):
            formatted += f"[{i+1}] **{source.document_name}**"
            if source.page:
                formatted += f" (Page {source.page})"
            if source.similarity:
                formatted += f" - Similarity: {source.similarity:.2f}"
            if source.url:
                formatted += f" - URL: {source.url}"
            formatted += f"\nSnippet: {source.content[:200]}...\n\n"
            
        return formatted

from typing import List
from app.models.conversation import ConversationContext
from app.rag_engine.retriever import Retriever
from app.rag_engine.ranking import Ranker
from app.providers.providers import ProviderFactory
from app.events.types import RetrieverEvent
from app.diagnostics.event_bus import event_bus
import time

class ContextProvidersLayer:
    def __init__(self):
        self.retriever = Retriever()
        self.ranker = Ranker()
        self.web_search = ProviderFactory.get_websearch_provider()
        
    def populate_context(self, context: ConversationContext):
        # 1. Memory Context (already populated in history)
        
        # 2. Vector Retrieval Context
        if context.pipeline_type in ["rag", "hybrid"]:
            start_time = time.time()
            try:
                sources = self.retriever.retrieve(
                    query=context.user_query,
                    strategy=context.search_strategy,
                    top_k=context.top_k,
                    threshold=context.similarity_threshold,
                    session_id=context.session_id
                )
                
                if not sources and context.pipeline_type in ["rag", "hybrid"]:
                    # Fallback: if the user explicitly queried the document (e.g. "summarize") 
                    # but similarity was too low, bypass the threshold to return the document's chunks.
                    sources = self.retriever.retrieve(
                        query=context.user_query,
                        strategy=context.search_strategy,
                        top_k=context.top_k,
                        threshold=0.0,
                        session_id=context.session_id
                    )
                context.retrieved_chunks = sources
                
                # Emit event
                event_bus.emit(RetrieverEvent(
                    session_id=context.session_id,
                    stage="vector_retrieval",
                    strategy=context.search_strategy,
                    top_k=context.top_k,
                    chunks_retrieved=len(sources),
                    avg_similarity=sum(s.similarity for s in sources) / len(sources) if sources else 0.0,
                    threshold=context.similarity_threshold,
                    latency_ms=round((time.time() - start_time) * 1000),
                    sources=[s.model_dump() for s in sources]
                ))
            except Exception as e:
                context.failures.append(f"Vector Retrieval Error: {str(e)}")
                
        # 3. Web Retrieval Context
        if context.pipeline_type in ["web", "hybrid"]:
            start_time = time.time()
            try:
                sources = self.web_search.search(
                    query=context.user_query,
                    top_k=context.top_k
                )
                context.web_results = sources
                
                event_bus.emit(RetrieverEvent(
                    session_id=context.session_id,
                    stage="web_retrieval",
                    strategy="web_search",
                    top_k=context.top_k,
                    chunks_retrieved=len(sources),
                    latency_ms=round((time.time() - start_time) * 1000),
                    sources=[s.model_dump() for s in sources]
                ))
            except Exception as e:
                context.failures.append(f"Web Retrieval Error: {str(e)}")
                
        # 4. Ranking
        all_sources = context.retrieved_chunks + context.web_results
        if all_sources:
            context.final_sources = self.ranker.rank(context.user_query, all_sources, context.top_k)

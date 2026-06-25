import os
from typing import List
# pyrefly: ignore [missing-import]
import chromadb
from app.providers.providers import VectorStoreProvider
from app.models.document import DocumentChunk
from app.models.conversation import Source

class ChromaDBProvider(VectorStoreProvider):
    def __init__(self, persist_directory: str = "./vector_db"):
        self.persist_directory = persist_directory
        if not os.path.exists(self.persist_directory):
            os.makedirs(self.persist_directory)
        self.client = chromadb.PersistentClient(path=self.persist_directory)
        # We will manage collections dynamically, but here we can define a default one
        self.collection_name = "default_collection"
        self.collection = self.client.get_or_create_collection(name=self.collection_name)

    def add_chunks(self, chunks: List[DocumentChunk]):
        if not chunks:
            return
            
        ids = [chunk.chunk_id for chunk in chunks]
        documents = [chunk.content for chunk in chunks]
        metadatas = [chunk.metadata for chunk in chunks]
        
        # In a real implementation, we would pass embeddings instead of text if we embed manually
        # but chroma can also use default embedding or we can pass embeddings explicitly.
        # Assuming RAG engine passes embedded chunks, we should add embeddings here.
        # For simplicity, we just pass documents and let Chroma handle it, or we expect
        # the caller to have embedded them. We'll refine this in the vectorstore integration.
        self.collection.add(
            ids=ids,
            documents=documents,
            metadatas=metadatas
        )

    def search(self, query_embedding: List[float], top_k: int = 4, threshold: float = 0.0) -> List[Source]:
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k
        )
        
        sources = []
        if not results['documents'] or not results['documents'][0]:
            return sources
            
        docs = results['documents'][0]
        metas = results['metadatas'][0]
        distances = results['distances'][0]
        ids = results['ids'][0]
        
        for i in range(len(docs)):
            similarity = 1.0 - (distances[i] / 2.0) if distances[i] else 0.0 # simple conversion assuming cosine distance
            
            if similarity >= threshold:
                sources.append(Source(
                    document_id=metas[i].get("document_id", ""),
                    document_name=metas[i].get("filename", "Unknown"),
                    chunk_id=ids[i],
                    content=docs[i],
                    similarity=similarity,
                    page=metas[i].get("page"),
                    section=metas[i].get("section")
                ))
                
        return sources

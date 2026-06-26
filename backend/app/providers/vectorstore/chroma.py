import os
import uuid
from typing import List
import chromadb
from app.providers.providers import VectorStoreProvider, ProviderFactory
from app.models.document import DocumentChunk
from app.models.conversation import Source

class ChromaDBProvider(VectorStoreProvider):
    def __init__(self, persist_directory: str = "./vector_db"):
        self.persist_directory = persist_directory
        try:
            if not os.path.exists(self.persist_directory):
                os.makedirs(self.persist_directory)
            self.client = chromadb.PersistentClient(path=self.persist_directory)
            print(f"ChromaDB persistent client created at {self.persist_directory}")
        except Exception as e:
            # Fallback for restricted environments like Hugging Face Spaces where os.makedirs or PersistentClient fail (e.g. read-only filesystem)
            print(f"Failed to create persistent client ({e}). Using EphemeralClient instead.")
            self.client = chromadb.EphemeralClient()
            
        self.collection_name = "default_collection"
        self.collection = self.client.get_or_create_collection(name=self.collection_name)

    def add_chunks(self, chunks: List[DocumentChunk]):
        if not chunks:
            return
            
        ids = [chunk.chunk_id for chunk in chunks]
        documents = [chunk.content for chunk in chunks]
        metadatas = [chunk.metadata for chunk in chunks]
        
        # We must manually compute embeddings so Chroma doesn't use the default all-MiniLM model
        embedding_provider = ProviderFactory.get_embedding_provider()
        embeddings = embedding_provider.embed_documents(documents)
        
        self.collection.add(
            ids=ids,
            embeddings=embeddings,
            documents=documents,
            metadatas=metadatas
        )

    def search(self, query_embedding: List[float], top_k: int = 4, threshold: float = 0.0, session_id: str = "default") -> List[Source]:
        # Using include=["documents", "metadatas", "distances"] explicitly
        where_filter = {"session_id": session_id}
        
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
            where=where_filter,
            include=["documents", "metadatas", "distances"]
        )
        
        sources = []
        if not results['documents'] or not results['documents'][0]:
            return sources
            
        docs = results['documents'][0]
        metas = results['metadatas'][0]
        distances = results['distances'][0]
        ids = results['ids'][0]
        
        for i in range(len(docs)):
            # Chroma uses L2 distance by default. L2 squared is up to 4 for normalized vectors.
            # Convert L2 distance to cosine similarity (assuming embeddings are normalized)
            # cosine_sim = 1 - (l2_squared / 2)
            similarity = 1.0 - (distances[i] / 2.0) if distances[i] else 0.0
            
            if similarity >= threshold:
                sources.append(Source(
                    document_id=metas[i].get("document_id", str(uuid.uuid4())),
                    document_name=metas[i].get("filename", "Unknown"),
                    chunk_id=ids[i],
                    content=docs[i],
                    similarity=similarity,
                    page=metas[i].get("page", 0),
                    section=metas[i].get("section", "")
                ))
                
        return sources


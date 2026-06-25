import os
import json
from typing import List, Dict, Any
from app.models.document import DocumentMetadata, DocumentChunk
from app.rag_engine.loaders import DocumentLoader
from app.rag_engine.cleaning import TextCleaner
from app.rag_engine.chunking import Chunker
from app.providers.providers import ProviderFactory

class IngestionPipeline:
    def __init__(self, metadata_dir: str = "./vector_db/collections"):
        self.loader = DocumentLoader()
        self.cleaner = TextCleaner()
        self.chunker = Chunker()
        self.metadata_dir = metadata_dir
        if not os.path.exists(self.metadata_dir):
            os.makedirs(self.metadata_dir)
        self.metadata_path = os.path.join(self.metadata_dir, "documents.json")
        self._documents_cache: Dict[str, dict] = self._load_metadata()

    def _load_metadata(self) -> Dict[str, dict]:
        if os.path.exists(self.metadata_path):
            try:
                with open(self.metadata_path, 'r') as f:
                    return json.load(f)
            except:
                return {}
        return {}
        
    def _save_metadata(self):
        with open(self.metadata_path, 'w') as f:
            json.dump(self._documents_cache, f, indent=2)
            
    def get_all_documents(self) -> List[DocumentMetadata]:
        return [DocumentMetadata(**doc) for doc in self._documents_cache.values()]
        
    def delete_document(self, document_id: str):
        if document_id in self._documents_cache:
            # We would also want to remove from vector store here, but Chroma doesn't 
            # easily support delete by metadata out of the box in this simple wrapper.
            # In a real app we'd call vector_store.delete(where={"document_id": document_id})
            del self._documents_cache[document_id]
            self._save_metadata()

    def process_file(self, file_content: bytes, filename: str) -> DocumentMetadata:
        # 1. Load
        raw_docs = self.loader.load(file_content, filename)
        
        # 2. Clean
        for doc in raw_docs:
            doc["content"] = self.cleaner.clean(doc["content"])
            
        # 3. Create Metadata
        _, ext = os.path.splitext(filename)
        doc_meta = DocumentMetadata(
            filename=filename,
            file_type=ext.lower()
        )
        
        # 4. Chunk
        chunks = self.chunker.chunk_documents(raw_docs, doc_meta.document_id, filename)
        
        doc_meta.page_count = len(raw_docs)
        doc_meta.chunk_count = len(chunks)
        
        # 5. Add to Vector Store (requires embeddings)
        # Assuming Chroma uses the default embedding function if none provided, 
        # or we explicitly use our ProviderFactory embedding provider.
        # But Chroma needs the embedding provider wrapped in its format.
        # To keep it simple, we just pass documents to Chroma and if it handles embeddings, great.
        vector_store = ProviderFactory.get_vectorstore_provider()
        vector_store.add_chunks(chunks)
        
        doc_meta.embedded = True
        doc_meta.embedding_model = "bge-small-en-v1.5" # Default for now
        
        # 6. Save Metadata
        self._documents_cache[doc_meta.document_id] = doc_meta.model_dump()
        self._save_metadata()
        
        return doc_meta

from typing import List, Dict, Any
import uuid
# pyrefly: ignore [missing-import]
from langchain_text_splitters import RecursiveCharacterTextSplitter
from app.models.document import DocumentChunk

class Chunker:
    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200):
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            separators=["\n\n", "\n", ".", " ", ""]
        )
        
    def chunk_documents(self, documents: List[Dict[str, Any]], document_id: str, filename: str) -> List[DocumentChunk]:
        chunks = []
        
        for doc in documents:
            split_texts = self.splitter.split_text(doc["content"])
            
            for i, text in enumerate(split_texts):
                meta = doc["metadata"].copy()
                meta.update({
                    "document_id": document_id,
                    "filename": filename,
                    "chunk_index": i,
                    "chunk_length": len(text)
                })
                
                chunks.append(DocumentChunk(
                    chunk_id=str(uuid.uuid4()),
                    document_id=document_id,
                    content=text,
                    metadata=meta
                ))
                
        return chunks

from app.rag_engine.ingestion import IngestionPipeline
from app.models.document import DocumentMetadata
from typing import List

class RAGService:
    def __init__(self):
        self.ingestion = IngestionPipeline()
        
    def upload_document(self, file_content: bytes, filename: str, session_id: str = "default") -> DocumentMetadata:
        return self.ingestion.process_file(file_content, filename, session_id)
        
    def get_all_documents(self, session_id: str = "default") -> List[DocumentMetadata]:
        return self.ingestion.get_all_documents(session_id)
        
    def delete_document(self, document_id: str, session_id: str = "default"):
        self.ingestion.delete_document(document_id, session_id)

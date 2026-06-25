from app.rag_engine.ingestion import IngestionPipeline
from app.models.document import DocumentMetadata
from typing import List

class RAGService:
    def __init__(self):
        self.ingestion = IngestionPipeline()
        
    def upload_document(self, file_content: bytes, filename: str) -> DocumentMetadata:
        return self.ingestion.process_file(file_content, filename)
        
    def get_all_documents(self) -> List[DocumentMetadata]:
        return self.ingestion.get_all_documents()
        
    def delete_document(self, document_id: str):
        self.ingestion.delete_document(document_id)

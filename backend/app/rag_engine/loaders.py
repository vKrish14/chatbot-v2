import tempfile
import os
from typing import List, Dict, Any
# pyrefly: ignore [missing-import]
from langchain_community.document_loaders import PyMuPDFLoader, Docx2txtLoader, TextLoader, CSVLoader
from app.models.document import DocumentMetadata

class DocumentLoader:
    def load(self, file_content: bytes, filename: str) -> List[Dict[str, Any]]:
        _, ext = os.path.splitext(filename)
        ext = ext.lower()
        
        with tempfile.NamedTemporaryFile(delete=False, suffix=ext) as temp_file:
            temp_file.write(file_content)
            temp_path = temp_file.name

        try:
            if ext == '.pdf':
                loader = PyMuPDFLoader(temp_path)
            elif ext in ['.docx', '.doc']:
                loader = Docx2txtLoader(temp_path)
            elif ext == '.csv':
                loader = CSVLoader(temp_path)
            else: # assume text
                loader = TextLoader(temp_path)
                
            documents = loader.load()
            
            parsed_docs = []
            for doc in documents:
                parsed_docs.append({
                    "content": doc.page_content,
                    "metadata": {
                        "source": filename,
                        "page": doc.metadata.get("page", 0) + 1 # 1-indexed
                    }
                })
            return parsed_docs
        finally:
            os.remove(temp_path)

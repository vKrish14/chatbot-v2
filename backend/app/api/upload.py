from fastapi import APIRouter, HTTPException, UploadFile, File, Form, Query
from typing import List
from app.services.rag_service import RAGService
from app.models.document import DocumentMetadata

router = APIRouter()
rag_service = RAGService()

@router.post("/upload", response_model=DocumentMetadata)
async def upload_document(file: UploadFile = File(...), session_id: str = Form("default")):
    try:
        content = await file.read()
        return rag_service.upload_document(content, file.filename, session_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/documents", response_model=List[DocumentMetadata])
async def list_documents(session_id: str = Query("default")):
    return rag_service.get_all_documents(session_id)

@router.delete("/documents/{document_id}")
async def delete_document(document_id: str, session_id: str = Query("default")):
    rag_service.delete_document(document_id, session_id)
    return {"status": "success"}

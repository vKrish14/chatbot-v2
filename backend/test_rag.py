import asyncio
from app.services.rag_service import RAGService
from app.rag_engine.retriever import Retriever
import time

def main():
    rag = RAGService()
    print("Uploading document...")
    # create a dummy text file
    content = b"This is a document about Antigravity. It is a secret project to build flying cars."
    doc = rag.upload_document(content, "test.txt")
    print(f"Uploaded: {doc.filename} with {doc.chunk_count} chunks")
    
    print("Retrieving...")
    retriever = Retriever()
    sources = retriever.retrieve("summarize this")
    print(f"Sources found for 'summarize this': {len(sources)}")
    for s in sources:
        print(f" - {s.similarity}: {s.content}")
        
    sources = retriever.retrieve("antigravity flying cars")
    print(f"Sources found for 'antigravity': {len(sources)}")
    for s in sources:
        print(f" - {s.similarity}: {s.content}")

if __name__ == "__main__":
    main()

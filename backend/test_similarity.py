import asyncio
from app.rag_engine.retriever import Retriever

def main():
    retriever = Retriever()
    sources = retriever.retrieve("summarize", threshold=-1.0)
    print(f"Sources found for 'summarize': {len(sources)}")
    for s in sources:
        print(f" - {s.similarity}: {s.content[:50]}...")

if __name__ == "__main__":
    main()

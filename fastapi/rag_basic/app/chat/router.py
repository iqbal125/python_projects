"""
FastAPI router for RAG chat endpoints.
"""
from fastapi import APIRouter, HTTPException

from app.chat.schemas import ChatRequest, ChatResponse, DocumentInput, IngestResponse
from app.chat.graph import run_rag_query
from app.chat.vector_store import add_documents, get_document_count, clear_collection
from app.chat.llm import check_ollama_health

router = APIRouter(prefix="/chat", tags=["chat"])


@router.post("/query", response_model=ChatResponse)
async def query_rag(request: ChatRequest):
    """
    Query the RAG system with a question.
    Returns the answer along with retrieved context.
    """
    try:
        result = run_rag_query(request.query)
        return ChatResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/ingest", response_model=IngestResponse)
async def ingest_documents(documents: list[DocumentInput]):
    """
    Ingest documents into the vector store.
    """
    try:
        contents = [doc.content for doc in documents]
        metadatas = [doc.metadata or {} for doc in documents]
        
        count = add_documents(contents, metadatas)
        
        return IngestResponse(
            message=f"Successfully ingested {count} documents",
            document_count=get_document_count()
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/ingest/text")
async def ingest_text(text: str):
    """
    Simple endpoint to ingest a single text document.
    Splits text into chunks for better retrieval.
    """
    try:
        # Simple chunking by paragraphs or fixed size
        chunks = [chunk.strip() for chunk in text.split("\n\n") if chunk.strip()]
        
        if not chunks:
            chunks = [text[i:i+500] for i in range(0, len(text), 500)]
        
        count = add_documents(chunks)
        
        return {
            "message": f"Successfully ingested {count} chunks",
            "document_count": get_document_count()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/stats")
async def get_stats():
    """Get statistics about the RAG system."""
    return {
        "document_count": get_document_count(),
        "ollama_available": check_ollama_health()
    }


@router.delete("/clear")
async def clear_documents():
    """Clear all documents from the vector store."""
    try:
        clear_collection()
        return {"message": "All documents cleared", "document_count": 0}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/health")
async def health_check():
    """Check the health of the RAG system components."""
    ollama_ok = check_ollama_health()
    
    return {
        "status": "healthy" if ollama_ok else "degraded",
        "components": {
            "vector_store": "ok",
            "ollama": "ok" if ollama_ok else "unavailable"
        },
        "message": None if ollama_ok else "Ollama is not running. Start it with 'ollama serve'"
    }

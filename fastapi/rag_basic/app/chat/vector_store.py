"""
Vector store module using ChromaDB and sentence-transformers.
All open-source libraries.
"""
import chromadb
from chromadb.utils import embedding_functions
from typing import List


# Use sentence-transformers for embeddings (open-source)
EMBEDDING_MODEL = "all-MiniLM-L6-v2"

# Initialize ChromaDB client (persistent storage)
chroma_client = chromadb.PersistentClient(path="./chroma_db")

# Create embedding function using sentence-transformers
embedding_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name=EMBEDDING_MODEL
)

# Get or create collection
collection = chroma_client.get_or_create_collection(
    name="rag_documents",
    embedding_function=embedding_fn,
    metadata={"hnsw:space": "cosine"}
)


def add_documents(documents: List[str], metadatas: List[dict] | None = None) -> int:
    """Add documents to the vector store."""
    if not documents:
        return 0
    
    # Generate unique IDs for documents
    existing_count = collection.count()
    ids = [f"doc_{existing_count + i}" for i in range(len(documents))]
    
    # Add to collection
    collection.add(
        documents=documents,
        metadatas=metadatas or [{}] * len(documents),
        ids=ids
    )
    
    return len(documents)


def search_documents(query: str, k: int = 3) -> List[str]:
    """Search for relevant documents based on query."""
    if collection.count() == 0:
        return []
    
    results = collection.query(
        query_texts=[query],
        n_results=min(k, collection.count())
    )
    
    # Return the document texts
    return results["documents"][0] if results["documents"] else []


def get_document_count() -> int:
    """Get the number of documents in the store."""
    return collection.count()


def clear_collection():
    """Clear all documents from the collection."""
    global collection
    chroma_client.delete_collection("rag_documents")
    collection = chroma_client.get_or_create_collection(
        name="rag_documents",
        embedding_function=embedding_fn,
        metadata={"hnsw:space": "cosine"}
    )

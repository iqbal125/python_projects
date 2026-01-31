"""
LangGraph RAG workflow.
Defines the graph for retrieval-augmented generation.
"""
from typing import TypedDict, List, Annotated
from langgraph.graph import StateGraph, END

from app.chat.vector_store import search_documents
from app.chat.llm import generate_response


# Define the state schema
class RAGState(TypedDict):
    query: str
    context: Annotated[List[str], "Retrieved documents"]
    answer: str


# Node functions
def retrieve_node(state: RAGState) -> dict:
    """Retrieve relevant documents from vector store."""
    query = state["query"]
    documents = search_documents(query, k=3)
    return {"context": documents}


def generate_node(state: RAGState) -> dict:
    """Generate answer using LLM with retrieved context."""
    query = state["query"]
    context = state.get("context", [])
    answer = generate_response(query, context)
    return {"answer": answer}


# Build the graph
def create_rag_graph() -> StateGraph:
    """Create and compile the RAG workflow graph."""
    
    # Initialize the graph with state schema
    workflow = StateGraph(RAGState)
    
    # Add nodes
    workflow.add_node("retrieve", retrieve_node)
    workflow.add_node("generate", generate_node)
    
    # Define edges
    workflow.set_entry_point("retrieve")
    workflow.add_edge("retrieve", "generate")
    workflow.add_edge("generate", END)
    
    # Compile the graph
    return workflow.compile()


# Create singleton instance
rag_graph = create_rag_graph()


def run_rag_query(query: str) -> dict:
    """Run a RAG query through the graph."""
    initial_state = {
        "query": query,
        "context": [],
        "answer": ""
    }
    
    result = rag_graph.invoke(initial_state)
    
    return {
        "query": result["query"],
        "context": result["context"],
        "answer": result["answer"]
    }

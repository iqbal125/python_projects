from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from llama_index.llms.ollama import Ollama
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader

from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core import Settings


# Configure LlamaIndex to use local Ollama model
llm = Ollama(model="llama3", request_timeout=120.0)

Settings.llm = llm
Settings.embed_model = HuggingFaceEmbedding(
    model_name="BAAI/bge-small-en-v1.5"
)

# Load documents and create index at startup
documents = SimpleDirectoryReader("./app/chat/data").load_data()
index = VectorStoreIndex.from_documents(documents)

router = APIRouter(prefix="/llama", tags=["Llama Chat"])

@router.get("/chat")
async def chat(q: str):
    async def generate():
        response = llm.stream_complete(q)
        for chunk in response:
            if chunk.delta:
                yield chunk.delta

    return StreamingResponse(generate(), media_type="text/plain")


# RAG, basic Q&A, not chatbot style.
@router.get("/chat-rag")
def chat_rag(q: str):
    query_engine = index.as_query_engine(streaming=True)
    
    def generate():
        response = query_engine.query(q)
        for text in response.response_gen:  # type: ignore
            yield text
    
    return StreamingResponse(generate(), media_type="text/plain")
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


# //add metadata to documents
# ingestion pipeline

router = APIRouter(prefix="/ingest", tags=["Ingest"])
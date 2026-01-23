from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from llama_index.llms.ollama import Ollama

router = APIRouter(prefix="/llama", tags=["Llama Chat"])

llm = Ollama(model="llama3", request_timeout=120.0)


@router.get("/chat")
async def chat(q: str):
    async def generate():
        response = llm.stream_complete(q)
        for chunk in response:
            yield chunk.delta

    return StreamingResponse(generate(), media_type="text/plain")

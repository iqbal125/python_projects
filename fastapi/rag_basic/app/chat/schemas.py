from pydantic import BaseModel


class ChatRequest(BaseModel):
    query: str


class ChatResponse(BaseModel):
    query: str
    context: list[str]
    answer: str


class DocumentInput(BaseModel):
    content: str
    metadata: dict | None = None


class IngestResponse(BaseModel):
    message: str
    document_count: int

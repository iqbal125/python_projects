from fastapi import FastAPI
from app.globals.db import Base, engine
from app.todo.router import router as todo_router
from app.chat.router import router as chat_router
from sqlalchemy import inspect

app = FastAPI(title="RAG Basic API", description="A minimal RAG application using LangGraph")

@app.get("/ping")
async def root():
    return {"message": "Hello Pong!"}

Base.metadata.create_all(bind=engine)
print(inspect(engine).get_table_names())
app.include_router(todo_router)
app.include_router(chat_router)



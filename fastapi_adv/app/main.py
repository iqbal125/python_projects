from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.globals.db import Base, engine
from app.todo.router import router as todo_router
from app.fileUpload.router import router as upload_router
from app.llamaSimple.router import router as llama_router
from sqlalchemy import inspect

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/ping")
async def root():
    return {"message": "Hello Pong!"}

Base.metadata.create_all(bind=engine)
print(inspect(engine).get_table_names())
app.include_router(todo_router)
app.include_router(upload_router)
app.include_router(llama_router)



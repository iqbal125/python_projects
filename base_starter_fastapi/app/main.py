from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.globals.db import Base, engine
from app.todo.router import router as todo_router
from sqlalchemy import inspect

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
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



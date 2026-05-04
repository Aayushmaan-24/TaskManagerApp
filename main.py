from fastapi import FastAPI, Request, HTTPException
from src.utils.db import Base, engine
from src.tasks.models import TaskModel
from src.tasks.router import task_routes

Base.metadata.create_all(bind=engine)

app = FastAPI(title="TaskManager")

app.include_router(task_routes)

@app.get("/")
def home():
    return {
        "message": "Welcome to TaskManager API!"
    }

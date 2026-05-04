from fastapi import FastAPI, Request, HTTPException
from src.utils.db import Base, engine
from src.tasks.models import TaskModel

Base.metadata.create_all(bind=engine)

app = FastAPI(title="TaskManager")

@app.get("/")
def home():
    return {
        "message": "Welcome to TaskManager API!"
    }

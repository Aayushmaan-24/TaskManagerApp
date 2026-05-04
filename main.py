from fastapi import FastAPI, Request, HTTPException
from src.utils.db import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI(title="TaskManager")

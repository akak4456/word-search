from fastapi import FastAPI, Form
from pydantic import BaseModel
from typing import List
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
origins = [
    "http://127.0.0.1:5173",
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
class PuzzleCreate(BaseModel):
    title: str
    description: str
    words: List[str]

@app.post("/puzzles")
async def create_puzzle(data: PuzzleCreate):
    return data
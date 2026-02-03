from fastapi import FastAPI, Form
from pydantic import BaseModel
from typing import List
from fastapi.middleware.cors import CORSMiddleware
import sqlite3

con = sqlite3.connect("db.db",check_same_thread=False)
cur = con.cursor()

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
    
@app.get("/puzzles")
async def get_puzzles():
    cur.execute("""
        SELECT id, title, description
        FROM word_search_puzzle
    """)
    rows = cur.fetchall()

    puzzles = []
    for row in rows:
        puzzles.append({
            "id": row[0],
            "title": row[1],
            "description": row[2]
        })

    return puzzles

@app.get("/puzzles/{puzzle_id}")
async def get_puzzle(puzzle_id: int):
    cur.execute(
        """
        SELECT 
            p.id,
            p.title,
            p.description,
            w.word
        FROM word_search_puzzle p
        LEFT JOIN word_search_puzzle_list w
            ON p.id = w.puzzle_id
        WHERE p.id = ?
        """,
        (puzzle_id,)
    )

    rows = cur.fetchall()

    if not rows:
        return {"error": "Puzzle not found"}

    # 첫 row에서 기본 정보 추출
    puzzle_info = rows[0]

    words = [row[3] for row in rows if row[3] is not None]

    return {
        "id": puzzle_info[0],
        "title": puzzle_info[1],
        "description": puzzle_info[2],
        "words": words
    }

@app.post("/puzzles")
async def create_puzzle(data: PuzzleCreate):
    # 1️⃣ 퍼즐 기본 정보 저장
    cur.execute(
        """
        INSERT INTO word_search_puzzle (title, description)
        VALUES (?, ?)
        """,
        (data.title, data.description)
    )
    con.commit()

    # 2️⃣ 방금 생성된 퍼즐 id 가져오기
    puzzle_id = cur.lastrowid

    # 3️⃣ 단어 리스트 저장
    for word in data.words:
        cur.execute(
            """
            INSERT INTO word_search_puzzle_list (puzzle_id, word)
            VALUES (?, ?)
            """,
            (puzzle_id, word)
        )

    con.commit()
    return "200"
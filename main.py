from fastapi import FastAPI, Form, WebSocket, WebSocketDisconnect
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List
from fastapi.middleware.cors import CORSMiddleware
import sqlite3
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta

pwd_context = CryptContext(
    schemes=["argon2"],
    deprecated="auto"
)

SECRET_KEY = "super-secret"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

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
    
class UserCreate(BaseModel):
    id: str
    password: str

class UserLogin(BaseModel):
    id: str
    password: str
    
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

@app.post("/signup")
def signup(user: UserCreate):
    hashed_pw = hash_password(user.password)

    try:
        cur.execute(
            "INSERT INTO users (id, password) VALUES (?, ?)",
            (user.id, hashed_pw)
        )
        con.commit()
    except sqlite3.IntegrityError:
        return JSONResponse(
            status_code=400,
            content={"message": "이미 존재하는 아이디입니다."}
        )

    return {"message": "회원가입 완료"}

@app.get("/users/check-id/{id}")
def check_id(id: str):
    cur.execute("SELECT id FROM users WHERE id = ?", (id,))
    user = cur.fetchone()

    if user:
        return {"available": False}
    return {"available": True}

@app.post("/login")
def login(user: UserLogin):
    cur.execute("SELECT * FROM users WHERE id = ?", (user.id,))
    db_user = cur.fetchone()

    if not db_user:
        return JSONResponse(status_code=400, content={"message": "존재하지 않는 사용자"})

    if not verify_password(user.password, db_user[1]):
        return JSONResponse(status_code=400, content={"message": "비밀번호 오류"})

    access_token = create_access_token({"sub": user.id})

    return {"access_token": access_token}

class ConnectionManager:
    def __init__(self):
        # puzzle_id 별로 관리
        self.rooms: Dict[str, List[WebSocket]] = {}
        self.user_states: Dict[str, Dict[str, dict]] = {}
        # 구조:
        # {
        #   "1": {
        #        "userA": { mappedWord: [...], elapsedTime: 10 }
        #   }
        # }

    async def connect(self, puzzle_id: str, user_id: str, websocket: WebSocket):
        await websocket.accept()

        if puzzle_id not in self.rooms:
            self.rooms[puzzle_id] = []
            self.user_states[puzzle_id] = {}

        self.rooms[puzzle_id].append(websocket)

        self.user_states[puzzle_id][user_id] = {
            "mappedWord": [],
            "elapsedTime": 0
        }

    def disconnect(self, puzzle_id: str, user_id: str, websocket: WebSocket):
        self.rooms[puzzle_id].remove(websocket)
        del self.user_states[puzzle_id][user_id]

    async def broadcast(self, puzzle_id: str):
        for connection in self.rooms[puzzle_id]:
            await connection.send_json(self.user_states[puzzle_id])


manager = ConnectionManager()

@app.websocket("/ws/{puzzle_id}/{user_id}")
async def websocket_endpoint(websocket: WebSocket, puzzle_id: str, user_id: str):
    await manager.connect(puzzle_id, user_id, websocket)

    try:
        while True:
            data = await websocket.receive_json()

            # 클라이언트가 보낸 상태 업데이트
            manager.user_states[puzzle_id][user_id] = data

            # 모든 유저에게 broadcast
            await manager.broadcast(puzzle_id)

    except WebSocketDisconnect:
        manager.disconnect(puzzle_id, user_id, websocket)
        await manager.broadcast(puzzle_id)
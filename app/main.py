from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Literal

from .rag import generate_answer


BASE_DIR = Path(__file__).resolve().parent.parent
FRONTEND_DIR = BASE_DIR / "frontend"
INDEX_FILE = FRONTEND_DIR / "index.html"

app = FastAPI(title="Pathsetter Alfred Chatbot", version="0.3.0")

# Serve frontend static files from the `frontend` folder at /static
if FRONTEND_DIR.exists():
    app.mount("/static", StaticFiles(directory=str(FRONTEND_DIR)), name="static")

# Allow CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --- DATA MODELS ---
class Message(BaseModel):
    role: Literal["user", "assistant", "system"]
    content: str


class ChatRequest(BaseModel):
    messages: List[Message]


class ChatResponse(BaseModel):
    answer: str


# --- ROUTES ---
@app.get("/", response_class=HTMLResponse)
async def get_ui():
    """Serves the Chat UI when you open the URL in browser"""
    if INDEX_FILE.exists():
        return FileResponse(str(INDEX_FILE))
    return HTMLResponse("<h1>Frontend not found</h1>", status_code=404)


@app.post("/chat", response_model=ChatResponse)
async def chat(req: ChatRequest):
    try:
        # Convert to dict and force lowercase roles
        msgs_dict = [
            {"role": m.role.lower(), "content": m.content}
            for m in req.messages
        ]
        answer, _ = generate_answer(msgs_dict)
        return ChatResponse(answer=answer)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

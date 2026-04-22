from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from backend.retriever import retrieve
from backend.chat import ask_groq

router = APIRouter()

class Message(BaseModel):
    role: str
    content: str

class AskRequest(BaseModel):
    question: str
    history: list[Message] = []

@router.post("/ask")
async def ask(body: AskRequest):
    if not body.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty")

    try:
        chunks = retrieve(body.question)
    except Exception:
        raise HTTPException(
            status_code=404,
            detail="No index found. Upload a PDF first."
        )

    answer = ask_groq(body.question, chunks, body.history)
    return {
        "answer": answer,
        "sources": [c[:200] + "..." for c in chunks]
    }
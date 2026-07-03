from fastapi import APIRouter
from pydantic import BaseModel

from rag.W1.chatbot import ask_chatbot

router = APIRouter()

class ChatRequest(BaseModel):
    question: str

@router.post("/chat")
def chat(req: ChatRequest):

    answer = ask_chatbot(req.question)

    return {
        "answer": answer
    }
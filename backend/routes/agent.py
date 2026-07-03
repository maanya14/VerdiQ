from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from rag.W4.Crew import run_legal_crew

router = APIRouter()


class AgentRequest(BaseModel):
    question: str


@router.post("/agent/ask")
def ask_agent(req: AgentRequest):
    try:
        result = run_legal_crew(req.question)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Agent pipeline failed: {e}")

    return {"result": result}

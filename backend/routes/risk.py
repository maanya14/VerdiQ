from fastapi import APIRouter
from pydantic import BaseModel

from rag.W3.risk_analyzer import analyze_clause

router = APIRouter()


class RiskRequest(BaseModel):
    clause: str


@router.post("/risk/analyze")
def analyze_risk(req: RiskRequest):
    result = analyze_clause(req.clause)
    return {"analysis": result}

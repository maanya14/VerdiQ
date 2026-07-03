import shutil
import tempfile
from pathlib import Path

from fastapi import APIRouter, UploadFile, File, HTTPException

from rag.W2.clause_extractor import extract_clauses

router = APIRouter()


@router.post("/clause/extract")
async def extract_clause(file: UploadFile = File(...)):
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")

    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir) / file.filename
        with open(tmp_path, "wb") as f:
            shutil.copyfileobj(file.file, f)

        try:
            clauses = extract_clauses(str(tmp_path))
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Clause extraction failed: {e}")

    return {"clauses": clauses}

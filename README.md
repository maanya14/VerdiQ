# JurístiQ — Legal AI Chatbot

FastAPI backend (RAG + CrewAI) with a React + Tailwind frontend.

## What changed in this pass

The backend had several breaking issues that were fixed so it actually runs:

- `app,py` → renamed to `app.py`.
- `routes/risk.py`, `routes/clause.py`, `routes/agent.py` were empty (the app
  would crash on import) — implemented all three.
- `rag/W1/chatbot.py` was a CLI input-loop script with no `ask_chatbot`
  function (which `routes/chat.py` already called) — refactored into a
  proper function.
- `rag/W2/clause_extractor.py` and `rag/W3/risk_analyzer.py` were one-off
  scripts with hardcoded paths — refactored into `extract_clauses(pdf_path)`
  and `analyze_clause(clause)` functions.
- Broken relative imports fixed throughout `rag/W2`, `rag/W3`, `rag/W4`
  (e.g. `from schemas import ...` → `from rag.W2.schemas import ...`) so the
  package imports correctly regardless of the working directory.
- `rag/W4/Crew.py` now exposes `run_legal_crew(question)` for the route to
  call.
- `requirements.txt` cleaned up (removed the nonexistent `crew` and
  built-in `typing` packages; added `python-multipart`, `python-dotenv`,
  `langchain-text-splitters`).
- Added a `/health` endpoint and confirmed all five routes register
  correctly via a mocked import test.

⚠️ **Your `.env` file has a live Google API key in it.** Rotate that key in
Google AI Studio / Cloud Console — it was sitting in plaintext in the zip
you uploaded, and `.env` is now gitignored so a fresh key won't get
committed by accident.

## Backend

```bash
cd backend
python -m venv venv && source venv/bin/activate   # optional but recommended
pip install -r requirements.txt
uvicorn app:app --reload --port 8000
```

Runs at `http://localhost:8000`. Interactive docs at `/docs`.

Endpoints:
| Method | Path             | Body                          | Description |
|--------|------------------|--------------------------------|--------------|
| GET    | `/health`        | —                              | Liveness check |
| POST   | `/chat`          | `{ "question": string }`       | General legal Q&A (RAG over `vectordb/`) |
| POST   | `/clause/extract`| `multipart/form-data` file (PDF) | Extracts termination/payment/arbitration/confidentiality/governing-law clauses |
| POST   | `/risk/analyze`  | `{ "clause": string }`         | Rates a clause's risk against `legal_db/` |
| POST   | `/agent/ask`     | `{ "question": string }`       | Runs the 3-agent CrewAI pipeline (clause → risk → advisor). Slow. |

Note: `vectordb/` and `legal_db/` already contain ingested embeddings, so
no re-ingestion is needed to run the API.

## Frontend

```bash
cd frontend
npm install
npm run dev
```

Runs at `http://localhost:5173` and talks to the backend at
`http://localhost:8000` by default (see `.env.example` — copy to `.env` to
change it).

Four tabs, one per backend feature: **General Counsel** (chat), **Clause
Extraction** (PDF upload), **Risk Assessment** (single clause), and **Full
Case Review** (the CrewAI pipeline).

## Known limitations worth knowing about

- `/agent/ask` can be slow (three sequential LLM-backed agents) — there's
  no streaming, so the UI just shows a loading state until it resolves.
- The risk analyzer prompts the model for raw JSON; if the model doesn't
  return clean JSON, the API falls back to `{ "raw_response": "..." }` and
  the frontend renders that as plain text instead of the structured
  risk-level/explanation/citation view.
- No auth on any endpoint — fine for local dev, not for deploying as-is.

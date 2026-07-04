# JurístiQ — Legal AI Chatbot

## What this is

JurístiQ is a legal-assistant web app focused on Indian law. It combines a
retrieval-augmented FastAPI backend with a React frontend, and covers four
distinct use cases:

- **General Counsel** — ask a plain-language legal question and get an
  answer grounded in an indexed library of legal reference material (RAG
  over a Chroma vector store), instead of an unsourced LLM guess.
- **Clause Extraction** — upload a contract PDF and get back its key
  clauses (termination, payment, arbitration, confidentiality, governing
  law) pulled out automatically.
- **Risk Assessment** — paste a single clause and get a risk rating
  (low/medium/high) with an explanation, checked against a separate indexed
  statute library.
- **Full Case Review** — a multi-agent pipeline (via CrewAI) that runs
  clause analysis, risk analysis, and an advisory agent in sequence to
  produce one combined report for a question or clause.

It's a two-part project: a FastAPI backend that does the actual LLM/RAG
work, and a React + Tailwind frontend (one tab per feature above) that
talks to it over a small JSON/multipart API.

**This is educational/informational tooling, not legal advice** — the app
says as much in its footer.

## Design

The UI uses a dark, paper-and-ink palette:
`#000000` (background), `#1F150C` (panels), `#412D15` (borders/cards),
`#E1DCC9` (text/accents) — folder-tab navigation across the four features,
serif headings, monospace labels for a "case file" feel.

The layout is responsive down to phone widths: the tab bar scrolls
horizontally instead of wrapping/squishing, content is capped at a
readable max-width on large screens, buttons and form fields go full-width
on small screens, and inputs use a 16px base font so iOS Safari doesn't
zoom in on focus.

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

### Troubleshooting: NumPy crash on startup

If uvicorn crashes on import with `A module that was compiled using NumPy
1.x cannot be run in NumPy 2.x`, it's a version conflict between NumPy 2.x
and the `sentence-transformers`/`torch` build used for embeddings — not an
app bug. Fix:

```bash
pip install "numpy<2"
```

This is already pinned in `requirements.txt`; the error only shows up if
NumPy 2.x got installed into the environment before that pin was added.

## Frontend

```bash
cd frontend
npm install
npm run dev
```

Runs at `http://localhost:5173` and talks to the backend at
`http://localhost:8000` by default (see `.env.example` — copy to `.env` to
point it elsewhere).

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

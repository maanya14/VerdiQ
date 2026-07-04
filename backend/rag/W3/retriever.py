from pathlib import Path
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

BACKEND_ROOT = Path(__file__).resolve().parents[2]
LEGAL_DB_PATH = str(BACKEND_ROOT / "legal_db")

_embedding = None
_db = None
_retriever = None


def get_retriever():
    global _embedding, _db, _retriever

    if _retriever is None:
        _embedding = HuggingFaceEmbeddings(
            model_name="BAAI/bge-small-en-v1.5"
        )

        _db = Chroma(
            persist_directory=LEGAL_DB_PATH,
            embedding_function=_embedding
        )

        _retriever = _db.as_retriever(
            search_kwargs={"k": 3}
        )

    return _retriever
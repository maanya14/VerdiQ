from pathlib import Path

from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

BACKEND_ROOT = Path(__file__).resolve().parents[2]
LEGAL_DB_PATH = str(BACKEND_ROOT / "legal_db")

embedding = HuggingFaceEmbeddings(
    model_name="BAAI/bge-small-en-v1.5"
)

db = Chroma(
    persist_directory=LEGAL_DB_PATH,
    embedding_function=embedding
)

retriever = db.as_retriever(
    search_kwargs={"k": 3}
)
from pathlib import Path

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

BACKEND_ROOT = Path(__file__).resolve().parents[2]
pdf_path = str(BACKEND_ROOT / "data" / "Contract Act.pdf")
persist_dir = str(BACKEND_ROOT / "legal_db")

loader = PyPDFLoader(pdf_path)
documents = loader.load()
print("Pages loaded:", len(documents))

# Larger chunks + bigger overlap + sentence-aware separators, so each
# chunk is much less likely to start/end mid-sentence. Fragments that get
# cut mid-word/mid-clause are what make citations built from this context
# look truncated downstream.
splitter = RecursiveCharacterTextSplitter(
    chunk_size=900,
    chunk_overlap=150,
    separators=["\n\n", "\n", ". ", " ", ""]
)

chunks = splitter.split_documents(documents)
print("Chunks:", len(chunks))

embeddings = HuggingFaceEmbeddings(
    model_name="BAAI/bge-small-en-v1.5"
)
print(chunks[0].page_content[:200])

db = Chroma.from_documents(
    documents=chunks,
    embedding=embeddings,
    persist_directory=persist_dir
)

print("Legal database created at", persist_dir)
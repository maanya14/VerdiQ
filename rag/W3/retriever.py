from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

embedding = HuggingFaceEmbeddings(
    model_name="BAAI/bge-small-en-v1.5"
)

db = Chroma(
    persist_directory="../../legal_db",
    embedding_function=embedding
)

retriever = db.as_retriever(
    search_kwargs={"k": 3}
)
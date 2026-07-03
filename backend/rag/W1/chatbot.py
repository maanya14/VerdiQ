import os
from pathlib import Path

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_core.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI

from dotenv import load_dotenv
load_dotenv()

# Resolve path relative to this file so it works no matter what
# directory uvicorn/pytest is launched from.
BACKEND_ROOT = Path(__file__).resolve().parents[2]
VECTOR_DB_PATH = str(BACKEND_ROOT / "vectordb")

_embeddings = None
_vectorstore = None
_retriever = None
_llm = None

_prompt_template = PromptTemplate(
    input_variables=["context", "question"],
    template="""
    You are an Indian Legal Assistant.
    Use ONLY the provided context to answer.
    Context:{context}
    Question:{question}
    Answer:

    """
)


def _get_retriever():
    global _embeddings, _vectorstore, _retriever
    if _retriever is None:
        _embeddings = HuggingFaceEmbeddings(model_name="BAAI/bge-small-en-v1.5")
        _vectorstore = Chroma(
            persist_directory=VECTOR_DB_PATH,
            embedding_function=_embeddings
        )
        _retriever = _vectorstore.as_retriever(search_kwargs={"k": 3})
    return _retriever


def _get_llm():
    global _llm
    if _llm is None:
        _llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0)
    return _llm


def ask_chatbot(question: str) -> str:
    """Answer a general legal question using the RAG vector store."""
    retriever = _get_retriever()
    llm = _get_llm()

    docs = retriever.invoke(question)
    context = "\n\n".join(doc.page_content for doc in docs)

    final_prompt = _prompt_template.format(context=context, question=question)
    response = llm.invoke(final_prompt)

    return response.content

from langchain_community.document_loaders import PyPDFLoader
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

from rag.W2.parser import parser
from rag.W2.prompts import CLAUSE_EXTRACTION_PROMPT

load_dotenv()

_llm = None


def _get_llm():
    global _llm
    if _llm is None:
        _llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0)
    return _llm


def extract_clauses(pdf_path: str) -> dict:
    """Extract key clauses from a contract PDF and return them as a dict."""
    loader = PyPDFLoader(pdf_path)
    docs = loader.load()

    contract_text = "\n\n".join(doc.page_content for doc in docs)

    prompt = CLAUSE_EXTRACTION_PROMPT.format(
        contract_text=contract_text,
        format_instructions=parser.get_format_instructions()
    )

    response = _get_llm().invoke(prompt)
    result = parser.parse(response.content)

    return result.model_dump()

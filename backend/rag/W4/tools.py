from crewai.tools import tool
import sys
from pathlib import Path

# Add W3 to path so we can import retriever
#sys.path.insert(0, str(Path(__file__).parent.parent / "W3"))
from rag.W3.retriever import retriever

@tool("Legal Document Search")
def legal_search(query: str) -> str:
    """
    Searches the legal knowledge base and returns
    the most relevant sections.
    """

    docs = retriever.invoke(query)

    if not docs:
        return "No relevant legal information found."

    return "\n\n".join(doc.page_content for doc in docs)
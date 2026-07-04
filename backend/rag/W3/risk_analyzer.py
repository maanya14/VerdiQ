import json
import re

from rag.W3.retriever import get_retriever
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate

from dotenv import load_dotenv
load_dotenv()

_llm = None

def get_llm():
    global _llm
    if _llm is None:
        _llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            temperature=0
        )
    return _llm
prompt = PromptTemplate(
    template="""
You are a legal risk analyst.

Clause:
{clause}

Relevant Law:
{law}

Determine:

1. Risk Level (Low/Medium/High)
2. Explanation
3. Legal Citation

""",
    input_variables=["clause", "law"]
)

def analyze_clause(clause):

    docs = get_retriever().invoke(clause)

    law_text = "\n".join(
        [doc.page_content for doc in docs]
    )

    final_prompt = prompt.format(
        clause=clause,
        law=law_text
    )

    result = get_llm().invoke(final_prompt)
    raw = result.content.strip()

    # The model is asked for JSON only, but sometimes wraps it in a
    # markdown code fence -- strip that before parsing.
    cleaned = re.sub(r"^```(json)?|```$", "", raw, flags=re.MULTILINE).strip()

    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        # Fall back to returning the raw text so the caller still
        # gets something useful instead of a hard failure.
        return {"raw_response": raw}
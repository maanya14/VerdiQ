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
You are a legal risk analyst reviewing Indian contracts.

Clause:
{clause}

Relevant Law (retrieved excerpts -- these may begin or end mid-sentence
because they are fragments of a larger document; never copy them
word-for-word):
{law}

Analyze the clause and respond with ONLY a JSON object, no markdown code
fences, no commentary before or after it, in exactly this shape:

{{
  "risk_level": "Low" | "Medium" | "High",
  "explanation": "2-4 complete, well-formed sentences in your own words explaining the risk.",
  "legal_citation": "The Act name and section number this relates to, written as a full clean reference (e.g. 'Section 108(m), Transfer of Property Act, 1882'), not a copied sentence fragment."
}}

Rules:
- Write in full, grammatically complete sentences. Never end a sentence
  mid-word or mid-clause.
- Paraphrase and summarize the relevant law in your own words -- do not
  quote the excerpts directly, since they are truncated at chunk
  boundaries and quoting them verbatim will reproduce that truncation.
- If the excerpts don't name a specific section clearly, give the most
  relevant Act/topic you can identify instead of an incomplete citation.
- Output must be valid, parseable JSON and nothing else.
""",
    input_variables=["clause", "law"]
)

def analyze_clause(clause):

    docs = get_retriever().invoke(clause)

    law_text = "\n\n---\n\n".join(
        [doc.page_content.strip() for doc in docs]
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
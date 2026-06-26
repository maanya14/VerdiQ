from retriever import retriever
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate

from dotenv import load_dotenv
load_dotenv()

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0
)
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

Return JSON only.
""",
    input_variables=["clause", "law"]
)

def analyze_clause(clause):

    docs = retriever.invoke(clause)

    law_text = "\n".join(
        [doc.page_content for doc in docs]
    )

    final_prompt = prompt.format(
        clause=clause,
        law=law_text
    )

    result = llm.invoke(final_prompt)

    return result.content
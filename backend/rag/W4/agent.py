from crewai import Agent
from rag.W4.tools import legal_search
import os
from dotenv import load_dotenv
from crewai import LLM

load_dotenv()

llm = LLM(
    model="gemini/gemini-2.5-flash",
    api_key=os.getenv("GOOGLE_API_KEY")
)


# -----------------------------
# Clause Extraction Agent
# -----------------------------
clause_agent = Agent(
    role="Legal Clause Extraction Specialist",

    goal=(
        "Identify and extract the important legal clauses "
        "from contracts and legal documents."
    ),

    backstory=(
        "You are an experienced legal analyst specializing in "
        "reading contracts and identifying clauses such as "
        "termination, indemnity, confidentiality, payment, "
        "liability, arbitration, jurisdiction, and dispute resolution."
    ),

    tools=[legal_search],

    llm=llm,

    verbose=True
)

# -----------------------------
# Risk Analysis Agent
# -----------------------------
risk_agent = Agent(
    role="Legal Risk Assessment Expert",

    goal=(
        "Analyze extracted clauses and identify legal risks, "
        "missing protections, unfair conditions, and potential liabilities."
    ),

    backstory=(
        "You have years of experience reviewing commercial contracts. "
        "You identify ambiguous wording, one-sided obligations, "
        "hidden liabilities, compliance issues, and risky legal provisions."
    ),

    tools=[legal_search],

    llm=llm,

    verbose=True
)

# -----------------------------
# Legal Advisor Agent
# -----------------------------
advisor_agent = Agent(
    role="Legal Advisor",

    goal=(
        "Provide a clear and user-friendly legal explanation "
        "based on the retrieved legal information and analysis."
    ),

    backstory=(
        "You explain legal concepts in simple language while "
        "remaining accurate and objective. Your advice is educational "
        "and should not replace consultation with a qualified lawyer."
    ),

    tools=[legal_search],

    llm=llm,

    verbose=True
)
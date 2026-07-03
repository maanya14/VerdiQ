from crewai import Task
from rag.W4.agent import clause_agent, risk_agent, advisor_agent

# -----------------------------
# Clause Extraction Task
# -----------------------------
clause_task = Task(
    description="""
    You MUST use the Legal Search tool before answering.
    Search the legal database using the user's query:

    {question}

    Search the legal knowledge base using the available tool.
    Identify and extract the important legal clauses relevant to
    the user's query.

    Focus on clauses such as:
    - Definitions
    - Rights and Duties
    - Payment
    - Termination
    - Indemnity
    - Liability
    - Confidentiality
    - Arbitration
    - Jurisdiction
    """,

    expected_output="""
    A structured list of the important legal clauses relevant to
    the user's query along with a short explanation of each.
    """,

    agent=clause_agent
)

# -----------------------------
# Risk Analysis Task
# -----------------------------
risk_task = Task(
    description="""
    Analyze the user's legal query:

    {question}

    Using the retrieved legal information,
    identify possible legal risks, ambiguous wording,
    missing protections, unfair conditions,
    and legal liabilities.

    Explain why each issue may create legal problems.
    """,

    expected_output="""
    A detailed legal risk report including:

    - Identified risks
    - Severity (Low / Medium / High)
    - Explanation of each risk
    - Possible legal consequences
    """,

    agent=risk_agent,
    context=[clause_task]
)

# -----------------------------
# Legal Advice Task
# -----------------------------
advisor_task = Task(
    description="""
    Using the legal information retrieved from the knowledge base
    and the previous analysis, answer the user's question:

    {question}

    Produce a clear, well-structured legal explanation.

    Summarize the important clauses,
    explain the risks,
    and provide practical recommendations.

    Keep the explanation easy to understand.
    """,

    expected_output="""
    A final legal report containing:

    1. Summary
    2. Important Clauses
    3. Legal Risks
    4. Recommendations
    5. Final Answer
    """,

    agent=advisor_agent,
    context=[clause_task,risk_task]
)
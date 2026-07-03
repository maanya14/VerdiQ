from crewai import Crew, Process

from rag.W4.agent import (
    clause_agent,
    risk_agent,
    advisor_agent
)

from rag.W4.task import (
    clause_task,
    risk_task,
    advisor_task
)

legal_crew = Crew(
    agents=[
        clause_agent,
        risk_agent,
        advisor_agent
    ],

    tasks=[
        clause_task,
        risk_task,
        advisor_task
    ],

    process=Process.sequential,

    verbose=True
)


def run_legal_crew(question: str) -> str:
    """Kick off the multi-agent legal analysis pipeline for a question."""
    result = legal_crew.kickoff(inputs={"question": question})
    return str(result)
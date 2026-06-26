from crewai import Crew, Process

from agent import (
    clause_agent,
    risk_agent,
    advisor_agent
)

from task import (
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
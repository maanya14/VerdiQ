from rag.W2.parser import parser

CLAUSE_EXTRACTION_PROMPT = f"""
You are a legal contract analyst.

Extract the following clauses:

- termination_clause
- payment_clause
- arbitration_clause
- confidentiality_clause
- governing_law

{{format_instructions}}

Contract:

{{contract_text}}
"""

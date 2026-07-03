from risk_analyzer import analyze_clause

clause = """
Landlord may terminate tenancy
without notice and remove tenant.
"""

response = analyze_clause(clause)

print(response)
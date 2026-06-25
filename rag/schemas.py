from pydantic import BaseModel
from typing import Optional

class ContractClause(BaseModel):
    termination_clause: Optional[str] = None
    payment_clause: Optional[str] = None
    arbitration_clause: Optional[str] = None
    confidentiality_clause: Optional[str] = None
    governing_law_clause: Optional[str] = None
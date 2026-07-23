from typing import List, Dict, Any, Optional
from pydantic import BaseModel, ConfigDict

class TBSRowInput(BaseModel):
    account: str
    debit: Optional[float] = 0.0
    credit: Optional[float] = 0.0

class TBSSubmission(BaseModel):
    rows: List[TBSRowInput]

class TBSScenarioResponse(BaseModel):
    id: int
    code: str
    title: str
    exhibit_html: str
    accounts_list: List[str]

    model_config = ConfigDict(from_attributes=True)

class TBSSubmissionResult(BaseModel):
    score: float
    is_balanced: bool
    total_debits: float
    total_credits: float
    passed: bool
    feedback_html: str

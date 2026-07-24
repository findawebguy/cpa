from typing import List, Dict, Any, Optional, Union
from pydantic import BaseModel, ConfigDict, field_validator

class TBSRowInput(BaseModel):
    account: str
    debit: Optional[Union[float, str]] = 0.0
    credit: Optional[Union[float, str]] = 0.0

    @field_validator('debit', 'credit', mode='before')
    @classmethod
    def parse_float_value(cls, v: Any) -> float:
        if v is None or v == "":
            return 0.0
        try:
            return float(v)
        except (ValueError, TypeError):
            return 0.0

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

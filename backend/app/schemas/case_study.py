from pydantic import BaseModel
from typing import List, Optional, Dict, Any

class CaseQuestionBase(BaseModel):
    question_text: str
    options_json: List[dict]
    explanation_html: str

class CaseQuestionResponse(CaseQuestionBase):
    id: int
    case_study_id: int

    class Config:
        from_attributes = True

class CaseStudyBase(BaseModel):
    title: str
    description: Optional[str]
    scenario_text: str
    exhibits_html: Optional[str]

class CaseStudyResponse(CaseStudyBase):
    id: int
    course_id: int
    questions: List[CaseQuestionResponse]

    class Config:
        from_attributes = True

class CaseStudySubmitRequest(BaseModel):
    answers: dict[int, int]  # map of question_id -> selected_option_index

class CaseStudySubmitResponse(BaseModel):
    score: float
    results: dict[int, dict]  # map of question_id -> {"is_correct": bool, "correct_idx": int}
    message: str

class LiveNewsIngestionRequest(BaseModel):
    raw_feed: Optional[Dict[str, Any]] = None
    api_key: Optional[str] = ""


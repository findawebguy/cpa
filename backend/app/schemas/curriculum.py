from typing import Optional, List, Any, Dict
from pydantic import BaseModel, ConfigDict

class OptionPublic(BaseModel):
    text: str

class OptionSubmit(BaseModel):
    index: int
    confidence: str = "medium"  # "low", "medium", "high"

class LearningNodeResponse(BaseModel):
    id: int
    node_key: str
    concept_name: str
    node_type: str  # "question", "remediation", "end"
    scenario_content: Optional[str] = None
    question_text: Optional[str] = None
    options: List[OptionPublic] = []
    remediation_html: Optional[str] = None
    has_interactive_tool: bool = False
    tool_type: Optional[str] = None
    next_node_key: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)

class NodeSubmissionResult(BaseModel):
    is_correct: bool
    explanation: str
    next_node_key: str
    mastery_delta: float
    current_mastery: float
    confidence_evaluated: str
    remediation_title: Optional[str] = None
    remediation_html: Optional[str] = None

class SyllabusWeekResponse(BaseModel):
    id: int
    week_number: int
    title: str
    node_count: int
    question_count: int = 0
    remediation_count: int = 0
    status: str  # "completed", "in-progress", "unlocked", "locked"
    start_node_key: Optional[str] = None

class CourseResponse(BaseModel):
    id: int
    code: str  # FAR, AUD, REG
    title: str
    description: Optional[str] = None
    total_weeks: int
    mastery_percent: float

    model_config = ConfigDict(from_attributes=True)

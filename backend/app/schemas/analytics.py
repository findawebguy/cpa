from typing import List, Dict
from pydantic import BaseModel

class DomainMasteryItem(BaseModel):
    domain: str
    score: float

class AnalyticsDiagnosticsResponse(BaseModel):
    readiness_index: float
    total_attempted: int
    accuracy_percent: float
    confidence_calibration: str  # "High", "Calibrated", "Overconfident"
    estimated_study_hours: float
    mastery_heatmap: List[DomainMasteryItem]
    insights: List[Dict[str, str]]

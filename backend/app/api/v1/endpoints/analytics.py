from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.app.db.session import get_db
from backend.app.models.user import User
from backend.app.models.curriculum import UserProgress, LearningNode, Syllabus, Course
from backend.app.models.simulation import TBSAttempt
from backend.app.schemas.analytics import AnalyticsDiagnosticsResponse, DomainMasteryItem
from backend.app.api.v1.endpoints.auth import get_current_user

router = APIRouter()

@router.get("/analytics/diagnostics", response_model=AnalyticsDiagnosticsResponse)
def get_analytics_diagnostics(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    progresses = db.query(UserProgress).filter(UserProgress.user_id == current_user.id).all()
    tbs_attempts = db.query(TBSAttempt).filter(TBSAttempt.user_id == current_user.id).all()

    total_attempted = len(progresses)
    avg_mastery = round(sum(p.mastery_level for p in progresses) / len(progresses), 1) if progresses else 0.0
    readiness = round(avg_mastery * 0.95, 1) if total_attempted > 0 else 0.0
    study_hours = round(total_attempted * 0.15 + len(tbs_attempts) * 0.5, 1)

    if total_attempted == 0:
        conf_calib = "Not Calibrated Yet"
    elif any(p.confidence_rating == "high" and p.mastery_level < 50 for p in progresses):
        conf_calib = "Overconfidence Detected"
    else:
        conf_calib = "Well-Calibrated"

    heatmap = [
        DomainMasteryItem(domain="Accounting Cycle", score=avg_mastery if total_attempted > 0 else 0.0),
        DomainMasteryItem(domain="Financial Prep", score=0.0),
        DomainMasteryItem(domain="ASC 606 Rev Rec", score=0.0),
        DomainMasteryItem(domain="Inventory & PPE", score=0.0),
        DomainMasteryItem(domain="ASC 842 Leases", score=0.0),
        DomainMasteryItem(domain="Consolidations", score=0.0)
    ]

    if total_attempted == 0:
        insights = [
            {
                "type": "info",
                "title": "Welcome, New Student!",
                "detail": "Complete your first adaptive module in Week 1 to generate personalized cognitive diagnostics and domain heatmaps."
            },
            {
                "type": "info",
                "title": "CPA Evolution 2026 Strategy",
                "detail": "Start with Week 1 (Accounting Cycle) in FAR before attempting Task-Based Simulations."
            }
        ]
    else:
        insights = [
            {
                "type": "success",
                "title": "Active Learning Path Underway",
                "detail": f"You have attempted {total_attempted} modules. Keep practicing to build exam readiness."
            },
            {
                "type": "info",
                "title": "CPA Evolution 2026 Tip",
                "detail": "Focus heavily on Data Analytics and Technology controls integrated within the AUD & FAR sections."
            }
        ]

    return AnalyticsDiagnosticsResponse(
        readiness_index=readiness,
        total_attempted=total_attempted,
        accuracy_percent=avg_mastery,
        confidence_calibration=conf_calib,
        estimated_study_hours=study_hours,
        mastery_heatmap=heatmap,
        insights=insights
    )

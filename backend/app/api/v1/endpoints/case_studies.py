from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from backend.app.db.session import get_db
from backend.app.api.v1.endpoints.auth import get_current_user
from backend.app.models.user import User
from backend.app.models.case_study import CaseStudy, CaseQuestion, CaseAttempt
from backend.app.models.curriculum import Course
from backend.app.schemas.case_study import CaseStudyResponse, CaseStudySubmitRequest, CaseStudySubmitResponse

router = APIRouter()

@router.get("/course/{course_code}", response_model=List[CaseStudyResponse])
def get_case_studies_by_course(
    course_code: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    course = db.query(Course).filter(Course.code == course_code.upper()).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
        
    case_studies = db.query(CaseStudy).filter(CaseStudy.course_id == course.id).all()
    return case_studies

@router.get("/{case_id}", response_model=CaseStudyResponse)
def get_case_study(
    case_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    case_study = db.query(CaseStudy).filter(CaseStudy.id == case_id).first()
    if not case_study:
        raise HTTPException(status_code=404, detail="Case study not found")
    return case_study

@router.post("/{case_id}/submit", response_model=CaseStudySubmitResponse)
def submit_case_study(
    case_id: int,
    request: CaseStudySubmitRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    case_study = db.query(CaseStudy).filter(CaseStudy.id == case_id).first()
    if not case_study:
        raise HTTPException(status_code=404, detail="Case study not found")

    results = {}
    correct_count = 0
    total_questions = len(case_study.questions)

    if total_questions == 0:
        raise HTTPException(status_code=400, detail="This case study has no questions.")

    for question in case_study.questions:
        selected_idx = request.answers.get(question.id)
        if selected_idx is None:
            selected_idx = -1 # Unanswered
            
        is_correct = (selected_idx == question.correct_answer_idx)
        if is_correct:
            correct_count += 1
            
        results[question.id] = {
            "is_correct": is_correct,
            "correct_idx": question.correct_answer_idx
        }

    score = (correct_count / total_questions) * 100.0

    # Save attempt
    attempt = CaseAttempt(
        user_id=current_user.id,
        case_study_id=case_id,
        submission_json=request.answers,
        score=score
    )
    db.add(attempt)
    db.commit()

    return CaseStudySubmitResponse(
        score=round(score, 1),
        passed=passed,
        message=f"Simulation score: {round(score, 1)}%. {'Passed!' if passed else 'Review explanations and retry.'}",
        results=results
    )


from backend.app.schemas.case_study import CaseStudyResponse, CaseStudySubmitRequest, CaseStudySubmitResponse, LiveNewsIngestionRequest

@router.post("/live-news/trigger-daily-ingestion")
def trigger_daily_live_news_ingestion(
    body: Optional[LiveNewsIngestionRequest] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Triggers the Senior Financial Analyst Agent (NVIDIA NIM)
    to review daily market news and insert into the database ONLY if approved.
    Enforces a strict 24-hour rate limit (once daily at most).
    """
    from backend.app.services.live_news_ingestion import LiveNewsIngestionService
    
    raw_feed = body.raw_feed if body and body.raw_feed else None
    api_key = body.api_key if body and body.api_key else ""
    
    if not raw_feed:
        raw_feed = {
            "title": "Federal Reserve Monetary Policy & Interest Rate Benchmarks Update",
            "summary": "Central bank interest rate decisions have increased discount rates used in fair value cash flow models across fixed income and commercial real estate sectors.",
            "url": "https://www.federalreserve.gov/monetarypolicy.htm",
            "published_at": "2026-07-24T00:00:00Z",
            "source": "Federal Reserve Press Release"
        }
    
    result = LiveNewsIngestionService.run_daily_agent_review_and_ingest(db, raw_feed, api_key=api_key)
    return result


@router.get("/live-news/llm-dataset-logs")
def get_llm_dataset_logs(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Returns collected LLM interaction datasets from the Senior Financial Analyst Agent for future model fine-tuning & dataset auditing.
    """
    from backend.app.models.agent_log import LLMAuditLog
    logs = db.query(LLMAuditLog).order_by(LLMAuditLog.timestamp.desc()).limit(100).all()
    return {
        "total_records": len(logs),
        "dataset": logs
    }


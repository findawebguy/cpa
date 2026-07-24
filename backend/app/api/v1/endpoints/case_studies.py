from typing import List
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
        score=score,
        results=results,
        message=f"You scored {score:.1f}% on this case study!"
    )

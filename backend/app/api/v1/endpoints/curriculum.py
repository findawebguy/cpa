from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.app.db.session import get_db
from backend.app.models.user import User
from backend.app.models.curriculum import Course, Syllabus, LearningNode, UserProgress
from backend.app.schemas.curriculum import CourseResponse, SyllabusWeekResponse, LearningNodeResponse, OptionPublic, OptionSubmit, NodeSubmissionResult
from backend.app.core.adaptive_engine import AdaptiveEngine
from backend.app.api.v1.endpoints.auth import get_current_user

router = APIRouter()

@router.get("/courses", response_model=List[CourseResponse])
def get_courses(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    courses = db.query(Course).all()
    results = []

    for c in courses:
        syllabi = db.query(Syllabus).filter(Syllabus.course_id == c.id).all()
        syllabus_ids = [s.id for s in syllabi]
        nodes = db.query(LearningNode).filter(LearningNode.syllabus_id.in_(syllabus_ids)).all() if syllabus_ids else []
        node_ids = [n.id for n in nodes]

        progresses = db.query(UserProgress).filter(
            UserProgress.user_id == current_user.id,
            UserProgress.node_id.in_(node_ids)
        ).all() if node_ids else []

        avg_mastery = (sum(p.mastery_level for p in progresses) / len(progresses)) if progresses else 0.0

        results.append(CourseResponse(
            id=c.id,
            code=c.code,
            title=c.title,
            description=c.description,
            total_weeks=len(syllabi),
            mastery_percent=round(avg_mastery, 1)
        ))
    return results

@router.get("/courses/{track_code}/syllabus", response_model=List[SyllabusWeekResponse])
def get_syllabus(track_code: str, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    course = db.query(Course).filter(Course.code == track_code.upper()).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course track not found")

    syllabi = db.query(Syllabus).filter(Syllabus.course_id == course.id).order_by(Syllabus.week_number).all()
    res = []
    for idx, s in enumerate(syllabi):
        node_count = db.query(LearningNode).filter(LearningNode.syllabus_id == s.id).count()
        status = "in-progress" if idx == 0 else "locked"
        res.append(SyllabusWeekResponse(
            id=s.id,
            week_number=s.week_number,
            title=s.title,
            node_count=node_count,
            status=status
        ))
    return res

@router.get("/nodes/{node_key}", response_model=LearningNodeResponse)
def get_node(node_key: str, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    node = db.query(LearningNode).filter(LearningNode.node_key == node_key).first()
    if not node:
        raise HTTPException(status_code=404, detail=f"Node key '{node_key}' not found")

    raw_options = node.options_json or []
    public_options = [OptionPublic(text=opt.get("text", "")) for opt in raw_options]

    has_tool = False
    tool_type = None
    if "balancer" in (node.concept_name or "").lower():
        has_tool = True
        tool_type = "equation_balancer"
    elif "prepaid" in (node.concept_name or "").lower() or "t-account" in (node.concept_name or "").lower():
        has_tool = True
        tool_type = "t_account_visualizer"

    return LearningNodeResponse(
        id=node.id,
        node_key=node.node_key,
        concept_name=node.concept_name,
        node_type=node.node_type,
        scenario_content=node.scenario_content,
        question_text=node.concept_name if node.node_type == "question" else None,
        options=public_options,
        remediation_html=node.remediation_html,
        has_interactive_tool=has_tool,
        tool_type=tool_type,
        next_node_key=node.next_correct_key
    )

@router.post("/nodes/{node_key}/submit", response_model=NodeSubmissionResult)
def submit_node_answer(
    node_key: str,
    body: OptionSubmit,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    node = db.query(LearningNode).filter(LearningNode.node_key == node_key).first()
    if not node:
        raise HTTPException(status_code=404, detail=f"Node key '{node_key}' not found")

    is_correct, explanation, next_key, delta, new_mastery, meta = AdaptiveEngine.evaluate_submission(
        db=db,
        user=current_user,
        node=node,
        selected_option_idx=body.index,
        confidence_level=body.confidence
    )

    return NodeSubmissionResult(
        is_correct=is_correct,
        explanation=explanation,
        next_node_key=next_key,
        mastery_delta=delta,
        current_mastery=new_mastery,
        confidence_evaluated=meta.get("evaluation_tag", "EVALUATED"),
        remediation_title=meta.get("remediation_title"),
        remediation_html=meta.get("remediation_html")
    )

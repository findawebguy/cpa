from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.app.db.session import get_db
from backend.app.models.user import User
from backend.app.models.curriculum import Course, Syllabus, LearningNode, UserProgress
from backend.app.models.simulation import TBSAttempt, TBSScenario
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
    
    # Get all nodes user has passed / mastered
    user_progresses = db.query(UserProgress).filter(UserProgress.user_id == current_user.id).all()
    mastered_node_ids = {p.node_id for p in user_progresses if p.mastery_level >= 60.0}
    attempted_node_ids = {p.node_id for p in user_progresses}

    # Check if user has passed TBS for this track (score >= 75%)
    tbs_passed = False
    passed_attempts = db.query(TBSAttempt).filter(TBSAttempt.user_id == current_user.id, TBSAttempt.score >= 75.0).first()
    if passed_attempts:
        tbs_passed = True

    res = []
    prev_week_completed = True  # Week 1 is unlocked by default

    for idx, s in enumerate(syllabi):
        nodes = db.query(LearningNode).filter(LearningNode.syllabus_id == s.id).order_by(LearningNode.id).all()
        node_count = len(nodes)
        first_node_key = nodes[0].node_key if nodes else None

        # Filter out remediation and end nodes to check core question nodes
        question_nodes = [n for n in nodes if n.node_type == "question"]
        end_nodes = [n for n in nodes if n.node_type == "end"]

        # A week is completed ONLY if the user has reached an "end" node for that week.
        # The end node UserProgress record is created via POST /nodes/{key}/visit.
        # Fallback: all question nodes mastered (mastery >= 60) OR TBS passed for week 1.
        end_node_reached = any(n.id in attempted_node_ids for n in end_nodes)
        all_questions_mastered = (len(question_nodes) > 0 and all(n.id in mastered_node_ids for n in question_nodes))

        is_completed = end_node_reached or all_questions_mastered or (s.week_number == 1 and tbs_passed)
        is_attempted = (len(nodes) > 0 and any(n.id in attempted_node_ids for n in nodes))

        if is_completed:
            status_str = "completed"
        elif is_attempted:
            status_str = "in-progress"
        elif prev_week_completed:
            status_str = "unlocked" if idx > 0 else "in-progress"
        else:
            status_str = "locked"

        # Sequential unlocking dependency: previous week MUST be completed to unlock next week
        prev_week_completed = is_completed

        # If week is locked, strip start_node_key so user cannot jump ahead
        node_key = first_node_key if status_str != "locked" else None

        res.append(SyllabusWeekResponse(
            id=s.id,
            week_number=s.week_number,
            title=s.title,
            node_count=node_count,
            status=status_str,
            start_node_key=node_key
        ))
    return res


@router.post("/nodes/{node_key}/visit")
def visit_node(
    node_key: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Record that a user visited a node (used for 'end' nodes to mark week completion)."""
    node = db.query(LearningNode).filter(LearningNode.node_key == node_key).first()
    if not node:
        raise HTTPException(status_code=404, detail=f"Node key '{node_key}' not found")

    # Only allow recording visits for end nodes
    if node.node_type != "end":
        return {"status": "skipped", "message": "Visit recording only applies to end nodes."}

    # Check if already recorded
    existing = db.query(UserProgress).filter(
        UserProgress.user_id == current_user.id,
        UserProgress.node_id == node.id
    ).first()
    if not existing:
        progress = UserProgress(
            user_id=current_user.id,
            node_id=node.id,
            mastery_level=100.0,  # End node = mastered
            streak_days=1
        )
        db.add(progress)
        db.commit()

    return {"status": "success", "message": f"End node '{node_key}' visit recorded."}

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

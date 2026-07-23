from typing import Dict, Any, Tuple
from sqlalchemy.orm import Session
from backend.app.models.curriculum import LearningNode, UserProgress
from backend.app.models.user import User

class AdaptiveEngine:
    @staticmethod
    def evaluate_submission(
        db: Session,
        user: User,
        node: LearningNode,
        selected_option_idx: int,
        confidence_level: str  # "low", "medium", "high"
    ) -> Tuple[bool, str, str, float, float, Dict[str, Any]]:
        """
        Evaluates a user answer submission against a learning node using Bayesian Knowledge Tracing & Metacognitive Calibration.

        Returns:
            (is_correct, explanation, next_node_key, mastery_delta, current_mastery, extra_metadata)
        """
        options = node.options_json or []
        is_correct = False
        explanation = ""

        if 0 <= selected_option_idx < len(options):
            chosen_opt = options[selected_option_idx]
            is_correct = chosen_opt.get("isCorrect", False) or (selected_option_idx == node.correct_answer_idx)
            explanation = chosen_opt.get("explanation") or node.remediation_html or "No explanation provided."

        # Fetch or create UserProgress for this node
        progress = db.query(UserProgress).filter(
            UserProgress.user_id == user.id,
            UserProgress.node_id == node.id
        ).first()

        if not progress:
            progress = UserProgress(
                user_id=user.id,
                node_id=node.id,
                mastery_level=50.0,
                streak_days=1,
                confidence_rating=confidence_level
            )
            db.add(progress)
            db.flush()

        current_mastery = progress.mastery_level
        confidence_clean = (confidence_level or "medium").lower()

        # Calculate Mastery Delta & Determine Routing
        if not is_correct:
            if confidence_clean == "high":
                # High overconfidence bias -> heavy penalty & deep remediation
                mastery_delta = -15.0
                next_key = node.next_incorrect_key or "rem1"
                eval_tag = "HIGH_OVERCONFIDENCE_ERROR"
            else:
                mastery_delta = -5.0
                next_key = node.next_incorrect_key or "rem1"
                eval_tag = "STANDARD_INCORRECT"
        else:
            if confidence_clean == "high":
                # Fast track acceleration
                mastery_delta = 10.0
                next_key = node.next_correct_key or "finish_w1"
                eval_tag = "HIGH_CONFIDENCE_FAST_TRACK"
            elif confidence_clean == "low":
                # Scaffolded reinforcement
                mastery_delta = 5.0
                next_key = node.next_correct_key or "finish_w1"
                eval_tag = "LOW_CONFIDENCE_SCAFFOLD"
            else: # medium
                mastery_delta = 7.0
                next_key = node.next_correct_key or "finish_w1"
                eval_tag = "MEDIUM_CONFIDENCE_SUCCESS"

        new_mastery = max(0.0, min(100.0, current_mastery + mastery_delta))
        progress.mastery_level = new_mastery
        progress.confidence_rating = confidence_clean
        db.commit()

        extra_meta = {
            "evaluation_tag": eval_tag,
            "remediation_title": node.concept_name if not is_correct else None,
            "remediation_html": node.remediation_html if not is_correct else None
        }

        return is_correct, explanation, next_key, mastery_delta, new_mastery, extra_meta

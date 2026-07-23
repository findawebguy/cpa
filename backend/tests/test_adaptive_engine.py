from backend.app.core.adaptive_engine import AdaptiveEngine
from backend.app.models.curriculum import LearningNode
from backend.app.models.user import User

def test_adaptive_engine_high_confidence_incorrect(db):
    user = db.query(User).filter(User.email == "student@cpa.com").first()
    node = db.query(LearningNode).filter(LearningNode.node_key == "q1").first()

    # Submit incorrect option with HIGH confidence -> High overconfidence error (-15% mastery)
    is_correct, explanation, next_key, delta, new_mastery, meta = AdaptiveEngine.evaluate_submission(
        db=db,
        user=user,
        node=node,
        selected_option_idx=1,  # Incorrect option
        confidence_level="high"
    )

    assert is_correct is False
    assert delta == -15.0
    assert next_key == "rem1"
    assert meta["evaluation_tag"] == "HIGH_OVERCONFIDENCE_ERROR"

def test_adaptive_engine_high_confidence_correct(db):
    user = db.query(User).filter(User.email == "student@cpa.com").first()
    node = db.query(LearningNode).filter(LearningNode.node_key == "q1").first()

    # Submit correct option with HIGH confidence -> Acceleration (+10% mastery)
    is_correct, explanation, next_key, delta, new_mastery, meta = AdaptiveEngine.evaluate_submission(
        db=db,
        user=user,
        node=node,
        selected_option_idx=0,  # Correct option
        confidence_level="high"
    )

    assert is_correct is True
    assert delta == 10.0
    assert next_key == "q2"
    assert meta["evaluation_tag"] == "HIGH_CONFIDENCE_FAST_TRACK"

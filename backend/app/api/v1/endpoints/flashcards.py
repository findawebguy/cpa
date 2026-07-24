from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.app.db.session import get_db
from backend.app.models.user import User
from backend.app.models.flashcard import Flashcard, FlashcardProgress
from backend.app.schemas.flashcard import FlashcardResponse, FlashcardRatingInput, FlashcardRatingResult
from backend.app.api.v1.endpoints.auth import get_current_user

router = APIRouter()

@router.get("/flashcards", response_model=List[FlashcardResponse])
def get_flashcards(domain: Optional[str] = None, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    query = db.query(Flashcard)
    if domain and domain.upper() in ["FAR", "AUD", "REG"]:
        query = query.filter(Flashcard.domain == domain.upper())
    
    cards = query.all()
    res = []
    for c in cards:
        fp = db.query(FlashcardProgress).filter(
            FlashcardProgress.user_id == current_user.id,
            FlashcardProgress.card_id == c.id
        ).first()

        box = fp.box_number if fp else 1
        stat = fp.status if fp else "review"

        res.append(FlashcardResponse(
            id=c.id,
            domain=c.domain,
            category=c.category,
            question=c.question,
            answer_html=c.answer_html,
            box_number=box,
            status=stat
        ))
    return res

@router.post("/flashcards/{card_id}/rate", response_model=FlashcardRatingResult)
def rate_flashcard(
    card_id: int,
    rating_in: FlashcardRatingInput,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if rating_in.rating.lower() not in {"easy", "medium", "hard", "mastered", "review"}:
        raise HTTPException(status_code=400, detail="Invalid rating. Must be 'easy', 'medium', 'hard', 'mastered', or 'review'.")

    card = db.query(Flashcard).filter(Flashcard.id == card_id).first()
    if not card:
        raise HTTPException(status_code=404, detail="Flashcard not found")

    fp = db.query(FlashcardProgress).filter(
        FlashcardProgress.user_id == current_user.id,
        FlashcardProgress.card_id == card.id
    ).first()

    if not fp:
        fp = FlashcardProgress(user_id=current_user.id, card_id=card.id, box_number=1, status="review")
        db.add(fp)

    if rating_in.rating.lower() == "mastered":
        fp.box_number = min(5, fp.box_number + 1)
        fp.status = "mastered"
    else:
        fp.box_number = 1
        fp.status = "review"

    db.commit()

    return FlashcardRatingResult(
        card_id=card.id,
        new_box_number=fp.box_number,
        new_status=fp.status
    )

from typing import Optional
from pydantic import BaseModel, ConfigDict

class FlashcardResponse(BaseModel):
    id: int
    domain: str
    category: str
    question: str
    answer_html: str
    box_number: int = 1
    status: str = "review"

    model_config = ConfigDict(from_attributes=True)

class FlashcardRatingInput(BaseModel):
    rating: str  # "mastered" or "review"

class FlashcardRatingResult(BaseModel):
    card_id: int
    new_box_number: int
    new_status: str

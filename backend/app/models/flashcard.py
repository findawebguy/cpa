from datetime import datetime
from sqlalchemy import String, Text, Integer, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from backend.app.db.session import Base

class Flashcard(Base):
    __tablename__ = "flashcards"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    domain: Mapped[str] = mapped_column(String, index=True, nullable=False)  # FAR, AUD, REG
    category: Mapped[str] = mapped_column(String, nullable=False)
    question: Mapped[str] = mapped_column(Text, nullable=False)
    answer_html: Mapped[str] = mapped_column(Text, nullable=False)

    user_progress = relationship("FlashcardProgress", back_populates="flashcard", cascade="all, delete-orphan")


class FlashcardProgress(Base):
    __tablename__ = "flashcard_progress"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    card_id: Mapped[int] = mapped_column(Integer, ForeignKey("flashcards.id", ondelete="CASCADE"), nullable=False)
    box_number: Mapped[int] = mapped_column(Integer, default=1)
    status: Mapped[str] = mapped_column(String, default="review")  # "review" or "mastered"
    last_reviewed: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="flashcard_progress")
    flashcard = relationship("Flashcard", back_populates="user_progress")

from datetime import datetime
from sqlalchemy import String, DateTime, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from backend.app.db.session import Base

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String, nullable=False)
    is_admin: Mapped[bool] = mapped_column(default=False)
    target_exam_date: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    progress_entries = relationship("UserProgress", back_populates="user", cascade="all, delete-orphan")
    tbs_attempts = relationship("TBSAttempt", back_populates="user", cascade="all, delete-orphan")
    flashcard_progress = relationship("FlashcardProgress", back_populates="user", cascade="all, delete-orphan")

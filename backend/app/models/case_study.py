from datetime import datetime
from typing import Optional, List
from sqlalchemy import String, Text, Integer, Float, ForeignKey, DateTime, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from backend.app.db.session import Base

class CaseStudy(Base):
    __tablename__ = "case_studies"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    course_id: Mapped[int] = mapped_column(Integer, ForeignKey("courses.id", ondelete="CASCADE"), nullable=False)
    title: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    scenario_text: Mapped[str] = mapped_column(Text, nullable=False)
    exhibits_html: Mapped[str] = mapped_column(Text, nullable=True)

    questions = relationship("CaseQuestion", back_populates="case_study", cascade="all, delete-orphan")
    attempts = relationship("CaseAttempt", back_populates="case_study", cascade="all, delete-orphan")


class CaseQuestion(Base):
    __tablename__ = "case_questions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    case_study_id: Mapped[int] = mapped_column(Integer, ForeignKey("case_studies.id", ondelete="CASCADE"), nullable=False)
    question_text: Mapped[str] = mapped_column(Text, nullable=False)
    options_json: Mapped[dict] = mapped_column(JSON, nullable=False)  # List of dicts: {"text": "...", "isCorrect": bool}
    correct_answer_idx: Mapped[int] = mapped_column(Integer, nullable=False)
    explanation_html: Mapped[str] = mapped_column(Text, nullable=False)

    case_study = relationship("CaseStudy", back_populates="questions")


class CaseAttempt(Base):
    __tablename__ = "case_attempts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    case_study_id: Mapped[int] = mapped_column(Integer, ForeignKey("case_studies.id", ondelete="CASCADE"), nullable=False)
    submission_json: Mapped[dict] = mapped_column(JSON, nullable=False)  # List of submitted answers
    score: Mapped[float] = mapped_column(Float, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    user = relationship("User", backref="case_attempts")
    case_study = relationship("CaseStudy", back_populates="attempts")

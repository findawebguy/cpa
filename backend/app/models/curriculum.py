from datetime import datetime
from typing import Optional, List
from sqlalchemy import String, Text, Integer, Float, ForeignKey, DateTime, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from backend.app.db.session import Base

class Course(Base):
    __tablename__ = "courses"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    code: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)  # FAR, AUD, REG
    title: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)

    syllabi = relationship("Syllabus", back_populates="course", cascade="all, delete-orphan")


class Syllabus(Base):
    __tablename__ = "syllabus"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    course_id: Mapped[int] = mapped_column(Integer, ForeignKey("courses.id", ondelete="CASCADE"), nullable=False)
    week_number: Mapped[int] = mapped_column(Integer, nullable=False)
    title: Mapped[str] = mapped_column(String, nullable=False)

    course = relationship("Course", back_populates="syllabi")
    nodes = relationship("LearningNode", back_populates="syllabus", cascade="all, delete-orphan")


class LearningNode(Base):
    __tablename__ = "learning_nodes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    syllabus_id: Mapped[int] = mapped_column(Integer, ForeignKey("syllabus.id", ondelete="CASCADE"), nullable=False)
    node_key: Mapped[str] = mapped_column(String, index=True, nullable=False)  # e.g., "q1", "rem1"
    concept_name: Mapped[str] = mapped_column(String, nullable=False)
    node_type: Mapped[str] = mapped_column(String, nullable=False)  # "question", "remediation", "end"
    scenario_content: Mapped[str] = mapped_column(Text, nullable=True)
    options_json: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)  # List of option dicts
    correct_answer_idx: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    remediation_html: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    next_correct_key: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    next_incorrect_key: Mapped[Optional[str]] = mapped_column(String, nullable=True)

    syllabus = relationship("Syllabus", back_populates="nodes")
    user_progress = relationship("UserProgress", back_populates="node", cascade="all, delete-orphan")


class UserProgress(Base):
    __tablename__ = "user_progress"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    node_id: Mapped[int] = mapped_column(Integer, ForeignKey("learning_nodes.id", ondelete="CASCADE"), nullable=False)
    mastery_level: Mapped[float] = mapped_column(Float, default=50.0)
    streak_days: Mapped[int] = mapped_column(Integer, default=1)
    confidence_rating: Mapped[str] = mapped_column(String, default="medium")  # low, medium, high
    last_activity: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="progress_entries")
    node = relationship("LearningNode", back_populates="user_progress")

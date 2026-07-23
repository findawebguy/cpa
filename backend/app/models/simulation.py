from datetime import datetime
from typing import Optional
from sqlalchemy import String, Text, Integer, Float, Boolean, ForeignKey, DateTime, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from backend.app.db.session import Base

class TBSScenario(Base):
    __tablename__ = "tbs_scenarios"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    code: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)
    title: Mapped[str] = mapped_column(String, nullable=False)
    exhibit_html: Mapped[str] = mapped_column(Text, nullable=False)
    accounts_list_json: Mapped[dict] = mapped_column(JSON, nullable=False)
    solution_mapping_json: Mapped[dict] = mapped_column(JSON, nullable=False)

    attempts = relationship("TBSAttempt", back_populates="scenario", cascade="all, delete-orphan")


class TBSAttempt(Base):
    __tablename__ = "tbs_attempts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    scenario_id: Mapped[int] = mapped_column(Integer, ForeignKey("tbs_scenarios.id", ondelete="CASCADE"), nullable=False)
    submission_json: Mapped[dict] = mapped_column(JSON, nullable=False)
    score: Mapped[float] = mapped_column(Float, nullable=False)
    is_balanced: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="tbs_attempts")
    scenario = relationship("TBSScenario", back_populates="attempts")

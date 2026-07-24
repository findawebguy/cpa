from datetime import datetime
from typing import Optional, Dict, Any
from sqlalchemy import Column, Integer, String, Text, DateTime, Float, JSON
from backend.app.db.session import Base

class LLMAuditLog(Base):
    __tablename__ = "llm_audit_logs"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    agent_role = Column(String(100), default="Senior Financial Analyst Agent", index=True)
    model_name = Column(String(100), default="meta/llama-3.1-8b-instruct", index=True)
    api_provider = Column(String(50), default="NVIDIA_NIM")
    
    # Dataset Content
    raw_input_feed = Column(JSON, nullable=True)
    prompt_sent = Column(Text, nullable=True)
    raw_llm_response = Column(Text, nullable=True)
    parsed_response = Column(JSON, nullable=True)
    
    # Metadata & Quality Control
    approval_status = Column(String(50), default="PENDING", index=True) # APPROVED, REJECTED, FALLBACK, FAILED
    financial_relevance_score = Column(Integer, nullable=True)
    latency_seconds = Column(Float, default=0.0)

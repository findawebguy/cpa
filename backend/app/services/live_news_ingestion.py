import json
from datetime import datetime, timedelta
from typing import Dict, Any, Tuple
from sqlalchemy.orm import Session

from backend.app.models.case_study import CaseStudy
from backend.app.models.curriculum import Course
from backend.app.services.nvidia_financial_agent import NVIDIAFinancialAnalystAgent

# Track last daily ingestion execution timestamp
_LAST_INGESTION_TIMESTAMP = None
INGESTION_INTERVAL_HOURS = 24

class LiveNewsIngestionService:
    @staticmethod
    def can_ingest_today() -> Tuple[bool, str]:
        """Enforces rate limiting: live data can only be ingested ONCE DAILY at most."""
        global _LAST_INGESTION_TIMESTAMP
        if _LAST_INGESTION_TIMESTAMP is None:
            return True, "Ingestion allowed (first run today)."

        elapsed = datetime.utcnow() - _LAST_INGESTION_TIMESTAMP
        if elapsed < timedelta(hours=INGESTION_INTERVAL_HOURS):
            remaining = timedelta(hours=INGESTION_INTERVAL_HOURS) - elapsed
            hours, remainder = divmod(int(remaining.total_seconds()), 3600)
            minutes = remainder // 60
            return False, f"Daily ingestion limit reached. Next review allowed in {hours}h {minutes}m."

        return True, "Ingestion allowed (24 hours elapsed)."

    @staticmethod
    def run_daily_agent_review_and_ingest(db: Session, raw_feed: Dict[str, Any], api_key: str = "") -> Dict[str, Any]:
        """
        Executes daily Senior Financial Analyst agent review via NVIDIA NIM API (DeepSeek-R1 / Llama-3.1-Nemotron-70B).
        Inserts verified content into the database ONLY if approved by the agent.
        """
        can_run, message = LiveNewsIngestionService.can_ingest_today()
        if not can_run:
            return {
                "status": "rate_limited",
                "message": message,
                "ingested": False
            }

        # 1. Invoke Senior Financial Analyst Agent (NVIDIA NIM Endpoint)
        agent = NVIDIAFinancialAnalystAgent(api_key=api_key)
        review_result = agent.review_and_format_news(raw_feed)

        # 2. Check Agent Approval Status
        if not review_result.get("is_usable") or review_result.get("approval_status") != "APPROVED":
            return {
                "status": "rejected_by_analyst",
                "reason": review_result.get("rejection_reason", "Data quality or financial relevance did not meet CPA guidelines."),
                "ingested": False
            }

        # 3. Target CPA Course Track
        target_domain = review_result.get("cpa_domain", "AUD").upper()
        course = db.query(Course).filter(Course.code == target_domain).first()
        if not course:
            course = db.query(Course).filter(Course.code == "FAR").first()

        # 4. Insert Verified Case Study into Database
        case_study = CaseStudy(
            course_id=course.id,
            title=review_result.get("title", "Verified Live Financial Case Study"),
            description=review_result.get("description", "Daily verified financial news scenario."),
            scenario_text=review_result.get("scenario_text", ""),
            exhibits_html=review_result.get("exhibits_html", ""),
            questions_json=review_result.get("questions", [])
        )
        db.add(case_study)
        db.commit()
        db.refresh(case_study)

        # Update last ingestion timestamp
        global _LAST_INGESTION_TIMESTAMP
        _LAST_INGESTION_TIMESTAMP = datetime.utcnow()

        return {
            "status": "success",
            "message": "Senior Financial Analyst Agent approved and ingested daily live news case study.",
            "ingested": True,
            "case_study_id": case_study.id,
            "title": case_study.title,
            "relevance_score": review_result.get("financial_relevance_score", 90),
            "next_ingestion_allowed_after": (_LAST_INGESTION_TIMESTAMP + timedelta(hours=24)).isoformat()
        }

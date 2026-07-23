from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Dict, Any

from backend.app.db.session import get_db
from backend.app.models.user import User
from backend.app.models.simulation import TBSScenario, TBSAttempt
from backend.app.schemas.simulation import TBSScenarioResponse, TBSSubmission, TBSSubmissionResult
from backend.app.api.v1.endpoints.auth import get_current_user

router = APIRouter()

@router.get("/tbs/{simulation_code}", response_model=TBSScenarioResponse)
def get_tbs_scenario(simulation_code: str, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    tbs = db.query(TBSScenario).filter(TBSScenario.code == simulation_code).first()
    if not tbs:
        # Fallback to first available simulation
        tbs = db.query(TBSScenario).first()
        if not tbs:
            raise HTTPException(status_code=404, detail="No Task-Based Simulations found")
    
    return TBSScenarioResponse(
        id=tbs.id,
        code=tbs.code,
        title=tbs.title,
        exhibit_html=tbs.exhibit_html,
        accounts_list=tbs.accounts_list_json or []
    )

@router.post("/tbs/{simulation_code}/submit", response_model=TBSSubmissionResult)
def submit_tbs_simulation(
    simulation_code: str,
    submission: TBSSubmission,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    tbs = db.query(TBSScenario).filter(TBSScenario.code == simulation_code).first()
    if not tbs:
        tbs = db.query(TBSScenario).first()
        if not tbs:
            raise HTTPException(status_code=404, detail="TBS Scenario not found")

    solution = tbs.solution_mapping_json or {}
    expected_debits = solution.get("expected_debits", {})
    expected_credits = solution.get("expected_credits", {})
    required_total = float(solution.get("required_total", 0.0))

    total_debits = 0.0
    total_credits = 0.0
    actual_debits = {}
    actual_credits = {}

    for row in submission.rows:
        acc = row.account
        d = float(row.debit or 0.0)
        c = float(row.credit or 0.0)
        if d > 0:
            total_debits += d
            actual_debits[acc] = actual_debits.get(acc, 0.0) + d
        if c > 0:
            total_credits += c
            actual_credits[acc] = actual_credits.get(acc, 0.0) + c

    is_balanced = (total_debits > 0) and (abs(total_debits - total_credits) < 0.01)

    # Calculate correctness score
    matched_debits = 0
    for acc, val in expected_debits.items():
        if abs(actual_debits.get(acc, 0.0) - float(val)) < 0.01:
            matched_debits += 1

    matched_credits = 0
    for acc, val in expected_credits.items():
        if abs(actual_credits.get(acc, 0.0) - float(val)) < 0.01:
            matched_credits += 1

    total_expected = len(expected_debits) + len(expected_credits)
    score_ratio = (matched_debits + matched_credits) / total_expected if total_expected > 0 else 0.0
    passed = is_balanced and (score_ratio >= 0.99)
    final_score = round(score_ratio * 100.0, 1)

    if passed:
        feedback = f"""
        <div class="font-bold flex items-center gap-1.5 text-sm mb-1 text-emerald-800">
            <i class="fa-solid fa-award text-emerald-600"></i> Simulation Passed with 100% Accuracy!
        </div>
        <p class="text-xs text-emerald-900">You correctly classified and recorded all journal entry adjustments. Total debits and credits equal <b>${total_debits:,.2f}</b>.</p>
        """
    else:
        feedback = f"""
        <div class="font-bold flex items-center gap-1.5 text-sm mb-1 text-amber-900">
            <i class="fa-solid fa-triangle-exclamation text-amber-600"></i> Journal Entries Require Adjustment
        </div>
        <p class="text-xs text-amber-900">Ensure all exhibit findings are debited/credited to the correct accounts. Total debits must equal credits at <b>${required_total:,.2f}</b>.</p>
        """

    attempt = TBSAttempt(
        user_id=current_user.id,
        scenario_id=tbs.id,
        submission_json=[r.model_dump() for r in submission.rows],
        score=final_score,
        is_balanced=is_balanced
    )
    db.add(attempt)
    db.commit()

    return TBSSubmissionResult(
        score=final_score,
        is_balanced=is_balanced,
        total_debits=total_debits,
        total_credits=total_credits,
        passed=passed,
        feedback_html=feedback
    )

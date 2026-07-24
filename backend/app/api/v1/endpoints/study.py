from typing import List, Optional
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from backend.app.models.user import User
from backend.app.api.v1.endpoints.auth import get_current_user

router = APIRouter()

class StudyModule(BaseModel):
    id: str
    track: str  # FAR, AUD, REG
    title: str
    subtitle: str
    codification_ref: str  # e.g., "FASB ASC 606", "AICPA AU-C 315", "IRC § 351"
    estimated_minutes: int
    reading_content_html: str
    linked_tbs_code: str
    linked_question_keys: List[str]

STUDY_MODULES_DB: List[StudyModule] = [
    StudyModule(
        id="far-asc-606",
        track="FAR",
        title="ASC 606: Revenue Recognition Framework",
        subtitle="5-Step Core Principle, Contract Balances & Variable Consideration",
        codification_ref="FASB ASC 606 / IFRS 15",
        estimated_minutes=15,
        reading_content_html="""
        <div class="space-y-4 text-slate-800 text-xs leading-relaxed">
            <div class="p-4 bg-sky-50 border-l-4 border-sky-600 rounded-r-xl font-medium">
                <h4 class="font-bold text-sky-900 text-sm mb-1">Core Principle (ASC 606-10-25-1)</h4>
                Recognize revenue to depict the transfer of promised goods or services to customers in an amount that reflects the consideration to which the entity expects to be entitled.
            </div>

            <h4 class="font-bold text-slate-900 text-sm border-b pb-1 border-slate-200">The 5-Step Revenue Recognition Model</h4>
            <ol class="list-decimal pl-5 space-y-2">
                <li><b>Identify the Contract with a Customer:</b> Enforceable rights, commercial substance, approved by both parties, probable collection.</li>
                <li><b>Identify Performance Obligations:</b> Distinct goods/services or series of substantially identical distinct goods/services. A good/service is distinct if the customer can benefit from it individually or with readily available resources.</li>
                <li><b>Determine the Transaction Price:</b> Total consideration expected (includes fixed fees, variable consideration estimates, significant financing components, and non-cash consideration).</li>
                <li><b>Allocate Transaction Price:</b> Relative Standalone Selling Price (SSP) allocation across all distinct performance obligations.</li>
                <li><b>Recognize Revenue:</b> When (or as) the entity satisfies a performance obligation by transferring control over the asset to the customer (Point-in-Time vs Over-Time).</li>
            </ol>

            <h4 class="font-bold text-slate-900 text-sm border-b pb-1 border-slate-200 mt-4">Contract Asset vs. Accounts Receivable</h4>
            <div class="grid grid-cols-1 sm:grid-cols-2 gap-3 font-mono text-[11px]">
                <div class="p-3 bg-white border border-slate-200 rounded-lg shadow-sm">
                    <div class="font-bold text-indigo-700">Contract Asset</div>
                    <div>Conditional right to consideration (e.g., must satisfy another obligation before billing).</div>
                </div>
                <div class="p-3 bg-white border border-slate-200 rounded-lg shadow-sm">
                    <div class="font-bold text-emerald-700">Accounts Receivable</div>
                    <div>Unconditional right to payment due solely to the passage of time.</div>
                </div>
            </div>
        </div>
        """,
        linked_tbs_code="tbs-1",
        linked_question_keys=["q1", "far_w3_q1"]
    ),
    StudyModule(
        id="far-asc-842",
        track="FAR",
        title="ASC 842: Lease Accounting & Balance Sheet Recognition",
        subtitle="Finance vs Operating Lease Classification, ROU Asset & Lease Liability",
        codification_ref="FASB ASC 842",
        estimated_minutes=20,
        reading_content_html="""
        <div class="space-y-4 text-slate-800 text-xs leading-relaxed">
            <div class="p-4 bg-amber-50 border-l-4 border-amber-600 rounded-r-xl font-medium">
                <h4 class="font-bold text-amber-900 text-sm mb-1">ASC 842 On-Balance Sheet Mandate</h4>
                Lessees must recognize a <b>Right-of-Use (ROU) Asset</b> and a <b>Lease Liability</b> on the balance sheet for virtually all leases (excluding short-term leases ≤ 12 months).
            </div>

            <h4 class="font-bold text-slate-900 text-sm border-b pb-1 border-slate-200">Lessee Lease Classification Test (5 Criteria)</h4>
            <p>If <b>ANY ONE</b> of the following 5 criteria is met at lease commencement, classify as a <b>Finance Lease</b>; otherwise, classify as an <b>Operating Lease</b>:</p>
            <ul class="list-disc pl-5 space-y-1.5 font-mono text-[11px]">
                <li><b>O - Ownership Transfer:</b> Ownership of underlying asset transfers to lessee by end of lease term.</li>
                <li><b>P - Purchase Option:</b> Lessee is reasonably certain to exercise a purchase option.</li>
                <li><b>N - Net Present Value:</b> PV of lease payments + guaranteed residual value &ge; 90% of Asset Fair Value.</li>
                <li><b>T - Term:</b> Lease term is &ge; 75% of asset's remaining economic life.</li>
                <li><b>S - Specialized Asset:</b> Asset has no alternative use to lessor at end of term.</li>
            </ul>

            <h4 class="font-bold text-slate-900 text-sm border-b pb-1 border-slate-200 mt-4">Income Statement Accounting Impact</h4>
            <div class="grid grid-cols-1 sm:grid-cols-2 gap-3 text-[11px]">
                <div class="p-3 bg-white border border-slate-200 rounded-lg">
                    <div class="font-bold text-slate-900">Finance Lease</div>
                    <ul class="list-disc pl-4 space-y-1 mt-1 text-slate-600">
                        <li>Amortization Expense (ROU Asset - Straight Line)</li>
                        <li>Interest Expense (Effective Interest Method on Liability)</li>
                        <li>Front-loaded total expense pattern</li>
                    </ul>
                </div>
                <div class="p-3 bg-white border border-slate-200 rounded-lg">
                    <div class="font-bold text-slate-900">Operating Lease</div>
                    <ul class="list-disc pl-4 space-y-1 mt-1 text-slate-600">
                        <li>Single Lease Expense (Straight Line total cost)</li>
                        <li>ROU Asset reduction is plug to balance Lease Expense & Liability interest</li>
                    </ul>
                </div>
            </div>
        </div>
        """,
        linked_tbs_code="tbs-1",
        linked_question_keys=["far_w5_q1"]
    ),
    StudyModule(
        id="aud-coso-ic",
        track="AUD",
        title="COSO Internal Control Integrated Framework",
        subtitle="5 Components, 17 Principles, & Auditor Risk Assessment",
        codification_ref="COSO Framework / AICPA AU-C 315",
        estimated_minutes=15,
        reading_content_html="""
        <div class="space-y-4 text-slate-800 text-xs leading-relaxed">
            <div class="p-4 bg-indigo-50 border-l-4 border-indigo-600 rounded-r-xl font-medium">
                <h4 class="font-bold text-indigo-900 text-sm mb-1">COSO Framework 5 Components (Mnemonic: CRIME)</h4>
                An effective internal control system requires that all 5 components be present, functioning, and operating together in an integrated manner.
            </div>

            <div class="space-y-3 font-sans">
                <div class="p-3 bg-white border border-slate-200 rounded-lg">
                    <b class="text-indigo-800">1. Control Environment ("Tone at the Top"):</b> Commitment to integrity, ethical values, board oversight, organizational structure, accountability.
                </div>
                <div class="p-3 bg-white border border-slate-200 rounded-lg">
                    <b class="text-indigo-800">2. Risk Assessment:</b> Specifying objectives, identifying operational/financial risks, assessing fraud risk, evaluating organizational changes.
                </div>
                <div class="p-3 bg-white border border-slate-200 rounded-lg">
                    <b class="text-indigo-800">3. Control Activities:</b> Selecting policies and procedures (Segregation of Duties, Authorization, IT Access Controls) to mitigate risks.
                </div>
                <div class="p-3 bg-white border border-slate-200 rounded-lg">
                    <b class="text-indigo-800">4. Information & Communication:</b> Obtaining relevant quality info, internal communication, external communication.
                </div>
                <div class="p-3 bg-white border border-slate-200 rounded-lg">
                    <b class="text-indigo-800">5. Monitoring Activities:</b> Ongoing evaluations, separate evaluations, communicating deficiencies to management/board.
                </div>
            </div>
        </div>
        """,
        linked_tbs_code="tbs-1",
        linked_question_keys=["q1_aud"]
    ),
    StudyModule(
        id="reg-corporate-nol",
        track="REG",
        title="IRC § 172: Corporate Taxation & NOL Deductions",
        subtitle="Post-2017 NOL 80% Taxable Income Cap, Indefinite Carryforward & M-1 Book-Tax Adjustments",
        codification_ref="Internal Revenue Code § 172 / § 243",
        estimated_minutes=20,
        reading_content_html="""
        <div class="space-y-4 text-slate-800 text-xs leading-relaxed">
            <div class="p-4 bg-emerald-50 border-l-4 border-emerald-600 rounded-r-xl font-medium">
                <h4 class="font-bold text-emerald-900 text-sm mb-1">TCJA Net Operating Loss (NOL) Rules (IRC § 172)</h4>
                For corporate tax losses generated in tax years after Dec 31, 2017:
                <ul class="list-disc pl-5 mt-1 space-y-1 font-mono text-[11px]">
                    <li><b>80% Limitation:</b> NOL deductions cannot exceed 80% of taxable income (computed before the NOL deduction).</li>
                    <li><b>Indefinite Carryforward:</b> Unused NOLs carry forward indefinitely (no 20-year expiration).</li>
                    <li><b>No Carryback:</b> Carrybacks are eliminated (0-year carryback).</li>
                </ul>
            </div>

            <h4 class="font-bold text-slate-900 text-sm border-b pb-1 border-slate-200">Dividends Received Deduction (DRD) Tiers (IRC § 243)</h4>
            <div class="grid grid-cols-1 sm:grid-cols-3 gap-2 text-center font-mono text-[11px]">
                <div class="p-3 bg-white border border-slate-200 rounded-lg">
                    <div class="font-bold text-emerald-700 text-sm">50% DRD</div>
                    <div class="text-slate-500">Ownership &lt; 20%</div>
                </div>
                <div class="p-3 bg-white border border-slate-200 rounded-lg">
                    <div class="font-bold text-emerald-700 text-sm">65% DRD</div>
                    <div class="text-slate-500">Ownership 20% to 80%</div>
                </div>
                <div class="p-3 bg-white border border-slate-200 rounded-lg">
                    <div class="font-bold text-emerald-700 text-sm">100% DRD</div>
                    <div class="text-slate-500">Affiliated Group (&ge; 80%)</div>
                </div>
            </div>
        </div>
        """,
        linked_tbs_code="tbs-1",
        linked_question_keys=["reg_w3_q0"]
    ),
    StudyModule(
        id="reg-ethics-circular230",
        track="REG",
        title="Treasury Circular 230 & Professional Conduct",
        subtitle="IRS Rules Governing Practice Before the IRS, Client Errors & Tax Preparer Penalties",
        codification_ref="Treasury Circular 230 / IRC § 6694",
        estimated_minutes=15,
        reading_content_html="""
        <div class="space-y-4 text-slate-800 text-xs leading-relaxed">
            <div class="p-4 bg-purple-50 border-l-4 border-purple-600 rounded-r-xl font-medium">
                <h4 class="font-bold text-purple-900 text-sm mb-1">Circular 230 § 10.21: Client Errors & Omissions</h4>
                A practitioner who knows a client has not complied with tax laws or made an error on a return MUST advise the client promptly of the noncompliance/error and the consequences. The practitioner is <b>NOT</b> required or permitted to notify the IRS directly without client consent.
            </div>

            <h4 class="font-bold text-slate-900 text-sm border-b pb-1 border-slate-200">Tax Return Position Standards (IRC § 6694)</h4>
            <div class="space-y-2 font-mono text-[11px]">
                <div class="p-2.5 bg-white border border-slate-200 rounded-lg">
                    <b>Substantial Authority (&approx; 40% chance):</b> Required to avoid tax preparer penalties for undisclosed positions.
                </div>
                <div class="p-2.5 bg-white border border-slate-200 rounded-lg">
                    <b>Reasonable Basis (&approx; 20% chance):</b> Minimum standard for adequately disclosed positions (Form 8275).
                </div>
            </div>
        </div>
        """,
        linked_tbs_code="tbs-1",
        linked_question_keys=["reg_w5_q0"]
    )
]

@router.get("/modules", response_model=List[StudyModule])
def list_study_modules(
    track: Optional[str] = None,
    current_user: User = Depends(get_current_user)
):
    """Return all available structured study modules (Reading -> Simulation -> Practice Quiz)."""
    if track:
        return [m for m in STUDY_MODULES_DB if m.track.upper() == track.upper()]
    return STUDY_MODULES_DB

@router.get("/modules/{module_id}", response_model=StudyModule)
def get_study_module(
    module_id: str,
    current_user: User = Depends(get_current_user)
):
    """Fetch details for a specific study module."""
    mod = next((m for m in STUDY_MODULES_DB if m.id == module_id), None)
    if not mod:
        raise HTTPException(status_code=404, detail=f"Study module '{module_id}' not found")
    return mod

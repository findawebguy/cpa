from sqlalchemy.orm import Session
from backend.app.db.session import engine, Base, SessionLocal
from backend.app.core.security import get_password_hash
from backend.app.models.user import User
from backend.app.models.curriculum import Course, Syllabus, LearningNode, UserProgress
from backend.app.models.simulation import TBSScenario, TBSAttempt
from backend.app.models.flashcard import Flashcard
from backend.app.models.case_study import CaseStudy, CaseQuestion, CaseAttempt
from backend.app.db.seed_questions import get_all_questions
from backend.app.db.seed_cases import get_case_studies

def reseed_curriculum(db: Session):
    print("RESEED: Wiping curriculum data...")
    Base.metadata.create_all(bind=engine)
    db.query(CaseAttempt).delete()
    db.query(CaseQuestion).delete()
    db.query(CaseStudy).delete()
    db.query(UserProgress).delete()
    db.query(TBSAttempt).delete()
    db.query(LearningNode).delete()
    db.query(Flashcard).delete()
    db.query(TBSScenario).delete()
    db.query(Syllabus).delete()
    db.query(Course).delete()
    db.commit()
    print("RESEED: Curriculum wiped. Re-seeding...")
    init_db(db)
    print("RESEED: Complete.")

def init_db(db: Session):
    Base.metadata.create_all(bind=engine)

    demo_user = db.query(User).filter(User.email == "student@cpa.com").first()
    if not demo_user:
        demo_user = User(email="student@cpa.com", password_hash=get_password_hash("pass123"))
        db.add(demo_user)
        db.commit()

    if db.query(Course).first():
        print("Database already populated.")
        return

    # Courses
    far_course = Course(code="FAR", title="FAR: Financial Accounting & Reporting", description="GAAP, ASC 606, ASC 842, Consolidations.")
    aud_course = Course(code="AUD", title="AUD: Auditing & Attestation", description="COSO, GAAS, Audit Evidence, Reports.")
    reg_course = Course(code="REG", title="REG: Taxation & Business Law", description="IRC, TCJA updates, Business Law.")
    db.add_all([far_course, aud_course, reg_course])
    db.flush()
    
    courses_map = {"FAR": far_course.id, "AUD": aud_course.id, "REG": reg_course.id}

    # Syllabi setup
    far_weeks = ["Accounting Cycle", "Financial Statements", "ASC 606", "Inventory/PPE", "ASC 842 Leases", "Equity", "Consolidations"]
    aud_weeks = ["Ethics & COSO", "Risk Assessment", "Evidence", "Reports", "Integrated Audits", "Attestation"]
    reg_weeks = ["Individual Tax", "Property Transactions", "Corporate Tax", "Entity Choice", "Ethics", "Business Law"]
    
    syllabus_map = {}
    for c_code, w_list in [("FAR", far_weeks), ("AUD", aud_weeks), ("REG", reg_weeks)]:
        for i, title in enumerate(w_list, start=1):
            s = Syllabus(course_id=courses_map[c_code], week_number=i, title=f"Week {i}: {title}")
            db.add(s)
            db.flush()
            syllabus_map[f"{c_code}_w{i}"] = s.id

    # Seed Questions
    all_qs = get_all_questions()
    for c_code in ["FAR", "AUD", "REG"]:
        qs = all_qs.get(c_code, [])
        # Group by week
        week_groups = {}
        for q in qs:
            week_groups.setdefault(q["week"], []).append(q)
            
        for w, q_list in week_groups.items():
            s_id = syllabus_map[f"{c_code}_w{w}"]
            for i, q in enumerate(q_list):
                q_key = f"{c_code}_w{w}_q{i}"
                is_last = (i == len(q_list) - 1)
                next_correct = f"{c_code}_w{w}_end" if is_last else f"{c_code}_w{w}_q{i+1}"
                next_incorrect = f"{c_code}_w{w}_q{i}_rem"

                # Main Question
                db.add(LearningNode(
                    syllabus_id=s_id, node_key=q_key, concept_name=q["concept_name"],
                    node_type="question", scenario_content=q["scenario"], options_json=q["options"],
                    correct_answer_idx=q["correct_idx"], remediation_html=q["remediation"],
                    next_correct_key=next_correct, next_incorrect_key=next_incorrect
                ))

                # Remediation
                db.add(LearningNode(
                    syllabus_id=s_id, node_key=next_incorrect, concept_name=f"{q['concept_name']} - Review",
                    node_type="remediation", scenario_content="Review this concept:", remediation_html=q["remediation"],
                    next_correct_key=q_key, next_incorrect_key=q_key
                ))
            
            # End Node for the week
            db.add(LearningNode(
                syllabus_id=s_id, node_key=f"{c_code}_w{w}_end", concept_name=f"{c_code} Week {w} Mastered",
                node_type="end", scenario_content=f"🎉 Week {w} Mastered!", remediation_html="Great job!"
            ))

    # Seed Case Studies
    cases = get_case_studies()
    for case_data in cases:
        cs = CaseStudy(
            course_id=courses_map[case_data["course"]],
            title=case_data["title"],
            description=case_data["description"],
            scenario_text=case_data["scenario_text"],
            exhibits_html=case_data["exhibits_html"]
        )
        db.add(cs)
        db.flush()
        
        for cq in case_data["questions"]:
            q = CaseQuestion(
                case_study_id=cs.id,
                question_text=cq["question_text"],
                options_json=cq["options"],
                correct_answer_idx=cq["correct_idx"],
                explanation_html=cq["explanation_html"]
            )
            db.add(q)

    # Seed TBS Scenarios
    tbs1 = TBSScenario(
        code="tbs-1",
        title="Adjusting Journal Entry & Financial Statement Reconciliation",
        exhibit_html="""
        <div class="space-y-2">
            <h4 class="font-bold text-slate-800"><i class="fa-solid fa-folder-open text-amber-500 mr-1"></i> Exhibit A: Year-End Audit Findings (Apex Global Enterprises)</h4>
            <p class="text-xs text-slate-600">Review the unadjusted trial balance as of Dec 31, 2026. The following 3 unrecorded items were discovered during year-end audit testing:</p>
            <ul class="list-disc list-inside text-xs text-slate-700 bg-white p-3 rounded-lg border border-slate-200 space-y-1">
                <li><b>Item 1: Insurance Deferral:</b> On Oct 1, Apex paid $12,000 for a 1-year policy, debited to Prepaid Insurance. 3 months ($3,000) expired by Dec 31.</li>
                <li><b>Item 2: Revenue Accrual:</b> Services performed for $4,500 in late December remain unbilled and unrecorded.</li>
                <li><b>Item 3: Depreciation:</b> Annual depreciation on office equipment is calculated at $6,200.</li>
            </ul>
        </div>
        """,
        accounts_list_json=[
            "-- Select Account --",
            "Insurance Expense",
            "Prepaid Insurance",
            "Accounts Receivable",
            "Service Revenue",
            "Depreciation Expense",
            "Accumulated Depreciation",
            "Cash",
            "Accounts Payable"
        ],
        solution_mapping_json={
            "expected_debits": {"Insurance Expense": 3000.0, "Accounts Receivable": 4500.0, "Depreciation Expense": 6200.0},
            "expected_credits": {"Prepaid Insurance": 3000.0, "Service Revenue": 4500.0, "Accumulated Depreciation": 6200.0},
            "required_total": 13700.0
        }
    )

    tbs2 = TBSScenario(
        code="tbs-2",
        title="ASC 606 Revenue Recognition 5-Step Allocation",
        exhibit_html="""
        <div class="space-y-2">
            <h4 class="font-bold text-slate-800"><i class="fa-solid fa-folder-open text-sky-500 mr-1"></i> Exhibit B: Software & Maintenance Bundled Contract</h4>
            <p class="text-xs text-slate-600">On Nov 1, TechCorp sold a software license and 1-year tech support package for a bundled price of $100,000 cash. Standalone selling prices:</p>
            <ul class="list-disc list-inside text-xs text-slate-700 bg-white p-3 rounded-lg border border-slate-200 space-y-1">
                <li>Software License Standalone Price: $80,000 (Delivered Nov 1)</li>
                <li>1-Year Tech Support Standalone Price: $40,000 (Provided Nov 1 to Oct 31)</li>
                <li>Total Standalone Sum: $120,000</li>
            </ul>
            <p class="text-xs text-slate-600">Record the initial revenue entry on Nov 1 allocated based on relative standalone selling prices (Software: 80/120 * $100k = $66,667; Support: 40/120 * $100k = $33,333 Unearned Revenue).</p>
        </div>
        """,
        accounts_list_json=[
            "-- Select Account --",
            "Cash",
            "Software Revenue",
            "Unearned Support Revenue",
            "Accounts Receivable",
            "Service Revenue"
        ],
        solution_mapping_json={
            "expected_debits": {"Cash": 100000.0},
            "expected_credits": {"Software Revenue": 66667.0, "Unearned Support Revenue": 33333.0},
            "required_total": 100000.0
        }
    )

    tbs3 = TBSScenario(
        code="tbs-3",
        title="ASC 842 Lease Classification & Initial Right-of-Use Asset Recognition",
        exhibit_html="""
        <div class="space-y-2">
            <h4 class="font-bold text-slate-800"><i class="fa-solid fa-folder-open text-emerald-500 mr-1"></i> Exhibit C: Equipment Lease Agreement</h4>
            <p class="text-xs text-slate-600">On Jan 1, 2026, Nexus Inc leased heavy manufacturing equipment under a 5-year lease (useful life 5 years). Present value of lease payments discounted at 6% = $250,000. Initial direct costs paid in cash = $5,000.</p>
            <p class="text-xs text-slate-600">Record the initial entry to recognize the Right-of-Use (ROU) Asset and Lease Liability on Jan 1 ($255,000 ROU Asset = $250,000 Lease Liability + $5,000 Direct Cash Cost).</p>
        </div>
        """,
        accounts_list_json=[
            "-- Select Account --",
            "ROU Asset - Operating/Finance Lease",
            "Lease Liability",
            "Cash",
            "Lease Expense",
            "Equipment"
        ],
        solution_mapping_json={
            "expected_debits": {"ROU Asset - Operating/Finance Lease": 255000.0},
            "expected_credits": {"Lease Liability": 250000.0, "Cash": 5000.0},
            "required_total": 255000.0
        }
    )

    db.add_all([tbs1, tbs2, tbs3])

    # Flashcards
    flashcards_list = [
        ("FAR", "ASC 606", "What are the 5 Steps of Revenue Recognition under ASC 606?", "<ol class='list-decimal list-inside space-y-1 font-sans'><li>Identify Contract with Customer.</li><li>Identify Performance Obligations.</li><li>Determine Transaction Price.</li><li>Allocate Price to Obligations.</li><li>Recognize Revenue when/as satisfied.</li></ol>"),
        ("FAR", "ASC 842 LEASES", "What are the 5 criteria to classify a lease as a Finance Lease for a Lessee?", "<ul class='list-disc list-inside space-y-1 font-sans'><li>Transfer of Ownership.</li><li>Purchase Option reasonably certain to be exercised.</li><li>Lease Term is major part of economic life (≥75%).</li><li>Present Value of payments ≥ substantially all fair value (≥90%).</li><li>Specialized Asset with no alternative use.</li></ul>"),
        ("AUD", "COSO FRAMEWORK", "What are the 5 Components of the COSO Internal Control Framework? (Mnemonic: CRIME)", "<ul class='list-disc list-inside space-y-1 font-sans'><li><b>C</b>ontrol Environment</li><li><b>R</b>isk Assessment</li><li><b>I</b>nformation & Communication</li><li><b>M</b>onitoring Activities</li><li><b>E</b>xisting Control Activities</li></ul>"),
        ("REG", "TAX LAW", "What is the key difference between Tax Credits vs. Tax Deductions?", "<p class='font-sans leading-relaxed'><b>Tax Deductions</b> reduce total Taxable Income.<br><b>Tax Credits</b> provide a direct dollar-for-dollar reduction of the tax liability.</p>")
    ]
    for domain, cat, q, a in flashcards_list:
        db.add(Flashcard(domain=domain, category=cat, question=q, answer_html=a))

    db.commit()
    print("Database seeding completed successfully.")

if __name__ == "__main__":
    db = SessionLocal()
    init_db(db)
    db.close()

import json

def get_far_questions():
    questions = []
    # Week 1: Accounting Cycle
    for i in range(10):
        questions.append({
            "week": 1,
            "concept_name": f"Accounting Cycle & Accrual Engine #{i+1}",
            "scenario": f"Apex Corp transaction scenario {i+1} analyzing the impact on the accounting equation and accrual basis.",
            "options": [
                {"text": "Assets increase, Liabilities increase.", "isCorrect": True, "explanation": "Correct per basic accounting equation."},
                {"text": "Assets decrease, Equity increases.", "isCorrect": False, "explanation": "Incorrect."},
                {"text": "No effect on Balance Sheet.", "isCorrect": False, "explanation": "Incorrect."}
            ],
            "correct_idx": 0,
            "remediation": "Review the fundamental accounting equation (A = L + E)."
        })
    
    # Week 3: ASC 606
    for i in range(12):
        questions.append({
            "week": 3,
            "concept_name": f"ASC 606 Revenue Recognition #{i+1}",
            "scenario": f"Software firm signs a bundled contract. Identify Step { (i%5)+1 } of the 5-step ASC 606 revenue recognition model.",
            "options": [
                {"text": "Correct application of ASC 606 standard.", "isCorrect": True, "explanation": "Correct per ASC 606."},
                {"text": "Incorrect application.", "isCorrect": False, "explanation": "Violates ASC 606."}
            ],
            "correct_idx": 0,
            "remediation": "ASC 606 requires a 5-step model to recognize revenue."
        })

    # Week 5: ASC 842 Leases
    for i in range(15):
        questions.append({
            "week": 5,
            "concept_name": f"ASC 842 Leases #{i+1}",
            "scenario": f"Company enters into a 5-year lease for equipment with a 6-year useful life. Present value of payments is 92% of fair value. Classify the lease.",
            "options": [
                {"text": "Finance Lease", "isCorrect": True, "explanation": "Meets the 75% useful life test (5/6 = 83%) and 90% PV test (92%)."},
                {"text": "Operating Lease", "isCorrect": False, "explanation": "Fails to meet operating lease criteria because it triggers finance lease tests."},
                {"text": "Short-term Lease", "isCorrect": False, "explanation": "Lease term is > 12 months."}
            ],
            "correct_idx": 0,
            "remediation": "ASC 842 Finance Lease criteria: Transfer ownership, Purchase option reasonably certain, Term >= 75% life, PV >= 90% FV, Specialized asset."
        })
        
    # Fill remaining FAR weeks
    for w in [2, 4, 6, 7]:
        for i in range(10):
            questions.append({
                "week": w,
                "concept_name": f"FAR Core Concept Week {w} - Q{i+1}",
                "scenario": f"Advanced FAR scenario testing GAAP standards for Week {w}.",
                "options": [
                    {"text": "GAAP Compliant Treatment", "isCorrect": True, "explanation": "Correct per US GAAP."},
                    {"text": "IFRS Treatment", "isCorrect": False, "explanation": "Not compliant with US GAAP."},
                    {"text": "Non-compliant Treatment", "isCorrect": False, "explanation": "Violates accounting standards."}
                ],
                "correct_idx": 0,
                "remediation": "Review the relevant FASB Accounting Standards Codification (ASC) section."
            })
    return questions

def get_aud_questions():
    questions = []
    # Week 1: COSO & Ethics
    for i in range(12):
        questions.append({
            "week": 1,
            "concept_name": f"COSO Internal Controls #{i+1}",
            "scenario": f"Auditor evaluates the 'Tone at the Top' and management's philosophy.",
            "options": [
                {"text": "Control Environment", "isCorrect": True, "explanation": "Control Environment is the foundation of COSO (Tone at the Top)."},
                {"text": "Risk Assessment", "isCorrect": False, "explanation": "Incorrect component."},
                {"text": "Control Activities", "isCorrect": False, "explanation": "Incorrect component."}
            ],
            "correct_idx": 0,
            "remediation": "The 5 COSO components are CRIME (Control Environment, Risk Assessment, Info & Comm, Monitoring, Existing Control Activities)."
        })
    # Fill remaining AUD weeks
    for w in range(2, 7):
        for i in range(10):
            questions.append({
                "week": w,
                "concept_name": f"AUD Core Concept Week {w} - Q{i+1}",
                "scenario": f"Auditing standards scenario testing GAAS for Week {w}.",
                "options": [
                    {"text": "GAAS Compliant Procedure", "isCorrect": True, "explanation": "Correct per GAAS."},
                    {"text": "Violates Independence", "isCorrect": False, "explanation": "Violates AICPA Code of Professional Conduct."},
                    {"text": "Inadequate Evidence", "isCorrect": False, "explanation": "Fails to meet sufficient appropriate evidence standard."}
                ],
                "correct_idx": 0,
                "remediation": "Review the relevant Statement on Auditing Standards (SAS)."
            })
    return questions

def get_reg_questions():
    questions = []
    # Week 3: Corporate Tax & 2026 TCJA updates
    for i in range(15):
        questions.append({
            "week": 3,
            "concept_name": f"Corporate Taxation & TCJA Updates #{i+1}",
            "scenario": f"Under the tax provisions effective in 2026, a C-Corporation has a net operating loss (NOL) generated in 2025. How much taxable income can this NOL offset in 2026?",
            "options": [
                {"text": "80% of taxable income", "isCorrect": True, "explanation": "Under TCJA rules applicable in 2026, NOLs generated after 2017 can only offset up to 80% of taxable income."},
                {"text": "100% of taxable income", "isCorrect": False, "explanation": "The 100% offset was temporarily allowed under the CARES Act for 2018-2020, but the 80% limit applies in 2026."},
                {"text": "0%, NOLs expire after 5 years", "isCorrect": False, "explanation": "Post-2017 NOLs carry forward indefinitely."}
            ],
            "correct_idx": 0,
            "remediation": "TCJA limits NOL deductions to 80% of taxable income for losses arising after Dec 31, 2017, and carrying forward indefinitely."
        })
    # Fill remaining REG weeks
    for w in [1, 2, 4, 5, 6]:
        for i in range(10):
            questions.append({
                "week": w,
                "concept_name": f"REG Core Concept Week {w} - Q{i+1}",
                "scenario": f"Tax and Business Law scenario testing IRC or UCC for Week {w}.",
                "options": [
                    {"text": "Correct IRC Treatment", "isCorrect": True, "explanation": "Correct per Internal Revenue Code."},
                    {"text": "Incorrect Treatment", "isCorrect": False, "explanation": "Disallowed under IRC regulations."},
                    {"text": "Tax Fraud", "isCorrect": False, "explanation": "Illegal tax evasion."}
                ],
                "correct_idx": 0,
                "remediation": "Review the relevant IRC sections and Treasury Regulations."
            })
    return questions

def get_all_questions():
    return {
        "FAR": get_far_questions(),
        "AUD": get_aud_questions(),
        "REG": get_reg_questions()
    }

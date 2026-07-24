import json

def get_far_questions():
    questions = []
    # Week 1: Accounting Cycle
    for i in range(10):
        questions.append({
            "week": 1,
            "concept_name": f"Accounting Cycle & Accrual Engine #{i+1}",
            "scenario": f"Apex Corp transaction scenario {i+1}: Analyzing revenue/expense accruals vs cash flows.",
            "options": [
                {"text": "Assets increase, Liabilities increase.", "isCorrect": True, "explanation": "Correct per basic accounting equation (A = L + E)."},
                {"text": "Assets decrease, Equity increases.", "isCorrect": False, "explanation": "Incorrect accounting equation impact."},
                {"text": "No effect on Balance Sheet.", "isCorrect": False, "explanation": "Incorrect."}
            ],
            "correct_idx": 0,
            "remediation": "Review the fundamental accounting equation (A = L + E) under accrual accounting."
        })
    
    # Week 3: ASC 606
    for i in range(12):
        questions.append({
            "week": 3,
            "concept_name": f"ASC 606 Revenue Recognition #{i+1}",
            "scenario": f"Software firm signs a bundled contract. Identify Step {(i%5)+1} of the 5-step ASC 606 revenue recognition model.",
            "options": [
                {"text": "Correct application of ASC 606 standard.", "isCorrect": True, "explanation": "Correct per ASC 606-10-25-1."},
                {"text": "Incorrect application of ASC 606 standard.", "isCorrect": False, "explanation": "Violates ASC 606 guidelines."}
            ],
            "correct_idx": 0,
            "remediation": "ASC 606 requires a 5-step model: 1. Contract 2. Performance Obligations 3. Price 4. Allocate 5. Recognize."
        })

    # Week 5: ASC 842 Leases
    for i in range(15):
        questions.append({
            "week": 5,
            "concept_name": f"ASC 842 Leases #{i+1}",
            "scenario": f"Company enters into a 5-year lease for equipment with a 6-year useful life. Present value of payments is 92% of fair value. Classify the lease under ASC 842.",
            "options": [
                {"text": "Finance Lease", "isCorrect": True, "explanation": "Meets the 75% useful life test (5/6 = 83.3%) and 90% PV test (92%)."},
                {"text": "Operating Lease", "isCorrect": False, "explanation": "Fails operating lease criteria because finance lease thresholds are exceeded."},
                {"text": "Short-term Lease", "isCorrect": False, "explanation": "Lease term is > 12 months."}
            ],
            "correct_idx": 0,
            "remediation": "ASC 842 Finance Lease criteria (O-P-N-T-S): Ownership transfer, Purchase option, NPV >= 90%, Term >= 75% life, Specialized asset."
        })
        
    # Remaining FAR weeks
    for w in [2, 4, 6, 7]:
        for i in range(10):
            questions.append({
                "week": w,
                "concept_name": f"FAR Concept Week {w} - Q{i+1}",
                "scenario": f"FAR Financial Statement & GAAP accounting evaluation for Week {w} concept {i+1}.",
                "options": [
                    {"text": "GAAP Compliant Financial Statement Treatment", "isCorrect": True, "explanation": "Correct under US GAAP rules."},
                    {"text": "Non-compliant Accounting Treatment", "isCorrect": False, "explanation": "Violates FASB ASC codification standards."}
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
            "scenario": f"Auditor evaluates management's philosophy, organizational structure, and 'Tone at the Top'.",
            "options": [
                {"text": "Control Environment", "isCorrect": True, "explanation": "Control Environment is the foundational component of COSO (Tone at the Top)."},
                {"text": "Risk Assessment", "isCorrect": False, "explanation": "Incorrect component."},
                {"text": "Control Activities", "isCorrect": False, "explanation": "Incorrect component."}
            ],
            "correct_idx": 0,
            "remediation": "The 5 COSO components are CRIME (Control Environment, Risk Assessment, Information & Communication, Monitoring, Existing Control Activities)."
        })

    # Week 2: Risk Assessment & Audit Risk Model (AU-C 315 / AU-C 320)
    for i in range(10):
        questions.append({
            "week": 2,
            "concept_name": f"Audit Risk Model & Materiality Q{i+1}",
            "scenario": f"An engagement team assesses Inherent Risk as High and Control Risk as High for inventory valuation. How should Detection Risk be set under AU-C 315?",
            "options": [
                {"text": "Detection Risk must be set Low, requiring more extensive substantive procedures", "isCorrect": True, "explanation": "Audit Risk = IR × CR × DR. If RMM (IR × CR) is High, Detection Risk must be set Low to keep overall Audit Risk acceptably low."},
                {"text": "Detection Risk should be set High to reduce audit hours", "isCorrect": False, "explanation": "Setting DR High when RMM is High results in unacceptably high audit risk."},
                {"text": "Detection Risk is fixed by GAAS and cannot be altered", "isCorrect": False, "explanation": "Detection Risk is controlled and adjusted by the auditor."}
            ],
            "correct_idx": 0,
            "remediation": "Audit Risk = Inherent Risk × Control Risk × Detection Risk. Higher RMM requires lower Detection Risk and more substantive evidence."
        })

    # Week 3: Audit Evidence & Sampling (AU-C 500 / AU-C 530)
    for i in range(10):
        questions.append({
            "week": 3,
            "concept_name": f"Audit Evidence & Sampling Q{i+1}",
            "scenario": f"The audit team is choosing between audit evidence sources for accounts receivable. Which evidence source provides the highest reliability under AU-C 500?",
            "options": [
                {"text": "Direct external confirmation received directly from debtor third parties", "isCorrect": True, "explanation": "Direct external written confirmations from independent third parties provide higher reliability than client internal records."},
                {"text": "Management representations in an internal memo", "isCorrect": False, "explanation": "Management statements have lower reliability than independent external evidence."},
                {"text": "Inquiries of client accounting staff", "isCorrect": False, "explanation": "Oral inquiries alone do not provide sufficient appropriate audit evidence."}
            ],
            "correct_idx": 0,
            "remediation": "Evidence reliability hierarchy: Direct external evidence > Auditor direct observation > Internal documents with effective controls > Internal documents alone."
        })

    # Week 4: Audit Reports & Opinions (AU-C 700 / AU-C 705)
    for i in range(10):
        questions.append({
            "week": 4,
            "concept_name": f"Audit Opinions & Reports Q{i+1}",
            "scenario": f"A client refused to allow the auditor to observe physical inventory (representing 45% of total assets), and no alternative procedures were possible. What audit opinion should be issued under AU-C 705?",
            "options": [
                {"text": "Disclaimer of Opinion due to a material and pervasive scope limitation", "isCorrect": True, "explanation": "A severe, material, and pervasive scope limitation prevents the auditor from forming an opinion, requiring a Disclaimer of Opinion."},
                {"text": "Unmodified Opinion with Emphasis-of-Matter", "isCorrect": False, "explanation": "An unmodified opinion cannot be issued when a material scope limitation exists."},
                {"text": "Adverse Opinion", "isCorrect": False, "explanation": "Adverse opinions are issued for material and pervasive GAAP departures, not scope limitations."}
            ],
            "correct_idx": 0,
            "remediation": "Scope Limitation (Material & Pervasive) = Disclaimer of Opinion. GAAP Departure (Material & Pervasive) = Adverse Opinion."
        })

    # Week 5: Integrated Audits & ICFR (PCAOB AS 2201 / AU-C 940)
    for i in range(10):
        questions.append({
            "week": 5,
            "concept_name": f"ICFR Deficiencies & Integrated Audits Q{i+1}",
            "scenario": f"During an integrated audit, the auditor discovers a deficiency where a single officer can approve and execute wire transfers up to $500,000 without oversight. There is a reasonable possibility a material misstatement would not be prevented. How should this deficiency be classified?",
            "options": [
                {"text": "Material Weakness requiring an adverse opinion on internal control over financial reporting", "isCorrect": True, "explanation": "A deficiency or combination of deficiencies resulting in a reasonable possibility of material misstatement is a Material Weakness."},
                {"text": "Significant Deficiency communicated only to management", "isCorrect": False, "explanation": "Reasonable possibility of material misstatement elevates the deficiency to a Material Weakness."},
                {"text": "Minor Control Deficiency requiring no formal communication", "isCorrect": False, "explanation": "Lack of segregation of duties over major funds is at least a significant deficiency or material weakness."}
            ],
            "correct_idx": 0,
            "remediation": "Material Weakness = Reasonable possibility of material misstatement. Results in adverse ICFR opinion."
        })

    # Week 6: Attestation & Review Engagements (SSARS / SSAE)
    for i in range(10):
        questions.append({
            "week": 6,
            "concept_name": f"SSARS Review & Compilation Standards Q{i+1}",
            "scenario": f"A CPA is engaged to perform a Financial Statement Review under SSARS. What level of assurance does the CPA provide?",
            "options": [
                {"text": "Limited (Negative) Assurance based on inquiry and analytical procedures", "isCorrect": True, "explanation": "Reviews under SSARS provide limited/negative assurance using analytical procedures and inquiry, without testing controls or substantive sampling."},
                {"text": "Reasonable (Positive) Assurance based on audit sampling", "isCorrect": False, "explanation": "Reasonable assurance is provided only in full audit engagements."},
                {"text": "Zero Assurance", "isCorrect": False, "explanation": "Compilations provide zero assurance; Reviews provide limited assurance."}
            ],
            "correct_idx": 0,
            "remediation": "Audit = Reasonable/Positive Assurance. Review (SSARS) = Limited/Negative Assurance. Compilation = No Assurance."
        })

    return questions

def get_reg_questions():
    questions = []
    
    # Week 1: Individual Taxation & Gross Income (IRC § 61, § 102, § 103)
    for i in range(10):
        questions.append({
            "week": 1,
            "concept_name": f"Individual Gross Income & Deductions Q{i+1}",
            "scenario": f"Taxpayer receives $5,000 in interest from Municipal Bonds issued by the State of Ohio and $3,000 in dividends from US corporate stock. How much is included in Gross Income under IRC § 61 and § 103?",
            "options": [
                {"text": "$3,000 (Municipal bond interest is excluded under IRC § 103)", "isCorrect": True, "explanation": "IRC § 103 excludes state and municipal bond interest from gross income. Corporate dividends are fully taxable under IRC § 61."},
                {"text": "$8,000 (All income is fully taxable)", "isCorrect": False, "explanation": "Fails to apply IRC § 103 municipal bond exclusion."},
                {"text": "$0 (Both items are excluded)", "isCorrect": False, "explanation": "Corporate dividends are not exempt."}
            ],
            "correct_idx": 0,
            "remediation": "IRC § 61 includes all income from whatever source derived. IRC § 103 specifically excludes state/local municipal bond interest."
        })

    # Week 2: Property Transactions & Capital Gains (IRC § 1001, § 1031, § 1231)
    for i in range(10):
        questions.append({
            "week": 2,
            "concept_name": f"Property Transactions & Like-Kind Exchange Q{i+1}",
            "scenario": f"Taxpayer exchanges real property held for investment (adjusted basis $200,000) for like-kind real property valued at $250,000 plus $20,000 cash (boot). What is the recognized gain under IRC § 1031?",
            "options": [
                {"text": "$20,000 recognized gain (lesser of realized gain $70K or boot received $20K)", "isCorrect": True, "explanation": "Realized gain = ($250K + $20K) - $200K = $70,000. Recognized gain under § 1031 is capped at boot received ($20,000)."},
                {"text": "$70,000 recognized gain", "isCorrect": False, "explanation": "Gain in a § 1031 like-kind exchange is deferred except to the extent of boot received."},
                {"text": "$0 recognized gain", "isCorrect": False, "explanation": "Receipt of cash boot triggers gain recognition up to the boot amount."}
            ],
            "correct_idx": 0,
            "remediation": "IRC § 1031 Like-Kind Exchanges apply ONLY to real property. Gain recognized = Lesser of Realized Gain OR Boot Received."
        })

    # Week 3: Corporate Taxation & 6 Differentiated Scenarios (IRC § 172, § 162, § 163, § 243)
    reg_w3_scenarios = [
        {
            "name": "NOL 80% Taxable Income Limit (IRC § 172)",
            "scenario": "A C-Corporation has 2026 taxable income of $500,000 before NOL deduction. It has a post-2017 NOL carryforward of $600,000. Under IRC § 172(a), what is the maximum NOL deduction allowed for 2026?",
            "options": [
                {"text": "$400,000 (80% of $500,000 taxable income)", "isCorrect": True, "explanation": "TCJA IRC § 172 limits NOL deductions for post-2017 losses to 80% of taxable income before the deduction ($500K × 80% = $400K)."},
                {"text": "$500,000 (100% of taxable income)", "isCorrect": False, "explanation": "100% offset applied prior to TCJA and temporarily under CARES Act, but 80% limit applies in 2026."},
                {"text": "$600,000 (Full NOL balance)", "isCorrect": False, "explanation": "NOL deduction cannot exceed 80% of taxable income."}
            ],
            "correct_idx": 0,
            "remediation": "Post-2017 NOLs offset up to 80% of taxable income. Unused NOLs ($200K) carry forward indefinitely."
        },
        {
            "name": "NOL Carryforward & Carryback Rules (TCJA § 172)",
            "scenario": "A C-Corporation incurs a Net Operating Loss of $150,000 in tax year 2025. How does the corporation treat this loss under current IRC § 172 rules?",
            "options": [
                {"text": "Carry forward indefinitely; no carryback allowed", "isCorrect": True, "explanation": "Under TCJA provisions applicable in 2026, post-2017 corporate NOLs cannot be carried back, but carry forward indefinitely."},
                {"text": "Carry back 2 years, carry forward 20 years", "isCorrect": False, "explanation": "2-year carryback / 20-year carryforward was the pre-TCJA rule."},
                {"text": "Carry back 5 years under CARES Act", "isCorrect": False, "explanation": "CARES Act 5-year carryback applied only to 2018-2020 losses."}
            ],
            "correct_idx": 0,
            "remediation": "Post-2017 corporate NOLs: 0-year carryback, Indefinite carryforward (subject to 80% taxable income limit)."
        },
        {
            "name": "Book-to-Tax M-1 Reconciliation (IRC § 265)",
            "scenario": "Apex Corp reports Net Book Income of $300,000. Items include $15,000 in tax-exempt municipal bond interest and $25,000 in Federal income tax expense. What is Apex's Taxable Income on Schedule M-1?",
            "options": [
                {"text": "$310,000 ($300K - $15K muni interest + $25K tax expense)", "isCorrect": True, "explanation": "Subtract non-taxable muni interest ($15K) and add back non-deductible federal tax expense ($25K): $300K - $15K + $25K = $310K."},
                {"text": "$300,000", "isCorrect": False, "explanation": "Fails to adjust for M-1 book-tax differences."},
                {"text": "$340,000", "isCorrect": False, "explanation": "Incorrect math on M-1 reconciliation items."}
            ],
            "correct_idx": 0,
            "remediation": "Schedule M-1: Taxable Income = Book Income - Tax-Exempt Income + Non-Deductible Expenses."
        },
        {
            "name": "Executive Compensation Limit (IRC § 162(m))",
            "scenario": "A publicly held C-Corporation pays its CEO $2,500,000 in annual base salary. Under IRC § 162(m), how much of this compensation is deductible by the corporation?",
            "options": [
                {"text": "$1,000,000 max deduction ($1.5M disallowed under § 162(m))", "isCorrect": True, "explanation": "IRC § 162(m) caps the corporate tax deduction for covered executive compensation at $1,000,000 per year."},
                {"text": "$2,500,000 full deduction", "isCorrect": False, "explanation": "Violates § 162(m) executive comp cap for public companies."},
                {"text": "$0 deduction", "isCorrect": False, "explanation": "Deduction is capped at $1M, not eliminated."}
            ],
            "correct_idx": 0,
            "remediation": "IRC § 162(m) limits public company compensation deduction to $1,000,000 for covered employees."
        },
        {
            "name": "Business Interest Expense Limitation (IRC § 163(j))",
            "scenario": "A C-Corporation with $50M average gross receipts has Adjusted Taxable Income (ATI) of $1,000,000 and business interest expense of $400,000. Under IRC § 163(j), what is the interest deduction cap?",
            "options": [
                {"text": "$300,000 deduction (30% of $1,000,000 ATI; $100K carried forward)", "isCorrect": True, "explanation": "IRC § 163(j) limits business interest expense deduction to 30% of ATI ($1M × 30% = $300K). Excess $100K carries forward indefinitely."},
                {"text": "$400,000 full deduction", "isCorrect": False, "explanation": "Exceeds 30% ATI statutory cap under § 163(j)."},
                {"text": "$150,000 deduction", "isCorrect": False, "explanation": "Incorrect percentage calculation."}
            ],
            "correct_idx": 0,
            "remediation": "IRC § 163(j) caps business interest expense deduction at 30% of Adjusted Taxable Income (ATI)."
        },
        {
            "name": "Dividends Received Deduction (IRC § 243)",
            "scenario": "A C-Corporation receives a $100,000 dividend from an un-affiliated domestic corporation in which it owns a 15% voting equity stake. What is the Dividends Received Deduction (DRD) under IRC § 243?",
            "options": [
                {"text": "$50,000 DRD (50% deduction for <20% ownership)", "isCorrect": True, "explanation": "Under current DRD rules: <20% ownership = 50% DRD ($50,000); 20%-80% ownership = 65% DRD; ≥80% ownership = 100% DRD."},
                {"text": "$65,000 DRD", "isCorrect": False, "explanation": "65% DRD applies to 20%-80% ownership stakes."},
                {"text": "$100,000 DRD", "isCorrect": False, "explanation": "100% DRD applies only to affiliated group members (≥80% ownership)."}
            ],
            "correct_idx": 0,
            "remediation": "DRD Tiers (IRC § 243): <20% ownership -> 50% DRD; 20%-80% -> 65% DRD; ≥80% -> 100% DRD."
        }
    ]

    for i in range(15):
        s_idx = i % len(reg_w3_scenarios)
        sc = reg_w3_scenarios[s_idx]
        questions.append({
            "week": 3,
            "concept_name": f"{sc['name']} - Case #{i+1}",
            "scenario": sc["scenario"],
            "options": sc["options"],
            "correct_idx": sc["correct_idx"],
            "remediation": sc["remediation"]
        })

    # Week 4: Entity Choice & S-Corp / Partnership Tax (IRC § 704, § 1366)
    for i in range(10):
        questions.append({
            "week": 4,
            "concept_name": f"Pass-Through Entity Taxation Q{i+1}",
            "scenario": f"An S-Corporation has 2 equal shareholders. The S-Corp generates $100,000 in ordinary business income and $10,000 in charitable contributions. How are these reported on Schedule K-1 under IRC § 1366?",
            "options": [
                {"text": "Separately stated: Each shareholder receives $50,000 ordinary income and $5,000 charitable contribution", "isCorrect": True, "explanation": "S-Corp items that affect individual tax liability differently (like charitable contributions) must be separately stated on Schedule K-1."},
                {"text": "Net together: Report $45,000 net ordinary income per shareholder", "isCorrect": False, "explanation": "Charitable contributions cannot be netted into ordinary business income."},
                {"text": "Taxed at S-Corp entity level at 21%", "isCorrect": False, "explanation": "S-Corporations are pass-through entities and generally pay no entity-level income tax."}
            ],
            "correct_idx": 0,
            "remediation": "IRC § 1366 requires S-Corporations to pass through non-separately computed income and separately stated items (charitable contributions, capital gains) to K-1s."
        })

    # Week 5: Ethics & Treasury Circular 230
    for i in range(10):
        questions.append({
            "week": 5,
            "concept_name": f"Treasury Circular 230 & CPA Ethics Q{i+1}",
            "scenario": f"A CPA discovers an error in a client's previously filed tax return during an ongoing IRS audit. Under Circular 230 § 10.21, what action MUST the CPA take?",
            "options": [
                {"text": "Promptly advise the client of the error and the consequences, but do NOT notify the IRS without client consent", "isCorrect": True, "explanation": "Circular 230 § 10.21 requires the practitioner to inform the client of the error and potential tax consequences, but duty of confidentiality forbids notifying the IRS directly without client authorization."},
                {"text": "Notify the IRS immediately to avoid preparer penalties", "isCorrect": False, "explanation": "Direct IRS notification without client consent violates confidentiality and AICPA Code of Professional Conduct."},
                {"text": "Ignore the error if it is under $10,000", "isCorrect": False, "explanation": "Practitioner must advise the client of known errors regardless of amount."}
            ],
            "correct_idx": 0,
            "remediation": "Circular 230 § 10.21: Advise client of error and consequences. Do not inform IRS directly without client permission."
        })

    # Week 6: Business Law, Agency & UCC Article 2
    for i in range(10):
        questions.append({
            "week": 6,
            "concept_name": f"UCC Article 2 & Agency Law Q{i+1}",
            "scenario": f"A merchant signs a written offer to sell 100 industrial valves to a buyer, promising in writing to keep the offer open for 60 days without receiving cash consideration. On Day 20, the merchant attempts to revoke. Under UCC § 2-205 (Merchant's Firm Offer), is the revocation valid?",
            "options": [
                {"text": "Invalid: The firm offer is irrevocable for up to 3 months without consideration if signed in writing by a merchant", "isCorrect": True, "explanation": "UCC § 2-205 Merchant's Firm Offer rule: Written, signed offer by a merchant to keep an offer open is irrevocable without consideration for the stated time (up to 3 months)."},
                {"text": "Valid: Offers without consideration can always be revoked at any time", "isCorrect": False, "explanation": "Fails to recognize UCC § 2-205 exception to common law consideration rules."},
                {"text": "Invalid: Firm offers remain open indefinitely for 10 years", "isCorrect": False, "explanation": "UCC § 2-205 limits firm offers to a maximum of 3 months."}
            ],
            "correct_idx": 0,
            "remediation": "UCC § 2-205 Merchant's Firm Offer: Signed writing by merchant = Irrevocable for specified time (max 3 months) even without consideration."
        })

    return questions

def get_all_questions():
    return {
        "FAR": get_far_questions(),
        "AUD": get_aud_questions(),
        "REG": get_reg_questions()
    }

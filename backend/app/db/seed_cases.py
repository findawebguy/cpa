import json

def get_case_studies():
    return [
        {
            "course": "FAR",
            "title": "Comprehensive Accounting Cycle & Revenue Recognition Simulation",
            "description": "Review the provided exhibits for Apex Corp and evaluate the year-end adjustments and revenue recognition under ASC 606.",
            "scenario_text": "Apex Corp is a software and consulting firm. It is December 31, 2026, and you are preparing the final year-end adjusting entries and reviewing revenue contracts.",
            "exhibits_html": '''
                <div class="space-y-4">
                    <div class="p-4 border rounded-lg bg-slate-50">
                        <h4 class="font-bold text-slate-800"><i class="fa-solid fa-file-invoice-dollar text-blue-500 mr-2"></i>Exhibit 1: Cloud Subscription Contract</h4>
                        <p class="text-sm mt-2">On October 1, 2026, Apex signed a 12-month cloud hosting contract with Client A for $120,000, receiving the full amount in cash upfront. The services are provided evenly over the 12 months.</p>
                        <div class="mt-3 pt-2 border-t text-xs text-slate-500">
                            <i class="fa-solid fa-link text-slate-400 mr-1"></i><b>Source Authority:</b> <a href="https://asc.fasb.org/" target="_blank" rel="noopener" class="text-blue-600 hover:underline">FASB ASC 606 Revenue Recognition Standard</a>
                        </div>
                    </div>
                    <div class="p-4 border rounded-lg bg-slate-50">
                        <h4 class="font-bold text-slate-800"><i class="fa-solid fa-file-signature text-green-500 mr-2"></i>Exhibit 2: Equipment Lease Agreement</h4>
                        <p class="text-sm mt-2">On January 1, 2026, Apex entered into a 5-year lease for servers. The servers have a useful life of 5 years. The present value of lease payments is $200,000, and the fair value of the servers is $210,000.</p>
                        <div class="mt-3 pt-2 border-t text-xs text-slate-500">
                            <i class="fa-solid fa-link text-slate-400 mr-1"></i><b>Source Authority:</b> <a href="https://asc.fasb.org/" target="_blank" rel="noopener" class="text-blue-600 hover:underline">FASB ASC 842 Leases Codification</a>
                        </div>
                    </div>
                </div>
            ''',
            "questions": [
                {
                    "question_text": "Based on Exhibit 1, how much revenue should Apex recognize for the year ended December 31, 2026?",
                    "options": [
                        {"text": "$30,000", "isCorrect": True},
                        {"text": "$120,000", "isCorrect": False},
                        {"text": "$10,000", "isCorrect": False},
                        {"text": "$0", "isCorrect": False}
                    ],
                    "correct_idx": 0,
                    "explanation_html": "<p>Apex provides the service evenly over 12 months ($10,000/month). By Dec 31, 3 months have passed (Oct, Nov, Dec). $10,000 x 3 = $30,000.</p>"
                },
                {
                    "question_text": "Based on Exhibit 2, how should Apex classify this lease under ASC 842?",
                    "options": [
                        {"text": "Operating Lease", "isCorrect": False},
                        {"text": "Finance Lease", "isCorrect": True},
                        {"text": "Short-term Lease", "isCorrect": False}
                    ],
                    "correct_idx": 1,
                    "explanation_html": "<p>The lease term (5 years) is 100% of the useful life (5 years), which meets the >= 75% criterion for a Finance Lease under ASC 842.</p>"
                }
            ]
        },
        {
            "course": "REG",
            "title": "CPA Exam Eligibility & 150-Credit Hour Rule Analysis",
            "description": "Evaluate state board educational requirements, course counting, and 150-hour credit rules for CPA licensure.",
            "scenario_text": "Candidate Jordan has completed 120 undergraduate semester hours in business administration and is planning their path toward the 150-credit hour requirement for CPA licensure.",
            "exhibits_html": '''
                <div class="space-y-4">
                    <div class="p-4 border rounded-lg bg-slate-50">
                        <h4 class="font-bold text-slate-800"><i class="fa-solid fa-newspaper text-indigo-500 mr-2"></i>Exhibit 1: CPA Licensure 150-Hour Credit Rule Guide</h4>
                        <p class="text-sm mt-2">State boards of accountancy require 150 semester hours of college credit to obtain a CPA license. While 120 hours are generally required to sit for the exam, 150 hours (including specific accounting and business concentrations) are required for full licensure.</p>
                        <div class="mt-3 pt-2 border-t text-xs text-slate-500">
                            <i class="fa-solid fa-arrow-up-right-from-square text-indigo-500 mr-1"></i><b>Source Article:</b> <a href="https://www.becker.com/blog/cpa/150-credit-hours-cpa-a-tale-of-courses-and-creative-counting" target="_blank" rel="noopener" class="text-blue-600 font-medium hover:underline">Becker CPA Blog - 150 Credit Hours CPA: A Tale of Courses and Creative Counting</a>
                        </div>
                    </div>
                    <div class="p-4 border rounded-lg bg-amber-50/70 border-amber-200">
                        <h4 class="font-bold text-amber-900"><i class="fa-solid fa-graduation-cap text-amber-600 mr-2"></i>Exhibit 2: 2025-2027 Emerging NASBA/AICPA UAA Alternative Pathway</h4>
                        <p class="text-sm mt-2 font-serif">In May 2025, NASBA and the AICPA approved an alternative Uniform Accountancy Act (UAA) pathway permitting candidates with a bachelor's degree (120 semester hours) + 2 years of verified professional accounting experience to qualify for full CPA licensure. Multiple state boards (including Alaska, Alabama, and Arizona) are enacting this alternative path alongside the traditional 150-hour route starting in 2026/2027.</p>
                        <div class="mt-3 pt-2 border-t text-xs text-slate-500">
                            <i class="fa-solid fa-link text-slate-400 mr-1"></i><b>Source Authority:</b> <a href="https://www.becker.com/blog/cpa/150-credit-hours-cpa-a-tale-of-courses-and-creative-counting" target="_blank" rel="noopener" class="text-blue-600 font-medium hover:underline">NASBA/AICPA UAA Licensure Pipeline Updates</a>
                        </div>
                    </div>
                </div>
            ''',
            "questions": [
                {
                    "question_text": "Under standard State Board regulations, what is the primary distinction between sitting for the CPA exam vs. initial CPA license issuance?",
                    "options": [
                        {"text": "Most jurisdictions allow candidates to sit at 120 semester hours, but require 150 semester hours for final licensure", "isCorrect": True},
                        {"text": "150 hours are required before sitting for any exam section in all 50 states", "isCorrect": False},
                        {"text": "120 hours grant automatic full licensure without work experience", "isCorrect": False}
                    ],
                    "correct_idx": 0,
                    "explanation_html": "<p>According to Becker CPA licensure guidance, most state boards permit candidates to sit for the CPA exam upon earning 120 credit hours (bachelor's degree), but require 150 total semester hours (plus work experience) to issue the official CPA license.</p>"
                },
                {
                    "question_text": "Based on Exhibit 2, how does the emerging 2025-2027 NASBA/AICPA Uniform Accountancy Act (UAA) alternative pathway modify traditional CPA licensure requirements?",
                    "options": [
                        {"text": "It permits candidates with a bachelor's degree (120 credit hours) to obtain licensure by completing 2 years of relevant work experience instead of 150 credit hours", "isCorrect": True},
                        {"text": "It eliminates the CPA exam requirement for master's degree graduates", "isCorrect": False},
                        {"text": "It requires 180 total credit hours for all future candidates starting 2026", "isCorrect": False}
                    ],
                    "correct_idx": 0,
                    "explanation_html": "<p>Under the updated NASBA/AICPA UAA model approved in 2025, states are introducing an additional pathway allowing a 120-hour bachelor's degree paired with 2 years of professional experience to qualify for initial licensure.</p>"
                }
            ]
        },
        {
            "course": "AUD",
            "title": "Audit Risk Assessment & Internal Control Testing",
            "description": "Evaluate audit risk components, COSO control deficiency identification, and audit report modification decisions.",
            "scenario_text": "You are the senior auditor on the annual financial statement audit of Sterling Manufacturing Co. During preliminary risk assessment, your team noted significant internal control changes.",
            "exhibits_html": '''
                <div class="space-y-4">
                    <div class="p-4 border rounded-lg bg-slate-50">
                        <h4 class="font-bold text-slate-800"><i class="fa-solid fa-clipboard-check text-indigo-500 mr-2"></i>Exhibit 1: Internal Control Interview Memo</h4>
                        <p class="text-sm mt-2">The company CFO recently bypassed standard authorization procedures to approve a $500,000 wire transfer to an off-shore vendor without dual signatures. Controls over inventory counts were also waived for two regional warehouses due to staffing shortages.</p>
                        <div class="mt-3 pt-2 border-t text-xs text-slate-500">
                            <i class="fa-solid fa-link text-slate-400 mr-1"></i><b>Source Authority:</b> <a href="https://www.coso.org/" target="_blank" rel="noopener" class="text-blue-600 hover:underline">COSO Internal Control Integrated Framework</a>
                        </div>
                    </div>
                </div>
            ''',
            "questions": [
                {
                    "question_text": "Based on Exhibit 1, what COSO internal control component is directly impaired by the CFO's management override?",
                    "options": [
                        {"text": "Control Environment (Tone at the Top)", "isCorrect": True},
                        {"text": "Information & Communication", "isCorrect": False},
                        {"text": "Monitoring Activities", "isCorrect": False}
                    ],
                    "correct_idx": 0,
                    "explanation_html": "<p>Management override directly undermines the Control Environment (Tone at the Top), which establishes ethical standards and control consciousness across the organization.</p>"
                }
            ]
        },
        {
            "course": "AUD",
            "title": "[LIVE FINANCIAL NEWS SIMULATION] Federal Reserve Interest Rate & Market Audit Impact",
            "description": "🌐 Real-Time Financial Data Case Study: Analyze macroeconomic news and federal interest rate adjustments on asset impairment and audit disclosures.",
            "scenario_text": "<b>[REAL-TIME MARKET NEWS SIMULATION]</b><br>The Federal Reserve has adjusted interest rates, causing benchmark bond yields to fluctuate. You are auditing Global Asset Management Corp's fixed-income portfolio and commercial real estate holdings as of the audit reporting date.",
            "exhibits_html": '''
                <div class="space-y-4">
                    <div class="p-4 border rounded-lg bg-blue-50/60 border-blue-200">
                        <div class="flex items-center gap-2 mb-2">
                            <span class="px-2 py-0.5 bg-blue-600 text-white font-bold text-[10px] rounded">LIVE NEWS FEED</span>
                            <h4 class="font-bold text-slate-900 text-sm">Exhibit 1: Real-Time Financial Market Update</h4>
                        </div>
                        <p class="text-xs text-slate-700 leading-relaxed">Central bank interest rate decisions have increased discount rates used in fair value cash flow models. Commercial real estate property values in urban sectors have declined 12% following recent macroeconomic shifts.</p>
                        <div class="mt-3 pt-2 border-t text-xs text-slate-500">
                            <i class="fa-solid fa-arrow-up-right-from-square text-blue-500 mr-1"></i><b>Live Source:</b> <a href="https://www.federalreserve.gov/monetarypolicy.htm" target="_blank" rel="noopener" class="text-blue-600 font-medium hover:underline">Federal Reserve Monetary Policy & Economic Statements</a>
                        </div>
                    </div>
                </div>
            ''',
            "questions": [
                {
                    "question_text": "How should the auditor evaluate the impact of these live financial market shifts on the client's commercial real estate asset valuations?",
                    "options": [
                        {"text": "Test for impairment under ASC 360 using updated higher discount rates in discounted cash flow models", "isCorrect": True},
                        {"text": "Ignore post-balance sheet market shifts as irrelevant to current financial statements", "isCorrect": False},
                        {"text": "Immediately write down all assets by 50% without testing", "isCorrect": False}
                    ],
                    "correct_idx": 0,
                    "explanation_html": "<p>Significant macroeconomic shifts and interest rate changes are trigger events requiring asset impairment testing under ASC 360/FASB standards using updated discount rates.</p>"
                }
            ]
        }
    ]

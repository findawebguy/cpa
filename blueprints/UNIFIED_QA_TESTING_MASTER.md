# Unified QA Testing Master Specification — CPA Interactive Study Guide Platform

**Target Environment:** `https://demo.i-te.am/cpa/` (Fallback: `http://localhost:8005/`)  
**Runtime Engine:** Browserless Chrome over CDP (Headless Chrome Automation)  
**Document Version:** 2.0 (Unified Master)  
**Last Updated:** 2026-07-24  

---

## 🎯 Executive Overview & Subagent Task Partitioning

This master document unifies all Quality Assurance (QA), financial accuracy, responsive layout, progression gating, and candidate experience testing for the **CPA Interactive Study Guide** platform. 

To maximize test efficiency and prevent state conflicts in the database, testing is partitioned into **four specialized subagent roles**. Each subagent must execute its assigned section under a dedicated user identity.

```mermaid
graph TD
    Master[Unified QA Master Task] --> Agent1[Subagent 1: UI & Responsive Layout QA]
    Master --> Agent2[Subagent 2: Financial Analyst & Codification QA]
    Master --> Agent3[Subagent 3: Adaptive Progression & Gating QA]
    Master --> Agent4[Subagent 4: Candidate Experience & Usability QA]

    Agent1 --> Output1[UI & Console Report]
    Agent2 --> Output2[Technical & Statutory Audit Report]
    Agent3 --> Output3[Curriculum Gating Report]
    Agent4 --> Output4[UX & Usability Report]
```

---

## 🔑 Global Subagent Authentication & Identity Protocol

> [!IMPORTANT]
> **Mandatory Unique Registration**:
> Prior to executing any test steps, every subagent **MUST** register a distinct email address using the format below. This guarantees that user progress, attempts, heatmap analytics, and audit logs are segregated cleanly in SQLite/Postgres.

| Subagent Role | Required Email Format | Test Password |
|---------------|----------------------|---------------|
| **Subagent 1: UI & Layout** | `qa_ui_agent_{timestamp_or_id}@cpa-qa.com` | `QAPass123!` |
| **Subagent 2: Financial Analyst** | `qa_analyst_{timestamp_or_id}@cpa-qa.com` | `QAPass123!` |
| **Subagent 3: Progression Gating** | `qa_curriculum_agent_{timestamp_or_id}@cpa-qa.com` | `QAPass123!` |
| **Subagent 4: Candidate Experience** | `qa_candidate_{timestamp_or_id}@cpa-qa.com` | `QAPass123!` |

**Registration Flow**:
1. Open target URL (`https://demo.i-te.am/cpa/`).
2. Click **Sign In / Register** in top header.
3. Fill email and password, click **Register**.
4. Confirm user identity badge renders in the top right header before starting test suite.

---

## 🤖 Section 1: Subagent 1 — UI, Responsive Layout & Console Health QA

**Assigned Subagent Role:** `UI & Responsive Layout QA Agent`  
**Identity:** `qa_ui_agent_{timestamp}@cpa-qa.com`  
**Primary Focus:** Cross-viewport visual fidelity, modal responsiveness, button alignments, zero console exceptions.

### 1.1 Responsive Navigation Bar Audit (Regression Fix Check)
- **Viewport Sizes:** `375px` (Mobile), `768px` (Tablet), `1280px` (Desktop).
- **Test Steps:**
  1. Set viewport to `375px`. Inspect global header and view-switcher sub-header.
  2. **Verify:** Root document width is strictly bounded ($375\text{px}$). No horizontal scrollbar appears on `body`.
  3. **Verify:** Primary navbar (`#tab-adaptive`, `#tab-study`, `#tab-simulation`, `#tab-casestudies`, `#tab-flashcards`, `#tab-analytics`) scrolls horizontally **within** its container (`overflow-x-auto min-w-max`).
  4. Repeat checks at `768px` and `1280px`.

### 1.2 Case Study Split-Screen Modal Breakpoint Audit (Regression Fix Check)
- **Test Steps:**
  1. Open `#casestudy-modal` by clicking **Case Studies** $\rightarrow$ **Launch Case Study #1**.
  2. At `1280px` (Desktop), verify modal renders a **50/50 side-by-side split screen**:
     - `#casestudy-left-pane` (Reading & Exhibits) occupies $50\%$ width (`md:w-1/2`).
     - `#casestudy-right-pane` (Questions & Submission Form) occupies $50\%$ width (`md:w-1/2`).
  3. At `375px` (Mobile), verify panes stack vertically without text clipping or horizontal overflow.

### 1.3 Remediation $\rightarrow$ Practical Application Visual Badges
- **Test Steps:**
  1. On any Adaptive Learn Path question (e.g. `FAR_w1_q0`), deliberately select a **WRONG** answer.
  2. **Verify:** The next screen renders an Amber **`WORKED EXAMPLE`** badge with a lightbulb icon.
  3. Click **Proceed to Practical Application**.
  4. **Verify:** The next screen renders a Blue/Sky **`PRACTICAL APPLICATION`** badge with a flask icon.
  5. **Verify:** The header badge MUST NEVER display `MODULE MASTERED` on an application node.
  6. Click **Return to Question**.
  7. **Verify:** Navigates back to the original question with identical scenario and choices intact.

### 1.4 DevTools Console & Error Monitoring
- **Requirement:** Zero uncaught JavaScript runtime exceptions or 404 network errors.
- **Critical Regression Test:** Finish a week, land on the completion screen, then click **Return to Syllabus**.
  - **Verify:** No `Uncaught TypeError: Cannot set properties of null (setting 'className') at switchView` occurs. View switches cleanly to the syllabus map.

---

## ⚖️ Section 2: Subagent 2 — Senior Financial Analyst & Statutory Codification QA

**Assigned Subagent Role:** `Senior Financial Analyst & CPA Quality Assurance Agent`  
**Identity:** `qa_analyst_{timestamp}@cpa-qa.com`  
**Primary Focus:** Technical accounting accuracy, FASB ASC / IRC / GAAS / COSO codification citations, live news feed ingestion, link security.

### 2.1 Accounting Technical Accuracy & Codification Audit
- **FASB ASC 606 (Revenue Recognition):**
  - Verify 5-step model (Identify Contract $\rightarrow$ Performance Obligations $\rightarrow$ Transaction Price $\rightarrow$ Allocate Price $\rightarrow$ Recognize Revenue).
  - Verify contract asset vs. accounts receivable distinction in Case Study 1.
- **FASB ASC 842 (Lease Accounting):**
  - Verify finance lease criteria mnemonic (**O-P-N-T-S**: Ownership transfer, Purchase option, Net Present Value $\ge 90\%$, Term $\ge 75\%$, Specialized nature).
- **REG IRC § 172 (Net Operating Losses):**
  - Verify post-2017 TCJA rules: $80\%$ taxable income limit, 0-year carryback, indefinite carryforward.
- **AICPA GAAS / PCAOB AS 2201 (Auditing):**
  - Verify ICFR Material Weakness vs. Significant Deficiency definitions and SSARS review vs. compilation standards.

### 2.2 REG Week 3 NOL 6-Scenario Differentiation Verification
- Audit all 6 question nodes in REG Week 3 (`REG_w3_q0` through `REG_w3_q5`) to confirm **6 distinct corporate tax scenarios**:
  1. *NOL 80% Taxable Income Limit (IRC § 172)*
  2. *NOL Indefinite Carryforward & 0-Year Carryback*
  3. *Schedule M-1 Book-to-Tax Reconciliation*
  4. *Executive Compensation $1,000,000 Cap (IRC § 162(m))*
  5. *Business Interest Expense 30% ATI Limitation (IRC § 163(j))*
  6. *Dividends Received Deduction (DRD) Tiers (IRC § 243: 50%, 65%, 100%)*

### 2.3 NASBA/AICPA UAA Alternative Pathway Exhibit Verification
- Open **Case Study 2 (REG)**.
- **Verify Exhibit 2:** Displays *2025–2027 Emerging NASBA/AICPA UAA Alternative Pathway* (120 credit hours / bachelor's degree + 2 years verified experience).
- **Verify Question 2:** Correctly tests the alternative licensure route against traditional 150-hour state requirements.

### 2.4 Live Market News Feed & Audit Endpoint (`/cases/live-news/feed`)
- **API Endpoint:** `GET /cpa/api/v1/cases/live-news/feed` (or `/api/v1/cases/live-news/feed`).
- **Verify:** Returns HTTP 200 OK with `status: "active"` and array of ingested live market case studies.
- **Verify LLM Dataset Audit Logs:** `GET /api/v1/cases/live-news/llm-dataset-logs` returns recorded prompts, completions, and latency.

### 2.5 External Source Link Security Audit
- Inspect all exhibit external hyperlinks (e.g. FASB ASC 606, Becker CPA 150-hour blog, COSO.org, Federal Reserve).
- **Verify:** All external `<a>` tags include `target="_blank"` **and** `rel="noopener"` (or `rel="noreferrer"`).
- **Verify:** No `javascript:` inline protocol injection risks exist.

---

## 🔒 Section 3: Subagent 3 — Adaptive Curriculum & Progression Gating QA

**Assigned Subagent Role:** `Adaptive Progression & Curriculum Gating Agent`  
**Identity:** `qa_curriculum_agent_{timestamp}@cpa-qa.com`  
**Primary Focus:** Graph-walk invariant verification, gating security, week unlock sequencing, state reset integrity.

### 3.1 Gating Invariant 1: Wrong Answer Never Completes a Week
- Submit an incorrect option to a question (e.g. `FAR_w1_q0`).
- **Verify:** `next_node_key` routes to `FAR_w1_q0_rem` (worked example) — **NEVER** to `FAR_w1_end`.
- **Verify:** In syllabus state (`GET /courses/FAR/syllabus`), Week 1 stays `in-progress` and Week 2 stays `locked`.

### 3.2 Gating Invariant 2: Dynamic Node Chain Integrity (`q -> _rem -> _app -> q`)
- Confirm every question node follows the complete 3-step loop upon incorrect submission:
  $$\text{Question Node } (q) \longrightarrow \text{Worked Example } (_rem) \longrightarrow \text{Practical Application } (_app) \longrightarrow \text{Question Node } (q)$$
- It MUST be impossible to reach `{TRACK}_w{w}_end` without correctly answering every question in that week.

### 3.3 Gating Invariant 3: Anti-Crafting Protection on End Nodes
- Execute a direct POST request to visit an end node without answering questions: `POST /api/v1/nodes/FAR_w1_end/visit`.
- **Verify:** Response returns `{"status": "success", "already_completed": false}` or `{"completed": false}`.
- **Verify:** Week 1 does **NOT** flip to `completed`, and Week 2 remains `locked`.

### 3.4 Gating Invariant 4: Sequential Week Unlocking
- Week $N+1$ MUST unlock ONLY after Week $N$ status is `completed`.
- Confirm Week 2 `start_node_key` is `null` while Week 2 is `locked`.

### 3.5 User Progress & Attempt Reset Integrity
- Trigger `POST /api/v1/auth/user/reset`.
- **Verify:** Wipes `UserProgress`, `TBSAttempt`, and `CaseAttempt` database records.
- **Verify:** Resets syllabus state back to initial state (Week 1 `in-progress`, Weeks 2–7 `locked`).

---

## 🎓 Section 4: Subagent 4 — Candidate Experience & Usability QA

**Assigned Subagent Role:** `Candidate Experience & Usability Agent`  
**Identity:** `qa_candidate_{timestamp}@cpa-qa.com`  
**Primary Focus:** End-to-end student journey, interactive tools, spaced repetition flashcards, UI micro-animations, toast feedback.

### 4.1 Study Hub & Structured Modules Audit
- Open **Study & Prep Hub**.
- Verify all 5 structured modules load with rich formatting:
  - `far-asc-606` (Revenue Recognition)
  - `far-asc-842` (Lease Accounting)
  - `aud-coso-ic` (COSO Internal Control)
  - `reg-corporate-nol` (Corporate Taxation & NOL)
  - `reg-ethics-circular230` (Treasury Circular 230 & Ethics)

### 4.2 Concept Flashcards & Spaced Repetition Box System
- Open **Concept Flashcards**.
- Verify cards load across FAR, AUD, and REG domains.
- Flip card, rate memory recall (Hard, Good, Easy), and verify box assignment advances (Box 1 $\rightarrow$ Box 2).

### 4.3 Task-Based Simulations (TBS) & Interactive Calculators
- Open **Task-Based Simulations (TBS)**.
- Load Journal Entry Simulation `tbs-1`.
- Verify interactive ledger tool (T-Account visualizer / Equation Balancer).
- Submit imbalanced journal entries $\rightarrow$ verify error toast: *"Total debits must equal credits at $13,700"*.
- Submit balanced, correct journal entries $\rightarrow$ verify score calculation and success state.

### 4.4 Admin Panel Ingestion Button & Toast Notifications
- Open **Admin Panel** modal.
- Click **Ingest Live News** button (`rss` icon).
- **Verify:** Animated glassmorphism toast notification system triggers:
  1. Loading toast with spinner (*"Ingesting live market news..."*).
  2. Green success toast (*"Live news ingestion complete!"*) or Amber rate limit warning.

---

## 📊 Unified Output Schema & Reporting Templates

Every subagent MUST compile its execution results into a markdown artifact inside `blueprints/` using the standardized schema below.

### Standard Subagent Markdown Report Template

```markdown
# [Subagent Name] Execution Report

**Role:** [UI / Financial Analyst / Progression Gating / Candidate Experience]  
**Identity:** `qa_[role]_{timestamp}@cpa-qa.com`  
**Target:** `https://demo.i-te.am/cpa/`  
**Execution Status:** [PASS / FAIL / PARTIAL]  

---

## 1. Scope & Verification Coverage
- [x] Check 1
- [x] Check 2

## 2. Detailed Findings & Evidentiary Log
| Test ID | Area | Status | Evidence Label | Observations |
|---------|------|--------|----------------|--------------|
| T-101   | ...  | PASS   | browser-verified | ... |

## 3. Discrepancies & Defect Reports (If Any)
### [Defect #1] Title
- **Severity:** [Critical / High / Medium / Low]
- **Component:** Component name
- **Reproduction:** Steps to reproduce
- **Expected vs Actual:** Explanation

## 4. Final Sign-off
- **Summary:** Concise conclusion.
```

---

## 🚀 Execution Command Matrix for Test Automation

Subagents can execute these test scripts directly from the workspace terminal:

```bash
# 1. Full Live Site End-to-End Walkthrough (33 Tests)
python qa_test_live.py https://demo.i-te.am/cpa

# 2. Pytest Unit & Progression Gating Test Suite (24 Tests)
python -m pytest backend/tests -v

# 3. Live News Feed Ingestion Endpoint Audit
python -c "
import urllib.request, json
req = urllib.request.Request('https://demo.i-te.am/cpa/api/v1/cases/live-news/feed')
with urllib.request.urlopen(req) as resp:
    print(json.loads(resp.read().decode('utf-8')))
"
```

---

*Unified Master QA Specification complete. Ready for Browserless CDP subagent execution.* 🛡️

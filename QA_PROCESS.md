# CPA Exam Platform - Comprehensive QA Testing Manual & Subagent Protocol

This document outlines the end-to-end Quality Assurance (QA) testing protocol for the **CPA Exam Adaptive Learning & Task Simulation Platform**. It is designed for human QA engineers as well as autonomous QA agents/subagents running on remote machines.

---

## 📋 System Architecture & Test Target

- **Base URL (Local)**: `http://localhost:8005/api/v1` (or subpath `/cpa/api/v1`)
- **Base URL (Live Demo)**: `https://demo.i-te.am/cpa/api/v1`
- **Default Test User**: `student@cpa.com` / `pass123`
- **Database Engine**: SQLite 3 (WAL mode) with SQLAlchemy 2.0 ORM

---

## 🛠️ Environment Setup & Quick Verification

### 1. Local Machine Setup
```bash
git clone https://github.com/findawebguy/cpa.git
cd cpa
python -m venv .venv
source .venv/bin/activate  # On Windows: .\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python -m uvicorn backend.app.main:app --host 0.0.0.0 --port 8005
```

### 2. Run Automated Pytest Suite
```bash
python -m pytest backend/tests -v
```
*(All 16 unit/integration tests must pass cleanly).*

### 3. Run Automated End-to-End Live QA Suite
```bash
$env:PYTHONIOENCODING='utf-8'; python qa_test_live.py
```
*(Executes 47 automated assertion checks against the target backend).*

---

## 🧪 Comprehensive QA Test Suites

### Suite 1: Authentication, QR Passkey Sync & Guest Session Migration

#### 1.1 Standard Login & Registration
- **Action**: Perform `POST /auth/login` with `{"email": "student@cpa.com", "password": "pass123"}`.
- **Expected Outcome**: HTTP 200 returned with valid `access_token` JWT string.
- **Header Check**: Subsequent requests must include `Authorization: Bearer <TOKEN>`.

#### 1.2 QR Mobile Passkey Authentication
- **Action**: 
  1. Call `POST /auth/qr-session` to generate a desktop QR auth token.
  2. Poll `GET /auth/qr-status?qr_token=<TOKEN>`.
  3. Simulate mobile scan by calling `POST /auth/qr-login?qr_token=<TOKEN>` with user credentials.
- **Expected Outcome**: Polling watcher returns `{"scanned": true, "access_token": "..."}`, automatically authenticating the desktop UI.

#### 1.3 Guest LocalStorage Session Migration
- **Action**: Perform guest attempts in local storage while logged out, then call `POST /auth/migrate-guest-session`.
- **Expected Outcome**: Guest progress entries are merged into the user account in the database without data loss.

---

### Suite 2: Sequential Week Progression & State Validation (Happy Path)

#### 2.1 Syllabus Initial State
- **Action**: Call `GET /courses/FAR/syllabus`.
- **Expected Outcome**:
  - Week 1: `status="in-progress"` or `"unlocked"`, `start_node_key="q1"`.
  - Weeks 2–7: `status="locked"`, `start_node_key=null`.
  - Node counts clearly indicate core questions and remediation branches (e.g. `3 Core Questions • 4 Remediations`).

#### 2.2 Core Question Progression (Happy Path)
- **Action**:
  1. Submit correct answer to `q1` (`index=0`, `confidence="high"`). Verify routing to `q2`.
  2. Submit correct answer to `q2` (`index=1`, `confidence="medium"`). Verify routing to `q3`.
  3. Submit correct answer to `q3` (`index=0`, `confidence="medium"`). Verify routing to `finish_w1`.
  4. Call `POST /nodes/finish_w1/visit` to record end-node visit.
- **Expected Outcome**:
  - `GET /courses/FAR/syllabus` shows Week 1 `status="completed"`.
  - Week 2 transitions to `status="unlocked"` with `start_node_key="far_w2_q1"`.
  - Week 3+ remain strictly `status="locked"`.

---

### Suite 3: Adaptive Engine & Remediation Loops (Non-Happy Paths)

#### 3.1 Overconfidence Penalty (High Confidence Error)
- **Action**: Submit an incorrect answer to `q1` (`index=1`, `confidence="high"`).
- **Expected Outcome**:
  - `mastery_delta` is heavily penalized (`-15.0`).
  - `confidence_evaluated` tag equals `"HIGH_OVERCONFIDENCE_ERROR"`.
  - `next_node_key` routes to remediation breakdown `rem1`.

#### 3.2 Remediation & Scaffolded Question Branching
- **Action**:
  1. Fetch remediation node `GET /nodes/rem1`.
  2. Verify `next_node_key` points to scaffolded practice question `q1_easy`.
  3. Submit correct answer to `q1_easy` (`index=0`). Verify routing proceeds to core question `q2`.
- **Non-Happy Verification**:
  - Answering remediation nodes or `q1_easy` does **NOT** complete Week 1.
  - Week 2 remains `status="locked"` until all core questions + end-node visit are completed.

#### 3.3 Locked Week Click Protection
- **Action**: Attempt to call `GET /nodes/far_w3_q1` while Week 3 is locked.
- **Expected Outcome**:
  - API returns HTTP 403 or strips sensitive fields.
  - Frontend alerts user: *"Week 3 is locked! Complete all modules in Week 2 to unlock."*

---

### Suite 4: Task-Based Simulations (TBS)

#### 4.1 Fetching TBS Scenario
- **Action**: Call `GET /tbs/tbs-1`.
- **Expected Outcome**: Returns multi-exhibit scenario text, account list, and initial row template.

#### 4.2 Submitting Journal Entries & Balance Validation
- **Action**: Submit general journal rows to `POST /tbs/tbs-1/submit`.
- **Expected Outcome**:
  - Calculates total debits vs. credits.
  - If total score &ge; 75.0%, marks TBS attempt as passed.

---

### Suite 5: Admin & QA Overrides

#### 5.1 Admin Syllabus Overview
- **Action**: Call `GET /auth/admin/syllabus-overview`.
- **Expected Outcome**: Returns complete matrix of all 3 course tracks (FAR, AUD, REG), displaying week numbers, titles, question counts, attempted counts, and completion status.

#### 5.2 Admin Module Completion Override
- **Action**: Call `POST /auth/admin/complete-week` with `{"track": "FAR", "week_number": 2}`.
- **Expected Outcome**:
  - Creates UserProgress records for all nodes in Week 2.
  - Marks Week 2 `completed` and unlocks Week 3 (`far_w3_q1`) without requiring manual question solving.

#### 5.3 Reset Progress (QA Testing)
- **Action**: Call `POST /auth/user/reset`.
- **Expected Outcome**: Wipes user progress records and resets syllabus back to Week 1 initial state.

#### 5.4 Full Curriculum Re-seed
- **Action**: Call `POST /auth/admin/reseed`.
- **Expected Outcome**: Drops and re-creates all course/syllabus/learning node tables from `init_db.py`, ensuring fresh curriculum data.

---

## 🤖 QA Subagent Execution & Bug Reporting Protocol

When autonomous subagents are executed on external machines to perform QA, subagents must follow this standard report format upon discovering a bug or regression:

### Subagent Bug Report Template

```markdown
### 🐛 QA Bug Report

**Test Suite**: [e.g., Suite 3 - Remediation Branching]
**Target Environment**: [e.g., Live Server https://demo.i-te.am/cpa/ / Local localhost:8005]
**Timestamp**: [YYYY-MM-DD HH:MM:SS UTC]

#### Steps to Reproduce
1. Log in as student@cpa.com.
2. Submit incorrect answer to node `far_w2_q2`.
3. Check `GET /courses/FAR/syllabus`.

#### Expected Behavior
Week 3 remains `status="locked"` and Week 2 remains `status="in-progress"`.

#### Actual Behavior
Week 2 marked `status="completed"` and Week 3 unlocked prematurely.

#### API Log Trace / Raw Response
```json
{
  "status_code": 200,
  "response": { "week_number": 2, "status": "completed" }
}
```

#### Proposed Fix / Root Cause Hypothesis
Check line XX in `curriculum.py` for `all_questions_mastered` criteria.
```

---

## ✅ QA Checklist Summary

- [ ] `pytest backend/tests -v` (16/16 Passed)
- [ ] `qa_test_live.py` (47/47 Assertions Passed)
- [ ] Auth & QR Passkey Sync Verified
- [ ] Sequential Unlocking Enforced (Week N locked until Week N-1 complete)
- [ ] Remediation Nodes Route to Scaffolded Questions (`q1_easy`, `q2_easy`, etc.)
- [ ] Study & Prep Hub loads FASB ASC / AICPA / IRC Guides
- [ ] Admin QA Panel overrides tested (`complete-week`, `reseed`)

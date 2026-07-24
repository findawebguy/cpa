# CPA Interactive Study Guide - QA Process

This document outlines the Quality Assurance (QA) testing process for the CPA Interactive Study Guide platform. Subagents executing these tests should perform both **Happy Path** (expected behavior) and **Non-Happy Path** (error handling, boundary conditions) testing.

When executing these tests, agents should act as human users interacting with the frontend UI, but they may also inspect network requests (e.g., via browser devtools) to verify backend functionality.

---

## 🔑 Agent Identity & Test Tracking

> [!IMPORTANT]
> **Unique Agent Identity Requirement**:
> Each subagent MUST register and test under its own dedicated identity so that test attempts, case study submissions, and analytics diagnostics can be tracked individually in the database.
>
> - **Email Format**: `qa_agent_{agent_role}_{timestamp_or_id}@cpa-qa.com`
>   - Example UI Agent: `qa_ui_agent_101@cpa-qa.com`
>   - Example Financial Analyst: `qa_analyst_2026@cpa-qa.com`
> - **Password**: Use a standard test password (e.g., `QAPass123!`).
>
> **Execution**:
> 1. Upon launching the site, click the User Profile icon / **Sign In / Register** button.
> 2. Enter the unique agent email and password, then click **Register**.
> 3. Verify the user badge updates to reflect the agent's identity before commencing test execution.

---

## Environment Setup
- Ensure the backend FastAPI server (`uvicorn backend.app.main:app --host 0.0.0.0 --port 8005 --reload`) and frontend (serving `static/index.html`) are active.
- Access the application via `http://localhost:8005` or production URL (`https://demo.i-te.am/cpa/`).

---

## 1. Authentication & Session Management

### Happy Path
- **Registration**: Register a new user with the agent's unique email (`qa_agent_{id}@cpa-qa.com`). Verify that the user is logged in automatically and the dashboard updates with the agent's identity.
- **Login**: Log out and log back in with the agent's credentials. Verify successful authentication and data recovery.
- **Logout**: Click "Log Out" in the Settings modal. Verify the session clears and returns to guest mode.
- **Guest Migration**: Answer a question as a guest, then register the agent account. Verify guest progress migrates into the agent's profile.

### Non-Happy Path
- **Invalid Login**: Attempt login with an incorrect password. Verify clear error feedback ("Incorrect email or password").
- **Duplicate Registration**: Attempt to register an existing agent email again. Verify graceful 400 Bad Request handling.

---

## 2. Core Question Engine (Adaptive Track)

### Happy Path
- **Answer Correctly**: Select the correct option. Verify positive feedback, confetti trigger, and progression to the next Core Question (`Question X of 10`).
- **Answer Incorrectly**: Select an incorrect option. Verify the `PRINCIPLE REMEDIATION` view renders. Click **"Proceed to Practical Application"** and verify it routes directly back to the target question without 404 errors.
- **Completion**: Complete all 10 questions in a week. Verify the `MODULE MASTERED` view appears and syllabus status updates to Completed.

### Non-Happy Path
- **Unselected Submission**: Attempt submission without selecting an option. Verify submission is blocked or alerted.

---

## 3. Case Studies & Task-Based Simulations (TBS)

### Happy Path
- **Case Study Viewer**: Open the "Case Studies" tab. Launch a case study (e.g. AUD or REG 150-credit hour rule). Verify split-screen exhibit viewer and clickable source article links.
- **Case Study Submission**: Submit multi-part answers under the agent's identity. Verify score calculation and attempt persistence.
- **TBS Interactive Input**: Add/remove debit and credit rows in the TBS tool. Verify balance calculations update in real time.

### Non-Happy Path
- **Imbalanced TBS Submission**: Submit an imbalanced journal entry. Verify rejection alert.

---

## 4. Settings & Account Management

### Happy Path
- **Update Exam Date**: Open Settings Modal, set a target exam date, and click **Save Changes**. Verify persistence under the agent's profile.

---

## Reporting Guidelines for Subagents

When logging a bug or suggestion:
1. **Agent ID**: `qa_agent_{id}@cpa-qa.com`
2. **Title**: Clear, concise summary.
3. **Path**: Happy Path or Non-Happy Path.
4. **Steps to Reproduce**: Exact click sequence.
5. **Expected vs. Actual Result**.

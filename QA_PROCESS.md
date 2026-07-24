# CPA Interactive Study Guide - QA Process

This document outlines the Quality Assurance (QA) testing process for the CPA Interactive Study Guide platform. Subagents executing these tests should perform both **Happy Path** (expected behavior) and **Non-Happy Path** (error handling, boundary conditions) testing.

When executing these tests, agents should act as human users interacting with the frontend UI, but they may also inspect network requests (e.g., via browser devtools) to verify backend functionality.

**Objective**: Create detailed bug reports or actionable suggestions for any failures encountered during the process.

## Environment Setup
- The application runs locally. Ensure the backend FastAPI server (`uvicorn backend.app.main:app --reload`) and frontend (serving `static/index.html`) are active.
- Access the application via `http://localhost:8000` or the configured local domain (e.g., `http://127.0.0.1:8000`).

---

## 1. Authentication & Session Management

### Happy Path
- **Registration**: Register a new user with a valid email and password. Verify that the user is logged in automatically and the dashboard updates.
- **Login**: Log in with an existing user (e.g., `student@cpa.com` / `pass123`). Verify successful login and data loading.
- **Logout**: Click the "Log Out" button in the Settings modal. Verify the session clears and the UI returns to the guest state.
- **Guest Migration**: Answer a few questions as a guest, then register an account. Verify that the guest progress (score, current week) migrates to the newly created account.

### Non-Happy Path
- **Invalid Login**: Attempt to log in with an incorrect password. Verify the UI displays an appropriate error message (e.g., "Incorrect email or password") and does not crash.
- **Duplicate Registration**: Attempt to register an account with an email that already exists. Verify the UI gracefully handles the 400 Bad Request error.
- **Session Expiry**: Simulate an expired JWT token (if possible) and attempt an authenticated action (like saving progress). Verify the app prompts the user to log in again rather than failing silently.

---

## 2. Core Question Engine (Adaptive Track)

### Happy Path
- **Answer Correctly**: Select the correct answer for a question. Verify the feedback is positive, confetti triggers, and the "Next Question" button navigates to the next logical node in the sequence.
- **Answer Incorrectly**: Select an incorrect answer. Verify the UI displays the remediation view. Click "Proceed to Practical Application" and verify it navigates to a scaffolded/easier question or retries the concept.
- **Completion**: Complete all questions in a given week. Verify the "Week Mastered" node appears and the Syllabus view reflects completion (e.g., Week 1 gets a green checkmark).

### Non-Happy Path
- **Empty Submission**: Attempt to submit a question without selecting an option. Verify the UI prevents submission or alerts the user.
- **Network Failure During Submission**: Simulate a network disconnect just before answering. Verify the UI handles the API error gracefully (e.g., "Failed to save progress") without crashing.

---

## 3. Case Studies & Task-Based Simulations (TBS)

### Happy Path
- **Case Study Viewer**: Navigate to the "Case Studies" tab. Open a simulation. Verify the split-screen modal appears with exhibits on the left and questions on the right.
- **Case Study Submission**: Answer the questions and submit. Verify that the results show correct/incorrect highlights, explanations are revealed, and the score updates.
- **TBS Interactive Input**: Navigate to the "Task-Based Simulations (TBS)" tab. Add and remove journal entry rows. Input valid debits/credits. Verify the balance calculator updates accurately.
- **TBS Submission**: Submit a fully balanced, correct journal entry. Verify positive feedback and score update.

### Non-Happy Path
- **Imbalanced TBS Entry**: Submit a journal entry where debits do not equal credits. Verify the system rejects it and alerts the user of the imbalance.
- **Partial Case Study Submission**: Submit a case study with some questions left blank. Verify the system treats blank answers as incorrect but does not crash, or prompts the user to finish.
- **Missing Exhibits**: If a case study lacks exhibits (data error), verify the UI handles the missing data gracefully (e.g., displaying "No exhibits provided").

---

## 4. Settings & Account Management

### Happy Path
- **Update Settings**: Open the Settings Modal. Change the "Target CPA Exam Date" and submit. Verify the UI updates and the data persists across a page reload.
- **Change Password**: Enter a new password and save. Verify the update succeeds, and subsequent logins require the new password.

### Non-Happy Path
- **Invalid Password Update**: Attempt to change the password to a blank string or an invalid format. Verify the UI/API rejects it with a clear error message.

---

## 5. Admin Panel (Database Reseed)

### Happy Path
- **Open Admin Panel**: Navigate to Settings > QA/Admin Panel.
- **Reseed Database**: Click "Reseed Database". Acknowledge the critical warning. Verify the backend successfully rebuilds the curriculum and the frontend resets cleanly without infinite loading states.

### Non-Happy Path
- **Unauthorized Access**: Attempt to call the `/api/v1/auth/admin/syllabus-overview` endpoint using a non-admin token (or standard student token). Verify it returns a 403 Forbidden.

---

## Reporting Guidelines for Subagents

When logging a bug or suggestion:
1. **Title**: Clear, concise summary of the issue.
2. **Path**: Happy or Non-Happy.
3. **Steps to Reproduce**: Exact sequence of clicks/inputs.
4. **Expected vs. Actual Result**: What should have happened vs. what actually happened.
5. **Logs**: Include frontend console errors or backend stack traces if applicable.
6. **Suggested Fix**: (Optional) Provide code-level suggestions for resolving the issue.

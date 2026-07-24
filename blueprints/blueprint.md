# CPA Exam Adaptive Learning & Task Simulation Platform — Master Architectural Blueprint

## 1. Executive Summary & System Goals
The CPA Exam Adaptive Learning & Task Simulation Platform is a production-ready, full-stack web application designed to prepare candidates for the 2026 CPA Exam (FAR, AUD, and REG tracks). The system combines:
- An **Adaptive Engine** incorporating Bayesian Knowledge Tracing and Metacognition (Confidence Calibration).
- **Task-Based Simulations (TBS)** featuring interactive general journals, T-account visualizers, debit/credit balance checkers, and multi-exhibit case studies.
- **Leitner Spaced-Repetition Flashcards** indexed by CPA domain authority standards (ASC 606, ASC 842, COSO, IRC §102, etc.).
- **Diagnostic Analytics Dashboard** powered by Chart.js providing real-time readiness scoring, domain heatmaps, and personalized remediation paths.

---

## 2. Technology Stack & Directory Layout

### Tech Stack
- **Backend Framework**: Python 3.11+ with FastAPI & Pydantic v2
- **Database**: SQLite with SQLAlchemy 2.0 ORM, Alembic migrations, PRAGMA journal_mode=WAL, and PRAGMA foreign_keys=ON
- **Authentication**: OAuth2 Password Flow with JWT tokens, Argons2 / Bcrypt password hashing (`passlib` + `pwd_context`), stored in HTTP-Only Cookies / Authorization Headers
- **Frontend**: Single-Page Web Application (`static/index.html` + `static/api.js`) using Tailwind CSS, FontAwesome 6, Chart.js, Canvas-Confetti, and vanilla ES6+ async/await Fetch API
- **Testing**: `pytest`, `pytest-asyncio`, and `httpx`
- **Containerization**: `Dockerfile` and `docker-compose.yml` serving Uvicorn behind static file mounting

### Project Directory Structure
```
cpa/
├── blueprint.md
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
├── .env
├── alembic.ini
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── api/
│   │   │   └── v1/
│   │   │       ├── api.py
│   │   │       └── endpoints/
│   │   │           ├── auth.py
│   │   │           ├── curriculum.py
│   │   │           ├── simulations.py
│   │   │           ├── flashcards.py
│   │   │           └── analytics.py
│   │   ├── core/
│   │   │   ├── config.py
│   │   │   ├── security.py
│   │   │   └── adaptive_engine.py
│   │   ├── db/
│   │   │   ├── base.py
│   │   │   ├── session.py
│   │   │   └── init_db.py
│   │   ├── models/
│   │   │   ├── user.py
│   │   │   ├── curriculum.py
│   │   │   ├── simulation.py
│   │   │   └── flashcard.py
│   │   └── schemas/
│   │       ├── user.py
│   │       ├── curriculum.py
│   │       ├── simulation.py
│   │       ├── flashcard.py
│   │       └── analytics.py
│   └── tests/
│       ├── conftest.py
│       ├── test_auth.py
│       ├── test_adaptive_engine.py
│       ├── test_curriculum.py
│       └── test_simulations.py
└── static/
    ├── index.html
    └── api.js
```

---

## 3. Database Schema & Models Specification (`cpa_prep.db`)

SQLite is configured with Write-Ahead Logging (`PRAGMA journal_mode=WAL; PRAGMA foreign_keys=ON;`).

```
+------------------+       +-------------------+       +---------------------+
|      Users       |       |      Courses      |       |      Syllabus       |
+------------------+       +-------------------+       +---------------------+
| id (PK)          |----<  | id (PK)           |----<  | id (PK)             |
| email (Unique)   |       | code (FAR/AUD/REG)|       | course_id (FK)      |
| password_hash    |       | title             |       | week_number         |
| target_exam_date |       | description       |       | title               |
| created_at       |       +-------------------+       +---------------------+
+------------------+                                              |
         |                                                        |
         v                                                        v
+------------------+                                   +---------------------+
|  UserProgress    |                                   |    LearningNodes    |
+------------------+                                   +---------------------+
| id (PK)          |                                   | id (PK)             |
| user_id (FK)     |                                   | syllabus_id (FK)    |
| node_id (FK)     |                                   | node_key ("q1", etc)|
| mastery_level    |                                   | concept_name        |
| streak_days      |                                   | node_type           |
| confidence_rating|                                   | scenario_content    |
| last_activity    |                                   | options_json        |
+------------------+                                   | correct_answer_idx  |
                                                       | remediation_html    |
                                                       | next_correct_key    |
                                                       | next_incorrect_key  |
                                                       +---------------------+
```

### Table Details:
1. **users**: `id` (Integer PK), `email` (String Unique), `password_hash` (String), `target_exam_date` (DateTime/Date), `created_at` (DateTime).
2. **courses**: `id` (Integer PK), `code` (String: FAR, AUD, REG), `title` (String), `description` (Text).
3. **syllabus**: `id` (Integer PK), `course_id` (FK to courses.id), `week_number` (Integer), `title` (String).
4. **learning_nodes**: `id` (Integer PK), `syllabus_id` (FK to syllabus.id), `node_key` (String Unique per course/global), `concept_name` (String), `node_type` (String: question, remediation, end), `scenario_content` (Text), `options_json` (JSON), `correct_answer_idx` (Integer), `remediation_html` (Text), `next_correct_key` (String), `next_incorrect_key` (String).
5. **user_progress**: `id` (Integer PK), `user_id` (FK to users.id), `node_id` (FK to learning_nodes.id), `mastery_level` (Float), `streak_days` (Integer), `confidence_rating` (String: low, medium, high), `last_activity` (DateTime).
6. **tbs_scenarios**: `id` (Integer PK), `code` (String), `title` (String), `exhibit_html` (Text), `accounts_list_json` (JSON), `solution_mapping_json` (JSON).
7. **tbs_attempts**: `id` (Integer PK), `user_id` (FK to users.id), `scenario_id` (FK to tbs_scenarios.id), `submission_json` (JSON), `score` (Float), `is_balanced` (Boolean), `created_at` (DateTime).
8. **flashcards**: `id` (Integer PK), `domain` (String: FAR, AUD, REG), `category` (String), `question` (Text), `answer_html` (Text).
9. **flashcard_progress**: `id` (Integer PK), `user_id` (FK to users.id), `card_id` (FK to flashcards.id), `box_number` (Integer), `status` (String: review, mastered), `last_reviewed` (DateTime).

---

## 4. Adaptive Difficulty Engine & Metacognitive Calibration Rules

The adaptive engine resides in `app/core/adaptive_engine.py`.

### Metacognitive Calibration Matrix:
| Submitted Accuracy | Self-Assessed Confidence | System Action & Mastery Adjustment |
| :--- | :--- | :--- |
| **Incorrect** | **High** | **High Overconfidence Bias Error**: Divert immediately to deep remediation node (`next_incorrect_key`). Decrease domain mastery weight by **-15%**. |
| **Incorrect** | **Medium / Low** | Standard Remediation Path: Route to remediation node (`next_incorrect_key`). Adjust mastery weight by **-5%**. |
| **Correct** | **High** | **Mastery Acceleration**: Fast-track skip over baseline practice nodes directly to high-difficulty exam node (`next_correct_key`). Increase mastery weight by **+10%**. |
| **Correct** | **Low** | **Scaffolded Reinforcement**: Route to a scaffolded practice node (`next_correct_key`) to solidify confidence before advancing. Increase mastery weight by **+5%**. |

---

## 5. API Endpoint Specifications (`/api/v1`)

### Authentication & User Profile
- `POST /api/v1/auth/register`: Register user with email & password.
- `POST /api/v1/auth/login`: Authenticate credentials, return JWT access token and HTTP-only cookie.
- `GET /api/v1/user/profile`: Fetch current user stats, active streak, overall readiness index, and domain mastery breakdown.

### Adaptive Curriculum
- `GET /api/v1/courses`: List available exam tracks (FAR, AUD, REG) with progress.
- `GET /api/v1/courses/{track_code}/syllabus`: Get multi-week syllabus with completion/lock statuses.
- `GET /api/v1/nodes/{node_key}`: Fetch node payload for current track. (Options are stripped of `isCorrect` markers for client security).
- `POST /api/v1/nodes/{node_key}/submit`: Submit option index + confidence (`low`, `medium`, `high`). Returns correctness, detailed breakdown/explanation, mastery delta, and next target node key determined by the adaptive engine.

### Task-Based Simulations (TBS)
- `GET /api/v1/tbs/{simulation_id}`: Fetch simulation exhibits, instructions, and account dropdown choices.
- `POST /api/v1/tbs/{simulation_id}/submit`: Validate journal entries (account classifications, debit/credit matching, balance check). Returns detailed line-by-line feedback and score.

### Flashcards & Analytics
- `GET /api/v1/flashcards?domain={domain}`: Retrieve flashcards for spaced repetition.
- `POST /api/v1/flashcards/{card_id}/rate`: Submit Leitner rate (`mastered` | `review`), updating box number and review queue.
- `GET /api/v1/analytics/diagnostics`: Compute domain mastery heatmap data, weakness diagnostics, and exam readiness percentage for Chart.js.

---

## 6. Seed Data Specifications (`init_db.py`)
- **FAR Track (7 Weeks)**: Accounting Cycle, Financial Statements & Cash Flows, Revenue Recognition (ASC 606), PPE & Depreciation, Leases (ASC 842), Equity & EPS, Consolidations & Non-Profit.
- **AUD Track (6 Weeks)**: Ethics & Professional Responsibilities, COSO Framework & Internal Control, Risk Assessment & Audit Planning, Audit Evidence & Sampling, Audit Reports & Modifications, Integrated Audits & Attestation.
- **REG Track (6 Weeks)**: Individual Tax & Gross Income (IRC §102/103), Property Transactions & Basis, Corporate Income Tax, Entity Choice (S-Corp/Partner/LLC), Ethics & Tax Practice, Business Law & Contracts.
- **Task-Based Simulations**: At least 3 full simulations with multi-item exhibits (Adjusting Journal Entries, Revenue Allocation under ASC 606, Lease Classification & Amortization Schedule under ASC 842).
- **Flashcards**: 50+ high-yield cards across FAR, AUD, and REG.

---

## 7. Frontend Integration (`static/index.html` & `static/api.js`)
- Auth modal/JWT token management stored in `localStorage` & request headers.
- Async API client (`api.js`) seamlessly connecting single-page views to FastAPI endpoints.
- Real-time updates for streak counter, readiness score, audio synthesis, Chart.js heatmaps, and Confetti animations.

---

## 8. Quality Assurance & Testing Plan
- Unit and Integration tests using `pytest` & `httpx`:
  - Authentication flow (Register -> Login -> Protected endpoints).
  - Adaptive Engine decision tree (Correct + High Conf vs Incorrect + High Conf).
  - TBS scoring logic & balance validation.
  - Diagnostic calculation correctness.

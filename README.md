# CPA Exam Adaptive Learning & Task Simulation Platform

![CPA Evolution 2026](https://img.shields.io/badge/CPA--Exam-2026--Evolution-blue.svg)
![Python 3.11+](https://img.shields.io/badge/Python-3.11%2B-green.svg)
![FastAPI](https://img.shields.io/badge/Backend-FastAPI-009688.svg)
![SQLite WAL](https://img.shields.io/badge/Database-SQLite%20WAL-lightgrey.svg)
![Pytest](https://img.shields.io/badge/Testing-Pytest-yellow.svg)

A full-stack, adaptive CPA Exam preparation and simulation platform built for the **2026 CPA Evolution** standards across Financial Accounting & Reporting (**FAR**), Auditing & Attestation (**AUD**), and Regulation (**REG**).

---

## 🌟 Key Features

- 🧠 **Bayesian Adaptive Engine**: Evaluates correctness alongside self-assessed metacognitive confidence (`low`, `medium`, `high`). High-confidence errors trigger immediate deep principle remediations, while high-confidence correct answers accelerate candidates directly to advanced CPA exam nodes.
- 📱 **Mobile Passkey Login**: Use your phone camera to scan a QR code on desktop for instant auto-login session synchronization.
- 🔓 **Strict Sequential Progression**: Modules unlock sequentially upon completing preceding requirements, with complete state validation across tracks.
- 🛠️ **Admin & QA Overrides**: Built-in Admin QA panel allowing instant module completion overrides, progress resets, and full curriculum re-seeding for fast manual testing.
- 📊 **Task-Based Simulations (TBS)**: Interactive exam environment featuring multi-exhibit audit findings, general journal workbooks, account classification dropdowns, and automatic debit/credit balance checkers.
- 🃏 **Leitner Spaced-Repetition Flashcards**: 50+ high-yield concept cards indexed by FASB/AICPA/IRC codification standards (ASC 606, ASC 842, COSO Framework, IRC § 102/103).
- 📈 **Cognitive Diagnostics Dashboard**: Chart.js domain heatmaps, exam readiness index scoring, and weakness insights.
- ⚡ **SQLite Write-Ahead Logging (WAL)**: High-concurrency, fast, local embedded relational database powered by SQLAlchemy 2.0 ORM and Pydantic v2 schemas.

---

## 🛠️ Technology Stack

- **Backend**: Python 3.11+, FastAPI, Pydantic v2, PyJWT, Passlib (bcrypt)
- **Database**: SQLite with SQLAlchemy 2.0 (PRAGMA `journal_mode=WAL; foreign_keys=ON;`)
- **Frontend**: Single-Page Web Application (`static/index.html` + `static/api.js`) using Tailwind CSS, FontAwesome 6, Chart.js, and Canvas-Confetti
- **Testing**: Pytest, Pytest-Asyncio, HTTPX
- **Packaging**: Docker & Docker Compose

---

## 🚀 Quick Start / Setup Instructions

### Option 1: Local Python Environment

1. **Clone the Repository**
   ```bash
   git clone https://github.com/findawebguy/cpa.git
   cd cpa
   ```

2. **Create and Activate a Virtual Environment**
   - **Windows (PowerShell)**:
     ```powershell
     python -m venv .venv
     .\.venv\Scripts\Activate.ps1
     ```
   - **macOS / Linux**:
     ```bash
     python3 -m venv .venv
     source .venv/bin/activate
     ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Initialize Database** (Automatic on first startup, or run manually):
   ```bash
   python -m backend.app.db.init_db
   ```

5. **Start the FastAPI Application**
   ```bash
   python -m uvicorn backend.app.main:app --host 0.0.0.0 --port 8005
   ```

6. **Access the Application**
   - **Web App**: Open [http://localhost:8005](http://localhost:8005) in your web browser.
   - **Interactive API Documentation**: Open [http://localhost:8005/docs](http://localhost:8005/docs)

---

### Option 2: Run via Docker Compose

1. **Build and Launch Container**
   ```bash
   docker-compose up -d --build
   ```
2. **Access Web App**: Open [http://localhost:8005](http://localhost:8005)

---

## 🧪 Running the Test Suite

Run the full automated pytest suite (Auth, Adaptive Engine, Curriculum, TBS Scoring):
```bash
python -m pytest backend/tests -v
```

---

## 🛠️ Admin & QA Testing Overrides

### 1. In-App Admin QA Panel
- Click your profile button in the top right to open **Account & Exam Settings**.
- Click **`Admin / QA`** (`shield-halved` icon) to view all tracks (FAR, AUD, REG) and their week-by-week progress.
- Click **`Mark Done`** next to any week to instantly complete that module without needing accounting knowledge.
- Click **`Reset Progress`** to clear all attempts and start testing from Week 1.

### 2. Updating / Re-seeding Production Database
When deploying updates to production, re-seed the live database without server downtime via API:

```bash
# 1. Obtain Auth Token
TOKEN=$(curl -s -X POST https://demo.i-te.am/cpa/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"student@cpa.com","password":"pass123"}' | python3 -c "import sys,json; print(json.load(sys.stdin)['access_token'])")

# 2. Trigger Full Re-seed (Drops & Re-populates Curriculum from init_db.py)
curl -s -X POST https://demo.i-te.am/cpa/api/v1/auth/admin/reseed \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json"
```

---

## 📁 Repository Structure

```
cpa/
├── README.md
├── blueprint.md
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── backend/
│   ├── app/
│   │   ├── main.py                   # FastAPI entry point
│   │   ├── api/v1/                   # REST API routes
│   │   ├── core/                     # Security, config, adaptive engine
│   │   ├── db/                       # Session, WAL setup, init_db seed script
│   │   ├── models/                   # SQLAlchemy 2.0 ORM models
│   │   └── schemas/                  # Pydantic v2 data validation schemas
│   └── tests/                        # Pytest test suite
└── static/
    ├── index.html                    # Single-Page Frontend App
    └── api.js                        # Async API client
```

---

## 📝 License
Distributed under the MIT License.

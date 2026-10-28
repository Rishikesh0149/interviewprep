# PrepPilot (AI-Powered Career & Interview Co-Pilot)

PrepPilot is an AI-powered resume and interview preparation platform built natively with Python (FastAPI), SQLite, and React (TypeScript + Vite). The project is completely **Docker-free** and runs with zero external container dependencies.

---

## Architecture Overview

- **Backend**: FastAPI 0.115+ running on Python 3.12, SQLAlchemy with native SQLite, Pydantic v2, PyMuPDF for resume parsing, and Google GenAI / Offline Heuristic LLM engine.
- **Frontend**: React 19, TypeScript, Vite, Monaco Editor, TailwindCSS v4, Recharts, and Lucide React.
- **Database**: Local SQLite database (`preppilot.db`) with automatic table creation and automatic seed data initialization on first startup.

---

## Features

1. **Resume Lab**: PDF/text resume parsing, multi-metric ATS scoring (quantified impact, action verb diversity, keyword alignment), and STAR bullet point improver.
2. **Skill Gap Analysis & 4-Week Syllabus**: Role competency delta analysis against target roles (Software Engineer, ML Engineer, Full Stack, DevOps, Frontend), auto-generating a tiered syllabus (Basic, Intermediate, Advanced) with daily interactive checkpoints.
3. **Mock Interview Arena**: Adaptive technical, behavioral, and system design simulations. Supports voice/speech-to-text input, real-time pace analysis (WPM, filler word counter), STAR rubric grading, and end-of-round debrief reports.
4. **Code Arena**: In-browser code editor powered by Monaco Editor. Supports Python and JavaScript with AST security verification, instant test case execution, and complexity analysis.
5. **Question Bank**: Categorized library of interview questions with full STAR ideal exemplar answers and interviewer grading rubrics.
6. **Company-Specific Prep**: Interview playbooks and round-by-round breakdown for Google, Amazon, Meta, Microsoft, and Stripe.

---

## Getting Started (Docker-Free)

### Prerequisites
- Python 3.10+ (with virtual environment in `backend/venv`)
- Node.js 18+ & npm

### Quick One-Click Launch (Windows PowerShell)
```powershell
.\start-dev.ps1
```

### Manual Native Launch

#### 1. Backend (FastAPI + SQLite)
```powershell
cd backend
.\venv\Scripts\python -m uvicorn app.main:app --reload --port 8000
```
- API Documentation (Swagger UI): [http://127.0.0.1:8000/api/v1/docs](http://127.0.0.1:8000/api/v1/docs)
- Health Check: [http://127.0.0.1:8000/api/health](http://127.0.0.1:8000/api/health)

#### 2. Frontend (React + Vite)
```powershell
cd frontend
npm run dev
```
- App UI: [http://localhost:5173](http://localhost:5173)

---

## Running Tests

### Backend Unit & Integration Tests (12 tests)
```powershell
cd backend
.\venv\Scripts\python -m pytest tests/ -v
```

### Frontend Type Check & Build
```powershell
cd frontend
npm run build
```

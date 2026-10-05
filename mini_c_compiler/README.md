# Mini C Compiler

A full-stack, handwritten compiler pipeline demonstrating compilation phases from raw text to execution via an intermediate representation (TAC).

Built as a Compiler Design (3170701) project for C. K. Pithawala College of Engineering and Technology.

## Features
- **Frontend**: React + Vite UI showing all compilation phases.
- **Backend**: FastAPI + Python (no external parsing libraries).
- **Phases**: Lexical, Syntax, Semantic, Code Generation, Optimization (5 passes), Execution (VM).

## Requirements
- Python 3.10+
- Node.js 18+

## Quick Start

### 1. Run the Backend
```bash
cd backend
python -m venv .venv

# Activate (Windows PowerShell):
.\.venv\Scripts\Activate.ps1

# Activate (Linux/Mac):
# source .venv/bin/activate

pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

### 2. Run the Frontend (in a new terminal)
```bash
cd frontend
npm install
npm run dev
```

Open your browser to `http://localhost:5173`.

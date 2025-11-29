
# Enterprise Support Automator (ESA) - Capstone Project

**Track:** Enterprise Agents
**Project:** Enterprise Support Automator (ESA)

This repository is a starter scaffold for the ESA capstone project based on Google ADK concepts (Agents, Tools, Sessions, Memory, A2A, Resumability, Observability, and Evaluation).

## Contents
- `backend/` - FastAPI + ADK backend with agents, tools, and runner.
- `frontend/` - Minimal React + Vite frontend scaffold (Chat UI + Admin placeholder).
- `docker-compose.yml` & `backend/Dockerfile` - Local docker setup.
- `evaluation/` - ADK evaluation test sets and config files.
- `README.md` - This file.

## Quick local run (development)
1. Set your environment variables (do NOT commit keys):
   - `GOOGLE_API_KEY` - your Gemini/Google API key
   - `SESSION_DB_URL` - e.g. `sqlite:///esa_sessions.db` (optional)

2. Backend (Python 3.11+)
```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

3. Frontend (optional)
- The frontend is a minimal scaffold. Use `npm install` and `npm run dev` after editing as needed.

## Docker (local)
```bash
docker-compose up --build
```

## Evaluation
ADK evaluation sets are in `evaluation/`. Use the `adk eval` command as in ADK docs.

## Notes
- This starter intentionally uses mocked tools (catalog, orders). Replace with real services or MCP/A2A agents when available.
- Do NOT put API keys in files. Use environment variables / secret manager.

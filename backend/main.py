"""
main.py
AI Meeting Watchdog — backend entrypoint

Two endpoints, matching frontend/frontend/src/services/api.js exactly:

    POST /upload   — multipart form, field "policy" (file) -> UploadResponse
    POST /analyze  — JSON {chunk, policy_id} -> AnalyzeResponse

Run locally (from the repo root, so `ai_engine` and `backend` are both
importable as top-level packages):

    pip install -r requirements.txt --break-system-packages
    uvicorn backend.main:app --reload --port 8000

Then set, in frontend/frontend/.env:
    VITE_API_URL=http://localhost:8000

Deploy on Railway:
    - Root directory: repo root (so both backend/ and ai_engine/ are visible)
    - Start command:  uvicorn backend.main:app --host 0.0.0.0 --port $PORT
    - Set GROQ_API_KEY in the Railway service's Variables tab
    - Set VITE_API_URL on the frontend's Railway/Vercel service to this
      backend's public Railway URL
"""

import os

from dotenv import load_dotenv

load_dotenv()  # loads backend/.env locally; no-op on Railway (uses dashboard vars instead)

from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware

from ai_engine.contradiction_checker import check_contradiction
from ai_engine.policy_parser import UnsupportedFileType, extract_text
from ai_engine.rule_extractor import extract_rules
from backend.schemas import AnalyzeRequest, AnalyzeResponse, UploadResponse
from backend.session_store import get_rules, save_policy

app = FastAPI(title="AI Meeting Watchdog API")

# ── CORS ──────────────────────────────────────────────────────────────────
# Locally the frontend runs on Vite's dev server (default :5173).
# In production it'll be whatever domain you deploy the frontend to.
# Set FRONTEND_ORIGIN on Railway once you know the deployed frontend URL;
# defaults to "*" so the demo isn't blocked by a misconfigured env var.
FRONTEND_ORIGIN = os.environ.get("FRONTEND_ORIGIN", "*")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[FRONTEND_ORIGIN] if FRONTEND_ORIGIN != "*" else ["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def health_check():
    """Simple liveness check — also handy for confirming the Railway
    deployment is actually up before wiring the frontend to it."""
    return {"status": "ok", "service": "ai-meeting-watchdog-backend"}


@app.post("/upload", response_model=UploadResponse)
async def upload_policy(policy: UploadFile = File(...)):
    """
    Accepts a policy document, extracts its text, splits it into discrete
    rule clauses via the LLM, and stores it under a new policy_id.

    Matches uploadPolicy() in api.js: expects multipart/form-data with a
    "policy" field, returns {policy_id, rules}.
    """
    file_bytes = await policy.read()

    if not file_bytes:
        raise HTTPException(status_code=400, detail="Uploaded file is empty.")

    try:
        raw_text = extract_text(policy.filename or "", file_bytes)
    except UnsupportedFileType as e:
        raise HTTPException(status_code=400, detail=str(e))

    if not raw_text.strip():
        raise HTTPException(
            status_code=400,
            detail="Couldn't extract any text from that file. "
            "If it's a scanned/image-only PDF, try a text-based .pdf, .txt, or .docx instead.",
        )

    rules = extract_rules(raw_text)
    policy_id = save_policy(raw_text, rules)

    return UploadResponse(policy_id=policy_id, rules=rules)


@app.post("/analyze", response_model=AnalyzeResponse)
async def analyze_chunk(payload: AnalyzeRequest):
    """
    Checks one transcript utterance against the policy's rules.

    Matches sendChunk() in api.js: expects JSON {chunk, policy_id},
    returns {contradiction: false} or the full flagged-contradiction shape.
    """
    rules = get_rules(payload.policy_id)

    if rules is None:
        raise HTTPException(
            status_code=404,
            detail="Unknown policy_id. Upload a policy document first via /upload.",
        )

    if not payload.chunk.strip():
        return AnalyzeResponse(contradiction=False)

    result = check_contradiction(payload.chunk, rules)
    return AnalyzeResponse(**result)

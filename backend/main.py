"""
main.py — FastAPI backend for the AI Meeting Watchdog.

Endpoints:
  POST /api/session                 -> create a session, returns session_id
  POST /api/session/{id}/policy      -> upload policy text, builds the initial ledger
  GET  /api/session/{id}/ledger      -> current decision ledger (for the dashboard panel)
  WS   /ws/session/{id}              -> client connects here for the live demo
  POST /api/session/{id}/replay      -> kicks off the demo transcript playback over the WS

The websocket is intentionally simple: the client opens it, then calls /replay
to start the simulated "live" meeting. Swap /replay for a real mic->STT feed
later without touching the contradiction logic at all.
"""

import asyncio
import uuid
from pathlib import Path

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel

from contradiction_engine import extract_decisions, analyze_segment

app = FastAPI(title="AI Meeting Watchdog")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # tighten before you ship past the hackathon
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve the frontend from /frontend relative to backend
_frontend = Path(__file__).parent.parent / "frontend"
if _frontend.exists():
    app.mount("/static", StaticFiles(directory=str(_frontend)), name="static")

    @app.get("/")
    def serve_frontend():
        return FileResponse(str(_frontend / "index.html"))

# In-memory store — totally fine for a 5-day hackathon demo.
# sessions[session_id] = {"ledger": [...], "log": [...], "ws": WebSocket|None}
sessions: dict[str, dict] = {}


class PolicyPayload(BaseModel):
    text: str


@app.post("/api/session")
def create_session():
    session_id = str(uuid.uuid4())[:8]
    sessions[session_id] = {"ledger": [], "log": [], "ws": None}
    return {"session_id": session_id}


@app.post("/api/session/{session_id}/policy")
def upload_policy(session_id: str, payload: PolicyPayload):
    decisions = extract_decisions(payload.text)
    sessions[session_id]["ledger"] = decisions
    return {"ledger": decisions}


@app.get("/api/session/{session_id}/ledger")
def get_ledger(session_id: str):
    return {"ledger": sessions[session_id]["ledger"]}


@app.websocket("/ws/session/{session_id}")
async def ws_endpoint(websocket: WebSocket, session_id: str):
    await websocket.accept()
    sessions[session_id]["ws"] = websocket
    try:
        while True:
            # we don't expect inbound client messages in the demo flow,
            # this just keeps the connection alive
            await websocket.receive_text()
    except WebSocketDisconnect:
        sessions[session_id]["ws"] = None


@app.post("/api/session/{session_id}/replay")
async def replay(session_id: str):
    """
    Streams backend/sample_transcript.txt line by line over the open websocket,
    with a short delay between lines so it FEELS like a live meeting.
    Every line is run through analyze_segment(). This is the whole demo.
    """
    asyncio.create_task(_run_replay(session_id))
    return {"status": "started"}


async def _run_replay(session_id: str):
    session = sessions[session_id]
    ws: WebSocket | None = session["ws"]
    if ws is None:
        return

    transcript_path = Path(__file__).parent / "sample_transcript.txt"
    lines = [l.strip() for l in transcript_path.read_text().splitlines() if l.strip()]

    for line in lines:
        result = analyze_segment(line, session["ledger"])

        await ws.send_json({"type": "transcript", "text": line})

        if result.get("is_decision") and not result.get("contradiction"):
            new_id = f"M{len(session['ledger']) + 1}"
            session["ledger"].append({
                "id": new_id,
                "statement": result["statement"],
                "category": result.get("category", "other"),
                "source": "this_meeting",
            })
            await ws.send_json({"type": "ledger_update", "ledger": session["ledger"]})

        if result.get("contradiction"):
            alert = {
                "type": "alert",
                "new_statement": result["statement"],
                "conflicts_with_id": result["conflicts_with_id"],
                "explanation": result["explanation"],
                "confidence": result["confidence"],
            }
            session["log"].append(alert)
            await ws.send_json(alert)

        await asyncio.sleep(2.2)  # pacing for the demo — tune to taste

    await ws.send_json({"type": "done", "alert_count": len(session["log"])})

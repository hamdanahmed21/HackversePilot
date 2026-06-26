# AI Meeting Watchdog

Flags contradictions *during* a meeting — not in a summary afterward.
Upload a policy doc, feed in a transcript (live or simulated), and it
diffs every new statement against everything already on record:
the doc, AND decisions made earlier in the same meeting.

## Run it locally

### 1. Backend
```bash
cd backend
python -m venv venv && source venv/bin/activate   # or your usual setup
pip install -r requirements.txt
export ANTHROPIC_API_KEY=sk-ant-...
uvicorn main:app --reload --port 8000
```

### 2. Frontend
Just open `frontend/index.html` in a browser. No build step.
(It talks to `http://localhost:8000` — update the `API` constant at the
top of the `<script>` tag if you deploy the backend elsewhere.)

### 3. Demo
1. Click **Load sample policy** (or paste your own doc).
2. Click **Start meeting**.
3. Watch `backend/sample_transcript.txt` play out line by line.
   Three contradictions are planted at increasing difficulty, plus one
   that only contradicts something said *earlier in this same meeting*
   — that last one is the detail that shows judges this isn't just a
   doc-diff tool.

To change the demo script, edit `backend/sample_transcript.txt`.

## Architecture

```
Policy doc  ──▶  extract_decisions()  ──▶  Decision Ledger (in-memory)
                                                   │
Transcript line ──▶  analyze_segment(line, ledger) │
                            │                       │
                somewhere a new decision? ──────────┘ (append to ledger)
                            │
                   contradicts ledger? ──▶ alert over websocket ──▶ dashboard
```

- `contradiction_engine.py` — the only two LLM calls in the whole app.
  Extraction uses Sonnet (runs once, accuracy matters). Live checking
  uses Haiku (runs per line, latency matters).
- `main.py` — FastAPI + a websocket. `/replay` simulates a live meeting
  by streaming `sample_transcript.txt` with a delay. Swap that for a
  real mic → speech-to-text feed later without touching the engine.
- `frontend/index.html` — single-file dashboard, no build step on purpose.
  Left panel = live transcript. Right panel = decision ledger. A flagged
  card slides in from the top on every contradiction.

## Known shortcuts (say these out loud in the demo, don't hide them)
- In-memory storage, single session at a time — fine for a hackathon,
  swap for Redis/Postgres for multi-meeting use.
- "Live" transcript is simulated playback, not real mic input. The
  contradiction logic doesn't care where the text comes from — that's
  the point.
- No retrieval/embeddings — the whole ledger gets stuffed into the
  prompt each time. Works because ledgers are small. Add a vector
  store if you extend this to long-running, multi-meeting policy sets.

## What's next (for the deck's roadmap slide)
- Real STT integration (Zoom/Meet/Teams bot)
- Multi-meeting memory — a policy ledger that persists across a whole project
- Severity scoring + Slack/email digest for flagged contradictions
- Org-wide "decision graph" across teams

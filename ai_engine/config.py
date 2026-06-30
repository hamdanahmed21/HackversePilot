"""
config.py
AI Meeting Watchdog — shared configuration

Reads secrets/config from environment variables only.
Locally: set these in backend/.env (loaded by python-dotenv in main.py)
On Railway: set these in the service's "Variables" tab in the dashboard.

Required:
    GROQ_API_KEY   — your Groq API key (https://console.groq.com)

Optional:
    GROQ_MODEL     — defaults to llama-3.3-70b-versatile
"""

import os

GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "")
GROQ_MODEL = os.environ.get("GROQ_MODEL", "llama-3.3-70b-versatile")

if not GROQ_API_KEY:
    # We don't raise here so the app can still boot (e.g. for local frontend
    # dev without a key yet) — but every real call to the LLM will fail loudly.
    print(
        "[ai_engine.config] WARNING: GROQ_API_KEY is not set. "
        "Set it in backend/.env locally, or in Railway's Variables tab in production."
    )

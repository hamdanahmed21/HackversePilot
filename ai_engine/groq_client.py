"""
groq_client.py
AI Meeting Watchdog — thin wrapper around the Groq chat completion API

Both rule_extractor.py and contradiction_checker.py call through here.
Centralising it means there's exactly one place that knows how to talk
to Groq, one place to add retries/timeouts, and one place to swap models.
"""

from groq import Groq

from . import config

_client = None


def get_client() -> Groq:
    """Lazily construct the Groq client (avoids crashing at import time
    if GROQ_API_KEY isn't set yet, e.g. during local frontend-only dev)."""
    global _client
    if _client is None:
        _client = Groq(api_key=config.GROQ_API_KEY)
    return _client


def chat_json(system_prompt: str, user_prompt: str, max_tokens: int = 1024) -> str:
    """
    Sends a chat completion request and returns the raw text response.
    Both callers ask the model to respond with ONLY JSON, then parse it
    themselves (different shapes), so we just return the raw string here.

    Raises whatever the Groq SDK raises on network/API failure — callers
    are responsible for catching and translating to a clean HTTP error.
    """
    client = get_client()

    response = client.chat.completions.create(
        model=config.GROQ_MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0.1,  # we want consistent, literal judgments, not creativity
        max_tokens=max_tokens,
    )

    return response.choices[0].message.content

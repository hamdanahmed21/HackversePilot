"""
contradiction_engine.py
Migrated from Anthropic SDK → Groq SDK (Llama 3.3 70B).

Groq's API is OpenAI-compatible, so the call shape is nearly identical.
Both functions use the same model — Llama 3.3 70B is fast enough for
live checking and accurate enough for extraction.

Get a free API key at: https://console.groq.com
"""

import json
import os
from groq import Groq

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

MODEL = "llama-3.3-70b-versatile"


def _force_json(raw: str) -> dict | list:
    """Strip code fences if the model added them, then parse."""
    cleaned = raw.strip()
    if cleaned.startswith("```"):
        cleaned = cleaned.split("```")[1]
        if cleaned.startswith("json"):
            cleaned = cleaned[4:]
    cleaned = cleaned.strip()
    return json.loads(cleaned)


def extract_decisions(doc_text: str) -> list[dict]:
    """
    Turn a raw policy doc into atomic, comparable decision records.
    Runs ONCE when the policy doc is uploaded.
    """
    prompt = f"""You extract atomic decisions and policies from a document.

DOCUMENT:
{doc_text}

Return ONLY a JSON array, no preamble, no markdown fences. Each item:
{{"id": "P1", "statement": "<one self-contained decision, plain English>", "category": "<budget|deadline|policy|scope|vendor|other>"}}

Rules:
- One decision per item. Split compound sentences into separate decisions.
- Rephrase for clarity but preserve exact numbers, dates, and names.
- Ignore sentences that are not decisions or commitments (e.g. background context).
- Return raw JSON only. No explanation before or after."""

    resp = client.chat.completions.create(
        model=MODEL,
        max_tokens=1500,
        messages=[{"role": "user", "content": prompt}],
    )
    raw = resp.choices[0].message.content
    decisions = _force_json(raw)
    for d in decisions:
        d["source"] = "policy_doc"
    return decisions


def analyze_segment(segment_text: str, ledger: list[dict]) -> dict:
    """
    The live check. Runs on EVERY new transcript line.
    Returns a structured dict indicating whether a contradiction was found.
    """
    ledger_text = (
        "\n".join(f"[{d['id']}] ({d['source']}) {d['statement']}" for d in ledger)
        or "(empty — nothing on record yet)"
    )

    prompt = f"""You are watching a live meeting transcript for contradictions against a running decision ledger. The ledger includes decisions from an uploaded policy doc AND decisions made earlier in THIS meeting.

LEDGER:
{ledger_text}

NEW TRANSCRIPT LINE:
"{segment_text}"

Decide:
1. Does this line state or confirm a new decision/commitment (not a question, not small talk)?
2. If yes, does it CONTRADICT any ledger entry? A contradiction means the new statement cannot both be true alongside the ledger entry — e.g. a different number, a reversed choice, a dropped requirement.
   Do not flag mere elaboration or partial overlap as a contradiction.

Return ONLY this JSON object, no markdown fences, no explanation:
{{
  "is_decision": <bool>,
  "statement": <string or null>,
  "category": <"budget"|"deadline"|"policy"|"scope"|"vendor"|"other"|null>,
  "contradiction": <bool>,
  "conflicts_with_id": <string or null>,
  "explanation": <string or null, one sentence, plain English>,
  "confidence": <float 0-1>
}}"""

    resp = client.chat.completions.create(
        model=MODEL,
        max_tokens=400,
        messages=[{"role": "user", "content": prompt}],
    )
    raw = resp.choices[0].message.content
    return _force_json(raw)

"""
contradiction_checker.py
AI Meeting Watchdog — the core of the whole product.

Takes one committed utterance from the live meeting transcript plus the
list of policy rules, and asks Groq's Llama 3.3 whether the utterance
contradicts any rule. This is deliberately a single, focused LLM call —
per the project brief, the entire backend is "compare transcript text
against a document using an LLM."
"""

import json
import re

from . import groq_client

SYSTEM_PROMPT = """You are an AI meeting watchdog. You monitor a live \
meeting transcript in real time and flag the moment a new statement \
contradicts a previously established policy, decision, or constraint.

You will be given:
1. A numbered list of existing policy rules / past decisions.
2. One new sentence just spoken in the meeting.

Decide: does the new sentence contradict, override, or violate any rule \
in the list? Only flag a genuine contradiction — a new decision that \
conflicts with a budget cap, deadline, scope, policy, or prior commitment. \
Do NOT flag sentences that are merely related to a rule, that elaborate on \
it without conflicting, or that are small talk, agreement, or unrelated \
discussion. When in doubt, do not flag it — false alarms undermine trust \
in the tool more than a missed one.

Respond with ONLY a JSON object, nothing else, no markdown fences, no \
commentary, in exactly one of these two shapes:

No contradiction:
{"contradiction": false}

Contradiction found:
{
  "contradiction": true,
  "flagged_text": "<the exact portion of the new sentence that conflicts>",
  "conflicting_rule": "<the exact rule text from the list that it breaks>",
  "explanation": "<one short sentence explaining the conflict, plain English>"
}
"""


def check_contradiction(chunk: str, rules: list[str]) -> dict:
    """
    Args:
        chunk: the committed transcript utterance to check.
        rules: the list of policy rule strings for this session.

    Returns:
        Either {"contradiction": False} or the full flagged dict matching
        the shape sendChunk() in the frontend expects. Never raises —
        on any failure it safely returns {"contradiction": False} so one
        bad LLM call never crashes the live session.
    """
    if not rules:
        # No policy loaded yet — nothing to compare against.
        return {"contradiction": False}

    numbered_rules = "\n".join(f"{i + 1}. {r}" for i, r in enumerate(rules))
    user_prompt = (
        f"Existing policy rules / past decisions:\n{numbered_rules}\n\n"
        f"New sentence just spoken in the meeting:\n\"{chunk}\""
    )

    try:
        raw = groq_client.chat_json(
            system_prompt=SYSTEM_PROMPT,
            user_prompt=user_prompt,
            max_tokens=512,
        )
        result = _parse_response(raw)
        if result is not None:
            return result
    except Exception as e:
        print(f"[contradiction_checker] LLM call failed: {e}")

    # Fail safe: an analysis error should never surface as a false alarm
    return {"contradiction": False}


def _parse_response(raw: str) -> dict | None:
    cleaned = raw.strip()
    cleaned = re.sub(r"^```(json)?", "", cleaned).strip()
    cleaned = re.sub(r"```$", "", cleaned).strip()

    data = json.loads(cleaned)

    if not isinstance(data, dict) or "contradiction" not in data:
        return None

    if data["contradiction"] is False:
        return {"contradiction": False}

    if data["contradiction"] is True:
        # Defensive defaults so a slightly malformed model response
        # still produces a renderable alert instead of a frontend crash.
        return {
            "contradiction": True,
            "flagged_text": str(data.get("flagged_text", "")).strip(),
            "conflicting_rule": str(data.get("conflicting_rule", "")).strip(),
            "explanation": str(data.get("explanation", "")).strip(),
        }

    return None

"""
rule_extractor.py
AI Meeting Watchdog — turns raw policy document text into a clean list
of discrete, checkable rule clauses.

Why use the LLM for this instead of just splitting on newlines/periods?
Policy docs are messy — paragraphs, bullet points, mixed formatting.
The LLM normalises all of that into short, self-contained statements
like "Budget for the marketing campaign must not exceed $10,000."
which is exactly the unit contradiction_checker.py needs to compare against.
"""

import json
import re

from . import groq_client

SYSTEM_PROMPT = """You are a precise policy-extraction engine for a meeting \
contradiction-detection tool. You will be given the raw text of a policy \
document or a set of past decisions. Extract every distinct rule, decision, \
constraint, or commitment as a short, self-contained, plain-English sentence.

Rules:
- Each item must be understandable on its own, with no pronouns referring \
  to other items (resolve "it"/"this"/"that" into the actual subject).
- Keep numbers, dates, names, and amounts exact — never round or paraphrase \
  figures.
- Skip headers, boilerplate, and anything that isn't an actual rule or \
  decision (e.g. skip "Table of Contents", signatures, page numbers).
- If the document is short or has very few distinct rules, that's fine — \
  return only what's actually there. Do not invent rules.
- Respond with ONLY a JSON object of this exact shape, nothing else, no \
  markdown code fences, no commentary:

{"rules": ["rule one text", "rule two text", "..."]}
"""

# Most policy docs comfortably fit in one call; this caps it defensively
# so we never send something so huge the model truncates badly.
MAX_INPUT_CHARS = 12000


def extract_rules(policy_text: str) -> list[str]:
    """
    Args:
        policy_text: plain text extracted from the uploaded policy document.

    Returns:
        A list of rule strings. Falls back to a naive line-split if the
        LLM call fails or returns something unparseable, so a flaky API
        call never blocks the whole upload flow.
    """
    text = policy_text[:MAX_INPUT_CHARS]

    try:
        raw = groq_client.chat_json(
            system_prompt=SYSTEM_PROMPT,
            user_prompt=f"Policy document text:\n\n{text}",
            max_tokens=2048,
        )
        rules = _parse_rules_response(raw)
        if rules:
            return rules
    except Exception as e:
        print(f"[rule_extractor] LLM extraction failed, falling back: {e}")

    return _naive_fallback_split(text)


def _parse_rules_response(raw: str) -> list[str]:
    """Parses the model's JSON response, tolerating stray markdown fences."""
    cleaned = raw.strip()
    cleaned = re.sub(r"^```(json)?", "", cleaned).strip()
    cleaned = re.sub(r"```$", "", cleaned).strip()

    data = json.loads(cleaned)
    rules = data.get("rules", [])
    return [r.strip() for r in rules if isinstance(r, str) and r.strip()]


def _naive_fallback_split(text: str) -> list[str]:
    """Last-resort splitter: one rule per non-empty line. Not as clean as
    the LLM version, but guarantees the user still gets *something* if
    Groq is briefly down during a demo."""
    lines = [line.strip(" \t-•*") for line in text.splitlines()]
    return [line for line in lines if len(line) > 8]

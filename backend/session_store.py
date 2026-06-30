"""
session_store.py
AI Meeting Watchdog — in-memory policy session storage

The hackathon brief is intentionally low-complexity: one job, no
external data sources. A real DB is overkill for a single-session demo,
so we keep uploaded policies in process memory, keyed by a generated
policy_id. This resets on server restart, which is fine for a demo —
the user re-uploads their policy doc at the start of each session anyway
(see Session.jsx: upload happens once per page load).

If you outgrow this (e.g. want sessions to survive a server restart, or
support multiple concurrent backend instances on Railway), swap this
module's internals for Redis or a simple SQLite table — the function
signatures below are the only contract the rest of the app depends on.
"""

import uuid

_policies: dict[str, dict] = {}
# shape per entry: { "raw_text": str, "rules": list[str] }


def save_policy(raw_text: str, rules: list[str]) -> str:
    """Stores a parsed policy and returns its new policy_id."""
    policy_id = uuid.uuid4().hex
    _policies[policy_id] = {"raw_text": raw_text, "rules": rules}
    return policy_id


def get_rules(policy_id: str) -> list[str] | None:
    """Returns the rule list for a policy_id, or None if it doesn't exist
    (e.g. server restarted since upload, or a stale/invalid id)."""
    entry = _policies.get(policy_id)
    return entry["rules"] if entry else None


def exists(policy_id: str) -> bool:
    return policy_id in _policies

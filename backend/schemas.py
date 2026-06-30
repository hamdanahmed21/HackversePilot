"""
schemas.py
AI Meeting Watchdog — request/response models

These mirror frontend/frontend/src/services/api.js exactly. If you ever
change a field name here, update api.js's JSDoc comments too, or the
two halves of the app will silently drift apart.
"""

from pydantic import BaseModel


class UploadResponse(BaseModel):
    policy_id: str
    rules: list[str]


class AnalyzeRequest(BaseModel):
    chunk: str
    policy_id: str


class AnalyzeResponse(BaseModel):
    contradiction: bool
    flagged_text: str | None = None
    conflicting_rule: str | None = None
    explanation: str | None = None

"""Interrupt / resume approval gate.

Model: request() pauses and persists state -> a human approves/denies (possibly in another
process) -> resume() reads the decision. Crucially, a DENIAL returns structured feedback so
the agent loop can incorporate it and retry — rejection feeds back, it does not just abort.

Idea attribution: LangGraph interrupt/resume (MIT) + HumanLayer approval flow. The
'rejection returns feedback into the loop' discipline is grounded in this repo's
delegation-policy. Reimplemented, no code copied.
"""

from __future__ import annotations

import time
import uuid
from typing import Any

from ..core.errors import InterruptPending
from . import store

PENDING = "pending"
APPROVED = "approved"
DENIED = "denied"


def request(payload: dict[str, Any], *, run_id: str | None = None) -> dict:
    """Pause for a human decision. Persists a pending record and returns it."""
    rid = run_id or uuid.uuid4().hex[:12]
    record = {
        "run_id": rid,
        "status": PENDING,
        "payload": payload,
        "feedback": None,
        "created": time.time(),
        "decided": None,
    }
    store.save(record)
    return record


def _decide(run_id: str, status: str, feedback: str | None) -> dict:
    record = store.load(run_id)
    if record is None:
        raise InterruptPending(f"no pending interrupt for run {run_id!r}")
    record.update(status=status, feedback=feedback, decided=time.time())
    store.save(record)
    return record


def approve(run_id: str, feedback: str | None = None) -> dict:
    return _decide(run_id, APPROVED, feedback)


def deny(run_id: str, feedback: str | None = None) -> dict:
    return _decide(run_id, DENIED, feedback)


def resume(run_id: str) -> dict:
    """Return the decided record. Raises InterruptPending if still awaiting a human."""
    record = store.load(run_id)
    if record is None:
        raise InterruptPending(f"unknown run {run_id!r}")
    if record["status"] == PENDING:
        raise InterruptPending(f"run {run_id!r} still awaiting a human decision")
    return record


def is_approved(record: dict) -> bool:
    return record.get("status") == APPROVED

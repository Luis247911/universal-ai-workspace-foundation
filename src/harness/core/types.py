"""Primitive data types shared by more than one harness area.

Kept deliberately small: only types imported by >= 2 areas live here. Area-specific
types live in their own module (no premature abstraction).
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class Severity(str, Enum):
    INFO = "info"
    WARN = "warn"
    ERROR = "error"


@dataclass
class Message:
    """A single chat message. role is conventionally system|user|assistant|tool."""

    role: str
    content: str

    def to_dict(self) -> dict:
        return {"role": self.role, "content": self.content}


@dataclass
class Outcome:
    """Result of a single check — an eval assertion OR a guardrail validation.

    score is in [0, 1]; weight scales its contribution to an aggregate. A skipped
    outcome carries weight 0 so it is excluded from both numerator and denominator.
    """

    passed: bool
    score: float = 0.0
    weight: float = 1.0
    skipped: bool = False
    detail: str = ""

    @classmethod
    def skip(cls, detail: str = "") -> Outcome:
        return cls(passed=True, score=0.0, weight=0.0, skipped=True, detail=detail)

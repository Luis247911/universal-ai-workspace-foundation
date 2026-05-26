"""Validators: each inspects text and returns an Outcome; each carries an on_fail policy.

A validator may optionally provide `fix(text) -> str` (used by OnFail.FIX) and
`redact(text) -> str` (used by OnFail.FILTER). Teaching-grade examples are included; real
deployments add their own by subclassing Validator.
"""

from __future__ import annotations

import json
import re

from ..core.types import Outcome
from .policies import OnFail


class Validator:
    """Base class. Override `validate`. Optionally override `fix` / `redact`."""

    def __init__(self, on_fail: OnFail = OnFail.RAISE) -> None:
        self.on_fail = on_fail

    @property
    def name(self) -> str:
        return type(self).__name__

    def validate(self, text: str) -> Outcome:  # pragma: no cover - abstract
        raise NotImplementedError

    def fix(self, text: str) -> str:
        return text

    def redact(self, text: str) -> str:
        return text


class RegexForbidden(Validator):
    """Fails if a forbidden pattern is present. redact() removes matches."""

    def __init__(self, pattern: str, on_fail: OnFail = OnFail.FILTER, label: str = "match") -> None:
        super().__init__(on_fail)
        self._re = re.compile(pattern)
        self._label = label

    def validate(self, text: str) -> Outcome:
        hits = self._re.findall(text)
        ok = not hits
        return Outcome(
            passed=ok, score=1.0 if ok else 0.0, detail="" if ok else f"{len(hits)} {self._label}"
        )

    def redact(self, text: str) -> str:
        return self._re.sub("[redacted]", text)


class NoEmail(RegexForbidden):
    def __init__(self, on_fail: OnFail = OnFail.FILTER) -> None:
        super().__init__(r"[\w.+-]+@[\w-]+\.[\w.-]+", on_fail, label="email(s)")


class MaxLength(Validator):
    def __init__(self, limit: int, on_fail: OnFail = OnFail.FIX) -> None:
        super().__init__(on_fail)
        self.limit = limit

    def validate(self, text: str) -> Outcome:
        ok = len(text) <= self.limit
        return Outcome(passed=ok, score=1.0 if ok else 0.0, detail="" if ok else f"len={len(text)}")

    def fix(self, text: str) -> str:
        return text[: self.limit]


class IsJSON(Validator):
    def __init__(self, on_fail: OnFail = OnFail.REASK) -> None:
        super().__init__(on_fail)

    def validate(self, text: str) -> Outcome:
        try:
            json.loads(text)
            return Outcome(passed=True, score=1.0)
        except (json.JSONDecodeError, TypeError) as e:
            return Outcome(passed=False, score=0.0, detail=f"not JSON: {e}")

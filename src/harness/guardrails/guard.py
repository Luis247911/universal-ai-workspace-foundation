"""A Guard composes validators on the input or output boundary and applies their on_fail.

apply() walks the validators; on a failure it dispatches the validator's on_fail policy
and may rewrite the text (fix/filter/refrain), stop hard (raise), or signal a retry (reask).
"""

from __future__ import annotations

from dataclasses import dataclass, field

from ..core.errors import ValidationError
from ..core.types import Outcome
from .policies import REFUSAL_TEXT, OnFail
from .validator import Validator


@dataclass
class GuardResult:
    text: str
    passed: bool
    boundary: str
    action: str | None = None  # the on_fail action that fired, if any
    reask: bool = False
    outcomes: list[Outcome] = field(default_factory=list)


class Guard:
    def __init__(self, *validators: Validator, boundary: str = "output") -> None:
        if boundary not in ("input", "output"):
            raise ValueError("boundary must be 'input' or 'output'")
        self.validators = list(validators)
        self.boundary = boundary

    def apply(self, text: str) -> GuardResult:
        outcomes: list[Outcome] = []
        action: str | None = None
        reask = False
        passed = True
        for v in self.validators:
            outcome = v.validate(text)
            outcomes.append(outcome)
            if outcome.passed:
                continue
            passed = False
            action = v.on_fail.value
            if v.on_fail is OnFail.RAISE:
                raise ValidationError(f"{v.name} rejected {self.boundary}: {outcome.detail}")
            if v.on_fail is OnFail.REFRAIN:
                return GuardResult(REFUSAL_TEXT, False, self.boundary, action, outcomes=outcomes)
            if v.on_fail is OnFail.FILTER:
                text = v.redact(text)
            elif v.on_fail is OnFail.FIX:
                text = v.fix(text)
            elif v.on_fail is OnFail.REASK:
                reask = True
            # NOOP: leave text unchanged, keep walking
        return GuardResult(text, passed, self.boundary, action, reask=reask, outcomes=outcomes)

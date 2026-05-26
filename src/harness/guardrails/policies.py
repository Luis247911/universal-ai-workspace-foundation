"""The on_fail policy enum — the heart of a guardrail.

A rail turns validation from pass/fail into a recoverable control-flow decision. When a
validator rejects content, its on_fail policy decides what happens next.

Idea attribution: the on_fail action set is reimplemented from Guardrails-AI / NeMo
Guardrails (Apache-2.0). No code copied. See /sources/credits.md.
"""

from __future__ import annotations

from enum import Enum


class OnFail(str, Enum):
    FIX = "fix"  # apply the validator's fixer and continue
    REASK = "reask"  # signal the caller to retry the generation
    FILTER = "filter"  # redact the offending part, continue with the rest
    REFRAIN = "refrain"  # replace output with a safe refusal
    RAISE = "raise"  # raise ValidationError (hard stop)
    NOOP = "noop"  # record the violation but pass content through unchanged


REFUSAL_TEXT = "[refrained: output withheld by a guardrail]"

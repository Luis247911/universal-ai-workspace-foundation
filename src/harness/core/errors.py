"""Exception hierarchy shared across the harness."""

from __future__ import annotations


class HarnessError(Exception):
    """Base class for all harness errors."""


class ConfigError(HarnessError):
    """A config/suite file is missing, malformed, or needs an optional extra."""


class ValidationError(HarnessError):
    """A guardrail validator rejected content under an on_fail=raise policy."""


class InterruptPending(HarnessError):
    """A run paused awaiting a human decision (see harness.hitl)."""

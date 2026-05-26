"""Shared primitives imported by the framework areas.

Import rule (anti-sprawl for code): a framework area may import from `harness.core`,
never from a sibling area, except the few compositions the canonical patterns require
(documented at the import site).
"""

from __future__ import annotations

from . import config, jsonio, llm, paths
from .errors import ConfigError, HarnessError, InterruptPending, ValidationError
from .registry import Registry
from .state import State
from .types import Message, Outcome, Severity

__all__ = [
    "config",
    "jsonio",
    "llm",
    "paths",
    "ConfigError",
    "HarnessError",
    "InterruptPending",
    "ValidationError",
    "Registry",
    "State",
    "Message",
    "Outcome",
    "Severity",
]

"""Typed fallback chains: different error classes get different fallback lists.

The reusable idea: a rate-limit should fall back differently than a context-window overflow
or a content-policy refusal. Each error type maps to its own ordered list of model-group
aliases to try next.

Idea attribution: LiteLLM's typed fallbacks (fallbacks / context_window_fallbacks /
content_policy_fallbacks). Reimplemented, no code copied.
"""

from __future__ import annotations

from enum import Enum


class ErrorClass(str, Enum):
    RATE_LIMIT = "rate_limit"
    CONTEXT_WINDOW = "context_window"
    CONTENT_POLICY = "content_policy"
    OTHER = "other"


class FallbackPolicy:
    def __init__(self, chains: dict[str, list[str]] | None = None) -> None:
        self.chains = {ErrorClass(k): v for k, v in (chains or {}).items()}

    def next_aliases(self, error: ErrorClass) -> list[str]:
        """Ordered list of model-group aliases to try for this error class."""
        return list(self.chains.get(error, self.chains.get(ErrorClass.OTHER, [])))

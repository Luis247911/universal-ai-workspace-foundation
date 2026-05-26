"""Router area: model-group routing, typed fallbacks, cache-breakpoint planning."""

from __future__ import annotations

from .cache_hint import MAX_BREAKPOINTS, Segment, lint_breakpoints
from .fallback import ErrorClass, FallbackPolicy
from .router import Deployment, ModelRouter

__all__ = [
    "ModelRouter",
    "Deployment",
    "FallbackPolicy",
    "ErrorClass",
    "Segment",
    "lint_breakpoints",
    "MAX_BREAKPOINTS",
]

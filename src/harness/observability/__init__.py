"""Observability area: typed spans with OTel gen_ai.* attribute names."""

from __future__ import annotations

from . import semconv
from .tracer import Span, Tracer

__all__ = ["semconv", "Span", "Tracer"]

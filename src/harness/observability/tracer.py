"""A minimal tracer: a tree of typed spans with gen_ai.* attributes, exported as JSONL.

A trace is a tree of spans (llm_call / tool_call / retrieval / agent / chain). Trace-level
attributes (user_id, session_id) propagate to every span. Message content is captured ONLY
when capture_content=True (privacy: opt-in, matching the OTel guidance).

The privacy filter is enforced at the choke point Span.set_attribute, so content-bearing
attributes are dropped whether they are passed when the span opens OR added later — there is
no way to leak content by writing the dict directly if you go through set_attribute.

Idea attribution: span-tree data model from Langfuse (MIT); attribute names from the OTel
GenAI semconv. Reimplemented, no code copied. See /sources/credits.md.
"""

from __future__ import annotations

import time
import uuid
from collections.abc import Iterator
from contextlib import contextmanager
from dataclasses import dataclass, field
from typing import Any

from ..core import jsonio
from . import semconv


@dataclass
class Span:
    name: str
    kind: str
    span_id: str
    parent_id: str | None
    capture_content: bool = True
    attributes: dict[str, Any] = field(default_factory=dict)
    start: float = 0.0
    end: float | None = None

    def set_attribute(self, key: str, value: Any) -> Span:
        """Set an attribute, honoring the content-capture policy (opt-in for message content)."""
        if key in semconv.CONTENT_ATTRIBUTES and not self.capture_content:
            return self  # dropped: content capture is off
        self.attributes[key] = value
        return self

    def set_attributes(self, attributes: dict[str, Any]) -> Span:
        for k, v in attributes.items():
            self.set_attribute(k, v)
        return self

    def to_dict(self) -> dict:
        return {
            "span_id": self.span_id,
            "parent_id": self.parent_id,
            "name": self.name,
            "kind": self.kind,
            "start": round(self.start, 6),
            "end": round(self.end, 6) if self.end is not None else None,
            "attributes": self.attributes,
        }


class Tracer:
    def __init__(self, *, capture_content: bool = False, **trace_attributes: Any) -> None:
        self.capture_content = capture_content
        self.trace_attributes = trace_attributes  # propagate to every span
        self.spans: list[Span] = []
        self._stack: list[str] = []

    @contextmanager
    def span(self, name: str, kind: str, **attributes: Any) -> Iterator[Span]:
        sp = Span(
            name=name,
            kind=kind,
            span_id=uuid.uuid4().hex[:12],
            parent_id=self._stack[-1] if self._stack else None,
            capture_content=self.capture_content,
            start=time.perf_counter(),
        )
        sp.set_attributes(self.trace_attributes)
        sp.set_attributes(attributes)
        self.spans.append(sp)
        self._stack.append(sp.span_id)
        try:
            yield sp
        finally:
            sp.end = time.perf_counter()
            self._stack.pop()

    def llm_call(self, name: str, *, model: str, provider: str = "anthropic", **attrs: Any):
        attributes = {
            semconv.GEN_AI_OPERATION_NAME: "chat",
            semconv.GEN_AI_PROVIDER_NAME: provider,
            semconv.GEN_AI_REQUEST_MODEL: model,
            **attrs,
        }
        return self.span(name, semconv.KIND_LLM_CALL, **attributes)

    def export_jsonl(self, path) -> None:
        jsonio.write_jsonl(path, (s.to_dict() for s in self.spans))

"""A tiny LLM gateway with an offline mock default.

Default (UAW_LLM unset or 'mock'): deterministic responses so tests, examples, and CI
run with no network and no API key. Set UAW_LLM=live (plus the [llm] extra and
ANTHROPIC_API_KEY) to call a real model. Keeping the mock deterministic is what lets the
whole repo stay green in CI without secrets.
"""

from __future__ import annotations

import hashlib
import os

from .types import Message


def llm_mode() -> str:
    return os.environ.get("UAW_LLM", "mock").lower()


def is_mock() -> bool:
    return llm_mode() != "live"


def complete(
    messages,
    *,
    system: str | None = None,
    model: str | None = None,
    max_tokens: int = 512,
) -> str:
    """Return a completion string. Deterministic in mock mode."""
    msgs = [m if isinstance(m, Message) else Message(**m) for m in messages]
    if is_mock():
        return _mock_complete(msgs, system)
    return _live_complete(msgs, system=system, model=model, max_tokens=max_tokens)


def _mock_complete(messages: list[Message], system: str | None) -> str:
    last_user = next((m.content for m in reversed(messages) if m.role == "user"), "")
    seed = (system or "") + "::" + last_user
    digest = hashlib.sha256(seed.encode("utf-8")).hexdigest()[:8]
    return f"[mock:{digest}] {last_user[:120]}"


def _live_complete(
    messages: list[Message], *, system: str | None, model: str | None, max_tokens: int
) -> str:
    try:
        import anthropic
    except ImportError as e:  # pragma: no cover - exercised only in live mode
        raise RuntimeError(
            "UAW_LLM=live requires the [llm] extra: pip install 'uaw-harness[llm]'"
        ) from e
    client = anthropic.Anthropic()
    resp = client.messages.create(
        model=model or "claude-sonnet-4-6",
        max_tokens=max_tokens,
        system=system or "",
        messages=[m.to_dict() for m in messages],
    )
    return "".join(b.text for b in resp.content if getattr(b, "type", None) == "text")

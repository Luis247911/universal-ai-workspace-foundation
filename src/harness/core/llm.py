"""A tiny LLM gateway with an offline mock default.

Default (UAW_LLM unset or 'mock'): deterministic responses so tests, examples, and CI
run with no network and no API key. Set UAW_LLM=live (plus the [llm] extra and
ANTHROPIC_API_KEY) to call a real model. Keeping the mock deterministic is what lets the
whole repo stay green in CI without secrets.

The live model defaults to DEFAULT_MODEL and can be overridden per call (``model=``) or per
environment (``UAW_MODEL``). On models that support it, a server-side refusal fallback is
enabled so a classifier decline is retried on Anthropic's recommended fallback model.
"""

from __future__ import annotations

import hashlib
import os

from .errors import HarnessError
from .types import Message

DEFAULT_MODEL = "claude-opus-5-5"
# Models that accept the server-side refusal fallback (`fallbacks="default"`).
_FALLBACK_MODELS = frozenset(
    {"claude-fable-5-1", "claude-opus-5-5", "claude-opus-5", "claude-sonnet-5-5"}
)
_FALLBACK_BETA = "server-side-fallback-2026-07-01"


def llm_mode() -> str:
    return os.environ.get("UAW_LLM", "mock").lower()


def is_mock() -> bool:
    return llm_mode() != "live"


def default_model() -> str:
    return os.environ.get("UAW_MODEL") or DEFAULT_MODEL


def complete(
    messages,
    *,
    system: str | None = None,
    model: str | None = None,
    max_tokens: int = 16000,
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
    client = anthropic.Anthropic()  # SDK default: 2 retries on 408/409/429/5xx
    model = model or default_model()
    params: dict = {
        "model": model,
        "max_tokens": max_tokens,
        "messages": [m.to_dict() for m in messages],
    }
    if system:
        params["system"] = system
    if model in _FALLBACK_MODELS:
        resp = client.beta.messages.create(**params, betas=[_FALLBACK_BETA], fallbacks="default")
    else:
        resp = client.messages.create(**params)
    if resp.stop_reason == "refusal":
        raise HarnessError(f"model declined the request (stop_details={resp.stop_details!r})")
    return "".join(b.text for b in resp.content if getattr(b, "type", None) == "text")

"""Live-path routing of harness.core.llm, exercised offline against a stub `anthropic` module."""

from __future__ import annotations

import sys
import types
from types import SimpleNamespace

import pytest

from harness.core import llm
from harness.core.errors import HarnessError


def _stub_anthropic(monkeypatch, stop_reason: str = "end_turn") -> dict:
    calls: dict = {}

    def _response(**_):
        return SimpleNamespace(
            stop_reason=stop_reason,
            stop_details=None,
            content=[SimpleNamespace(type="text", text="PASS")],
        )

    def create(**kw):
        calls["plain"] = kw
        return _response()

    def beta_create(**kw):
        calls["beta"] = kw
        return _response()

    client = SimpleNamespace(
        messages=SimpleNamespace(create=create),
        beta=SimpleNamespace(messages=SimpleNamespace(create=beta_create)),
    )
    mod = types.ModuleType("anthropic")
    mod.Anthropic = lambda: client  # type: ignore[attr-defined]
    monkeypatch.setitem(sys.modules, "anthropic", mod)
    monkeypatch.setenv("UAW_LLM", "live")
    monkeypatch.delenv("UAW_MODEL", raising=False)
    return calls


def test_default_model_uses_refusal_fallback(monkeypatch):
    calls = _stub_anthropic(monkeypatch)
    assert llm.complete([{"role": "user", "content": "hi"}]) == "PASS"
    kw = calls["beta"]
    assert kw["model"] == llm.DEFAULT_MODEL
    assert kw["fallbacks"] == "default"
    assert kw["betas"] == ["server-side-fallback-2026-07-01"]
    assert "system" not in kw  # empty system is not sent


def test_uaw_model_override_without_fallback_support(monkeypatch):
    calls = _stub_anthropic(monkeypatch)
    monkeypatch.setenv("UAW_MODEL", "claude-haiku-4-5")
    llm.complete([{"role": "user", "content": "hi"}], system="be brief")
    kw = calls["plain"]
    assert kw["model"] == "claude-haiku-4-5"
    assert kw["system"] == "be brief"
    assert "fallbacks" not in kw and "beta" not in calls


def test_refusal_raises(monkeypatch):
    _stub_anthropic(monkeypatch, stop_reason="refusal")
    with pytest.raises(HarnessError, match="declined"):
        llm.complete([{"role": "user", "content": "hi"}])

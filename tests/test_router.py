import pytest

from harness.core.errors import ConfigError
from harness.router.cache_hint import Segment, lint_breakpoints
from harness.router.fallback import ErrorClass, FallbackPolicy
from harness.router.router import ModelRouter

CONFIG = {
    "model_groups": {
        "fast": [{"model": "haiku"}, {"model": "sonnet"}],
        "smart": [{"model": "opus"}],
    },
    "routing_strategy": "first",
    "fallbacks": {"rate_limit": ["smart"], "context_window": ["smart"]},
}


def test_pick_first():
    assert ModelRouter(CONFIG).pick("fast").model == "haiku"


def test_pick_round_robin():
    cfg = {**CONFIG, "routing_strategy": "round_robin"}
    r = ModelRouter(cfg)
    assert [r.pick("fast").model for _ in range(3)] == ["haiku", "sonnet", "haiku"]


def test_unknown_alias_raises():
    with pytest.raises(ConfigError):
        ModelRouter(CONFIG).pick("nope")


def test_typed_fallbacks():
    fb = FallbackPolicy(CONFIG["fallbacks"])
    assert fb.next_aliases(ErrorClass.RATE_LIMIT) == ["smart"]
    assert fb.next_aliases(ErrorClass.CONTENT_POLICY) == []  # no chain, no 'other' default


def test_cache_lint_clean():
    segs = [
        Segment("tools", 2000),
        Segment("system", 1500, breakpoint=True),
        Segment("messages", 500),
    ]
    assert lint_breakpoints(segs) == []


def test_cache_lint_flags_breakpoint_after_volatile():
    segs = [
        Segment("tools", 2000, volatile=True),  # e.g. a per-request timestamp injected here
        Segment("system", 1500, breakpoint=True),
    ]
    warns = lint_breakpoints(segs)
    assert any("volatile" in w for w in warns)


def test_cache_lint_flags_unordered_and_budget():
    segs = [Segment("messages", 2000, breakpoint=True)] + [
        Segment("tools", 2000, breakpoint=True)
    ] * 5
    warns = lint_breakpoints(segs)
    assert any("most-stable-first" in w for w in warns)
    assert any("budget" in w for w in warns)

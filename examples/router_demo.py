"""Offline router demo: pick a deployment, walk a typed fallback chain, lint a cache plan.

python examples/router_demo.py
"""

from __future__ import annotations

from harness.router import ErrorClass, FallbackPolicy, ModelRouter, Segment, lint_breakpoints

CONFIG = {
    "model_groups": {
        "fast": [{"model": "claude-haiku-4-5"}, {"model": "claude-sonnet-4-6"}],
        "smart": [{"model": "claude-opus-4-7"}],
    },
    "routing_strategy": "first",
    "fallbacks": {"rate_limit": ["smart"], "context_window": ["smart"]},
}


def main() -> int:
    router = ModelRouter(CONFIG)
    print(f"pick(fast) -> {router.pick('fast').model}")

    fb = FallbackPolicy(CONFIG["fallbacks"])
    print(f"on rate_limit -> {fb.next_aliases(ErrorClass.RATE_LIMIT)}")

    good = [
        Segment("tools", 2000),
        Segment("system", 1500, breakpoint=True),
        Segment("messages", 400),
    ]
    bad = [Segment("system", 1500, volatile=True), Segment("messages", 800, breakpoint=True)]
    print(f"sound cache plan warnings: {lint_breakpoints(good)}")
    print(f"bad cache plan warnings:   {lint_breakpoints(bad)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

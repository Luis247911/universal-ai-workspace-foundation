"""CLI: python -m harness.router pick --alias fast [--config PATH]
       python -m harness.router explain [--config PATH]
       python -m harness.router cache-lint [--bad]

With no --config, a small built-in demo config is used so the command runs offline.
`cache-lint` lints a built-in cache-breakpoint plan; --bad shows a plan with warnings.
"""

from __future__ import annotations

import argparse
import json
import sys

from .cache_hint import Segment, lint_breakpoints
from .fallback import ErrorClass, FallbackPolicy
from .router import ModelRouter

_DEMO_CONFIG = {
    "model_groups": {
        "fast": [{"model": "claude-haiku-4-5"}, {"model": "claude-sonnet-4-6"}],
        "smart": [{"model": "claude-opus-4-7"}],
    },
    "routing_strategy": "first",
    "fallbacks": {"rate_limit": ["smart"], "context_window": ["smart"], "content_policy": []},
}


def _load(path):
    if path:
        from ..core.config import load_config

        return load_config(path)
    return _DEMO_CONFIG


def _cache_lint(bad: bool) -> int:
    if bad:
        # a timestamp (volatile) sits in the prefix and a breakpoint is placed after it
        segments = [
            Segment("system", tokens=2000),
            Segment("system", tokens=50, volatile=True, breakpoint=True),
            Segment("tools", tokens=1500),
        ]
    else:
        segments = [
            Segment("tools", tokens=1500, breakpoint=True),
            Segment("system", tokens=1200),
            Segment("messages", tokens=300, volatile=True),
        ]
    warns = lint_breakpoints(segments)
    if not warns:
        print("cache plan OK (no breakpoint warnings)")
        return 0
    for w in warns:
        print(f"WARN: {w}")
    return 1


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="harness.router")
    sub = parser.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("pick")
    p.add_argument("--alias", required=True)
    p.add_argument("--config", default=None)
    e = sub.add_parser("explain")
    e.add_argument("--config", default=None)
    cl = sub.add_parser("cache-lint", help="Lint a cache-breakpoint plan.")
    cl.add_argument("--bad", action="store_true", help="Show a plan that has warnings.")
    args = parser.parse_args(argv)

    if args.cmd == "cache-lint":
        return _cache_lint(args.bad)

    config = _load(args.config)
    router = ModelRouter(config)

    if args.cmd == "pick":
        dep = router.pick(args.alias)
        print(
            json.dumps(
                {"deployment": dep.model, "provider": dep.provider, "strategy": router.strategy}
            )
        )
        return 0
    if args.cmd == "explain":
        fb = FallbackPolicy(config.get("fallbacks"))
        for ec in ErrorClass:
            chain = fb.next_aliases(ec)
            if chain:
                print(f"{ec.value}: {' -> '.join(chain)}")
        return 0
    return 2


if __name__ == "__main__":
    sys.exit(main())

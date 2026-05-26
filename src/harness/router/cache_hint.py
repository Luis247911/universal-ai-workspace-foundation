"""Prompt-cache breakpoint planner + linter.

Caching is the highest-leverage cost lever, and the #1 mistake is putting a cache
breakpoint AFTER volatile content (which busts the cache every request). The rule: order
the prefix most-stable first (tools -> system -> messages), place breakpoints only on the
stable prefix, and never exceed the breakpoint budget.

Idea attribution: Anthropic prompt-caching guidance (cache hierarchy tools->system->messages,
<=4 breakpoints, ~0.1x read). Concept reused, no prose/code copied.
"""

from __future__ import annotations

from dataclasses import dataclass

# stability rank: lower = more stable = should come earlier in the cached prefix
STABILITY_RANK = {"tools": 0, "system": 1, "messages": 2}
MAX_BREAKPOINTS = 4


@dataclass
class Segment:
    role: str  # "tools" | "system" | "messages"
    tokens: int
    volatile: bool = False  # changes every request (e.g. a timestamp)?
    breakpoint: bool = False  # is a cache breakpoint requested after this segment?


def lint_breakpoints(segments: list[Segment], *, min_prefix_tokens: int = 1024) -> list[str]:
    """Return a list of warnings. Empty list == the cache plan is sound."""
    warns: list[str] = []
    n_breaks = sum(1 for s in segments if s.breakpoint)
    if n_breaks > MAX_BREAKPOINTS:
        warns.append(f"{n_breaks} breakpoints exceed the budget of {MAX_BREAKPOINTS}")

    ranks = [STABILITY_RANK.get(s.role, 99) for s in segments]
    if ranks != sorted(ranks):
        warns.append("segments are not ordered most-stable-first (tools -> system -> messages)")

    seen_volatile = False
    prefix_tokens = 0
    for s in segments:
        if s.volatile:
            seen_volatile = True
        if s.breakpoint:
            if seen_volatile:
                warns.append(
                    f"breakpoint after volatile content ({s.role}) busts the cache every request"
                )
            if prefix_tokens + s.tokens < min_prefix_tokens:
                warns.append(
                    f"breakpoint at {s.role} caches only ~{prefix_tokens + s.tokens} tokens "
                    f"(< {min_prefix_tokens} min cacheable)"
                )
        prefix_tokens += s.tokens
    return warns

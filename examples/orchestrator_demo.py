"""Offline orchestrator demo: each canonical workflow shape + a supervisor handoff loop.

python examples/orchestrator_demo.py
"""

from __future__ import annotations

from harness.core.state import State
from harness.orchestrator import patterns
from harness.orchestrator.handoff import build_supervisor


def main() -> int:
    print("sequential:", patterns.sequential("caching", [lambda t: f"outline({t})", str.upper]))

    print(
        "router:   ",
        patterns.route(
            "my invoice is wrong",
            classify=lambda t: "billing" if "invoice" in t else "tech",
            routes={"billing": lambda t: "-> billing team", "tech": lambda t: "-> tech team"},
        ),
    )

    print(
        "evaluator-optimizer:",
        patterns.evaluator_optimizer(
            "draft a title",
            generate=lambda _t, fb: "great title" if fb else "ok title",
            evaluate=lambda d: {"ok": "great" in d, "feedback": "make it punchier"},
        ),
    )

    def decide(s: State):
        if not s.get("research"):
            return "research"
        if not s.get("write"):
            return "write"
        return None

    graph = build_supervisor(
        {"research": lambda s: s.set("research", True), "write": lambda s: s.set("write", True)},
        decide,
    )
    final = graph.run(State())
    print(
        f"supervisor: research={final.get('research')} write={final.get('write')} (loop terminated)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

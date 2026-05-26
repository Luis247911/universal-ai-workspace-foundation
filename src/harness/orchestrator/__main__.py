"""CLI: python -m harness.orchestrator run --pattern PATTERN

PATTERN in: sequential | router | parallel | vote | orchestrator-workers | evaluator-optimizer
            | supervisor

Workers here are tiny deterministic functions so the demo runs offline; swap in LLM-backed
workers (harness.core.llm.complete) for real use.
"""

from __future__ import annotations

import argparse
import sys

from ..core.state import State
from . import patterns
from .handoff import build_supervisor


def _demo(pattern: str) -> str:
    if pattern == "sequential":
        return patterns.sequential(
            "topic: caching",
            [lambda t: f"outline({t})", lambda t: f"draft<{t}>", str.upper],
        )
    if pattern == "router":
        classify = lambda t: "billing" if "invoice" in t else "tech"  # noqa: E731
        routes = {
            "billing": lambda t: f"billing handled: {t}",
            "tech": lambda t: f"tech handled: {t}",
        }
        return patterns.route("my invoice is wrong", classify, routes)
    if pattern == "parallel":
        return patterns.parallel_sections(
            "ship the feature",
            [lambda t: f"risks({t})", lambda t: f"tests({t})", lambda t: f"docs({t})"],
            lambda parts: " | ".join(parts),
        )
    if pattern == "vote":
        return patterns.vote("2+2", lambda t: "4", n=3, pick=lambda rs: max(set(rs), key=rs.count))
    if pattern == "orchestrator-workers":
        return patterns.orchestrator_workers(
            "a,b,c",
            plan=lambda t: t.split(","),
            worker=lambda task: f"done:{task}",
            synthesize=lambda rs: "; ".join(rs),
        )
    if pattern == "evaluator-optimizer":

        def generate(_text, feedback):
            return "v2" if feedback else "v1"

        def evaluate(draft):
            return {"ok": draft == "v2", "feedback": "make it better"}

        draft, rounds = patterns.evaluator_optimizer("task", generate, evaluate, max_rounds=3)
        return f"{draft} (after {rounds} rounds)"
    if pattern == "supervisor":

        def worker_a(s: State) -> State:
            return s.set("a_done", True)

        def worker_b(s: State) -> State:
            return s.set("b_done", True)

        def decide(s: State) -> str | None:
            if not s.get("a_done"):
                return "a"
            if not s.get("b_done"):
                return "b"
            return None  # done -> END

        graph = build_supervisor({"a": worker_a, "b": worker_b}, decide)
        final = graph.run(State())
        return f"a_done={final.get('a_done')} b_done={final.get('b_done')}"
    raise SystemExit(f"unknown pattern {pattern!r}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="harness.orchestrator")
    sub = parser.add_subparsers(dest="cmd", required=True)
    r = sub.add_parser("run")
    r.add_argument("--pattern", required=True)
    args = parser.parse_args(argv)
    if args.cmd == "run":
        print(_demo(args.pattern))
        return 0
    return 2


if __name__ == "__main__":
    sys.exit(main())

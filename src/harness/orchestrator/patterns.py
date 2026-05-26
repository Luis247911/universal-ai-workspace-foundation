"""The canonical workflow shapes from Anthropic's 'Building Effective Agents'.

Each is a small, composable function over worker callables so it is testable offline with
pure functions (and works the same with LLM-backed workers). Start with the simplest shape
that fits — do not reach for an agent when a workflow suffices.

    sequential          prompt chaining: fixed steps, each feeds the next
    route               routing: classify input, dispatch to a specialist
    parallel_sections   parallelization (sectioning): independent subtasks, then combine
    vote                parallelization (voting): same task N times, then aggregate
    orchestrator_workers a planner splits work, workers execute, a synthesizer combines
    evaluator_optimizer  generate -> evaluate -> refine loop until good or budget spent

Idea attribution: the five pattern names are from Anthropic's 'Building Effective Agents'
(proprietary — names/concepts reused, no prose/code copied). 'ReAct' (see graph.py loop) is
from the ReAct paper / LangChain, NOT Anthropic. See /sources/credits.md.
"""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

Worker = Callable[[str], str]


def sequential(text: str, steps: list[Worker]) -> str:
    for step in steps:
        text = step(text)
    return text


def route(text: str, classify: Callable[[str], str], routes: dict[str, Worker]) -> str:
    key = classify(text)
    if key not in routes:
        raise KeyError(f"router produced unknown route {key!r}; known: {sorted(routes)}")
    return routes[key](text)


def parallel_sections(
    text: str, branches: list[Worker], aggregate: Callable[[list[str]], str]
) -> str:
    return aggregate([b(text) for b in branches])


def vote(text: str, worker: Worker, n: int, pick: Callable[[list[str]], str]) -> str:
    return pick([worker(text) for _ in range(n)])


def orchestrator_workers(
    text: str,
    plan: Callable[[str], list[str]],
    worker: Worker,
    synthesize: Callable[[list[str]], str],
) -> str:
    tasks = plan(text)
    return synthesize([worker(t) for t in tasks])


def evaluator_optimizer(
    text: str,
    generate: Callable[[str, dict | None], str],
    evaluate: Callable[[str], dict[str, Any]],
    *,
    max_rounds: int = 3,
) -> tuple[str, int]:
    """Returns (final_draft, rounds_used). evaluate() returns {'ok': bool, 'feedback': str}."""
    feedback: dict | None = None
    draft = generate(text, None)
    for rnd in range(1, max_rounds + 1):
        verdict = evaluate(draft)
        if verdict.get("ok"):
            return draft, rnd
        feedback = verdict
        draft = generate(text, feedback)
    return draft, max_rounds

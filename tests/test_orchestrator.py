import pytest

from harness.core.errors import HarnessError
from harness.core.state import State
from harness.orchestrator import patterns
from harness.orchestrator.graph import Graph
from harness.orchestrator.handoff import build_supervisor


def test_sequential():
    out = patterns.sequential("x", [lambda t: t + "1", lambda t: t + "2"])
    assert out == "x12"


def test_route_dispatches():
    out = patterns.route(
        "invoice problem",
        classify=lambda t: "billing" if "invoice" in t else "tech",
        routes={"billing": lambda t: "B", "tech": lambda t: "T"},
    )
    assert out == "B"


def test_vote_majority():
    out = patterns.vote("q", lambda t: "4", n=3, pick=lambda rs: max(set(rs), key=rs.count))
    assert out == "4"


def test_evaluator_optimizer_converges():
    draft, rounds = patterns.evaluator_optimizer(
        "task",
        generate=lambda _t, fb: "good" if fb else "bad",
        evaluate=lambda d: {"ok": d == "good", "feedback": "improve"},
        max_rounds=3,
    )
    # first draft is "bad"; after one round of feedback it becomes "good" -> converges round 2
    assert draft == "good" and rounds == 2


def test_graph_static_edges_terminate():
    g = Graph()
    g.add_node("a", lambda s: s.set("a", 1)).add_node("b", lambda s: s.set("b", 2))
    g.add_edge("a", "b").set_entry("a")
    final = g.run(State())
    assert final.get("a") == 1 and final.get("b") == 2


def test_supervisor_handoff_loop_terminates():
    def wa(s: State) -> State:
        return s.set("a_done", True)

    def wb(s: State) -> State:
        return s.set("b_done", True)

    def decide(s: State):
        if not s.get("a_done"):
            return "a"
        if not s.get("b_done"):
            return "b"
        return None

    g = build_supervisor({"a": wa, "b": wb}, decide)
    final = g.run(State())
    assert final.get("a_done") and final.get("b_done")


def test_graph_max_steps_guards_runaway():
    g = Graph()
    g.add_node("loop", lambda s: s).add_conditional_edges("loop", lambda s: "loop")
    g.set_entry("loop")
    with pytest.raises(HarnessError):
        g.run(State(), max_steps=10)

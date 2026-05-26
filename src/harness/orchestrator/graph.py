"""A tiny state graph: nodes + typed edges over a shared State object.

Every orchestration shape is a graph of nodes (State -> State) and edges:
    static edge        always go to the named node next      (Sequential)
    conditional edge   a function picks the next node        (Router / loop / handoff)
    no outgoing edge   terminal                              (END)

Spans are emitted via the observability area so a run is traceable. This is the one
sanctioned cross-area import (orchestrator -> observability), documented here.

Idea attribution: node/edge-over-shared-state model reimplemented from LangGraph (MIT).
No code copied. See /sources/credits.md.
"""

from __future__ import annotations

from collections.abc import Callable

from ..core.errors import HarnessError
from ..core.state import State
from ..observability import semconv
from ..observability.tracer import Tracer

NodeFn = Callable[[State], State]
RouterFn = Callable[[State], str | None]


class Graph:
    def __init__(self, *, tracer: Tracer | None = None) -> None:
        self.nodes: dict[str, NodeFn] = {}
        self.edges: dict[str, str] = {}
        self.conditional: dict[str, RouterFn] = {}
        self.entry: str | None = None
        self.tracer = tracer

    def add_node(self, name: str, fn: NodeFn) -> Graph:
        self.nodes[name] = fn
        return self

    def add_edge(self, src: str, dst: str) -> Graph:
        self.edges[src] = dst
        return self

    def add_conditional_edges(self, src: str, router: RouterFn) -> Graph:
        self.conditional[src] = router
        return self

    def set_entry(self, name: str) -> Graph:
        self.entry = name
        return self

    def _next(self, current: str, state: State) -> str | None:
        if current in self.conditional:
            return self.conditional[current](state)
        return self.edges.get(current)

    def run(self, state: State, start: str | None = None, *, max_steps: int = 100) -> State:
        current = start or self.entry
        if current is None:
            raise HarnessError("graph has no entry node")
        tracer = self.tracer or Tracer()
        steps = 0
        while current is not None:
            if steps >= max_steps:
                raise HarnessError(
                    f"graph exceeded max_steps={max_steps} (possible missing done-check)"
                )
            if current not in self.nodes:
                raise HarnessError(f"unknown node {current!r}")
            with tracer.span(current, semconv.KIND_AGENT):
                state = self.nodes[current](state)
            current = self._next(current, state)
            steps += 1
        return state

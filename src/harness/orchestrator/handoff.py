"""The one axis that distinguishes multi-agent topologies:

    handoff       transfer OWNERSHIP — the next agent takes over the conversation
                  (supervisor / swarm). Implemented as setting a routing variable in
                  shared state that a conditional edge reads.
    agent-as-tool CALL & RETURN — the manager invokes a sub-agent, gets a result, and
                  keeps control (hierarchical / network where one node coordinates).

Idea attribution: handoff-vs-agent-as-tool framing from OpenAI Agents SDK / LangGraph /
AutoGen / CrewAI (all MIT). Reimplemented, no code copied. See /sources/credits.md.
"""

from __future__ import annotations

from collections.abc import Callable

from ..core.state import State
from .graph import Graph

Agent = Callable[[State], State]


def agent_as_tool(agent: Agent, name: str) -> Callable[[State], State]:
    """Wrap an agent as a tool the manager calls and returns from (control stays with manager)."""

    def tool(state: State) -> State:
        result = agent(state)
        state.set(f"{name}_result", result.get("result"))
        return state

    tool.__name__ = f"tool_{name}"
    return tool


def build_supervisor(
    workers: dict[str, Agent],
    decide: Callable[[State], str | None],
    *,
    supervisor_name: str = "supervisor",
) -> Graph:
    """Supervisor topology via handoff: the supervisor sets state.route to the next worker
    (or None to finish); each worker hands control back to the supervisor."""
    g = Graph()

    def supervisor(state: State) -> State:
        return state.goto(decide(state))

    g.add_node(supervisor_name, supervisor)
    g.add_conditional_edges(supervisor_name, lambda s: s.route)
    for name, fn in workers.items():
        g.add_node(name, fn)
        g.add_edge(name, supervisor_name)  # worker hands ownership back to the supervisor
    g.set_entry(supervisor_name)
    return g

"""Orchestrator area: node/edge graph + the canonical workflow shapes + handoff topologies."""

from __future__ import annotations

from . import patterns
from .graph import Graph, NodeFn, RouterFn
from .handoff import agent_as_tool, build_supervisor

__all__ = ["Graph", "NodeFn", "RouterFn", "patterns", "agent_as_tool", "build_supervisor"]

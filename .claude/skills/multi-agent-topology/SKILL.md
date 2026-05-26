---
name: multi-agent-topology
description: Use this when you are tempted to build a multi-agent system — to first decide whether you need more than one agent at all, and if so which topology (supervisor, hierarchical, network, swarm) fits, with the failure modes of each. Triggers on "multi-agent", "multiple agents", "swarm", "supervisor agent", "agents talking to each other", "how many agents".
version: 1.0.0
compat: skill-format-1.0
status: experimental
---

# multi-agent-topology

Helps you choose *how agents are wired together* — or, more often, talk you out of needing several. The strong default is **one agent with tools**. Reach for a topology only when a single agent's context or control flow genuinely cannot carry the task.

## When to use

- You are about to spin up "a team of agents" and want to sanity-check that you need more than one.
- A single agent's context is overflowing or its tool set has become incoherent.
- You need to pick between supervisor / hierarchical / network / swarm and want the trade-offs.

## First question: do you need multi-agent at all?

Prefer a single agent when the task fits one coherent context and tool set. Split into
multiple agents only for: clear separation of concerns, parallelism across independent
subtasks, or context-window pressure that prompt design cannot fix. More agents means more
coordination cost, more failure surface, and harder debugging.

## The four topologies (detail in `reference.md`)

| Topology | Shape | Use when | Main risk |
|----------|-------|----------|-----------|
| **Supervisor** | one router delegates to workers, workers return | clear subtasks, central control | supervisor is a bottleneck |
| **Hierarchical** | supervisors of supervisors | many workers, layered domains | latency, error propagation |
| **Network** | any agent may call any agent | dynamic, peer collaboration | loops, runaway cost |
| **Swarm** | agents hand off control by role | one active agent at a time, role transfer | lost context on handoff |

## Runnable example

The supervisor topology is implemented and runnable:

```
python -m harness.orchestrator run --pattern supervisor
```

## Boundaries

- This skill **owns** the topology *choice* and the "do you even need this" gate.
- For the single-agent *workflow* patterns (chaining, routing, parallel) and their runnable
  code, use [[orchestrator-patterns]] — that skill owns the engine.
- To triage from a one-line problem to the right pattern or topology, start at [[agent-pattern-selector]].

## Attribution

Topology names and the simplicity-first stance reimplemented from LangGraph, AutoGen, CrewAI and OpenAI-agents (OSS) and Anthropic's "Building Effective Agents" (concept names only). No prose copied. See `/sources/credits.md`.

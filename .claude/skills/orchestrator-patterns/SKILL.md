---
name: orchestrator-patterns
description: Use this when you need to structure an agent workflow — to pick among the proven shapes (prompt chaining, routing, parallel sectioning, voting, orchestrator-workers, evaluator-optimizer) plus the ReAct loop, and run each as working code. Triggers on "workflow", "chain steps", "orchestrate", "parallelize", "evaluator", "agent loop", "ReAct".
version: 1.0.0
compat: skill-format-1.0
status: experimental
---

# orchestrator-patterns

Owns the runnable **workflow shapes** for a single agent system. These five composable patterns (plus the ReAct loop) cover the large majority of real agent workflows; reach for a multi-agent topology only when none of them fit.

## When to use

- Deciding how to structure steps: one prompt, a chain, a branch, a fan-out, or a refine loop.
- You want a working reference implementation, not just a diagram.
- Composing patterns (e.g. route → then chain inside one branch).

## Run it (every pattern is runnable offline)

```
python -m harness.orchestrator run --pattern sequential
python -m harness.orchestrator run --pattern router
python -m harness.orchestrator run --pattern parallel
python -m harness.orchestrator run --pattern vote
python -m harness.orchestrator run --pattern orchestrator-workers
python -m harness.orchestrator run --pattern evaluator-optimizer
```

## The patterns (detail in `reference.md`)

1. **Prompt chaining (`sequential`)** — decompose into fixed ordered steps; each step's output feeds the next.
2. **Routing (`router`)** — classify the input, dispatch to a specialized handler.
3. **Parallel — sectioning (`parallel`)** — split independent subtasks, run concurrently, join.
4. **Parallel — voting (`vote`)** — run the same task N times, aggregate (majority/best).
5. **Orchestrator-workers (`orchestrator-workers`)** — a planner decomposes dynamically, workers execute, a synthesizer combines.
6. **Evaluator-optimizer (`evaluator-optimizer`)** — generate, evaluate against criteria, refine until it passes or the round budget runs out.
7. **ReAct loop** — reason → act (tool) → observe → repeat; the base loop of a tool-using agent (see `reference.md`).

## Method

1. Start with the simplest shape that fits; **prefer a single LLM call** before any orchestration.
2. Use a fixed workflow (chaining/routing) when the steps are known; use the agentic loop (ReAct, evaluator-optimizer) when they are not.
3. Add structure only to remove a concrete failure, never speculatively.

## Boundaries

- This skill **owns** the single-agent workflow shapes and their runnable code (the `orchestrator` engine).
- For wiring *multiple* agents together (supervisor/network/swarm), use [[multi-agent-topology]].
- For the generate→evaluate→refine loop's *scoring*, the criteria come from [[eval-judge]] or [[eval-loop-builder]].

## Evals

See `evaluate.md` — 3 scenarios with a no-skill baseline.

## Attribution

The five workflow shape *names* are from Anthropic's "Building Effective Agents" (concept names only, no prose). The ReAct loop is from the ReAct paper (not Anthropic). Reimplemented; no code copied. See `/sources/credits.md`.

---
name: agent-pattern-selector
description: Use this when you have an agent problem but are not sure which approach or skill applies — to triage from a one-line symptom to the right harness skill, and to be reminded that the simplest thing that works usually wins. Triggers on "where do I start", "which pattern", "what should I use", "how do I build this agent", "is this the right approach".
version: 1.0.0
compat: skill-format-1.0
status: experimental
---

# agent-pattern-selector

The front door. A read-only triage that maps a one-line problem to the harness skill that owns
it — and, just as often, reminds you that you do not need the fancy thing yet. It writes
nothing and runs nothing; it points.

## When to use

- You know the symptom ("too slow", "it forgets", "needs sign-off") but not the tool.
- You are about to build something elaborate and want a sanity check first.
- Onboarding to the harness and looking for the right entry point.

## The prime directive

> Find the simplest thing that works, and only add complexity when it demonstrably earns its keep.

Most "agent" problems are solved by a better prompt, one good tool, or a single workflow shape —
not by more agents. Reach for orchestration and multi-agent topologies last, not first.

## Triage table

| Your problem | Start here |
|--------------|-----------|
| "Is the new prompt/model actually better?" / I need a regression gate | [[eval-loop-builder]] |
| "Grade this one open-ended answer against a rubric" | [[eval-judge]] |
| "Block PII / enforce a format / refuse unsafe output at runtime" | [[guardrail-designer]] |
| "What did the agent do? where's the time/cost going?" | [[observability-tracer]] |
| "A human must approve before this runs" | [[hitl-gate]] |
| "Too slow / too expensive / caching won't hit" | [[cost-latency-optimizer]] |
| "How should I structure these steps?" (chain/route/parallel/refine) | [[orchestrator-patterns]] |
| "Do I need multiple agents, and wired how?" | [[multi-agent-topology]] |
| "What should the agent remember, and where?" | [[memory-architect]] |
| "I'm writing/editing a skill" | [[skill-author]] |
| "Is this third-party skill safe to run?" | [[skill-supply-chain-check]] |

## How to use the result

1. Match the symptom to a row; open that skill.
2. If two rows fit, you probably have two steps — do the cheaper one first and measure.
3. If nothing fits, the answer is likely "a single LLM call with one tool" — start there.

## Boundaries

- This skill **owns** triage only. It never implements; it routes to the skill that does.
- Every target skill declares its own boundaries, so follow the link rather than guessing.

## Attribution

Simplicity-first triage stance reimplemented from Anthropic's "Building Effective Agents"
(concept only, no prose copied). See `/sources/credits.md`.

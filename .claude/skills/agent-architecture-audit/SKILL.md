---
name: agent-architecture-audit
description: Use this when a multi-agent pipeline misbehaves but every single step looks correct — to audit the architecture across layers (system prompt, memory, tools, sub-agents, rendering, persistence) for failures that hide between the layers. Read-only and advisory. Triggers on "agent audit", "pipeline audit", "why does the agent behave weirdly", "memory contamination", "layer audit", "architecture review".
version: 1.0.0
compat: skill-format-1.0
status: experimental
---

# agent-architecture-audit

A read-only diagnostic for agent *systems*. It looks for failures that arise *between* layers — not
in a single output (that is an eval) and not in one tool call, but in how prompt, memory, tools,
sub-agents, rendering, and persistence are wired together. It reports findings per layer with a fix
plan; you decide and apply.

## When to use

- A pipeline behaves oddly, yet each individual step looks correct in isolation.
- After restructuring a multi-agent system (new sub-agent role, new phase, new memory source).
- After a bulk memory import or cleanup (contamination risk).
- Before releasing an agent kit for others to run (architecture sanity check).

## The twelve layers

System-prompt, session-history, long-term-memory, distillation, active-recall, tool-selection,
tool-execution, tool-interpretation, answer-shaping, platform-rendering, hidden-repair-loops,
persistence.

Any layer can corrupt the final output without its neighbour noticing.

## The five failure patterns

1. **Wrapper regression** — the base model could do it, but pipeline layers make it worse (too many
   constraints, contradictory phase prompts).
2. **Memory contamination** — old or foreign context leaks into a new task (global memory bleeding
   into a project-scoped job, orphaned observation dirs).
3. **Tool-discipline gap** — a sub-agent declares tools in frontmatter but the workflow does not
   enforce them, or grants broader access than the step needs.
4. **Rendering corruption** — the platform mutates a correct internal answer (broken markdown tables,
   encoding damage, truncated HTML).
5. **Hidden repair loops** — silent retry / auto-revise passes nobody sees or logs.

## Workflow

1. **Scope** — name the pipeline and the symptom. Which skills / agents / phases are involved?
2. **Evidence** — read the involved system prompts, sub-agent definitions, and phase files; grep for
   contradictory constraints between phases, sub-agent spawns without an aggregation rule, tool lists
   broader than the phase purpose, un-logged retry paths.
3. **Map** — per finding: symptom, mechanism, affected layer (of 12), failure pattern, evidence
   (`file:line`), confidence.
4. **Fix** — prioritise **code-first over prompt-first** (an enforced tool restriction beats a polite
   request in a prompt). Per fix: why it matters, effort, reversibility.

## Output shape

```
AGENT ARCHITECTURE AUDIT — <pipeline> — <date>
Scope: <pipeline> (<n> phases + sub-agents)   Symptom: <if reported>

[YELLOW] Layer 3 (long-term-memory) — memory-contamination
  <what, why it can leak, evidence file:line> · confidence: medium
[GREEN]  Layer 6-8 (tool-discipline) — sub-agent tools scoped

FIX PLAN (code-first, prioritised)
1. ...  2. ...
```

## Boundaries

- This skill **owns** the *system-level* architecture audit (layer interaction, contamination, tool
  discipline). It is read-only and never auto-fixes.
- For grading one *output* against a rubric, use [[eval-judge]]; for a regression gate over outputs,
  use [[eval-loop-builder]].
- For *runtime* enforcement (block / validate at the boundary), use [[guardrail-designer]].
- For *where the time, cost, and tokens go*, use [[observability-tracer]]; for *which topology*, use
  [[multi-agent-topology]].

## Attribution

Structural idea (a layered, read-only agent-architecture audit with named failure patterns)
reimplemented from a public skill pattern; no code or prose copied. See `/sources/credits.md`.

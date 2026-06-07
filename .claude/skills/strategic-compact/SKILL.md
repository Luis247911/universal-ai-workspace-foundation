---
name: strategic-compact
description: Use this on a long or multi-phase session to compact context at logical task boundaries instead of letting auto-compaction fire mid-task — decide when a manual compaction helps and what survives it. Triggers on "should I compact", "context is full", "long session", "phase boundary", "before I switch tasks", "compact now".
version: 1.0.0
compat: skill-format-1.0
status: experimental
---

# strategic-compact

Suggests a manual compaction at *strategic* points in a workflow rather than relying on arbitrary
auto-compaction, which tends to fire mid-task and drop context you still need. You decide whether to
compact; this skill tells you *when* it helps and *what* you will keep.

## When to use

- Long sessions approaching the context limit.
- Multi-phase tasks (research → plan → implement → test).
- Switching between unrelated tasks in one session.
- After a milestone, or after a failed approach whose dead-end reasoning is now noise.

## Why at boundaries, not arbitrarily

Auto-compaction has no sense of task structure: it can fire mid-implementation and lose variable
names, paths, and partial state. A boundary is the cheap moment — the prior phase's bulk is spent and
its distilled output already lives in a file or task list.

## When to compact

| Transition | Compact? | Why |
|---|---|---|
| Research → Planning | yes | research is bulky; the plan is the distilled keeper |
| Planning → Implementation | yes | plan is in a file or task list; free the window for code |
| Implementation → Testing | maybe | keep if tests lean on recent code; compact if focus shifts |
| Debugging → next feature | yes | debug traces pollute unrelated work |
| Mid-implementation | **no** | losing names, paths, and partial state is expensive |
| After a failed approach | yes | clear the dead-end before a new attempt |

## What survives a compaction

| Persists | Lost |
|---|---|
| Project instructions (CLAUDE.md / AGENTS.md) | intermediate reasoning |
| Task list | file contents you read earlier |
| Files on disk; git state | multi-step conversation context |
| Durable state notes you wrote | verbally-stated nuance not written down |

**Therefore: write before you compact.** Persist the keepers (a state note, the task list, a file)
first, then compact with a one-line focus for the next phase.

## Boundaries

- This skill **owns** *when to compact a session* and what to preserve across it (session hygiene).
- For *what an agent should remember and where it lives* (type and scope, in-context versus archival),
  use [[memory-architect]] — memory design, not session compaction.
- For trimming *start-of-session* load and budgets, use [[harness-optimizer]].
- An opt-in hook can nudge a compaction suggestion at a tool-call threshold — see the automation
  layer; default off.

## Attribution

Structural idea (strategic manual compaction at task boundaries; a survives-compaction model)
reimplemented from a public skill pattern; no code or prose copied. See `/sources/credits.md`.

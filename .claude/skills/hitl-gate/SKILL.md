---
name: hitl-gate
description: Use this when an agent must pause for human approval before a risky or irreversible action — to persist an interrupt, wait across process restarts, then resume on approve or loop back with feedback on deny. Triggers on "human in the loop", "approval", "confirm before", "pause for review", "gate the action".
version: 1.0.0
compat: skill-format-1.0
status: experimental
---

# hitl-gate

Implements a **durable human-in-the-loop interrupt**. The agent requests approval, the pause is written to disk, and the run can be resumed by a *different process* — approve to proceed, deny to re-enter the loop with feedback. The point: the pause survives a crash or restart, so an unattended agent never executes a risky action on its own.

## When to use

- Before irreversible or high-blast-radius actions (sending mail, deleting data, spending money, pushing code).
- When a human reviewer is asynchronous — the agent may exit and the decision arrives later.
- Encoding an approval policy where deny should *teach* the next attempt (feedback loop), not just stop.

## Run it (three separate processes — that's the point)

```
python -m harness.hitl request --payload "send the invoice email"   # prints a run_id, status=pending
python -m harness.hitl approve --run <run_id> --feedback "looks good"
python -m harness.hitl resume  --run <run_id>                        # -> proceed
# deny path:
python -m harness.hitl deny    --run <run_id> --feedback "wrong recipient"
python -m harness.hitl resume  --run <run_id>                        # -> loop-with-feedback
```

`resume` on a still-pending run exits non-zero (status 3) — so a supervisor can tell "not yet decided" apart from "approved".

## Statuses

- `pending` → awaiting a decision (persisted at the run's `interrupt.json`).
- `approved` → `resume` returns *proceed*.
- `denied` → `resume` returns *loop-with-feedback* carrying the reviewer's note.

## Method

1. At the risky step, call `request` with a human-readable payload describing exactly what will happen.
2. Stop the agent. The interrupt is now durable.
3. A human (or a separate workflow) calls `approve`/`deny`.
4. On the next tick, `resume`: proceed, or feed the denial reason back into the next generation.

## Boundaries

- This skill **owns** the durable pause/resume and the approve/deny state machine.
- For *automatic* content checks that need no human, use [[guardrail-designer]].
- For routing which agent/worker runs next (no human), use [[orchestrator-patterns]].

## Evals

See `evaluate.md` — 3 scenarios with a no-skill baseline.

## Attribution

Interrupt/resume shape reimplemented from LangGraph's `interrupt` and HumanLayer's approval pattern (OSS); no code copied. See `/sources/credits.md`.

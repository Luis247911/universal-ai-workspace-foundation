---
name: harness-optimizer
description: Use this when your Claude-Code-style harness feels heavy or slow and you want the highest-leverage config changes, not a rewrite — a read-only audit of hooks (count, redundancy, latency), session context budgets, model routing, and MCP load that returns the few reversible tweaks worth making. Never writes config. Triggers on "optimize my harness", "tune my setup", "sessions feel sluggish", "too many hooks", "context too full at start".
version: 1.0.0
compat: skill-format-1.0
status: experimental
---

# harness-optimizer

Raises completion quality by changing *configuration*, not content. It reads the real harness, scores
a few leverage domains, and names the changes with the best expected effect-to-effort ratio. Every
recommendation is minimal and reversible — it writes nothing; you decide and apply.

## When to use

- Periodically, or after a bigger harness change (a new hook, a new MCP server, a new prompt-submit chain).
- Sessions feel sluggish (many hooks firing on every prompt).
- The context feels too full at session start (budget tuning).

**Precondition:** fix outstanding *health* problems first (broken paths, invalid config) — a broken
harness is not optimized, it is repaired.

## Five leverage domains

1. **Hooks — latency & redundancy.** How many hooks fire per event? A `UserPromptSubmit` or
   `SessionStart` hook is a fixed cost on every prompt or start. The same script wired to several
   matchers — intended, or consolidatable? Are blocking hooks bounded by timeouts?
2. **Context — budgets.** Sum the auto-loaded sources at session start (bootstrap context, routers,
   reminders). Does the start-load crowd out the actual task? Are per-file and total caps set?
3. **Routing — model & effort.** Is a high effort or verbosity level on permanently when most tasks
   don't need it? Are sub-agent jobs tiered by model (classification → cheap, routine → mid,
   architecture → top)?
4. **Eval — quality gates.** Are self-eval gates present where output leaves the system? Do expensive
   LLM evaluators run *conditionally* (claims, numbers) rather than always?
5. **Coverage — guards.** Do guard hooks cover the relevant tool matchers (gaps)? Any redundant guard
   calls that cost latency without adding protection?

## What to read

The harness config (`settings.json`), the hook directory (`.claude/hooks/`), and the active MCP
config. Read-only.

## Output shape

```
HARNESS OPTIMIZER — scorecard <date>
[GREEN]  Hooks     <n> events, 0 critical redundancies
[YELLOW] Context   start-load high (bootstrap + router)
[YELLOW] Routing   high effort always-on, no model tiering

TOP CHANGES (by effect / effort)
1. [Context] <minimal, reversible change> — expected: ~X ms/prompt; risk: low; rollback: <how>
2. ...  3. ...
```
Then the full per-domain finding list with `file:line`.

## Boundaries

- This skill **owns** *harness configuration* tuning (hooks, start-budgets, routing knobs, MCP load).
- For the *runtime* cost and latency of the agents the harness builds (prompt-cache breakpoints,
  batching, streaming, model fallback), use [[cost-latency-optimizer]] — a different object: the
  harness around the agent versus the agent's own request path.
- For *where* the time and tokens actually go, use [[observability-tracer]].
- For *security posture* of the config (permissions, supply chain) this skill defers — it judges
  latency and redundancy, not risk; scan a skill's scripts with [[skill-supply-chain-check]].
- Never auto-applies; proposes reversible deltas only.

## Attribution

Structural idea (a read-only, five-domain harness optimization audit returning reversible deltas)
reimplemented from a public skill pattern; no code or prose copied. See `/sources/credits.md`.

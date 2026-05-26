---
name: cost-latency-optimizer
description: Use this when an agent is too slow or too expensive — to apply the four levers (prompt caching, batching, streaming, model routing) in the right order and lint a cache-breakpoint plan for the mistakes that silently bust the cache. Triggers on "too expensive", "latency", "speed up", "cut cost", "prompt caching", "which model", "routing".
version: 1.0.0
compat: skill-format-1.0
status: experimental
---

# cost-latency-optimizer

Cuts cost and latency with four levers, applied highest-leverage first. The bundled tool lints a **prompt-cache breakpoint plan** — because the #1 caching mistake (a breakpoint after volatile content) silently busts the cache on every request and costs more than no cache at all.

## When to use

- An agent's bill or p95 latency is too high.
- You added prompt caching but it isn't hitting.
- Choosing which model handles which request (cheap-first with fallback).

## The four levers (detail in `reference.md`)

1. **Prompt caching** — highest leverage. Order the prefix most-stable-first, cache the stable part.
2. **Routing** — send easy requests to a cheap model, hard ones to a strong model; fall back on error.
3. **Batching** — for non-interactive bulk work, trade latency for throughput/discount.
4. **Streaming** — does not cut cost, but cuts *perceived* latency; use for interactive UX.

## Run it

```
python -m harness.router cache-lint           # a sound plan -> "cache plan OK"
python -m harness.router cache-lint --bad      # a plan with mistakes -> warnings, non-zero exit
python -m harness.router pick --alias fast      # which deployment a route resolves to
python -m harness.router explain                # the fallback chains per error class
```

## The cache rule (what the linter enforces)

- Order segments most-stable-first: **tools → system → messages**.
- Never place a breakpoint *after* volatile content (a timestamp, the latest user turn).
- Stay within the breakpoint budget (≤ 4) and above the minimum cacheable prefix (~1024 tokens).

## Boundaries

- This skill **owns** the four cost/latency levers and cache-plan linting.
- For *which model* in a multi-step graph and error-driven fallback wiring, it shares the `router` engine with runtime routing; for topology choice use [[multi-agent-topology]].
- For the token numbers that tell you where the cost is, use [[observability-tracer]].

## Evals

See `evaluate.md` — 3 scenarios with a no-skill baseline.

## Attribution

Cache hierarchy (tools→system→messages, ≤4 breakpoints, ~0.1× read) is Anthropic prompt-caching guidance — concept reused, no prose copied. Routing/fallback shape reimplemented from LiteLLM (OSS). See `/sources/credits.md`.

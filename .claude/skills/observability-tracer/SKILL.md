---
name: observability-tracer
description: Use this when you need to see what an agent did — to emit a tree of typed spans (llm_call, tool_call, retrieval, agent, chain) with gen_ai.* attributes and export them as JSONL, with message content captured only when you opt in. Triggers on "tracing", "observability", "spans", "what did the agent do", "token usage", "debug the agent run".
version: 1.0.0
compat: skill-format-1.0
status: experimental
---

# observability-tracer

Emits a **tree of typed spans** for an agent run. Each span carries OpenTelemetry GenAI attribute names (`gen_ai.*`); trace-level attributes (user/session id) propagate to every child. Message content is captured **only when you opt in** — the privacy default is off.

## When to use

- Debugging "what did the agent actually do, in what order, and how long did each step take?"
- Recording token usage and model per call for cost analysis.
- Producing portable JSONL traces you can diff in CI or load into a viewer.

## Run it

```
python -m harness.observability trace                       # content dropped (default)
python -m harness.observability trace --capture-content     # opt in to message content
python .claude/skills/observability-tracer/scripts/run.py trace --out trace.jsonl
```

## The privacy choke point

Content attributes (`gen_ai.input.messages`, `gen_ai.output.messages`) are dropped at a single choke point — `Span.set_attribute` — so they cannot leak whether passed at span-open or added later. Turning capture on is a deliberate `capture_content=True`. This is the one invariant the skill defends: **traces are safe to ship by default.**

## Span kinds and attributes

- **kinds**: `agent`, `chain`, `llm_call`, `tool_call`, `retrieval`.
- **non-content attrs** (always kept): `gen_ai.request.model`, `gen_ai.operation.name`, `gen_ai.usage.input_tokens`, `gen_ai.usage.output_tokens`.
- **content attrs** (opt-in only): `gen_ai.input.messages`, `gen_ai.output.messages`.

## Method

1. Open an `agent` span at the top; nest `llm_call`/`tool_call`/`retrieval` under it.
2. Set token usage on each `llm_call` for cost rollups.
3. Leave content capture off in shared/CI environments; enable locally when debugging.
4. Export to JSONL and attach to the run.

## Boundaries

- This skill **owns** span emission and the content-capture policy.
- For *cost* decisions derived from the token numbers traces expose, use [[cost-latency-optimizer]].
- For grading the run's quality, use [[eval-loop-builder]].

## Evals

See `evaluate.md` — 3 scenarios with a no-skill baseline.

## Attribution

Span-tree data model reimplemented from Langfuse (MIT); attribute *names* from the OpenTelemetry GenAI semantic conventions (names are not code). No code copied. See `/sources/credits.md`.

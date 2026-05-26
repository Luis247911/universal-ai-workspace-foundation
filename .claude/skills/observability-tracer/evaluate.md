# evaluate — observability-tracer

Judged on whether the emitted trace is correct *and* private-by-default.

## Rubric

| Dimension | Pass condition |
|-----------|----------------|
| Tree shape | Child spans carry the parent's `span_id` as `parent_id`; root has `parent_id=None`. |
| GenAI keys | `llm_call` spans use `gen_ai.request.model` / `gen_ai.operation.name`. |
| Privacy default | With capture off, no content attribute appears, even when set post-hoc. |
| Opt-in works | With `--capture-content`, content attributes are present. |

## Scenario 1 — content is dropped by default

- **No-skill baseline**: raw prompts/responses logged to disk, a privacy leak.
- **Expected**: `trace` (no flag) → exported JSONL contains zero `gen_ai.input.messages` values.

## Scenario 2 — opt-in captures content

- **No-skill baseline**: all-or-nothing logging.
- **Expected**: `trace --capture-content` → content attributes present in the JSONL.

## Scenario 3 — nesting and timing are preserved

- **No-skill baseline**: a flat list of log lines, no parent/child or durations.
- **Expected**: the JSONL has a root `agent` span and nested `llm_call`/`retrieval` spans each with `start`/`end`.

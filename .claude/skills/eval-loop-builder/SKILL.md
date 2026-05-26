---
name: eval-loop-builder
description: Use this when you need to build or extend an evaluation for an agent or prompt — to turn a vague "it seems better" into a dataset, weighted assertions, and a threshold gate that fails CI. Triggers on "eval", "test the prompt", "regression", "is the new prompt better", "scorecard".
version: 1.0.0
compat: skill-format-1.0
status: experimental
---

# eval-loop-builder

Builds the load-bearing feedback loop of the harness: **dataset + typed assertions + runner + threshold gate**. Without an eval you are guessing; with one, every prompt or model change is measured and a regression blocks the merge.

## When to use

- Starting any agent feature — write the eval *first* (evals-first), then make it pass.
- "Is the new prompt/model actually better?" → encode the answer as a scored suite.
- Wiring a CI gate that must fail when quality drops below a threshold.
- Adding cases for a bug you just fixed so it never regresses silently.

## Run it

```
# scaffold a runnable starter suite, then run it
python -m harness.eval scaffold --out my.suite.json
python -m harness.eval run --suite my.suite.json

# from a fresh clone (no install): use the bundled shim
python .claude/skills/eval-loop-builder/scripts/run.py run --suite my.suite.json --threshold 0.9
```

`run` exits non-zero when the weighted score is below the threshold — that exit code is what makes it a CI gate.

## Suite format (JSON; YAML works with the `[yaml]` extra)

```json
{
  "suite": "name", "threshold": 0.8,
  "cases": [
    { "id": "case-1",
      "input": { "kind": "inline", "output": "the text under test" },
      "assertions": [ { "type": "contains", "value": "hello", "weight": 2.0 } ] }
  ]
}
```

- **input kinds**: `inline` (output given directly), `file` (read a file relative to the suite's `base`), `cmd` (stdout of a subprocess; args as a list, never a shell string).
- **assertion types**: `exact`, `contains`, `regex`, `json_schema`, `llm_rubric`. The first four are deterministic and need no model. `llm_rubric` is skipped offline by default so suites stay green without an API key, and grades for real under `UAW_LLM=live`.
- **weights**: each assertion contributes `score × weight`; skipped outcomes carry weight 0.

## Method

1. Collect 5–20 representative cases (include the failure you are fixing).
2. Prefer deterministic assertions; reserve `llm_rubric` for genuinely subjective quality.
3. Pick a threshold you can defend, then ratchet it up over time.
4. Run in CI on every change. A red suite blocks the merge.

## Boundaries

- This skill **owns** the dataset, the suite format, the runner, and the gate.
- For grading a single open-ended output with a rubric, use [[eval-judge]] (it wraps the same `llm_rubric`).
- For validating live request/response content (PII, format) at runtime rather than in a test, use [[guardrail-designer]].

## Evals

See `evaluate.md` — 3 scenarios with a no-skill baseline.

## Attribution

Typed-assertion-list-with-weights shape reimplemented from promptfoo / DeepEval / Phoenix (OSS); no code copied. See `/sources/credits.md`.

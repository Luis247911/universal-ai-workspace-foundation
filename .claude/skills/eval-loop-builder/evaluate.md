# evaluate — eval-loop-builder

Evals-first: this skill is judged by whether the loop it produces actually *gates*. Each
scenario states the no-skill baseline (what a model does unaided) and the bar to clear.

## Rubric

| Dimension | Pass condition |
|-----------|----------------|
| Runs offline | The produced suite runs with `UAW_LLM=mock` (default), no API key, exit defined. |
| Gates | Score below threshold yields a non-zero exit; at/above yields 0. |
| Deterministic | Same suite + same inputs → same score every run. |
| Right assertion | Deterministic checks used where possible; `llm_rubric` only for subjective quality. |

## Scenario 1 — scaffold then run is green

- **No-skill baseline**: model hand-writes JSON, often invalid or non-runnable.
- **Expected**: `python -m harness.eval scaffold --out s.json && python -m harness.eval run --suite s.json` → exit 0, prints `PASS`.

## Scenario 2 — the gate actually fails

- **No-skill baseline**: "looks worse" — no enforced consequence.
- **Expected**: a suite scoring 1.0 run with `--threshold 1.01` → non-zero exit. This proves the gate is load-bearing, not decorative.

## Scenario 3 — offline rubric stays green, grades live

- **No-skill baseline**: an `llm_rubric` case needs a key, so CI breaks without secrets.
- **Expected**: with `UAW_LLM=mock` an `llm_rubric` assertion is skipped (weight 0, suite green); under `UAW_LLM=live` it grades for real and can lower the score.

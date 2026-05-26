# evaluate — eval-judge

Judged on whether it returns a calibrated, deterministic verdict offline and a real one live.

## Rubric

| Dimension | Pass condition |
|-----------|----------------|
| Deterministic offline | Same output + rubric → same verdict every run (no key needed). |
| Discriminates | A matching output PASSes; an unrelated output FAILs. |
| Exit code | FAIL exits non-zero so it can gate a loop or a check. |
| Honest mode flag | The result reports `mock` true/false so callers know how it was graded. |

## Scenario 1 — relevant output passes

- **No-skill baseline**: "looks fine to me" — unrecorded, unrepeatable.
- **Expected**: `judge --rubric "mentions caching and latency" --output "use caching to cut latency"` → PASS, exit 0.

## Scenario 2 — irrelevant output fails

- **No-skill baseline**: lenient self-grading passes almost anything.
- **Expected**: `judge --rubric "mentions kubernetes pipelines" --output "hello world"` → FAIL, exit non-zero.

## Scenario 3 — same judge, two call sites

- **No-skill baseline**: each feature reimplements its own grader, drifting apart.
- **Expected**: the verdict from this CLI matches the `llm_rubric` outcome used inside [[eval-loop-builder]] suites (one judge, shared).

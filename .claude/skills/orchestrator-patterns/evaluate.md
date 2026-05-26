# evaluate — orchestrator-patterns

Judged on whether each shape runs as code and produces the structurally correct result.

## Rubric

| Dimension | Pass condition |
|-----------|----------------|
| Runs | Each `--pattern` runs offline and exits 0. |
| Correct shape | Output reflects the pattern (chained order, routed branch, joined parts, converged refine). |
| Bounded | Loop patterns terminate within their round/step budget. |
| Simplest-first | Recommendation favors a single call / workflow before an agentic loop. |

## Scenario 1 — routing dispatches to the right branch

- **No-skill baseline**: one mega-prompt tries to handle every input kind.
- **Expected**: `run --pattern router` on a billing input → the billing branch handles it.

## Scenario 2 — evaluator-optimizer converges via feedback

- **No-skill baseline**: a single generation with no refinement.
- **Expected**: `run --pattern evaluator-optimizer` → a first draft is critiqued, then refined to a passing result within the round budget.

## Scenario 3 — parallel sectioning joins independent parts

- **No-skill baseline**: sequential handling of independent subtasks (slower, entangled).
- **Expected**: `run --pattern parallel` → independent sections produced and joined into one result.

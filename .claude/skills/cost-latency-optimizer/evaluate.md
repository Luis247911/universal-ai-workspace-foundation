# evaluate — cost-latency-optimizer

Judged on whether it catches the cache mistakes that cost real money and routes correctly.

## Rubric

| Dimension | Pass condition |
|-----------|----------------|
| Catches bad plans | A breakpoint-after-volatile plan produces a warning and non-zero exit. |
| Passes good plans | A most-stable-first plan with a valid breakpoint exits 0. |
| Routing resolves | An alias resolves to a concrete deployment deterministically. |
| Lever order | Caching is recommended before streaming (leverage order, per `reference.md`). |

## Scenario 1 — the linter catches a cache-busting plan

- **No-skill baseline**: caching "enabled" but a breakpoint sits after a timestamp → 0% hit rate, silent waste.
- **Expected**: `cache-lint --bad` → warns "breakpoint after volatile content", exit non-zero.

## Scenario 2 — a sound plan passes

- **No-skill baseline**: unsure whether caching is configured correctly.
- **Expected**: `cache-lint` → "cache plan OK", exit 0.

## Scenario 3 — routing picks the cheap deployment

- **No-skill baseline**: every request hits the strongest (most expensive) model.
- **Expected**: `pick --alias fast` → resolves to the cheap deployment; `explain` shows the fallback chain.

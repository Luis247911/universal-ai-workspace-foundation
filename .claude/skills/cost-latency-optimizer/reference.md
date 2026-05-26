# reference — the four cost/latency levers

Apply in order of leverage. Measure with [[observability-tracer]] before and after — never optimize blind.

## 1. Prompt caching (highest leverage)

The model can reuse a previously-processed prefix at roughly a tenth of the input cost. The
entire payoff depends on the prefix being *byte-identical* across requests.

- **Order most-stable-first**: tools (rarely change) → system prompt → conversation messages.
- **Place breakpoints only on the stable prefix.** A breakpoint after anything volatile (a
  timestamp, the newest user turn) means the cached span changes every request → 0% hit rate,
  and you pay the cache-write premium for nothing.
- **Budget**: keep to a small number of breakpoints (≤ 4) and above the minimum cacheable
  prefix (~1024 tokens) or the cache will not engage.
- Lint a plan: `python -m harness.router cache-lint` (and `--bad` to see the failure modes).

## 2. Model routing

Most requests are easy; a few are hard. Routing sends each to the cheapest model that can
handle it, with an error-driven fallback to a stronger one.

- Define model groups by capability (`fast`, `smart`) behind stable aliases.
- Fall back on `rate_limit` and `context_window` errors to a larger deployment; do **not**
  silently retry on `content_policy`.
- Inspect: `python -m harness.router pick --alias fast` and `python -m harness.router explain`.

## 3. Batching

For non-interactive, high-volume work (offline evals, bulk classification), submit work as a
batch. You trade immediacy for higher throughput and a lower per-unit price. Use it when no
human is waiting on any single response.

## 4. Streaming

Streaming tokens does **not** reduce cost or total latency — it reduces *perceived* latency by
showing progress. Use it for interactive surfaces; skip it for backend/batch paths where only
the final result matters.

## Decision order

1. Can the prefix be cached? Fix the cache plan first — it is usually the biggest win.
2. Are cheap requests hitting an expensive model? Add routing.
3. Is the work non-interactive and bulky? Batch it.
4. Is a human watching a slow response? Stream it.

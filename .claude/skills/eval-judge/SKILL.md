---
name: eval-judge
description: Use this when you need to grade a single open-ended output against a rubric (LLM-as-judge) — to get a PASS/FAIL with a score, deterministically offline and with a real model when live. Triggers on "LLM as judge", "grade this", "rubric", "score the answer", "is this output good", "judge".
version: 1.0.0
compat: skill-format-1.0
status: experimental
---

# eval-judge

The shared **LLM-as-judge**. Given one output and a rubric, it returns PASS/FAIL with a score.
Offline it grades deterministically by rubric-keyword overlap (so CI is green without a key);
under `UAW_LLM=live` it asks a real model with a reason-then-decide prompt. It is the single
judge that [[eval-loop-builder]] and [[orchestrator-patterns]] both rely on — not a second copy.

## When to use

- Grading a subjective quality that no `exact`/`regex` check can express (tone, completeness, helpfulness).
- The scoring step inside an evaluator-optimizer loop.
- A one-off "is this answer good enough?" check.

## Run it

```
python -m harness.eval judge --rubric "mentions both cost and latency" --output "use caching to cut latency and cost"
python -m harness.eval judge --rubric "is a polite refusal" --output-file reply.txt
python .claude/skills/eval-judge/scripts/run.py judge --rubric "..." --output "..."
```

Prints JSON `{verdict, score, detail, mock}` and exits non-zero on FAIL.

## How it judges

- **Offline (mock)**: PASS if salient rubric keywords appear in the output. Deterministic — same
  inputs, same verdict. Good enough to wire the plumbing and keep CI green.
- **Live (`UAW_LLM=live` + `[llm]` extra + key)**: a strict evaluator prompt — reason internally,
  then answer exactly PASS or FAIL. The reasoning is discarded; only the verdict is scored.

## Judge design rules

1. Make the rubric **specific and checkable** ("mentions X and Y"), not vague ("is good").
2. Prefer **categorical** verdicts (PASS/FAIL) over fuzzy 1–10 scores you cannot calibrate.
3. Keep the judge prompt independent of the generator's prompt to avoid shared blind spots.
4. Spot-check the judge against human labels before trusting it at scale.

## Boundaries

- This skill **owns** single-output rubric grading (the `llm_rubric` assertion, surfaced as a CLI).
- For a *dataset* of cases with weighted assertions and a CI gate, use [[eval-loop-builder]] (it
  calls the same judge for its `llm_rubric` cases).
- For runtime blocking of bad content (not grading), use [[guardrail-designer]].

## Evals

See `evaluate.md` — 3 scenarios with a no-skill baseline.

## Attribution

LLM-as-judge with rubric + reason-then-discard + categorical verdict reimplemented from common
eval practice (promptfoo / DeepEval); no code/prose copied. See `/sources/credits.md`.

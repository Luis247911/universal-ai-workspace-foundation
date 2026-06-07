---
name: iterative-retrieval
description: Use this when a subagent or retrieval step does not know up front which files or context it needs — to refine context in short dispatch, evaluate, refine cycles instead of dumping everything or guessing. Triggers on "subagent context", "what context do I send", "context too large", "missing context", "progressive retrieval", "RAG over code".
version: 1.0.0
compat: skill-format-1.0
status: experimental
---

# iterative-retrieval

Solves the subagent context problem: an agent spawned to do a job rarely knows in advance which
files, symbols, or terms it needs. Sending everything blows the window; sending nothing starves it;
guessing is usually wrong. Instead, retrieve in short cycles that get sharper each pass.

## When to use

- Spawning a subagent that needs codebase context it cannot predict.
- Building a retrieval step where the first query rarely returns the right set.
- Hitting "context too large" or "missing context" failures in delegated tasks.

## The loop (max 3 cycles, then proceed with best-so-far)

1. **DISPATCH** — broad first query from the task intent: a few path globs, keywords, obvious excludes.
2. **EVALUATE** — score each hit for relevance (high / medium / low / none) and, crucially, name what
   is still *missing* — the gap drives the next pass.
3. **REFINE** — fold the evaluation back in: add the terms the codebase actually uses, add globs from
   high-relevance hits, exclude confirmed-irrelevant paths, target the named gaps.
4. **LOOP** — repeat with the refined query. Stop when you have enough high-relevance context (rule of
   thumb: ~3 strongly relevant sources and no critical gap), or after 3 cycles — whichever first.

## Why cap at three

The first cycle usually exists to *learn the vocabulary* (the project says "throttle", not "rate
limit"); the second converges; a third is the exception, not the rule. Cycles past that buy little
and cost tokens — proceed with the best context you have and let the work surface any real gap.

## Worked sketch

```
Task: "fix the token-expiry bug"
  cycle 1  dispatch: "token","auth","expiry" in src/**  -> auth.* (high), tokens.* (high), user.* (low)
           refine:   add "refresh","jwt"; drop user.*
  cycle 2  dispatch: refined  -> session-manager.* (high), jwt-utils.* (high); no critical gap -> stop
result: auth.*, tokens.*, session-manager.*, jwt-utils.*
```

## Anti-patterns

- **One mega-query.** Over-specifying the first pass assumes you already know the vocabulary you are
  there to discover.
- **No gap tracking.** Without naming what is missing, refinement has nothing to aim at.
- **Looping forever.** Three good sources beat ten mediocre ones; stop at "good enough".

## Boundaries

- This skill **owns** the progressive-retrieval loop — how to *find* the right context iteratively.
- For *what an agent should remember and where it lives*, use [[memory-architect]].
- For *how steps are wired* (chain / route / parallel / evaluator-optimizer), use [[orchestrator-patterns]];
  for *how many agents and how connected*, use [[multi-agent-topology]].
- For *searching for an existing library or tool before building*, use [[search-first]].

## Attribution

Structural idea (iterative dispatch-evaluate-refine retrieval for subagents) reimplemented from a
public skill pattern; no code or prose copied. See `/sources/credits.md`.

---
name: verification-loop
description: Use this right after a code change — run the tests and the real output, and iterate on failure instead of coding on. Triggers on "verify and iterate", "run the tests", "smoke check", "did my change work", "verification loop", "check it actually works".
version: 1.0.0
compat: skill-format-1.0
status: experimental
---

# verification-loop

Change, verify, iterate. After every change you run the tests *and* look at the real output; on
failure you stop and diagnose rather than piling on more code. The discipline is "look at what it
actually does", not "the exit code was zero".

## When to use

- Right after editing source or tests.
- After a dependency update or a config change.

## The loop

```
change → run tests
           |- green → smoke-test with real input
           |            |- output as expected → done
           |            \- unexpected output → diagnose, iterate
           \- red → STOP coding, diagnose, fix, re-run
```

## Per-iteration checks

1. **Unit tests** for the changed layer.
2. **Type-check** where the stack has one.
3. **Smoke-test with real input** — one example, look at the actual output, not just the exit code.
4. **Neighbour check** — if the change sits under a layer others use, run their tests too.

## Stop conditions

- Tests red **and** diagnosis unclear after ~3 iterations → step back, get help or review the plan.
- Smoke output diverges from spec while unit tests are green → **the tests are incomplete**; add the
  missing test rather than ignoring the output.
- More than ~5 iterations without progress → strategic stop, re-plan.

## Anti-patterns

- "Tests aren't everything" → coding on without running them.
- Silencing type errors with an ignore or cast instead of understanding them.
- Skipping the smoke-test because units are green — tests check what they know; the smoke-test checks
  what you didn't anticipate.
- Changing several layers in one run, so a red result has no single cause.

## Boundaries

- This skill **owns** the *operational* change-verify-iterate discipline for a single change.
- For *writing the test before the implementation*, use [[tdd-workflow]].
- For a *reusable regression gate* over agent outputs (suite + pass-threshold), use
  [[eval-loop-builder]]; for grading one open-ended answer, use [[eval-judge]].

## Attribution

A general software-verification discipline (change → test → smoke → iterate); community practice,
nothing copied. See `/sources/credits.md`.

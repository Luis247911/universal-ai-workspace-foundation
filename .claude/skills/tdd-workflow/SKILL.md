---
name: tdd-workflow
description: Use this for a code change you want test-first — write the failing test, confirm it is red, then the minimal implementation, then refactor green. Triggers on "tdd", "test first", "test-first", "write the test first", "red green refactor".
version: 1.0.0
compat: skill-format-1.0
status: experimental
---

# tdd-workflow

Test-first discipline: red, green, refactor. The test goes in before the implementation, you confirm
it fails for the right reason, then you write the simplest code that turns it green.

## When to use

- A new function, class, or module.
- A bugfix for a reproduced failure (the test reproduces it first).
- An API change to an existing function.

## Red, green, refactor

1. **RED.** Write the test before the implementation. Name it for the observable behaviour
   (`loads_yaml_and_rejects_unknown_field`, not `testParseYaml`). Run it and **confirm it is red** —
   a test that passes with no implementation is testing nothing.
2. **GREEN.** Write the simplest thing that passes. No early refactoring, no speculative abstractions.
   Re-run: the new test green, the others **still** green.
3. **REFACTOR.** Only now: clean naming, pull duplicates, extract local helpers. Re-run after each
   step; if red, step back.

## Stop conditions

- Test green with no implementation → it does not test what it should; sharpen it.
- Implementation "kind of works" with no test → stop, backfill the test.
- A skip or ignore workaround with no stated reason → stop.
- A pre-commit hook fails → diagnose; do not bypass it.

## Anti-patterns

- **Test after implementation** — it then only checks what the code happens to do, not what it should.
- **Several behaviours in one test** — a break gives no clear cause.
- **Mocking pure deterministic logic** — no mocks needed there.
- **Real domain data in fixtures** — use generic structures, not sensitive or real values.

## Boundaries

- This skill **owns** *test-first* authoring (write the test before the code).
- For verifying a change *after* it is made (run tests + smoke + iterate), use [[verification-loop]].
- For evals of *agent outputs* (rubric or threshold), use [[eval-loop-builder]] and [[eval-judge]] —
  those grade model behaviour; this drives unit code.
- For the evals-first discipline when *authoring a skill*, use [[skill-author]].

## Attribution

Test-driven development (red-green-refactor) is established practice (Kent Beck and others); concept
only, nothing copied. See `/sources/credits.md`.

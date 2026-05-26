---
name: guardrail-designer
description: Use this when you need to validate or sanitize what crosses the agent boundary at runtime — to block PII, enforce a format, cap length, or refuse unsafe output, with an explicit on-fail action. Triggers on "guardrail", "validation", "PII", "block", "sanitize", "filter output", "content policy".
version: 1.0.0
compat: skill-format-1.0
status: experimental
---

# guardrail-designer

Composes input/output **guards**: ordered validators run at a boundary, each with an explicit `on_fail` action. A guardrail is not an eval — it runs on live traffic and decides what happens *right now* when a check fails.

## When to use

- Stripping or blocking PII (emails, secrets) before it is logged or returned.
- Enforcing a response shape (valid JSON, max length) before downstream parsing.
- Refusing or rewriting unsafe content instead of passing it through.
- Validating untrusted *input* before it reaches the model.

## Run it

```
python -m harness.guardrails check --text "reach me at jane@example.com" --boundary output
python .claude/skills/guardrail-designer/scripts/run.py check --text "x" --boundary input
```

## The on_fail contract

Every validator declares what to do when it fails — this is the heart of guardrail design:

| `on_fail` | Effect |
|-----------|--------|
| `fix`     | Deterministically repair (e.g. truncate to max length). |
| `filter`  | Remove the offending span (e.g. redact emails). |
| `reask`   | Signal the caller to regenerate (sets `reask=True`). |
| `refrain` | Replace the whole output with a safe refusal. |
| `raise`   | Hard-stop with an error. |
| `noop`    | Record the failure but pass the text through. |

## Method

1. Decide the boundary: **input** (defend the model) or **output** (defend the user/logs).
2. Order validators cheapest-first; a `refrain` short-circuits the rest.
3. Choose `on_fail` per validator by blast radius: `fix`/`filter` for cosmetic issues, `refrain`/`raise` for safety.
4. Pair with an eval (see below) so you measure how often each guard trips.

## Boundaries

- This skill **owns** runtime boundary validation and the `on_fail` dispatch.
- For measuring quality in a test/CI rather than live traffic, use [[eval-loop-builder]].
- For deciding whether a *human* must approve an action, use [[hitl-gate]].

## Evals

See `evaluate.md` — 3 scenarios with a no-skill baseline.

## Attribution

`on_fail` action vocabulary and the validator-composition shape reimplemented from Guardrails-AI and NeMo-Guardrails (OSS); no code copied. See `/sources/credits.md`.

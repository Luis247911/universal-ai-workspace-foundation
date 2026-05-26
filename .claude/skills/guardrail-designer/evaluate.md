# evaluate — guardrail-designer

A guardrail is judged on whether it takes the *declared action* at the boundary, not on prose.

## Rubric

| Dimension | Pass condition |
|-----------|----------------|
| Action taken | The configured `on_fail` actually fires (text fixed/filtered/refused). |
| Boundary correct | Input guards run before the model; output guards before return/log. |
| No over-block | Clean text passes unchanged (`passed=True`, action `noop`). |
| Deterministic | Same input → same action and same text. |

## Scenario 1 — PII is filtered from output

- **No-skill baseline**: the email is returned and lands in logs.
- **Expected**: `check --text "mail me at a@b.com"` with a `NoEmail(filter)` guard → email span removed, `action=filter`.

## Scenario 2 — clean text passes untouched

- **No-skill baseline**: naive filters mangle safe text (false positives).
- **Expected**: `check --text "a clean response"` → `passed=True`, text unchanged.

## Scenario 3 — over-long output is repaired, not dropped

- **No-skill baseline**: output silently truncated mid-token or rejected wholesale.
- **Expected**: a `MaxLength(fix)` guard caps the text to the limit and reports `action=fix`.

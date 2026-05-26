# evaluate — skill-supply-chain-check

Judged on whether it catches genuinely risky scripts without drowning clean ones in noise.

## Rubric

| Dimension | Pass condition |
|-----------|----------------|
| Catches high risk | `os.system`, outbound HTTP, installs, secrets → `high` findings, non-zero exit. |
| Clean passes | A thin shim (import + delegate) yields zero findings. |
| Scope correct | SKILL.md prose mentioning "pip install"/"curl" produces no finding (scripts only). |
| Severity ranked | Findings carry `high`/`med` so reviewers triage. |

## Scenario 1 — a malicious script is flagged

- **No-skill baseline**: the skill is run and the script executes unreviewed.
- **Expected**: a script with `os.system(...)` + `requests.get(...)` → `high` findings, exit non-zero.

## Scenario 2 — a clean skill passes

- **No-skill baseline**: blanket distrust, or blanket trust — both wrong.
- **Expected**: auditing this repo's own thin-shim skills → zero `high` findings, exit 0.

## Scenario 3 — prose is not mistaken for code

- **No-skill baseline**: naive grep flags the word "curl" in documentation.
- **Expected**: a SKILL.md that *describes* risky commands in prose produces no finding; only executable files are scanned.

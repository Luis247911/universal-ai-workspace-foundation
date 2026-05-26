# evaluate — skill-author

Judged on whether the linter accepts valid skills and rejects malformed ones — objectively.

## Rubric

| Dimension | Pass condition |
|-----------|----------------|
| Accepts valid | A contract-compliant SKILL.md lints with zero errors. |
| Rejects invalid | Missing keys, bad name, wrong compat/status → error-level issues + non-zero exit. |
| Name == folder | A skill whose `name` differs from its folder is flagged (E013). |
| Dogfoods | Every skill in this repo passes the linter. |

## Scenario 1 — a well-formed skill passes

- **No-skill baseline**: hand-checking frontmatter by eye; subtle errors slip through.
- **Expected**: `lint` on a compliant skill → `[ok]`, exit 0.

## Scenario 2 — a forbidden name is caught

- **No-skill baseline**: a skill named with "claude" or with uppercase ships and fails to load.
- **Expected**: `lint` flags E010/E012 and exits non-zero.

## Scenario 3 — the repo dogfoods the contract

- **No-skill baseline**: skills drift from the format over time.
- **Expected**: `lint .claude/skills` → all skills pass; this is enforced in the test suite.

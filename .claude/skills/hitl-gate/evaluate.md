# evaluate — hitl-gate

Judged on whether the pause is genuinely durable and the decision routes correctly.

## Rubric

| Dimension | Pass condition |
|-----------|----------------|
| Durable | The interrupt persists to disk and is readable by a separate process. |
| Blocks | `resume` on a pending run returns non-zero (no silent proceed). |
| Approve → proceed | After `approve`, `resume` reports proceed. |
| Deny → feedback | After `deny`, `resume` returns the feedback for the next attempt. |

## Scenario 1 — pause survives process exit

- **No-skill baseline**: approval state held in memory, lost on restart → action runs unguarded.
- **Expected**: `request` in one process, `resume` in another before any decision → non-zero (pending).

## Scenario 2 — approve resumes the action

- **No-skill baseline**: no record of who approved or whether they did.
- **Expected**: `approve --run <id>` then `resume --run <id>` → proceed, exit 0.

## Scenario 3 — deny re-enters the loop with feedback

- **No-skill baseline**: denial just aborts; the reason is lost.
- **Expected**: `deny --run <id> --feedback "wrong recipient"` then `resume` → loop-with-feedback carrying that note.

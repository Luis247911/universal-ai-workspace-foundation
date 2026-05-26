# evaluate — memory-architect

Judged on whether the type×scope choices and the in-context/archival boundary hold up.

## Rubric

| Dimension | Pass condition |
|-----------|----------------|
| Boundary | Working items stay in-context; archival items are retrieved, not always present. |
| Recall | A similarity query returns the relevant archival item above noise. |
| Promote | Promoting a working item moves it out of context into durable storage. |
| Right scope | A user preference is stored at `user` scope, not `conversation`. |

## Scenario 1 — recall finds the relevant fact

- **No-skill baseline**: stuff everything in the prompt, or forget entirely.
- **Expected**: `demo` → querying "which test framework does the user like" returns the pytest preference from archival.

## Scenario 2 — promote crosses the boundary

- **No-skill baseline**: working notes are either lost or pinned in context forever.
- **Expected**: `demo` → a working item is promoted to episodic/user and the in-context count reflects it left core.

## Scenario 3 — scope is chosen by truth, not convenience

- **No-skill baseline**: everything saved at one scope, so facts leak or vanish.
- **Expected**: a durable preference is stored at `user` scope; transient task state stays at `conversation`/`session`.

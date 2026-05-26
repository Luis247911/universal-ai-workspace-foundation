# reference — memory types and scopes

Two axes. Pick a type (what kind of memory) and a scope (how widely shared). Then decide
in-context vs archival.

## Types

| Type | What it holds | Example | Lifetime |
|------|---------------|---------|----------|
| **working** | the current task scratchpad | "user is debugging a flaky test" | this turn / session |
| **factual** | stable facts | "the user prefers pytest" | long |
| **episodic** | events that happened, with time | "last week we migrated CI to GitHub Actions" | long, time-stamped |
| **semantic** | distilled knowledge / generalizations | "this team favors integration tests over mocks" | long |

Working memory is the in-context scratchpad; the other three are usually archival and
retrieved on demand.

## Scopes (narrowest → widest)

| Scope | Shared across | Use for |
|-------|---------------|---------|
| **conversation** | one thread | transient task state |
| **session** | one working session | things to carry between turns |
| **user** | all of a user's sessions | preferences, stable personal facts |
| **org** | all users in an org | shared policy, team conventions |

Rule of thumb: store a fact at the **widest scope at which it is actually true**, and no wider.
A personal preference is `user`; a one-off detail is `conversation`.

## In-context vs archival

- **In-context (core)**: always in the prompt. Keep it tiny — every token here is a token not
  available for reasoning. `core_append`, `core_replace`, `core_view`.
- **Archival**: stored outside the prompt, fetched by similarity search when relevant.
  `archival_insert`, `archival_search`, `recall_search`.
- **promote**: when a working item recurs or proves durable, promote it across the boundary
  into archival memory at the right type and scope.

## Anti-patterns

- Dumping everything into context "to be safe" → context bloat, higher cost, worse focus.
- Storing transient state at `user`/`org` scope → stale facts leak across sessions.
- Never promoting → the agent re-learns the same thing every session.
- Retrieving without tracing → you cannot tell *why* the agent recalled something.

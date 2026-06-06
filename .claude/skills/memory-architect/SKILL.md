---
name: memory-architect
description: Use this when an agent needs to remember things across turns or sessions — to choose the right memory type (working, factual, episodic, semantic) and scope (conversation, session, user, org), and to move items between in-context and archival storage. Triggers on "memory", "remember", "long-term", "persist context", "recall", "what should the agent store".
version: 1.0.0
compat: skill-format-1.0
status: experimental
---

# memory-architect

Designs an agent's memory along two axes: **what kind** of memory (type) and **how widely it is shared** (scope). The core discipline is deciding what lives *in context* (small, always present) versus *archival* (large, retrieved on demand) — because context is the scarce resource.

## When to use

- An agent forgets across turns/sessions, or its context is bloated with stale facts.
- Deciding what to keep in the prompt vs. retrieve on demand.
- Choosing whether a fact is per-conversation or shared across all of a user's sessions.

## Run it

```
python -m harness.memory demo
python .claude/skills/memory-architect/scripts/run.py demo
```

The demo walks working memory → promote to archival → vector recall, all in-memory and offline.

## Two axes (detail in `reference.md`)

- **Type**: `working` (in-context scratchpad), `factual` (stable facts), `episodic` (events that happened), `semantic` (distilled knowledge).
- **Scope**: `conversation` → `session` → `user` → `org` (narrowest to widest sharing).

## In-context vs archival

- **Core / in-context**: tiny, always in the prompt (current task, key facts). `core_append`, `core_view`.
- **Archival**: large, stored out-of-context, retrieved by similarity. `archival_insert`, `archival_search`.
- **promote**: move a working item across the boundary into durable archival memory when it proves worth keeping.

## Method

1. Default everything to working/conversation scope; promote only what recurs.
2. Keep the in-context set small — retrieve the rest from archival.
3. Pick the widest scope a fact is *true* at (a user preference is `user`, not `conversation`).
4. Pair recall with [[observability-tracer]] so you can see what was retrieved and why.

## Boundaries

- This is the toolkit for giving **an agent you build** a memory — **not** the memory of this workspace itself (that lives in `.ai-workspace/state/`; see the glossary in the repo `README.md`).
- This skill **owns** the type×scope model and the in-context/archival boundary.
- For *guarding* what gets written (no PII into long-term memory), use [[guardrail-designer]].
- The backend (pure-python cosine by default, numpy under the `[vector]` extra) is an implementation detail of the `memory` engine.

## Evals

See `evaluate.md` — 3 scenarios with a no-skill baseline.

## Attribution

Scope model reimplemented from mem0; the core/recall/archival split from Letta / MemGPT (OSS). No code copied. See `/sources/credits.md`.

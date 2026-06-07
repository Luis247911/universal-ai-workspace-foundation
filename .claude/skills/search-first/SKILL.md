---
name: search-first
description: Use this before writing custom code or adding a dependency — search for an existing library, tool, MCP server, or skill first, then decide adopt, extend, compose, or build. Triggers on "is there a library for", "before I build", "add X functionality", "do we already have", "research before coding", "reinvent the wheel".
version: 1.0.0
compat: skill-format-1.0
status: experimental
---

# search-first

Research before you code. Before writing a utility or adding functionality, check whether a
maintained solution already exists — in the repo, in package registries, in an MCP server, or in
another skill — and only then decide to build.

## When to use

- Starting a feature that probably has existing solutions.
- Adding a dependency or integration.
- About to write a new utility, helper, or abstraction.

## Workflow

1. **Need analysis** — state the capability and the language or framework constraints.
2. **Search in parallel** — does it already exist *in this repo* (grep modules and tests)? as a
   package (npm / PyPI / crates)? as an MCP server? as another skill?
3. **Evaluate** candidates: fit, maintenance, community, docs, license, dependency weight.
4. **Decide** with the matrix below.
5. **Implement** — install and configure, or write the minimal informed custom code.

## Decision matrix

| Signal | Action |
|---|---|
| Exact match, maintained, permissive license | **Adopt** — use directly |
| Partial match, good foundation | **Extend** — adopt + a thin wrapper |
| Several weak matches | **Compose** — combine a couple of small pieces |
| Nothing suitable | **Build** — custom, but informed by the search |

## Anti-patterns

- **Jumping to code** — writing a utility without checking it exists.
- **Ignoring MCP** — not checking whether a server already provides the capability.
- **Over-wrapping** — wrapping a library so heavily it loses its benefit.
- **Dependency bloat** — a huge package for one small need; prefer the smaller informed build.

## Boundaries

- This skill **owns** the *adopt-before-build* research step for tools and libraries.
- For triaging *which harness skill* fits a problem, use [[agent-pattern-selector]].
- For progressively retrieving *codebase context* (not external libraries), use [[iterative-retrieval]].

## Attribution

Structural idea (research-before-build with an adopt/extend/compose/build matrix) reimplemented from
a public skill pattern; no code or prose copied. See `/sources/credits.md`.

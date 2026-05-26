# Changelog

All notable changes to this project are documented here. Format based on
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/); this project follows
[Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [3.0.0] — 2026-05-26

v3.0 turns the foundation from a **pure Markdown control/policy layer** into a genuine, runnable
**starter harness** — while keeping the Markdown governance core unchanged in its role. Two layers
now live side by side: `.ai-workspace/` (governance, persists) and `.claude/` + `src/harness/`
(execution, runs). See `AGENTS.md` §2.5.

### Added

- **Engine `src/harness/`** — a pip-installable, stdlib-first package (`uaw-harness`) with eight
  areas: `eval`, `router`, `hitl`, `guardrails`, `observability`, `memory`, `orchestrator`,
  `skills`. A bare `pip install -e .` pulls **zero** third-party wheels.
- **12 Claude Code skills** under `.claude/skills/<slug>/` with official SKILL.md frontmatter; each
  script skill is a thin wrapper that forwards to `harness.<area>.__main__` (no duplicated logic).
- **Eval gate** with exit-code semantics (non-zero below threshold) — CI-usable, and the repo
  dogfoods it against its own skills and invariants.
- **mock-offline default** (`UAW_LLM=mock`): deterministic, no network/key → green CI. Live model
  calls are opt-in (`[llm]` extra + `UAW_LLM=live` + `ANTHROPIC_API_KEY`).
- **Tests + examples** — `pytest` per module, golden eval suites under `tests/goldens/`, one offline
  demo per area under `examples/`.
- **Packaging & CI** — `pyproject.toml`, `.github/workflows/ci.yml` (lint + test + eval gate on a
  Windows + Linux matrix, no secrets).
- **Release artifacts** — `NOTICE`, `sources/credits.md` (every borrowed structural idea attributed,
  no code/prose copied), active `.gitignore` and `.claudeignore`, `.claude/settings.json`
  (+ `.example` for local overrides, no secrets).
- **New policy** — `.ai-workspace/skills-authoring-policy.md` (frontmatter schema, SemVer + status
  promotion, the State-Write-Contract, no-premature-abstraction rule, domain neutrality).
- `install-harness.md` — how to install and run the execution layer.

### Changed

- **README** repositioned to a v3.0 runnable harness: the two-layer model, a runnable quickstart, a
  skill catalog, and an "Upgrade von v2.0" section.
- **Constitutional reconciliation** of the governance docs so the repo no longer contradicts itself:
  `AGENTS.md` (§2.5 two-layer model, §3 `.claude/` + infra-allowlist carve-outs, §5/§8 scoped),
  `setup-protocol.md` (decision-tree "Frage 0" routes runnable code to `.claude/`/`src/`),
  `security-policy.md` (§4.5 in-repo-code-trust model: versioned in-repo code is trusted to *run*,
  its outputs stay untrusted, external fetch/install stays gated), `adapter-policy.md` (§11 core vs.
  domain skills), plus `context-policy.md`, `quality-gates.md`, `file-lifecycle.md`, `CLAUDE.md`,
  `install-checklist.md`.

### Unchanged (intentionally)

- The governance core `.ai-workspace/**` stays **Markdown-only** and strict. Mount-point discipline,
  delegation model, context-loading rules, file-lifecycle, knowledge-graph protocol, and the
  document-normalization pipeline keep their v2.0 behavior and role.

### Breaking / repositioning

- The "**not an agent harness, not a skill-pack**" positioning is **removed** — the repo now *is* a
  runnable harness. Forks that relied on that framing should re-read the README and `AGENTS.md` §2.5.
- The top level now contains **non-Markdown files** (`src/`, `tests/`, `examples/`, `pyproject.toml`,
  `.claude/`, `.github/`, active ignore files). The Markdown-only invariant is now scoped to
  `.ai-workspace/**` (it was previously phrased repo-wide). Tooling that assumed "every file is
  Markdown" repo-wide must be re-scoped to `.ai-workspace/`.
- The **anti-sprawl rule gained two carve-outs** (`.claude/` execution mount + infra allowlist). A
  fork that copied the old `AGENTS.md` §3 verbatim should merge these edits, or its own discipline
  rules will reject the new layout.
- No prior git tags existed; **3.0.0 is the first tagged release**.

### Migration from v2.0

Two supported paths:

1. **Governance only (no-op).** Keep using `.ai-workspace/` + the boot files as before. Nothing
   breaks. To pick up the reconciled wording, merge the changed governance docs listed above.
2. **Adopt the harness.** Copy the execution layer as a unit (`.claude/`, `src/`, `tests/`,
   `examples/`, `pyproject.toml`, `.github/`, `sources/`, the active ignore files), then follow
   [`install-harness.md`](install-harness.md) (`pip install -e .` → zero third-party wheels). The
   skills load on demand via their `description`; start triage with `agent-pattern-selector`.

[3.0.0]: https://github.com/Luis247911/universal-ai-workspace-foundation/releases/tag/v3.0.0

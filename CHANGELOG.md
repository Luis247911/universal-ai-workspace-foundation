# Changelog

All notable changes to this project are documented here. Format based on
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/); this project follows
[Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [3.1.0] — 2026-06-06

A first-run onboarding plus an opt-in daily maintenance routine. The governance core
`.ai-workspace/**` stays Markdown-only and motorless; all new executable code lives in the execution
layer (`.claude/`). The kit's "default off" promise is deliberately and visibly amended: a single
one-time onboarding nudge now fires on first start (documented exception, opt-out via flag or
`UAW_DISABLE_ONBOARDING`).

### Added

- **First-run onboarding** — `first_run_onboarding` SessionStart(startup) hook (default ON) detects a
  fresh, unconfigured workspace (state placeholders present, no marker) and asks the model to run
  `/start`. Goes inert via a gitignored marker (`.claude/.onboarding-state.json`) or once the state
  placeholders are filled. Deletes nothing; opt-out via `UAW_DISABLE_ONBOARDING`.
- **`/start` command** — a single entry-point "conductor": forks existing-project (delegates to
  `/onboard`) vs. start-from-scratch (drives `setup-protocol.md` §1–§2) vs. leave-me-alone, then
  offers the opt-in helpers in plain language. Fills the previously missing interactive greenfield path.
- **Daily maintenance routine** — `daily_maintenance` SessionStart(startup+resume) hook (opt-in,
  default OFF) nudges one maintenance pass per local calendar day (file `scratch/`, flag dead
  `[[wiki-links]]`/stale notes, orphaned artifacts) per the `knowledge-graph-policy.md` §12 blueprints.
  Suggests only — never auto-applies. Finally gives the long-specified blueprints a trigger.
- **`tests/test_automation_hooks.py`** — off-path (inert, empty stdout, exit 0) and on-path (exactly
  one valid `hookSpecificOutput` JSON) checks for every automation hook; guards double-print
  regressions. Runs in the existing pytest gate.

### Changed

- **`.claude/AUTOMATION.md`** — the "default off / fresh clone fires nothing" line is amended to the
  documented one-time-onboarding exception; capability table, file list, self-tests, and a run-marker
  doctrine (a hook may write its own gitignored run-marker, never governance state or config) added.
- **`/uaw-automation`** — now covers the third helper (`daily_maintenance`) and the default-on
  onboarding in plain everyday terms.
- **Governance reconciliation** so the docs no longer contradict themselves: `knowledge-graph-policy.md`
  §7/§12 ("no active routine" → "an opt-in active maintenance nudge ships in the execution layer"),
  `file-lifecycle.md` §7 (cadences now have an opt-in trigger), `adapter-policy.md` §8,
  `setup-protocol.md` §2, `README.md` quickstart (advertises `/start`).
- **Decisions** — D-2026-06-06-01 (default-on first-run onboarding), D-2026-06-06-02 (opt-in daily
  maintenance), D-2026-06-06-03 (run-marker doctrine).

### Unchanged (intentionally)

- The governance core `.ai-workspace/**` stays Markdown-only and motorless; the invariant test
  `tests/test_governance_invariants.py` stays green (all new code is under `.claude/`). No new engine
  area and no `harness.governance` linter — named as future work (O1/O6).

## [3.0.1] — 2026-05-30

A documentation-clarity pass plus one machine-checked structural invariant. The governance core
`.ai-workspace/**` keeps its role **and** its content; this release only clarifies wording and adds a
guard rail. No new engine area, no new CLI, no version reposition.

### Added

- **Glossary** in `README.md` — disambiguates the easily-confused terms (governance, execution,
  `state` vs. the `memory` engine, knowledge, data-space, source, artifact, adapter, skill,
  delegation): what each is, where it lives, where it is governed. A pointer/index, not a second copy
  of any rule.
- **`tests/test_governance_invariants.py`** — asserts the two purely-mechanical invariants of the
  governance layer: `.ai-workspace/**` is Markdown-only, and no anti-sprawl-forbidden top-level
  directory exists under it. Runs inside the existing `pytest` gate — no new CI step, and **not** a
  shipped maintenance routine (stays within `knowledge-graph-policy.md` §12).
- **Scaling note** in `setup-protocol.md` (§7) — one workspace = one bounded context; unrelated
  domains get their own instance; shared knowledge is referenced by pointer, not copied.
- **State-file-compaction** note in `file-lifecycle.md` (§5) — how to roll up append-growing state
  files into a dated archive while leaving a pointer index behind.

### Changed

- **`memory-architect` skill** — its Boundaries now state explicitly that it builds memory for an
  agent you create, **not** the memory of this workspace (that is `.ai-workspace/state/`).

### Unchanged (intentionally)

- No `MAP.md`, no `foundation_version` stamp (rejected: without a sync mechanism it would silently go
  stale and lie), no `harness.governance` engine area. The `v3.0` strings stay — this is a PATCH, not
  a repositioning.

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

[3.1.0]: https://github.com/Luis247911/universal-ai-workspace-foundation/releases/tag/v3.1.0
[3.0.1]: https://github.com/Luis247911/universal-ai-workspace-foundation/releases/tag/v3.0.1
[3.0.0]: https://github.com/Luis247911/universal-ai-workspace-foundation/releases/tag/v3.0.0

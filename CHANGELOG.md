# Changelog

All notable changes to this project are documented here. Format based on
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/); this project follows
[Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [3.4.0] — 2026-09-30

Phase 5 of the long-term memory: autopilot. The memory now runs by itself in both ways in: a
fresh clone needs no `pip install`, and an existing project gets everything with one idempotent
command. Manual steps per way in: fresh clone 7 → 2, existing project 20 → 4 (README,
"Was automatisch läuft").

### Added

- **`adopt`** (`python3 <foundation>/.claude/uaw/mdm.py adopt <projekt> [--dry-run]`,
  D-2026-09-30-10): brings the memory into an existing project and only adds or merges. Governance
  skeleton where missing; existing `AGENTS.md`/`CLAUDE.md` keep their content and get one marked
  block (`<!-- uaw:begin -->`); the v3.2 `@current-session.md` import becomes `@now.md`; memory
  hooks, skills `merken` and `pflege`; `settings.json`, `automation.flags.json`, `.gitignore`,
  `.gitattributes` merged; migrations `now migrate`, `split-decisions`, optionally
  `import-automemory`, then `index`; CI template `.github/workflows/uaw-memory.yml` when the
  project uses GitHub. Files the foundation owns are listed with sha256 in
  `.claude/uaw/manifest.json`; an upgrade replaces only untouched ones. Second run: no diff.
- **Engine copy `.claude/uaw/`**: `harness.mdmemory` vendored by `adopt` (stdlib only), shim
  `.claude/uaw/mdm.py` (`python3 .claude/uaw/mdm.py <befehl>` = `python -m harness.mdmemory`,
  no install; in the foundation it uses `src/`). Registered in `AGENTS.md` §2.5,
  `context-policy.md` and `setup-protocol.md`.
- **Launcher `.claude/hooks/run.sh`**: every hook runs as `sh .../run.sh <hook>.py` and picks
  `$UAW_PYTHON`, `python3` or `python` (>= 3.9). Before, hooks called `python`, which a stock Mac
  does not have.
- **Hook `index_refresh`** (default ON, D-2026-09-30-09): regenerates the generated files after an
  edit to a note (PostToolUse) and heals a stale index at start (after `git pull`/merge).
- **`memory_boot`** nudges the skill `pflege` when the last report is older than 7 days (once a
  day at most).
- **`journal add KIND TEXT --session ID`**: appends and creates the session journal on first use;
  `now_init` names the exact command.
- **Python 3.9 support for the memory engine and hooks** (the stock macOS `python3`): new CI job
  `stock-macos-python` runs the memory, hook and end-to-end tests on `/usr/bin/python3`.
- **`tests/test_autopilot_e2e.py`**: Weg A (fresh clone, no install) and Weg B (fictional v3.2
  project with own AGENTS/CLAUDE, legacy registers, `current-session.md`, own settings hook,
  auto-memory folder): dry run changes nothing, adopt is lossless, second run has no diff, upgrade
  keeps edited files, a whole session runs through the hooks with only `python3` on the PATH.
- Decisions D-2026-09-30-09 (hooks keep the index current; supersedes -06) and
  D-2026-09-30-10 (engine copy per `adopt`; supersedes -05).

### Fixed (review of the 3.3.0 phases; fixed in their own branches)

- Phase 1: lossy frontmatter parse of `\"` before ` #`; BOM/blank after fences; duplicate keys
  and line breaks now rejected; `now trim` endless loop on multibyte lines and tiny limits;
  bullets moved with their continuation lines; CRLF size; Codex UUIDv7 short ids collided within
  ~1 min, CLI default session `manual` collided; a session over midnight got two journals;
  `now migrate` byte-exact via bytes + sha256, idempotent across days, seeds a template-only
  `now.md`; `journal append` limited to `journal/`.
- Phase 2: INDEX cap not guaranteed with many pinned notes; finished pinned notes stayed in the
  boot index; `@path` in summaries would be imported via the boot index; sensitive notes had
  speaking ids; `import-automemory` used a wrong folder name (spaces, dots, worktrees); broken
  note -> traceback.
- Phase 3: `memory_boot` listed the own journal after midnight and a parallel session could
  freeze a running journal (`pending` now lists finished journals only); `conflict` not
  idempotent; supersede cycles; unvalidated `--date`; `consolidated` ignored aliases and root;
  `journal_stub` appended on every exit; compact reminder lost without the engine.
- Phase 4: `report` ignored the hard boot limit in its exit code, wrote rollups in stdout mode
  and showed titles of sensitive notes; `--global` could point into the project and ignored it
  for path arguments; orphan/duplicate false positives.

### Changed

- All hook commands in `.claude/settings.json` and `.codex/hooks.json` go through `run.sh`.
- `AUTOMATION.md`, `memory-contract.md`, `session-contract.md`, the skills and the policies
  reference D-2026-09-30-09/-10. README rewritten around the two ways in.
- Boot 4,990 tokens (target 5,000), worst case 8,748 (hard 12,000).

### Upgrade from 3.2.x or 3.3.0

Run the starter prompt (README) or, from a fresh foundation clone,
`python3 <klon>/.claude/uaw/mdm.py adopt <projekt> --dry-run`, then without `--dry-run`. It
covers every step of "Migration from 3.2.x" below. The foundation repo itself: pull, nothing else.

## [3.3.0] — 2026-09-30

Phase 4 of the long-term memory: maintenance and division of labour. Completes the 3.3.0 line
(phases 1–4: journal + now.md, atomic notes + tiered index, consolidation, maintenance).

### Added

- **`memory-contract.md`** — ownership table, load contract and write paths for every memory
  (now.md, journal, notes, generated files, tables, external systems, auto-memory, optional
  global namespace), plus the five defaults: Markdown in git is canonical (operational data
  only by pointer), Claude auto-memory off, `scope`/`sensitivity` with an optional global
  namespace (off; private content belongs in a separate repo), local only with a later
  read-only MCP that may only write journal proposals, `merken` writes directly but asks first
  for person, global preference, supersede/correction and conflict.
- **`"autoMemoryEnabled": false`** in `.claude/settings.json` (per machine also
  `CLAUDE_CODE_DISABLE_AUTO_MEMORY=1`); existing auto-memory comes in via `import-automemory`.
- **Skill `pflege`** (weekly; `evaluate.md`, `reference.md` for `/schedule` and launchd) and
  **`python -m harness.mdmemory report [--write]`**: lint, stale notes (`review_after`,
  `last_confirmed` > 180 days), orphans, duplicate candidates, unconsolidated journals, boot
  budget, monthly rollup. Result is a report under the gitignored `scratch/maintenance/` or a PR,
  never an auto-merge.
- **Optional global namespace** — `--global` on every `harness.mdmemory` command, rooted at
  `$UAW_GLOBAL_MEMORY_DIR`; off unless set.
- **`templates/recall-set.md`** — 30 questions with expected notes; full-text or vector search
  only below 90 % hit rate (documented, not built).
- Decision D-2026-09-30-08 (memory contract).

### Changed

- `CLAUDE.md`, `state/project-index.md` and the boot index tightened again (INDEX lists only
  non-empty types); boot 4,944 tokens (target 5,000), worst case 8,707 (hard 12,000).
- `context-policy.md`, `.ai-workspace/README.md`, `AGENTS.md` cross-links, README glossary and
  `knowledge-graph-policy.md` §12 reference the contract and the `pflege` skill.

## [3.3.0a3] — 2026-09-30

Phase 3 of the long-term memory: consolidation. Journal entries become notes through one
tool-neutral procedure, and three small hooks keep it from being forgotten.

### Added

- **Skill `merken`** (`.claude/skills/merken/`, with `evaluate.md`, 5 scenarios): per candidate
  NOOP / ADD / UPDATE / SUPERSEDE / CONFLICT against existing notes. Asks first for person notes,
  global preferences, SUPERSEDE/corrections and CONFLICT; writes everything else directly.
  External content gets `origin: external` and never shows its summary in the index.
- **Consolidation helpers** in `harness.mdmemory`: `pending`, `candidates`, `supersede`
  (both sides, idempotent), `confirm` (NOOP with `last_confirmed`), `conflict` (pinned question
  of kind conflict), `consolidated` (freezes a journal with `konsolidiert_zu`). Lint checks that
  every `konsolidiert_zu` id exists.
- **Hooks, default ON, each behind a flag** in `.claude/automation.flags.json`:
  `memory_boot` (SessionStart: unconsolidated journals of other sessions, reminder after
  compact), `journal_stub` (SessionEnd: one fixed closing entry in this session's existing,
  unconsolidated journal; creates nothing; well below the 1.5 s budget), `precompact_reminder`
  (PreCompact: `systemMessage` to the user only, never blocks).
- **Codex**: `.codex/hooks.json` runs the same scripts (`now_init`, `memory_boot`,
  `journal_stub`, `precompact_reminder`) with `--tool codex`; hooks need trust via `/hooks`.
- Decisions D-2026-09-30-06 (memory hooks default ON, hook write doctrine (d); supersedes
  D-2026-09-30-02 and -03) and D-2026-09-30-07 (`.codex/` as config-only execution mount).

### Changed

- `AGENTS.md` §3 (`.codex/`), §6 (procedure `merken`); `session-contract.md` §3.3 describes the
  procedure tool-neutrally; `context-policy.md`, `.claude/AUTOMATION.md`, README follow.
- The boot index shows only the summary per line (sub indexes keep title + summary), so new
  decisions do not push the boot budget; `new` rejects titles over 100 characters.

## [3.3.0a2] — 2026-09-30

Phase 2 of the long-term memory: one note per file, a generated and capped boot index, the four
registers become generated views. Boot cost drops from ~7.1k to ~5.0k tokens and has a tested
worst case.

### Added

- **Atomic notes** `knowledge/<typ>/<id>.md` (types person, preference, project, decision,
  reference, concept, question), schema v1 in `templates/knowledge-note.md` and
  `harness.mdmemory.notes`: validity (`valid_from/valid_until`), symmetric
  `supersedes/superseded_by`, `change` (veraendert/korrigiert), `sources` (required),
  `scope`, `sensitivity`, `origin`, `pinned`, review dates. Old IDs stay valid as `aliases`.
- **Generated, tiered index** — `knowledge/INDEX.md` (pinned + recently changed, capped at 8 KB /
  80 lines, now the fifth boot file, imported by `CLAUDE.md`) and `knowledge/_typen/<typ>.md`
  (<= 50 entries per part, split beyond). Sensitive or external notes appear with their id only.
- **`harness.mdmemory` commands** — `index [--check]`, `lint`, `budget`, `new`,
  `split-decisions`, `export-legacy`, `rollup` (`journal/YYYY/MM/_rollup.md`),
  `import-automemory` (Claude auto-memory files -> one journal with candidates; the source is
  never changed; idempotent by content hash).
- **Boot budget test** — AGENTS + CLAUDE + project-index + now + INDEX: target 5,000 tokens
  (lint warning), hard 12,000 including the worst case of now.md (4 KB) and INDEX.md (8 KB).
- **Merge test for parallel decisions** — two worktrees each record a decision: legacy register
  conflicts every time, notes + generated views merge cleanly (`merge=union` in
  `.gitattributes`, then `mdmemory index`).
- Decisions D-2026-09-30-04 (atomic notes canonical, registers generated) and D-2026-09-30-05
  (scripts may write derived Markdown; supersedes D-2026-06-04-01).

### Changed

- `state/decisions.md`, `open-questions.md`, `assumptions.md`, `risks-and-constraints.md` are
  generated views. The 10 decisions are notes under `knowledge/decision/`; the pre-migration
  registers are archived byte for byte in `archive/2026-09-30/state-*.md`. Round trip register
  -> notes -> register is tested; `export-legacy` rebuilds the old format.
- `templates/knowledge-note.md` is now schema v1; the long-form template lives on as
  `templates/topic-note.md` (topic graph with MOCs stays optional).
- `AGENTS.md` (boot order with five files, §2 mounts, §9 memory), `CLAUDE.md` (duplicates of
  AGENTS/policies removed, content kept in the policies), `state/project-index.md` tightened;
  `context-policy.md`, `session-contract.md` §3.3, `knowledge-graph-policy.md` §4–§8,
  `skills-authoring-policy.md` §6 and the references in the other policies follow.
- New note ids carry a random 4-hex suffix and no automatic counter alias, so parallel
  worktrees never create the same file or alias (`new --alias auto` on request).

### Migration

Existing projects: `python -m harness.mdmemory split-decisions` (archives each register byte for
byte, converts entries, checks the round trip before writing, idempotent), then
`python -m harness.mdmemory lint`.

## [3.3.0a1] — 2026-09-30

Phase 1 of the long-term memory (3.3.0 line): episodes are kept, parallel sessions no longer
conflict. The shared, overwritten `state/current-session.md` is replaced by a per-worktree
`state/now.md` plus an append-only session journal.

### Added

- **`journal/` mount** — `.ai-workspace/journal/YYYY/MM/<datum>-<kurzid>.md`, one file per session,
  append-only, written *during* the work after each relevant result, Never Auto-Load, frozen after
  consolidation. Registered in `AGENTS.md` §2, `context-policy.md`, `setup-protocol.md` (decision
  tree 6b), `file-lifecycle.md` (seventh zone) and `.ai-workspace/README.md`. Template
  `templates/journal-entry.md`, rules in `journal/README.md`.
- **`harness.mdmemory`** (stdlib) — `now ensure|trim|migrate`, `journal new|append`; a
  deterministic frontmatter subset; all budgets and tool limits with doc links in `limits.py`.
  Console script `uaw-mdmemory`.
- **`now_init` hook** — SessionStart (all sources), **default ON**: creates the gitignored
  `state/now.md` from `templates/session-state.md`, trims it to 4 KB (overflow goes to the session
  journal, never dropped), names session short id + journal path, flags a leftover
  `current-session.md`.
- **Merge test** `tests/test_parallel_sessions.py` — real `git merge` of two worktrees. Measured
  with `--runs 60`: before 60/60 runs with a session-state conflict, after 0/60.
- Decisions D-2026-09-30-01 (now.md + journal, supersedes D-2026-06-07-01), -02 (hook write
  doctrine, supersedes D-2026-06-06-03), -03 (automation defaults, supersedes D-2026-06-04-02).

### Changed

- **Boot file 4** is `state/now.md` (was `state/current-session.md`); `CLAUDE.md` imports it.
- **`session-contract.md`** — journal first, then `now.md`; "check/scan decisions.md and
  open-questions.md" is replaced by "read the index, then grep; never read files over 1,000 lines
  in full" (§1.4, §5.3).
- `boot_reload`, `recitation_nudge`, `session_state_guard` point at `now.md` / the journal
  (`boot_reload` falls back to a legacy `current-session.md`).
- `templates/session-state.md` is now the `now.md` template (≤ 4 KB).
- `.gitignore` and `templates/gitignore-template.md` ignore `.ai-workspace/state/now.md`.

### Removed (with migration path)

- `state/current-session.md` — its content is preserved byte for byte in
  `journal/2026/09/2026-09-30-migration.md`.

### Migration from 3.2.x

1. `python -m harness.mdmemory now migrate` — copies `state/current-session.md` verbatim into
   `journal/<yyyy>/<mm>/<datum>-migration.md` and seeds a local `state/now.md` from it.
2. Rerun with `--remove-legacy` (deletes the old file only after checking the journal holds it
   byte for byte), add `.ai-workspace/state/now.md` to `.gitignore`, commit.
3. Replace `@.ai-workspace/state/current-session.md` with `@.ai-workspace/state/now.md` in
   `CLAUDE.md`.

## [3.2.1] — 2026-09-29

Quick wins from a repo review: a deterministic boot, a current live-model default, and a type
check in CI. No new skill, hook, or engine area.

### Changed

- **Boot order is now enforced** — `CLAUDE.md` imports `AGENTS.md`, `state/project-index.md` and
  `state/current-session.md` via `@`-imports, so Claude Code loads all four boot files without
  relying on the model to follow "read AGENTS.md first". `boot_reload` is now largely redundant
  for Claude Code (kept for compatibility, still default OFF).
- **Live LLM gateway** (`harness.core.llm`) — default model `claude-opus-5-5` (was
  `claude-sonnet-4-6`), overridable via `UAW_MODEL`; default `max_tokens` 16000 (was 512, too low
  for models that think before answering); server-side refusal fallback (`fallbacks="default"`)
  on supporting models; a remaining refusal raises `HarnessError` instead of returning empty text;
  empty `system` is no longer sent. `[llm]` extra now requires `anthropic>=1.9`.
- **`tests/test_llm.py`** — offline tests for the live path (fallback routing, `UAW_MODEL`
  override, refusal) against a stub `anthropic` module.
- **Router demo config** — current model IDs (`claude-sonnet-5-5`, `claude-opus-5-5`).
- **CI** — `mypy src` gate added; matrix now covers macOS and Python 3.13 (was 3.12).
- **mypy clean** — optional-extra imports ignored via `[tool.mypy]` overrides; typed
  `_JSON_TYPES` in `eval/assertions.py`.
- **Doc drift fixed** — README skill count (12 → 21), version-free onboarding prompts,
  `/automation` → `/uaw-automation` in `session-contract.md`, `harness.__version__` (was 3.0.0).

## [3.2.0] — 2026-06-07

Nine new domain-neutral **pattern skills** plus four **opt-in automation hooks** (default OFF) that
back several of them with an enforcement/reminder layer, plus a canonical answer to "how is
current-session.md kept safe?". The governance core `.ai-workspace/**` stays Markdown-only and
motorless; all new code is under `.claude/`. The first-run-onboarding invariant is untouched (fires
once on a fresh clone, then inert).

### Added

- **Nine pure-pattern skills** (instruction-only, no bundled code) under `.claude/skills/`:
  `iterative-retrieval`, `agent-architecture-audit`, `external-content-security`, `harness-optimizer`,
  `strategic-compact`, `verification-loop`, `tdd-workflow`, `search-first`, `prompt-optimizer`. Each
  reimplements a public structural idea (attributed in `NOTICE` / `sources/credits.md`); the
  `agent-pattern-selector` triage table and the README skill catalog route to them.
- **`prompt_optimizer` hook** — `UserPromptSubmit`, default OFF. On a vague prompt (short with no
  action verb, antecedent-less pronouns, or a semantically open question) it injects the
  `prompt-optimizer` skill's three-tier "expose-assumptions-first" protocol. Advisory; never blocks.
- **`external_content_guard` hook** — `PostToolUse` (`WebFetch|WebSearch`), default OFF. Re-asserts
  the `external-content-security` quarantine (treat results as DATA, scan for injection) after a
  fetch, and optionally checks the called URL against a gitignored per-project deny-list
  (`.claude/external-content-denylist.txt`; the repo ships none). Advisory; never blocks.
- **`compact_nudge` hook** — `PostToolUse`, default OFF. Counts context-growing tool calls in a
  gitignored marker and suggests a strategic `/compact` at a task boundary every
  `UAW_COMPACT_NUDGE_THRESHOLD` (default 60) calls; silent in between.
- **`session_state_guard` hook** — `PostToolUse` (`Write|Edit|NotebookEdit`), default OFF. A
  throttled, **staleness-gated** reminder: it speaks only when `current-session.md` has not been
  updated for `UAW_STATE_GUARD_STALE_MINUTES` (default 20) of active work, at most once per window —
  so diligent recitation never triggers it. Answers "a per-turn nudge is noisy".
- **Tests** — `tests/test_automation_hooks.py` extended (now 8 hooks): off-path inert for all, plus
  fire/inert paths for each new hook (vague vs. clear prompt, watched vs. other tool + deny-list hit,
  threshold counter, fresh vs. stale vs. throttled state).

### Changed

- **`.claude/automation.flags.json`** — four new keys, all `false` (`first_run_onboarding` stays
  `true`); **`.claude/settings.json`** — additive registration only (existing SessionStart and the
  `recitation_nudge` PostToolUse entry are byte-for-byte unchanged); a `UserPromptSubmit` block added.
- **`.claude/AUTOMATION.md`** — capability table, file list, off-path self-tests, verified primitives
  (`UserPromptSubmit` + arbitrary `PostToolUse` matchers), and a new **Session-State-Durability**
  section answering the rotation and end-of-session questions.
- **`session-contract.md` §3 / `current-session.md` §5** — clarified that `current-session.md` is a
  living file whose history is git (overwrite is safe with regular commits), not per-session archive
  rotation.
- **`/uaw-automation`** — now also lists the four advanced opt-in helpers in plain language.
- **Decisions** — D-2026-06-07-01 (state-durability = living file + git), D-2026-06-07-02 (four
  opt-in hooks).

### Unchanged (intentionally)

- The first-run-onboarding behavior (`first_run_onboarding`, default ON, once per fresh workspace) and
  the three existing helpers (`boot_reload`, `recitation_nudge`, `daily_maintenance`) are untouched.
  The governance invariant test `tests/test_governance_invariants.py` stays green (all new code under
  `.claude/`). No reliable end-of-session auto-write is claimed — a hard kill fires no hook.

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

[3.2.1]: https://github.com/Luis247911/universal-ai-workspace-foundation/releases/tag/v3.2.1
[3.2.0]: https://github.com/Luis247911/universal-ai-workspace-foundation/releases/tag/v3.2.0
[3.1.0]: https://github.com/Luis247911/universal-ai-workspace-foundation/releases/tag/v3.1.0
[3.0.1]: https://github.com/Luis247911/universal-ai-workspace-foundation/releases/tag/v3.0.1
[3.0.0]: https://github.com/Luis247911/universal-ai-workspace-foundation/releases/tag/v3.0.0

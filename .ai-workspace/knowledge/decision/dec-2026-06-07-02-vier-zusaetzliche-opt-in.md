---
id: dec-2026-06-07-02-vier-zusaetzliche-opt-in
type: decision
title: Vier zusaetzliche opt-in Execution-Hooks unter .claude/ (default AUS)…
summary: "Vier zusaetzliche opt-in Execution-Hooks unter .claude/ (default AUS): prompt_optimizer (UserPromptSubmit…"
aliases: [D-2026-06-07-02]
status: active
valid_from: 2026-06-07
valid_until:
supersedes: []
superseded_by:
change:
confidence: bestaetigt
sources: ["legacy:state/decisions.md#D-2026-06-07-02"]
links: []
scope: project
sensitivity: normal
origin: internal
pinned: false
updated: 2026-06-07
last_confirmed: 2026-06-07
review_after:
alternatives: []
reversibility: reversible
decided_by:
legacy_keys: [ID, Datum, Status, Reversibilitaet, Follow-up-Date, Supersedes]
---
Migriert aus `state/decisions.md` am 2026-09-30.

## Entscheidung

Vier zusaetzliche opt-in Execution-Hooks unter `.claude/` (default AUS): `prompt_optimizer` (UserPromptSubmit, vage-Prompt-Disambiguierung), `external_content_guard` (PostToolUse WebFetch|WebSearch, Quarantaene-Reminder + optionale gitignored Projekt-Deny-Liste), `compact_nudge` (PostToolUse, periodischer Strategic-Compact-Vorschlag via gitignored Zaehler-Marker), `session_state_guard` (PostToolUse Write|Edit|NotebookEdit, staleness-gegateter, gedrosselter Reminder, `current-session.md` zu sichern). Statisch + additiv in `settings.json` registriert; bestehende Hooks (inkl. `first_run_onboarding` default AN) unveraendert.

## Begruendung

Ergaenzt die Phase-1-Skills (external-content-security, strategic-compact, prompt-optimizer) um ihre opt-in Durchsetzungs-/Erinnerungs-Schicht. Jeder Hook self-gated (Flag false -> inert), advisory (kein exit 2, kein Governance-State-Write), Marker gemaess D-2026-06-06-03. `session_state_guard` beantwortet "Per-Turn-Reminder nervt" durch Staleness-Gating statt Per-Event-Nudge. Haelt C1/C2 + D-2026-06-04-01.

## Verlauf

- 2026-09-30 · migriert aus `state/decisions.md` (Alt-ID D-2026-06-07-02)

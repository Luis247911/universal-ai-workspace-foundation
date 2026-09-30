---
id: dec-2026-09-30-codex-ist-zweiter-execution-mount-nur-6a3b
type: decision
title: .codex/ ist zweiter Execution-Mount, nur fuer die Hook-Konfiguration von Codex
summary: Codex ruft dieselben Hook-Skripte aus .claude/hooks/ auf; .codex/ enthaelt keinen eigenen Code
aliases: [D-2026-09-30-07]
status: active
valid_from: 2026-09-30
valid_until:
supersedes: []
superseded_by:
change:
confidence: bestaetigt
sources: [user:auftrag-2026-09-30-memory-phase-3]
links: [D-2026-09-30-06]
scope: project
sensitivity: normal
origin: internal
pinned: false
updated: 2026-09-30
last_confirmed: 2026-09-30
review_after:
alternatives: []
reversibility: reversible
decided_by: user
---
## Entscheidung

`.codex/` ist neben `.claude/` ein zweiter Execution-Mount im Repo-Root. Er enthaelt nur die Konfiguration `.codex/hooks.json`, keinen eigenen Code und keine Inhalte.

Die Hooks rufen dieselben Skripte unter `.claude/hooks/` auf:

- ueber `$(git rev-parse --show-toplevel)`,
- mit `--tool codex`,
- gesteuert von denselben Flags in `.claude/automation.flags.json`.

Das Konsolidierungs-Verfahren (`merken`) ist tool-neutral in `AGENTS.md` §6 und `session-contract.md` §3.3 beschrieben. Codex nutzt es ohne eigenen Skill-Mount.

## Begruendung

Codex liest `AGENTS.md`, aber nicht `.claude/settings.json`. Ohne eigene Hook-Konfiguration fehlten `now.md`, der Hinweis auf offene Journale und der Journal-Abschluss.

Eine gemeinsame Skript-Basis verhindert doppelte Logik. Projekt-Hooks laufen in Codex erst, wenn der User sie per `/hooks` geprueft und als vertrauenswuerdig markiert hat. Es gibt also keine stille Ausfuehrung.

`.codex/` ist kein verbotener Name, und die Invarianten C1 und C2 betreffen nur `.ai-workspace/`.

## Belege

- `tests/test_mdmemory_consolidate.py::test_hook_registrations_match_flags_and_scripts`: gleiche Hooks in beiden Tools, SessionEnd-Timeout hoechstens 3 s.

## Verlauf

- 2026-09-30 · angelegt

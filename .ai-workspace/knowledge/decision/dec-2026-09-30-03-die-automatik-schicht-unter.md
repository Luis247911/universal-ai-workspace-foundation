---
id: dec-2026-09-30-03-die-automatik-schicht-unter
type: decision
title: Die Automatik-Schicht unter .claude/ bleibt opt-in und default AUS
summary: Die Automatik-Schicht unter .claude/ bleibt opt-in und default AUS
aliases: [D-2026-09-30-03]
status: superseded
valid_from: 2026-09-30
valid_until: 2026-09-30
supersedes: [dec-2026-06-04-02-eine-optionale-repo-committete]
superseded_by: dec-2026-09-30-gedaechtnis-hooks-sind-default-an-hooks-ec11
change:
confidence: bestaetigt
sources: ["legacy:state/decisions.md#D-2026-09-30-03"]
links: []
scope: project
sensitivity: normal
origin: internal
pinned: false
updated: 2026-09-30
last_confirmed: 2026-09-30
review_after:
alternatives: []
reversibility: reversible
decided_by:
legacy_keys: [ID, Datum, Status, Reversibilitaet, Follow-up-Date, Supersedes]
---
Migriert aus `state/decisions.md` am 2026-09-30.

## Entscheidung

Die Automatik-Schicht unter `.claude/` bleibt opt-in und default AUS. Ausnahmen mit default AN sind der einmalige Erst-Start-Stups `first_run_onboarding` (D-2026-06-06-01) und `now_init` (SessionStart: legt die lokale `state/now.md` an, haelt 4 KB ein, nennt Session-Kurz-ID und Journal-Pfad). Jeder Hook bleibt self-gated ueber `.claude/automation.flags.json`, reversibel und beruehrt `~/.claude/` nie.

## Begruendung

Ohne `now_init` fehlt in jedem frischen Clone und jedem neuen Worktree die Boot-Datei `now.md`, weil sie gitignored ist. Der Hook ist deterministisch, schnell und schreibt keine Inhalte der Arbeit. Uebernimmt den Rest von D-2026-06-04-02 unveraendert.

## Verlauf

- 2026-09-30 · migriert aus `state/decisions.md` (Alt-ID D-2026-09-30-03)
- 2026-09-30 · abgeloest durch dec-2026-09-30-gedaechtnis-hooks-sind-default-an-hooks-ec11 (veraendert)

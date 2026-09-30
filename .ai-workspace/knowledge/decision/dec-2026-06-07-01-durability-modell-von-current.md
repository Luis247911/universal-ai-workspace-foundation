---
id: dec-2026-06-07-01-durability-modell-von-current
type: decision
title: Durability-Modell von current-session.md ist kanonisch die lebende Datei +…
summary: Durability-Modell von current-session.md ist kanonisch die lebende Datei + git-Historie (kein mechanischer…
aliases: [D-2026-06-07-01]
status: superseded
valid_from: 2026-06-07
valid_until: 2026-09-30
supersedes: []
superseded_by: dec-2026-09-30-01-der-live-zustand-liegt-in-state
change:
confidence: bestaetigt
sources: ["legacy:state/decisions.md#D-2026-06-07-01"]
links: []
scope: project
sensitivity: normal
origin: internal
pinned: false
updated: 2026-09-30
last_confirmed: 2026-06-07
review_after:
alternatives: []
reversibility: reversible
decided_by:
legacy_keys: [ID, Datum, Status, Reversibilitaet, Follow-up-Date, Supersedes]
---
Migriert aus `state/decisions.md` am 2026-09-30.

## Entscheidung

Durability-Modell von `current-session.md` ist kanonisch die lebende Datei + git-Historie (kein mechanischer Pro-Session-Archiv-Rotations-Kreislauf). Overwrite ist non-destruktiv via git (getrackte Datei); `archive/` bleibt fuer semantische Snapshots. `session-contract.md` §3 / `current-session.md` §5 entsprechend praezisiert. Ein zuverlaessiger End-of-Session-Auto-Write ist nicht machbar (harter Kill feuert keinen Hook; Hook schreibt keinen Governance-State); Absicherung = kontinuierliche Frische (opt-in `session_state_guard`) + Commit-Disziplin.

## Begruendung

Macht die implizite Design-Entscheidung explizit und beantwortet die wiederkehrende Frage Rotation-vs-Overwrite. git ist bereits die Versionshistorie -> Rotation waere redundant + Churn. Haelt den motorlosen Governance-Core (D-2026-06-04-01); der Reminder lebt in der Execution-Schicht.

## Verlauf

- 2026-09-30 · migriert aus `state/decisions.md` (Alt-ID D-2026-06-07-01)

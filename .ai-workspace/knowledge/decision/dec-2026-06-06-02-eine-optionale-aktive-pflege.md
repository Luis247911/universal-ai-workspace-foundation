---
id: dec-2026-06-06-02-eine-optionale-aktive-pflege
type: decision
title: Eine optionale aktive Pflege-Routine (daily_maintenance) wird als opt-in…
summary: Eine optionale aktive Pflege-Routine (daily_maintenance) wird als opt-in SessionStart-Hook (startup+resume) unter…
aliases: [D-2026-06-06-02]
status: active
valid_from: 2026-06-06
valid_until:
supersedes: []
superseded_by:
change:
confidence: bestaetigt
sources: ["legacy:state/decisions.md#D-2026-06-06-02"]
links: []
scope: project
sensitivity: normal
origin: internal
pinned: false
updated: 2026-06-06
last_confirmed: 2026-06-06
review_after:
alternatives: []
reversibility: reversible
decided_by:
legacy_keys: [ID, Datum, Status, Reversibilitaet, Follow-up-Date, Supersedes]
---
Migriert aus `state/decisions.md` am 2026-09-30.

## Entscheidung

Eine optionale aktive Pflege-Routine (`daily_maintenance`) wird als opt-in SessionStart-Hook (startup+resume) unter `.claude/` ergaenzt, default AUS. Sie nudged 1x/lokalem-Kalendertag einen Pflege-Pass (scratch/-Einsortierung, KG-Lint tote `[[wiki-links]]`/stale notes, verwaiste Artefakte) gemaess knowledge-graph-policy.md §12 Blueprints; sie schlaegt nur vor, mutiert nie selbst.

## Begruendung

Schliesst die Luecke "keine aktive Routine" (kg-policy.md §7/§12) mit einem Motor in der Execution-Schicht, ohne den motorlosen Governance-Core (D-2026-06-04-01) zu verletzen. Modell prueft + schlaegt vor, Hauptsession verifiziert (delegation-policy.md).

## Verlauf

- 2026-09-30 · migriert aus `state/decisions.md` (Alt-ID D-2026-06-06-02)

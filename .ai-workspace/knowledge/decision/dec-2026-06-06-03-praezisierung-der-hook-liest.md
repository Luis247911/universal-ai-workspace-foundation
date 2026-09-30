---
id: dec-2026-06-06-03-praezisierung-der-hook-liest
type: decision
title: "Praezisierung der \"Hook liest nur\"-Doktrin: Execution-Hooks unter .claude/…"
summary: "Praezisierung der \"Hook liest nur\"-Doktrin: Execution-Hooks unter .claude/ duerfen ihren eigenen ephemeren, gitignored…"
aliases: [D-2026-06-06-03]
status: superseded
valid_from: 2026-06-06
valid_until: 2026-09-30
supersedes: []
superseded_by: dec-2026-09-30-02-schreib-doktrin-fuer-execution
change:
confidence: bestaetigt
sources: ["legacy:state/decisions.md#D-2026-06-06-03"]
links: []
scope: project
sensitivity: normal
origin: internal
pinned: false
updated: 2026-09-30
last_confirmed: 2026-06-06
review_after:
alternatives: []
reversibility: reversible
decided_by:
legacy_keys: [ID, Datum, Status, Reversibilitaet, Follow-up-Date, Supersedes]
---
Migriert aus `state/decisions.md` am 2026-09-30.

## Entscheidung

Praezisierung der "Hook liest nur"-Doktrin: Execution-Hooks unter `.claude/` duerfen ihren eigenen ephemeren, gitignored Lauf-Marker schreiben (z.B. `.claude/.daily_maintenance_last`; `/start` schreibt `.claude/.onboarding-state.json`). Verboten bleibt das Schreiben nach `.ai-workspace/**` (Governance-State) und nach `automation.flags.json` (Config) ausser durch Modell/Nutzer.

## Begruendung

Ein 1x/Tag-Hook braucht einen eigenen Timestamp, um nicht mehrfach zu feuern. Die Grenze ist nicht "Hook schreibt nie", sondern "Hook schreibt nie Governance-State/Config". Haelt Invarianten C1/C2 + D-2026-06-04-01 ein.

## Verlauf

- 2026-09-30 · migriert aus `state/decisions.md` (Alt-ID D-2026-06-06-03)

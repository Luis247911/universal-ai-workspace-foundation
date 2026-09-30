---
id: dec-2026-09-30-02-schreib-doktrin-fuer-execution
type: decision
title: Schreib-Doktrin fuer Execution-Hooks
summary: Schreib-Doktrin fuer Execution-Hooks
aliases: [D-2026-09-30-02]
status: superseded
valid_from: 2026-09-30
valid_until: 2026-09-30
supersedes: [dec-2026-06-06-03-praezisierung-der-hook-liest]
superseded_by: dec-2026-09-30-gedaechtnis-hooks-sind-default-an-hooks-ec11
change:
confidence: bestaetigt
sources: ["legacy:state/decisions.md#D-2026-09-30-02"]
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

Schreib-Doktrin fuer Execution-Hooks. Ein Hook darf (a) seinen eigenen ephemeren, gitignored Lauf-Marker unter `.claude/` schreiben, (b) die gitignored, worktree-lokale `state/now.md` aus der Vorlage anlegen und auf 4 KB kuerzen, (c) den dabei entstehenden Ueberlauf ans Ende des eigenen Session-Journals anhaengen (Datei anlegen, falls sie fehlt). Verboten bleiben: bestehende Inhalte aendern, fremde Journale, Notizen, Decisions oder andere State-Dateien beschreiben, `automation.flags.json` aendern.

## Begruendung

`now.md` ist gitignored und hat eine harte Groessengrenze; beides laesst sich nur mechanisch zuverlaessig einhalten. Der Ueberlauf wandert verlustfrei ins Journal statt verworfen zu werden. Alle geschriebenen Dateien sind `.md`, die Invarianten C1/C2 bleiben gruen. Uebernimmt die Marker-Regel aus D-2026-06-06-03.

## Verlauf

- 2026-09-30 · migriert aus `state/decisions.md` (Alt-ID D-2026-09-30-02)
- 2026-09-30 · abgeloest durch dec-2026-09-30-gedaechtnis-hooks-sind-default-an-hooks-ec11 (veraendert)

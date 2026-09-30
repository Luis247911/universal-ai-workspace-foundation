---
id: dec-2026-09-30-01-der-live-zustand-liegt-in-state
type: decision
title: Der Live-Zustand liegt in state/now.md (gitignored, pro Worktree, harte Grenze…
summary: Der Live-Zustand liegt in state/now.md (gitignored, pro Worktree, harte Grenze 4 KB, Trim ins Journal)
aliases: [D-2026-09-30-01]
status: active
valid_from: 2026-09-30
valid_until:
supersedes: [dec-2026-06-07-01-durability-modell-von-current]
superseded_by:
change:
confidence: bestaetigt
sources: ["legacy:state/decisions.md#D-2026-09-30-01"]
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

Der Live-Zustand liegt in `state/now.md` (gitignored, pro Worktree, harte Grenze 4 KB, Trim ins Journal). Die Historie liegt im neuen Mount `journal/YYYY/MM/<datum>-<kurzid>.md`: eine Datei pro Session, nur ergaenzt, waehrend der Arbeit nach jedem relevanten Ergebnis geschrieben, Never Auto-Load, nach Konsolidierung unveraenderlich. `state/current-session.md` entfaellt; ihr Inhalt ist als `journal/2026/09/2026-09-30-migration.md` byte-genau gesichert, Migrationspfad `python -m harness.mdmemory now migrate`.

## Begruendung

Eine geteilte, ueberschriebene Datei verliert zwischen zwei Commits jede fruehere Fassung und erzeugt bei zwei parallelen Sessions in jedem Fall einen Merge-Konflikt (gemessen: 100 %; mit now.md + Journal: 0 %, Test `tests/test_parallel_sessions.py`). Eine Datei pro Session hat genau einen Schreiber. Schreiben waehrend der Arbeit statt am Ende schuetzt vor Verlust bei hartem Abbruch, weil kein Hook den Abbruch zuverlaessig abfaengt.

## Verlauf

- 2026-09-30 · migriert aus `state/decisions.md` (Alt-ID D-2026-09-30-01)

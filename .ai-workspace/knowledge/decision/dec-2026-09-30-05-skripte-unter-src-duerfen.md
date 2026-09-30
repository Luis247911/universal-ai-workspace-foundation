---
id: dec-2026-09-30-05-skripte-unter-src-duerfen
type: decision
title: Skripte unter src/ duerfen abgeleitete Markdown-Dateien in .ai-workspace/ schreiben
summary: Generierte Indizes, Sichten und Rollups entstehen per Skript; der Core bleibt markdown-only und ohne eigenen Motor
aliases: [D-2026-09-30-05]
status: superseded
valid_from: 2026-09-30
valid_until: 2026-09-30
supersedes: [dec-2026-06-04-01-der-governance-core-ai]
superseded_by: dec-2026-09-30-die-gedaechtnis-engine-kommt-per-adopt-66bd
change: veraendert
confidence: bestaetigt
sources: [user:auftrag-2026-09-30-memory-phase-2]
links: [D-2026-09-30-04, D-2026-09-30-02]
scope: project
sensitivity: normal
origin: internal
pinned: true
updated: 2026-09-30
last_confirmed: 2026-09-30
review_after: 2027-03-31
alternatives: [Indizes von Hand pflegen, Indizes nur ausserhalb des Repos erzeugen]
reversibility: reversible
decided_by: user
---
## Entscheidung

Der Governance-Core `.ai-workspace/` bleibt markdown-only und ohne eigenen Motor. Ausfuehrbarer Code lebt weiter nur unter `.claude/` und `src/`, und die Invarianten C1 und C2 gelten unveraendert.

Neu: Code aus `src/harness/mdmemory/` darf in `.ai-workspace/` abgeleitete Dateien schreiben, wenn er dabei vier Regeln einhaelt:

1. Nur `.md`-Dateien.
2. Deterministisch: ein zweiter Lauf erzeugt keinen Diff, die Ausgabe enthaelt keine Uhrzeiten.
3. Die Datei traegt die Marke `GENERIERT`.
4. Die Datei laesst sich jederzeit aus den kanonischen Quellen neu erzeugen.

Das gilt heute fuer `knowledge/INDEX.md`, `knowledge/_typen/*.md`, die vier Register-Sichten unter `state/` und `journal/YYYY/MM/_rollup.md`.

Dazu kommen Migrationsbefehle, die ein Mensch ausdruecklich aufruft (`split-decisions`, `import-automemory`, `new`). Sie legen neue Dateien an und aendern keine bestehenden Inhalte. Einzige Ausnahme sind die Register, die zu Sichten werden. Deren Original liegt vorher byte-genau im Archiv.

Hooks sind durch diese Decision nicht erweitert. Fuer sie gilt weiter D-2026-09-30-02.

## Begruendung

Ein Index, der von Hand gepflegt wird, veraltet und erzeugt Merge-Konflikte. Ein generierter Index ist reproduzierbar. Kommt es doch zu einem Konflikt, loest ihn ein neuer Lauf von `python -m harness.mdmemory index` (dazu `merge=union` in `.gitattributes`).

Der Core feuert weiterhin nichts von selbst. Geschrieben wird nur, wenn ein Mensch, ein Skill oder CI den Befehl aufruft. Uebernimmt den Rest von D-2026-06-04-01 unveraendert.

## Belege

- `tests/test_mdmemory_notes.py`: zweiter Index-Lauf ohne Diff.
- `tests/test_governance_invariants.py`: C1 und C2 gruen.

## Verlauf

- 2026-09-30 · angelegt, ersetzt D-2026-06-04-01
- 2026-09-30 · abgeloest durch dec-2026-09-30-die-gedaechtnis-engine-kommt-per-adopt-66bd (veraendert)

---
id: dec-2026-09-30-04-atomare-notizen-unter-knowledge
type: decision
title: Atomare Notizen unter knowledge/<typ>/ sind kanonisch; Register und Indizes werden generiert
summary: Wissen, Decisions und Fragen leben als eine Notiz pro Datei; INDEX.md ist die fuenfte Boot-Datei
aliases: [D-2026-09-30-04]
status: active
valid_from: 2026-09-30
valid_until:
supersedes: []
superseded_by:
change:
confidence: bestaetigt
sources: [user:auftrag-2026-09-30-memory-phase-2, system:harness.mdmemory]
links: [D-2026-09-30-05, D-2026-09-30-01]
scope: project
sensitivity: normal
origin: internal
pinned: true
updated: 2026-09-30
last_confirmed: 2026-09-30
review_after: 2027-03-31
alternatives: [Register-Dateien bleiben kanonisch, Datenbank oder Vektorspeicher als Quelle]
reversibility: reversible
decided_by: user
---
## Entscheidung

Dauerhaftes Wissen liegt als eine Notiz pro Datei unter `knowledge/<typ>/<id>.md`. Die Typen sind `person`, `preference`, `project`, `decision`, `reference`, `concept` und `question`, das Schema v1 steht in `templates/knowledge-note.md`.

Kanonisch sind die Notizen. Diese Dateien werden daraus generiert und nie von Hand editiert:

- der Boot-Index `knowledge/INDEX.md` mit angehefteten und zuletzt geaenderten Notizen, gedeckelt auf 8 KB,
- die Unterindizes `knowledge/_typen/<typ>.md` mit hoechstens 50 Eintraegen je Teil,
- die Sichten `state/decisions.md`, `state/open-questions.md`, `state/assumptions.md` und `state/risks-and-constraints.md`.

`INDEX.md` ist die fuenfte Boot-Datei. Das Boot-Budget fuer AGENTS, CLAUDE, project-index, now und INDEX liegt bei hoechstens 5.000 Tokens (Ziel) und 12.000 Tokens (harte Grenze inklusive Worst Case). Ein CI-Test prueft beides.

`state/source-registry.md` und `state/artifact-index.md` bleiben Tabellen. Die frueheren Registerinhalte liegen byte-genau unter `archive/2026-09-30/state-*.md`. Die Alt-IDs `D-…`, `Q-…`, `A-…` und `R-…` bleiben als `aliases` gueltig.

Damit gilt nicht mehr, was im Kopf von `state/decisions.md` stand: „Kanonisch in v2 (keine Per-Decision-Files)“. Ausserdem wird `knowledge-graph-policy.md` §6 („Kein Parallel-State“) neu gefasst: Die Notizen sind der State, die Register sind nur noch Sichten darauf.

## Begruendung

Eine Datei pro Eintrag hat genau einen Schreiber. Zwei Sessions, die parallel je eine Decision anlegen, erzeugen deshalb keinen Merge-Konflikt. Frueher haengten beide an dieselbe Stelle von `decisions.md` an.

Der Index waechst nicht mit dem Bestand, weil er gedeckelt ist. Dadurch bleiben die Boot-Kosten fest, auch bei tausenden Notizen.

`supersedes` und `superseded_by` werden symmetrisch geprueft (`python -m harness.mdmemory lint`). Das ersetzt die Handpflege von Status und Verweisen in einer langen Datei.

## Belege

- Round-Trip-Test `tests/test_mdmemory_notes.py`: Register → Notizen → Register ohne Verlust.
- Migration: `python -m harness.mdmemory split-decisions` (idempotent), altes Vollformat per `export-legacy`.

## Verlauf

- 2026-09-30 · angelegt

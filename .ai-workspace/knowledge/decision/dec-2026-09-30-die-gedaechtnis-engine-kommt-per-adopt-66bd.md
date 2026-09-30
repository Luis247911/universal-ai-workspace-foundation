---
id: dec-2026-09-30-die-gedaechtnis-engine-kommt-per-adopt-66bd
type: decision
title: Die Gedaechtnis-Engine kommt per adopt als Kopie nach .claude/uaw/ ins Projekt
summary: adopt vendort harness.mdmemory nach .claude/uaw, verschmilzt Boot-Dateien per Block und migriert idempotent
aliases: [D-2026-09-30-10]
status: active
valid_from: 2026-09-30
valid_until:
supersedes: [dec-2026-09-30-05-skripte-unter-src-duerfen]
superseded_by:
change: veraendert
confidence: bestaetigt
sources: [user:auftrag-2026-09-30-memory-phase-5]
links: [D-2026-09-30-09, D-2026-09-30-04, D-2026-09-30-08]
scope: project
sensitivity: normal
origin: internal
pinned: true
updated: 2026-09-30
last_confirmed: 2026-09-30
review_after: 2027-03-31
alternatives: [pip install uaw-harness im Projekt-venv, ganzer Harness nach src/, keine Engine im Projekt]
reversibility: reversible
decided_by: user
---
## Entscheidung

Der Governance-Core `.ai-workspace/` bleibt markdown-only und ohne eigenen Motor; ausfuehrbarer Code lebt nur unter `.claude/` und `src/`. Die Invarianten C1 und C2 gelten unveraendert.

Abgeleitete Dateien in `.ai-workspace/` darf die Engine `harness.mdmemory` schreiben, nach den vier Regeln von D-2026-09-30-05: nur `.md`, deterministisch, Marke `GENERIERT`, jederzeit neu erzeugbar. Neu ist, **wo** die Engine liegen darf:

1. `src/harness/mdmemory/` (die Foundation selbst oder ein Projekt mit ganzem Harness),
2. **neu:** als Kopie unter `.claude/uaw/harness/mdmemory/` mit dem Aufruf `.claude/uaw/mdm.py`. Das ist ein Unter-Mount des Execution-Mounts `.claude/`, kein neuer Top-Level-Ordner. Nur Standardbibliothek, lauffaehig ab Python 3.9.

Ein Projekt bekommt die Engine ueber `adopt` (aus einem Klon der Foundation). `adopt` ergaenzt und verschmilzt nur:

- Vorhandene `AGENTS.md`/`CLAUDE.md` behalten ihren Inhalt und bekommen einen markierten Block (`<!-- uaw:begin -->`), den ein spaeterer Lauf ersetzt.
- `settings.json`, `automation.flags.json`, `.gitignore` und `.gitattributes` werden zusammengefuehrt, nie ersetzt.
- Migrationen laufen mit den bestehenden Befehlen (`now migrate`, `split-decisions`, optional `import-automemory`, `index`).
- Dateien, die die Foundation besitzt, stehen mit Pruefsumme in `.claude/uaw/manifest.json`; ein Upgrade ersetzt nur unveraenderte.
- Ein zweiter Lauf aendert nichts.

## Begruendung

Die Hooks importierten die Engine nur aus `<projekt>/src`. In einem Projekt ohne Harness waren sie still wirkungslos, und Index, `lint` und Migration mussten von Hand laufen. `pip install` hilft den Hooks nicht, weil sie mit dem System-Python starten, nicht mit dem venv des Projekts. Den ganzen Harness nach `src/` zu kopieren kollidiert mit fremden Layouts. Die Kopie unter `.claude/uaw/` laeuft offline mit jedem Python ab 3.9 und ist mit dem Projekt versioniert.

Ersetzt D-2026-09-30-05 und uebernimmt dessen Regeln vollstaendig. Hooks regelt D-2026-09-30-09.

## Belege

- `tests/test_autopilot_e2e.py`: Weg B mit fiktivem v3.2-Projekt: Trockenlauf ohne Aenderung, verlustfreie Migration, zweiter Lauf ohne Diff, Upgrade ersetzt nur unveraenderte Dateien, ganze Session auf der Kopie.
- `tests/test_governance_invariants.py`: C1 und C2 gruen.

## Verlauf

- 2026-09-30 · angelegt
- 2026-09-30 · ersetzt dec-2026-09-30-05-skripte-unter-src-duerfen (veraendert)

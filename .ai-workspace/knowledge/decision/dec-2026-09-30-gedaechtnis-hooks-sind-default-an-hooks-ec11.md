---
id: dec-2026-09-30-gedaechtnis-hooks-sind-default-an-hooks-ec11
type: decision
title: Gedaechtnis-Hooks default AN; Hooks duerfen einen Abschluss-Eintrag ins eigene Journal schreiben
summary: memory_boot, journal_stub und precompact_reminder laufen standardmaessig; alles andere bleibt opt-in
aliases: [D-2026-09-30-06]
status: superseded
valid_from: 2026-09-30
valid_until: 2026-09-30
supersedes: [dec-2026-09-30-02-schreib-doktrin-fuer-execution, dec-2026-09-30-03-die-automatik-schicht-unter]
superseded_by: dec-2026-09-30-hooks-halten-den-gedaechtnis-index-c464
change: veraendert
confidence: bestaetigt
sources: [user:auftrag-2026-09-30-memory-phase-3]
links: [D-2026-09-30-07, D-2026-06-06-01]
scope: project
sensitivity: normal
origin: internal
pinned: true
updated: 2026-09-30
last_confirmed: 2026-09-30
review_after:
alternatives: []
reversibility: reversible
decided_by: user
---
## Entscheidung

Die Automatik-Schicht unter `.claude/` bleibt grundsaetzlich opt-in und default AUS. Diese Hooks sind **default AN**:

- `first_run_onboarding`: einmaliger Erst-Start-Stups (D-2026-06-06-01).
- `now_init`: legt beim Start `state/now.md` an und haelt 4 KB ein.
- `memory_boot` (SessionStart): meldet nicht konsolidierte Journale und erinnert nach einem Compact. Liest nur.
- `journal_stub` (SessionEnd): schreibt einen Abschluss-Eintrag ins eigene Journal.
- `precompact_reminder` (PreCompact): zeigt dem User eine Erinnerung und blockiert nie.

Jeder Hook bleibt ueber `.claude/automation.flags.json` abschaltbar, ist reversibel und beruehrt `~/.claude/` nie.

Schreib-Doktrin fuer Hooks. Ein Hook darf:

- (a) seinen eigenen ephemeren, gitignored Lauf-Marker unter `.claude/` schreiben,
- (b) die gitignored `state/now.md` aus der Vorlage anlegen und auf 4 KB kuerzen,
- (c) den dabei entstehenden Ueberlauf ans Ende des eigenen Session-Journals anhaengen und die Datei dafuer anlegen,
- (d) **neu:** ans Ende des eigenen, bereits existierenden und nicht konsolidierten Session-Journals einen festen Abschluss-Eintrag (`uebergabe`) anhaengen. Der Eintrag enthaelt keine Inhalte der Arbeit und keine lokalen Pfade.

Verboten bleiben:

- bestehende Inhalte aendern,
- fremde oder konsolidierte Journale beschreiben,
- ein Journal nur fuer den Abschluss-Eintrag anlegen,
- Notizen, Decisions, generierte Indizes oder andere State-Dateien schreiben,
- `automation.flags.json` aendern.

## Begruendung

Ohne Erinnerung beim Start bleiben Journale unkonsolidiert, und Wissen landet nie in den Notizen. `memory_boot` liest nur und schweigt, wenn nichts offen ist.

`journal_stub` markiert das Session-Ende deterministisch in deutlich unter 1,5 s. Das ist das gemeinsame SessionEnd-Budget von Claude Code, bei Codex liegt es bei hoechstens 3 s.

PreCompact kann dem Modell keinen Kontext geben. Die Erinnerung geht deshalb an den User, und die fuer das Modell kommt nach dem Compact ueber `memory_boot`.

Ersetzt D-2026-09-30-02 (Schreib-Doktrin) und D-2026-09-30-03 (Defaults). Deren Inhalte sind hier vollstaendig uebernommen.

## Belege

- `tests/test_mdmemory_consolidate.py`: Hooks sind bei Flag aus wirkungslos, `journal_stub` legt nichts an, schont eingefrorene Journale und bleibt unter 1,5 s. `precompact_reminder` liefert nur `systemMessage`.

## Verlauf

- 2026-09-30 · angelegt
- 2026-09-30 · ersetzt dec-2026-09-30-02-schreib-doktrin-fuer-execution (veraendert)
- 2026-09-30 · ersetzt dec-2026-09-30-03-die-automatik-schicht-unter (veraendert)
- 2026-09-30 · abgeloest durch dec-2026-09-30-hooks-halten-den-gedaechtnis-index-c464 (veraendert)

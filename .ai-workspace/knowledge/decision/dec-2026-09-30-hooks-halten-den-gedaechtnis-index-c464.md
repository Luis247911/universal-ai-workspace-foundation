---
id: dec-2026-09-30-hooks-halten-den-gedaechtnis-index-c464
type: decision
title: Hooks halten den Gedaechtnis-Index aktuell und stupsen die woechentliche Pflege an
summary: index_refresh erneuert generierte Dateien nach Notiz-Aenderungen und beim Start; memory_boot erinnert an pflege
aliases: [D-2026-09-30-09]
status: active
valid_from: 2026-09-30
valid_until:
supersedes: [dec-2026-09-30-gedaechtnis-hooks-sind-default-an-hooks-ec11]
superseded_by:
change: veraendert
confidence: bestaetigt
sources: [user:auftrag-2026-09-30-memory-phase-5]
links: [D-2026-09-30-10, D-2026-09-30-07, D-2026-06-06-01]
scope: project
sensitivity: normal
origin: internal
pinned: true
updated: 2026-09-30
last_confirmed: 2026-09-30
review_after:
alternatives: [Modell ruft index selbst auf, nur CI prueft den Index]
reversibility: reversible
decided_by: user
---
## Entscheidung

Die Automatik-Schicht unter `.claude/` bleibt grundsaetzlich opt-in und default AUS. Diese Hooks sind **default AN**:

- `first_run_onboarding`: einmaliger Erst-Start-Stups (D-2026-06-06-01).
- `now_init`: legt beim Start `state/now.md` an, haelt 4 KB ein und nennt den Befehl fuer Journal-Eintraege.
- `index_refresh` (**neu**; PostToolUse auf Notizen, SessionStart startup/resume): erneuert die generierten Dateien, sobald sich eine Notiz aendert oder der Index nach `git pull`/Merge veraltet ist.
- `memory_boot` (SessionStart): meldet abgeschlossene, nicht konsolidierte Journale, erinnert nach einem Compact und **neu** beim Start an den Skill `pflege`, wenn der letzte Bericht aelter als 7 Tage ist (hoechstens einmal pro Tag).
- `journal_stub` (SessionEnd): schreibt einmal einen Abschluss-Eintrag ins eigene Journal.
- `precompact_reminder` (PreCompact): zeigt dem User eine Erinnerung und blockiert nie.

Jeder Hook bleibt ueber `.claude/automation.flags.json` abschaltbar, ist reversibel und beruehrt `~/.claude/` nie. Gestartet werden die Hooks ueber den Launcher `.claude/hooks/run.sh`, der `python3` oder `python` (ab 3.9) waehlt.

Schreib-Doktrin fuer Hooks. Ein Hook darf:

- (a) seinen eigenen ephemeren, gitignored Lauf-Marker unter `.claude/` schreiben,
- (b) die gitignored `state/now.md` aus der Vorlage anlegen und auf 4 KB kuerzen,
- (c) den dabei entstehenden Ueberlauf ans Ende des eigenen Session-Journals anhaengen und die Datei dafuer anlegen,
- (d) ans Ende des eigenen, bereits existierenden und nicht konsolidierten Session-Journals einmal einen festen Abschluss-Eintrag (`uebergabe`) anhaengen, ohne Inhalte der Arbeit und ohne lokale Pfade,
- (e) **neu:** die als GENERIERT markierten Dateien nach D-2026-09-30-05 neu erzeugen (`knowledge/INDEX.md`, `knowledge/_typen/`, Register-Sichten). Nur `index_refresh`, nur mit denselben Regeln wie `harness.mdmemory index`.

Verboten bleiben:

- bestehende Inhalte aendern,
- fremde oder konsolidierte Journale beschreiben,
- ein Journal nur fuer den Abschluss-Eintrag anlegen,
- Notizen, Decisions oder andere State-Dateien schreiben,
- `automation.flags.json` aendern.

## Begruendung

Bisher hingen `index`, das Anlegen des Journals und die Pflege am Gedaechtnis des Modells. Ein vergessenes `index` laesst den Boot-Index veralten, und `lint` schlaegt erst in CI oder gar nicht an. Der Hook macht das deterministisch; er schreibt nur Dateien, die sich jederzeit aus den Notizen neu erzeugen lassen. Gemessen bei 600 Notizen: unter 0,1 s pro Lauf.

Nach einem Merge mit `merge=union` sind die generierten Dateien absichtlich inkonsistent; der Start-Lauf heilt das, bevor das Modell den Index liest.

Ersetzt D-2026-09-30-06 und uebernimmt dessen Inhalte vollstaendig.

## Belege

- `tests/test_autopilot_e2e.py`: ganze Session ueber `run.sh` (Weg A und B), Index nach Notiz-Aenderung aktuell, `lint` gruen.
- `tests/test_mdmemory_consolidate.py`, `tests/test_mdmemory_consolidate_edgecases.py`: Hooks bei Flag aus wirkungslos, `journal_stub` einmal und unter 1,5 s.

## Verlauf

- 2026-09-30 · angelegt
- 2026-09-30 · ersetzt dec-2026-09-30-gedaechtnis-hooks-sind-default-an-hooks-ec11 (veraendert)

# session-contract.md — Session-Lifecycle

Definiert Start, Work, Handoff, Resume einer Arbeitssession auf dieser Foundation.

## 1. Session-Start

Beim Start einer Session:

1. Lies die vier Boot-Dateien in der vorgegebenen Reihenfolge: `AGENTS.md`, `CLAUDE.md` (falls Tool=Claude), `state/project-index.md`, `state/current-session.md`.
2. Fuehre den Reboot-Test mental durch (Section 2).
3. Pruefe `state/current-session.md` auf "Open Handoffs". Falls vorhanden: erst entscheiden, ob diese fortgesetzt werden oder zurueckgestellt.
4. Pruefe `state/open-questions.md` und `state/decisions.md` auf relevante Eintraege.
5. Beginne erst danach mit produktiver Arbeit.

## 2. Reboot-Test (5 Fragen)

`state/current-session.md` muss diese fuenf Fragen beantworten. Bei Resume oder Handoff werden sie aktiv geprueft. Wenn die Datei sie nicht beantwortet, muss sie zuerst aktualisiert werden.

1. **Wo bin ich?** (Projekt, aktiver Task, derzeitiger Bearbeitungsstand.)
2. **Was ist das Ziel?** (Konkrete Output-Erwartung der laufenden Arbeit.)
3. **Was hat sich geaendert?** (Was wurde seit dem letzten Update getan oder entschieden.)
4. **Was bleibt offen?** (Naechste Schritte, offene Fragen, blockierende Punkte.)
5. **Welche Evidenz?** (Worauf stuetzen sich die juengsten Aussagen — Quellen, Decisions, Artefakte.)

## 3. `state/current-session.md` Update-Regeln

Pflicht-Updates an `current-session.md`:

- **Vor `/compact`** (oder vergleichbare Compaction-Aktion in einem anderen Tool).
- **Vor Handoff** an eine andere Session, eine andere Person oder eine spaetere Wiederaufnahme.
- **Vor Task-Wechsel** (alter Active Task abgeschlossen oder pausiert, neuer Active Task uebernommen).
- **Nach jeder groesseren Aktion**, die das Verstaendnis des Zustands aendert (neue Decision, neuer Risk, abgeschlossenes Artefakt, neuer Source-Eintrag).

Update-Inhalte:

- Last-Update-Timestamp.
- Active-Task-String aktualisiert.
- Status (`in_progress` / `blocked` / `waiting_for_user` / `paused` / `done`) korrekt.
- Reboot-Test-Antworten aktualisiert.
- Recent-Actions-Liste (max. 10 Eintraege; aeltere via Cleanup gepruned).
- Resume-Notes geschrieben — was muss eine neue Session zuerst tun.
- Offene Handoffs notiert.
- Pointer auf relevante `decisions.md`/`open-questions.md`/`knowledge/<topic>/_moc.md` aktualisiert.

## 4. Handoff-Procedure

Wenn eine Session bewusst beendet wird mit der Erwartung, dass eine spaetere Session uebernimmt:

1. `current-session.md` vollstaendig aktualisieren (Reboot-Test, Resume-Notes, Open Handoffs).
2. Optional ein `templates/handoff.md`-Dokument als zusaetzliches Briefing schreiben, falls die Uebergabe komplex ist (z.B. an eine andere Person oder an eine separate Tool-Instanz). Speicherort: `archive/YYYY-MM-DD-handoff-<slug>.md` oder `scratch/handoff-<slug>.md`, je nach Persistenzbedarf.
3. Eintrag in `state/artifact-index.md`, falls ein dauerhafter Handoff-Artikel entsteht.

## 5. Resume-Procedure

Wenn eine Session resumed wird:

1. Boot-Order durchgehen.
2. Reboot-Test gegen `current-session.md` mental beantworten.
3. `state/decisions.md` und `state/open-questions.md` auf relevante neue Eintraege scannen (besonders, wenn andere Sessions zwischenzeitlich aktiv waren).
4. Falls Open Handoffs in `current-session.md`: explizit entscheiden, was zu tun ist.
5. Falls `current-session.md` aelter als 7 Tage und kein Handoff dokumentiert: Stale-Session-Detection (Section 6) ausloesen.

## 6. Stale-Session-Detection

Wenn `current-session.md` Last-Update-Timestamp aelter als 7 Tage ist und keine explizite Pause oder Handoff-Notiz enthaelt:

- Pruefen, ob die dokumentierten Aussagen noch valide sind.
- Pruefen, ob zwischen-Aktionen ausserhalb der Foundation passiert sind, die jetzt nachgepflegt werden muessten.
- `state/decisions.md` und `state/open-questions.md` auf Aenderungen pruefen.
- Vor neuer produktiver Arbeit: `current-session.md` aktualisieren oder explizit als "stale, will be reset" markieren.
- Falls drastische Reset noetig: `current-session.md` aus `templates/session-state.md` neu initialisieren; alte Inhalte als Handoff-Snapshot nach `archive/YYYY-MM-DD-session-snapshot-<slug>.md` archivieren (manuell, nicht automatisch).

## Cross-Links

- Behavior-Datei: `protocol.md`.
- Live-Zustand: `state/current-session.md`.
- Templates: `templates/session-state.md`, `templates/handoff.md`.
- Lifecycle: `file-lifecycle.md`.

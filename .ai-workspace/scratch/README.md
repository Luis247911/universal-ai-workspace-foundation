# scratch/ — Ephemere, untrusted Arbeit

Dieses Verzeichnis enthaelt alles Ephemerische und Untrusted: Notizen, Drafts, Tool-Outputs, Maintenance-Routine-Outputs (Default-Pfad `scratch/maintenance/<datum>-<routine>.md`), explorative Skizzen.

## Was hierher gehoert

- Alles, was nicht laenger als noetig leben muss.
- Drafts vor Promotion nach `research/` oder `deliverables/`.
- Tool-Outputs vor Verifikation.
- Maintenance-Routine-Outputs.
- Explorative Markdown-Skizzen.

## Was hierher NICHT gehoert

- State-relevante Inhalte (gehoeren in `state/`).
- Verifizierte Inhalte (gehoeren in `research/`, `deliverables/` oder `knowledge/`).
- Sensible operative Daten (siehe `security-policy.md` Section 11).
- Originalbinaerdateien (extern oder im Project Data Space).

## Retention-Default

7 Tage. Nach 7 Tagen: im naechsten Cleanup-Review (`templates/cleanup-review.md` Sektion 1) Pro Eintrag entscheiden: `keep` / `archive` / `delete`. Kein automatisches Loeschen — alle Cleanup-Aktionen sind durch Hauptsession verifizierte Aktionen.

## Lade-Regel

`Never Auto-Load`. Inhalte unter `scratch/` werden nur auf explizite Anfrage geladen. Maintenance-Routinen schreiben dorthin als Default-Output, mutieren aber niemals durable State.

## Promote nach

- `scratch/` -> `research/`: bei "potentiell wertvoll" (Quality-Gate).
- `scratch/` -> `deliverables/`: bei direkt kuratierter Form (selten — meist Umweg ueber `research/`).

## Trust-Level

Default `untrusted, ephemer`. Inhalte gelten nicht als Beleg fuer Decisions oder Knowledge-Notes, ohne explizite Promotion.

## Cross-Links

- Lifecycle: `../file-lifecycle.md`.
- Quality-Gates: `../quality-gates.md`.
- Cleanup-Review-Template: `../templates/cleanup-review.md`.

---
id: current-session
type: current-session
title: "Live-Zustand"
status: active
created: <YYYY-MM-DD>
updated: <YYYY-MM-DD>
owner: <user>
---

# Current Session

Live-Zustand. Diese Datei ist eine der vier Boot-Dateien. Sie wird **vor `/compact`, vor Handoff, vor Task-Wechsel und nach jeder groesseren Aktion** aktualisiert.

## 1. Last Update

`<YYYY-MM-DD HH:MM>`

## 2. Active Task

`<1-satz-beschreibung-der-aktuellen-aufgabe>`

## 3. Status

`<in_progress / blocked / waiting_for_user / paused / done>`

## 4. Reboot-Test-Antworten

Diese fuenf Fragen werden bei jedem Resume aktiv geprueft. Wenn die Antworten leer oder veraltet sind, muss diese Datei zuerst aktualisiert werden.

- **Wo bin ich?** `<projekt + aktiver task + bearbeitungsstand>`
- **Was ist das Ziel?** `<konkrete output-erwartung>`
- **Was hat sich geaendert?** `<was wurde seit letztem update getan oder entschieden>`
- **Was bleibt offen?** `<naechste schritte / blocker>`
- **Welche Evidenz?** `<quellen / decisions / artefakte>`

## 5. Recent Actions (max 10)

Append-only-Liste; aeltere Eintraege werden bei Update gepruned und ggf. in `archive/YYYY-MM-DD-session-snapshot-<slug>.md` archiviert.

(noch keine)

## 6. Resume Notes

Was muss eine neue Session zuerst tun, um produktiv weiterzuarbeiten?

`<text>`

## 7. Open Handoffs

Was wurde an wen oder welche Tool-Instanz delegiert? Erwartete Rueckmeldung?

(noch keine)

## 8. Pointer auf relevante State-/KG-Eintraege

- Decisions: `<liste der aktuell relevanten D-IDs>`
- Open Questions: `<liste der aktuell relevanten Q-IDs>`
- Risks: `<liste der aktuell relevanten R-IDs>`
- Knowledge: `<liste der aktuell relevanten knowledge/<topic>/_moc.md oder knowledge/<topic>/<slug>.md>`

## Cross-Links

- Identitaet: `project-index.md`.
- Decisions: `decisions.md`.
- Open Questions: `open-questions.md`.
- Artifacts: `artifact-index.md`.
- Session-Lifecycle-Regeln: `../session-contract.md`.
- Handoff-Template: `../templates/handoff.md`.

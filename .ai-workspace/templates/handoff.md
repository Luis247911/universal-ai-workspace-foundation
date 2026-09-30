---
id: <handoff-slug>
type: handoff
title: "Session-Handoff"
status: draft
created: <YYYY-MM-DD>
updated: <YYYY-MM-DD>
owner: <user>
related: []
verification_status: unverified
---

# Handoff

Vorlage fuer einen ausfuehrlichen Session-Handoff. Wird genutzt, wenn die Uebergabe komplexer ist, als `state/now.md` und das Session-Journal allein leisten koennen (z.B. an eine andere Person, eine andere Tool-Instanz, eine spaetere Wiederaufnahme nach laengerer Pause).

## Aktueller Task

`<beschreibung>`

## Status

`<in_progress / blocked / waiting_for_user / paused>`

## Was wurde getan

Liste der wesentlichen Aktionen seit Session-Start oder letztem Handoff.

## Was steht an

Liste der naechsten Schritte, in priorisierter Reihenfolge.

## Open Questions

Verweis auf relevante Fragen (Notizen unter `knowledge/question/`, `kind: question`; alte `Q-IDs` gelten als Alias). Sicht: `state/open-questions.md` (generiert).

## Open Risks

Verweis auf relevante Risiken (Notizen unter `knowledge/question/`, `kind: risk`/`constraint`; alte `R-IDs` gelten als Alias). Sicht: `state/risks-and-constraints.md` (generiert).

## Resume-Anweisungen

Was muss eine neue Session zuerst tun? Welche Dateien zuerst lesen? Welche Decisions oder Assumptions sind besonders relevant?

## Wichtige Dateien als Pointer

- `<pfad-1>` — `<warum relevant>`
- `<pfad-2>` — `<warum relevant>`

## Ungeprueftes / Unsicheres

Was wurde noch nicht verifiziert? Welche Aussagen sollten skeptisch betrachtet werden?

## Cross-Links

- Live-Zustand: `../state/now.md` (lokal). Historie: `../journal/`.
- Session-Lifecycle: `../session-contract.md`.
- Lifecycle: `../file-lifecycle.md`.

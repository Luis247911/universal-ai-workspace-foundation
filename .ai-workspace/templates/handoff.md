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

Vorlage fuer einen ausfuehrlichen Session-Handoff. Wird genutzt, wenn die Uebergabe komplexer ist, als `state/current-session.md` allein leisten kann (z.B. an eine andere Person, eine andere Tool-Instanz, eine spaetere Wiederaufnahme nach laengerer Pause).

## Aktueller Task

`<beschreibung>`

## Status

`<in_progress / blocked / waiting_for_user / paused>`

## Was wurde getan

Liste der wesentlichen Aktionen seit Session-Start oder letztem Handoff.

## Was steht an

Liste der naechsten Schritte, in priorisierter Reihenfolge.

## Open Questions

Verweis auf relevante `Q-IDs` in `state/open-questions.md`.

## Open Risks

Verweis auf relevante `R-IDs` in `state/risks-and-constraints.md`.

## Resume-Anweisungen

Was muss eine neue Session zuerst tun? Welche Dateien zuerst lesen? Welche Decisions oder Assumptions sind besonders relevant?

## Wichtige Dateien als Pointer

- `<pfad-1>` — `<warum relevant>`
- `<pfad-2>` — `<warum relevant>`

## Ungeprueftes / Unsicheres

Was wurde noch nicht verifiziert? Welche Aussagen sollten skeptisch betrachtet werden?

## Cross-Links

- Live-Zustand: `../state/current-session.md`.
- Session-Lifecycle: `../session-contract.md`.
- Lifecycle: `../file-lifecycle.md`.

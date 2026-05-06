---
id: <D-YYYY-MM-DD-NN>
type: decision-record
title: "<entscheidung in 1 satz>"
status: active
created: <YYYY-MM-DD>
updated: <YYYY-MM-DD>
owner: <user>
verification_status: unverified
---

# Decision Record

Vorlage fuer einen einzelnen Decision-Eintrag, bereit fuer Append in `state/decisions.md`. Per-Decision-Files sind in v2 nicht Pflicht — die kanonische Quelle ist `state/decisions.md`. Dieses Template kann genutzt werden, wenn ein Adapter Per-Decision-Files einbringt.

## ID-Vorschlag

`D-YYYY-MM-DD-NN`

## Datum

`<YYYY-MM-DD>`

## Entscheidung

`<1 satz>`

## Begruendung

`<1-3 saetze>`

## Verworfene Alternativen

- `<alternative-1>` — verworfen weil `<grund>`
- `<alternative-2>` — verworfen weil `<grund>`

## Reversibilitaet

`<reversible / hard-to-reverse / irreversible>`

## Follow-up

- **Follow-up-Date:** `<YYYY-MM-DD oder leer>`
- **Verantwortlich:** `<wer>`
- **Naechste Aktion:** `<was>`

## Cross-Links

- Decisions-Log: `../state/decisions.md`.
- Annahmen: `../state/assumptions.md`.
- Open Questions: `../state/open-questions.md`.

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

Denkhilfe fuer eine Entscheidung. Seit v3.3 ist jede Decision eine eigene Notiz unter `knowledge/decision/` (D-2026-09-30-04); `state/decisions.md` ist nur noch eine generierte Sicht. Anlegen: `python -m harness.mdmemory new decision "<titel>"`, die Abschnitte unten in den Koerper der Notiz uebernehmen (Alternativen ins Feld `alternatives`, Reversibilitaet ins Feld `reversibility`, Follow-up-Date ins Feld `review_after`), danach `python -m harness.mdmemory index`. Eine Decision, die eine fruehere ersetzt, setzt `supersedes`; die alte bekommt `superseded_by` und `status: superseded`.

## ID-Vorschlag

Notiz-ID `dec-YYYY-MM-DD-<slug>-<4hex>` (vergibt `new`); optionaler Alias `D-YYYY-MM-DD-NN` (`--alias auto`).

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

- Schema: `knowledge-note.md` (Typ `decision`).
- Decision-Notizen: `../knowledge/decision/`, Sicht `../state/decisions.md` (generiert).
- Annahmen und offene Fragen: `../knowledge/question/`, Sichten `../state/assumptions.md`, `../state/open-questions.md`.

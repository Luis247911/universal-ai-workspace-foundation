---
id: <source-note-slug>
type: source-note
title: "<titel>"
status: draft
created: <YYYY-MM-DD>
updated: <YYYY-MM-DD>
owner: <user-or-adapter>
source-id: <source-id-aus-source-registry>
uri: <uri-or-pointer>
fetched_date: <YYYY-MM-DD>
trust_level: external
hash_optional: <optional sha256, sonst leer>
related: []
kg_linked: no
lifecycle: research
verification_status: unverified
---

# Source Note

Vorlage fuer eine Source-Notiz in `research/<source-id>-<datum>.md`. **Nicht** die Tabellenzeile in `state/source-registry.md` — die bleibt dort. Diese Datei ist die paraphrasierte Markdown-Version mit Verlaesslichkeits-Einschaetzung.

## Zusammenfassung

`<3-5 saetze paraphrasiert>`

## Relevante Auszuege

Paraphrasiert. Woertliche Zitate nur, wenn fuer kritische Aussagen unverzichtbar; dann mit Markierung als Zitat und Quellenangabe.

## Verlaesslichkeits-Einschaetzung

- Autor / Herausgeber: `<wer>`
- Datum / Aktualitaet: `<wann>`
- Methodik / Begruendung: `<wie>`
- Bekannte Schwaechen: `<was>`

## Moegliche Bias

`<welche perspektive, welcher blick fehlt>`

## KG-Linkage

Pflichtsektion (auch wenn leer):

- Verwandte Knowledge-Notes: `[[<wiki-link>]]`
- Verwandte MOCs: `[[<moc-link>]]`
- Verwandte Decisions: `[[D-YYYY-MM-DD-NN]]`

## Cross-Links

- Source-Registry: `../state/source-registry.md`.
- Source-Policy: `../source-policy.md`.
- Quality-Gates: `../quality-gates.md`.

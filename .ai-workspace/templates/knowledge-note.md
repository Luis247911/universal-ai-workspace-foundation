---
id: <knowledge-note-slug>
type: knowledge-note
title: "<titel>"
status: draft
created: <YYYY-MM-DD>
updated: <YYYY-MM-DD>
owner: <user-or-adapter>
source_ids: []
trust_level: external
lifecycle: knowledge
related: []
review_after: <YYYY-MM-DD>
link_validity: ok
freshness: <YYYY-MM-DD>
verification_status: unverified
---

# Knowledge Note

Vorlage fuer eine Knowledge-Note im Markdown-Knowledge-Graph. Lebt unter `knowledge/<topic>/<slug>.md`. Verbunden ueber `[[wiki-links]]`.

## 1. Summary

3-5 Saetze: Was ist diese Note? Warum wichtig?

## 2. Key Facts

Bullet-Liste. Jeder Fakt mit Source-ID-Verweis.

- `<fakt-1>` (Quelle: `<source-id>`)
- `<fakt-2>` (Quelle: `<source-id>`)

## 3. Relationships

Wie haengt diese Note mit anderen zusammen? Mit semantischem Beziehungs-Kontext, nicht nur Linkliste.

- Ergaenzt: `[[<note-1>]]` — `<warum>`
- Steht im Kontrast zu: `[[<note-2>]]` — `<wie>`
- Wird ergaenzt durch: `[[<note-3>]]` — `<wodurch>`

## 4. Open Questions

Verweis auf `Q-IDs` aus `state/open-questions.md`.

- `[[Q-YYYY-MM-DD-NN]]` — `<frage>`

## 5. Evidence

Pointer auf research-reports, source-notes, decisions, externe Quellen.

- `[[<research-report-slug>]]`
- `[[<source-note-slug>]]`
- `[[D-YYYY-MM-DD-NN]]`

## 6. Backlinks to Maintain

Welche anderen Notes oder MOCs sollten auf diese Note zeigen, falls sie wichtig wird? Manueller Hinweis fuer Maintenance.

## 7. Review-After

`<YYYY-MM-DD>` — wann diese Note wieder geprueft werden soll.

## Cross-Links

- KG-Policy: `../knowledge-graph-policy.md`.
- MOC-Template: `moc.md`.
- Source-Note-Template: `source-note.md`.
- Quality-Gates: `../quality-gates.md`.

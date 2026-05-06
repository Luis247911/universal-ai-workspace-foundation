---
id: <research-id>
type: research-report
title: "<titel>"
status: draft
created: <YYYY-MM-DD>
updated: <YYYY-MM-DD>
owner: <user-or-adapter>
research_date: <YYYY-MM-DD>
related_source_ids: []
related_question_ids: []
related: []
trust_level: external
lifecycle: research
verification_status: unverified
review_after: <YYYY-MM-DD>
---

# Research Report

Vorlage fuer ein Research-Artefakt in `research/`. Inhalt darf inline aus mehreren Quellen synthetisieren, muss aber jede Aussage einer Quelle (oder einer eigenen Begruendung) zuordnen.

## Frage

`<welche frage wird mit diesem report beantwortet>`

## Methodik

`<wie wurden die quellen erschlossen, ausgewaehlt, gewichtet>`

## Findings

Bullet-Liste oder Subsektionen. Pro Finding:
- Aussage
- Quelle (`source-id`)
- Confidence (`high` / `medium` / `low`)

## Confidence

Globale Confidence-Einschaetzung des Reports.

## Open Sub-Questions

Verweis auf neue oder verbleibende `Q-IDs` in `state/open-questions.md`.

## Stale-Risk

Wann verlieren die Aussagen Geltung? Quellen-Aktualitaet? Aenderbarkeit?

## Pointer zu Sources

Liste der `source-id`s aus `state/source-registry.md`, die diesen Report stuetzen.

## KG-Linkage

Liste der `[[wiki-links]]` zu Knowledge-Notes oder MOCs, die diesen Report einordnen oder ergaenzen. Pflichtsektion (auch wenn leer).

## Promotion-Hinweis

Wenn die Findings stabilisiert sind: Empfehlung in welche `knowledge/<topic>/<slug>.md` sie ueberfuehrt werden koennten, und welcher MOC aktualisiert werden sollte.

## Cross-Links

- Source-Registry: `../state/source-registry.md`.
- Source-Note-Template: `source-note.md`.
- Quality-Gates: `../quality-gates.md`.
- KG-Policy: `../knowledge-graph-policy.md`.

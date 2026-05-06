---
id: <ingestion-record-slug>
type: ingestion-record
title: "Ingestion-Record fuer <input-id>"
status: draft
created: <YYYY-MM-DD>
updated: <YYYY-MM-DD>
owner: <user-or-adapter>
input_id: <input-id>
input_type: <pdf / docx / pptx / xlsx / image / audio / video / other>
original_location: <pfad-oder-uri-oder-extern>
source_registry_id: <source-id-aus-source-registry>
received_date: <YYYY-MM-DD>
sensitivity: <low / medium / high>
allowed_processing: <manual / automated-with-approval / none>
extraction_method: <manual-summary / OCR / parser-tool / not-extracted>
extraction_status: <pending / in_progress / done / skipped / failed>
markdown_outputs: []
graph_links_created: []
do_not_load_rules: []
verification_status: unverified
cleanup_or_retention: "<beschreibung>"
review_date: <YYYY-MM-DD>
---

# Ingestion Record

Pro Ingestion-Vorgang ein Eintrag. Dokumentiert, wie eine Binaerdatei in Markdown ueberfuehrt wurde.

## 1. Notes

`<besonderheiten der ingestion: schwer zu lesen, sensible inhalte gefiltert, format-probleme, etc.>`

## 2. Skipped Sections

`<welche teile des originals wurden bewusst nicht in markdown uebernommen; mit begruendung>`

## 3. Open Issues

Verweis auf `Q-IDs` in `state/open-questions.md`.

- `[[Q-YYYY-MM-DD-NN]]` — `<frage>`

## Cross-Links

- Source-Policy: `../source-policy.md`.
- Lifecycle: `../file-lifecycle.md`.
- Data-Space-Template: `data-space.md`.
- Source-Registry: `../state/source-registry.md`.
- Normalized-Document-Template: `normalized-document.md`.
- Normalization-Review-Template: `normalization-review.md`.

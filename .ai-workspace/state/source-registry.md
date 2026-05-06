---
id: source-registry
type: source-registry
title: "Externe Quellen — Registry"
status: active
created: <YYYY-MM-DD>
updated: <YYYY-MM-DD>
owner: <user>
---

# Source Registry

Registry aller externen Quellen. **Kanonisch in v2** (keine Per-Source-Files). Jede Quelle, die in Foundation-Dateien zitiert oder referenziert wird, hat hier einen Eintrag.

## Pflichtfelder pro Eintrag

| Feld | Bedeutung |
|------|-----------|
| `source-id` | Eindeutiger Slug (kebab-case). |
| `type` | `url` / `binary` / `data-space`. |
| `uri-or-pointer` | URL, Dateipfad oder externer Pointer. |
| `first-fetched-date` | `YYYY-MM-DD`. |
| `last-checked-date` | `YYYY-MM-DD`. |
| `trust-level` | `trusted` / `external` / `hostile`. |
| `summary-pointer` | Pfad zu `research/<source-id>-<datum>.md`. |
| `hash-optional` | SHA-256 hex-lowercase, leer wenn keiner. |
| `kg_linked` | `yes` / `no`. |
| `do_not_load` | `yes` / `no` (Default `no`). |
| `sensitivity` | `low` / `medium` / `high` (Pflicht bei `type: binary`). |
| `original_location` | Externer Speicherort (fuer `binary` und `data-space`). |
| `extraction_method` | `manual-summary` / `OCR` / `parser-tool` / `not-extracted` (fuer `binary`). |
| `normalized_markdown_path` | Pfad zu `templates/normalized-document.md`-Instanz (fuer `binary`). |
| `normalization_review_path` | Pfad zu `templates/normalization-review.md`-Instanz (fuer `binary`). |
| `normalization_status` | `none` / `draft` / `reviewed` / `verified` / `rejected` (fuer `binary`). |
| `verification_status` | `unverified` / `partially_verified` / `verified` / `do_not_use` (fuer `binary`). |
| `original_retained` | `yes` / `no` (fuer `binary`). |
| `critical_claims_require_original_check` | `yes` / `no` (fuer `binary`). |
| `notes` | Freitext, kurz. |

## Eintraege

Tabellarische Form (eine Zeile pro Quelle). Bei groesseren Inventaren in `notes` einen Bezug auf eine `research/<source-id>-<datum>.md` setzen statt Inhalt inline.

| source-id | type | uri-or-pointer | first-fetched | last-checked | trust-level | summary-pointer | hash-optional | kg_linked | do_not_load | sensitivity | original_location | extraction_method | normalized_markdown_path | normalization_review_path | normalization_status | verification_status | original_retained | critical_claims_require_original_check | notes |
|-----------|------|----------------|---------------|--------------|-------------|-----------------|---------------|-----------|-------------|-------------|-------------------|-------------------|--------------------------|---------------------------|----------------------|---------------------|-------------------|----------------------------------------|-------|
| (noch keine) | | | | | | | | | | | | | | | | | | | |

## Cross-Links

- Source-Policy: `../source-policy.md`.
- Sicherheit (Sensitivity, `do_not_load`): `../security-policy.md`.
- Document-Normalization: `../knowledge-graph-policy.md`.
- Templates: `../templates/data-space.md`, `../templates/ingestion-record.md`, `../templates/normalized-document.md`, `../templates/normalization-review.md`, `../templates/source-note.md`, `../templates/research-report.md`.

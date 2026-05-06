---
id: <cleanup-review-slug>
type: cleanup
title: "Cleanup Review <YYYY-MM-DD>"
status: draft
created: <YYYY-MM-DD>
updated: <YYYY-MM-DD>
owner: <user>
verification_status: unverified
---

# Cleanup Review

Vorlage fuer die periodische Cleanup-Review (Default alle 30 Tage; per Adapter ueberschreibbar). Output-Datei landet in `scratch/maintenance/<datum>-cleanup-review.md` oder durch Hauptsession-Promote in `archive/YYYY-MM-DD-cleanup-review-<slug>.md`.

## Datum

`<YYYY-MM-DD>`

## Reviewer

`<user oder adapter-slug>`

## 1. Scratch-Aging-Liste

Dateien in `scratch/` aelter als 7 Tage. Pro Eintrag: Pfad, Alter, Empfehlung (`keep` / `archive` / `delete`).

(noch keine)

## 2. Research-90-Tage-Trigger-Liste

Dateien in `research/` aelter als 90 Tage. Pro Eintrag: Pfad, Alter, Empfehlung (`promote` / `archive` / `keep` / `re-verify`).

(noch keine)

## 3. Stale-Sources-Liste

Eintraege in `state/source-registry.md` mit `last-checked > 365 Tage`. Pro Eintrag: source-id, Letztes Datum, Empfehlung.

(noch keine)

## 4. Verwaiste Pointer

Pointer in State-Dateien oder Knowledge-Notes, deren Ziel nicht mehr existiert. Pro Eintrag: Pointer, Quell-Datei, Empfehlung.

(noch keine)

## 5. KG-Lint-Findings

- **Tote `[[wiki-links]]`:** `<liste>` — Empfehlung pro Link.
- **`status: planned`-Links ohne Stub:** `<liste>` — Empfehlung.
- **Verwaiste Knowledge-Notes** (keine eingehenden Links + kein MOC-Eintrag): `<liste>`.
- **Knowledge-Notes mit `updated > 180 Tage`** ohne Maintenance-Touch: `<liste>`.

## 6. MOC-Drift

- **MOCs ohne neue Eintraege > 90 Tage:** `<liste>`.
- **Topic-MOCs mit > 50 Eintraegen** (Subdivision-Vorschlag): `<liste>`.

## 7. Source-Registry-Hygiene

- **Sources ohne `kg_linked`-Status, obwohl Markdown-Derivat existiert:** `<liste>`.
- **Sources mit `last-checked > 365 Tage`:** `<liste>`.
- **Binary-Sources ohne `extraction_method`:** `<liste>`.
- **Binary-Sources ohne `normalization_status` oder `verification_status`:** `<liste>`.

## 8. Data-Space-Drift

- **Data-Spaces ohne neue Eintraege > 180 Tage:** `<liste>`.
- **Data-Spaces mit fehlenden `do_not_load`-Markierungen** auf sensiblen Inhalten: `<liste>`.

## 9. Maintenance-Routine-Status

- **Registrierte Routines mit `last_reviewed > 90 Tage`:** `<liste>`.
- **Routine-Outputs noch nicht in durable State integriert:** `<liste>`.

## 10. Document-Normalization-Drift

- **Sources `type: binary` ohne Normalized-Markdown:** `<liste>`.
- **Normalized-Markdown ohne Normalization-Review:** `<liste>`.
- **Normalized-Markdown mit `verification_status: do_not_use`** und trotzdem referenziert: `<liste>` (kritisch — sofortige Korrektur).
- **Normalized-Markdown mit `partially_verified` und keinen markierten unsicheren Stellen:** `<liste>`.

## 11. Vorgeschlagene Aktionen

Pro Item aus den Sektionen oben: `archive` / `delete` / `keep` / `update` / `verify` + Begruendung.

## 12. Cross-Links

- Lifecycle: `../file-lifecycle.md`.
- Artifact-Index: `../state/artifact-index.md`.
- KG-Policy: `../knowledge-graph-policy.md`.
- Source-Policy: `../source-policy.md`.

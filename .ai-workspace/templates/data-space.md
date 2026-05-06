---
id: <data-space-slug>
type: data-space
title: "<data-space-titel>"
status: active
created: <YYYY-MM-DD>
updated: <YYYY-MM-DD>
owner: <user-or-adapter>
sensitivity: <low / medium / high>
allowed_processing: <manual / automated-with-approval / none>
retention_policy: "<beschreibung>"
source_registry_id: <source-id-aus-source-registry>
---

# Data Space Manifest: `<data-space-titel>`

Manifest fuer einen Project Data Space. **Diese Datei enthaelt nur Metadaten und Pointer.** Die Originaldaten leben extern (auf Netzwerklaufwerk, Cloud-Storage, externem Speicherort) oder im projektspezifisch deklarierten Speicherort — **niemals im Foundation-Tree selbst**.

## 1. Description

`<was enthaelt dieser data space; welche art von daten>`

## 2. Location

`<pfad oder uri zum externen speicherort; bei sensitivity=high keine konkrete location, nur abstrakter hinweis>`

## 3. Allowed Users

`<wer darf darauf zugreifen; rollen oder einzelpersonen>`

## 4. Sensitivity Notes

- **Klassifikation:** `<low / medium / high>`.
- **PII / Privileg / Compliance-Hinweise:** `<welche regeln gelten>`.
- **Begruendung:** `<warum diese sensitivitaet>`.

## 5. Ingestion-Pipeline

Welche Methode wird genutzt, um Inhalte aus diesem Data Space in `.md` zu normalisieren? Verweis auf konkrete `templates/ingestion-record.md`-Instanzen pro Ingestion-Vorgang.

- Default-Methode: `<manual-summary / OCR / parser-tool / not-extracted>`.
- Default-Approval-Anforderung: `<wer muss freigeben>`.

## 6. Catalog

Liste der enthaltenen Binaerdateien (oder Pointer auf einen ausfuehrlicheren Index, wenn die Liste sehr lang ist). Der Catalog **ersetzt nicht** `state/source-registry.md` — dort sind die Quellen einzeln registriert.

```text
- <binaer-1.pdf> | sensitivity:<low/medium/high> | normalized_markdown_path:<pfad-oder-leer> | normalization_review_path:<pfad-oder-leer>
- <binaer-2.docx> | sensitivity:<...> | ...
```

(noch keine)

## 7. `do_not_load`-Direktiven

Welche Dateien duerfen Claude oder ein RAG-System niemals geladen werden?

- `<datei-pfad>` — Begruendung.

## 8. Cleanup / Retention

- **Retention-Regel:** `<wie lange wird dieser data space aktiv gehalten>`.
- **Archive-Trigger:** `<unter welchen bedingungen wird der data space deaktiviert>`.
- **Archive-Verfahren:** Manifest und Pointer wandern nach `archive/YYYY-MM-DD-<slug>.md`. Originaldaten bleiben extern oder werden gemaess externer Retention-Regeln behandelt.

## Cross-Links

- Source-Registry: `../state/source-registry.md`.
- Source-Policy: `../source-policy.md`.
- Sicherheit: `../security-policy.md`.
- Ingestion-Record-Template: `ingestion-record.md`.
- Data-Space-README: `../data-space/README.md`.

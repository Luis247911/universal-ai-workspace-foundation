---
id: <normalized-document-slug>
type: normalized-document
title: "<titel>"
status: draft
source_registry_id: <source-id-aus-source-registry>
original_location: <pfad-oder-uri-oder-extern>
original_type: <pdf / docx / pptx / xlsx / image / audio / video / other>
normalized_from: <input-id-aus-ingestion-record>
created: <YYYY-MM-DD>
updated: <YYYY-MM-DD>
owner: <user-or-adapter>
sensitivity: <low / medium / high>
extraction_method: <manual-summary / OCR / parser-tool / not-extracted>
normalization_status: draft
verification_status: unverified
related: []
trust_level: external
lifecycle: research
review_after: <YYYY-MM-DD>
critical_claims_require_original_check: yes
---

# Normalized Document

**Hartregel:** Diese Datei darf nicht so behandelt werden, als sei sie korrekt, solange `verification_status` nicht `verified` ist. Bei kritischen Aussagen muss auf das Originaldokument oder die Normalization Review zurueckverwiesen werden.

## 1. Kurzbeschreibung

`<2-3 saetze: worum geht es im original; was wurde extrahiert>`

## 2. Herkunft / Originalreferenz

- **Original:** `<pfad oder uri>`.
- **Source-Registry-Eintrag:** `<source-id>`.
- **Original-Typ:** `<pdf/docx/pptx/xlsx/image/audio/video>`.
- **Aufnahmedatum:** `<YYYY-MM-DD>`.

## 3. Struktur des Originals

Uebersicht der Originalstruktur — Ueberschriften, Abschnitte, Tabellen, Anhaenge, Seitenbezuege.

```text
1. <abschnitt>
   1.1 <unterabschnitt>
2. <abschnitt>
   - tabelle <name>
   - anhang <name>
```

## 4. Normalisierter Inhalt

Hier folgt der eigentliche normalisierte Markdown-Text. Pro Abschnitt eine Markdown-Sektion mit Originalreferenz (z.B. "Originalseite 4-5") wo sinnvoll.

### `<abschnitt-1>` (Originalreferenz)

`<inhalt>`

### `<abschnitt-2>` (Originalreferenz)

`<inhalt>`

## 5. Ausgelassene Inhalte

Was wurde bewusst **nicht** in dieses Markdown-Derivat uebernommen?

- `<inhalt-1>` — Begruendung.
- `<inhalt-2>` — Begruendung.

## 6. Unsichere Stellen

Was ist beim Uebertragen unsicher? Niedrige OCR-Qualitaet? Mehrdeutige Formulierungen? Tabellenwerte mit unklarer Zuordnung?

- **Unsicher:** `<stelle>` — Begruendung.

## 7. Tabellen / Listen / Anhaenge

Wurden Tabellen vollstaendig uebernommen, paraphrasiert oder ausgelassen? Welche Listen oder Anhaenge wurden behandelt?

## 8. Wichtige Extraktionsentscheidungen

Welche Entscheidungen wurden getroffen, die das Verstehen beeinflussen (z.B. "Fussnoten ans Sektionsende verschoben", "Bildunterschriften als Bullet-Liste extrahiert")?

## 9. Verbindungen zu Knowledge Notes oder MOCs

`[[wiki-links]]`-Verbindungen, die diesen Inhalt im KG einordnen — sobald Verifikation den Status auf mindestens `partially_verified` hebt.

## 10. Hinweise fuer spaetere Pruefung

Was sollte bei der naechsten Verifikation oder einer document-normalization-review besonders beachtet werden?

## Cross-Links

- Source-Registry: `../state/source-registry.md`.
- Normalization-Review-Template: `normalization-review.md`.
- KG-Policy (Document-Normalization-Pipeline): `../knowledge-graph-policy.md`.
- Quality-Gates: `../quality-gates.md`.

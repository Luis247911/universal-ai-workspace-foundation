# data-space/ — Manifest-only Mount Point

**Wichtig:** `data-space/` ist im Foundation-Tree ein **Manifest-only Mount Point**. Hier wohnen ausschliesslich `.md`-Manifeste und Pointer. **Niemals** Original-Binaerdateien, **niemals** sensible Rohdaten, **niemals** Credentials.

## Was hier wohnt

- Data-Space-Manifeste in `.md` (aus `templates/data-space.md`).
- Naming-Konvention: `<datum>-<slug>.md` (z.B. `2026-05-06-projektspeicher-extern.md`).
- Optional ein `_index.md` als Catalog-MOC ueber alle Manifeste.

## Was hier NICHT wohnt

- Original-Binaerdateien (PDF, DOCX, PPTX, XLSX, Bilder, Audio, Video, etc.). Sie leben **extern**.
- Sensible Rohdaten.
- Credentials, API-Keys, Tokens.
- Auto-Sync-Skripte zu externen Speichersystemen.
- Generated Outputs (gehoeren ausserhalb der Foundation).

## Definition Project Data Space

Ein Project Data Space ist ein **projektspezifischer operativer Datenraum** fuer Inputs, Arbeitsdaten, Analysen, Zwischenstaende, Outputs und Nachweisdokumentation.

- **Foundation = Kontroll- und Managementschicht.** Hier wohnen Manifeste, Pointer, Tracking, Verifikations-Statuses.
- **Project Data Space = projektspezifischer operativer Datenraum.** Originaldaten leben dort, ausserhalb der Foundation.

Ein optionales RAG-/Retrieval-System ist nur ein Such- oder Zugriffslayer ueber einem sauber deklarierten Project Data Space. **RAG ist niemals Source of Truth.**

## Source of Truth-Hierarchie

1. Originaldokument (als Referenzquelle).
2. Deklarierter Project Data Space (extern).
3. Verifiziertes normalisiertes Markdown.
4. `state/source-registry.md` und `state/artifact-index.md`.
5. Verifizierte `.md`-Knowledge-Notes und Research-Reports.

## Manifest-Pattern

Pro Data Space ein `.md`-Manifest aus `templates/data-space.md` mit:

- Sensitivity-Klassifikation (low/medium/high).
- Allowed-Processing (manual / automated-with-approval / none).
- External Location (Pfad oder URI; bei `sensitivity: high` keine konkrete Location, nur abstrakter Hinweis).
- Catalog (Liste der enthaltenen Binaerdateien mit Pointern, optional verweisend auf `state/source-registry.md`).
- Retention-Policy.
- `do_not_load`-Direktiven fuer einzelne Inhalte.

## Beziehung zu state/

- Jeder Data-Space hat einen Eintrag in `state/source-registry.md` mit `type: data-space`.
- Manifest-Aenderungen werden in `state/artifact-index.md` getrackt.

## Sicherheit

- Bei `sensitivity: high`: keine konkrete Location im Manifest, nur abstrakter Hinweis. Inhalt verbleibt extern. Critical-Claims-Aussagen erfordern explizite manuelle Pruefung.
- Bei `sensitivity: medium`: explizite Freigabe oder Adapter-Regel mit deklariertem Schutzraum.
- Bei `sensitivity: low`: Extraktion in `research/`/`knowledge/` erlaubt nach Source-Registry-Eintrag.

Siehe `security-policy.md` Section 8 und `source-policy.md` Section 8-9.

## Lade-Regel

`Load on Relevance` (wenn Data-Space aktiv und relevant). Einzelne Manifeste ueber Pfad-Verweis. **Niemals automatisches Laden von Originalbinaerdateien.**

## Cross-Links

- Source-Policy: `../source-policy.md`.
- Sicherheit: `../security-policy.md`.
- Data-Space-Template: `../templates/data-space.md`.
- Ingestion-Record-Template: `../templates/ingestion-record.md`.
- Source-Registry: `../state/source-registry.md`.
- KG-Policy: `../knowledge-graph-policy.md`.

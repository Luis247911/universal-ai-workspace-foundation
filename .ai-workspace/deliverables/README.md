# deliverables/ — Kuratierte `.md`-Outputs

Dieses Verzeichnis enthaelt **strikt Markdown-first** kuratierte Outputs des Projekts. Fertige Reports, Briefings, Spezifikationen, Konzepte, Dokumentationen — alles als `.md`.

## Markdown-first-Regel

**Alle Foundation-Deliverables sind `.md`-Dateien.** Foundation-Tree enthaelt **keine Pflicht-Struktur** `_generated/`. Wenn ein Projekt PDF/PPTX/DOCX/XLSX oder andere Formate als finalen Kunden-Export benoetigt:

1. Die kanonische Arbeitsversion bleibt `.md`.
2. Der Export wird **nur** in `state/artifact-index.md` referenziert (mit Pfad zum externen Speicherort oder zum projektspezifisch deklarierten Project Data Space).
3. Der Export wird nicht automatisch geladen.
4. Der Export ersetzt **niemals** die `.md`-Quelle.
5. Foundation-Core liefert **keine** `_generated/`-Struktur.

Generated-Outputs leben **ausserhalb** der Foundation oder in einem projektspezifisch deklarierten Speicherort, nicht im Foundation-Tree selbst.

## Promotion-Trigger

Ein Artefakt wird nur dann nach `deliverables/` promoted, wenn:

- `verification_status: verified` (siehe `quality-gates.md`).
- Eine kuratierte, finale oder kunden-/aussenstehenden-orientierte Form vorliegt.
- Eintrag in `state/artifact-index.md` Status `active` und Typ `deliverable`.

## Versionierung

- Datum-Slug-Naming: `<datum>-<slug>.md`.
- Versionierungs-Suffix `_v2`, `_v3` nur falls explizit noetig (sonst neueres Datum oder neuer Slug).

## Lifecycle

- `deliverables/` -> `archive/`: wenn supersedet oder abgeschlossen. Datei nach `archive/YYYY-MM-DD-<slug>.md` verschieben; Active-Pointer zuruecklassen falls verlinkt; Status in `state/artifact-index.md` auf `archived`.
- Kein Silent-Delete.

## Was hierher NICHT gehoert

- Generated Nicht-Markdown-Files (PDF/PPTX/DOCX/XLSX als Default in der Foundation-Struktur).
- Drafts oder ungeprueftes Material (lebt in `research/` oder `scratch/`).
- Kunden-Originaldateien (lebt im Project Data Space oder extern).

## Cross-Links

- Lifecycle: `../file-lifecycle.md`.
- Quality-Gates: `../quality-gates.md`.
- Artifact-Index: `../state/artifact-index.md`.

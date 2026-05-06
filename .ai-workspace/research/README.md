# research/ — Geprueftes oder zu pruefendes Material

Dieses Verzeichnis enthaelt geprueftes oder zu pruefendes externes Material in `.md`-Form. Quellen-Outputs, Source-Notes, Research-Reports, Normalized-Documents und Normalization-Reviews leben hier, bis sie geprueft und nach `knowledge/` oder `deliverables/` promoted werden — oder als veraltet/widerlegt nach `archive/` wandern.

## Was hierher gehoert

- Source-Notes (`.md` aus `templates/source-note.md`).
- Research-Reports (`.md` aus `templates/research-report.md`).
- Normalized-Documents in `draft`/`reviewed` Status (`.md` aus `templates/normalized-document.md`).
- Normalization-Reviews (`.md` aus `templates/normalization-review.md`).
- Sonstige paraphrasierte oder synthetisierte externe Inhalte.

## Was hierher NICHT gehoert

- Originalbinaerdateien (PDF/DOCX/PPTX/XLSX/Bilder/Audio/Video). Diese leben extern oder im projektspezifisch deklarierten Project Data Space.
- Inhalte ohne Source-Registry-Bezug (jeder Eintrag muss eine `source-id` referenzieren).
- Sensible Volltexte aus Quellen mit `sensitivity: high` (siehe `security-policy.md`).
- Aktive Skripte, Hooks, MCP-Configs.

## Naming-Konvention

`<datum>-<source-id>-<slug>.md` oder `<source-id>-<datum>.md`. Datum im Format `YYYY-MM-DD`. ASCII, kebab-case.

## Trust-Level-Tagging

Frontmatter `trust_level` ist Pflicht (`trusted` / `external` / `hostile`).

## 90-Tage-Review-Trigger

Dateien aelter als 90 Tage werden im naechsten Cleanup-Review gepruft (`templates/cleanup-review.md` Sektion 2).

## Promotion-Pfade

- `research/` -> `knowledge/`: bei stabilisiertem Wissen, nach Quality-Gate-Promotion `verified`.
- `research/` -> `deliverables/`: bei kuratierten Outputs.
- `research/` -> `archive/`: bei Veraltung oder Widerlegung.

## Cross-Links

- Source-Policy: `../source-policy.md`.
- Quality-Gates: `../quality-gates.md`.
- Lifecycle: `../file-lifecycle.md`.
- KG-Policy: `../knowledge-graph-policy.md`.
- Source-Note-Template: `../templates/source-note.md`.
- Research-Report-Template: `../templates/research-report.md`.
- Normalized-Document-Template: `../templates/normalized-document.md`.
- Normalization-Review-Template: `../templates/normalization-review.md`.

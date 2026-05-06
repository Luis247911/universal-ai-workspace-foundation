---
id: <normalization-review-slug>
type: normalization-review
title: "Normalization Review fuer <normalized-document-slug>"
normalized_document_id: <normalized-document-slug>
source_registry_id: <source-id>
original_location: <pfad-oder-uri-oder-extern>
reviewer: <user-or-adapter>
review_date: <YYYY-MM-DD>
review_method: <manual / delegated / maintenance-routine / independent-second-review>
verification_status: unverified
sensitivity: <low / medium / high>
follow_up_required: yes
---

# Normalization Review

Pruefprotokoll fuer eine `templates/normalized-document.md`-Instanz. Ergebnis legt fest, ob die normalisierte Version als bevorzugte Arbeitsfassung genutzt werden darf.

## 1. Review Summary

`<3-5 saetze: was wurde geprueft, was ist das ergebnis>`

## 2. Original geprueft?

- **Geprueft:** `<yes/no>`.
- **Welcher Teil:** `<gesamtes original / nur abschnitte X-Y>`.

## 3. Markdown geprueft?

- **Geprueft:** `<yes/no>`.

## 4. Strukturpruefung

- **Ueberschriften:** `<vollstaendig / partiell / fehler>` — Anmerkung.
- **Abschnitte:** `<vollstaendig / partiell / fehler>`.
- **Tabellen:** `<vollstaendig / partiell / fehler>`.
- **Listen:** `<vollstaendig / partiell / fehler>`.
- **Anhaenge:** `<vollstaendig / partiell / fehler>`.
- **Seiten-/Abschnittsbezuege:** `<klar / partiell / fehler>`.

## 5. Inhaltspruefung

- **Zahlen:** `<korrekt / fehler / unsicher>` — Anmerkung.
- **Daten:** `<korrekt / fehler / unsicher>`.
- **Namen:** `<korrekt / fehler / unsicher>`.
- **Definitionen:** `<korrekt / fehler / unsicher>`.
- **Negationen:** `<korrekt / fehler / unsicher>`.
- **Tabellenwerte:** `<korrekt / fehler / unsicher>`.
- **Fussnoten:** `<korrekt / fehler / unsicher>`.
- **Wichtige Einschraenkungen:** `<korrekt / fehler / unsicher>`.

## 6. Fehlende Inhalte

Was fehlt im Markdown-Derivat?

- `<inhalt-1>` — Schweregrad / Auswirkung.

## 7. Unsichere Inhalte

Welche Stellen konnten nicht vollstaendig verifiziert werden?

- `<stelle-1>` — Begruendung.

## 8. Moegliche Uebertragungsfehler

Welche Fehler koennten beim Normalisieren passiert sein?

- `<fehler-1>` — Begruendung.

## 9. Kritische Aussagen, die zurueck zum Original geprueft werden muessen

- `<aussage-1>` — Begruendung.
- `<aussage-2>` — Begruendung.

## 10. Discrepancy Log

Liste aller gefundenen Diskrepanzen mit Schweregrad.

| Diskrepanz | Schweregrad | Originalreferenz | Status |
|------------|-------------|------------------|--------|
| (noch keine) | | | |

## 11. Empfehlung

Wahl: `use_as_working_copy` / `use_with_caution` / `reprocess_required` / `do_not_use`.

- **Empfehlung:** `<wahl>`.
- **Begruendung:** `<warum>`.

## 12. Follow-up Actions

Was muss als Naechstes passieren?

- `<aktion-1>` — Owner — Datum.

## 13. Links zu erzeugten Knowledge Notes, Research Reports oder Deliverables

- `[[<knowledge-note>]]`
- `[[<research-report>]]`

## Cross-Links

- Normalized-Document-Template: `normalized-document.md`.
- Source-Registry: `../state/source-registry.md`.
- Artifact-Index: `../state/artifact-index.md`.
- KG-Policy: `../knowledge-graph-policy.md`.
- Quality-Gates: `../quality-gates.md`.

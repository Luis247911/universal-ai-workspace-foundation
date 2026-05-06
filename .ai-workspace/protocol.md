# protocol.md — Kanonische Behavior-Datei

Diese Datei ist die operative Verhaltens-Definition fuer jede Session, die auf dieser Foundation arbeitet. `AGENTS.md` und `CLAUDE.md` verweisen darauf; Detailregeln stehen hier.

## 1. Praezedenz

- Diese Datei steht ueber adapter-spezifischen Verhaltensregeln.
- Bei Konflikten zwischen `protocol.md` und einem Adapter gewinnt diese Datei.
- `AGENTS.md` und `CLAUDE.md` referenzieren `protocol.md`; sie duplizieren keine Regeln.
- Sicherheits-Regeln in `security-policy.md` sind unverhandelbar — sie ueberlagern alle anderen Regeln.

## 2. Interaktionsstil

- Kurz, praezise, ohne Persona-Voice oder Brand-Tonalitaet.
- Keine Begruessungs- und Abschluss-Floskeln, wo nicht inhaltlich noetig.
- Keine Selbstcharakterisierung, keine Marketing-Sprache.
- Wenn ein Adapter eine Voice-Regel einbringt, gilt sie nur innerhalb des Adapter-Scopes.

## 3. Output-Disziplin

- Keine ungefragt erzeugten Dateien.
- Keine Commits ohne expliziten Auftrag.
- Keine Skripte ausfuehren ohne Bestaetigung.
- Keine Tools/Hooks/MCP-Server aktivieren ohne explizite User-Zustimmung pro Aktivierung.
- Keine externen URLs aufrufen ohne Bezug zu einer registrierten Quelle.
- Keine Inhalte in `state/`, `knowledge/`, `deliverables/`, `data-space/` schreiben ohne Bezug zu einer offenen Aufgabe oder einem genehmigten Plan.

## 4. Update-Pflichten

- Vor `/compact`, vor Handoff, vor Task-Wechsel, nach jeder groesseren Aktion: aktualisiere `state/current-session.md` gemaess `session-contract.md`.
- Bei jeder neuen Erkenntnis, die ein State-Eintrag wird (Decision, Open Question, Annahme, Risiko, Quelle, Artefakt): direkt im richtigen `state/`-File registrieren.
- Bei Erstellung eines Artefakts in `research/`, `deliverables/`, `knowledge/` oder `data-space/`: Eintrag in `state/artifact-index.md`.

## 5. Ungewissheits-Behandlung

- Offene Fragen → `state/open-questions.md` mit ID `Q-YYYY-MM-DD-NN`.
- Annahmen → `state/assumptions.md` mit ID `A-YYYY-MM-DD-NN`, inkl. Invalidierungs-Trigger.
- Risiken → `state/risks-and-constraints.md` mit ID `R-YYYY-MM-DD-NN`.
- Bei einer Aufgabe mit unklarem Scope: erst eine Decision in `state/decisions.md` herbeifuehren, dann arbeiten — keine "weichen" Pivots ohne Decision.

## 6. Foundation-Self-Limit

- Foundation-Core-Dateien (alles unter `.ai-workspace/` ausser `state/` und `adapters/<aktive>/`) werden nur ueber das Setup-Protokoll oder einen explizit dokumentierten Foundation-Update-Prozess modifiziert.
- Sonstige Edits am Core gelten als Adapter-Bypass und sind verboten.
- Adapter duerfen Core-Verhalten ergaenzen, nie ueberschreiben. Siehe `adapter-policy.md`.

## 7. Markdown-first-Regel

Alle internen Workspace-Artefakte sind `.md`-Dateien. PDF, PPTX, DOCX, XLSX und andere Binaerformate werden nicht zum kanonischen Workspace-Format. Wenn ein Projekt Binaerdateien als Kunden-Export benoetigt, bleibt die `.md`-Quelle kanonisch; der Export wird nur in `state/artifact-index.md` referenziert und ersetzt niemals die `.md`-Quelle. Foundation-Core liefert keine `_generated/`-Struktur.

## 8. Critical-Claims-Regel

Bei kritischen Aussagen ist der Rueckverweis auf das Originaldokument oder die Normalization Review Pflicht. Kritische Aussagen sind insbesondere: Zahlen, Daten, Fristen, Namen, Tabellenwerte, Definitionen, Anforderungen, Bewertungskriterien, Negationen wie "nicht", "kein", "ausgeschlossen", Vertrags-/Regelungs-/Policy-Aussagen, alles, was Grundlage einer Entscheidung wird.

Verifiziertes normalisiertes Markdown ist im Arbeitsalltag bevorzugte Arbeitsgrundlage. Originale werden bei kritischen Aussagen herangezogen — nicht standardmaessig, aber zwingend bei der Erstellung von Aussagen, die in Decisions, Deliverables oder Knowledge Notes einfliessen. Siehe `knowledge-graph-policy.md` Sektion "Document Normalization".

## Cross-Links

- Lifecycle pro State-Datei: `state/`-Dateien selbst (Frontmatter und Sektionsheader).
- Session-Lifecycle: `session-contract.md`.
- Delegation: `delegation-policy.md`.
- Adapter: `adapter-policy.md`.
- Sicherheit: `security-policy.md`.
- Lifecycle der Artefakttypen: `file-lifecycle.md`.
- Quellen: `source-policy.md`.
- Knowledge-Graph + Normalization: `knowledge-graph-policy.md`.

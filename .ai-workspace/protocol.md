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

- Vor `/compact`, vor Handoff, vor Task-Wechsel, nach jeder groesseren Aktion: Journal-Eintrag anhaengen und `state/now.md` aktualisieren gemaess `session-contract.md` §3.
- Bei jeder neuen Erkenntnis, die ein Eintrag wird: Decision, Open Question, Annahme oder Risiko direkt als Notiz unter `knowledge/decision/` bzw. `knowledge/question/` anlegen (`python -m harness.mdmemory new …`, danach `python -m harness.mdmemory index`); Quelle und Artefakt direkt im richtigen `state/`-File registrieren (`source-registry.md`, `artifact-index.md`).
- Bei Erstellung eines Artefakts in `research/`, `deliverables/`, `knowledge/` oder `data-space/`: Eintrag in `state/artifact-index.md`.

## 5. Ungewissheits-Behandlung

Jeder Eintrag ist eine eigene Notiz (D-2026-09-30-04): `python -m harness.mdmemory new question "<titel>" --kind question|assumption|risk|constraint` bzw. `new decision "<titel>"`, danach `python -m harness.mdmemory index`. Die Sichten `state/open-questions.md`, `state/assumptions.md`, `state/risks-and-constraints.md` und `state/decisions.md` sind generiert und werden nie von Hand editiert. Alte IDs (`Q-`/`A-`/`R-`/`D-YYYY-MM-DD-NN`) bleiben als `aliases` gueltig.

- Offene Fragen → Notiz unter `knowledge/question/` mit `kind: question`.
- Annahmen → Notiz unter `knowledge/question/` mit `kind: assumption`, inkl. Invalidierungs-Trigger.
- Risiken → Notiz unter `knowledge/question/` mit `kind: risk` (Constraints: `kind: constraint`).
- Bei einer Aufgabe mit unklarem Scope: erst eine Decision (Notiz unter `knowledge/decision/`) herbeifuehren, dann arbeiten — keine "weichen" Pivots ohne Decision.

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

# context-policy.md — Was wird wann geladen

Diese Datei definiert pro Pfad die Lade-Regel. Ziel: kleiner stabiler Kontext beim Session-Start, alles weitere lazy oder auf Anfrage.

## 1. Vier Lade-Kategorien

| Kategorie | Definition |
|-----------|------------|
| **Always Load** | Bei jedem Session-Start automatisch wahrgenommen. |
| **Load on Relevance** | Bei thematischer Relevanz (Aufgabentyp passt) zu lesen. |
| **Load on Explicit Request** | Nur lesen, wenn der User oder eine konkrete Aufgabe es verlangt. |
| **Never Auto-Load** | Niemals automatisch — nur auf explizite Anfrage zugaenglich. |

## 2. Pfad-zu-Kategorie-Tabelle

| Pfad | Kategorie | Begruendung |
|------|-----------|-------------|
| `AGENTS.md` | Always Load | Tool-agnostischer Root-Contract. |
| `CLAUDE.md` (falls Tool=Claude) | Always Load | Tool-Delta. |
| `state/project-index.md` | Always Load | Projekt-Identitaet. |
| `state/current-session.md` | Always Load | Live-Zustand. |
| `protocol.md` | Load on Relevance | Operative Verhaltens-Detailregeln. |
| `setup-protocol.md` | Load on Relevance | Bei Setup oder Strukturentscheidungen. |
| `session-contract.md` | Load on Relevance | Bei Compact, Handoff, Resume. |
| `context-policy.md` (diese Datei) | Load on Relevance | Bei Lade-Entscheidungen. |
| `file-lifecycle.md` | Load on Relevance | Bei Promotion, Archivierung, Stale-Reviews. |
| `source-policy.md` | Load on Relevance | Bei Source-Eintrag oder Reference-Frage. |
| `security-policy.md` | Load on Relevance | Bei Security-Frage; ueberlagert sonst alles. |
| `delegation-policy.md` | Load on Relevance | Bei Subagent-Spawn, Maintenance-Routine, externer Analyse. |
| `adapter-policy.md` | Load on Relevance | Bei Adapter-Aktivierung/Deaktivierung. |
| `quality-gates.md` | Load on Relevance | Bei Promotion-Entscheidungen. |
| `knowledge-graph-policy.md` | Load on Relevance | Bei KG-Aktion oder Document-Normalization. |
| `state/open-questions.md` | Load on Relevance | Bei offener Frage oder Resume. |
| `state/decisions.md` | Load on Relevance | Bei jeder Decision-relevanten Entscheidung. |
| `state/assumptions.md` | Load on Relevance | Bei Annahme-Pruefung. |
| `state/risks-and-constraints.md` | Load on Relevance | Bei Risiko-/Constraint-Pruefung. |
| `state/source-registry.md` | Load on Relevance | Bei Source-Bezug. |
| `state/artifact-index.md` | Load on Relevance | Bei Artefakt-Bezug. |
| `knowledge/_index.md` | Load on Relevance | Wenn Knowledge-Graph aktiv. |
| `knowledge/<topic>/_moc.md` | Load on Relevance | Wenn Topic relevant. |
| `knowledge/<topic>/<slug>.md` | Load on Explicit Request | Ueber `[[wiki-link]]`-Verfolgung. |
| `data-space/<manifest>.md` | Load on Relevance | Wenn Data-Space aktiv und relevant. |
| `templates/*` | Load on Explicit Request | Beim Anlegen neuer Artefakte. |
| `research/*` | Load on Explicit Request | Bei konkreter Recherche-Referenz. |
| `deliverables/*` | Load on Explicit Request | Bei Auslieferung-Vorbereitung. |
| `scratch/*` | Never Auto-Load | Ephemer, untrusted. |
| `archive/*` | Never Auto-Load | Inerte Historie. |
| `adapters/<aktiv>/adapter.md` | Load on Relevance | Wenn Adapter aktiviert + Aufgabe im Adapter-Scope. |
| `adapters/<aktiv>/<sonstige>.md` | Load on Explicit Request | Adapter-Inhalte jenseits adapter.md. |
| `adapters/<inaktiv>/**` | Never Auto-Load | Inaktive Adapter werden ignoriert. |
| Quellen mit `do_not_load: true` in `state/source-registry.md` | Never Auto-Load | Direktive blockiert Auto-Inject. |
| Original-Binaerdateien | Never Auto-Load | Werden nie automatisch geladen — Document-Normalization-Pipeline siehe `knowledge-graph-policy.md`. |

## 3. KG-Navigations-Regel

Bei Wissens- oder Konzept-Anfragen:

1. Lies zuerst `knowledge/_index.md` (Root-MOC).
2. Identifiziere relevante Topic-MOCs (`knowledge/<topic>/_moc.md`).
3. Folge selektiv `[[wiki-links]]` zu konkreten Knowledge-Notes.
4. Lade nicht den ganzen Graphen blind.
5. Beruehre `archive/`, `scratch/`, inaktive Adapter nicht automatisch.
6. Bei grossen MOCs (>50 Eintraege): pruefe nur die thematisch passenden Subsektionen.

## 4. Original-Binary-Lade-Regel

Originale (PDF, DOCX, PPTX, XLSX, Bilder, Audio, Video) werden niemals automatisch geladen. Bevorzugung: verifiziertes normalisiertes Markdown (`templates/normalized-document.md`-Form). Bei kritischen Aussagen muss zurueck auf das Original oder die Normalization Review verwiesen werden — siehe `protocol.md` Section 8 und `knowledge-graph-policy.md` Sektion "Document Normalization".

## 5. Unverified-Markdown-Regel

`normalized-document.md`-Dateien mit `verification_status: unverified` oder `partially_verified` werden nur mit Warnhinweis genutzt. `do_not_use`-Markdown wird nicht verwendet. Verifiziertes Markdown ist die bevorzugte Arbeitsgrundlage.

## 6. RAG-Lade-Regel (falls Adapter eingebracht)

Wenn ein Adapter ein RAG-System anbindet:

- RAG-Calls sind explizite Tool-Calls, kein Auto-Inject.
- RAG-Output-Trust-Level = `external` (untrusted-default).
- RAG-Output landet maximal in `research/` oder `scratch/`.
- `do_not_load`-Direktiven in `state/source-registry.md` muessen vom RAG-System respektiert werden.
- RAG ist niemals Source of Truth (siehe `knowledge-graph-policy.md`).

## 7. Lazy-Load-Default

Alles, was nicht in "Always Load" steht, ist Lazy-Load. Beim Session-Start werden ausschliesslich die vier Boot-Dateien wahrgenommen. Alles weitere wird ueber explizite Pfad-Referenzen oder ueber den Workflow erschlossen.

## Cross-Links

- Behavior: `protocol.md`.
- Adapter: `adapter-policy.md`.
- KG: `knowledge-graph-policy.md`.
- Sicherheit: `security-policy.md`.
- Quellen: `source-policy.md`.

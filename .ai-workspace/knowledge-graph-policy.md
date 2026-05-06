# knowledge-graph-policy.md — Markdown-KG, Document-Normalization, Maintenance-Blueprints, RAG-Beziehung

Diese Datei definiert das Markdown-Knowledge-Graph-Protokoll, die Document-Normalization-Pipeline und das Maintenance-Routine-Konzept. Sie ist die kanonische Referenz fuer alle KG-, Normalization- und Maintenance-Themen.

## 1. Zweck

Der Markdown Knowledge Graph ist das primaere menschenlesbare Langzeitgedaechtnis des Projekts. `.md`-Dateien sind kanonisch. Eine optionale RAG-Anbindung ist nur Suchlayer, niemals Source of Truth.

## 2. Obsidian-Kompatibilitaet

Foundation darf `[[wiki-links]]`, YAML-Frontmatter und MOC-Dateien (Map of Content) nutzen. Sie bleibt aber auch ohne Obsidian lesbar — keine harte Obsidian-Abhaengigkeit. Dateinamen ASCII, kebab-case, ohne Whitespaces.

## 3. Link-Regeln

- Nutze `[[wiki-links]]` fuer zentrale Konzepte, Entscheidungen, Quellen, Artefakte und Adapter.
- Setze keine nackten Links ohne semantischen Beziehungskontext, wenn die Beziehung wichtig ist. Beispiel: nicht "siehe `[[concept-x]]`", sondern "ergaenzt das Pattern in `[[concept-x]]`".
- Beschreibe semantische Beziehungen in normalem Markdown.
- Verlinke nur auf existierende oder bewusst geplante Notes.
- Geplante, aber noch nicht existierende Links: markiere die Ziel-Note (auch als Stub erstellt) im Frontmatter mit `status: planned`. Optional Inline-Kommentar `<!-- planned: <slug> -->` an der Quell-Stelle, falls die Ziel-Note noch nicht existiert.

## 4. Frontmatter-Regeln

Jede dauerhafte Knowledge-Graph-Datei (Knowledge-Note, MOC, Source-Note, Research-Report, Normalized-Document, Normalization-Review, Decision-Record, Data-Space-Manifest, Ingestion-Record) sollte Frontmatter mit folgenden Feldern enthalten:

```yaml
id: <slug>                       # eindeutig im Projekt
type: <typ>                      # knowledge-note / moc / source-note / research-report / decision-record / data-space / ingestion-record / maintenance-routine / normalized-document / normalization-review
status: <status>                 # draft / active / planned / superseded / archived
created: YYYY-MM-DD
updated: YYYY-MM-DD
owner: <user-or-adapter-slug>
source_ids: [<source-id>, ...]   # Liste der Quellen aus state/source-registry.md
related: [[[wiki-link]], ...]    # semantisch relevante Verbindungen
trust_level: <trust>             # trusted / external / hostile
lifecycle: <zone>                # scratch / research / knowledge / deliverable / archive — Pfad-konsistent
review_after: YYYY-MM-DD         # optional
```

Erweiterte Felder fuer normalized-document und normalization-review siehe `templates/normalized-document.md` und `templates/normalization-review.md`.

## 5. MOC-/Index-Regeln

Eine MOC-Datei (Map of Content) ist Einstiegspunkt fuer ein Topic. MOCs **duerfen Links sammeln, aber keine zweite State-Quelle werden**. MOCs referenzieren State-Dateien (z.B. `[[D-2026-04-17-NN]]` fuer eine Decision aus `state/decisions.md`), ersetzen sie aber nicht.

- Root-MOC: `knowledge/_index.md`.
- Topic-MOCs: `knowledge/<topic>/_moc.md`.
- Adapter-spezifische MOCs leben unter `adapters/<slug>/<sub>/_moc.md` und werden ggf. vom Root-MOC verlinkt mit Adapter-Hinweis.

## 6. Kein Parallel-State

Der Knowledge Graph darf **nicht** `current-session.md`, `decisions.md`, `source-registry.md`, `artifact-index.md` oder andere State-Dateien ersetzen. Er darf sie nur referenzieren.

Beispiel: Eine Decision lebt als Zeile in `state/decisions.md` mit ID `D-YYYY-MM-DD-NN`. Eine Knowledge-Note kann diese Decision via `[[D-YYYY-MM-DD-NN]]` referenzieren und in narrativem Kontext einordnen, aber den Decision-Inhalt nicht duplizieren.

## 7. Pflege-Regeln

Es muss moeglich sein:

- Tote `[[wiki-links]]` zu erkennen.
- Veraltete Notes zu markieren.
- Unverbundene Notes (keine eingehenden Links, kein MOC-Eintrag) zu melden.
- Widerspruechliche Notes zu melden.
- Alte Notes nicht automatisch zu loeschen.
- Aenderungen ueber `templates/cleanup-review.md` und `state/artifact-index.md` nachvollziehbar zu machen.

Die Foundation liefert dafuer **keine aktive Routine**, sondern nur das Pflege-Protokoll und das Maintenance-Routine-Template (siehe Section 11 + `templates/maintenance-routine.md`).

## 8. Retrieval-Regel

Bei Wissens- oder Konzept-Anfragen navigiert die Hauptsession den KG **agentisch**:

1. Lies zuerst `knowledge/_index.md` (Root-MOC) oder das thematisch naechste MOC.
2. Folge selektiv relevante `[[wiki-links]]`.
3. Lade nicht den ganzen Graphen blind.
4. `archive/`, `scratch/` oder inaktive Adapter werden nicht automatisch traversiert.
5. Bei grossen MOCs (>50 Eintraege): pruefe nur die thematisch passenden Subsektionen.

## 9. Beziehung zu RAG

RAG / Retrieval-Augmented-Generation oder semantische Suche sind **optional**. Wenn ein RAG existiert, ist es nur ein Suchlayer ueber dem Markdown Knowledge Graph oder Project Data Space. **RAG ist niemals Source of Truth.** Die `.md`-Dateien und registrierten Quellen bleiben kanonisch.

Source-of-Truth-Hierarchie:

1. Originaldokument (als Referenzquelle).
2. Deklarierter Project Data Space (extern).
3. Verifiziertes normalisiertes Markdown.
4. `state/source-registry.md` und `state/artifact-index.md`.
5. Verifizierte `.md`-Knowledge-Notes und Research-Reports.

Adapter, die ein RAG einbinden, deklarieren das in `adapter.md`, dokumentieren Indexierungs-Scope und respektieren `do_not_load`-Direktiven (siehe `security-policy.md` Section 9-10 und `adapter-policy.md` Section 9).

## 10. Document Normalization Pipeline

Foundation definiert eine **achtstufige Pipeline** als verbindliches Protokoll. Foundation liefert kein aktives Tooling; nur die Spezifikationen, Templates und Verifikations-Stufen.

### Drei-Schichten-Architektur

1. **Original Document.** Die unveraenderte Originaldatei (PDF, DOCX, PPTX, XLSX, Bild, Scan, Audio, Video oder anderer Binary-Input). Wird in `state/source-registry.md` referenziert. Nicht automatisch geladen. Bleibt als Referenz- und Beweisquelle erhalten.
2. **Normalized Markdown.** Aus dem Original erzeugte `.md`-Arbeitsfassung, menschenlesbar, Claude-lesbar, diffbar, verlinkbar, KG-kompatibel. Erst nach Pruefung bevorzugte Arbeitsgrundlage.
3. **Normalization Review.** `.md`-Pruefprotokoll mit `verification_status` und Discrepancy-Log.

### Pipeline (8 Stufen)

```text
Original Binary
  |
  v
1. Intake
   - Originaldatei wird als Source registriert (state/source-registry.md, type=binary)
   - Sensitivity, allowed_processing, do_not_load gesetzt
  |
  v
2. First Markdown Normalization
   - Erste Markdown-Version erzeugt (templates/normalized-document.md)
   - Status: draft
   - normalization_status: draft
   - verification_status: unverified
  |
  v
3. Structural Review
   - Pruefung von Ueberschriften, Abschnitten, Tabellen, Listen, Anhaengen, Seitenbezuegen
   - Ergebnis in templates/normalization-review.md (Sektion 4)
  |
  v
4. Content Review
   - Pruefung kritischer Inhalte: Zahlen, Daten, Namen, Definitionen, Negationen, Tabellenwerte, Fussnoten
   - Ergebnis in normalization-review.md (Sektion 5)
  |
  v
5. Discrepancy Logging
   - Jede Unsicherheit, Luecke, moegliche Fehluebertragung dokumentiert
   - Ergebnis in normalization-review.md (Sektionen 6-10)
  |
  v
6. Independent Review
   - Zweite Pruefung durch Mensch, separate Session, delegierte Arbeit, Maintenance Routine oder projektspezifischen Adapter
   - Foundation liefert keine aktiven Agents; Review-Vertrag in delegation-policy.md
  |
  v
7. Promotion
   - Bei erfolgreicher Pruefung: verification_status auf 'verified' gesetzt
   - Erst dann darf die Markdown-Version als bevorzugte Arbeitsgrundlage gelten
   - Knowledge-Graph-Linkage erlaubt (siehe Section 11 unten)
  |
  v
8. Ongoing Review
   - Bei neuer Original-Version, neuer Quelle oder Widerspruch:
     verification_status zurueck auf 'partially_verified' oder 'unverified'
   - Bei kritischen Fehlern: 'do_not_use' (Note darf nicht verwendet werden)
```

### Hartregel

**Originaldokumente bleiben die Referenzquelle.** **Verifiziertes Markdown ist die bevorzugte Arbeitsfassung.** **Kritische Aussagen muessen auf das Originaldokument rueckfuehrbar sein.**

Im Arbeitsalltag: bevorzugt verifiziertes normalisiertes Markdown nutzen. Bei kritischen Aussagen: zwingend Rueckverweis auf Originalquelle oder Normalization Review.

**Kritische Aussagen** sind insbesondere: Zahlen, Daten, Fristen, Namen, Tabellenwerte, Definitionen, Anforderungen, Bewertungskriterien, Negationen wie "nicht", "kein", "ausgeschlossen", Vertrags-/Regelungs-/Policy-Aussagen, alles, was Grundlage einer Entscheidung wird.

### Sensitivity-Stufen-Interaktion

- `sensitivity: low` -> Normalisierung erlaubt nach Source-Registry-Eintrag.
- `sensitivity: medium` -> Normalisierung erfordert explizite Freigabe oder Adapter-Regel mit deklariertem Schutzraum.
- `sensitivity: high` -> keine automatische Normalisierung; Inhalt verbleibt extern; nur Pfad/Existenz-Hinweis in Source-Registry.

## 11. Normalized-Markdown-Integration in den KG

Eine Normalized-Markdown-Datei darf in den Knowledge-Graph aufgenommen werden, wenn:

- `source_registry_id` vorhanden ist.
- `verification_status` mindestens `partially_verified` ist.
- Unsichere Inhalte klar markiert sind.
- Kritische Claims auf Originalquelle rueckfuehrbar bleiben.

Verifizierte Normalized Markdown darf als bevorzugte Arbeitsfassung genutzt werden. Unverified nur mit Warnhinweis. Do-not-use nicht verwendet.

## 12. Maintenance-Routine-Konzept

Eine Maintenance Routine ist ein **optionaler**, projektspezifisch oder global definierter Wartungsprozess, der den Markdown-Knowledge-Graph, die Source Registry, den Artifact Index, Adapter, Lifecycle-Dateien oder Normalized-Documents prueft und Reports erzeugt.

**Foundation-Status:** Foundation enthaelt **keine aktive Maintenance Routine**. Foundation enthaelt:

- Das **Konzept** (diese Sektion).
- Die **Spezifikations-Vorlage** (`templates/maintenance-routine.md`).
- Die **Registrierungs-Regel** (`adapter-policy.md`: nur via Adapter oder explizite User-Konfiguration).
- Die **Trust-Boundary** (Outputs sind delegierte Arbeit; siehe `delegation-policy.md`).

### Universelle Blueprints (sechs + ein optionaler)

Diese Blueprints sind **Plan-Referenz**, nicht Foundation-Inhalt. Adapter koennen sie als Vorlage nutzen, indem sie pro adopted Routine eine Spezifikation aus `templates/maintenance-routine.md` ableiten.

**Wichtig:** Keine konkreten Frequenzen als Default. Keine Uhrzeiten. Keine Cron-Strings. Keine Hook-Events. Keine konkreten Skill-Namen aus User-Setups. Keine Implementierung. Keine Skripte. Keine MCP-Konfiguration. Keine automatische Aktivierung. Typische Kadenz wird generisch beschrieben: "manual / daily / weekly / monthly depending on project need".

#### Blueprint 1: knowledge-graph-lint

Prueft tote `[[wiki-links]]`, fehlende Backlinks, verwaiste Knowledge-Notes, MOC-Drift, fehlendes Frontmatter, widersprueechliche Links.

#### Blueprint 2: knowledge-graph-sync

Prueft, ob neue Research Reports, Source Notes, Decisions, Deliverables, Normalized Documents, Normalization Reviews oder Ingestion Records in den Markdown-Knowledge-Graph uebernommen oder verlinkt werden sollten.

#### Blueprint 3: session-memory-review

Prueft, ob wichtige Erkenntnisse aus Session-Verlaeufen, Handoffs oder `current-session.md` in durable State, Decisions, Assumptions, Knowledge Notes oder Open Questions uebernommen werden sollten.

#### Blueprint 4: source-artifact-hygiene

Prueft Source Registry, Artifact Index, stale Sources, unregistrierte Artefakte, Research Reports ohne Trust-Level, Binary Sources ohne Normalized Markdown und Deliverables ohne kanonische Markdown-Quelle.

#### Blueprint 5: adapter-lifecycle-review

Prueft aktive und inaktive Adapter, fehlende Registrierung, unklare Outputs, stale Adapter und moegliche Core-Regel-Verletzungen.

#### Blueprint 6: document-normalization-review

Prueft, ob normalized Markdown-Dateien korrekt, vollstaendig, verifiziert und auf Originalquellen rueckfuehrbar sind. Konkret: Original existiert noch, Source-Registry-Eintrag existiert, Normalized-Markdown existiert, Normalization-Review existiert, `verification_status` ist gesetzt, kritische Claims sind markiert, unsichere Stellen sind dokumentiert, veraltete Normalisierungen sind als solche markiert, `do_not_use`-Dokumente werden nicht referenziert.

#### Blueprint 7 (optional, nicht Core-Default): session-snapshot-export

Erstellt einen redacted Session-Snapshot als Markdown. Nur zulaessig, wenn Speicherort, Sensitivitaet, Redaction-Regeln und Retention geklaert sind. Kein externer Sync ohne explizite User-Freigabe.

### Pflicht-Regeln fuer jeden Blueprint

- Output ist `unverified` bis Hauptsession verifiziert.
- Niemals direkte durable-State-Mutation.
- Niemals Secrets lesen.
- Niemals externe Repos klonen oder downloaden.
- Niemals Binaerdateien automatisch verarbeiten, wenn `sensitivity` ungeklaert ist.
- Niemals Parallelstrukturen erzeugen.
- Keine MCP-Server, Hooks, Cronjobs ohne explizite User-Bestaetigung registrieren.

### Aktivierungs-Flow

1. Adapter wird in `state/project-index.md` als aktiv markiert.
2. Adapter deklariert die Routine in `adapter.md`.
3. Pro Routine wird `templates/maintenance-routine.md` ausgefuellt und unter `adapters/<slug>/maintenance/<routine-name>.md` abgelegt.
4. Trigger ist manuell oder via Adapter-Mechanismus.
5. Output landet in Default-Location `scratch/maintenance/<datum>-<routine>.md` oder vom Adapter spezifizierten Pfad.
6. Hauptsession verifiziert; promovierte Findings landen in den entsprechenden State-Dateien.

## 13. MOC-Hygiene

Bei jeder neuen Knowledge-Note pruefen: passt sie ins existierende MOC, oder ist ein neuer Topic-MOC noetig? Bei MOCs mit > 50 Eintraegen: Subdivision-Vorschlag im naechsten Cleanup-Review.

## 14. Stale-Detection

Notes mit `updated > 180 Tage` und keinem Maintenance-Touch werden im naechsten Cleanup-Review zur Pruefung vorgemerkt (Default; per Adapter ueberschreibbar).

## Cross-Links

- Context-Loading: `context-policy.md`.
- Lifecycle: `file-lifecycle.md`.
- Quellen: `source-policy.md`.
- Setup: `setup-protocol.md`.
- Adapter: `adapter-policy.md`.
- Quality-Gates: `quality-gates.md`.
- Delegation: `delegation-policy.md`.
- Templates: `templates/knowledge-note.md`, `templates/moc.md`, `templates/source-note.md`, `templates/research-report.md`, `templates/data-space.md`, `templates/ingestion-record.md`, `templates/normalized-document.md`, `templates/normalization-review.md`, `templates/maintenance-routine.md`, `templates/cleanup-review.md`.
- Subdirectory-READMEs: `knowledge/README.md`, `data-space/README.md`, `archive/README.md`.

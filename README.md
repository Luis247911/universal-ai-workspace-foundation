# Universal AI Workspace Foundation

Ein striktes, domain-neutrales, kopierfertiges Markdown-Skelett fuer beliebige Projekte, die mit AI-Assistants bearbeitet werden.

## Was diese Foundation ist

- Eine Mount-Point-Disziplin gegen Parallelstrukturen.
- Ein Setup-Protokoll fuer saubere Adapter-Anbindung.
- Ein generisches Delegation-Modell ohne vordefinierte Agents.
- Ein Sicherheits-Default mit Untrusted-Default fuer externe Inhalte.
- Ein Context-Loading-Modell mit klaren Regeln (auto / on relevance / on request / never).
- Ein File-Lifecycle-Modell mit expliziten Retention-Regeln.
- Ein Markdown-Knowledge-Graph-Protokoll mit Obsidian-kompatiblen Konventionen.
- Eine Document-Normalization-Pipeline fuer externe Binaerdateien.
- Maintenance-Routine-Blueprints als optionale Spezifikationen.
- Eine Kontroll- und Managementschicht (kein Datenspeicher fuer Rohdaten).

## Was diese Foundation NICHT ist

- Kein Agent-Harness, kein Skill-Pack.
- Keine MCP-Default-Bundle, keine Hook-Sammlung.
- Kein Coding-, HR-, Legal- oder Sales-Harness.
- Kein Automatisierungs-Framework.
- Kein RAG-System, keine Vector-Datenbank, kein Crawler.
- Kein automatisiertes Binary-Parsing (kein PDF-Parser, kein OCR, kein Office-Reader, kein Bild-zu-Text-Modell).
- Kein Datenspeicher fuer sensible Rohdaten.

## Markdown-first-Prinzip

Alle internen Workspace-Artefakte sind `.md`. Externe Binaerdateien (PDF, DOCX, PPTX, XLSX, Bilder, Audio, Video) duerfen referenziert werden, niemals zur kanonischen Arbeitsfassung. Wenn ein Projekt Binaerdateien als Kunden-Export benoetigt, bleibt die `.md`-Quelle kanonisch; der Export wird nur in `state/artifact-index.md` referenziert und ersetzt niemals die `.md`-Quelle.

## Quickstart (Prompt in den Chat eines neuen Projektes kopieren)
------
PROMPT:

,,Du arbeitest in meinem aktuellen Projekt.

Bitte analysiere zuerst die vorhandene Projektstruktur:
- Welche Ordner gibt es schon?
- Wo liegen Notizen, Prompts, Agents, Docs, Wissen, Sessions oder temporäre Dateien?
- Gibt es doppelte oder unklare Strukturen?

Nutze danach dieses öffentliche GitHub-Repo als Referenz:
https://github.com/Luis247911/universal-ai-workspace-foundation

Lies besonders:
- README.md
- AGENTS.md
- install-checklist.md
- .ai-workspace/setup-protocol.md

Ziel:
Prüfe, welche Teile dieser Struktur für dieses Projekt sinnvoll sind.

Wichtig:
- Übernimm nicht blind alles.
- Lösche nichts ohne Rückfrage.
- Erstelle keine neuen Top-Level-Ordner ohne Rückfrage.
- Passe alles an die vorhandene Struktur an.
- Wenn es schon Ordner wie agents, prompts, notes, docs, wiki, skills oder tasks gibt, schlage eine saubere Migration vor.
- Erkläre erst deinen Plan, bevor du Dateien änderst.

Liefere zuerst:
1. Kurze Analyse der aktuellen Struktur.
2. Was aus dem Referenz-Repo sinnvoll übernommen werden sollte.
3. Was nicht nötig ist.
4. Einen kleinen Migrationsplan.
5. Eine Liste aller Dateien und Ordner, die du neu anlegen oder ändern würdest.

Warte danach auf meine Bestätigung."

-----
## Mount-Point-Uebersicht

| Pfad | Zweck |
|------|-------|
| `AGENTS.md`, `CLAUDE.md` | Boot-Dateien (Verhaltens-Contract) |
| `install-checklist.md` | Manuelle Setup-Anleitung |
| `.ai-workspace/` | Foundation-Kern |
| `.ai-workspace/state/` | Operativer kanonischer Zustand |
| `.ai-workspace/templates/` | Markdown-Vorlagen |
| `.ai-workspace/knowledge/` | Markdown-Knowledge-Graph |
| `.ai-workspace/data-space/` | Manifest-only Mount Point fuer externe Datenraeume |
| `.ai-workspace/research/` | Geprueftes oder zu pruefendes Material |
| `.ai-workspace/deliverables/` | Kuratierte `.md`-Outputs |
| `.ai-workspace/scratch/` | Ephemere, untrusted Arbeit |
| `.ai-workspace/archive/` | Inerte Historie |
| `.ai-workspace/adapters/` | Projektspezifische Erweiterungen |

## KG-Konzept-Kurzbeschreibung

Markdown ist das Gedaechtnis dieses Workspaces. Dauerhaftes Wissen lebt unter `knowledge/`, verbunden ueber `[[wiki-links]]`, navigierbar ueber Map-of-Content-Dateien (`_moc.md`), durch YAML-Frontmatter maschinenlesbar.

Verifiziertes normalisiertes Markdown ist die bevorzugte Arbeitsfassung. Bei kritischen Aussagen (Zahlen, Daten, Fristen, Namen, Tabellenwerte, Definitionen, Negationen, Vertragsaussagen, entscheidungsrelevante Inhalte) muss auf das Originaldokument oder die Normalization Review zurueckverwiesen werden.

## Naechste Schritte

- Lies `AGENTS.md`.
- Folge `install-checklist.md`.
- Konsultiere `.ai-workspace/README.md` fuer die vollstaendige Mount-Point-Map.
- Lies `.ai-workspace/knowledge-graph-policy.md` fuer das KG-Protokoll.

## Source-of-Truth-Hierarchie

1. Originaldokument (als Referenzquelle, in `state/source-registry.md` referenziert).
2. Deklarierter Project Data Space (extern, projektspezifisch — Foundation enthaelt nur Manifeste).
3. Verifiziertes normalisiertes Markdown (`verification_status: verified`).
4. `state/source-registry.md` und `state/artifact-index.md`.
5. Verifizierte `.md`-Knowledge-Notes und Research-Reports.

Ein optionales RAG-System ist niemals Source of Truth.

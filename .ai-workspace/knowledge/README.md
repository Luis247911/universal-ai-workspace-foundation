# knowledge/ — Markdown-Knowledge-Graph

Dieses Verzeichnis ist der primaere Mount Point fuer das menschenlesbare Langzeitgedaechtnis des Projekts. **Alle Inhalte sind `.md`** — verbunden ueber `[[wiki-links]]`, navigierbar ueber MOC-Dateien, durch YAML-Frontmatter maschinenlesbar.

## Was hier wohnt

- Knowledge-Notes (`.md` aus `templates/knowledge-note.md`).
- MOCs (Map of Content; `.md` aus `templates/moc.md`):
  - Root-MOC: `_index.md`.
  - Topic-MOCs: `<topic>/_moc.md`.
- Verifizierte Normalized-Documents nach Promotion aus `research/`.

## Verzeichnis-Struktur

```text
knowledge/
  README.md                 # diese Datei
  _index.md                 # Root-MOC (falls KG aktiv)
  <topic-1>/
    _moc.md                 # Topic-MOC
    <slug-1>.md             # Knowledge-Note
    <slug-2>.md
  <topic-2>/
    _moc.md
    ...
```

## Naming-Konvention

ASCII, kebab-case, ohne Whitespaces, ohne Umlaute. Topic-Verzeichnisse mit kurzen, generischen Namen.

## Link-Disziplin

- `[[wiki-link]]` fuer KG-interne Verbindungen.
- `[label](pfad)` fuer Verweise auf Nicht-KG-Knoten (z.B. State-Dateien, Adapter-Inhalte).
- Semantischer Beziehungs-Kontext begleitet jeden bedeutungstragenden Link.
- Geplante, aber noch nicht existierende Links: Ziel-Note als Stub mit Frontmatter `status: planned` anlegen.
- Tote Links nicht stillschweigend entfernen — als `status: planned` markieren oder im naechsten Cleanup-Review erfassen.

## Lifecycle

- Knowledge-Notes werden **updated, nicht promoted**. Status `superseded` oder `archived` markieren statt loeschen.
- Archivierte Notes wandern nach `archive/YYYY-MM-DD-<slug>.md`.
- Stale-Trigger: 180 Tage ohne Maintenance-Touch -> im naechsten Cleanup-Review pruefen.

## Lade-Regel (`Load on Relevance` fuer MOCs, `Load on Explicit Request` fuer einzelne Notes)

Bei Wissens- oder Konzept-Anfragen:

1. Lies zuerst `_index.md` (Root-MOC).
2. Identifiziere relevante Topic-MOCs (`<topic>/_moc.md`).
3. Folge selektiv `[[wiki-links]]` zu konkreten Knowledge-Notes.
4. Lade nicht den ganzen Graphen blind.

Siehe `context-policy.md` Section 3 und `knowledge-graph-policy.md` Section 8.

## Beziehung zu State-Dateien

KG referenziert State (z.B. `[[D-YYYY-MM-DD-NN]]` fuer Decisions, `[[Q-YYYY-MM-DD-NN]]` fuer Open-Questions), **ersetzt** State aber niemals. State-Dateien sind kanonisch.

## Beziehung zu Project Data Space und RAG

Knowledge-Notes koennen Pointer auf Original-Binaerdateien (via Source-Registry-IDs) und auf Data-Space-Manifeste enthalten. **RAG ist (falls existent) nur Suchlayer ueber dem KG**, niemals Source of Truth.

## Cross-Links

- KG-Policy: `../knowledge-graph-policy.md`.
- Knowledge-Note-Template: `../templates/knowledge-note.md`.
- MOC-Template: `../templates/moc.md`.
- Source-Note-Template: `../templates/source-note.md`.
- Quality-Gates: `../quality-gates.md`.
- Source-Registry: `../state/source-registry.md`.

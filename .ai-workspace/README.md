# `.ai-workspace/` — Mount-Point-Map

Diese Datei ist eine reine Routing-Funktion. Sie erklaert, was unter `.ai-workspace/` lebt, ohne Policy-Inhalt zu duplizieren. Detail-Regeln stehen in den jeweiligen Policy-Dateien.

## Konvention

`.ai-workspace/` ist der Foundation-Kern eines Projekts, das diese Foundation kopiert hat. Alle Foundation-Artefakte sind `.md`-Dateien. Das Verzeichnis ist nicht versionsspezifisch und kann unveraendert in beliebige Projekte kopiert werden.

## Top-Level-Inhalt

| Pfad | Zweck | Lifecycle | Lade-Regel |
|------|-------|-----------|------------|
| `README.md` (diese Datei) | Mount-Point-Map | statisch | Load on Relevance |
| `protocol.md` | Kanonische Behavior-Datei | statisch | Load on Relevance |
| `setup-protocol.md` | New-Project-Setup-Flow + Anti-Parallel-Regel | statisch | Load on Relevance |
| `session-contract.md` | Session-Lifecycle (Start/Work/Handoff/Resume) | statisch | Load on Relevance |
| `context-policy.md` | Lade-Regeln pro Pfad | statisch | Load on Relevance |
| `file-lifecycle.md` | Wo wohnt welcher Artefakttyp | statisch | Load on Relevance |
| `source-policy.md` | Externe Quellen-Behandlung + Trust-Levels | statisch | Load on Relevance |
| `security-policy.md` | Untrusted-Content + Secrets + Execution-Boundaries | statisch | Load on Relevance |
| `delegation-policy.md` | Generische Regeln fuer delegierte Arbeit | statisch | Load on Relevance |
| `adapter-policy.md` | Adapter-Vertrag + Boundaries | statisch | Load on Relevance |
| `quality-gates.md` | Verifikationsstufen | statisch | Load on Relevance |
| `knowledge-graph-policy.md` | Markdown-KG, Wiki-Links, Frontmatter, MOC, Document Normalization, Maintenance Blueprints | statisch | Load on Relevance |
| `state/` | Operativer kanonischer Zustand | live | siehe Subdirektive |
| `templates/` | Markdown-Vorlagen | statisch | Load on Explicit Request |
| `knowledge/` | Markdown-Knowledge-Graph | durable | MOC-first, dann selektiv |
| `data-space/` | Manifest-only Mount Point fuer externe Datenraeume | durable Manifest | Load on Relevance bei aktivem Data-Space |
| `research/` | Geprueftes oder zu pruefendes Material | retentions-getriggert | Load on Explicit Request |
| `deliverables/` | Kuratierte `.md`-Outputs | durable | Load on Explicit Request |
| `scratch/` | Ephemere, untrusted Arbeit | 7 Tage | Never Auto-Load |
| `archive/` | Inerte Historie | immutable | Never Auto-Load (ausser Anfrage) |
| `adapters/` | Projektspezifische Erweiterungen | adapterspezifisch | nur aktive Adapter, registriert in `state/project-index.md` |

## Markdown-only-Regel

Alle Dateien innerhalb dieses Verzeichnisses sind `.md`. Keine `.json`, `.yaml`, `.yml`, `.txt`, `.template`, `.sh`, `.ps1`, `.py`, `.js`, `.ts`, `.exe` oder Binaerdateien. Externe Binaerdateien werden ueber `state/source-registry.md` referenziert; ihre Inhalte werden ueber die Document-Normalization-Pipeline in `.md` ueberfuehrt (siehe `knowledge-graph-policy.md`).

## Boot-Set

Vier Dateien werden beim Session-Start automatisch wahrgenommen:

1. `../AGENTS.md`
2. `../CLAUDE.md` (falls Tool = Claude)
3. `state/project-index.md`
4. `state/current-session.md`

Alles andere wird auf Relevanz, auf Anfrage oder gar nicht geladen. Siehe `context-policy.md`.

## Verbotene Top-Level-Verzeichnisse

`.ai-workspace/` enthaelt keine Verzeichnisse mit folgenden Namen: `agents/`, `skills/`, `commands/`, `hooks/`, `tasks/`, `responses/`, `runs/`, `memory/`, `sessions/`, `workflows/`, `prompts/`, `notes/`, `docs/`, `ai/`, `claude-system/`, `agent-system/`, `harness/`, `workspace/`, `context/`, `project-state/`, `wiki/`, `vector/`, `embeddings/`, `index/`, `rag/`, `cache/`, `logs/`, `infra/`, `mcp/`. Falls Aequivalente noetig sind, leben sie als Substruktur unter `adapters/<slug>/`. Siehe `setup-protocol.md`.

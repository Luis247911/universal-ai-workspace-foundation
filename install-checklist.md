# Install-Checklist — Foundation in ein neues Projekt kopieren

Diese Checkliste ist fuer den Menschen gedacht, der die Foundation kopiert und ein neues Projekt initialisiert. Sie enthaelt keinen ausfuehrbaren Code. Jeder Schritt wird manuell ausgefuehrt und bestaetigt.

## Pre-Copy-Checks

- [ ] Zielprojektverzeichnis existiert und ist leer oder enthaelt kein bestehendes `.ai-workspace/`.
- [ ] Kein bereits existierendes Workspace-System neben dem geplanten Ziel (kein paralleles `agents/`, `prompts/`, `memory/`, `wiki/` etc.).
- [ ] Klar, dass dies ein domain-neutrales Skelett ist und Domain-Inhalte ueber Adapter ergaenzt werden.

## Copy-Schritte

- [ ] Kopiere den Inhalt des Foundation-Verzeichnisses in das Zielprojektverzeichnis.
- [ ] Verzeichnisstruktur:
  - `AGENTS.md`, `CLAUDE.md`, `README.md`, `install-checklist.md` im Root.
  - `.ai-workspace/` mit Subdirektoren `state/`, `templates/`, `knowledge/`, `data-space/`, `research/`, `deliverables/`, `scratch/`, `archive/`, `adapters/`.
  - Alle Dateien innerhalb `.ai-workspace/` haben `.md`-Endung.
- [ ] Keine Datei mit Endung `.json`, `.yaml`, `.yml`, `.txt`, `.template`, `.sh`, `.ps1`, `.py`, `.js`, `.ts`, `.exe` aus dem Foundation-Tree mitgenommen.

## Initiale Befuellung

- [ ] `.ai-workspace/state/project-index.md` ausfuellen unter Verwendung von `.ai-workspace/templates/project-brief.md` als Vorlage. Mindestens Slug, Zweck, Scope, Goals, Owner.
- [ ] `.ai-workspace/state/current-session.md` initialisieren unter Verwendung von `.ai-workspace/templates/session-state.md`. Active-Task = "Initial setup", Status = `in_progress`.
- [ ] `.ai-workspace/state/decisions.md` als leeren Append-only-Log mit Kopfzeile vorbereiten.
- [ ] `.ai-workspace/state/open-questions.md`, `assumptions.md`, `risks-and-constraints.md`, `source-registry.md`, `artifact-index.md` als leere Stubs vorbereiten.

## Ignore-Files (manuell)

- [ ] Aus `.ai-workspace/templates/gitignore-template.md` die empfohlenen Patterns extrahieren und in eine projektspezifische `.gitignore`-Datei im Projekt-Root kopieren. **Hinweis:** Die Foundation-Datei ist eine Markdown-Anleitung; sie ist kein aktives Ignore-File.
- [ ] Aus `.ai-workspace/templates/claudeignore-template.md` die empfohlenen Patterns extrahieren und in eine projektspezifische `.claudeignore`-Datei im Projekt-Root kopieren.
- [ ] Projekt-spezifische zusaetzliche Patterns ergaenzen.

## Erste Adapter-Entscheidung

- [ ] Entscheide, ob das Projekt sofort einen Adapter braucht.
- [ ] Wenn ja: lege `.ai-workspace/adapters/<slug>/adapter.md` aus `.ai-workspace/templates/adapter-readme.md` an. Trage in `.ai-workspace/state/project-index.md` Sektion "Aktive Adapter" ein.
- [ ] Wenn nein: dokumentiere die Verzichts-Entscheidung in `.ai-workspace/state/decisions.md`.

## Vier Setup-Fragen aus `setup-protocol.md`

### Frage 1: Markdown-Knowledge-Graph aktivieren?

- [ ] Antwort entschieden (ja / nein).
- [ ] Bei ja: `.ai-workspace/knowledge/_index.md` aus `.ai-workspace/templates/moc.md` als Root-MOC anlegen. In `state/project-index.md` Sektion "Knowledge-Graph-Aktivierung" als aktiv markieren.
- [ ] Bei nein: Verzicht in `state/decisions.md` festhalten.

### Frage 2: Project Data Space deklarieren?

- [ ] Antwort entschieden (ja / nein, ggf. mehrere Spaces).
- [ ] Bei ja: pro Data Space ein `.ai-workspace/data-space/<datum>-<slug>.md` aus `.ai-workspace/templates/data-space.md` anlegen. Eintrag in `state/source-registry.md` mit `type: data-space`.
- [ ] Bei nein: Verzicht in `state/decisions.md` festhalten.

### Frage 3: Maintenance Routine Blueprints adoptieren?

- [ ] Antwort entschieden (ja / nein, ggf. welche).
- [ ] Bei ja: in einem Adapter (`adapters/<slug>/maintenance/<routine-name>.md`) mit `.ai-workspace/templates/maintenance-routine.md` registrieren. Als Auswahl-Hilfe dienen die universellen Blueprints im Plan (Section 5.6.5: knowledge-graph-lint, knowledge-graph-sync, session-memory-review, source-artifact-hygiene, adapter-lifecycle-review, document-normalization-review, optional session-snapshot-export).
- [ ] Bei nein: Verzicht in `state/decisions.md` festhalten.

### Frage 4: Externe Binaerinputs erwartet, die normalisiert werden muessen?

- [ ] Antwort entschieden (ja / nein).
- [ ] Bei ja: Document-Normalization-Plan in `state/decisions.md` festhalten. Erste Normalization-Records vorbereiten via `.ai-workspace/templates/normalized-document.md` und `.ai-workspace/templates/normalization-review.md` (sobald erste Binaeren vorliegen).
- [ ] Bei nein: Verzicht in `state/decisions.md` festhalten.

## Setup-Artefakte registrieren

- [ ] Alle erzeugten Setup-Artefakte (project-index.md, current-session.md, decisions.md erste Eintraege, evtl. neu erzeugte MOCs/Data-Space-Manifeste) in `.ai-workspace/state/artifact-index.md` mit Status `active` eintragen.

## Setup-Session-Summary

- [ ] `current-session.md` enthaelt am Ende:
  - Liste angelegter Setup-Decisions (D-IDs)
  - Liste offener Setup-Questions (Q-IDs)
  - Liste registrierter Setup-Artefakte (Pfade)
  - Liste aktiver Adapter (oder "keiner")
  - Liste aktiver Maintenance-Routinen (oder "keine")
  - KG-Aktivierungsstatus
  - Data-Space-Status
  - Document-Normalization-Status
  - Resume-Anweisung fuer naechste Arbeitssession

## Verifikation

- [ ] `AGENTS.md` und `CLAUDE.md` als Boot-Dateien vorhanden.
- [ ] `state/project-index.md` und `state/current-session.md` befuellt.
- [ ] Keine Parallelstruktur ausserhalb der Foundation-Mount-Points entstanden.
- [ ] Alle Foundation-Dateien haben `.md`-Endung.
- [ ] Keine Originalbinaerdateien im Foundation-Tree (Originale leben extern oder im deklarierten Project Data Space).
- [ ] Keine Secrets im Foundation-Tree.

Setup abgeschlossen, sobald alle Boxen oben angekreuzt sind. Naechste reale Arbeitssession kann starten und mit dem Boot-Order aus `AGENTS.md` beginnen.

# Install-Checklist — Foundation in ein neues Projekt kopieren

Diese Checkliste ist für den Menschen gedacht, der die Foundation kopiert und ein neues Projekt initialisiert. Sie enthält keinen ausführbaren Code. Jeder Schritt wird manuell ausgeführt und bestätigt.

## Geführtes Onboarding mit Claude Code (Alternative)

Statt die Schritte unten manuell abzuarbeiten, kannst du die Foundation auch von Claude Code anbinden lassen. Besonders für ein **bestehendes Projekt** mit eigener Ordnerstruktur.

- **Foundation schon kopiert / `.claude/` vorhanden?** Führe in deinem Projekt `/onboard` aus (`.claude/commands/onboard.md`). Der Befehl analysiert deine Struktur, entscheidet mit dir Governance-only vs. +Execution, liefert einen Migrationsplan und fragt nach, bevor er etwas ändert.
- **Noch nichts installiert (Kalt-Start ohne Klonen)?** Öffne dein Projekt in Claude Code und gib diesen Prompt ein. Er liest dieses öffentliche Repo nur als Referenz und kopiert/installiert nichts:

```text
Du arbeitest in meinem aktuellen Projekt und sollst prüfen, ob und wie es sich an der
Universal AI Workspace Foundation (v3.0) ausrichten lässt.

Die Foundation hat ZWEI Schichten - wir entscheiden gemeinsam, welche dieses Projekt braucht:
- Governance (.ai-workspace/, reines Markdown): Regeln, Zustand, Wissen. Fast immer sinnvoll.
- Execution (.claude/ + src/harness/, Python): 12 Claude-Code-Skills über einer
  pip-installierbaren Engine (Evals, Guardrails, Tracing, HITL, Routing, Memory,
  Orchestrierung). Nur wenn das Projekt sie wirklich nutzt.

Schritt 1 - Analysiere die vorhandene Projektstruktur (Ordner; wo Notizen/Prompts/Agents/Docs/
Wissen/Sessions/Code/Temp liegen; doppelte oder unklare Strukturen).
Schritt 2 - Nutze dieses öffentliche Repo als Referenz (nur lesen, nichts klonen/installieren):
https://github.com/Luis247911/universal-ai-workspace-foundation
Lies: README.md, AGENTS.md (Paragraph 2.5, 3), install-checklist.md, install-harness.md (nur falls
relevant), .ai-workspace/setup-protocol.md (Paragraph 3 Frage 0 + Paragraph 2 vier Setup-Fragen).
Schritt 3 - Entscheide MIT MIR: nur Governance, oder auch Execution? Begründe anhand Schritt 1.

Regeln (nicht verhandelbar): nichts blind übernehmen; nichts ohne Rückfrage löschen; keine
neuen Top-Level-Ordner ohne Rückfrage (Anti-Sprawl - einziger Code-Mount .claude/, sonst
src/tests/examples); vorhandene Ordner (agents/prompts/notes/docs/wiki/skills/tasks) sauber
migrieren statt Parallelstruktur; erst Plan erklären, dann ändern.

Liefere zuerst (noch nichts anlegen): 1. Analyse. 2. Empfehlung Governance-only vs. +Execution
(begründet). 3. Was übernehmen. 4. Was nicht. 5. Schrittweiser Migrationsplan (Governance
zuerst, Execution optional). 6. Liste neu/geändert. Warte danach auf meine Bestätigung.
```

Die manuelle Variante (für einen sauberen Start in einem leeren Projekt) folgt unten.

## Pre-Copy-Checks

- [ ] Zielprojektverzeichnis existiert und ist leer oder enthält kein bestehendes `.ai-workspace/`.
- [ ] Kein bereits existierendes Workspace-System neben dem geplanten Ziel (kein paralleles `agents/`, `prompts/`, `memory/`, `wiki/` etc.).
- [ ] Klar, dass dies ein domain-neutrales Skelett ist und Domain-Inhalte über Adapter ergänzt werden.

## Copy-Schritte

- [ ] Kopiere den Inhalt des Foundation-Verzeichnisses in das Zielprojektverzeichnis.
- [ ] Verzeichnisstruktur:
  - `AGENTS.md`, `CLAUDE.md`, `README.md`, `install-checklist.md` im Root.
  - `.ai-workspace/` mit Subdirektoren `state/`, `templates/`, `knowledge/`, `data-space/`, `research/`, `deliverables/`, `scratch/`, `archive/`, `adapters/`.
  - **Alle Dateien innerhalb `.ai-workspace/` haben `.md`-Endung** (die Governance-Schicht ist markdown-only — diese Regel ist unverändert strikt).
- [ ] Keine Nicht-Markdown-Datei (`.json`, `.yaml`, `.py`, `.sh`, ...) **innerhalb `.ai-workspace/`**. Solche Dateien gehören nie in die Governance-Schicht.

### Optional: die lauffähige Harness-Schicht

Dieses Repo kann die Execution-Schicht mitliefern (siehe `AGENTS.md` §2.5): `.claude/` (Skills/Hooks/Commands), die Engine `src/harness/`, `tests/`, `examples/`, `pyproject.toml`, `.github/`. Das ist **echter Code** und damit bewusst **nicht** markdown-only.

- [ ] Entscheide, ob das neue Projekt den Harness mitnimmt. Reine Governance-Nutzung (nur `.ai-workspace/`) ist weiterhin möglich.
- [ ] Falls ja: die Harness-Schicht als Einheit kopieren und gemäß `install-harness.md` installieren (`pip install -e .` zieht null Third-Party-Wheels; Extras sind opt-in).
- [ ] Falls nein: nur `.ai-workspace/` + die Root-Governance-Dateien kopieren — die o.g. Markdown-only-Prüfung gilt dann für das gesamte kopierte Set.

## Initiale Befüllung

- [ ] `.ai-workspace/state/project-index.md` ausfüllen unter Verwendung von `.ai-workspace/templates/project-brief.md` als Vorlage. Mindestens Slug, Zweck, Scope, Goals, Owner.
- [ ] `.ai-workspace/state/current-session.md` initialisieren unter Verwendung von `.ai-workspace/templates/session-state.md`. Active-Task = "Initial setup", Status = `in_progress`.
- [ ] `.ai-workspace/state/decisions.md` als leeren Append-only-Log mit Kopfzeile vorbereiten.
- [ ] `.ai-workspace/state/open-questions.md`, `assumptions.md`, `risks-and-constraints.md`, `source-registry.md`, `artifact-index.md` als leere Stubs vorbereiten.

## Ignore-Files (manuell)

- [ ] Aus `.ai-workspace/templates/gitignore-template.md` die empfohlenen Patterns extrahieren und in eine projektspezifische `.gitignore`-Datei im Projekt-Root kopieren. **Hinweis:** Die Foundation-Datei ist eine Markdown-Anleitung; sie ist kein aktives Ignore-File.
- [ ] Aus `.ai-workspace/templates/claudeignore-template.md` die empfohlenen Patterns extrahieren und in eine projektspezifische `.claudeignore`-Datei im Projekt-Root kopieren.
- [ ] Projekt-spezifische zusätzliche Patterns ergänzen.

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

### Frage 4: Externe Binärinputs erwartet, die normalisiert werden müssen?

- [ ] Antwort entschieden (ja / nein).
- [ ] Bei ja: Document-Normalization-Plan in `state/decisions.md` festhalten. Erste Normalization-Records vorbereiten via `.ai-workspace/templates/normalized-document.md` und `.ai-workspace/templates/normalization-review.md` (sobald erste Binären vorliegen).
- [ ] Bei nein: Verzicht in `state/decisions.md` festhalten.

## Setup-Artefakte registrieren

- [ ] Alle erzeugten Setup-Artefakte (project-index.md, current-session.md, decisions.md erste Einträge, evtl. neu erzeugte MOCs/Data-Space-Manifeste) in `.ai-workspace/state/artifact-index.md` mit Status `active` eintragen.

## Setup-Session-Summary

- [ ] `current-session.md` enthält am Ende:
  - Liste angelegter Setup-Decisions (D-IDs)
  - Liste offener Setup-Questions (Q-IDs)
  - Liste registrierter Setup-Artefakte (Pfade)
  - Liste aktiver Adapter (oder "keiner")
  - Liste aktiver Maintenance-Routinen (oder "keine")
  - KG-Aktivierungsstatus
  - Data-Space-Status
  - Document-Normalization-Status
  - Resume-Anweisung für nächste Arbeitssession

## Verifikation

- [ ] `AGENTS.md` und `CLAUDE.md` als Boot-Dateien vorhanden.
- [ ] `state/project-index.md` und `state/current-session.md` befüllt.
- [ ] Keine Parallelstruktur ausserhalb der Foundation-Mount-Points entstanden (Harness-Ausnahme `.claude/` + Infra-Allowlist siehe `setup-protocol.md` §4).
- [ ] Alle Dateien innerhalb `.ai-workspace/` haben `.md`-Endung (Governance-Schicht markdown-only).
- [ ] Keine Originalbinärdateien im `.ai-workspace/`-Tree (Originale leben extern oder im deklarierten Project Data Space).
- [ ] Keine Secrets im gesamten Tree (auch nicht in `.claude/` oder `src/`).

Setup abgeschlossen, sobald alle Boxen oben angekreuzt sind. Nächste reale Arbeitssession kann starten und mit dem Boot-Order aus `AGENTS.md` beginnen.

# Install-Checklist — Foundation in ein neues Projekt kopieren

**Der automatische Weg ist `adopt`** (README, Weg B): Der Starter-Prompt holt die Foundation in ein Temp-Verzeichnis und ruft `python3 <klon>/.claude/uaw/mdm.py adopt <projekt> [--dry-run]` auf. Alle mit **[adopt]** markierten Schritte unten erledigt dieser Befehl idempotent. Er überschreibt nichts, was das Projekt besitzt, und meldet Abweichungen. Diese Checkliste bleibt die manuelle Referenz, und die übrigen Schritte (Setup-Fragen, Adapter, Projekt-Index) führt das Onboarding mit dir durch.

Sie ist für den Menschen gedacht, der die Foundation kopiert und ein neues Projekt initialisiert. Jeder Schritt wird manuell ausgeführt und bestätigt.

## Pre-Copy-Checks

- [ ] Zielprojektverzeichnis existiert und ist leer oder enthält kein bestehendes `.ai-workspace/`.
- [ ] Kein bereits existierendes Workspace-System neben dem geplanten Ziel (kein paralleles `agents/`, `prompts/`, `memory/`, `wiki/` etc.).
- [ ] Klar, dass dies ein domain-neutrales Skelett ist und Domain-Inhalte über Adapter ergänzt werden.

## Copy-Schritte

- [ ] **[adopt]** Kopiere den Inhalt des Foundation-Verzeichnisses in das Zielprojektverzeichnis (adopt: nur Policies, Vorlagen, Mount-READMEs und State-Stubs; nicht die Notizen, Journale und das Archiv der Foundation selbst).
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
- [ ] **[Hook]** `.ai-workspace/state/now.md` anlegen aus `.ai-workspace/templates/session-state.md` (gitignored; der Hook `now_init` legt sie beim ersten Start an; eine alte `current-session.md` uebernimmt **[adopt]** per `now migrate`). Aktive Aufgabe = "Initial setup", Status = `in_progress`.
- [ ] **[adopt]** `.ai-workspace/state/now.md` in das projektspezifische `.gitignore` aufnehmen (siehe `gitignore-template.md`); dazu `merge=union` fuer die generierten Dateien in `.gitattributes`.
- [ ] **[adopt]** `.ai-workspace/state/source-registry.md` und `artifact-index.md` als leere Stubs vorbereiten.
- [ ] **[adopt]** Gedaechtnis-Hooks, Skills `merken`/`pflege`, Engine-Kopie `.claude/uaw/` und `"autoMemoryEnabled": false` in `.claude/settings.json` (zusammengefuehrt, eigene Hooks bleiben). Alte Register (`state/decisions.md` usw.) werden Notizen (**[adopt]** `split-decisions`, Original im Archiv), Auto-Memory kommt auf Wunsch als Journal-Kandidat (`--import-automemory`).
- [ ] Entscheidungen, offene Fragen, Annahmen und Risiken entstehen als eine Notiz pro Datei unter `.ai-workspace/knowledge/decision/` bzw. `knowledge/question/` (`python -m harness.mdmemory new decision "<titel>"` bzw. `new question "<titel>"`; ohne Harness von Hand aus `.ai-workspace/templates/knowledge-note.md`). `state/decisions.md`, `open-questions.md`, `assumptions.md`, `risks-and-constraints.md` sowie `knowledge/INDEX.md` und `knowledge/_typen/` werden **nicht** von Hand angelegt — sie sind generiert (`python -m harness.mdmemory index`).

## Ignore-Files (manuell)

- [ ] Aus `.ai-workspace/templates/gitignore-template.md` die empfohlenen Patterns extrahieren und in eine projektspezifische `.gitignore`-Datei im Projekt-Root kopieren. **Hinweis:** Die Foundation-Datei ist eine Markdown-Anleitung; sie ist kein aktives Ignore-File.
- [ ] Aus `.ai-workspace/templates/claudeignore-template.md` die empfohlenen Patterns extrahieren und in eine projektspezifische `.claudeignore`-Datei im Projekt-Root kopieren.
- [ ] Projekt-spezifische zusätzliche Patterns ergänzen.

## Erste Adapter-Entscheidung

- [ ] Entscheide, ob das Projekt sofort einen Adapter braucht.
- [ ] Wenn ja: lege `.ai-workspace/adapters/<slug>/adapter.md` aus `.ai-workspace/templates/adapter-readme.md` an. Trage in `.ai-workspace/state/project-index.md` Sektion "Aktive Adapter" ein.
- [ ] Wenn nein: dokumentiere die Verzichts-Entscheidung als Decision-Notiz unter `.ai-workspace/knowledge/decision/`.

## Vier Setup-Fragen aus `setup-protocol.md`

### Frage 1: Markdown-Knowledge-Graph aktivieren?

- [ ] Antwort entschieden (ja / nein).
- [ ] Bei ja: `.ai-workspace/knowledge/_index.md` aus `.ai-workspace/templates/moc.md` als Root-MOC anlegen. In `state/project-index.md` Sektion "Knowledge-Graph-Aktivierung" als aktiv markieren.
- [ ] Bei nein: Verzicht als Decision-Notiz unter `.ai-workspace/knowledge/decision/` festhalten.

### Frage 2: Project Data Space deklarieren?

- [ ] Antwort entschieden (ja / nein, ggf. mehrere Spaces).
- [ ] Bei ja: pro Data Space ein `.ai-workspace/data-space/<datum>-<slug>.md` aus `.ai-workspace/templates/data-space.md` anlegen. Eintrag in `state/source-registry.md` mit `type: data-space`.
- [ ] Bei nein: Verzicht als Decision-Notiz unter `.ai-workspace/knowledge/decision/` festhalten.

### Frage 3: Maintenance Routine Blueprints adoptieren?

- [ ] Antwort entschieden (ja / nein, ggf. welche).
- [ ] Bei ja: in einem Adapter (`adapters/<slug>/maintenance/<routine-name>.md`) mit `.ai-workspace/templates/maintenance-routine.md` registrieren. Als Auswahl-Hilfe dienen die universellen Blueprints im Plan (Section 5.6.5: knowledge-graph-lint, knowledge-graph-sync, session-memory-review, source-artifact-hygiene, adapter-lifecycle-review, document-normalization-review, optional session-snapshot-export).
- [ ] Bei nein: Verzicht als Decision-Notiz unter `.ai-workspace/knowledge/decision/` festhalten.

### Frage 4: Externe Binärinputs erwartet, die normalisiert werden müssen?

- [ ] Antwort entschieden (ja / nein).
- [ ] Bei ja: Document-Normalization-Plan als Decision-Notiz unter `.ai-workspace/knowledge/decision/` festhalten. Erste Normalization-Records vorbereiten via `.ai-workspace/templates/normalized-document.md` und `.ai-workspace/templates/normalization-review.md` (sobald erste Binären vorliegen).
- [ ] Bei nein: Verzicht als Decision-Notiz unter `.ai-workspace/knowledge/decision/` festhalten.

## Setup-Artefakte registrieren

- [ ] **[Hook]** `python3 .claude/uaw/mdm.py index` ausführen, nachdem alle Setup-Notizen angelegt sind (mit Hooks erledigt das `index_refresh` nach jeder Notiz) (erzeugt `knowledge/INDEX.md` und die Register-Sichten unter `state/`).
- [ ] Alle erzeugten Setup-Artefakte (project-index.md, erste Decision-Notizen, evtl. neu erzeugte MOCs/Data-Space-Manifeste) in `.ai-workspace/state/artifact-index.md` mit Status `active` eintragen.

## Setup-Session-Summary

- [ ] Das Journal der Setup-Session (`.ai-workspace/journal/`) enthält am Ende einen Eintrag `ergebnis` mit:
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

- [ ] Die fünf Boot-Dateien vorhanden: `AGENTS.md`, `CLAUDE.md`, `state/project-index.md`, `state/now.md`, `knowledge/INDEX.md` (generiert).
- [ ] `state/project-index.md` befüllt; `state/now.md` lokal vorhanden und gitignored.
- [ ] Keine Parallelstruktur ausserhalb der Foundation-Mount-Points entstanden (Harness-Ausnahme `.claude/` + Infra-Allowlist siehe `setup-protocol.md` §4).
- [ ] Alle Dateien innerhalb `.ai-workspace/` haben `.md`-Endung (Governance-Schicht markdown-only).
- [ ] Keine Originalbinärdateien im `.ai-workspace/`-Tree (Originale leben extern oder im deklarierten Project Data Space).
- [ ] Keine Secrets im gesamten Tree (auch nicht in `.claude/` oder `src/`).

Setup abgeschlossen, sobald alle Boxen oben angekreuzt sind. Nächste reale Arbeitssession kann starten und mit dem Boot-Order aus `AGENTS.md` beginnen.

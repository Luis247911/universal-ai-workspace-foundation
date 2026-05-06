# setup-protocol.md — New-Project-Setup-Flow + Anti-Parallel-Regel

Diese Datei ist die kritische Stelle, an der entschieden wird, ob ein neues Projekt sauber an die Foundation andockt oder ob Parallelstrukturen entstehen. Setup wird manuell durchgefuehrt; die Foundation enthaelt keine Auto-Setup-Skripte.

## 1. New-Project-Setup-Flow

Lineare Schritte:

1. **Pre-Check.** Foundation in leeres oder neu-initialisiertes Projektverzeichnis kopieren. Falls bereits ein `.ai-workspace/` existiert: Setup abbrechen und Konflikt eskalieren.
2. **`state/project-index.md`** befuellen aus `templates/project-brief.md` — mindestens Slug, Zweck, Scope, Goals, Owner.
3. **`state/current-session.md`** initialisieren aus `templates/session-state.md` — Active-Task = "Initial setup", Status = `in_progress`.
4. **Setup-Decisions** in `state/decisions.md` festhalten (z.B. "Wir starten ohne Adapter", "Datenraum wird extern gehalten").
5. **Setup-Open-Questions** in `state/open-questions.md` festhalten.
6. **Setup-Risks** in `state/risks-and-constraints.md` festhalten (z.B. wenn Projekt regulierte Daten beruehrt).
7. **Ignore-Files** aus `templates/gitignore-template.md` und `templates/claudeignore-template.md` ableiten und ins Projekt-Root kopieren (manuell). Foundation-Core enthaelt keine aktiven Ignore-Files.
8. **Adapter-Entscheidung.** Wenn Adapter sofort noetig: `adapters/<slug>/adapter.md` aus `templates/adapter-readme.md` anlegen + in `state/project-index.md` Sektion "Aktive Adapter" eintragen. Sonst: spaeter entscheiden, Verzicht in `decisions.md`.
9. **Vier KG/Data-Space/Maintenance/Normalization-Setup-Fragen** (Section 2 dieser Datei).
10. **Setup-Artefakte registrieren** in `state/artifact-index.md`.
11. **Setup-Session-Summary** in `current-session.md` schreiben, Status auf `done` fuer die Initial-Setup-Phase.

## 2. Vier Setup-Fragen

Diese vier Fragen werden im Setup beantwortet. Die Antworten landen in `state/decisions.md`.

### Frage 1: Markdown-Knowledge-Graph aktivieren?

- **Ja:** `knowledge/_index.md` aus `templates/moc.md` als Root-MOC anlegen. In `state/project-index.md` Sektion "Knowledge-Graph-Aktivierung" als aktiv markieren. Erste Topic-MOCs koennen spaeter folgen.
- **Nein:** Verzicht in `decisions.md` festhalten. `knowledge/`-Verzeichnis bleibt leer ausser `README.md`.

### Frage 2: Project Data Space deklarieren?

- **Ja:** Pro Data Space ein `data-space/<datum>-<slug>.md` aus `templates/data-space.md`. Eintrag in `state/source-registry.md` mit `type: data-space`. Originaldaten leben **extern** oder im projektspezifisch deklarierten Speicherort, nicht im Foundation-Tree. Manifest enthaelt nur Pointer + Sensitivity + Allowed-Processing.
- **Nein:** Verzicht in `decisions.md` festhalten.

### Frage 3: Maintenance-Routine-Blueprints adoptieren?

- **Ja:** In einem Adapter (`adapters/<slug>/maintenance/<routine-name>.md`) mit `templates/maintenance-routine.md` registrieren. Universelle Blueprints stehen als Auswahl-Hilfe zur Verfuegung (knowledge-graph-lint, knowledge-graph-sync, session-memory-review, source-artifact-hygiene, adapter-lifecycle-review, document-normalization-review, optional session-snapshot-export). Aktivierung erst nach explizitem User-Aktivierungs-Schritt pro Routine.
- **Nein:** Verzicht in `decisions.md` festhalten.

### Frage 4: Externe Binaerinputs erwartet?

- **Ja:** Document-Normalization-Plan in `decisions.md` festhalten. Pro erwartetem Binaer-Typ (PDF/DOCX/PPTX/XLSX/Bild/Audio/Video) Sensitivity-Default und Allowed-Processing-Default in `decisions.md` deklarieren. Erste Ingestion-Records werden via `templates/normalized-document.md` und `templates/normalization-review.md` angelegt, sobald Inputs vorliegen.
- **Nein:** Verzicht in `decisions.md` festhalten.

## 3. Mount-Point-Decision-Tree (vor jeder Strukturerstellung)

Bevor irgendein neues Verzeichnis oder eine neue Datei ausserhalb bestehender Mount-Points angelegt wird, durchlaufe diese Reihenfolge:

```text
Frage 1: Gehoert das nach state/?              -> Ja: dorthin. Stop.
Frage 2: Gehoert das nach adapters/<slug>/?    -> Ja: dort einbauen. Stop.
Frage 3: Gehoert das nach research/?           -> Ja: dorthin. Stop.
Frage 4: Gehoert das nach deliverables/?       -> Ja: dorthin. Stop.
Frage 5: Gehoert das nach scratch/?            -> Ja: dorthin. Stop.
Frage 6: Gehoert das nach archive/?            -> Ja: dorthin. Stop.
Frage 7: Gehoert das nach knowledge/?          -> Ja: dorthin. Stop.
Frage 8: Gehoert das nach data-space/?         -> Ja (nur als .md-Manifest). Stop.
Frage 9: Gehoert das nach templates/?          -> Ja (nur bei Foundation-Erweiterung). Stop.
Sonst:   STOPPE. Frage den User. Lege keinen neuen Top-Level-Ordner ohne
         Erlaubnis an. Wenn neuer Ort genehmigt: dokumentiere die Begruendung
         in state/decisions.md.
```

## 4. Verbotene Top-Level-Verzeichnisnamen

Diese Verzeichnisnamen duerfen nicht als Foundation-Top-Level-Ordner entstehen:

`agents/`, `skills/`, `commands/`, `hooks/`, `tasks/`, `responses/`, `runs/`, `memory/`, `sessions/`, `workflows/`, `prompts/`, `notes/`, `docs/`, `ai/`, `claude-system/`, `agent-system/`, `harness/`, `workspace/`, `context/`, `project-state/`, `wiki/`, `vector/`, `embeddings/`, `index/`, `rag/`, `cache/`, `logs/`, `infra/`, `mcp/`.

Falls solche Konzepte trotzdem noetig sind: gehoeren in `adapters/<slug>/` als Substruktur, nicht als Projekt-Top-Level-Ordner.

## 5. Anti-Parallelstruktur-Pflichtregel

> **Erstelle kein zweites Workspace-System.**
>
> Wenn der Drang aufkommt, einen neuen Top-Level-Ordner anzulegen, ist der Drang ein Signal, zuerst zu fragen — niemals zuerst zu erstellen. Bevor ein neuer Top-Level-Ordner ausserhalb der Foundation-Mount-Points entsteht, muss explizit beim User angefragt werden. Die Begruendung wird in `state/decisions.md` festgehalten.

## 6. First-Session-Setup-Summary-Format

Am Ende der Setup-Session enthaelt `current-session.md`:

- Liste angelegter Setup-Decisions (D-IDs).
- Liste offener Setup-Questions (Q-IDs).
- Liste registrierter Setup-Artefakte (Pfade).
- Liste aktiver Adapter (oder "keiner").
- Liste aktiver Maintenance-Routinen (oder "keine").
- KG-Aktivierungsstatus (aktiv/inaktiv).
- Data-Space-Status (aktiv/inaktiv, Liste).
- Document-Normalization-Status (geplant/inaktiv).
- Resume-Anweisung fuer die naechste Arbeitssession.

## Cross-Links

- Adapter: `adapter-policy.md`.
- State-Dateien: `state/project-index.md`, `state/current-session.md`, `state/decisions.md`, `state/open-questions.md`, `state/risks-and-constraints.md`, `state/source-registry.md`, `state/artifact-index.md`.
- Templates: `templates/project-brief.md`, `templates/project-setup.md`, `templates/session-state.md`, `templates/data-space.md`, `templates/maintenance-routine.md`, `templates/adapter-readme.md`, `templates/gitignore-template.md`, `templates/claudeignore-template.md`.
- Knowledge-Graph + Document-Normalization: `knowledge-graph-policy.md`.

# setup-protocol.md — New-Project-Setup-Flow + Anti-Parallel-Regel

Diese Datei ist die kritische Stelle, an der entschieden wird, ob ein neues Projekt sauber an die Foundation andockt oder ob Parallelstrukturen entstehen. Setup wird manuell durchgefuehrt; die Foundation enthaelt keine Auto-Setup-Skripte.

## 1. New-Project-Setup-Flow

Lineare Schritte:

1. **Pre-Check.** Foundation in leeres oder neu-initialisiertes Projektverzeichnis kopieren. Falls bereits ein `.ai-workspace/` existiert: Setup abbrechen und Konflikt eskalieren.
2. **`state/project-index.md`** befuellen aus `templates/project-brief.md` — mindestens Slug, Zweck, Scope, Goals, Owner.
3. **`state/now.md`** initialisieren aus `templates/session-state.md` (gitignored, pro Worktree; der Hook `now_init` legt sie sonst beim ersten Start an) — Aktive Aufgabe = "Initial setup", Status = `in_progress`. Das Setup wird zusaetzlich im Journal der Session festgehalten (`journal/README.md`).
4. **Setup-Decisions** als Notizen unter `knowledge/decision/` anlegen, eine pro Entscheidung (z.B. "Wir starten ohne Adapter", "Datenraum wird extern gehalten"): `python -m harness.mdmemory new decision "<titel>"`. `state/decisions.md` wird nicht befuellt, sondern generiert.
5. **Setup-Open-Questions** als Notizen unter `knowledge/question/` mit `kind: question` anlegen (`python -m harness.mdmemory new question "<titel>"`).
6. **Setup-Risks** als Notizen unter `knowledge/question/` mit `kind: risk` bzw. `kind: constraint` anlegen (z.B. wenn Projekt regulierte Daten beruehrt). Danach `python -m harness.mdmemory index`: erzeugt `knowledge/INDEX.md`, `knowledge/_typen/` und die generierten Sichten `state/decisions.md`, `state/open-questions.md`, `state/assumptions.md`, `state/risks-and-constraints.md` (nie von Hand editieren).
7. **Ignore-Files** aus `templates/gitignore-template.md` und `templates/claudeignore-template.md` ableiten und ins Projekt-Root kopieren (manuell). Foundation-Core enthaelt keine aktiven Ignore-Files.
8. **Adapter-Entscheidung.** Wenn Adapter sofort noetig: `adapters/<slug>/adapter.md` aus `templates/adapter-readme.md` anlegen + in `state/project-index.md` Sektion "Aktive Adapter" eintragen. Sonst: spaeter entscheiden, Verzicht als Decision-Notiz.
9. **Vier KG/Data-Space/Maintenance/Normalization-Setup-Fragen** (Section 2 dieser Datei).
10. **Setup-Artefakte registrieren** in `state/artifact-index.md`.
11. **Setup-Session-Summary** als Journal-Eintrag `ergebnis` schreiben (dauerhaft, committet) und in `now.md` uebernehmen, Status auf `done` fuer die Initial-Setup-Phase.

## 2. Vier Setup-Fragen

Diese vier Fragen werden im Setup beantwortet. Jede Antwort wird eine Decision-Notiz unter `knowledge/decision/` (`python -m harness.mdmemory new decision "<titel>"`, danach `python -m harness.mdmemory index`).

### Frage 1: Markdown-Knowledge-Graph aktivieren?

- **Ja:** `knowledge/_index.md` aus `templates/moc.md` als Root-MOC anlegen. In `state/project-index.md` Sektion "Knowledge-Graph-Aktivierung" als aktiv markieren. Erste Topic-MOCs koennen spaeter folgen.
- **Nein:** Verzicht als Decision-Notiz festhalten. `knowledge/` enthaelt dann nur `README.md`, die atomaren Notizen unter `knowledge/<typ>/` und die generierten `INDEX.md` und `_typen/` — keine MOCs, keine Themen-Notizen.

### Frage 2: Project Data Space deklarieren?

- **Ja:** Pro Data Space ein `data-space/<datum>-<slug>.md` aus `templates/data-space.md`. Eintrag in `state/source-registry.md` mit `type: data-space`. Originaldaten leben **extern** oder im projektspezifisch deklarierten Speicherort, nicht im Foundation-Tree. Manifest enthaelt nur Pointer + Sensitivity + Allowed-Processing.
- **Nein:** Verzicht als Decision-Notiz festhalten.

### Frage 3: Maintenance-Routine-Blueprints adoptieren?

- **Ja:** In einem Adapter (`adapters/<slug>/maintenance/<routine-name>.md`) mit `templates/maintenance-routine.md` registrieren. Universelle Blueprints stehen als Auswahl-Hilfe zur Verfuegung (knowledge-graph-lint, knowledge-graph-sync, session-memory-review, source-artifact-hygiene, adapter-lifecycle-review, document-normalization-review, optional session-snapshot-export). Aktivierung erst nach explizitem User-Aktivierungs-Schritt pro Routine. Alternativ steht seit v3.1 die mitgelieferte opt-in Pflege-Routine `daily_maintenance` bereit (Execution-Schicht, default AUS, ueber `/start` oder `/uaw-automation` schaltbar), die diese Blueprints einmal pro Tag anstupst.
- **Nein:** Verzicht als Decision-Notiz festhalten.

### Frage 4: Externe Binaerinputs erwartet?

- **Ja:** Document-Normalization-Plan als Decision-Notiz festhalten. Pro erwartetem Binaer-Typ (PDF/DOCX/PPTX/XLSX/Bild/Audio/Video) Sensitivity-Default und Allowed-Processing-Default in dieser Decision-Notiz deklarieren. Erste Ingestion-Records werden via `templates/normalized-document.md` und `templates/normalization-review.md` angelegt, sobald Inputs vorliegen.
- **Nein:** Verzicht als Decision-Notiz festhalten.

## 3. Mount-Point-Decision-Tree (vor jeder Strukturerstellung)

Bevor irgendein neues Verzeichnis oder eine neue Datei ausserhalb bestehender Mount-Points angelegt wird, durchlaufe diese Reihenfolge:

```text
Frage 0: Ist es lauffaehiger, tool-nativer Harness-Code (Skill, Hook, Command,
         Agent-Definition) oder Engine-Code/Tests?
         -> Skill/Hook/Command/Agent: nach .claude/ (z.B. .claude/skills/<slug>/). Stop.
         -> Engine/Tests/Beispiele: nach src/ , tests/ , examples/ (Infra-Allowlist). Stop.
         -> NUR wenn das Repo den Harness mitliefert; sonst gehoert Code in einen Adapter.
Frage 1: Gehoert das nach state/?              -> Ja: dorthin. Stop.
         (nur project-index, now.md, source-registry, artifact-index;
          die Register-Sichten dort sind GENERIERT, nie von Hand)
Frage 2: Gehoert das nach adapters/<slug>/?    -> Ja: dort einbauen. Stop.
Frage 3: Gehoert das nach research/?           -> Ja: dorthin. Stop.
Frage 4: Gehoert das nach deliverables/?       -> Ja: dorthin. Stop.
Frage 5: Gehoert das nach scratch/?            -> Ja: dorthin. Stop.
Frage 6: Gehoert das nach archive/?            -> Ja: dorthin. Stop.
Frage 6b: Ist es eine Episode einer Session?   -> Ja: journal/YYYY/MM/ (eine Datei pro Session). Stop.
Frage 7: Gehoert das nach knowledge/?          -> Ja: dorthin. Stop.
         (Decision, Frage/Annahme/Risiko, Person, Praeferenz, Projekt,
          Referenz, Konzept: eine Notiz pro Datei unter knowledge/<typ>/;
          INDEX.md und _typen/ sind GENERIERT)
Frage 8: Gehoert das nach data-space/?         -> Ja (nur als .md-Manifest). Stop.
Frage 9: Gehoert das nach templates/?          -> Ja (nur bei Foundation-Erweiterung). Stop.
Sonst:   STOPPE. Frage den User. Lege keinen neuen Top-Level-Ordner ohne
         Erlaubnis an. Wenn neuer Ort genehmigt: dokumentiere die Begruendung
         als Decision-Notiz unter knowledge/decision/.
```

## 4. Verbotene Top-Level-Verzeichnisnamen

Diese Verzeichnisnamen duerfen nicht als Foundation-Top-Level-Ordner entstehen:

`agents/`, `skills/`, `commands/`, `hooks/`, `tasks/`, `responses/`, `runs/`, `memory/`, `sessions/`, `workflows/`, `prompts/`, `notes/`, `docs/`, `ai/`, `claude-system/`, `agent-system/`, `harness/`, `workspace/`, `context/`, `project-state/`, `wiki/`, `vector/`, `embeddings/`, `index/`, `rag/`, `cache/`, `logs/`, `infra/`, `mcp/`.

Falls solche Konzepte trotzdem noetig sind: gehoeren in `adapters/<slug>/` als Substruktur, nicht als Projekt-Top-Level-Ordner.

**Ausnahme bei mitgeliefertem Harness.** Wenn das Repo die lauffaehige Harness-Schicht enthaelt (siehe `AGENTS.md` §2.5), sind genau diese Top-Level-Eintraege erlaubt: `.claude/` (Execution-Mount; `skills/`, `hooks/`, `commands/`, `agents/` leben *darunter*, nie nackt im Root) sowie die Infra-Allowlist `src/`, `tests/`, `examples/`, `sources/`, `.github/`, `pyproject.toml`. Alle anderen Namen oben bleiben verboten. `harness/` bleibt als *nackter* Top-Level-Name verboten — die Engine lebt unter `src/harness/`.

## 5. Anti-Parallelstruktur-Pflichtregel

> **Erstelle kein zweites Workspace-System.**
>
> Wenn der Drang aufkommt, einen neuen Top-Level-Ordner anzulegen, ist der Drang ein Signal, zuerst zu fragen — niemals zuerst zu erstellen. Bevor ein neuer Top-Level-Ordner ausserhalb der Foundation-Mount-Points (inkl. der Harness-Ausnahme in §4) entsteht, muss explizit beim User angefragt werden. Die Begruendung wird als Decision-Notiz unter `knowledge/decision/` festgehalten (`python -m harness.mdmemory new decision "<titel>"`, danach `index`).
>
> Die Regel zielt auf **Workspace-Content-Sprawl** innerhalb `.ai-workspace/`. Sie verbietet nicht das normale Scaffolding eines Python-Pakets, wenn der Harness Teil des Repos ist.

## 6. First-Session-Setup-Summary-Format

Am Ende der Setup-Session enthaelt das Journal der Setup-Session (Eintrag `ergebnis`, Kurzfassung auch in `now.md`):

- Liste angelegter Setup-Decisions (D-IDs).
- Liste offener Setup-Questions (Q-IDs).
- Liste registrierter Setup-Artefakte (Pfade).
- Liste aktiver Adapter (oder "keiner").
- Liste aktiver Maintenance-Routinen (oder "keine").
- KG-Aktivierungsstatus (aktiv/inaktiv).
- Data-Space-Status (aktiv/inaktiv, Liste).
- Document-Normalization-Status (geplant/inaktiv).
- Resume-Anweisung fuer die naechste Arbeitssession.

## 7. Skalierung: ein Workspace = ein Bounded Context

Ein Workspace entspricht **einem** Bounded Context (einer kohaerenten Domaene oder Aufgabe). Mehrere Agenten teilen sich einen Workspace nur, wenn sie Wissen/State teilen und sich koordinieren muessen; unverbundene Domaenen bekommen je eine **eigene** Foundation-Instanz statt eines gemeinsamen Sammel-Workspaces. Eine gemeinsame Wissensbasis wird per Data-Space-Manifest/Pointer referenziert (`knowledge-graph-policy.md`), nicht kopiert.

## Cross-Links

- Adapter: `adapter-policy.md`.
- State-Dateien: `state/project-index.md`, `state/now.md` (lokal), `state/source-registry.md`, `state/artifact-index.md`; generierte Sichten `state/decisions.md`, `state/open-questions.md`, `state/assumptions.md`, `state/risks-and-constraints.md`.
- Notizen: `knowledge/<typ>/<id>.md` (Schema `templates/knowledge-note.md`), Einstieg `knowledge/INDEX.md` (generiert).
- Journal: `journal/README.md`.
- Templates: `templates/project-brief.md`, `templates/project-setup.md`, `templates/session-state.md`, `templates/journal-entry.md`, `templates/data-space.md`, `templates/maintenance-routine.md`, `templates/adapter-readme.md`, `templates/gitignore-template.md`, `templates/claudeignore-template.md`.
- Knowledge-Graph + Document-Normalization: `knowledge-graph-policy.md`.

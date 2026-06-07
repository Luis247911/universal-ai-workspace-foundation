---
description: Use this to onboard an EXISTING project to the Universal AI Workspace Foundation — analyze its current structure, decide governance-only vs. governance+execution together with the user, and produce a step-by-step migration plan before changing anything. Triggers on "/onboard", "adopt the foundation", "align my project", "migrate to the workspace foundation", "onboard this repo".
argument-hint: "[optional hint, e.g. 'governance only' or a folder to focus on]"
---

# /onboard — bestehendes Projekt an die Foundation ausrichten

Du richtest das **aktuelle Projekt** an der Universal AI Workspace Foundation (v3.1) aus. Die
Foundation-Dateien liegen bereits lokal in diesem Repo vor — lies sie mit `Read`/`Glob`/`Grep`,
**nicht** aus dem Netz.

Optionaler Hinweis des Users: $ARGUMENTS

## Die zwei Schichten (Kurzfassung)

- **Governance** (`.ai-workspace/`, reines Markdown): Regeln, Zustand, Wissen. Fast immer sinnvoll.
- **Execution** (`.claude/` + `src/harness/`, Python): Skills ueber einer pip-installierbaren
  Engine (Evals, Guardrails, Tracing, HITL, Routing, Memory, Orchestrierung). Nur wenn das Projekt
  sie wirklich nutzt.

Details: `AGENTS.md` §2.5.

> **Optionale Automatik (opt-in, default AUS):** Die Execution-Schicht bringt eine schaltbare
> Session-Automatik mit (Boot-Reload des Live-States + Recitation-Reminder). Sie ist **kein**
> Pflicht-Teil des Onboardings. Wer sie spaeter aktivieren oder nur verstehen will, ruft
> `/uaw-automation` auf — steuert nur dieses Repo, nie globale `~/.claude/`-Konfiguration.

## Harte Regeln (nicht verhandelbar)

- Nichts blind uebernehmen.
- Nichts ohne Rueckfrage loeschen oder ueberschreiben.
- **Kein neuer Top-Level-Ordner ohne Rueckfrage.** Verbotene Namen siehe `.ai-workspace/setup-protocol.md`
  §4 (u.a. `agents/`, `skills/`, `prompts/`, `notes/`, `docs/`, `wiki/`, `tasks/`). Einzige Ausnahmen:
  `.claude/` (Execution-Mount) plus Infra-Allowlist (`src/`, `tests/`, `examples/`, `sources/`,
  `.github/`, `pyproject.toml`).
- Vorhandene Ordner (`agents/`, `prompts/`, `notes/`, `docs/`, `wiki/`, `skills/`, `tasks/`) sauber
  **migrieren**, nicht als Parallelstruktur daneben neu aufbauen.
- Erst Plan erklaeren, dann aendern. Vor jedem Schreib-/Verschiebe-/Loesch-Schritt pausieren.
- Domain-neutral bleiben: fach-/kunden-spezifische Inhalte gehoeren in `.ai-workspace/adapters/<slug>/`,
  nicht in den Core.

## Ablauf

### Schritt 1 — bestehendes Projekt analysieren (read-only)

Verschaffe dir mit `Glob`/`Grep`/`Read` ein Bild des bestehenden Projekts (nicht der Foundation-Dateien):

- Welche Top-Level-Ordner gibt es? Wo liegen Notizen, Prompts, Agent-Definitionen, Docs, Wissen,
  Sessions, Code, Temp-Dateien?
- Gibt es doppelte/unklare Strukturen, verwaiste Dateien oder mehrere konkurrierende „Workspace"-Ansaetze?
- Existiert bereits ein `.ai-workspace/` mit echtem Inhalt (nicht das frisch kopierte Skelett)? Falls ja:
  das ist ein Konflikt — eskalieren, nicht ueberschreiben (vgl. `setup-protocol.md` §1 Pre-Check).

Fasse den Befund in 5–10 Bullets zusammen.

### Schritt 2 — Foundation-Referenz lesen (lokal)

Lies, soweit fuer die Entscheidung relevant:

- `README.md` (Zwei-Schichten-Modell)
- `AGENTS.md` §2.5 (Schichten) + §3 (Anti-Parallelstruktur, Carve-outs)
- `.ai-workspace/setup-protocol.md` §3 (Mount-Point-Decision-Tree, **Frage 0**) + §2 (vier Setup-Fragen)
- `install-checklist.md` (manueller Copy-/Init-Flow)
- nur falls Execution in Frage kommt: `install-harness.md` + `.ai-workspace/skills-authoring-policy.md`

### Schritt 3 — Schicht-Entscheidung MIT dem User

Stelle die Schluesselfrage und begruende eine Empfehlung aus Schritt 1:

- **Nur Governance** — wenn das Projekt vor allem Struktur, Regeln, Wissen und Zustand braucht
  (Doku-, Recherche-, Wissens-, Prozess-Projekte). Das ist der Default.
- **Governance + Execution** — nur wenn das Projekt die Agent-Engineering-Bausteine wirklich nutzt
  (Evals, Guardrails, Tracing, HITL, Routing, Memory, Orchestrierung).

Nutze `AskUserQuestion`. Fahre erst fort, wenn der User entschieden hat.

### Schritt 4 — Plan liefern, dann STOPPEN

Liefere (und lege/aendere noch **nichts**):

1. **Analyse** (aus Schritt 1).
2. **Empfehlung** Governance-only vs. +Execution, begruendet aus der Analyse.
3. **Was uebernehmen** — welche Foundation-Teile, in welche Mount-Points.
4. **Was nicht** — was dieses Projekt nicht braucht.
5. **Migrationsplan**, schrittweise, **Governance zuerst**, Execution optional danach. Pro Schritt:
   welche bestehende Datei / welcher Ordner wandert wohin (Mount-Point-Decision-Tree, Frage 0–9).
   Keine Parallelstruktur.
6. **Liste neu / geaendert / verschoben** (konkrete Pfade).

Danach **warte auf die ausdrueckliche Bestaetigung des Users.** Ohne ein explizites „Ja" wird nichts geaendert.

### Schritt 5 — Migration ausfuehren (nur nach Bestaetigung, schrittweise)

- Arbeite den Plan Schritt fuer Schritt ab. Vor jedem Schreib-/Verschiebe-/Loesch-Schritt kurz ankuendigen.
- **Governance zuerst:** `.ai-workspace/state/project-index.md` + `current-session.md` aus den Templates
  befuellen; bestehende Notizen/Docs/Wissen in die passenden Mount-Points migrieren (`knowledge/`,
  `research/`, `deliverables/`, …); Entscheidungen in `state/decisions.md` festhalten; die vier
  Setup-Fragen (`setup-protocol.md` §2) beantworten.
- **Execution nur, falls in Schritt 3 gewaehlt:** `.claude/` + `src/harness/` + `pyproject.toml` etc.
  uebernehmen, gemaess `install-harness.md` `pip install -e .`, danach `python -m harness.skills lint
  .claude/skills` pruefen.
- Nichts loeschen ohne Rueckfrage. Bei Unsicherheit ueber einen Ablageort: Mount-Point-Decision-Tree —
  und im Zweifel fragen, nicht raten.
- Zum Abschluss: Setup-Session-Summary in `current-session.md` (`setup-protocol.md` §6), erzeugte
  Artefakte in `state/artifact-index.md` registrieren.

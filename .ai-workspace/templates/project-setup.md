---
id: project-setup
type: project-setup
title: "First-Session-Setup-Checkliste"
status: draft
created: <YYYY-MM-DD>
updated: <YYYY-MM-DD>
owner: <user>
---

# Project Setup

Schritt-fuer-Schritt-Checkliste, die in der ersten Arbeitssession auf einem neu kopierten Foundation-Tree abgearbeitet wird. Im Gegensatz zu `install-checklist.md` (im Root, fuer den Menschen) ist diese Datei fuer die AI-Assistant-Instanz oder den User ablauf-orientiert.

## Pre-Check

- [ ] `state/project-index.md` und `state/current-session.md` sind als Stubs vorhanden.
- [ ] Verzeichnisstruktur passt zu Foundation-Default.
- [ ] Keine Parallelstruktur ausserhalb der Foundation-Mount-Points.

## Schritt 1: Project Brief

- [ ] Aus `templates/project-brief.md` ein neues Brief im Kopf oder Notizfile entwerfen.
- [ ] Slug, Name, Zweck, Scope, Goals, Owner notieren.
- [ ] Inhalte in `state/project-index.md` Sektionen 1-4 uebernehmen.

## Schritt 2: Erste Session initialisieren

- [ ] `state/current-session.md` aus `templates/session-state.md` befuellen.
- [ ] Active-Task = "Initial setup".
- [ ] Status = `in_progress`.

## Schritt 3: Setup-Decisions

- [ ] Initiale Setup-Decisions in `state/decisions.md` festhalten (z.B. "Wir starten ohne Adapter", "PII-Policy bleibt Default", "Datenraum extern").

## Schritt 4: Setup-Open-Questions und -Risks

- [ ] Offene Fragen in `state/open-questions.md`.
- [ ] Risiken in `state/risks-and-constraints.md`.
- [ ] Annahmen in `state/assumptions.md`.

## Schritt 5: Vier Setup-Fragen aus `setup-protocol.md`

- [ ] **Frage 1:** Markdown-Knowledge-Graph aktivieren?
  - Ja -> `knowledge/_index.md` aus `templates/moc.md` anlegen + in `state/project-index.md` Sektion 9 als aktiv markieren.
  - Nein -> Verzicht in `state/decisions.md`.
- [ ] **Frage 2:** Project-Data-Space deklarieren?
  - Ja -> Manifest unter `data-space/<datum>-<slug>.md` aus `templates/data-space.md` + Eintrag in `state/source-registry.md` mit `type: data-space` + Eintrag in `state/project-index.md` Sektion 10.
  - Nein -> Verzicht in `state/decisions.md`.
- [ ] **Frage 3:** Maintenance-Routine-Blueprints adoptieren?
  - Ja -> Adapter anlegen + Spezifikationen aus `templates/maintenance-routine.md` ableiten + in `state/project-index.md` Sektion 11.
  - Nein -> Verzicht in `state/decisions.md`.
- [ ] **Frage 4:** Externe Binaerinputs erwartet?
  - Ja -> Document-Normalization-Plan in `state/decisions.md` festhalten; Default-Sensitivity definieren.
  - Nein -> Verzicht in `state/decisions.md`.

## Schritt 6: Setup-Artefakte registrieren

- [ ] Alle erzeugten Setup-Artefakte (project-index, current-session, decisions Eintraege, evtl. Root-MOC, evtl. Data-Space-Manifest, evtl. Adapter-README) in `state/artifact-index.md` mit Status `active` eintragen.

## Schritt 7: Ignore-Files

- [ ] Aus `templates/gitignore-template.md` ein projektspezifisches `.gitignore` ins Projekt-Root ableiten (manuell).
- [ ] Aus `templates/claudeignore-template.md` ein projektspezifisches `.claudeignore` ins Projekt-Root ableiten (manuell).

## Schritt 8: Setup-Session-Summary

- [ ] `state/current-session.md` enthaelt die Setup-Summary (D-IDs, Q-IDs, Artefakt-Pfade, aktive Adapter, KG-/Data-Space-/Maintenance-/Normalization-Status, Resume-Anweisung).
- [ ] Status in `current-session.md` auf `done` fuer die Setup-Phase oder auf `in_progress` mit naechstem Task.

## Cross-Links

- Setup-Protokoll: `../setup-protocol.md`.
- State-Templates: `session-state.md`, `decision-record.md`.
- Adapter: `adapter-readme.md`.
- Projekt-Brief: `project-brief.md`.

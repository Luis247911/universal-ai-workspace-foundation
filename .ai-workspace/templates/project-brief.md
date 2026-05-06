---
id: <projekt-slug>
type: project-brief
title: "<voller projekt-name>"
status: draft
created: <YYYY-MM-DD>
updated: <YYYY-MM-DD>
owner: <user>
---

# Project Brief

Vorlage fuer die initiale Projektdefinition. Wird zu `state/project-index.md` ausgearbeitet.

## Slug + Name + Zweck

- **Slug:** `<projekt-slug>` (kebab-case, ASCII).
- **Name:** `<voller projekt-name>`.
- **Zweck (1 Satz):** `<beschreibung>`.

## Scope-Statement

- **In scope:** `<was ist drin>`.
- **Nicht in scope:** `<was ist explizit drausen>`.

## Goals

Priorisierte Liste (3-7 Eintraege):

1. `<goal-1>`
2. `<goal-2>`
3. `<goal-3>`

## Owner + Stakeholder

- **Owner:** `<owner-identifier>`.
- **Stakeholder:** `<liste>`.

## Externe Systeme

Plattformen oder Systeme, mit denen das Projekt interagiert (als Strings, ohne Credentials).

(noch keine)

## KG / Data-Space / Maintenance / Document-Normalization

- **Markdown-Knowledge-Graph aktivieren?** `<yes/no>` — falls ja, Root-MOC `knowledge/_index.md` anlegen.
- **Project-Data-Space deklarieren?** `<yes/no>` — falls ja, Manifeste unter `data-space/<datum>-<slug>.md`.
- **Maintenance-Routine-Blueprints adoptieren?** `<yes/no>` — falls ja, Adapter mit `templates/maintenance-routine.md`.
- **Document-Normalization erwartet?** `<yes/no>` — falls ja, Sensitivity-Defaults und erwartete Binaer-Typen dokumentieren.

## Setup-Datum

`<YYYY-MM-DD>`

## Cross-Links

- Setup-Protokoll: `../setup-protocol.md`.
- Project-Setup-Checklist: `project-setup.md`.
- Identitaet im State: `../state/project-index.md`.

---
id: project-index
type: project-index
title: "<projekt-slug>"
status: active
created: <YYYY-MM-DD>
updated: <YYYY-MM-DD>
owner: <user>
---

# Project Index

Projekt-Identitaet. Wird beim Setup ausgefuellt und nur bei strukturellen Aenderungen geaendert. Diese Datei ist eine der vier Boot-Dateien.

## 1. Projekt-Slug + Name + Zweck

- **Slug:** `<projekt-slug>` (kebab-case, ASCII).
- **Name:** `<voller projekt-name>`.
- **Zweck (1 Satz):** `<beschreibung>`.

## 2. Scope-Statement

- **In scope:** `<was ist drin>`.
- **Nicht in scope:** `<was ist explizit drausen>`.

## 3. Goals

Priorisierte Liste (3-7 Eintraege):

1. `<goal-1>`
2. `<goal-2>`
3. `<goal-3>`

## 4. Owner + Stakeholder

- **Owner:** `<owner-identifier>`.
- **Stakeholder:** `<liste>`.

## 5. Aktive Adapter

Eintraege werden hier nur dann hinzugefuegt, wenn ein Adapter aktiv geschaltet wird. Format:

```text
- <adapter-slug-1> | aktiviert <YYYY-MM-DD> | <zweck-1-satz> | Pfad: adapters/<adapter-slug-1>/adapter.md
```

(noch keine)

## 6. Kanonische Pfade

Falls von der Foundation-Default-Struktur abweichend, hier dokumentieren. Sonst leer.

(unveraendert gegenueber Foundation-Default)

## 7. Externe Systeme

Liste der Plattformen oder Systeme, mit denen das Projekt interagiert (als Strings, ohne Credentials, ohne Endpoints).

(noch keine)

## 8. Setup-Datum + Letzte Strukturaenderung

- **Setup-Datum:** `<YYYY-MM-DD>`.
- **Letzte Strukturaenderung:** `<YYYY-MM-DD>`.

## 9. Knowledge-Graph-Aktivierung

- **Aktiv:** `<yes/no>`.
- **Root-MOC:** `knowledge/_index.md` (falls aktiv).

## 10. Project-Data-Space-Aktivierung

Liste der aktiven Data-Spaces. Format:

```text
- <data-space-slug> | aktiviert <YYYY-MM-DD> | <kurzbeschreibung> | Manifest: data-space/<datum>-<slug>.md
```

(noch keine)

## 11. Maintenance-Routines aktiv

Liste der registrierten Maintenance-Routines. Format:

```text
- <routine-name> | adapter: <adapter-slug> | Spezifikation: adapters/<adapter-slug>/maintenance/<routine-name>.md
```

(noch keine)

## 12. Document-Normalization aktiv

- **Aktiv:** `<yes/no>`.
- **Erwartete Binaer-Inputs:** `<typen, falls bekannt>`.
- **Default-Sensitivity:** `<low/medium/high>`.
- **Default-Allowed-Processing:** `<manual / automated-with-approval / none>`.

## Cross-Links

- Live-Zustand: `current-session.md`.
- Setup: `../setup-protocol.md`.
- Adapter: `../adapter-policy.md`, `../adapters/README.md`.
- KG: `../knowledge/README.md`.
- Data-Space: `../data-space/README.md`.

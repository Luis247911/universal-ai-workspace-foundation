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

Projekt-Identitaet, Boot-Datei (`AGENTS.md` §1). Beim Setup ausfuellen, danach nur bei strukturellen Aenderungen aendern.

## 1. Projekt-Slug + Name + Zweck

- **Slug:** `<projekt-slug>` · **Name:** `<voller projekt-name>`
- **Zweck (1 Satz):** `<beschreibung>`

## 2. Scope-Statement

- **In scope:** `<was ist drin>` · **Nicht in scope:** `<was ist explizit draussen>`

## 3. Goals

1. `<goal-1>` (3-7 Eintraege, priorisiert)

## 4. Owner + Stakeholder

- **Owner:** `<owner-identifier>` · **Stakeholder:** `<liste>`

## 5. Aktive Adapter

Format: `- <slug> | aktiviert <YYYY-MM-DD> | <zweck> | Pfad: adapters/<slug>/adapter.md`

(noch keine)

## 6. Kanonische Pfade

(unveraendert gegenueber Foundation-Default)

## 7. Externe Systeme

Nur Namen, keine Credentials oder Endpoints.

(noch keine)

## 8. Setup-Datum + Letzte Strukturaenderung

- **Setup:** `<YYYY-MM-DD>` · **Letzte Strukturaenderung:** `<YYYY-MM-DD>`

## 9. Knowledge-Graph-Aktivierung

- **Gedaechtnis-Notizen:** immer aktiv (`knowledge/<typ>/`, Index `knowledge/INDEX.md`).
- **Topic-MOCs:** `<yes/no>`, Root-MOC `knowledge/_index.md` (falls aktiv).

## 10. Project-Data-Space-Aktivierung

Format: `- <slug> | aktiviert <YYYY-MM-DD> | <kurzbeschreibung> | Manifest: data-space/<datum>-<slug>.md`

(noch keine)

## 11. Maintenance-Routines aktiv

Format: `- <routine> | adapter: <slug> | Spezifikation: adapters/<slug>/maintenance/<routine>.md`

(noch keine)

## 12. Document-Normalization aktiv

- **Aktiv:** `<yes/no>` · **Binaer-Inputs:** `<typen>` · **Default-Sensitivity:** `<low/medium/high>` · **Processing:** `<manual / automated-with-approval / none>`

## Cross-Links

`../setup-protocol.md` · `../adapter-policy.md` · `../memory-contract.md`

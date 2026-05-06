---
id: <adapter-slug>
type: adapter-readme
title: "<adapter-name>"
status: active
created: <YYYY-MM-DD>
updated: <YYYY-MM-DD>
owner: <user-or-team>
adapter_slug: <adapter-slug>
activation_date: <YYYY-MM-DD>
scope_statement: "<1-2 saetze>"
---

# Adapter README

Pflicht-Dokument fuer jeden Adapter unter `adapters/<slug>/adapter.md`. Beschreibt Scope, Datei-Inventar, Sicherheits-Anmerkungen und Aktivierungsbedingungen.

## Beschreibung

`<was leistet dieser adapter; welche projektspezifische erweiterung bringt er>`

## Scope-Statement

- **In scope:** `<was deckt der adapter ab>`.
- **Nicht in scope:** `<was deckt er nicht ab>`.

## Aktivierungsbedingung

`<wann wird dieser adapter aktiviert; wann wird er deaktiviert>`

## Datei-Inventar

- `<pfad-im-adapter-1>` — `<zweck>`
- `<pfad-im-adapter-2>` — `<zweck>`

## Sicherheits-Anmerkungen

- **Tools / Hooks / MCP-Configs / Skills:** `<liste; oder "keine">`
- **Trust-Implikationen:** `<welche externen quellen werden beruehrt; welche credentials sind noetig>`
- **Sensitivitaet-Annahmen:** `<wenn der adapter mit sensiblen daten arbeitet, welche regeln gelten>`

## Maintenance Routines

`<liste registrierter Maintenance-Routinen mit Pointer auf adapters/<slug>/maintenance/<routine-name>.md; oder "keine">`

## RAG-Anbindung

`<falls dieser adapter ein rag-system einbringt: indexierungs-scope, do_not_load-compliance, trust-boundary; sonst "keine">`

## KG-Topics / MOC-Strukturen

`<falls dieser adapter eigene moc-strukturen oder topic-hierarchien beitraegt: pointer auf relevante moc-dateien; sonst "keine">`

## Beziehung zu Foundation-Policies

`<welche foundation-policies werden beruehrt; welche regeln werden ergaenzt; foundation-regeln werden niemals gelockert>`

## Deaktivierungs-Verfahren

1. Eintrag aus `state/project-index.md` Sektion "Aktive Adapter" entfernen.
2. Adapter-Verzeichnis nach `archive/YYYY-MM-DD-<slug>/` verschieben.
3. Pointer in `state/artifact-index.md` Status auf `archived` setzen.

## Cross-Links

- Adapter-Policy: `../../adapter-policy.md`.
- Setup: `../../setup-protocol.md`.
- Aktive Adapter im State: `../../state/project-index.md`.

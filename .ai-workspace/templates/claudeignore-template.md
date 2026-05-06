---
id: claudeignore-template
type: ignore-template
title: ".claudeignore-Template (Markdown-Anleitung)"
status: active
created: <YYYY-MM-DD>
updated: <YYYY-MM-DD>
owner: foundation
---

# .claudeignore — Anleitung (Markdown, kein aktives Ignore-File)

**Wichtig:** Diese Datei ist eine **Anleitung in Markdown**. Sie ist **kein** aktives `.claudeignore`. Foundation-Tree enthaelt keine aktiven Ignore-Files. Wenn ein Projekt diese Foundation kopiert, leitet der User aus dieser Datei ein projektspezifisches `.claudeignore` ab und legt es im Projekt-Root ab.

## Drei-Header-Struktur (empfohlen)

Ein `.claudeignore` bekommt drei klar getrennte Abschnitte: Secrets, Privacy/PII, Token-Saving. So bleibt Sicherheit von Token-Sparmassnahmen klar unterscheidbar.

```text
# === 1. SECRETS (immer ignorieren, nicht-verhandelbar) ===
.env
.env.*
*.key
*.pem
*.pfx
*.p12
secrets/
credentials/
**/password*
**/api-key*
**/auth-token*

# === 2. PRIVACY / PII (projektspezifisch ergaenzen) ===
# Adapter sollten hier projektspezifische PII-Patterns ergaenzen.
# Foundation-Default enthaelt keine PII-Patterns aus echten Projekten.
# Beispiele (nur als Hinweis, nicht aktiv): personenbezogene Datensaetze,
# Kunden-Manifeste, regulierte Dokumente. Konkrete Patterns kommen aus
# dem projektspezifischen Adapter.

# === 3. TOKEN-SAVING (Foundation-Default) ===
.ai-workspace/scratch/
.ai-workspace/archive/
.ai-workspace/research/_raw/
.ai-workspace/adapters/*/private/

# === 4. NICHT ignorieren: nicht den ganzen .ai-workspace/ ignorieren ===
# Die vier Boot-Dateien und state/ muessen lesbar bleiben.
# Diese Datei zeigt nur, was zusaetzlich ignoriert werden soll.
```

## Hinweise

- **Niemals** den gesamten `.ai-workspace/` ignorieren — die Boot-Dateien (AGENTS.md, CLAUDE.md, state/project-index.md, state/current-session.md) muessen lesbar bleiben.
- PII-Patterns sind projektspezifisch und gehoeren in den projektspezifischen Adapter, nicht in den Foundation-Default.
- Adapter, die mit besonders sensiblen Inhalten arbeiten, koennen erweiterte PII-Patterns in `adapters/<slug>/claudeignore-additions.md` (Markdown-Anleitung) bereitstellen.

## Cross-Links

- Setup-Anleitung: `../../install-checklist.md`.
- Sicherheit (Secret-Hygiene, Sensitivity-Stufen, `do_not_load`): `../security-policy.md`.
- Context-Loading: `../context-policy.md`.

---
id: gitignore-template
type: ignore-template
title: ".gitignore-Template (Markdown-Anleitung)"
status: active
created: <YYYY-MM-DD>
updated: <YYYY-MM-DD>
owner: foundation
---

# .gitignore — Anleitung (Markdown, kein aktives Ignore-File)

**Wichtig:** Diese Datei ist eine **Anleitung in Markdown**. Sie ist **kein** aktives `.gitignore`. Foundation-Tree enthaelt keine aktiven Ignore-Files. Wenn ein Projekt diese Foundation kopiert, leitet der User aus dieser Datei ein projektspezifisches `.gitignore` ab und legt es im Projekt-Root ab.

## Empfohlene Patterns (zum Kopieren in das projektspezifische `.gitignore`)

```text
# === Secrets (oben, breit gefasst) ===
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
**/api_key*
**/auth-token*

# === OS-Cruft ===
.DS_Store
Thumbs.db
desktop.ini

# === Editor-Cruft ===
.vscode/
.idea/
*.swp
*.swo
*~

# === Foundation-Lifecycle (projektspezifisch anpassen) ===
.ai-workspace/scratch/
.ai-workspace/research/_drafts/

# === Generated Outputs ausserhalb der Foundation (Projektspezifisch) ===
# (Foundation-Tree enthaelt keinen _generated/-Ordner; falls ein Projekt
#  Generated Outputs ausserhalb der Foundation produziert, hier ergaenzen.)
```

## Hinweise

- Das ableitende `.gitignore` ist projektspezifisch. Diese Vorlage ist konservativ; weitere Patterns koennen je nach Tech-Stack ergaenzt werden.
- Tech-Stack-Specifics werden **nicht** als Foundation-Default aufgenommen — sie gehoeren in einen projektspezifischen Adapter oder in das vom User selbst angepasste `.gitignore`.
- Der Foundation-Tree wird unter Umstaenden **mit** Versionskontrolle genutzt — dann wirkt das projektspezifische `.gitignore` ab dem Projekt-Root.

## Cross-Links

- Setup-Anleitung: `../../install-checklist.md`.
- Sicherheit (Secret-Hygiene): `../security-policy.md`.
- Ignore-Hinweise im Workspace-Lifecycle: `../file-lifecycle.md`.

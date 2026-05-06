# adapters/ — Projektspezifische Erweiterungen

Dieses Verzeichnis ist der **einzige** Ort fuer projekt-, kunden- oder domain-spezifische Erweiterungen. Foundation-Core bleibt domain-neutral; Domain-Inhalte leben hier.

## Adapter-Struktur

Pro Adapter ein Verzeichnis `adapters/<slug>/`. Pflicht-Datei darin: `adapter.md` (aus `templates/adapter-readme.md`).

```text
adapters/
  <adapter-slug>/
    adapter.md              # Pflicht
    workflows/              # frei
    prompts/                # frei
    templates/              # frei (adapter-spezifische templates)
    tools/                  # frei
    maintenance/            # frei (Routinen-Spezifikationen aus templates/maintenance-routine.md)
    ...
```

## Aktivierung

Ein Adapter wird in `state/project-index.md` Sektion "Aktive Adapter" eingetragen. Adapter ohne Eintrag gelten als **inaktiv** und werden nicht ausgewertet.

```text
- <adapter-slug-1> | aktiviert <YYYY-MM-DD> | <zweck-1-satz> | Pfad: adapters/<adapter-slug-1>/adapter.md
```

## Was Adapter duerfen

Siehe `adapter-policy.md` Section 1. Kurz:

- Projektspezifischen Kontext, Workflows, Prompts, Templates, Tools, Evaluationskriterien.
- Optionale Agents/Skills/Hooks/MCP-Configs (in `adapter.md` deklariert).
- Maintenance Routines (aus `templates/maintenance-routine.md`).
- RAG-Anbindungen (mit deklarierter Trust-Boundary).
- Domain-spezifische MOC-Strukturen.
- Document-Normalization-Tools (Parser, OCR, Office-Reader — sensitivity-konform).

## Was Adapter NICHT duerfen

Siehe `adapter-policy.md` Section 2. Kurz:

- Core-Protokolle ueberschreiben.
- Zweite State-/Source-/Artifact-Strukturen aufbauen.
- Sich auto-laden ohne Registrierung.
- Tools/Hooks/MCP default ausfuehren.
- Foundation-Sicherheits-Defaults lockern.

## Multi-Adapter-Koexistenz

Konflikte zwischen Adaptern werden in `state/decisions.md` dokumentiert + vom User explizit aufgeloest. Mehrere Adapter teilen sich dieselbe `state/`-Struktur.

## Deaktivierung

1. Eintrag aus `state/project-index.md` Sektion "Aktive Adapter" entfernen.
2. Adapter-Verzeichnis nach `archive/YYYY-MM-DD-<slug>/` verschieben.
3. Pointer in `state/artifact-index.md` Status auf `archived` setzen.

## Foundation-Defaults

**Foundation-Core enthaelt keinen Adapter.** Foundation-Tree enthaelt nur diese `README.md` und das Template `templates/adapter-readme.md`.

## Cross-Links

- Adapter-Policy: `../adapter-policy.md`.
- Setup: `../setup-protocol.md`.
- Aktive Adapter: `../state/project-index.md`.
- Adapter-Template: `../templates/adapter-readme.md`.
- Maintenance-Routine-Template: `../templates/maintenance-routine.md`.

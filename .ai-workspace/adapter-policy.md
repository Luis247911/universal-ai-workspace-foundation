# adapter-policy.md — Adapter-Vertrag + Boundaries

Definiert, wie projektspezifische Adapter funktionieren, ohne den Foundation-Core zu kontaminieren.

## 1. Adapter-Scope (was Adapter duerfen)

Adapter sind der einzige legitime Ort fuer projekt-, kunden- oder domain-spezifische Erweiterungen. Sie duerfen einbringen:

- Projektspezifischen Kontext (z.B. interne Glossare, Stilvorgaben).
- Workflows (Skripte, Slash-Commands, mehrstufige Anleitungen).
- Prompts (System-Prompts, Skill-Bodies, Persona-Dateien — nur innerhalb des Adapter-Scopes).
- Templates (Brief-Templates, Briefing-Templates, projektspezifische Zwischenformate).
- Tools (CLI-Wrapper, MCP-Configs — sofern in `adapter.md` deklariert + Sicherheitsmodell respektiert).
- Evaluationskriterien (Quality-Gates jenseits der Foundation-Defaults — ergaenzen, nicht ueberschreiben).
- Optionale Agents/Skills/Hooks/MCP-Configs (sofern sicherheits-konform und in `adapter.md` deklariert).
- **Maintenance Routines** (sofern via `templates/maintenance-routine.md` spezifiziert).
- **RAG-Anbindungen** (mit deklarierter Trust-Boundary, `do_not_load`-Compliance).
- **Domain-spezifische MOC-Strukturen oder Topic-Hierarchien** (Foundation-Templates bleiben generisch).
- **Document-Normalization-Tools** (Parser, OCR, Office-Reader — sofern Sensitivity-Regeln eingehalten und in `adapter.md` deklariert).

## 2. Was Adapter NICHT duerfen

- AGENTS.md, CLAUDE.md, protocol.md, setup-protocol.md, security-policy.md, source-policy.md, delegation-policy.md, file-lifecycle.md, context-policy.md, quality-gates.md, knowledge-graph-policy.md ueberschreiben.
- Eine zweite State-Struktur, Session-Struktur, Source-Registry, Artifact-Index aufbauen — alle Adapter teilen sich `state/`.
- Sich auto-laden, ohne in `state/project-index.md` als aktiv markiert zu sein.
- Tools/Hooks/MCP default-maessig ausfuehren — Aktivierung erfordert User-Bestaetigung pro Aktivierungs-Schritt.
- Ungetrackte Artefakte erzeugen — alle Adapter-Outputs muessen auf demselben Lifecycle (`scratch/`/`research/`/`deliverables/`/`archive/`/`knowledge/`/`data-space/`) sitzen.
- Parallele Top-Level-Verzeichnisse ausserhalb `adapters/<slug>/` erzeugen.
- Foundation-Sicherheits-Defaults lockern.
- Maintenance Routines aktivieren, ohne explizite User-Bestaetigung pro Aktivierungs-Schritt.
- RAG-Index ohne `do_not_load`-Compliance-Deklaration aufbauen.
- Den KG ohne MOC-Hygiene-Regel mit Auto-Generated Notes ueberschwemmen.
- Sensible Original-Binaerdateien automatisch normalisieren bei `sensitivity: high`.
- Generated-Nicht-Markdown-Dateien als kanonische Foundation-Deliverables behandeln.

## 3. Adapter-Verzeichnisstruktur

Pflicht-Layout:

```text
adapters/<slug>/
  adapter.md         # Pflicht: Beschreibung, Scope, Aktivierungsbedingung,
                     # Datei-Inventar, Sicherheits-Anmerkungen.
  <freie Substruktur, z.B.:>
  workflows/
  prompts/
  templates/
  tools/
  maintenance/<routine-name>.md   # Spezifikation aus templates/maintenance-routine.md
  ...
```

`adapter.md` ist Pflicht. Substruktur ist frei, soll aber dem Markdown-only-Prinzip folgen.

## 4. Registrierung

Ein Adapter wird in `state/project-index.md` Sektion "Aktive Adapter" eingetragen, sonst gilt er als inaktiv und wird nicht ausgewertet:

```text
- adapter-slug-1 | aktiviert YYYY-MM-DD | Zweck (1 Satz) | Pfad: adapters/adapter-slug-1/adapter.md
- adapter-slug-2 | aktiviert YYYY-MM-DD | Zweck (1 Satz) | Pfad: adapters/adapter-slug-2/adapter.md
```

## 5. Adapter-Inheritance

Adapter erben Foundation-Policies. Sie koennen nichts lockern, nur ergaenzen.

## 6. Multi-Adapter-Coexistenz

Zwei Adapter teilen sich `state/`. Konflikte zwischen Adaptern (z.B. zwei Adapter wollen denselben Hook registrieren, oder zwei Adapter haben widerspruechliche MOC-Topics):

1. Aufgedeckt durch Setup-Check oder Periodic Review.
2. In `state/decisions.md` als Konflikt-Entry dokumentiert.
3. Vom User explizit aufgeloest (welcher Adapter Vorrang).

## 7. Adapter-Deaktivierung

1. Eintrag aus `state/project-index.md` Sektion "Aktive Adapter" entfernen.
2. Adapter-Verzeichnis nach `archive/YYYY-MM-DD-<slug>/` verschieben (oder in `archive/` direkt mit Datum-Slug-Naming).
3. Pointer in `state/artifact-index.md` Status auf `archived` setzen.

## 8. Maintenance-Routine-Registrierung

**Pflicht-Regel:** Maintenance Routines duerfen ausschliesslich ueber Adapter oder explizite globale User-Konfiguration registriert werden. **Foundation-Core enthaelt keine aktive Routine.**

Ein Adapter, der Routines einbringt:

1. Dokumentiert sie in `adapter.md` Sektion "Maintenance Routines".
2. Liefert pro Routine eine Spezifikation gemaess `templates/maintenance-routine.md`, abgelegt unter `adapters/<slug>/maintenance/<routine-name>.md`.
3. Trigger-Mechanismus (manueller Aufruf, Hook, Cron, Slash-Command) liegt im Adapter, nicht im Core.
4. Default-Output-Pfad benannt (Empfehlung: `scratch/maintenance/<datum>-<routine>.md`).
5. Approval-Anforderungen explizit gemacht.
6. Eintrag in `state/project-index.md` Sektion "Maintenance-Routines aktiv".

Outputs gelten als delegierte Arbeit — siehe `delegation-policy.md` Section 6.

## 9. RAG/Vector-DB-Adapter-Klausel

Wenn ein Adapter ein RAG-System einbringt:

- Adapter deklariert in `adapter.md`: Indexierungs-Scope (welche Quellen werden indexiert), Trust-Boundary, `do_not_load`-Compliance, Verifikations-Workflow.
- RAG-Output gilt als externer Quellen-Output (Untrusted-Default).
- RAG ist niemals Source of Truth — siehe `knowledge-graph-policy.md` Section "Beziehung zu RAG".
- Foundation-Core enthaelt kein RAG, keine Vector-DB, keinen Crawler.

## 10. KG-Adapter-Klausel

Adapter duerfen domain-spezifische MOC-Strukturen oder Topic-Hierarchien einbringen. Foundation-Templates bleiben generisch. Wenn ein Adapter neue MOCs erzeugt, sind sie ueber `[[wiki-links]]` aus dem Root-MOC (`knowledge/_index.md`) erreichbar oder explizit als "adapter-specific MOC" markiert (Frontmatter-Hinweis).

## Cross-Links

- Setup: `setup-protocol.md`.
- Behavior: `protocol.md`.
- Adapters-README: `adapters/README.md`.
- Maintenance-Routine-Template: `templates/maintenance-routine.md`.
- Delegation: `delegation-policy.md`.
- KG-Policy: `knowledge-graph-policy.md`.
- Sicherheit: `security-policy.md`.
- State-Tracking: `state/project-index.md`.

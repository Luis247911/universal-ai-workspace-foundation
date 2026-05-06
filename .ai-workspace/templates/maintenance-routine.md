---
name: <routine-name>
type: maintenance-routine
purpose: "<1-2 saetze>"
status: proposed
created: <YYYY-MM-DD>
updated: <YYYY-MM-DD>
owner: <user-or-adapter-slug>
last_reviewed: <YYYY-MM-DD>
default_output_trust: unverified
approval_required_before_state_mutation: yes
verification_required: yes
activation_method: adapter or explicit-user-config
---

# Maintenance Routine Spezifikation

Vorlage fuer die **Spezifikation** einer Maintenance Routine. **Foundation enthaelt keine aktive Routine, nur die Spezifikations-Vorlage.** Adapter koennen Routinen registrieren, indem sie pro Routine eine Datei aus dieser Vorlage ableiten und unter `adapters/<slug>/maintenance/<routine-name>.md` ablegen.

## Name

`<routine-name>` (Slug, kebab-case).

## Purpose

`<1-2 saetze: was leistet diese routine>`

## Typical Use Case

`<warum braucht ein projekt diese routine>`

## Typical Cadence

Generisch: `manual / daily / weekly / monthly depending on project need`. **Keine konkrete Frequenz, Uhrzeit oder Cron-Konfiguration im Core.** Konkrete Trigger werden ggf. im Adapter-Trigger-Mechanismus dokumentiert.

## Trigger

`<manual / scheduled-via-adapter / on-event-by-adapter>` — Foundation triggert nichts.

## Frequency

`<empfehlung; pro adapter zu konkretisieren>` — keine Foundation-Default-Frequenz.

## Scope

`<welche pfade darf die routine lesen>`

## Allowed Paths

Explizite Liste:

- `<pfad-1>` (z.B. `knowledge/**`, `state/source-registry.md`).

## Forbidden Paths

Explizite Liste:

- `**/secrets/**`
- `**/.env*`
- `**/credentials*`
- alle Pfade ausserhalb des Projekts
- `<weitere-projekt-spezifische-verbote>`

## Inputs

`<welche inputs nimmt die routine entgegen>`

## Outputs

`<welche reports erzeugt sie; immer als markdown>`

## Report Location

`<default: scratch/maintenance/<datum>-<routine>.md; eskalierbar nach research/ oder archive/ durch hauptsession>`

## Approval Required

`<welche aktionen erfordern explizite user-bestaetigung>` — Default: alle State-Mutationen.

## Verification Required

`<vor state-promote>` — Default: ja, durch Hauptsession.

## State Files Touched

`<welche state-dateien duerfen mutiert werden>` — Default: keine; nur Reports werden geschrieben.

## Rollback or Revert Notes

`<wie revertiert man, falls die routine einen fehler einbringt>`

## Owner

`<user-or-adapter-slug>`

## Last Reviewed

`<YYYY-MM-DD>`

## Allowed Actions (generisch)

- Tote Links melden.
- Fehlende Backlinks melden.
- Stale notes markieren.
- Source-registry auf fehlende Felder pruefen.
- Artifact-index auf verwaiste Artefakte pruefen.
- Adapter-lifecycle pruefen.
- Markdown-normalisierte Inputs pruefen.
- Cleanup-review vorbereiten.
- Setup-drift melden.
- Document-normalization-status pruefen.

## Forbidden Actions (generisch)

- Eigenstaendig Secrets lesen.
- Externe Repos klonen oder downloaden.
- Binaerdateien automatisch verarbeiten, wenn Sensitivitaet ungeklaert ist.
- State-Dateien ohne Hauptsession-Review ueberschreiben.
- Findings direkt in durable State promoten.
- Neue Parallelstrukturen erzeugen.
- Aktive Hooks, MCP-Server oder Cronjobs im Core installieren.

## Cross-Links

- KG-Policy (Section 11): `../knowledge-graph-policy.md`.
- Delegation: `../delegation-policy.md`.
- Adapter-Policy: `../adapter-policy.md`.
- Quality-Gates: `../quality-gates.md`.
- Delegated-Work-Report-Template: `delegated-work-report.md`.

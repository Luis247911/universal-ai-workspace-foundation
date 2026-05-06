---
id: artifact-index
type: artifact-index
title: "Artifact Index"
status: active
created: <YYYY-MM-DD>
updated: <YYYY-MM-DD>
owner: <user>
---

# Artifact Index

Tracking produzierter Artefakte. Append-only mit Status-Updates erlaubt. Nicht jede Scratch-Datei wird gelistet — nur Artefakte mit Bedeutung (Research-Reports, Deliverables, Decisions, Handoffs, Cleanup-Reviews, Knowledge-Notes, MOCs, Data-Space-Manifeste, Ingestion-Records, Normalized-Documents, Normalization-Reviews, Maintenance-Outputs).

## Erlaubte Typen

- `research`
- `deliverable`
- `decision`
- `handoff`
- `cleanup`
- `knowledge-note`
- `moc`
- `data-space`
- `ingestion-record`
- `normalized-document`
- `normalization-review`
- `maintenance-output`

## Pflichtfelder pro Eintrag

| Feld | Bedeutung |
|------|-----------|
| `artifact-id` | Eindeutiger Slug. |
| `Pfad` | Relativer Pfad innerhalb des Foundation-Tree. |
| `Typ` | Einer der erlaubten Typen oben. |
| `Created-Date` | `YYYY-MM-DD`. |
| `Last-Updated-Date` | `YYYY-MM-DD`. |
| `Status` | `draft` / `active` / `archived` / `superseded`. |
| `Producer` | `User` / `Assistant` / `Delegated-<adapter-slug>`. |
| `Verification-Status` | `unverified` / `verified` / `trusted` (siehe `quality-gates.md`). |

## Eintraege

| artifact-id | Pfad | Typ | Created | Last-Updated | Status | Producer | Verification-Status |
|-------------|------|-----|---------|--------------|--------|----------|---------------------|
| (noch keine) | | | | | | | |

## Cross-Links

- Lifecycle: `../file-lifecycle.md`.
- Quality-Gates: `../quality-gates.md`.
- Subdirectory-READMEs: `../research/README.md`, `../deliverables/README.md`, `../knowledge/README.md`, `../data-space/README.md`, `../archive/README.md`.

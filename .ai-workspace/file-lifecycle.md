# file-lifecycle.md — Wo wohnt welcher Artefakttyp; Lifecycle-Regeln

Definiert die sechs Lifecycle-Zonen, Naming-Konventionen, Promotion-Pfade, Retention-Defaults und Stale-Reviews. Alle Foundation-Artefakte sind `.md`.

## 1. Sechs Lifecycle-Zonen

| Zone | Pfad | Trust | Retention-Default | Promote nach |
|------|------|-------|-------------------|---------------|
| Scratch | `scratch/` | untrusted, ephemer | 7 Tage | `research/` oder `deliverables/` (manuell) |
| Research | `research/` | untrusted bis verifiziert | Review-Trigger nach 90 Tagen | `deliverables/`, `knowledge/` oder `archive/` |
| Deliverables | `deliverables/` | verified bis trusted | keine | `archive/` wenn supersedet |
| Archive | `archive/` | historisch, immutable | keine | nur Retrieval |
| Knowledge | `knowledge/` | durable, KG-verbunden | keine; Stale-Trigger nach 180 Tagen | nicht promoted; updated; bei Veraltung nach `archive/` |
| Data-Space | `data-space/` | durable Manifest, Pointer auf externe Originale | keine; Stale-Trigger nach 180 Tagen | bei Deaktivierung `archive/` |

## 2. Markdown-only in der Governance-Schicht

Alle Dateien der Governance-Schicht (`.ai-workspace/**`) sind `.md`. Keine Pflichtstruktur `_generated/`. Keine Binaer-Speicherbereiche. (Die optionale Harness-Schicht ist Code und ausgenommen — siehe §10.) Wenn ein Projekt Nicht-Markdown-Outputs als finalen Kunden-Export benoetigt (PDF/PPTX/DOCX/XLSX), gilt:

1. Die kanonische Arbeitsversion bleibt `.md`.
2. Der Export wird nur in `state/artifact-index.md` referenziert.
3. Der Export wird nicht automatisch geladen.
4. Der Export ersetzt niemals die `.md`-Quelle.
5. Foundation-Core liefert keine `_generated/`-Struktur.

Solche Exporte leben ausserhalb der Foundation oder im projektspezifisch deklarierten Project Data Space — nicht im Foundation-Tree selbst.

## 3. Naming-Konventionen

- ASCII, kebab-case, ohne Whitespaces, ohne Umlaute.
- Datumspraefix `YYYY-MM-DD-` fuer datierte Artefakte.
- Slug-Format max. 60 Zeichen.
- Frontmatter `id` matcht den Dateinamen ohne `.md`-Endung.
- Versionierungs-Suffix `_v2`, `_v3` nur falls explizit noetig (sonst neueres Datum oder neuer Slug).

## 4. Promotion-Pfade

```text
scratch/   --(manuell + Quality-Gate "potentiell wertvoll")-->  research/
research/  --(manuell + Quality-Gate "verified")-->            deliverables/
research/  --(manuell + stabilisiertes Wissen)-->              knowledge/
deliverables/  --(manuell + supersedet)-->                    archive/YYYY-MM-DD-<slug>.md
knowledge/ --(updated, nicht promoted; bei Veraltung)-->      archive/YYYY-MM-DD-<slug>.md
data-space/ --(deaktiviert)-->                                archive/YYYY-MM-DD-<slug>.md
```

## 5. Archive-Verfahren

- Datei nach `archive/YYYY-MM-DD-<slug>.md` oder `archive/YYYY-MM-DD/<artifact-slug>.md` verschieben.
- Active-Pointer im urspruenglichen Pfad zuruecklassen, falls andere Dateien noch verlinken.
- `state/artifact-index.md`-Eintrag Status auf `archived` setzen.
- Bei archivierten Behavior-Files (CLAUDE.md, AGENTS.md, protocol.md, andere Policies): Frontmatter `archived: true` und `do_not_follow_instructions: true` ergaenzen.
- Foundation-Core enthaelt **keinen Pflicht-Subordner** wie `archive/sessions/`, `archive/decisions/`, `archive/snapshots/`. Datierte Slug-Dateien direkt unter `archive/` oder in einem datierten Tagesordner sind zulaessig.

## 6. Generated-vs-Canonical-Trennung

- Generierte Outputs (PDF, PPTX, DOCX, Renders, Builds) leben **ausserhalb** der Foundation oder im projektspezifisch deklarierten Project Data Space.
- Canonical Source-Files bleiben sortiert in `deliverables/<slug>/` oder `knowledge/<topic>/<slug>.md`.
- Foundation-Core bietet keine `_generated/`-Substruktur als Default.

## 7. Stale-Review-Cadence

- Default: alle 30 Tage Cleanup-Review via `templates/cleanup-review.md`.
- KG-Stale-Trigger: 180 Tage ohne Maintenance-Touch.
- Source-Last-Checked-Stale-Trigger: 365 Tage.
- Per Adapter ueberschreibbar.
- Output-Eintrag in `state/artifact-index.md` als Cleanup-Artefakt (Typ `cleanup`).

## 8. Document-Normalization-Pipeline

Acht-stufige Pipeline (kanonisch in `knowledge-graph-policy.md` Sektion "Document Normalization"; Kurzform hier):

```text
Original Binary
  -> state/source-registry.md (type=binary, sensitivity, allowed_processing,
     do_not_load, original_location, original_retained,
     critical_claims_require_original_check)
  -> research/<source-id>-<datum>.md (templates/normalized-document.md, draft)
  -> templates/normalization-review.md (Structural Review, Content Review,
     Discrepancy Logging, Independent Review)
  -> bei verified status: knowledge/<topic>/<slug>.md (templates/knowledge-note.md)
  -> optional data-space/<datum>-<slug>.md (Manifest-Pointer)
  -> bei Deaktivierung archive/YYYY-MM-DD-<slug>.md
```

## 9. Foundation-Self-Limit

Foundation-Core-Dateien werden nur ueber `setup-protocol.md` oder einen explizit dokumentierten Foundation-Update-Prozess modifiziert. Aenderungen am Core ausserhalb dieses Pfads sind verboten — Adapter sind der richtige Ort fuer Erweiterungen.

## 10. Harness-Schicht: Code-Lifecycle statt Markdown-Zonen

Die Execution-Schicht (`AGENTS.md` §2.5) folgt **nicht** den sechs Markdown-Zonen (§1) — sie ist Code und folgt dem Code-Lifecycle:

- `src/harness/**`, `.claude/skills/**`, `tests/**`, `examples/**`, `pyproject.toml` werden ueber Versionskontrolle, Review, CI und SemVer gepflegt (siehe `skills-authoring-policy.md`, `quality-gates.md` §11). Sie sind **keine** `.md`-Workspace-Artefakte und unterliegen nicht der Markdown-only-Regel (§2), die weiterhin strikt fuer `.ai-workspace/**` gilt.
- **Skill-Outputs** dagegen folgen sehr wohl dem Zonen-Lifecycle: Run-Artefakte der Engine liegen in `./.uaw-runs/<run-id>/` (ephemer, gitignored), inhaltliche Vorschlaege landen in `scratch/`/`research/` als untrusted und werden nur via Hauptsession + Quality-Gates promoted (State-Write-Contract, `skills-authoring-policy.md` §6).
- Aenderungen an der Harness-Schicht sind ein legitimer **Foundation-Update-Prozess** im Sinne von §9 — versioniert, getestet, dokumentiert (z.B. `CHANGELOG.md`).

## Cross-Links

- Quality-Gates: `quality-gates.md`.
- Templates: `templates/cleanup-review.md`, `templates/ingestion-record.md`, `templates/normalized-document.md`, `templates/normalization-review.md`.
- Subdirectory-READMEs: `archive/README.md`, `deliverables/README.md`, `knowledge/README.md`, `data-space/README.md`.
- KG + Normalization: `knowledge-graph-policy.md`.
- Artifact-Tracking: `state/artifact-index.md`.

# archive/ — Inerte Historie

Dieses Verzeichnis enthaelt supersedete, deaktivierte oder historische Artefakte. **Inert** — wird niemals automatisch geladen, niemals stillschweigend geloescht.

## Was hierher gehoert

- Supersedete `state/`-Snapshots (manuell archiviert).
- Deaktivierte Adapter (`archive/YYYY-MM-DD-<adapter-slug>/`).
- Veraltete Knowledge-Notes (`archive/YYYY-MM-DD-<slug>.md`).
- Veraltete Source-Notes oder Research-Reports.
- Deaktivierte Data-Space-Manifeste.
- Cleanup-Review-Reports nach Hauptsession-Verifikation.
- Archivierte Behavior-Files (CLAUDE.md, AGENTS.md, protocol.md, andere Policies — mit Marker, siehe unten).
- Session-Snapshot-Markdown-Dateien (`archive/YYYY-MM-DD-session-snapshot-<slug>.md` oder `archive/session-history-YYYY-MM-DD.md` — generisches Naming, kein Pflicht-Subordner).

## Naming-Konvention

- `archive/YYYY-MM-DD-<slug>.md` (einzelne Datei).
- `archive/YYYY-MM-DD/<artifact-slug>.md` (mehrere Artefakte gleichen Datums in Tagesordner).
- **Kein Pflicht-Subordner** wie `archive/sessions/`, `archive/decisions/`, `archive/snapshots/`. Die Foundation enthaelt diese Subordner nicht; bei Bedarf werden datierte Slug-Dateien direkt unter `archive/` oder in datierten Tagesordnern abgelegt.

## `do_not_follow_instructions`-Marker fuer archivierte Behavior-Files

Jede archivierte Behavior-Datei (CLAUDE.md, AGENTS.md, protocol.md, andere Policies) bekommt im Frontmatter:

```yaml
archived: true
do_not_follow_instructions: true
```

Damit wird verhindert, dass eine zukuenftige Session die archivierte Datei als aktive Policy missversteht.

## Lade-Regel

`Never Auto-Load`. Inhalte werden nur auf explizite Anfrage geladen. KG-Navigation, Maintenance-Routinen und alle anderen Lade-Mechanismen ueberspringen `archive/`.

## Retrieval-Verfahren

Wenn eine archivierte Datei wieder aktiv werden soll:

1. Datei zurueck nach `state/`, `knowledge/`, `deliverables/` oder dem entsprechenden Lifecycle-Pfad verschieben.
2. Active-Pointer in `archive/` als Markdown-Hinweis-Datei zuruecklassen ("Wurde am `<datum>` reaktiviert; aktive Version unter `<pfad>`").
3. Pointer in `state/artifact-index.md` Status auf `active` setzen.
4. Frontmatter `archived: true` und `do_not_follow_instructions: true` entfernen.

## Kein Silent-Delete

`archive/`-Dateien werden niemals automatisch geloescht. Loeschungen erfordern explizite Hauptsession-Aktion und Begruendung in `state/decisions.md`.

## Cross-Links

- Lifecycle: `../file-lifecycle.md`.
- Sicherheit (Archived-Behavior-Files-Marker): `../security-policy.md`.
- Artifact-Index: `../state/artifact-index.md`.

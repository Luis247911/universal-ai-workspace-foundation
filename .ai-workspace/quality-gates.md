# quality-gates.md — Generische Verifikations-Stufen

Diese Datei definiert generische Quality-Gates fuer jeden Artefakttyp. Foundation enthaelt keine domain-spezifischen Quality-Checks (kein Tone-Lint, kein Brand-Check, kein Code-Style-Lint). Adapter duerfen domain-spezifische Quality-Gates ergaenzen.

## 1. Drei Stufen

| Stufe | Definition |
|-------|------------|
| `unverified` | Default fuer alles in `scratch/` und `research/`. Keine andere Quelle/Methode hat das Ergebnis bestaetigt. |
| `verified` | Mindestens eine andere Quelle/Methode bestaetigt; oder der User hat geprueft. Promotion in `deliverables/` oder `knowledge/` zulaessig. |
| `trusted` | Mehrfach verifiziert; mindestens einmal in einer Session genutzt ohne Korrektur; in `deliverables/` aufgenommen. |

## 2. Promotion-Trigger

- `unverified` -> `verified`: zweite unabhaengige Pruefung; oder User-Verifikation; oder erfolgreiche Konsistenzpruefung gegen vorhandene `state/`-Eintraege.
- `verified` -> `trusted`: erfolgreiche Promotion in `deliverables/` und mindestens einmal aktive Verwendung ohne Korrektur.
- Bei Konflikt mit neuen Erkenntnissen: Status zuruecksetzen + Eintrag in `state/decisions.md` mit Begruendung.

## 3. Failure-Handling

Wenn ein Artefakt eine Stufe verliert (z.B. Quelle wird stale, Aussage widerlegt, normalisierte Markdown-Datei zeigt sich als falsch):

1. Verification-Status zuruecksetzen.
2. Eintrag in `state/decisions.md` (warum, ab wann, durch welche Beobachtung).
3. Pointer in `state/artifact-index.md` aktualisieren.
4. Falls schwerwiegend (z.B. Aussage in Decisions oder Deliverables eingeflossen): zusaetzlich `state/risks-and-constraints.md`-Eintrag.

## 4. Foundation-Domain-Neutralitaet

Foundation enthaelt **keine** domain-spezifischen Quality-Checks. Adapter duerfen domain-spezifische Quality-Gates ergaenzen — z.B. ein Adapter koennte stilistische Lints, Compliance-Checks oder fachliche Plausibilitaets-Checks definieren. Diese leben unter `adapters/<slug>/quality/<check-name>.md` und werden in `adapter.md` registriert.

## 5. Verification-Status-Field-Format

Jedes Foundation-Template enthaelt ein Frontmatter-Feld:

```yaml
verification_status: unverified  # unverified / verified / trusted
```

Pflicht in: `templates/research-report.md`, `templates/decision-record.md`, `templates/knowledge-note.md`, `templates/source-note.md`, `templates/normalized-document.md`, `templates/normalization-review.md`, `templates/maintenance-routine.md` (Output), `templates/delegated-work-report.md`.

## 6. Knowledge-Note-Verification-Spezifika

Knowledge-Notes haben zusaetzliche Felder im Frontmatter:

- `link_validity` — `ok` / `partial` / `broken`. Alle `[[wiki-links]]` zeigen auf existierende oder als `status: planned` markierte Notes.
- `freshness` — Datum, wann die Note zuletzt gegen Quellen verifiziert wurde.

Eine Knowledge-Note kann erst auf `verified` gehoben werden, wenn `link_validity = ok` und mindestens eine `source_ids`-Reference vorliegt.

## 7. Maintenance-Routine-Findings-Verifikation

Findings einer Maintenance Routine (z.B. "20 tote Links gefunden", "5 verwaiste Knowledge-Notes", "12 Sources mit fehlendem Markdown-Derivat") sind initial `unverified` und muessen von der Hauptsession verifiziert werden, bevor durable State (Knowledge-Note-Updates, Archive-Bewegungen, Source-Registry-Aenderungen, Artifact-Index-Updates) erfolgt. Siehe `delegation-policy.md` Section 6.

## 8. Document-Normalization-Verifikation

Normalized Markdown durchlaeuft die acht-stufige Pipeline (siehe `knowledge-graph-policy.md` Sektion "Document Normalization Pipeline"):

- `normalization_status: draft` -> `reviewed` -> `verified` (oder `rejected`).
- `verification_status: unverified` -> `partially_verified` -> `verified` (oder `do_not_use`).

Vor Promotion einer Normalized-Markdown-Datei in `knowledge/` muss `verification_status` mindestens `partially_verified` sein, mit dokumentierten unsicheren Stellen. Bei `verified` ist Promotion zulaessig. Bei `do_not_use` ist die Datei nicht zu verwenden — der Eintrag bleibt aber bestehen, um Wiederholungs-Versuche dokumentiert zu vermeiden.

## 9. Unverified-Markdown-Nutzung

`unverified` oder `partially_verified` Markdown wird nur mit Warnhinweis genutzt. **`do_not_use`-Markdown wird nicht verwendet** und nicht in Knowledge-Notes, Deliverables oder Decisions zitiert.

## 10. Tool- und Command-Begriffe

Tool-/Command-Namen erscheinen in dieser Foundation **ausschliesslich** in `security-policy.md` als Beispiele fuer verbotene oder genehmigungspflichtige Ausfuehrung. Sie erscheinen nicht in `quality-gates.md` als Lint-Tool-Empfehlung, nicht in anderen Policies als Setup-/Workflow-Default. Domain-spezifische Tool-Empfehlungen leben in Adaptern.

## Cross-Links

- Lifecycle: `file-lifecycle.md`.
- Delegation: `delegation-policy.md`.
- Templates: `templates/research-report.md`, `templates/decision-record.md`, `templates/knowledge-note.md`, `templates/source-note.md`, `templates/normalized-document.md`, `templates/normalization-review.md`, `templates/maintenance-routine.md`, `templates/delegated-work-report.md`.
- KG + Document-Normalization: `knowledge-graph-policy.md`.

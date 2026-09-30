# knowledge/ — Langzeitgedaechtnis

Primaerer Mount Point fuer das dauerhafte, menschenlesbare Gedaechtnis des Projekts. **Alle Inhalte sind `.md`**, maschinenlesbar ueber YAML-Frontmatter. Seit v3.3 kanonisch fuer Wissen, Decisions, Praeferenzen, offene Fragen, Annahmen und Risiken (D-2026-09-30-04).

## Was hier wohnt

- **Atomare Notizen**, eine Aussage pro Datei, unter `<typ>/<id>.md`. Schema v1 steht in `../templates/knowledge-note.md`.
- **Generierte Indizes**, nie von Hand editieren: `INDEX.md` (Boot-Datei) und `_typen/<typ>.md`.
- **Optional ein Themen-Graph in Langform**: Topic-Notizen (`../templates/topic-note.md`), MOCs (`../templates/moc.md`) und verifizierte Normalized-Documents nach Promotion aus `research/`.

## Verzeichnis-Struktur

```text
knowledge/
  README.md                 # diese Datei
  INDEX.md                  # GENERIERT: angeheftet + zuletzt geaendert (Boot, max. 8 KB)
  _typen/<typ>.md           # GENERIERT: eine Zeile je Notiz (<= 50 je Teil)
  person/ preference/ project/ decision/ reference/ concept/ question/
    <praefix>-<datum>-<slug>-<4hex>.md   # eine Notiz
  _index.md                 # optional: Root-MOC des Themen-Graphen
  <topic>/_moc.md           # optional: Topic-MOC
  <topic>/<slug>.md         # optional: Topic-Notiz (Langform)
```

Typ-Ordner und `_typen/` sind reserviert und keine Topic-Namen.

## Arbeitsweise

```text
python -m harness.mdmemory new decision "Fiktive Entscheidung" --source journal:<pfad>   # Skelett
python -m harness.mdmemory index     # INDEX.md, _typen/, Sichten unter state/ neu erzeugen
python -m harness.mdmemory lint      # Schema, Supersede-Ketten, Aktualitaet, Boot-Budget
```

- Jede Notiz hat mindestens eine Quelle (`sources`). Eine Aussage aus einer Session verweist auf das Journal.
- `summary` wird 1:1 in den Index kopiert, deshalb ein Satz mit hoechstens 120 Zeichen und ohne URL.
- Ersetzen statt Ueberschreiben: Die neue Notiz setzt `supersedes`, die alte bekommt `superseded_by` und `status: superseded`. Mit `change: korrigiert` war die alte falsch, mit `veraendert` hat sich die Welt geaendert.
- Personenbezogenes: `sensitivity: personal` (Standard bei `person`). Titel und Summary erscheinen dann in keinem Index. Private Inhalte gehoeren besser in ein separates Repo, weil Daten aus der git-Historie kaum zu loeschen sind.
- Alt-IDs aus den frueheren Registern (`D-…`, `Q-…`, `A-…`, `R-…`) bleiben als `aliases` gueltig.

Ohne installierten Harness lassen sich Notizen von Hand aus der Vorlage anlegen. `INDEX.md`, `_typen/` und die Sichten unter `state/` veralten dann, bis jemand `python -m harness.mdmemory index` ausfuehrt. Die Notizen selbst bleiben die gueltige Quelle.

## Naming-Konvention

ASCII, kebab-case, ohne Leerzeichen und ohne Umlaute. Die Notiz-ID vergibt `new`. Das Zufalls-Suffix verhindert, dass zwei parallele Worktrees dieselbe Datei anlegen. Topic-Verzeichnisse bekommen kurze, generische Namen.

## Link-Disziplin

- `links:` im Frontmatter fuer Notiz-zu-Notiz-Verweise (IDs oder Aliase; lint prueft, dass sie existieren).
- `[[wiki-link]]` fuer Verbindungen im Themen-Graphen, `[label](pfad)` fuer Verweise auf Nicht-KG-Knoten.
- Geplante, noch fehlende Topic-Links: Ziel als Stub mit `status: planned` anlegen. Tote Links nicht stillschweigend entfernen.

## Lifecycle

- Notizen werden aktualisiert oder ersetzt, **nie geloescht**: `superseded`, `retracted`, `archived`.
- Langform-Notizen, die veraltet sind, wandern nach `archive/YYYY-MM-DD-<slug>.md`.
- Pruef-Trigger: `review_after` ueberschritten oder 180 Tage ohne `last_confirmed`. Die Pflege meldet beides.

## Lade-Regel

`INDEX.md` wird beim Boot geladen. Danach nur gezielt einen Unterindex oder eine Notiz lesen, nie den ganzen Ordner. Siehe `../context-policy.md` §3 und `../knowledge-graph-policy.md` §8.

## Beziehung zu State-Dateien

Die Register `state/decisions.md`, `open-questions.md`, `assumptions.md` und `risks-and-constraints.md` sind generierte Sichten auf die Notizen hier. `state/now.md`, `journal/`, `state/source-registry.md` und `state/artifact-index.md` bleiben eigene Quellen, auf die Notizen verweisen.

## Beziehung zu Project Data Space und RAG

Notizen koennen auf Original-Binaerdateien (ueber Source-Registry-IDs) und auf Data-Space-Manifeste zeigen. **RAG oder Volltextsuche ist, falls vorhanden, nur eine Suchschicht** und niemals Source of Truth.

## Cross-Links

- Schema: `../templates/knowledge-note.md` · Langform: `../templates/topic-note.md` · MOC: `../templates/moc.md`
- KG-Policy: `../knowledge-graph-policy.md` · Lade-Regeln: `../context-policy.md` · Quality-Gates: `../quality-gates.md`
- Source-Registry: `../state/source-registry.md`

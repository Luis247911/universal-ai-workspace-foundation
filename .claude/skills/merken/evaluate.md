# evaluate — merken

Bewertet, ob Journal-Eintraege korrekt, belegt und ohne Datenverlust zu Notizen werden. Die
mechanischen Teile prueft `tests/test_mdmemory_consolidate.py`; die Szenarien unten pruefen das
Urteil. Alle Inhalte sind fiktiv.

## Rubrik

| Dimension | Bestanden, wenn |
|-----------|-----------------|
| Operation | Die gewaehlte Operation (NOOP/ADD/UPDATE/SUPERSEDE/CONFLICT) passt zum Bestand. |
| Belege | Jede neue oder geaenderte Notiz hat mindestens eine Quelle, die auf das Journal zeigt. |
| Kette | Bei SUPERSEDE sind beide Seiten gesetzt, die alte Notiz ist `superseded`, nichts geloescht. |
| Rueckfrage | Bei person, preference global, SUPERSEDE/korrigiert und CONFLICT wird vorher gefragt. |
| Idempotenz | Ein zweiter Lauf ueber dasselbe Journal erzeugt keinen Diff. |
| Extern | Inhalte aus Web/Tools tragen `origin: external`; ihre Summary steht nicht im Index. |
| Abschluss | `mdmemory index` und `lint` laufen, lint zeigt 0 Fehler, das Journal ist eingefroren. |

## Szenario 1 — neue Decision aus dem Journal (ADD)

- **Journal**: `### 10:12 · entscheidung` — "Das Beispielteam legt Protokolle nur noch als Markdown ab."
- **Bestand**: keine aehnliche Notiz (`candidates` liefert nichts ueber 0.2).
- **No-Skill-Baseline**: haengt den Satz an eine Sammeldatei an oder vergisst ihn; keine Quelle.
- **Erwartet**: ADD ohne Rueckfrage, Notiz `knowledge/decision/dec-…md` mit
  `sources: [journal:<pfad>]`, danach index + lint, Journal `konsolidiert: true`.

## Szenario 2 — die Welt hat sich geaendert (SUPERSEDE, veraendert)

- **Bestand**: aktive Notiz "Wochentreffen des Beispielteams ist dienstags".
- **Journal**: "Ab Mai ist das Wochentreffen donnerstags."
- **No-Skill-Baseline**: ueberschreibt die alte Notiz; die Historie ist weg.
- **Erwartet**: Rueckfrage, dann neue Notiz + `supersede <alt> <neu> --change veraendert`; alte
  Notiz `superseded`, `valid_until` gesetzt, beide Verlauf-Zeilen vorhanden.

## Szenario 3 — Widerspruch ohne Klaerung (CONFLICT)

- **Bestand**: Notiz A "Ablage fuer Anhaenge ist der Projektordner".
- **Journal**: eine andere Session notierte "Anhaenge liegen im Archivsystem".
- **No-Skill-Baseline**: waehlt still eine Variante oder behaelt beide als aktiv.
- **Erwartet**: Rueckfrage; ohne Klaerung `mdmemory conflict A B "<frage>"`: angeheftete
  Frage mit `kind: conflict`, beide Notizen unveraendert.

## Szenario 4 — externe Behauptung (ADD, extern)

- **Journal**: Ein Web-Artikel behauptet eine Leistungszahl eines fiktiven Werkzeugs.
- **No-Skill-Baseline**: uebernimmt die Zahl als bestaetigten Fakt in den Index.
- **Erwartet**: `reference`-Notiz mit `origin: external`, `confidence: unbestaetigt`,
  `sources: [url:…]`; der Index zeigt nur die ID.

## Szenario 5 — bekannte Praeferenz, zweiter Lauf (NOOP, Idempotenz)

- **Bestand**: Praeferenz "Antworten kurz halten" existiert und ist aktiv.
- **Journal**: bestaetigt sie erneut.
- **No-Skill-Baseline**: legt eine Dublette an.
- **Erwartet**: NOOP, hoechstens `confirm <id>`; ein zweiter Durchlauf aendert keine Datei.

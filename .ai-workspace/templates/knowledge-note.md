---
id: <prefix>-<YYYY-MM-DD>-<slug>-<4hex>
type: <person|preference|project|decision|reference|concept|question>
title: <kurzer Titel, max. 100 Zeichen>
summary: <ein Satz, max. 120 Zeichen, keine URL; wird 1:1 in den Index kopiert>
aliases: []
status: active
valid_from: <YYYY-MM-DD>
valid_until:
supersedes: []
superseded_by:
change:
confidence: bestaetigt
sources: [<art>:<verweis>]
links: []
scope: project
sensitivity: normal
origin: internal
pinned: false
updated: <YYYY-MM-DD>
last_confirmed: <YYYY-MM-DD>
review_after:
---
## Inhalt

<Die eigentliche Aussage in wenigen Saetzen. Eine Notiz, ein Gedanke.>

## Belege

- <Journal-Eintrag, Quelle oder Gespraech, aus dem die Aussage stammt>

## Verlauf

- <YYYY-MM-DD> · angelegt

<!--
Schema v1 der atomaren Gedaechtnis-Notiz (D-2026-09-30-04). Ablage: knowledge/<typ>/<id>.md.
Skelett mit allen Feldern: python -m harness.mdmemory new <typ> "<titel>" [--alias D-…|auto]
Danach: python -m harness.mdmemory index  (INDEX.md, _typen/, Register-Sichten)
Pruefen: python -m harness.mdmemory lint   (Fehler brechen CI)
Die Code-Quelle des Schemas ist src/harness/mdmemory/notes.py; bei Abweichung gilt der Code.

Pflichtfelder (alle Schluessel muessen vorhanden sein, Werte duerfen leer sein ausser):
  id, type, title, summary, status, valid_from, updated, sources (mind. ein Eintrag)

id          Praefix je Typ: person per · preference pref · project proj · decision dec ·
            reference ref · concept con · question q. Gleich dem Dateinamen ohne .md.
aliases     Alte oder sprechende IDs (D-2026-06-04-01, Q-…, A-…, R-…). Global eindeutig.
status      active | superseded | retracted | archived. Nie loeschen, nur Status aendern.
valid_from / valid_until
            Gueltigkeitszeitraum. Beim Ersetzen setzt die alte Notiz valid_until.
supersedes / superseded_by
            Immer beidseitig: neue Notiz supersedes [alt], alte Notiz superseded_by neu und
            status superseded. Lint prueft Symmetrie und Zyklen.
change      leer | veraendert (die Welt hat sich geaendert) | korrigiert (die alte Notiz war falsch)
confidence  bestaetigt | unbestaetigt
sources     Liste <art>:<verweis>, art = journal | url | legacy | automemory | system | note | user.
            Beispiele: journal:2031/03/2031-03-04-1a2b3c4d.md, url:https://example.org/spec
links       IDs oder Aliase verwandter Notizen (muessen existieren).
scope       project | global (global = gilt ueber dieses Projekt hinaus, z. B. Arbeitsweise)
sensitivity normal | personal | restricted. personal/restricted: Titel und Summary erscheinen
            in keinem generierten Index, nur die ID. person-Notizen standardmaessig personal.
origin      internal | external. external (z. B. aus Web oder fremden Dateien): nie Summary im Index.
pinned      true | false. Angeheftete Notizen stehen immer im Boot-Index (max. 20).
updated / last_confirmed / review_after
            Letzte Aenderung, letzte Bestaetigung, naechste Pruefung (Pflege meldet Ueberfaelliges).

Typ-spezifische Zusatzfelder (ebenfalls Pflicht-Schluessel):
  person      relation, context (arbeit | privat)
  preference  applies_to (tool | project | global)
  project     phase, external_ref (Pointer auf das externe System; Tasks/Status/KPIs nie hier)
  decision    alternatives [], reversibility (reversible | hard-to-reverse | irreversible), decided_by
  question    kind (question | assumption | risk | constraint | conflict), blocks [], resolution

Koerper: freie ## Abschnitte. "Belege", "Verlauf" und "Beziehungen" sind reserviert.
Migrierte Notizen tragen zusaetzlich legacy_keys (fuer den verlustfreien Export).
Alle Beispiele in dieser Vorlage sind fiktiv.
-->

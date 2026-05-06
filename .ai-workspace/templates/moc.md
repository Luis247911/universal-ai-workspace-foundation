---
id: <moc-slug>
type: moc
title: "<topic-titel>"
status: active
created: <YYYY-MM-DD>
updated: <YYYY-MM-DD>
owner: <user-or-adapter>
scope: "<topic-beschreibung>"
review_after: <YYYY-MM-DD>
---

# MOC: `<topic-titel>`

Vorlage fuer eine Map of Content (Topic-Index im Knowledge-Graph). Lebt unter `knowledge/_index.md` (Root) oder `knowledge/<topic>/_moc.md` (Topic-MOC).

MOCs **sammeln Links, ersetzen aber niemals State-Dateien**. Ein MOC referenziert State-Eintraege (z.B. `[[D-IDs]]`), dupliziert sie aber nicht.

## 1. Thema

`<1-2 saetze: was deckt dieses moc ab>`

## 2. Zweck

`<warum existiert dieses moc; welche frage beantwortet es einer suchenden person>`

## 3. Scope

- **In scope:** `<was deckt dieses moc ab>`.
- **Nicht in scope:** `<abgrenzung zu benachbarten mocs>`.

## 4. Zentrale Links

Liste der wichtigsten Knowledge-Notes mit `[[wiki-link]]` + 1-Satz Kontext.

- `[[<knowledge-note-1>]]` — `<kontext>`
- `[[<knowledge-note-2>]]` — `<kontext>`

(noch keine)

## 5. Relevante State-Dateien

Verweise auf relevante State-Eintraege.

- Decisions: `[[D-YYYY-MM-DD-NN]]` — `<kontext>`
- Open Questions: `[[Q-YYYY-MM-DD-NN]]` — `<kontext>`
- Risks: `[[R-YYYY-MM-DD-NN]]` — `<kontext>`
- Annahmen: `[[A-YYYY-MM-DD-NN]]` — `<kontext>`

(noch keine)

## 6. Relevante Research-Dateien

Verweise auf `research/<...>.md`.

(noch keine)

## 7. Relevante Deliverables

Verweise auf `deliverables/<...>.md`.

(noch keine)

## 8. Relevante Adapter

Welche Adapter beruehren dieses Topic?

(noch keine)

## 9. Offene Fragen

Verweise auf `Q-IDs`, die noch nicht beantwortet sind.

(noch keine)

## 10. Review-Datum

`<YYYY-MM-DD>` — wann dieses MOC wieder gepflegt werden sollte.

## Cross-Links

- KG-Policy: `../knowledge-graph-policy.md`.
- Knowledge-Note-Template: `knowledge-note.md`.

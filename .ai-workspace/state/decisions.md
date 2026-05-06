---
id: decisions
type: decisions
title: "Decision Log"
status: active
created: <YYYY-MM-DD>
updated: <YYYY-MM-DD>
owner: <user>
---

# Decisions

Append-only Decision-Log. **Kanonisch in v2** (keine Per-Decision-Files). Per-Decision-Files koennen erst durch einen Adapter eingebracht werden, falls explizit noetig — Adapter darf diese Datei aber nicht ersetzen.

## Format pro Eintrag

```text
- ID: D-YYYY-MM-DD-NN
- Datum: YYYY-MM-DD
- Entscheidung: <1 satz>
- Begruendung: <1-3 saetze>
- Status: <active / superseded>
- Reversibilitaet: <reversible / hard-to-reverse / irreversible>
- Follow-up-Date: <YYYY-MM-DD oder leer>
- Supersedes: <fruehere D-ID, falls ersetzt, oder leer>
```

## Sortierung

Konsistent neueste zuerst (oder aelteste zuerst — eine Konvention pro Projekt; per Adapter dokumentierbar). Diese Foundation-Vorlage nutzt **neueste zuerst**.

## Aktive Eintraege

(noch keine)

## Cross-Links

- Annahmen: `assumptions.md`.
- Decision-Record-Template: `../templates/decision-record.md`.
- Behavior: `../protocol.md`.

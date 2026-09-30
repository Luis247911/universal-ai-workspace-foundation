---
id: dec-2026-09-30-memory-vertrag-besitz-ladevertrag-2a34
type: decision
title: "Memory-Vertrag: Besitz, Ladevertrag, Schreibwege und fuenf Festlegungen"
summary: Markdown kanonisch, Auto-Memory aus, scope/sensitivity, nur lokal, merken fragt bei heiklen Faellen
aliases: [D-2026-09-30-08]
status: active
valid_from: 2026-09-30
valid_until:
supersedes: []
superseded_by:
change:
confidence: bestaetigt
sources: [user:auftrag-2026-09-30-memory-phase-4]
links: [D-2026-09-30-04, D-2026-09-30-06]
scope: project
sensitivity: normal
origin: internal
pinned: false
updated: 2026-09-30
last_confirmed: 2026-09-30
review_after:
alternatives: [Auto-Memory parallel weiterlaufen lassen, Datenbank als Quelle, MCP-Server sofort]
reversibility: reversible
decided_by: user
---
## Entscheidung

`memory-contract.md` ist die Uebersicht darueber, wer welches Gedaechtnis besitzt, laedt und schreibt. Dazu gehoeren die Besitz-Tabelle, der Ladevertrag und die Schreibwege. Fuenf Festlegungen gelten:

1. **Markdown in git ist kanonisch** fuer Wissen, Decisions und Praeferenzen. Operative Daten (Tasks, Status, KPIs) bleiben extern, Notizen verweisen nur per `external_ref` darauf.
2. **Claude Auto-Memory ist aus**, ueber `"autoMemoryEnabled": false` in `.claude/settings.json`. Pro Maschine geht auch `CLAUDE_CODE_DISABLE_AUTO_MEMORY=1`. Bestandsnotizen holt `import-automemory` als Journal-Kandidaten herein.
3. **`scope` und `sensitivity` an jeder Notiz.** Der globale Namespace ist optional und standardmaessig aus; er wird ueber `UAW_GLOBAL_MEMORY_DIR` eingeschaltet. Private Inhalte gehoeren in ein separates Repo.
4. **Nur lokal**: Claude Code und Codex. Ein spaeterer MCP-Server liest nur und schreibt hoechstens Journal-Vorschlaege (`tool: mcp-proposal`).
5. **`merken` schreibt direkt**, fragt aber vorher bei `person`, bei `preference` mit globalem Scope, bei SUPERSEDE bzw. Korrektur und bei CONFLICT.

Die Pflege laeuft woechentlich ueber den Skill `pflege`. Ergebnis ist ein Bericht oder ein PR, nie ein Auto-Merge. Die Qualitaet misst ein Recall-Set mit 30 Fragen. Suche kommt erst bei einer Trefferquote unter 90 % in Betracht.

## Begruendung

Zwei Gedaechtnisse fuer dasselbe Projekt driften auseinander. Auto-Memory liegt ausserhalb des Repos, ist fuer Codex und fuer andere Clones unsichtbar und laesst sich nicht reviewen. Ein einziger, versionierter Ort ist pruefbar (lint, CI) und fuer jedes Tool gleich.

Die Rueckfragen verhindern, dass personenbezogene oder weitreichende Aenderungen still entstehen. Auf alltaegliche Eintraege wird dabei nicht gebremst.

## Belege

- `tests/test_mdmemory_maintenance.py`: Auto-Memory ist in den Projekt-Settings aus, der globale Namespace ist standardmaessig aus, der Pflege-Bericht aendert keine Notiz, die Recall-Vorlage hat 30 Fragen.

## Verlauf

- 2026-09-30 · angelegt

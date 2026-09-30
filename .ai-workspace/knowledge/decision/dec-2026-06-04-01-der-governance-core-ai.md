---
id: dec-2026-06-04-01-der-governance-core-ai
type: decision
title: Der Governance-Core (.ai-workspace/) bleibt eingefroren markdown-only und…
summary: Der Governance-Core (.ai-workspace/) bleibt eingefroren markdown-only und motorlos; jede ausfuehrbare Automatik lebt…
aliases: [D-2026-06-04-01]
status: superseded
valid_from: 2026-06-04
valid_until: 2026-09-30
supersedes: []
superseded_by: dec-2026-09-30-05-skripte-unter-src-duerfen
change:
confidence: bestaetigt
sources: ["legacy:state/decisions.md#D-2026-06-04-01"]
links: []
scope: project
sensitivity: normal
origin: internal
pinned: false
updated: 2026-09-30
last_confirmed: 2026-06-04
review_after:
alternatives: []
reversibility: hard-to-reverse
decided_by:
legacy_keys: [ID, Datum, Status, Reversibilitaet, Follow-up-Date, Supersedes]
---
Migriert aus `state/decisions.md` am 2026-09-30.

## Entscheidung

Der Governance-Core (`.ai-workspace/`) bleibt eingefroren markdown-only und motorlos; jede ausfuehrbare Automatik lebt ausschliesslich unter `.claude/` bzw. `src/` (gesegnete Execution-Mounts, AGENTS.md §3/§8).

## Begruendung

Die Trennung von Haltung (Governance/State/Memory als auditierbares Markdown) und Motor (versionierter Execution-Code) haelt den Core tool-agnostisch und die 2-Invarianten-Pytest gruen. Bewusst KEINE selbst-feuernde Routine im Core (security-policy.md §7).

## Verlauf

- 2026-09-30 · migriert aus `state/decisions.md` (Alt-ID D-2026-06-04-01)
- 2026-09-30 · abgeloest durch D-2026-09-30-05 (Skripte duerfen abgeleitete Dateien schreiben)

---
id: dec-2026-06-06-01-ein-einmaliges-erst-start
type: decision
title: Ein einmaliges Erst-Start-Onboarding feuert DEFAULT AN…
summary: Ein einmaliges Erst-Start-Onboarding feuert DEFAULT AN (additionalContext-Stups via SessionStart-Hook…
aliases: [D-2026-06-06-01]
status: active
valid_from: 2026-06-06
valid_until:
supersedes: []
superseded_by:
change:
confidence: bestaetigt
sources: ["legacy:state/decisions.md#D-2026-06-06-01"]
links: []
scope: project
sensitivity: normal
origin: internal
pinned: false
updated: 2026-06-06
last_confirmed: 2026-06-06
review_after:
alternatives: []
reversibility: reversible
decided_by:
legacy_keys: [ID, Datum, Status, Reversibilitaet, Follow-up-Date, Supersedes]
---
Migriert aus `state/decisions.md` am 2026-09-30.

## Entscheidung

Ein einmaliges Erst-Start-Onboarding feuert DEFAULT AN (additionalContext-Stups via SessionStart-Hook `first_run_onboarding` in `.claude/`, startup-Matcher) und ruft `/start` auf. Es startet ein Gespraech, schreibt keine Config/Governance-State, entfernt sich nicht selbst; es wird inert ueber den gitignored Marker `.claude/.onboarding-state.json` (status done/skipped, von `/start` geschrieben) bzw. wenn die State-Platzhalter gefuellt sind. AUTOMATION.md "feuert nichts" wird entsprechend praezisiert.

## Begruendung

Bewusste, dokumentierte Ausnahme von der Default-AUS-Linie zugunsten Erst-Nutzer-Fuehrung. Abgesichert durch Einmaligkeit, Reversibilitaet, Marker-inert (nie Self-Deletion), reinen Stups (keine Zwangsausfuehrung). `UAW_DISABLE_ONBOARDING` als Maintainer-Escape. Ergaenzt D-2026-06-04-02.

## Verlauf

- 2026-09-30 · migriert aus `state/decisions.md` (Alt-ID D-2026-06-06-01)

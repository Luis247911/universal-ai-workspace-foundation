---
id: dec-2026-06-04-02-eine-optionale-repo-committete
type: decision
title: Eine optionale, repo-committete Session-Automatik-Schicht (boot_reload +…
summary: Eine optionale, repo-committete Session-Automatik-Schicht (boot_reload + recitation_nudge) wird unter .claude/…
aliases: [D-2026-06-04-02]
status: superseded
valid_from: 2026-06-04
valid_until: 2026-09-30
supersedes: []
superseded_by: dec-2026-09-30-03-die-automatik-schicht-unter
change:
confidence: bestaetigt
sources: ["legacy:state/decisions.md#D-2026-06-04-02"]
links: []
scope: project
sensitivity: normal
origin: internal
pinned: false
updated: 2026-09-30
last_confirmed: 2026-06-04
review_after:
alternatives: []
reversibility: reversible
decided_by:
legacy_keys: [ID, Datum, Status, Reversibilitaet, Follow-up-Date, Supersedes]
---
Migriert aus `state/decisions.md` am 2026-09-30.

## Entscheidung

Eine optionale, repo-committete Session-Automatik-Schicht (boot_reload + recitation_nudge) wird unter `.claude/` ergaenzt -- default AUS, reversibel ueber `.claude/automation.flags.json`, gefuehrt durch den Begleiter `/automation`.

## Begruendung

Das Kit bleibt eine Vorlage, die nichts by default ausfuehrt; das Onboarding weist aber auf die opt-in Automatik hin. Jeder Hook ist self-gated (Flag false -> sofort inert) und vollstaendig self-contained im Repo. Beruehrt `~/.claude/` (die globale, private Schicht) nie. Setzt D-2026-06-04-01 voraus: der Motor lebt unter `.claude/`, nicht im Governance-Markdown.

## Verlauf

- 2026-09-30 · migriert aus `state/decisions.md` (Alt-ID D-2026-06-04-02)

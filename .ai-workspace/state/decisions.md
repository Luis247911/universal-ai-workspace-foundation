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

- ID: D-2026-06-06-03
- Datum: 2026-06-06
- Entscheidung: Praezisierung der "Hook liest nur"-Doktrin: Execution-Hooks unter `.claude/` duerfen ihren eigenen ephemeren, gitignored Lauf-Marker schreiben (z.B. `.claude/.daily_maintenance_last`; `/start` schreibt `.claude/.onboarding-state.json`). Verboten bleibt das Schreiben nach `.ai-workspace/**` (Governance-State) und nach `automation.flags.json` (Config) ausser durch Modell/Nutzer.
- Begruendung: Ein 1x/Tag-Hook braucht einen eigenen Timestamp, um nicht mehrfach zu feuern. Die Grenze ist nicht "Hook schreibt nie", sondern "Hook schreibt nie Governance-State/Config". Haelt Invarianten C1/C2 + D-2026-06-04-01 ein.
- Status: active
- Reversibilitaet: reversible
- Follow-up-Date:
- Supersedes:

- ID: D-2026-06-06-02
- Datum: 2026-06-06
- Entscheidung: Eine optionale aktive Pflege-Routine (`daily_maintenance`) wird als opt-in SessionStart-Hook (startup+resume) unter `.claude/` ergaenzt, default AUS. Sie nudged 1x/lokalem-Kalendertag einen Pflege-Pass (scratch/-Einsortierung, KG-Lint tote `[[wiki-links]]`/stale notes, verwaiste Artefakte) gemaess knowledge-graph-policy.md §12 Blueprints; sie schlaegt nur vor, mutiert nie selbst.
- Begruendung: Schliesst die Luecke "keine aktive Routine" (kg-policy.md §7/§12) mit einem Motor in der Execution-Schicht, ohne den motorlosen Governance-Core (D-2026-06-04-01) zu verletzen. Modell prueft + schlaegt vor, Hauptsession verifiziert (delegation-policy.md).
- Status: active
- Reversibilitaet: reversible
- Follow-up-Date:
- Supersedes:

- ID: D-2026-06-06-01
- Datum: 2026-06-06
- Entscheidung: Ein einmaliges Erst-Start-Onboarding feuert DEFAULT AN (additionalContext-Stups via SessionStart-Hook `first_run_onboarding` in `.claude/`, startup-Matcher) und ruft `/start` auf. Es startet ein Gespraech, schreibt keine Config/Governance-State, entfernt sich nicht selbst; es wird inert ueber den gitignored Marker `.claude/.onboarding-state.json` (status done/skipped, von `/start` geschrieben) bzw. wenn die State-Platzhalter gefuellt sind. AUTOMATION.md "feuert nichts" wird entsprechend praezisiert.
- Begruendung: Bewusste, dokumentierte Ausnahme von der Default-AUS-Linie zugunsten Erst-Nutzer-Fuehrung. Abgesichert durch Einmaligkeit, Reversibilitaet, Marker-inert (nie Self-Deletion), reinen Stups (keine Zwangsausfuehrung). `UAW_DISABLE_ONBOARDING` als Maintainer-Escape. Ergaenzt D-2026-06-04-02.
- Status: active
- Reversibilitaet: reversible
- Follow-up-Date:
- Supersedes:

- ID: D-2026-06-04-02
- Datum: 2026-06-04
- Entscheidung: Eine optionale, repo-committete Session-Automatik-Schicht (boot_reload + recitation_nudge) wird unter `.claude/` ergaenzt -- default AUS, reversibel ueber `.claude/automation.flags.json`, gefuehrt durch den Begleiter `/automation`.
- Begruendung: Das Kit bleibt eine Vorlage, die nichts by default ausfuehrt; das Onboarding weist aber auf die opt-in Automatik hin. Jeder Hook ist self-gated (Flag false -> sofort inert) und vollstaendig self-contained im Repo. Beruehrt `~/.claude/` (die globale, private Schicht) nie. Setzt D-2026-06-04-01 voraus: der Motor lebt unter `.claude/`, nicht im Governance-Markdown.
- Status: active
- Reversibilitaet: reversible
- Follow-up-Date:
- Supersedes:

- ID: D-2026-06-04-01
- Datum: 2026-06-04
- Entscheidung: Der Governance-Core (`.ai-workspace/`) bleibt eingefroren markdown-only und motorlos; jede ausfuehrbare Automatik lebt ausschliesslich unter `.claude/` bzw. `src/` (gesegnete Execution-Mounts, AGENTS.md §3/§8).
- Begruendung: Die Trennung von Haltung (Governance/State/Memory als auditierbares Markdown) und Motor (versionierter Execution-Code) haelt den Core tool-agnostisch und die 2-Invarianten-Pytest gruen. Bewusst KEINE selbst-feuernde Routine im Core (security-policy.md §7).
- Status: active
- Reversibilitaet: hard-to-reverse
- Follow-up-Date:
- Supersedes:

## Cross-Links

- Annahmen: `assumptions.md`.
- Decision-Record-Template: `../templates/decision-record.md`.
- Behavior: `../protocol.md`.

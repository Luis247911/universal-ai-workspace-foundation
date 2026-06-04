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

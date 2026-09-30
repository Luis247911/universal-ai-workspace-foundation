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

- ID: D-2026-09-30-03
- Datum: 2026-09-30
- Entscheidung: Die Automatik-Schicht unter `.claude/` bleibt opt-in und default AUS. Ausnahmen mit default AN sind der einmalige Erst-Start-Stups `first_run_onboarding` (D-2026-06-06-01) und `now_init` (SessionStart: legt die lokale `state/now.md` an, haelt 4 KB ein, nennt Session-Kurz-ID und Journal-Pfad). Jeder Hook bleibt self-gated ueber `.claude/automation.flags.json`, reversibel und beruehrt `~/.claude/` nie.
- Begruendung: Ohne `now_init` fehlt in jedem frischen Clone und jedem neuen Worktree die Boot-Datei `now.md`, weil sie gitignored ist. Der Hook ist deterministisch, schnell und schreibt keine Inhalte der Arbeit. Uebernimmt den Rest von D-2026-06-04-02 unveraendert.
- Status: active
- Reversibilitaet: reversible
- Follow-up-Date:
- Supersedes: D-2026-06-04-02

- ID: D-2026-09-30-02
- Datum: 2026-09-30
- Entscheidung: Schreib-Doktrin fuer Execution-Hooks. Ein Hook darf (a) seinen eigenen ephemeren, gitignored Lauf-Marker unter `.claude/` schreiben, (b) die gitignored, worktree-lokale `state/now.md` aus der Vorlage anlegen und auf 4 KB kuerzen, (c) den dabei entstehenden Ueberlauf ans Ende des eigenen Session-Journals anhaengen (Datei anlegen, falls sie fehlt). Verboten bleiben: bestehende Inhalte aendern, fremde Journale, Notizen, Decisions oder andere State-Dateien beschreiben, `automation.flags.json` aendern.
- Begruendung: `now.md` ist gitignored und hat eine harte Groessengrenze; beides laesst sich nur mechanisch zuverlaessig einhalten. Der Ueberlauf wandert verlustfrei ins Journal statt verworfen zu werden. Alle geschriebenen Dateien sind `.md`, die Invarianten C1/C2 bleiben gruen. Uebernimmt die Marker-Regel aus D-2026-06-06-03.
- Status: active
- Reversibilitaet: reversible
- Follow-up-Date:
- Supersedes: D-2026-06-06-03

- ID: D-2026-09-30-01
- Datum: 2026-09-30
- Entscheidung: Der Live-Zustand liegt in `state/now.md` (gitignored, pro Worktree, harte Grenze 4 KB, Trim ins Journal). Die Historie liegt im neuen Mount `journal/YYYY/MM/<datum>-<kurzid>.md`: eine Datei pro Session, nur ergaenzt, waehrend der Arbeit nach jedem relevanten Ergebnis geschrieben, Never Auto-Load, nach Konsolidierung unveraenderlich. `state/current-session.md` entfaellt; ihr Inhalt ist als `journal/2026/09/2026-09-30-migration.md` byte-genau gesichert, Migrationspfad `python -m harness.mdmemory now migrate`.
- Begruendung: Eine geteilte, ueberschriebene Datei verliert zwischen zwei Commits jede fruehere Fassung und erzeugt bei zwei parallelen Sessions in jedem Fall einen Merge-Konflikt (gemessen: 100 %; mit now.md + Journal: 0 %, Test `tests/test_parallel_sessions.py`). Eine Datei pro Session hat genau einen Schreiber. Schreiben waehrend der Arbeit statt am Ende schuetzt vor Verlust bei hartem Abbruch, weil kein Hook den Abbruch zuverlaessig abfaengt.
- Status: active
- Reversibilitaet: reversible
- Follow-up-Date:
- Supersedes: D-2026-06-07-01

- ID: D-2026-06-07-02
- Datum: 2026-06-07
- Entscheidung: Vier zusaetzliche opt-in Execution-Hooks unter `.claude/` (default AUS): `prompt_optimizer` (UserPromptSubmit, vage-Prompt-Disambiguierung), `external_content_guard` (PostToolUse WebFetch|WebSearch, Quarantaene-Reminder + optionale gitignored Projekt-Deny-Liste), `compact_nudge` (PostToolUse, periodischer Strategic-Compact-Vorschlag via gitignored Zaehler-Marker), `session_state_guard` (PostToolUse Write|Edit|NotebookEdit, staleness-gegateter, gedrosselter Reminder, `current-session.md` zu sichern). Statisch + additiv in `settings.json` registriert; bestehende Hooks (inkl. `first_run_onboarding` default AN) unveraendert.
- Begruendung: Ergaenzt die Phase-1-Skills (external-content-security, strategic-compact, prompt-optimizer) um ihre opt-in Durchsetzungs-/Erinnerungs-Schicht. Jeder Hook self-gated (Flag false -> inert), advisory (kein exit 2, kein Governance-State-Write), Marker gemaess D-2026-06-06-03. `session_state_guard` beantwortet "Per-Turn-Reminder nervt" durch Staleness-Gating statt Per-Event-Nudge. Haelt C1/C2 + D-2026-06-04-01.
- Status: active
- Reversibilitaet: reversible
- Follow-up-Date:
- Supersedes:

- ID: D-2026-06-07-01
- Datum: 2026-06-07
- Entscheidung: Durability-Modell von `current-session.md` ist kanonisch die lebende Datei + git-Historie (kein mechanischer Pro-Session-Archiv-Rotations-Kreislauf). Overwrite ist non-destruktiv via git (getrackte Datei); `archive/` bleibt fuer semantische Snapshots. `session-contract.md` §3 / `current-session.md` §5 entsprechend praezisiert. Ein zuverlaessiger End-of-Session-Auto-Write ist nicht machbar (harter Kill feuert keinen Hook; Hook schreibt keinen Governance-State); Absicherung = kontinuierliche Frische (opt-in `session_state_guard`) + Commit-Disziplin.
- Begruendung: Macht die implizite Design-Entscheidung explizit und beantwortet die wiederkehrende Frage Rotation-vs-Overwrite. git ist bereits die Versionshistorie -> Rotation waere redundant + Churn. Haelt den motorlosen Governance-Core (D-2026-06-04-01); der Reminder lebt in der Execution-Schicht.
- Status: superseded
- Reversibilitaet: reversible
- Follow-up-Date:
- Supersedes:

- ID: D-2026-06-06-03
- Datum: 2026-06-06
- Entscheidung: Praezisierung der "Hook liest nur"-Doktrin: Execution-Hooks unter `.claude/` duerfen ihren eigenen ephemeren, gitignored Lauf-Marker schreiben (z.B. `.claude/.daily_maintenance_last`; `/start` schreibt `.claude/.onboarding-state.json`). Verboten bleibt das Schreiben nach `.ai-workspace/**` (Governance-State) und nach `automation.flags.json` (Config) ausser durch Modell/Nutzer.
- Begruendung: Ein 1x/Tag-Hook braucht einen eigenen Timestamp, um nicht mehrfach zu feuern. Die Grenze ist nicht "Hook schreibt nie", sondern "Hook schreibt nie Governance-State/Config". Haelt Invarianten C1/C2 + D-2026-06-04-01 ein.
- Status: superseded
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
- Status: superseded
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

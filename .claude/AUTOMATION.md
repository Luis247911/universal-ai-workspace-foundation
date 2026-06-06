# AUTOMATION.md — Opt-in Automatik-Schicht (Execution-Layer)

Kanonische Operator-Doku der **optionalen** Session-Automatik dieses Kits. Diese Schicht ist
**Execution-Layer** (`.claude/`), nicht Governance — der Governance-Core (`.ai-workspace/`)
bleibt markdown-only und motorlos (siehe `state/decisions.md` D-2026-06-04-01).

> **Default: AUS** fuer alle *wiederkehrenden* Helfer (`boot_reload`, `recitation_nudge`,
> `daily_maintenance`). Einzige Ausnahme: frisch geklont feuert **genau ein einmaliger,
> reversibler Onboarding-Stups** beim ersten Start (`first_run_onboarding`, default AN, ruft
> `/start` auf) -- und sonst nichts. Aktivierung/Deaktivierung ist opt-in, reversibel und wird
> durch den Begleiter `/uaw-automation` gefuehrt.

## In einfachen Worten

Dieses Projekt kann dir drei kleine Helfer einschalten:

- **"Stand wieder laden":** Startest du Claude neu, liest es automatisch die Notiz wieder, woran
  ihr zuletzt gearbeitet habt. Du musst nichts neu erklaeren.
- **"Ans Mitschreiben erinnern":** Nach einer Datei-Aenderung stupst es Claude an, die Notiz
  aktuell zu halten.
- **"Taegliche Pflege-Erinnerung":** Einmal pro Tag stupst es Claude an, kurz aufzuraeumen
  (scratch/ einsortieren, tote Verweise + alte Notizen pruefen). Nur eine Erinnerung -- es loescht
  nie von selbst.

Alle drei sind **aus**, bis du sie einschaltest, **jederzeit umkehrbar**, und sie wirken **nur in
diesem Projekt**. Am einfachsten steuerst du sie mit dem Begleiter `/uaw-automation` (fuehrt dich
Schritt fuer Schritt durch). Zusaetzlich begruesst dich beim allerersten Start ein einmaliges
Onboarding (`/start`) -- das einzige, was frisch geklont von selbst anspringt. Der Rest dieser
Datei ist die technische Referenz.

## Harte Grenze

Steuert ausschliesslich dieses Repo. Liest/kopiert/veraendert **nie** `~/.claude/` (globale,
private Claude-Code-Schicht). 100 % repo-committed und self-contained (Python-stdlib, keine
externen Abhaengigkeiten, kein API).

## Faehigkeiten

| Flag | Event | Was es tut | Prinzip |
|---|---|---|---|
| `boot_reload` | `SessionStart` | Liest `.ai-workspace/state/current-session.md` und speist es als `additionalContext` ein -> jede neue/resumte/gecleart/compactete Session bootet mit dem Live-State. | Hook liest nur, was das Modell schrieb. |
| `recitation_nudge` | `PostToolUse` | Nach Write/Edit/NotebookEdit ein kurzer Reminder, `current-session.md` fortzuschreiben (Task + naechster Schritt + Evidenz, `session-contract.md` §3). | Hook erinnert, **Modell schreibt**. |
| `first_run_onboarding` | `SessionStart` (startup) | Bei frischem, uneingerichtetem Workspace (State-Platzhalter da, kein Onboarding-Marker) speist es einen Stups ein: begruesse den Nutzer + starte `/start`. **Default AN.** Escape: `UAW_DISABLE_ONBOARDING`. | Hook stupst nur an; `/start` + Modell handeln. |
| `daily_maintenance` | `SessionStart` (startup+resume) | Beim ersten Start eines lokalen Kalendertages ein Pflege-Pass-Vorschlag (scratch/ einsortieren, tote `[[wiki-links]]`/stale notes, verwaiste Artefakte). Schreibt nur seinen gitignored Datums-Marker. | Hook erinnert + schreibt nur eigenen Lauf-Marker, **Modell schlaegt vor/handelt**. |

Die beiden Recitation-Helfer (`boot_reload`/`recitation_nudge`) setzen die Manus-Lehre lokal um:
**kontinuierliche Recitation + Reload beim Boot**. Der State ueberlebt Compaction nicht, weil ein
Hook den Moment abfaengt, sondern weil er laufend frisch ist und bei jedem Boot neu eingespeist wird.

**Marker-Doktrin (D-2026-06-06-03).** Die Grenze ist nicht "Hook schreibt nie", sondern: ein Hook
darf seinen **eigenen ephemeren, gitignored Lauf-Marker** unter `.claude/` schreiben
(`daily_maintenance` schreibt `.daily_maintenance_last`; `/start` schreibt `.onboarding-state.json`)
-- aber **nie** Governance-State (`.ai-workspace/**`) oder die Config (`automation.flags.json`).
Das halten die Invarianten C1/C2 und D-2026-06-04-01 ein.

## Dateien

- `.claude/automation.flags.json` — die Toggles. Default `{ "first_run_onboarding": true, "boot_reload": false, "recitation_nudge": false, "daily_maintenance": false }`.
- `.claude/hooks/_flags.py` — stdlib-Helper: Repo-Root (`CLAUDE_PROJECT_DIR`, sonst aus `__file__`) + Flag lesen. Jeder Fehler -> `False` (fail-safe).
- `.claude/hooks/boot_reload.py` — SessionStart-Handler, self-gated auf `boot_reload`.
- `.claude/hooks/recitation_nudge.py` — PostToolUse-Handler, self-gated auf `recitation_nudge`.
- `.claude/hooks/first_run_onboarding.py` — SessionStart(startup)-Handler, self-gated auf `first_run_onboarding` (default AN) + Onboarding-Marker + State-Platzhalter + `UAW_DISABLE_ONBOARDING`-Escape.
- `.claude/hooks/daily_maintenance.py` — SessionStart(startup+resume)-Handler, self-gated auf `daily_maintenance`; schreibt gitignored `.daily_maintenance_last`.
- `.claude/commands/start.md` — der Erst-Start-Dirigent (`/start`); schreibt den gitignored Onboarding-Marker `.onboarding-state.json` (status done/skipped).
- `.claude/settings.json` -> `hooks`-Block — registriert die Hooks statisch. **Inert bis Flag true** (ausser `first_run_onboarding`, default AN).

## Self-Gating (warum committet sicher ist)

Die Hooks sind in `settings.json` registriert, aber jedes Script liest zuerst seinen Flag. Flag
`false`/fehlt -> sofort `exit 0` ohne Output -> Claude Code sieht nichts (verifiziert: exit 0 +
keine Ausgabe = vollstaendig inert). Aktivieren = einen Boolean kippen, nie JSON-Hook-Chirurgie.

## Aktivieren / Deaktivieren

- **Gefuehrt:** `/uaw-automation` (zeigt Stand, erklaert, kippt nach Bestaetigung).
- **Direkt:** `.claude/automation.flags.json` editieren, Flag auf `true`/`false`.
- **Wirkung:** `boot_reload` ab naechstem Session-Start (`/clear`, Resume, neue Session);
  `recitation_nudge` ab naechster Write/Edit/NotebookEdit-Aktion.
- **Voll-Entfernung:** `hooks`-Block aus `settings.json` + `.claude/hooks/*.py` + `automation.flags.json` loeschen.

## Cross-Surface & Plattform

- Committete `.claude/`-Hooks laufen laut Docs **auch in Web-/Cloud-Sessions**; user-globale
  `~/.claude/`-Hooks reisen nicht mit — darum ist alles repo-lokal + stdlib.
- Launcher ist `python`. Auf manchen Linux-/Web-Umgebungen heisst er `python3`; das ist die
  einzige plattformabhaengige Stelle (in `settings.json`, oder pro Maschine in `settings.local.json`).
- Faellt ein Hook aus (Launcher fehlt, Pfad nicht aufgeloest): **fail-safe inert**, nie blockierend.

## Verifizierte Primitive (Claude-Code-Docs)

- Modell-sichtbarer Kontext: `{"hookSpecificOutput": {"hookEventName": "...", "additionalContext": "..."}}` bei `exit 0`.
- `exit 0` ohne Ausgabe = inert. `exit 2` = blockierend (hier bewusst nie genutzt).
- **SessionStart-Matcher koennen NICHT pipe-alterniert werden** — je `source`
  (startup/resume/clear/compact) ein eigener Matcher-Eintrag. PostToolUse erlaubt `Write|Edit|NotebookEdit`.
- Repo-Root im Command via `$CLAUDE_PROJECT_DIR`.

## Selbsttest (ohne echte Session)

Off-Pfad (Repo wie ausgeliefert) — `daily_maintenance` ist AUS, erwartet je: keine Ausgabe, exit 0:

    '{}' | python .claude/hooks/boot_reload.py
    '{}' | python .claude/hooks/recitation_nudge.py
    '{}' | python .claude/hooks/daily_maintenance.py

`first_run_onboarding` ist **default AN**: im ausgelieferten Template (State-Platzhalter vorhanden,
kein Marker) gibt es das Onboarding-`additionalContext`-JSON aus. Stummschalten via
`UAW_DISABLE_ONBOARDING=1` oder `.claude/.onboarding-state.json` anlegen:

    '{}' | python .claude/hooks/first_run_onboarding.py   # erwartet: hookSpecificOutput-JSON

On-Pfad, ohne die echten Flags zu kippen (Sandbox-Projektdir via `CLAUDE_PROJECT_DIR`):

    $tmp = Join-Path $env:TEMP "uaw-hooktest"
    New-Item -ItemType Directory -Force (Join-Path $tmp ".claude") | Out-Null
    New-Item -ItemType Directory -Force (Join-Path $tmp ".ai-workspace\state") | Out-Null
    '{ "boot_reload": true, "recitation_nudge": true }' | Set-Content -Encoding utf8 (Join-Path $tmp ".claude\automation.flags.json")
    "ACTIVE TASK: test" | Set-Content -Encoding utf8 (Join-Path $tmp ".ai-workspace\state\current-session.md")
    $env:CLAUDE_PROJECT_DIR = $tmp
    '{}' | python .claude/hooks/boot_reload.py        # erwartet: hookSpecificOutput-JSON mit additionalContext
    Remove-Item env:CLAUDE_PROJECT_DIR; Remove-Item -Recurse -Force $tmp

## Verwandte Governance

- `state/decisions.md` — D-2026-06-04-01 (Core-Freeze), D-2026-06-04-02 (opt-in Automatik), D-2026-06-06-01 (default-AN Erst-Start-Onboarding), D-2026-06-06-02 (opt-in Pflege-Routine), D-2026-06-06-03 (Lauf-Marker-Doktrin).
- `session-contract.md` §3.1 — Recitation-Rationale + Pointer auf diese Schicht.
- `adapter-policy.md` §8 — Abgrenzung Automatik-Schicht vs. Adapter/Maintenance-Routine.

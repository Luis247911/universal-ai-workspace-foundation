# AUTOMATION.md — Opt-in Automatik-Schicht (Execution-Layer)

Kanonische Operator-Doku der **optionalen** Session-Automatik dieses Kits. Diese Schicht ist
**Execution-Layer** (`.claude/`), nicht Governance — der Governance-Core (`.ai-workspace/`)
bleibt markdown-only und motorlos (D-2026-09-30-10, ersetzt D-2026-09-30-05). Die Engine
`harness.mdmemory` (unter `src/` oder als Kopie unter `.claude/uaw/`) erzeugt dort abgeleitete
`GENERIERT`-Dateien (`knowledge/INDEX.md`, `knowledge/_typen/`, Register-Sichten); was Hooks
schreiben duerfen, regelt D-2026-09-30-09 (ersetzt D-2026-09-30-06).

> **Default: AUS** fuer alle *wiederkehrenden* Helfer (`boot_reload`, `recitation_nudge`,
> `daily_maintenance`, `prompt_optimizer`, `external_content_guard`, `compact_nudge`,
> `session_state_guard`). Ausnahmen, default AN: der einmalige Onboarding-Stups beim ersten Start
> (`first_run_onboarding`, ruft `/start` auf), `now_init` (legt `state/now.md` an, haelt 4 KB)
> und die Gedaechtnis-Hooks `index_refresh`, `memory_boot`, `journal_stub`, `precompact_reminder`
> (D-2026-09-30-09). Aktivierung/Deaktivierung ist opt-in, reversibel und wird
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
| `now_init` | `SessionStart` (alle Quellen) | Legt `.ai-workspace/state/now.md` (gitignored, pro Worktree) aus `templates/session-state.md` an, falls sie fehlt; kuerzt sie ueber 4 KB verlustfrei (Ueberlauf ins Session-Journal); nennt Session-Kurz-ID + Journal-Pfad; meldet eine alte `current-session.md`. **Default AN.** | Hook legt nur die lokale Live-Datei an und haelt ihre Groesse; Inhalte schreibt das Modell (D-2026-09-30-09). |
| `index_refresh` | `PostToolUse` (Write/Edit/MultiEdit/NotebookEdit) + `SessionStart` (startup/resume) | Nach einer Aenderung an einer Notiz unter `knowledge/<typ>/` sofort `harness.mdmemory index`; beim Start nur, wenn der Index veraltet ist (z. B. nach `git pull` oder einem Merge mit `merge=union`). Kaputte Notiz: nennt sie dem Modell. **Default AN.** | Schreibt nur `GENERIERT`-Dateien, nie Notizen; < 0,1 s bei 600 Notizen (D-2026-09-30-09). |
| `memory_boot` | `SessionStart` (alle Quellen) | Nennt abgeschlossene, nicht konsolidierte Journale anderer Sessions (max. 5; mit `uebergabe` oder aelter als heute, laufende Sessions bleiben aussen vor) und schlaegt `merken` vor; nach `compact` Erinnerung, Journal und `now.md` zu pruefen; beim `startup` Stups fuer den Skill `pflege`, wenn der letzte Bericht aelter als 7 Tage ist (max. 1x pro Tag). **Default AN.** | Liest; schreibt nur den eigenen Marker `.claude/.pflege_hint`; schweigt ohne Anlass (D-2026-09-30-09). |
| `journal_stub` | `SessionEnd` | Haengt an das existierende, nicht konsolidierte Journal dieser Session einen festen Abschluss-Eintrag (`uebergabe`). **Default AN.** | Legt nichts an, schreibt keine Inhalte der Arbeit; < 1,5 s (D-2026-09-30-09). |
| `precompact_reminder` | `PreCompact` | Erinnert den User, vor dem Compact Journal und `now.md` zu sichern. **Default AN.** | Nur `systemMessage`, blockiert nie (D-2026-09-30-09). |
| `boot_reload` | `SessionStart` | Liest `.ai-workspace/state/now.md` (Legacy-Fallback `current-session.md`) und speist es als `additionalContext` ein -> jede neue/resumte/gecleart/compactete Session bootet mit dem Live-State. Seit v3.2.1 laedt `CLAUDE.md` die Datei bereits per `@`-Import; fuer Claude Code ist der Hook damit weitgehend redundant. | Hook liest nur, was das Modell schrieb. |
| `recitation_nudge` | `PostToolUse` | Nach Write/Edit/NotebookEdit ein kurzer Reminder: relevantes Ergebnis ins Journal, dann `now.md` fortschreiben (Task + naechster Schritt + Evidenz, `session-contract.md` §3). | Hook erinnert, **Modell schreibt**. |
| `first_run_onboarding` | `SessionStart` (startup) | Bei frischem, uneingerichtetem Workspace (State-Platzhalter da, kein Onboarding-Marker) speist es einen Stups ein: begruesse den Nutzer + starte `/start`. **Default AN.** Escape: `UAW_DISABLE_ONBOARDING`. | Hook stupst nur an; `/start` + Modell handeln. |
| `daily_maintenance` | `SessionStart` (startup+resume) | Beim ersten Start eines lokalen Kalendertages ein Pflege-Pass-Vorschlag (scratch/ einsortieren, tote `[[wiki-links]]`/stale notes, verwaiste Artefakte). Schreibt nur seinen gitignored Datums-Marker. | Hook erinnert + schreibt nur eigenen Lauf-Marker, **Modell schlaegt vor/handelt**. |
| `prompt_optimizer` | `UserPromptSubmit` | Erkennt einen vagen Prompt (kurz ohne Aktionsverb, mehrere antezedenzlose Pronomen, offene Frage) und speist das 3-Stufen-Disambiguierungs-Protokoll ein (Annahmen offenlegen + fortfahren). Klarer Prompt -> inert. | Hook erinnert, **Modell** entscheidet; blockt nie. |
| `external_content_guard` | `PostToolUse` (WebFetch/WebSearch) | Nach einem externen Fetch: Quarantaene-Reminder (Inhalt = Daten, nie Anweisungen) + Injection-Scan-Hinweis; optional Abgleich der genutzten URL gegen die gitignored Projekt-Deny-Liste `.claude/external-content-denylist.txt`. | Advisory; blockt nie (kein exit 2). |
| `compact_nudge` | `PostToolUse` (kontext-wachsende Tools) | Zaehlt Tool-Calls in einem gitignored Marker und schlaegt alle `UAW_COMPACT_NUDGE_THRESHOLD` (default 60) Calls einen strategischen `/compact` an einer Task-Grenze vor; dazwischen still. | Hook erinnert, **Modell/Du** compacted. |
| `session_state_guard` | `PostToolUse` (Write/Edit/NotebookEdit) | Erinnert **nur**, wenn `now.md` veraltet ist (>= `UAW_STATE_GUARD_STALE_MINUTES`, default 20, nicht angefasst), gedrosselt auf max. 1x/Fenster, den Live-State zu sichern; bei fleissigem Mitschreiben still. | Staleness-gegated; Hook schreibt nie State. |

Die beiden Recitation-Helfer (`boot_reload`/`recitation_nudge`) setzen die Manus-Lehre lokal um:
**kontinuierliche Recitation + Reload beim Boot**. Der State ueberlebt Compaction nicht, weil ein
Hook den Moment abfaengt, sondern weil er laufend frisch ist und bei jedem Boot neu eingespeist wird.

**Schreib-Doktrin (D-2026-09-30-09; vollstaendig dort, hier die Kurzfassung).** Ein Hook darf schreiben:
(a) seinen **eigenen ephemeren, gitignored Lauf-Marker** unter `.claude/` (`daily_maintenance`
schreibt `.daily_maintenance_last`; `/start` schreibt `.onboarding-state.json`); (b) die lokale,
gitignored `state/now.md` **anlegen** (aus der Vorlage) und **auf 4 KB kuerzen**; (c) den dabei
entstehenden Ueberlauf ans Ende des **eigenen** Session-Journals **anhaengen**; (d) einmal einen
festen Abschluss-Eintrag ans eigene Journal haengen (`journal_stub`); (e) `GENERIERT`-Dateien neu
erzeugen (`index_refresh`). Nie: bestehende
Inhalte aendern, fremde Journale, Notizen, Decisions oder die Config (`automation.flags.json`)
beschreiben. Alles bleibt `.md`, die Invarianten C1/C2 halten.

## Dateien

- `.claude/automation.flags.json` — die Toggles. Default: `first_run_onboarding`, `now_init`, `index_refresh`, `memory_boot`, `journal_stub`, `precompact_reminder` `true`, alle uebrigen `false` (`boot_reload`, `recitation_nudge`, `daily_maintenance`, `prompt_optimizer`, `external_content_guard`, `compact_nudge`, `session_state_guard`).
- `.claude/hooks/run.sh` — Launcher fuer alle Hooks (`sh .claude/hooks/run.sh <hook>.py`): nimmt `$UAW_PYTHON`, sonst `python3`, sonst `python`, jeweils nur ab Python 3.9. Kein Interpreter: eine Zeile auf stderr, exit 0.
- `.claude/hooks/_flags.py` — stdlib-Helper: Repo-Root (`CLAUDE_PROJECT_DIR`, sonst aus `__file__`) + Flag lesen (jeder Fehler -> `False`, fail-safe); `load_engine` findet die Engine in `src/`, sonst in `.claude/uaw/`, sonst installiert.
- `.claude/uaw/mdm.py` — Aufruf der Engine ohne Installation: `python3 .claude/uaw/mdm.py <befehl>` = `python -m harness.mdmemory <befehl>`. In adoptierten Projekten liegt daneben die Engine-Kopie `harness/mdmemory/` mit `manifest.json` (D-2026-09-30-10).
- `.claude/hooks/index_refresh.py` — PostToolUse-/SessionStart-Handler, self-gated auf `index_refresh` (default AN); erneuert die generierten Dateien.
- `.claude/hooks/now_init.py` — SessionStart-Handler (startup/resume/clear/compact), self-gated auf `now_init` (default AN); nutzt `src/harness/mdmemory` (ohne Engine: inert). Codex: `--tool codex` uebergeben.
- `.claude/hooks/memory_boot.py` — SessionStart-Handler (alle Quellen), self-gated auf `memory_boot` (default AN); liest nur; meldet nicht konsolidierte Journale anderer Sessions (max. 5) und erinnert nach `compact`. Schweigt, wenn nichts offen ist.
- `.claude/hooks/journal_stub.py` — SessionEnd-Handler, self-gated auf `journal_stub` (default AN); haengt an das *existierende*, nicht konsolidierte Journal dieser Session einmal einen festen `uebergabe`-Eintrag (nur wenn es schon Eintraege hat und der letzte keine `uebergabe` ist). Legt nichts an, keine Inhalte, keine Pfade; deutlich unter dem 1,5-s-Budget.
- `.claude/hooks/precompact_reminder.py` — PreCompact-Handler, self-gated auf `precompact_reminder` (default AN); gibt nur `systemMessage` an den User aus (PreCompact kann dem Modell keinen Kontext geben), blockiert nie.
- `.codex/hooks.json` — dieselben Gedaechtnis-Hooks plus `now_init` fuer Codex (D-2026-09-30-07), Befehl ueber `$(git rev-parse --show-toplevel)` mit `--tool codex`. Codex fuehrt Projekt-Hooks erst aus, nachdem der User sie per `/hooks` geprueft und als vertrauenswuerdig markiert hat; SessionEnd-Timeout hoechstens 3 s.
- `.claude/hooks/boot_reload.py` — SessionStart-Handler, self-gated auf `boot_reload`.
- `.claude/hooks/recitation_nudge.py` — PostToolUse-Handler, self-gated auf `recitation_nudge`.
- `.claude/hooks/first_run_onboarding.py` — SessionStart(startup)-Handler, self-gated auf `first_run_onboarding` (default AN) + Onboarding-Marker + State-Platzhalter + `UAW_DISABLE_ONBOARDING`-Escape.
- `.claude/hooks/daily_maintenance.py` — SessionStart(startup+resume)-Handler, self-gated auf `daily_maintenance`; schreibt gitignored `.daily_maintenance_last`.
- `.claude/hooks/prompt_optimizer.py` — UserPromptSubmit-Handler, self-gated auf `prompt_optimizer`; injiziert bei vagem Prompt das 3-Stufen-Protokoll. Blockt nie.
- `.claude/hooks/external_content_guard.py` — PostToolUse(WebFetch|WebSearch)-Handler, self-gated auf `external_content_guard`; liest optional `.claude/external-content-denylist.txt` (gitignored, projekt-eigene PII-Deny-Liste; Repo liefert keine).
- `.claude/hooks/compact_nudge.py` — PostToolUse-Handler, self-gated auf `compact_nudge`; schreibt gitignored `.claude/.compact_nudge_state` (Zaehler).
- `.claude/hooks/session_state_guard.py` — PostToolUse(Write|Edit|NotebookEdit)-Handler, self-gated auf `session_state_guard`; staleness-gegated; schreibt gitignored `.claude/.session_state_guard` (Drossel-Timestamp).
- `.claude/commands/start.md` — der Erst-Start-Dirigent (`/start`); schreibt den gitignored Onboarding-Marker `.onboarding-state.json` (status done/skipped).
- `.claude/settings.json` -> `hooks`-Block — registriert die Hooks statisch. **Inert bis Flag true** (die default-AN-Hooks siehe oben).

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
- Launcher ist `sh .claude/hooks/run.sh`: er waehlt `python3` oder `python` (ab 3.9), damit die
  Hooks auch auf einem Mac ohne `python`-Alias (nur `/usr/bin/python3`, 3.9) laufen. Anderer
  Interpreter pro Maschine: `UAW_PYTHON=/pfad/zu/python`. Windows: Claude Code startet Hooks ueber
  Git Bash (`sh`).
- Faellt ein Hook aus (Launcher fehlt, Pfad nicht aufgeloest): **fail-safe inert**, nie blockierend.

## Verifizierte Primitive (Claude-Code-Docs)

- Modell-sichtbarer Kontext: `{"hookSpecificOutput": {"hookEventName": "...", "additionalContext": "..."}}` bei `exit 0`.
- `exit 0` ohne Ausgabe = inert. `exit 2` = blockierend (hier bewusst nie genutzt).
- **SessionStart-Matcher koennen NICHT pipe-alterniert werden** — je `source`
  (startup/resume/clear/compact) ein eigener Matcher-Eintrag. PostToolUse erlaubt `Write|Edit|NotebookEdit`.
- `UserPromptSubmit` unterstuetzt ebenfalls `additionalContext` bei `exit 0` (vom `prompt_optimizer`
  genutzt). `PostToolUse`-Matcher sind beliebige Tool-Namen-Regexes (z.B. `WebFetch|WebSearch`,
  `Read|Grep|Glob|Bash|Task|...`), nicht nur `Write|Edit|NotebookEdit`.
- Repo-Root im Command via `$CLAUDE_PROJECT_DIR`.
- `SessionEnd`: alle SessionEnd-Hooks teilen sich 1,5 s; Ausgaben steuern nichts mehr.
- `@`-Import einer fehlenden Datei in `CLAUDE.md` (geprueft mit Claude Code 2.1.285): die Zeile
  bleibt als Text stehen, kein Fehler. Eine Datei, die erst der SessionStart-Hook anlegt, wird in
  dieser Session noch nicht importiert, ab der naechsten schon. Darum ist `now.md` im frischen
  Klon in der ersten Session nicht im Kontext (sie ist dann ohnehin nur die Vorlage).
- `PreCompact`: kein `additionalContext`, nur `systemMessage` an den User oder Block
  (`decision: block` / exit 2, hier nie genutzt). Die Erinnerung ans Modell kommt darum nach dem
  Compact ueber `memory_boot` (SessionStart-Quelle `compact`).
- `additionalContext` bzw. stdout: max. 10.000 Zeichen, darueber wird ausgelagert.

## Selbsttest (ohne echte Session)

Off-Pfad (Repo wie ausgeliefert) — die opt-in Helfer sind AUS, erwartet je: keine Ausgabe, exit 0:

    echo '{}' | sh .claude/hooks/run.sh boot_reload.py
    echo '{}' | sh .claude/hooks/run.sh recitation_nudge.py
    echo '{}' | sh .claude/hooks/run.sh daily_maintenance.py
    echo '{}' | sh .claude/hooks/run.sh prompt_optimizer.py
    echo '{}' | sh .claude/hooks/run.sh external_content_guard.py
    echo '{}' | sh .claude/hooks/run.sh compact_nudge.py
    echo '{}' | sh .claude/hooks/run.sh session_state_guard.py

`first_run_onboarding` ist **default AN**: im ausgelieferten Template (State-Platzhalter vorhanden,
kein Marker) gibt es das Onboarding-`additionalContext`-JSON aus. Stummschalten via
`UAW_DISABLE_ONBOARDING=1` oder `.claude/.onboarding-state.json` anlegen:

    echo '{}' | sh .claude/hooks/run.sh first_run_onboarding.py   # erwartet: hookSpecificOutput-JSON

On-Pfad, ohne die echten Flags zu kippen (Sandbox-Projektdir via `CLAUDE_PROJECT_DIR`):

    tmp=$(mktemp -d)
    mkdir -p "$tmp/.claude" "$tmp/.ai-workspace/state"
    echo '{ "boot_reload": true, "recitation_nudge": true }' > "$tmp/.claude/automation.flags.json"
    echo "ACTIVE TASK: test" > "$tmp/.ai-workspace/state/now.md"
    echo '{}' | CLAUDE_PROJECT_DIR="$tmp" sh .claude/hooks/run.sh boot_reload.py   # erwartet: hookSpecificOutput-JSON
    rm -rf "$tmp"

## Session-State-Durabilitaet (now.md + Journal)

Seit v3.3 gibt es zwei Dateien mit getrennten Aufgaben (`session-contract.md` §3, D-2026-09-30-01):

- **`state/now.md`** — aktueller Stand *dieses* Worktrees. Gitignored, max. 4 KB, wird
  ueberschrieben. Zwei parallele Sessions in zwei Worktrees haben zwei eigene Dateien und damit
  keinen Merge-Konflikt. `now_init` legt sie an und haelt die Grenze ein.
- **`journal/YYYY/MM/<datum>-<kurzid>.md`** — Historie *dieser* Session. Committet, nur ergaenzt,
  **waehrend** der Arbeit geschrieben (nach jedem relevanten Ergebnis). Das ist der Garant gegen
  Verlust, nicht mehr die git-Historie einer ueberschriebenen Datei.

**Wird beim Session-Ende automatisch gesichert?** Ein harter Kill/Crash feuert keinen Hook. Darum
wird das Journal laufend geschrieben statt am Ende geflusht; ein Abbruch verliert hoechstens den
letzten Schritt. `session_state_guard` (opt-in) erinnert zusaetzlich, wenn `now.md` veraltet ist.

**Upgrade von <= 3.2:** `python -m harness.mdmemory now migrate --remove-legacy` sichert die alte
`state/current-session.md` byte-genau als Migrations-Journal, legt daraus eine lokale `now.md` an
und entfernt die alte Datei; danach committen. `now_init` weist beim Start darauf hin.

## Verwandte Governance

- Decisions (Notizen unter `knowledge/decision/`, Sicht `state/decisions.md` generiert) — D-2026-06-04-01 (Core-Freeze, ersetzt durch D-2026-09-30-05), D-2026-06-06-01 (default-AN Erst-Start-Onboarding), D-2026-06-06-02 (opt-in Pflege-Routine), D-2026-06-07-02 (vier zusaetzliche opt-in Hooks), D-2026-09-30-01 (now.md + Journal, ersetzt D-2026-06-07-01), D-2026-09-30-02 (Hook-Schreib-Doktrin, ersetzt D-2026-06-06-03), D-2026-09-30-03 (Automatik-Defaults, ersetzt D-2026-06-04-02), D-2026-09-30-04 (atomare Notizen unter `knowledge/<typ>/` kanonisch, Register nur noch generierte Sichten), D-2026-09-30-05 (abgeleitete `GENERIERT`-Dateien per `harness.mdmemory`, ersetzt D-2026-06-04-01), D-2026-09-30-06 (Gedaechtnis-Hooks default AN + Schreib-Doktrin, ersetzt D-2026-09-30-02 und -03, ersetzt durch D-2026-09-30-09), D-2026-09-30-07 (`.codex/` fuer Codex-Hooks), D-2026-09-30-09 (`index_refresh` + Pflege-Stups, Schreib-Doktrin (e)), D-2026-09-30-10 (Engine-Kopie unter `.claude/uaw/` per `adopt`, ersetzt D-2026-09-30-05).
- `session-contract.md` §3.1 — Recitation-Rationale + Pointer auf diese Schicht.
- `adapter-policy.md` §8 — Abgrenzung Automatik-Schicht vs. Adapter/Maintenance-Routine.

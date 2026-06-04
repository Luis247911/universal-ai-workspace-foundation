---
description: Companion for this kit's OPT-IN automation layer (boot_reload + recitation_nudge). Shows the current on/off state, explains each capability in plain terms, and turns it on or off on request — always after explicit confirmation, never automatically. Triggers on "/uaw-automation", "kit automation", "activate automation", "enable recitation", "turn on boot reload", "automation status", "disable automation".
argument-hint: "[optional: 'status' | 'on' | 'off' | 'boot_reload' | 'recitation_nudge']"
---

# /uaw-automation — Begleiter fuer die opt-in Automatik dieses Kits

Du fuehrst den User durch die **optionale, repo-eigene** Automatik-Schicht dieses Kits.
Optionaler Wunsch/Hinweis des Users: $ARGUMENTS

## Harte Grenze (bei Aktivierung/Deaktivierung zuerst sagen)

Diese Automatik steuert **ausschliesslich dieses Repo** (`.claude/` dieses Kits). Sie liest,
kopiert oder veraendert **niemals** `~/.claude/` — die globale, private Claude-Code-Konfiguration
des Users (Persona, Infra-Gate, globale Skills/Hooks/Memory). Repo-Automatik und globale
Konfiguration werden nicht vermischt.

## Was diese Schicht ist

Zwei unabhaengig schaltbare Faehigkeiten, beide **lokal, modellgetrieben, reversibel**,
**standardmaessig AUS**. Prinzip ueberall: **der Hook erinnert nur, das Modell schreibt** — kein
Script faelscht je State-Inhalt.

- **boot_reload** (`SessionStart`): Liest beim Session-Start `.ai-workspace/state/current-session.md`
  und speist es als Kontext ein, damit eine neue/fortgesetzte/gecleart/compactete Session sofort
  mit dem Live-Zustand bootet. Das deterministische, zuverlaessigste Stueck.
- **recitation_nudge** (`PostToolUse` bei Write/Edit/NotebookEdit): Nach einer Datei-Aenderung ein
  kurzer Reminder, `current-session.md` fortzuschreiben (aktiver Task + naechster Schritt +
  Evidenz) gemaess `session-contract.md` §3. Schreibt nichts selbst.

Vollstaendige Operator-Doku: `.claude/AUTOMATION.md`. Hintergrund-Entscheidung:
`.ai-workspace/state/decisions.md` (D-2026-06-04-01/-02).

## Ablauf

### 1. Stand zeigen (immer)

Lies `.claude/automation.flags.json` und zeige pro Faehigkeit **AN/AUS** in Klartext. Fehlt die
Datei oder ein Flag, gilt **AUS** (fail-safe).

### 2. Erklaeren (bei `status`, ohne Argument, oder wenn der User unsicher ist)

Erklaere jede Faehigkeit in einem Satz (s.o.) und dass nichts von selbst feuert, solange das
jeweilige Flag `false` ist — die Hooks sind in `settings.json` zwar registriert, aber self-gated
und damit inert.

### 3. Umschalten (nur auf ausdruecklichen Wunsch, nach Bestaetigung)

Wenn der User eine Faehigkeit **aktivieren oder deaktivieren** will:

1. Nenne die betroffene Faehigkeit und das Ziel (`true`/`false`) und hol eine **explizite
   Bestaetigung** ein. Aktiviere nie ungefragt.
2. Setze den Flag per `Edit` in `.claude/automation.flags.json` (nur den einen Boolean kippen).
3. Sag, **wann es wirkt**: `boot_reload` ab dem naechsten Session-Start (`/clear`, Resume oder
   neue Session); `recitation_nudge` ab der naechsten Write/Edit/NotebookEdit-Aktion.
4. Deaktivieren ist derselbe Weg zurueck: Flag auf `false`. Danach sind die Hooks wieder inert.

### 4. Voll-Entfernung (falls gewuenscht)

Wer die Schicht ganz herausnehmen will: den `hooks`-Block aus `.claude/settings.json` entfernen,
`.claude/hooks/boot_reload.py` + `recitation_nudge.py` + `_flags.py` loeschen und
`.claude/automation.flags.json` entfernen. Das Governance-Markdown (decisions/session-contract/
adapter-policy) bleibt unberuehrt — es dokumentiert nur, dass die Option existierte.

### 5. Cross-Surface-Hinweis (bei Aktivierung erwaehnen)

Die Hooks sind committet und laufen darum auch in Web-/Cloud-Sessions. Der Launcher in
`settings.json` ist `python`; auf manchen Linux-/Web-Umgebungen heisst er `python3` — falls ein
Hook dort nicht greift, ist das die einzige anzupassende Stelle (in `settings.json` oder pro
Maschine in `settings.local.json`). Faellt ein Hook aus, ist der Effekt **inert**, nie blockierend.

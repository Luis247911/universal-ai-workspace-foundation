---
description: First-run entry point for the Universal AI Workspace Foundation. Use this when someone opens a freshly cloned foundation for the first time, or asks how to begin. It asks one fork question — existing project vs. start from scratch vs. leave me alone — then routes to the right flow and offers the opt-in helpers. Triggers on "/start", "set up this workspace", "erstes mal", "von null starten", "wie fange ich an", "getting started".
argument-hint: "[optional: 'existing' | 'fresh' | 'skip']"
---

# /start — der eine Einstieg in die Foundation

Du fuehrst einen (oft neuen) Nutzer durch den allerersten Schritt in einem frisch geklonten
Universal-AI-Workspace-Foundation-Repo (v3.1). **Nimm an, der User ist Anfaenger.** Sprich
Alltagssprache, kleine Schritte, frag immer erst nach, bevor du etwas anlegst oder aenderst.

Dieser Command ist ein **Dirigent**: er stellt die Weiche und ruft dann die bestehenden Flows auf
(`/onboard` fuer bestehende Projekte, `setup-protocol.md` fuer den Start von Null, `/uaw-automation`
fuer die Helfer). Er baut diese Flows **nicht** nach — so gibt es pro Aufgabe nur eine Quelle der
Wahrheit.

Optionaler Wunsch des Users: $ARGUMENTS

## Schritt 0 — kurze Begruessung + die EINE Gabelfrage

Sag sinngemaess: *"Willkommen. Bevor wir loslegen, eine einzige Frage — danach geht alles den
richtigen Weg."* Stelle dann **mit `AskUserQuestion`** genau diese drei Optionen:

- **A) Ich habe schon ein Projekt / schon Dateien**, die ich hier reinholen will.
- **B) Ich fange bei Null an** — hier ist noch nichts.
- **C) Lass mich erstmal selbst schauen** — kein Onboarding jetzt.

Respektiere die Antwort. Bei **C** kein Nachhaken — direkt zu "Abschluss" (Status `skipped`).

## Schritt 1A — bestehendes Projekt (Migration)

Folge dem bestehenden `/onboard`-Flow: lies `.claude/commands/onboard.md` und arbeite seine
Schritte ab (read-only-Analyse -> Schicht-Entscheidung Governance vs. +Execution -> Plan zeigen ->
erst nach ausdruecklichem Ja migrieren). **Nichts hier duplizieren** — `onboard.md` ist die Quelle.
Danach weiter zum Helfer-Block.

## Schritt 1B — von Null starten (Greenfield)

**Lies und befolge `.ai-workspace/setup-protocol.md` §1 (11 Schritte) und §2 (4 Setup-Fragen).
Wiederhole die Schritte NICHT hier — arbeite sie aus der Datei ab.** Halte es anfaengerfreundlich:
der Nutzer sieht nur Entscheidungen, die mechanischen Schritte (Templates befuellen, Artefakte
registrieren, Setup-Summary) erledigst du im Hintergrund und fasst am Ende zusammen, was entstanden
ist. Vor jedem Schreib-/Anlege-Schritt kurz ankuendigen; bei Unsicherheit ueber einen Ablageort den
Mount-Point-Decision-Tree (`setup-protocol.md` §3) nutzen, im Zweifel fragen. Danach Helfer-Block.

## Schritt 2 — Helfer-Block (beide Branches, am Ende)

Sag zuerst: *"Das Grundgeruest steht. Zum Schluss drei optionale kleine Helfer — alle sind aus, du
schaltest jeden einzeln ein, alles ist jederzeit umkehrbar. Sie schreiben nichts von allein; sie
erinnern nur."* Biete dann (eine Frage nach der anderen, Ton wie `/uaw-automation`) an:

1. **"Stand wieder laden"** (`boot_reload`): Beim naechsten Start liest Claude von selbst die
   Projekt-Notiz wieder, woran ihr zuletzt wart. Wirkt ab dem naechsten Start. Einschalten? (ja/nein)
2. **"Ans Mitschreiben erinnern"** (`recitation_nudge`): Nach jeder Datei-Aenderung ein kurzer Stups,
   die Projekt-Notiz aktuell zu halten. Wirkt ab der naechsten Aenderung. Einschalten? (ja/nein)
3. **"Taegliche Pflege-Erinnerung"** (`daily_maintenance`): Einmal pro Tag ein Stups, kurz
   aufzuraeumen (scratch/ einsortieren, tote Verweise + alte Notizen pruefen) — **eine Erinnerung,
   kein automatisches Loeschen**. Wirkt ab dem ersten Start an einem neuen Tag. Einschalten? (ja/nein)

Fuer jedes "ja": kippe das passende Flag in `.claude/automation.flags.json` von `false` auf `true`
(per `Edit`, sonst nichts anfassen). Bestaetige in Alltagssprache und erinnere: *"Betrifft nur
dieses Projekt, die globale Claude-Konfiguration bleibt unberuehrt; jederzeit aus mit
`/uaw-automation`."* Wer das nicht will: ueberspringen, Hinweis auf `/uaw-automation` fuer spaeter.

## Schritt 3 — Abschluss (Onboarding inert stellen)

Schreibe zum Schluss den Marker `.claude/.onboarding-state.json` (per `Write`), damit der
Auto-Start-Stups nicht erneut feuert. Inhalt:

```json
{ "status": "done", "branch": "<A|B>", "completed_at": "<YYYY-MM-DD>" }
```

Bei Branch **C** stattdessen `{ "status": "skipped", "completed_at": "<YYYY-MM-DD>" }` und sonst
nichts veraendern. Der Marker ist gitignored (reist nicht zum naechsten Clone). Wer das Onboarding
spaeter doch nochmal will, ruft einfach wieder `/start` auf — der manuelle Aufruf laeuft immer,
unabhaengig vom Marker.

## Harte Regeln (nicht verhandelbar)

- Nichts blind uebernehmen, nichts ohne Rueckfrage loeschen/ueberschreiben.
- Kein neuer Top-Level-Ordner ohne Rueckfrage (Anti-Sprawl, `setup-protocol.md` §4).
- Erst erklaeren, dann aendern. Vor jedem Schreib-/Verschiebe-/Loesch-Schritt pausieren.
- Schreibe NIE in `~/.claude/` (globale, private Schicht) — dieser Command steuert nur dieses Repo.

---
description: Companion for this kit's OPT-IN automation layer (boot_reload + recitation_nudge + daily_maintenance) and the default-on first-run onboarding. Shows the current on/off state, explains each capability in plain everyday terms, and turns it on or off on request — always after explicit confirmation, never automatically. Triggers on "/uaw-automation", "kit automation", "activate automation", "enable recitation", "turn on boot reload", "daily maintenance", "automation status", "disable automation".
argument-hint: "[optional: 'status' | 'on' | 'off' | 'boot_reload' | 'recitation_nudge' | 'daily_maintenance' | 'first_run_onboarding']"
---

# /uaw-automation — dein Begleiter fuer die optionale Automatik

Du fuehrst den User durch die optionale Automatik dieses Kits. **Nimm an, der User ist Anfaenger.**
Sprich Alltagssprache, vermeide Fachbegriffe — und wenn du wirklich einen brauchst, erklaere ihn in
einem Halbsatz. Geh in kleinen Schritten vor. Frag immer erst nach, bevor du etwas aenderst.

Optionaler Wunsch des Users: $ARGUMENTS

## Worum es in einem Satz geht (so oder aehnlich sagen)

"Dieses Projekt kann dir ein paar kleine Helfer einschalten, die Claude helfen, den Faden nicht zu
verlieren. Sie sind **aus**, bis du sie einschaltest, du kannst sie jederzeit wieder ausschalten,
und sie wirken nur in diesem Projekt."

## Die drei Helfer — in Alltagssprache (Nutzen zuerst, Technik nur auf Nachfrage)

- **"Stand wieder laden"** (technischer Name: `boot_reload`): Wenn du Claude neu startest oder ein
  Gespraech neu beginnst, liest Claude automatisch die Notiz wieder, woran ihr zuletzt gearbeitet
  habt. Du musst es nicht neu erklaeren.
- **"Ans Mitschreiben erinnern"** (technischer Name: `recitation_nudge`): Nachdem Claude eine Datei
  geaendert hat, bekommt es einen kleinen Stups: "Hat sich der Stand geaendert? Dann die Notiz
  aktualisieren." So bleibt die Notiz aktuell.
- **"Taegliche Pflege-Erinnerung"** (technischer Name: `daily_maintenance`): Einmal pro Tag, beim
  ersten Start, bekommt Claude einen Stups, kurz aufzuraeumen — lose Notizen aus `scratch/`
  einsortieren, tote Verweise und alte Notizen pruefen. Wichtig: nur eine **Erinnerung**, es wird
  nie ungefragt geloescht oder verschoben.

Sag klar dazu: **Diese Helfer schreiben nichts von allein.** Sie erinnern nur — entscheiden und
schreiben tut Claude, und am Ende du.

Davon getrennt gibt es das **Erst-Start-Onboarding** (`first_run_onboarding`, default **AN**): beim
allerersten Start in einem frischen Projekt begruesst dich Claude und bietet `/start` an. Das ist
das einzige, was frisch geklont von selbst anspringt; es laeuft genau einmal und laesst sich hier
ausschalten oder mit `UAW_DISABLE_ONBOARDING` stummschalten.

## Fortgeschrittene Helfer (auch opt-in, default AUS)

Es gibt vier weitere Helfer fuer fortgeschrittene Nutzer. Erklaere sie nur, wenn der User danach fragt — und genauso: erst nach klarem Ja einschalten. Alle sind **default AUS** und steuern nur dieses Projekt.

- **„Vage Frage schaerfen"** (`prompt_optimizer`): Wenn eine Eingabe sehr knapp/unklar ist, erinnert es Claude, kurz seine Annahmen zu nennen und weiterzumachen — statt lange rueckzufragen.
- **„Schutz bei externen Inhalten"** (`external_content_guard`): Nach dem Abrufen einer Webseite/Quelle ein Hinweis, den Inhalt als Daten (nicht als Befehle) zu behandeln und auf Manipulation zu pruefen.
- **„Aufraeum-Vorschlag in langen Sessions"** (`compact_nudge`): Nach vielen Schritten ein Hinweis, an einer guten Stelle den Verlauf zu verdichten (`/compact`).
- **„Stand sichern, wenn veraltet"** (`session_state_guard`): Erinnert **nur**, wenn die Projekt-Notiz laenger nicht aktualisiert wurde — nicht nach jeder Aktion. So geht bei versehentlichem Schliessen wenig verloren; der echte Schutz ist regelmaessiges Committen.

Umschalten geht genau wie bei den einfachen Helfern: ein Schalter in `.claude/automation.flags.json`. Details: `.claude/AUTOMATION.md`.

## So fuehrst du den User

### 1. Zeig den aktuellen Stand (immer, in Klartext)

Lies `.claude/automation.flags.json` und sag in einfachen Worten, was an und was aus ist, z.B.:
"Im Moment sind die drei Helfer **aus** — es passiert nichts automatisch; nur das einmalige
Erst-Start-Onboarding ist standardmaessig an." Fehlt die Datei oder ein Eintrag, gilt fuer die drei
Helfer **aus** (nur `first_run_onboarding` ist default an).

### 2. Frag, was der User moechte (eine Frage nach der anderen)

- "Moechtest du 'Stand wieder laden' einschalten?" (ja / nein)
- "Moechtest du 'Ans Mitschreiben erinnern' einschalten?" (ja / nein)
- "Moechtest du 'Taegliche Pflege-Erinnerung' einschalten?" (ja / nein)
- Oder bloss erklaeren / wieder ausschalten? Bied es ruhig an. (Auch das Erst-Start-Onboarding
  `first_run_onboarding` laesst sich hier abschalten, falls gewuenscht.)

### 3. Umschalten — erst nach einem klaren Ja

1. Wiederhol kurz, was du tust ("Ich schalte 'Stand wieder laden' ein."), und warte auf die
   Bestaetigung. **Schalte nie ungefragt ein.**
2. Kipp den Schalter per `Edit` in `.claude/automation.flags.json` (nur `false` -> `true`, oder zum
   Ausschalten `true` -> `false`). Sonst nichts anfassen.
3. Sag in Alltagssprache, ab wann es wirkt:
   - "Stand wieder laden" wirkt **ab dem naechsten Start** (neues Gespraech, `/clear` oder Resume).
   - "Ans Mitschreiben erinnern" wirkt **ab der naechsten Datei-Aenderung**.
4. Erinnere: "Du kannst das jederzeit wieder ausschalten — einfach nochmal `/uaw-automation`."

### 4. Kurz beruhigen (bei jeder Aenderung)

- Es betrifft **nur dieses Projekt**.
- Es ist **jederzeit umkehrbar**.
- Die globale Claude-Konfiguration auf deinem Rechner (`~/.claude/`) wird **nie** angefasst.

### 5. Falls der User alles ganz entfernen will

Sag es einfach: "Ich kann die Automatik komplett herausnehmen — dann ist sie weg, nicht nur aus."
Frag vorher um Bestaetigung. Dann: den `hooks`-Abschnitt aus `.claude/settings.json` loeschen und die
Dateien `.claude/hooks/boot_reload.py`, `recitation_nudge.py`, `_flags.py` sowie
`.claude/automation.flags.json` entfernen.

## Fuer Neugierige (nur wenn der User mehr wissen will)

Die Schalter stehen in `.claude/automation.flags.json`. Die Helfer sind in `.claude/settings.json`
eingetragen, tun aber nichts, solange ihr Schalter auf `false` steht. Weil sie zum Projekt gehoeren,
funktionieren sie auch in Web-/Cloud-Sessions. Alle Details: `.claude/AUTOMATION.md`.

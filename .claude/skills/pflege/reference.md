# reference — pflege: planen

Ein geplanter Lauf erzeugt **nur** den Bericht und die generierten Rollups. Aenderungen an Notizen
brauchen eine Session mit Mensch; Ergebnis ist ein PR, nie ein Merge.

## Variante A: Claude Code `/schedule` (Cloud-Routine)

`/schedule` legt in Claude Code eine wiederkehrende Routine an, die in der Cloud auf dem
GitHub-Repo laeuft. Die genauen Optionen stehen in der Claude-Code-Doku; die Routine selbst:

- **Rhythmus**: woechentlich, z. B. montags frueh.
- **Auftrag** (als Prompt der Routine):

```text
Fuehre den Skill pflege aus: python -m harness.mdmemory report --write, dann den Bericht
auswerten. Aendere keine Notizen. Wenn Rollups neu erzeugt wurden oder lint Fehler zeigt, die
sich mit "python -m harness.mdmemory index" beheben lassen: Branch pflege/<datum>, commit,
PR oeffnen mit dem Bericht als Beschreibung. Nie mergen.
```

- **Rechte**: nur dieses Repo; PR oeffnen erlaubt, Merge nicht.

## Variante B: macOS launchd (lokal, ohne Modell)

Erzeugt woechentlich nur den Bericht unter `scratch/maintenance/`. Datei
`~/Library/LaunchAgents/local.uaw.pflege.plist` (Pfade anpassen; das Repo liefert die Datei
nicht aus, weil `.ai-workspace/` markdown-only ist und der Pfad maschinenabhaengig):

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>Label</key><string>local.uaw.pflege</string>
  <key>ProgramArguments</key>
  <array>
    <string>/PFAD/ZUM/REPO/.venv/bin/python</string>
    <string>-m</string><string>harness.mdmemory</string>
    <string>--root</string><string>/PFAD/ZUM/REPO</string>
    <string>report</string><string>--write</string>
  </array>
  <key>StartCalendarInterval</key>
  <dict><key>Weekday</key><integer>1</integer><key>Hour</key><integer>8</integer><key>Minute</key><integer>0</integer></dict>
  <key>StandardOutPath</key><string>/tmp/uaw-pflege.log</string>
  <key>StandardErrorPath</key><string>/tmp/uaw-pflege.log</string>
</dict>
</plist>
```

Laden: `launchctl load ~/Library/LaunchAgents/local.uaw.pflege.plist`; entfernen:
`launchctl unload …` und Datei loeschen. Den Bericht liest man danach in einer normalen Session
mit dem Skill `pflege` (Schritt 2).

## Variante C: manuell

`python -m harness.mdmemory report` (stdout) oder mit `--write`. Exit-Code 1 bei Lint-Fehlern,
damit ein eigener Cron oder CI-Job darauf reagieren kann.

## Schwellen (in `src/harness/mdmemory/report.py`)

- veraltet: `review_after` ueberschritten oder `last_confirmed` aelter als 180 Tage,
- Waise: aktiv, nicht angeheftet, aelter als 30 Tage, keine Verbindung in `links`, `blocks`,
  `supersedes`, `superseded_by` (weder ein- noch ausgehend),
- Duplikat-Kandidat: gleicher Typ, Wortueberlappung von Titel + Summary ≥ 0,6.

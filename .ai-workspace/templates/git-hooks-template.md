# Template: git-Hooks fuer Kit-Hygiene

Diese Datei ist eine **Markdown-Anleitung** (wie `gitignore-template.md`), kein aktives Hook-Set. Die lauffaehigen Hooks dieses Repos liegen unter `.githooks/` im Projekt-Root: echter Shell-Code und damit bewusst kein Teil der markdown-only Governance-Schicht. Ein abgeleitetes Projekt uebernimmt die Hooks aus `.githooks/` oder erzeugt sie aus den Bloecken unten. Kanonische Quelle ist `.githooks/`; die Bloecke hier sind identisch zum Stand dieses Repos.

## Zweck

Verhindert, dass die reine **Nutzung** eines Kits versehentlich Echtdaten ins Repository traegt: force-hinzugefuegte ignorierte Artefakte, hartcodierte Secrets, private Klarnamen. Bewusste Entwickler-Edits bleiben moeglich (normaler Commit, bei Bedarf `--no-verify`). Die Loesung sitzt tool-agnostisch auf git-Ebene und greift unabhaengig davon, ob ein Commit aus der IDE, per Skript, von einem Sub-Agent oder von Hand kommt.

## Aktivierung (opt-in, pro Klon)

```sh
git config core.hooksPath .githooks
chmod +x .githooks/pre-commit .githooks/pre-push   # unixoide Systeme / Git-bash
```

- **Windows:** Die Hooks laufen ueber die mitgelieferte `sh` von Git for Windows. Zeilenenden muessen LF sein; dafuer sorgt der Eintrag `.githooks/** text eol=lf` in `.gitattributes`. Ohne ihn macht `core.autocrlf=true` aus der Shebang ein `#!/bin/sh` mit angehaengtem CR, und der Hook bricht mit "bad interpreter".
- **Deaktivieren:** `git config --unset core.hooksPath`.
- **Bewusster Bypass, einmalig:** `git commit --no-verify` bzw. `git push --no-verify`.

## Private Begriffsliste (PII bleibt ungetrackt)

Echte Namen (Mandanten, Personen, interne Projekte) gehoeren nicht in den getrackten Hook-Code. Lege sie in eine Datei `.private-scan-terms` im Projekt-Root, eine Zeile pro Begriff:

```text
# Kommentare (#) und Leerzeilen werden ignoriert
Beispielmandant GmbH
Projekt-Codename
```

`.private-scan-terms` ist via `.gitignore` ausgeschlossen und wird nie committet. Die Hooks lesen die Datei und blocken, sobald ein Begriff im Diff (pre-commit) bzw. im getrackten Baum (pre-push) auftaucht.

## Was blockiert wird

| Hook | Prueft | Blockt bei |
|---|---|---|
| pre-commit | gestagter Diff: neue Dateien plus neue Zeilen | force-added ignorierte Datei, Secret-Muster, privater Begriff |
| pre-push | gesamter getrackter Baum (Pre-Release-Scan) | Secret-Muster, privater Begriff |

Secret-Erkennung: hochpraezise Provider-Token (AWS-, GitHub-, Slack-, OpenAI-Stil), PEM-Privatschluessel und generische Zuweisungen der Form `keyword = "literalwert"`. Ein blosses Vorkommen der Woerter (etwa "secret" im Fliesstext) loest bewusst nicht aus, damit Doku und regulaerer Code keine Fehlalarme erzeugen. Die Hook-Dateien und dieses Template sind vom pre-push-Scan ausgenommen, weil sie die Muster selbst als Text enthalten.

## pre-commit

```sh
#!/bin/sh
# Kit-Hygiene pre-commit (Foundation). Verhindert, dass Kit-NUTZUNG versehentlich
# ignorierte Artefakte, Secrets oder private Klarnamen in einen Commit traegt.
# Opt-in:           git config core.hooksPath .githooks
# Bewusster Bypass: git commit --no-verify
# PII-frei: echte Namen stehen NUR in der ungetrackten .private-scan-terms.
set -u
problems=""

# (1) Mit "git add -f" erzwungene, eigentlich ignorierte Dateien
while IFS= read -r f; do
	[ -z "$f" ] && continue
	git check-ignore -q --no-index "$f" && problems="$problems
  force-added trotz .gitignore: $f"
done <<EOF
$(git diff --cached --name-only --diff-filter=A)
EOF

# Nur neu hinzugefuegte Zeilen des Commits betrachten
added="$(git diff --cached -U0 --diff-filter=ACM | grep '^+' | grep -v '^+++' || true)"

# (2) Secrets: hochpraezise Provider-Token, PEM-Keys, Zuweisung mit Literalwert
hits="$(printf '%s\n' "$added" | grep -nEi \
	-e '(AKIA[0-9A-Z]{16}|ghp_[0-9A-Za-z]{36}|gho_[0-9A-Za-z]{36}|github_pat_[0-9A-Za-z_]{40,}|xox[baprs]-[0-9A-Za-z-]{10,}|sk-[0-9A-Za-z]{20,})' \
	-e 'BEGIN[ A-Z]*PRIVATE KEY' \
	-e "(secret|password|passwd|api[_-]?key|access[_-]?token|auth[_-]?token|client[_-]?secret|token)[[:space:]]*[:=][[:space:]]*['\"][^'\"]{8,}" \
	|| true)"
[ -n "$hits" ] && problems="$problems
  moegliches Secret:
$hits"

# (3) Private Klarnamen aus ungetrackter .private-scan-terms (fixed-string)
if [ -f .private-scan-terms ]; then
	while IFS= read -r t; do
		[ -z "$t" ] && continue
		case "$t" in \#*) continue ;; esac
		printf '%s\n' "$added" | grep -qFi -e "$t" && problems="$problems
  privater Begriff im Diff: $t"
	done < .private-scan-terms
fi

if [ -n "$problems" ]; then
	echo "pre-commit BLOCK (kit-hygiene):$problems"
	echo "Bewusst trotzdem committen: git commit --no-verify"
	exit 1
fi
exit 0
```

## pre-push

```sh
#!/bin/sh
# Kit-Hygiene pre-push (Foundation) = Pre-Release-Scan ueber den GESAMTEN getrackten Baum.
# Opt-in:           git config core.hooksPath .githooks
# Bewusster Bypass: git push --no-verify
# Die Hook-Dateien und das Template enthalten die Muster selbst als Text -> ausgeschlossen.
set -u
problems=""
X1=":!.githooks"
X2=":!.ai-workspace/templates/git-hooks-template.md"

# (1) Secrets ueber alle getrackten Dateien (git grep sieht nur Getracktes)
hits="$(git grep -nEi \
	-e '(AKIA[0-9A-Z]{16}|ghp_[0-9A-Za-z]{36}|gho_[0-9A-Za-z]{36}|github_pat_[0-9A-Za-z_]{40,}|xox[baprs]-[0-9A-Za-z-]{10,}|sk-[0-9A-Za-z]{20,})' \
	-e 'BEGIN[ A-Z]*PRIVATE KEY' \
	-e "(secret|password|passwd|api[_-]?key|access[_-]?token|auth[_-]?token|client[_-]?secret|token)[[:space:]]*[:=][[:space:]]*['\"][^'\"]{8,}" \
	-- "$X1" "$X2" 2>/dev/null || true)"
[ -n "$hits" ] && problems="$problems
  moegliches Secret:
$hits"

# (2) Private Klarnamen aus ungetrackter .private-scan-terms (fixed-string)
if [ -f .private-scan-terms ]; then
	while IFS= read -r t; do
		[ -z "$t" ] && continue
		case "$t" in \#*) continue ;; esac
		m="$(git grep -nFi -e "$t" -- "$X1" "$X2" 2>/dev/null || true)"
		[ -n "$m" ] && problems="$problems
  privater Begriff getrackt: $t"
	done < .private-scan-terms
fi

if [ -n "$problems" ]; then
	echo "pre-push BLOCK (kit-hygiene, Pre-Release-Scan):$problems"
	echo "Bewusst trotzdem pushen: git push --no-verify"
	exit 1
fi
exit 0
```

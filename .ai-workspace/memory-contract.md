# memory-contract.md — Wer besitzt, laedt und schreibt welches Gedaechtnis

Dieser Vertrag bindet die Gedaechtnis-Regeln aus `AGENTS.md`, `session-contract.md`, `context-policy.md` und `knowledge-graph-policy.md` in einer Uebersicht zusammen (D-2026-09-30-08). Er fuehrt im Projekt keine neuen Ablageorte ein; der optionale globale Namespace (§5) liegt in einem eigenen Repo ausserhalb. Bei Widerspruch im Detail gilt die jeweilige Policy, und dieser Vertrag wird nachgezogen.

## 1. Die fuenf Festlegungen

1. **Markdown in git ist kanonisch** fuer Wissen, Decisions und Praeferenzen (`knowledge/<typ>/`, D-2026-09-30-04). Operative Daten wie Tasks, Status und KPIs liegen in ihren externen Systemen. Notizen verweisen nur darauf (Typ `project`, Feld `external_ref`) und kopieren sie nie.
2. **Claude Auto-Memory ist in Foundation-Repos aus.** Dafuer steht `"autoMemoryEnabled": false` in `.claude/settings.json`; pro Maschine geht auch die Env-Variable `CLAUDE_CODE_DISABLE_AUTO_MEMORY=1`. Vorhandene Auto-Memory-Dateien holt `python -m harness.mdmemory import-automemory` einmalig als Journal-Kandidaten herein. Die Quelle bleibt dabei unveraendert, uebernommen wird ueber `merken`.
3. **`scope` und `sensitivity` an jeder Notiz.** Ein globaler Namespace ist optional und standardmaessig aus (§5). Personenbezogenes bekommt `sensitivity: personal` und erscheint in keinem Index. **Private Inhalte gehoeren in ein separates Repo**, weil sich Daten aus der git-Historie kaum loeschen lassen: Sie stecken in jedem Clone, Fork und Cache.
4. **Nur lokal**: Claude Code und Codex arbeiten auf den Dateien im Repo. Schema und Journal sind so gebaut, dass ein spaeterer MCP-Server nur lesen und hoechstens Journal-Vorschlaege schreiben muss (§6).
5. **`merken` schreibt direkt, fragt aber vorher** bei Typ `person`, bei `preference` mit `scope: global`, bei SUPERSEDE bzw. Korrekturen (`change: korrigiert`) und bei CONFLICT (`session-contract.md` §3.3).

## 2. Besitz-Tabelle

| Speicher | Ort | Kanonisch fuer | Besitzer (schreibt) | Lebensdauer |
|---|---|---|---|---|
| Live-Zustand | `state/now.md` (gitignored, pro Worktree, max. 4 KB) | aktuelle Aufgabe dieses Worktrees | Modell; Hook `now_init` legt an und kuerzt | ueberschrieben |
| Journal | `journal/YYYY/MM/<datum>-<kurzid>.md` | was in einer Session geschah | Modell (nur anhaengen); Hooks nur Ueberlauf und Abschluss-Eintrag | dauerhaft, nach Konsolidierung eingefroren |
| Notizen | `knowledge/<typ>/<id>.md` | Wissen, Decisions, Praeferenzen, Fragen, Annahmen, Risiken | Modell ueber `merken` bzw. Hauptsession | dauerhaft, ersetzen statt loeschen |
| Generierte Dateien | `knowledge/INDEX.md`, `knowledge/_typen/`, Register-Sichten in `state/`, `journal/*/*/_rollup.md` | nichts; abgeleitet | nur `python -m harness.mdmemory` | jederzeit neu erzeugbar |
| Tabellen | `state/source-registry.md`, `state/artifact-index.md`, `state/project-index.md` | Quellen, Artefakte, Projekt-Identitaet | Hauptsession | dauerhaft |
| Pflege-Berichte | `scratch/maintenance/<datum>-pflege.md` (gitignored) | nichts; Vorschlaege | Skill `pflege` | ephemer |
| Operative Daten | externe Systeme | Tasks, Status, KPIs | dort | dort |
| Claude Auto-Memory | ausserhalb des Repos | nichts (aus) | niemand | nur Import-Quelle |
| Globaler Namespace (optional) | eigenes Repo, Pfad in `UAW_GLOBAL_MEMORY_DIR` | Notizen mit `scope: global` | Modell ueber `merken`, nach Rueckfrage | dauerhaft |

## 3. Ladevertrag

| Stufe | Was | Wann |
|---|---|---|
| Boot | `AGENTS.md`, `CLAUDE.md`, `state/project-index.md`, `state/now.md`, `knowledge/INDEX.md` | immer; Ziel ≤ 5.000 Tokens, hart ≤ 12.000 inklusive Worst Case (CI-Test, `mdmemory budget`) |
| Bei Bedarf | `knowledge/_typen/<typ>.md`, die Register-Sichten | wenn der Boot-Index nicht reicht |
| Gezielt | eine Notiz, ein Journal | ueber Index, `links`, Alias, `sources` oder `grep` |
| Nie automatisch | `journal/**` als Ordner, `archive/`, `scratch/`, Auto-Memory, globaler Namespace | nur auf ausdrueckliche Anfrage |

Die Deckel stehen in `src/harness/mdmemory/limits.py`: `INDEX.md` hat hoechstens 8 KB bzw. 80 Zeilen, ein Unterindex-Teil hoechstens 50 Eintraege, `now.md` hoechstens 4 KB. Tool-Grenzen stehen dort ebenfalls, mit Quelle:

- Claude Code: `additionalContext` hoechstens 10.000 Zeichen, SessionEnd hoechstens 1,5 s.
- Codex: Hook-Kontext ab etwa 2.500 Tokens ausgelagert, SessionEnd hoechstens 3 s.

## 4. Schreibwege

| Weg | Darf schreiben | Darf nicht |
|---|---|---|
| Modell / Hauptsession | Journal (anhaengen), `now.md`, Notizen, Tabellen | generierte Dateien von Hand, fremde Journale aendern |
| Skill `merken` | Notizen, Einfrieren des Journals (`konsolidiert`) | ohne Quelle schreiben; bei den Faellen aus §1 Punkt 5 ohne Rueckfrage schreiben |
| Skill `pflege` | Journal-Rollups, Bericht unter `scratch/maintenance/` | Notizen aendern, Auto-Merge; Korrekturen aus dem Bericht (`confirm`, `supersede`, Archivieren) setzt die Hauptsession nach Bestaetigung um |
| Hooks (D-2026-09-30-06) | `now.md` anlegen und kuerzen, Ueberlauf und Abschluss-Eintrag ins eigene Journal, eigene Marker | Notizen, Decisions, generierte Dateien, Flags |
| `harness.mdmemory` (D-2026-09-30-05) | generierte Dateien; Skelette und Migrationen auf ausdruecklichen Aufruf | kanonische Inhalte umschreiben |
| CI | nichts; prueft `lint`, Budget, Round-Trip | — |
| MCP-Server (spaeter, §6) | Journal-Vorschlaege | Notizen, State, generierte Dateien |

## 5. Optionaler globaler Namespace

Standardmaessig aus. Ein Nutzer kann Praeferenzen und Arbeitsweisen, die ueber ein Projekt hinaus gelten (`scope: global`), in einem **eigenen, privaten Repo** mit derselben Struktur (`.ai-workspace/knowledge/…`) sammeln:

```text
export UAW_GLOBAL_MEMORY_DIR=~/pfad/zum/privaten-gedaechtnis   # enthaelt .ai-workspace/
python -m harness.mdmemory --global new preference "Antworten kurz halten" --source user:2031-01-01
python -m harness.mdmemory --global index
```

Nichts davon wird automatisch geladen oder ins Projekt-Repo kopiert. Ist die Variable nicht gesetzt oder zeigt sie auf keinen Workspace, bricht `--global` mit einer Meldung ab.

## 6. MCP spaeter: nur lesen, Vorschlaege ins Journal

Ein spaeterer MCP-Server fuer andere Oberflaechen braucht keine neue Ablage:

- **Lesen:** `INDEX.md`, Unterindizes, einzelne Notizen per ID oder Alias, Suche. Notizen mit `sensitivity` personal oder restricted gibt er nur auf ausdrueckliche Nutzeranfrage heraus.
- **Schreiben:** ausschliesslich neue Journal-Dateien mit `tool: mcp-proposal`. Uebernommen wird wie jeder andere Journal-Eintrag ueber `merken` in einer lokalen Session.

## 7. Qualitaet messen: Recall-Set

Ob das Gedaechtnis traegt, misst ein Recall-Set aus 30 Fragen mit erwarteter Notiz (Vorlage `templates/recall-set.md`). Volltext- oder Vektorsuche kommt erst in Frage, wenn die Trefferquote **unter 90 %** faellt. Auch dann bleibt sie nur eine Suchschicht, und die Notizen bleiben die Quelle.

## Cross-Links

`session-contract.md` §3 · `context-policy.md` · `knowledge-graph-policy.md` §4–§8, §12 · `security-policy.md` · `.claude/AUTOMATION.md` · `templates/knowledge-note.md` · `templates/recall-set.md`

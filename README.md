# Universal AI Workspace Foundation

Ein Starter-Kit für Projekte, die du mit einem AI-Coding-Assistenten bearbeitest (zuerst für Claude Code gebaut). Es bringt zwei Dinge in einem Repo zusammen:

1. **Regeln und Gedächtnis** in reinem Markdown (Ordner `.ai-workspace/`): klare Konventionen, wo was liegt, plus einen Wissens- und Zustandsspeicher, den der Assistent über mehrere Sitzungen hinweg liest.
2. **Lauffähige Werkzeuge** (Ordner `.claude/` + `src/harness/`): 12 fertige Bausteine („Skills") über einer kleinen Python-Engine. Damit kannst du zum Beispiel die Antworten eines AI-Agenten automatisch bewerten (Eval), riskante Ein- und Ausgaben blockieren (Guardrail) oder vor einem kritischen Schritt einen Menschen freigeben lassen (Human-in-the-Loop).

Du nimmst beide Schichten oder nur die Regeln. Die Werkzeuge laufen offline: ohne API-Key, ohne Internet, ohne große Zusatz-Bibliotheken.

**Für wen?** Für Entwickler, die AI-Projekte sauber aufsetzen wollen, statt Prompts und Skripte immer wieder zu kopieren. Du solltest mit Kommandozeile und Python umgehen können; tiefe AI-Vorkenntnisse sind nicht nötig.

## Schnellstart

Zwei Wege - der erste braucht kein Klonen.

### 1. An ein bestehendes Projekt anbinden (der eigentliche Einstieg, kein Klonen)

Öffne dein Projekt in Claude Code und gib diesen Prompt ein. Er liest dieses Repo nur als Referenz, analysiert deine Struktur und schlägt einen Plan vor, bevor er etwas ändert - er installiert oder kopiert nichts:

```text
Du arbeitest in meinem aktuellen Projekt und sollst prüfen, ob und wie es sich an der
Universal AI Workspace Foundation (v3.0) ausrichten lässt.

Die Foundation hat ZWEI Schichten - wir entscheiden gemeinsam, welche dieses Projekt braucht:
- Governance (.ai-workspace/, reines Markdown): Regeln, Zustand, Wissen. Fast immer sinnvoll.
- Execution (.claude/ + src/harness/, Python): 12 Claude-Code-Skills über einer
  pip-installierbaren Engine (Evals, Guardrails, Tracing, HITL, Routing, Memory,
  Orchestrierung). Nur wenn das Projekt sie wirklich nutzt.

Schritt 1 - Analysiere die vorhandene Projektstruktur (Ordner; wo Notizen/Prompts/Agents/Docs/
Wissen/Sessions/Code/Temp liegen; doppelte oder unklare Strukturen).
Schritt 2 - Nutze dieses öffentliche Repo als Referenz (nur lesen, nichts klonen/installieren):
https://github.com/Luis247911/universal-ai-workspace-foundation
Lies: README.md, AGENTS.md (Paragraph 2.5, 3), install-checklist.md, install-harness.md (nur falls
relevant), .ai-workspace/setup-protocol.md (Paragraph 3 Frage 0 + Paragraph 2 vier Setup-Fragen).
Schritt 3 - Entscheide MIT MIR: nur Governance, oder auch Execution? Begründe anhand Schritt 1.

Regeln (nicht verhandelbar): nichts blind übernehmen; nichts ohne Rückfrage löschen; keine
neuen Top-Level-Ordner ohne Rückfrage (Anti-Sprawl - einziger Code-Mount .claude/, sonst
src/tests/examples); vorhandene Ordner (agents/prompts/notes/docs/wiki/skills/tasks) sauber
migrieren statt Parallelstruktur; erst Plan erklären, dann ändern.

Liefere zuerst (noch nichts anlegen): 1. Analyse. 2. Empfehlung Governance-only vs. +Execution
(begründet). 3. Was übernehmen. 4. Was nicht. 5. Schrittweiser Migrationsplan (Governance
zuerst, Execution optional). 6. Liste neu/geändert. Warte danach auf meine Bestätigung.
```

Hat dein Projekt die Foundation schon (oder ist `.claude/` vorhanden)? Dann führe stattdessen `/onboard` aus.

### 2. Engine selbst ausprobieren (klonen + installieren)

```bash
git clone https://github.com/Luis247911/universal-ai-workspace-foundation
cd universal-ai-workspace-foundation
python -m venv .venv && . .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -e .                               # Paket "uaw-harness", zieht KEINE Fremd-Pakete
python examples/eval_demo.py                    # Offline-Demo, endet mit "PASS" (exit 0)
```

Python >= 3.10. Engine-Aufrufe laufen über `python -m harness.<bereich>` (CLI-Name `harness`, Paketname `uaw-harness`), identisch auf Windows, macOS, Linux. Nur die Governance-Regeln manuell in ein bestehendes Projekt holen: [`install-checklist.md`](install-checklist.md). Volle Anleitung inkl. Extras und echtem LLM statt Mock: [`install-harness.md`](install-harness.md).

## Das Zwei-Schichten-Modell

Die Foundation trennt sauber, was *persistiert*, von dem, was *läuft*:

| Schicht | Pfad | Rolle | Format |
|---------|------|-------|--------|
| **Governance + State + Memory** | `.ai-workspace/` | Regeln, Zustand, Wissen: die Wahrheit, die persistiert | Markdown-only (strikt) |
| **Execution** | `.claude/` + `src/harness/` | tool-nativer Code, der läuft: Skills + Engine | Code |

Die Grenze ist scharf: **Code, der läuft, lebt in `.claude/` und `src/`. Wahrheit, die persistiert, lebt in `.ai-workspace/`.** Keine Schicht schreibt die kanonischen Dateien der anderen. Skill-*Outputs* sind delegierte Arbeit (untrusted bis verifiziert) und folgen dem `scratch/`/`research/`-Lifecycle; `state/` ändern sie nur über den deklarierten State-Write-Contract (`.ai-workspace/skills-authoring-policy.md`). Details: `AGENTS.md` §2.5.

`.ai-workspace/` und `AGENTS.md` bleiben tool-neutral. `.claude/` ist Claude-Code-spezifisch; die Engine `src/harness/` ist tool-unabhängig und auch ohne `.claude/` nutzbar.

## Glossar — die leicht verwechselbaren Begriffe

Eine Referenz, **kein** zweiter Regeltext: jede Zeile zeigt nur, *was* ein Begriff ist und *wo* er geregelt wird. Die vollständige Mount-Point-Map steht in [`.ai-workspace/README.md`](.ai-workspace/README.md).

| Begriff | Was es ist | Wo es lebt | Wo geregelt |
|---------|-----------|-----------|-------------|
| **Governance** | Die Schicht, die *persistiert*: Regeln, Zustand, Wissen (Markdown) | `.ai-workspace/` | `AGENTS.md` §2.5 |
| **Execution** | Die Schicht, die *läuft*: Skills + Engine (Code) | `.claude/` + `src/harness/` | `AGENTS.md` §2.5 |
| **State** | Operativer kanonischer Projektzustand — das **Gedächtnis dieses Workspaces** | `.ai-workspace/state/` | `protocol.md` §4, `security-policy.md` §11 |
| **Memory** (Engine) | **Baukasten**, um einem Agenten, den *du baust*, ein Gedächtnis zu geben (Typ × Scope, in-context/archival). **Nicht** `state/` | `src/harness/memory/`, Skill `memory-architect` | `skills-authoring-policy.md` |
| **Knowledge** | Dauerhaftes, verlinktes Langzeitwissen (`[[wiki-links]]`, MOCs) | `.ai-workspace/knowledge/` | `knowledge-graph-policy.md` |
| **Data-Space** | Manifest-only: Pointer auf *externe* Originaldaten, nie die Rohdaten selbst | `.ai-workspace/data-space/` | `knowledge-graph-policy.md`, `security-policy.md` §11 |
| **Source** | Registrierte externe Quelle (Datei/URL/Binär) mit Trust-Level | Eintrag in `state/source-registry.md` | `source-policy.md` |
| **Artifact** | Erzeugtes Output (Research/Deliverable/Note), getrackt per Index | Eintrag in `state/artifact-index.md` | `file-lifecycle.md` |
| **Adapter** | Projekt-/domänenspezifische Erweiterung; Core bleibt domain-neutral | `.ai-workspace/adapters/<slug>/` | `adapter-policy.md` |
| **Skill** | Tool-nativer, lauffähiger Baustein (dünner Wrapper über der Engine) | `.claude/skills/<slug>/` | `skills-authoring-policy.md` |
| **Delegation** | Jede ausgelagerte Arbeit (Subagent/Task/Routine); Output untrusted bis verifiziert | Vertrag, kein Ordner | `delegation-policy.md` |

## Was diese Foundation ist

**Execution-Schicht (neu in v3.0):**

- Eine lauffähige Engine `src/harness/` mit acht Bereichen: `eval`, `router`, `hitl`, `guardrails`, `observability`, `memory`, `orchestrator`, `skills`.
- 12 echte Claude-Code-Skills unter `.claude/skills/<slug>/` mit offiziellem SKILL.md-Frontmatter.
- **stdlib-first**: ein nacktes `pip install -e .` zieht **null** Third-Party-Wheels.
- **mock-offline by default** (`UAW_LLM=mock`): ruft ein Skill ein LLM auf, antwortet im Default ein deterministischer Mock, ohne Netz und ohne Key (grüne CI). Echte LLM-Calls sind opt-in (siehe [`install-harness.md`](install-harness.md)).
- Ein Eval-Gate mit Exit-Code-Semantik (nicht-null unter Schwelle): CI-tauglich, dogfoodet die eigenen Skills.

**Governance-Schicht (unverändert aus v2.0):**

- Eine Mount-Point-Disziplin gegen Parallelstrukturen.
- Ein Setup-Protokoll für saubere Adapter-Anbindung.
- Ein generisches Delegation-Modell ohne vordefinierte Agents.
- Ein Sicherheits-Default, der externe Inhalte als untrusted behandelt.
- Ein Context-Loading-Modell mit klaren Regeln (auto / on relevance / on request / never).
- Ein File-Lifecycle-Modell mit expliziten Retention-Regeln.
- Ein Markdown-Knowledge-Graph-Protokoll mit Obsidian-kompatiblen Konventionen.
- Eine Document-Normalization-Pipeline für externe Binärdateien.

## Was diese Foundation nicht ist

- Kein Coding-, HR-, Legal- oder Sales-Harness. Die Skills sind domain-neutrale Agent-Engineering-Bausteine, kein fertiges Fachsystem.
- Keine schwere Agent-Library und kein Wrapper um eine. Die Patterns sind aus öffentlichen OSS-Ideen **nachgebaut** (nicht eingebunden; siehe [`NOTICE`](NOTICE)).
- Kein RAG-System, keine Vector-Datenbank, kein Crawler (ein optionaler Vector-Memory-Backend ist ein opt-in Extra, niemals Source of Truth).
- Kein automatisiertes Binary-Parsing (kein PDF-Parser, kein OCR, kein Office-Reader).
- Kein Datenspeicher für sensible Rohdaten.
- Kein MCP-Default-Bundle. Hooks sind present-but-advisory (opt-in via `.claude/settings.json`).

## Skill-Katalog (12)

| Skill | Bereich | Engine-Modul |
|-------|---------|--------------|
| `eval-loop-builder` | Eval-Suiten + Gate | `harness.eval` |
| `eval-judge` | LLM-as-judge (Rubrik) | `harness.eval` |
| `guardrail-designer` | Input/Output-Validierung, `on_fail`-Enum | `harness.guardrails` |
| `observability-tracer` | Tracing mit `gen_ai.*`-Semconv | `harness.observability` |
| `hitl-gate` | Human-in-the-loop Approval-Pause | `harness.hitl` |
| `cost-latency-optimizer` | Caching / Batch / Streaming / Routing | `harness.router` |
| `multi-agent-topology` | Supervisor / Hierarchie / Network / Swarm | (Text + reference) |
| `orchestrator-patterns` | 5 Workflow-Muster + ReAct | `harness.orchestrator` |
| `memory-architect` | Memory scope x type | `harness.memory` |
| `agent-pattern-selector` | Triage / Einstieg (read-only) | (Router) |
| `skill-author` | Skills schreiben + linten | `harness.skills` |
| `skill-supply-chain-check` | Supply-Chain-Audit von Skill-Code | `harness.skills` |

In Claude Code laden die Skills bei Bedarf über ihre `description`, **nicht** in den 4-File-Boot-Context. Einstieg/Triage: `agent-pattern-selector` mappt ein Problem auf den richtigen Skill. Jeder Script-Skill ist ein dünner Wrapper (`.claude/skills/<slug>/scripts/run.py` forwarded an `harness.<area>.__main__`), **keine duplizierte Logik**. Skills schreiben/ändern: `.ai-workspace/skills-authoring-policy.md` + `python -m harness.skills lint .claude/skills`.

## Repo-Layout (Top-Ebenen)

```text
AGENTS.md / CLAUDE.md          Boot-Dateien (tool-neutraler Contract + Claude-Delta)
README.md / CHANGELOG.md       diese Datei + v2->v3-Migration
LICENSE / NOTICE               MIT + Attributions-Hinweis
install-checklist.md           manueller Governance-Copy-Flow
install-harness.md             pip install + Demos ausführen
pyproject.toml                 Paket "uaw-harness", deps=[] (stdlib-first)
.ai-workspace/                 GOVERNANCE: Markdown-only (Kern unverändert)
.claude/                       EXECUTION: Skills, settings.json (gesegneter Mount)
src/harness/                   die importierbare Engine (8 Bereiche, getestet)
examples/                      eine Offline-Demo pro Bereich
tests/                         pytest + goldene Eval-Suiten (Repo dogfoodet sein Gate)
sources/credits.md             jede geliehene Struktur-Idee attribuiert
.github/workflows/ci.yml       lint + test + Eval-Gate (Windows + Linux)
```

## Anti-Sprawl bleibt strikt

Die verbotenen Top-Level-Namen (`skills/`, `agents/`, `hooks/`, `harness/`, `mcp/` und weitere) bleiben verboten, mit **zwei begründeten Ausnahmen**: `.claude/` ist der einzige gesegnete Execution-Mount (`.claude/skills/`, nicht nacktes `skills/`), und Standard-Projekt-Infrastruktur (`src/`, `tests/`, `examples/`, `sources/`, `.github/`, `pyproject.toml`) steht auf der Allowlist. Innerhalb `.ai-workspace/` bleibt die Markdown-only-Regel **unverändert** streng. Details: `AGENTS.md` §3.

## Schutz vor versehentlichen Leaks (optionale git-Hooks)

Damit die reine *Nutzung* dieses Kits keine Echtdaten ins Repository trägt, liegen unter `.githooks/` zwei optionale Hooks bereit. Sie sind opt-in und greifen erst nach:

```sh
git config core.hooksPath .githooks
chmod +x .githooks/pre-commit .githooks/pre-push   # unixoide Systeme / Git-bash
```

- **pre-commit** blockt einen Commit, der eine per `.gitignore` ausgeschlossene Datei force-added (`git add -f`), ein Secret-Muster (Provider-Token, PEM-Schlüssel, hartcodierte Zuweisung) oder einen privaten Begriff enthält.
- **pre-push** wiederholt den Scan als Pre-Release-Check über den gesamten getrackten Baum.
- Echte Namen (Mandanten, Personen) kommen in die ungetrackte Datei `.private-scan-terms`, eine Zeile pro Begriff, nicht in den Hook-Code. Sie ist über `.gitignore` ausgeschlossen und wird nie committet.
- Eine bewusste Ausnahme bleibt möglich: `git commit --no-verify` bzw. `git push --no-verify`.
- Windows: Die Hooks brauchen LF-Zeilenenden; `.gitattributes` erzwingt das, sonst bricht die Shebang.

Aufbau, Anpassung und die vollständigen Skripte stehen in [`.ai-workspace/templates/git-hooks-template.md`](.ai-workspace/templates/git-hooks-template.md).

## Optionale Session-Automatik (opt-in)

Über die git-Hooks hinaus bringt die Execution-Schicht eine **optionale, schaltbare Session-Automatik** mit, **standardmäßig AUS**. Das Kit führt von selbst keinen Code aus; es weist nur auf die Möglichkeit hin, sie zu aktivieren. Zwei Fähigkeiten, beide lokal, modellgetrieben und reversibel (Prinzip: *der Hook erinnert, das Modell schreibt*; kein Script verändert je den State):

- **boot_reload** (`SessionStart`): lädt beim Start `.ai-workspace/state/current-session.md` als Kontext, damit jede neue, fortgesetzte oder compactete Session sofort mit dem Live-Zustand bootet.
- **recitation_nudge** (`PostToolUse`): erinnert nach einer Datei-Änderung daran, `current-session.md` fortzuschreiben (gemäß `session-contract.md` §3).

Aktivieren, erklären lassen oder wieder abschalten: alles über den Begleiter `/uaw-automation`, oder direkt über den Toggle `.claude/automation.flags.json` (Default `{ "boot_reload": false, "recitation_nudge": false }`). Die Hooks sind in `.claude/settings.json` registriert, aber **self-gated**: solange ein Flag `false` ist, beenden sie sich ohne jede Ausgabe (inert). Weil sie committet sind, greifen sie auch in Web-/Cloud-Sessions; sie steuern ausschließlich dieses Repo und rühren globale `~/.claude/`-Konfiguration nie an. Vollständige Operator-Doku: [`.claude/AUTOMATION.md`](.claude/AUTOMATION.md).

## Upgrade von v2.0

v2.0 war eine reine Markdown-Kontroll- und Policy-Schicht („kein Agent-Harness, kein Skill-Pack"). v3.0 behält diese Schicht **unverändert in ihrer Rolle** und legt die Execution-Schicht daneben.

- **Nichts Bestehendes bricht.** `.ai-workspace/` und die Boot-Dateien funktionieren wie zuvor; die Markdown-only-Disziplin im Governance-Kern bleibt strikt.
- **Neu hinzugekommen:** `.claude/`, `src/harness/`, `tests/`, `examples/`, `sources/`, `pyproject.toml`, `.github/`, aktive `.gitignore`/`.claudeignore`, `NOTICE`, `CHANGELOG.md`.
- **Die Verfassung wurde nachgezogen:** `AGENTS.md` (§2.5 Zwei-Schichten-Modell, §3 Carve-outs), `setup-protocol.md`, `security-policy.md`, `adapter-policy.md` und die neue `skills-authoring-policy.md` legitimieren den Execution-Mount, ohne die Anti-Sprawl-Disziplin aufzugeben.
- **Migration eines bestehenden v2.0-Projekts:** Bleib rein bei der Governance-Schicht (nichts zu tun) oder übernimm die Harness-Schicht als Einheit. Siehe [`CHANGELOG.md`](CHANGELOG.md) und [`install-harness.md`](install-harness.md).

## Nächste Schritte

- Code ausführen: [`install-harness.md`](install-harness.md).
- Optionale Session-Automatik (opt-in, default AUS): `/uaw-automation` bzw. [`.claude/AUTOMATION.md`](.claude/AUTOMATION.md).
- Governance verstehen: `AGENTS.md`, dann `.ai-workspace/README.md` (vollständige Mount-Point-Map).
- Skills schreiben: `.ai-workspace/skills-authoring-policy.md`.
- Knowledge-Graph: `.ai-workspace/knowledge-graph-policy.md`.
- Attribution: [`NOTICE`](NOTICE) + [`sources/credits.md`](sources/credits.md).

## Lizenz

MIT, siehe [`LICENSE`](LICENSE). Patterns sind aus öffentlichen OSS-Ideen nachgebaut; kein Upstream-Code oder -Prosa wurde kopiert ([`NOTICE`](NOTICE)).

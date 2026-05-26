# Universal AI Workspace Foundation

Ein lauffaehiges, domain-neutrales Starter-Harness fuer Projekte, die mit AI-Assistants (Claude
Code zuerst) bearbeitet werden. Zwei Schichten in einem Repo: eine **Governance-Schicht** aus
striktem Markdown und eine **Execution-Schicht** aus echtem, getestetem Python.

> **v3.0** — Diese Version macht aus dem fruheren reinen Markdown-Regelwerk ein echtes Harness:
> 12 Claude-Code-Skills ueber einer pip-installierbaren Engine (`src/harness/`), die offline im
> Mock-Modus laeuft — kein API-Key, keine Netzwerkverbindung, keine schwere Agent-Library.
> Migration von v2.0: siehe [`CHANGELOG.md`](CHANGELOG.md) und Abschnitt *Upgrade von v2.0* unten.

## Das Zwei-Schichten-Modell

Die Foundation trennt sauber, was *persistiert*, von dem, was *laeuft*:

| Schicht | Pfad | Rolle | Format |
|---------|------|-------|--------|
| **Governance + State + Memory** | `.ai-workspace/` | Regeln, Zustand, Wissen — die Wahrheit, die persistiert | Markdown-only (strikt) |
| **Execution** | `.claude/` + `src/harness/` | tool-nativer Code, der laeuft — Skills + Engine | Code |

Die Grenze ist scharf: **Code, der laeuft, lebt in `.claude/` und `src/`. Wahrheit, die
persistiert, lebt in `.ai-workspace/`.** Keine Schicht schreibt die kanonischen Dateien der
anderen. Skill-*Outputs* sind delegierte Arbeit (untrusted bis verifiziert) und folgen dem
`scratch/`/`research/`-Lifecycle — sie mutieren `state/` nur ueber den deklarierten
State-Write-Contract (`.ai-workspace/skills-authoring-policy.md`). Details: `AGENTS.md` §2.5.

`.ai-workspace/` und `AGENTS.md` bleiben tool-neutral. `.claude/` ist Claude-Code-spezifisch; die
Engine `src/harness/` ist tool-unabhaengig und auch ohne `.claude/` nutzbar
(`python -m harness.<area>`).

## Was diese Foundation IST

**Execution-Schicht (neu in v3.0):**

- Eine lauffaehige Engine `src/harness/` mit acht Bereichen: `eval`, `router`, `hitl`,
  `guardrails`, `observability`, `memory`, `orchestrator`, `skills`.
- 12 echte Claude-Code-Skills unter `.claude/skills/<slug>/` mit offiziellem SKILL.md-Frontmatter.
- **stdlib-first**: ein nacktes `pip install -e .` zieht **null** Third-Party-Wheels.
- **mock-offline by default** (`UAW_LLM=mock`): deterministisch, ohne Netz/Key → gruene CI.
- Ein Eval-Gate mit Exit-Code-Semantik (nicht-null unter Schwelle) — CI-tauglich, dogfoodet die
  eigenen Skills.

**Governance-Schicht (unveraendert aus v2.0):**

- Eine Mount-Point-Disziplin gegen Parallelstrukturen.
- Ein Setup-Protokoll fuer saubere Adapter-Anbindung.
- Ein generisches Delegation-Modell ohne vordefinierte Agents.
- Ein Sicherheits-Default mit Untrusted-Default fuer externe Inhalte.
- Ein Context-Loading-Modell mit klaren Regeln (auto / on relevance / on request / never).
- Ein File-Lifecycle-Modell mit expliziten Retention-Regeln.
- Ein Markdown-Knowledge-Graph-Protokoll mit Obsidian-kompatiblen Konventionen.
- Eine Document-Normalization-Pipeline fuer externe Binaerdateien.

## Was diese Foundation NICHT ist

- Kein Coding-, HR-, Legal- oder Sales-Harness — die Skills sind domain-neutrale
  Agent-Engineering-Bausteine, kein fertiges Fachsystem.
- Keine schwere Agent-Library und kein Wrapper um eine — die Patterns sind aus oeffentlichen
  OSS-Ideen **nachgebaut**, nicht eingebunden (siehe [`NOTICE`](NOTICE)).
- Kein RAG-System, keine Vector-Datenbank, kein Crawler (ein optionaler Vector-Memory-Backend ist
  ein opt-in Extra, niemals Source of Truth).
- Kein automatisiertes Binary-Parsing (kein PDF-Parser, kein OCR, kein Office-Reader).
- Kein Datenspeicher fuer sensible Rohdaten.
- Kein MCP-Default-Bundle. Hooks sind present-but-advisory (opt-in via `.claude/settings.json`).

## Quickstart — Execution-Schicht (lauffaehig)

```bash
# bare install — zieht ZERO Third-Party-Wheels, alles laeuft im Mock-Modus
pip install -e .

# Offline-Demo: ein gewichtetes Eval-Gate
python examples/eval_demo.py

# Eval-Gate gegen die Repo-Invarianten (exit 0 = bestanden)
python -m harness.eval run --suite tests/goldens/repo.suite.json --threshold 0.9
```

Python >= 3.10. Identisch auf Windows, macOS, Linux (Aufruf immer `python -m harness.<area>`, nie
ein Shell-Skript). Vollstaendige Anleitung inkl. Extras und Mock-vs-Live:
[`install-harness.md`](install-harness.md).

In Claude Code laden die 12 Skills bei Bedarf ueber ihre `description` — **nicht** in den
4-File-Boot-Context. Einstieg/Triage: der Skill `agent-pattern-selector` mappt ein Problem auf den
richtigen Skill.

## Quickstart — Governance-Schicht (in ein Projekt uebernehmen)

Zwei Wege zum selben Ziel — die Governance-Schicht sauber in dein Projekt bringen.

### Variante A (empfohlen): gefuehrtes Onboarding

Besonders fuer ein **bestehendes Projekt** mit eigener Ordnerstruktur, die migriert werden soll.

- **Foundation schon kopiert / `.claude/` vorhanden?** Fuehre in deinem Projekt `/onboard` aus
  ([`.claude/commands/onboard.md`](.claude/commands/onboard.md)). Der Befehl analysiert deine
  Struktur, entscheidet mit dir Governance-only vs. +Execution, liefert einen Migrationsplan und
  wartet auf deine Bestaetigung, bevor er irgendetwas aendert.
- **Noch nichts installiert? Kalt-Start ohne Klonen:** Oeffne dein Projekt in Claude Code und gib
  diesen Prompt ein — er liest dieses oeffentliche Repo nur als Referenz, kopiert/installiert nichts:

  ```text
  Du arbeitest in meinem aktuellen Projekt und sollst pruefen, ob und wie es sich an der
  Universal AI Workspace Foundation (v3.0) ausrichten laesst.

  Die Foundation hat ZWEI Schichten — wir entscheiden gemeinsam, welche dieses Projekt braucht:
  - Governance (.ai-workspace/, reines Markdown): Regeln, Zustand, Wissen. Fast immer sinnvoll.
  - Execution (.claude/ + src/harness/, Python): 12 Claude-Code-Skills ueber einer
    pip-installierbaren Engine (Evals, Guardrails, Tracing, HITL, Routing, Memory,
    Orchestrierung). Nur wenn das Projekt sie wirklich nutzt.

  Schritt 1 — Analysiere die vorhandene Projektstruktur (Ordner; wo Notizen/Prompts/Agents/Docs/
  Wissen/Sessions/Code/Temp liegen; doppelte oder unklare Strukturen).
  Schritt 2 — Nutze dieses oeffentliche Repo als Referenz (nur lesen, nichts klonen/installieren):
  https://github.com/Luis247911/universal-ai-workspace-foundation
  Lies: README.md, AGENTS.md (§2.5, §3), install-checklist.md, install-harness.md (nur falls
  relevant), .ai-workspace/setup-protocol.md (§3 Frage 0 + §2 vier Setup-Fragen).
  Schritt 3 — Entscheide MIT MIR: nur Governance, oder auch Execution? Begruende anhand Schritt 1.

  Regeln (nicht verhandelbar): nichts blind uebernehmen; nichts ohne Rueckfrage loeschen; keine
  neuen Top-Level-Ordner ohne Rueckfrage (Anti-Sprawl — einziger Code-Mount .claude/, sonst
  src/tests/examples); vorhandene Ordner (agents/prompts/notes/docs/wiki/skills/tasks) sauber
  migrieren statt Parallelstruktur; erst Plan erklaeren, dann aendern.

  Liefere zuerst (noch nichts anlegen): 1. Analyse. 2. Empfehlung Governance-only vs. +Execution
  (begruendet). 3. Was uebernehmen. 4. Was nicht. 5. Schrittweiser Migrationsplan (Governance
  zuerst, Execution optional). 6. Liste neu/geaendert. Warte danach auf meine Bestaetigung.
  ```

### Variante B: manuell (sechs Schritte)

Fuer einen sauberen Start in einem leeren oder neuen Projektverzeichnis.

1. Lege ein leeres Projektverzeichnis an.
2. Kopiere den Inhalt dieses Foundation-Tree in das Projektverzeichnis.
3. Folge [`install-checklist.md`](install-checklist.md) Schritt fuer Schritt (entscheide dort, ob
   das Projekt die optionale Harness-Schicht mitnimmt).
4. Lies `AGENTS.md` als tool-agnostischen Root-Contract.
5. Initialisiere `.ai-workspace/state/project-index.md` und `current-session.md` aus den Templates.
6. Beantworte die vier Setup-Fragen aus `.ai-workspace/setup-protocol.md` (Knowledge-Graph,
   Project Data Space, Maintenance Routines, Document Normalization).

Reine Governance-Nutzung (nur `.ai-workspace/` + die Root-Boot-Dateien, ohne `.claude/`/`src/`)
ist weiterhin moeglich.

## Skill-Katalog (12)

| Skill | Bereich | Engine-Modul |
|-------|---------|--------------|
| `eval-loop-builder` | Eval-Suiten + Gate | `harness.eval` |
| `eval-judge` | LLM-as-judge (Rubrik) | `harness.eval` |
| `guardrail-designer` | Input/Output-Validierung, `on_fail`-Enum | `harness.guardrails` |
| `observability-tracer` | Tracing mit `gen_ai.*`-Semconv | `harness.observability` |
| `hitl-gate` | Human-in-the-loop Approval-Pause | `harness.hitl` |
| `cost-latency-optimizer` | Caching / Batch / Streaming / Routing | `harness.router` |
| `multi-agent-topology` | Supervisor / Hierarchie / Network / Swarm | — (Text + reference) |
| `orchestrator-patterns` | 5 Workflow-Muster + ReAct | `harness.orchestrator` |
| `memory-architect` | Memory scope × type | `harness.memory` |
| `agent-pattern-selector` | Triage / Einstieg (read-only) | — (Router) |
| `skill-author` | Skills schreiben + linten | `harness.skills` |
| `skill-supply-chain-check` | Supply-Chain-Audit von Skill-Code | `harness.skills` |

Jeder Script-Skill ist ein duenner Wrapper: `.claude/skills/<slug>/scripts/run.py` forwarded an
`harness.<area>.__main__` — **keine duplizierte Logik**. Skills schreiben/aendern:
`.ai-workspace/skills-authoring-policy.md` + `python -m harness.skills lint .claude/skills`.

## Repo-Layout (Top-Ebenen)

```text
AGENTS.md / CLAUDE.md          Boot-Dateien (tool-neutraler Contract + Claude-Delta)
README.md / CHANGELOG.md       diese Datei + v2→v3-Migration
LICENSE / NOTICE               MIT + Attributions-Hinweis
install-checklist.md           manueller Governance-Copy-Flow
install-harness.md             pip install + Demos ausfuehren
pyproject.toml                 Paket "uaw-harness", deps=[] (stdlib-first)
.ai-workspace/                 GOVERNANCE — Markdown-only (Kern unveraendert)
.claude/                       EXECUTION — Skills, settings.json (gesegneter Mount)
src/harness/                   die importierbare Engine (8 Bereiche, getestet)
examples/                      eine Offline-Demo pro Bereich
tests/                         pytest + goldene Eval-Suiten (Repo dogfoodet sein Gate)
sources/credits.md             jede geliehene Struktur-Idee attribuiert
.github/workflows/ci.yml       lint + test + Eval-Gate (Windows + Linux)
```

## Anti-Sprawl bleibt strikt

Die verbotenen Top-Level-Namen (`skills/`, `agents/`, `hooks/`, `harness/`, `mcp/`, …) bleiben
verboten — mit **zwei begruendeten Ausnahmen**: `.claude/` ist der einzige gesegnete Execution-Mount
(`.claude/skills/`, nicht nacktes `skills/`), und Standard-Projekt-Infrastruktur (`src/`, `tests/`,
`examples/`, `sources/`, `.github/`, `pyproject.toml`) ist Allowlist. Innerhalb `.ai-workspace/`
bleibt die Markdown-only-Regel **unveraendert** streng. Details: `AGENTS.md` §3.

## Markdown-first (Governance-Schicht)

Alle Dateien der Governance-Schicht (`.ai-workspace/**`) sind `.md`. Die Execution-Schicht ist Code
und davon ausgenommen. Externe Binaerdateien (PDF, DOCX, PPTX, XLSX, Bilder, Audio, Video) duerfen
referenziert werden, niemals als kanonische Arbeitsfassung. Bei kritischen Aussagen (Zahlen, Daten,
Fristen, Namen, Tabellenwerte, Definitionen, Negationen, Vertragsaussagen) muss auf das
Originaldokument oder die Normalization Review zurueckverwiesen werden.

## Upgrade von v2.0

v2.0 war eine reine Markdown-Kontroll-/Policy-Schicht („kein Agent-Harness, kein Skill-Pack"). v3.0
behaelt diese Schicht **unveraendert in ihrer Rolle** und legt die Execution-Schicht daneben.

- **Nichts Bestehendes bricht.** `.ai-workspace/` und die Boot-Dateien funktionieren wie zuvor; die
  Markdown-only-Disziplin im Governance-Kern ist unveraendert strikt.
- **Neu hinzugekommen:** `.claude/`, `src/harness/`, `tests/`, `examples/`, `sources/`,
  `pyproject.toml`, `.github/`, aktive `.gitignore`/`.claudeignore`, `NOTICE`, `CHANGELOG.md`.
- **Die Verfassung wurde nachgezogen:** `AGENTS.md` (§2.5 Zwei-Schichten-Modell, §3 Carve-outs),
  `setup-protocol.md`, `security-policy.md`, `adapter-policy.md` und die neue
  `skills-authoring-policy.md` legitimieren den Execution-Mount, ohne die Anti-Sprawl-Disziplin
  aufzugeben.
- **Migration eines bestehenden v2.0-Projekts:** Du kannst rein bei der Governance-Schicht bleiben
  (nichts zu tun) oder die Harness-Schicht als Einheit uebernehmen — siehe
  [`CHANGELOG.md`](CHANGELOG.md) und [`install-harness.md`](install-harness.md).

## Naechste Schritte

- Code ausfuehren: [`install-harness.md`](install-harness.md).
- Governance verstehen: `AGENTS.md`, dann `.ai-workspace/README.md` (vollstaendige Mount-Point-Map).
- Skills schreiben: `.ai-workspace/skills-authoring-policy.md`.
- Knowledge-Graph: `.ai-workspace/knowledge-graph-policy.md`.
- Attribution: [`NOTICE`](NOTICE) + [`sources/credits.md`](sources/credits.md).

## Lizenz

MIT — siehe [`LICENSE`](LICENSE). Patterns sind aus oeffentlichen OSS-Ideen nachgebaut; kein
Upstream-Code oder -Prosa wurde kopiert ([`NOTICE`](NOTICE)).

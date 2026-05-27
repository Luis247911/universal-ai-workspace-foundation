# Universal AI Workspace Foundation

Ein Starter-Kit für Projekte, die du mit einem AI-Coding-Assistenten bearbeitest (zuerst für Claude Code gebaut). Es bringt zwei Dinge in einem Repo zusammen:

1. **Regeln und Gedächtnis** in reinem Markdown (Ordner `.ai-workspace/`): klare Konventionen, wo was liegt, plus einen Wissens- und Zustandsspeicher, den der Assistent über mehrere Sitzungen hinweg liest.
2. **Lauffähige Werkzeuge** (Ordner `.claude/` + `src/harness/`): 12 fertige Bausteine („Skills") über einer kleinen Python-Engine. Damit kannst du zum Beispiel die Antworten eines AI-Agenten automatisch bewerten (Eval), riskante Ein- und Ausgaben blockieren (Guardrail) oder vor einem kritischen Schritt einen Menschen freigeben lassen (Human-in-the-Loop).

Du nimmst beide Schichten oder nur die Regeln. Die Werkzeuge laufen offline: ohne API-Key, ohne Internet, ohne große Zusatz-Bibliotheken.

**Für wen?** Für Entwickler, die AI-Projekte sauber aufsetzen wollen, statt Prompts und Skripte immer wieder zu kopieren. Du solltest mit Kommandozeile und Python umgehen können; tiefe AI-Vorkenntnisse sind nicht nötig.

## Schnellstart

Voraussetzung: Python >= 3.10. Empfohlen ist ein virtuelles Environment, damit nichts global installiert wird.

```bash
python -m venv .venv
. .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -e .              # installiert das Paket "uaw-harness", zieht KEINE Fremd-Pakete
python examples/eval_demo.py  # Offline-Demo eines bewerteten Eval-Gates -> endet mit "PASS" (exit 0)
```

Aufrufe der Engine laufen über `python -m harness.<bereich>` (CLI-Name `harness`, Paketname `uaw-harness`). Identisch auf Windows, macOS, Linux. Volle Anleitung inkl. Extras und echtem LLM statt Mock: [`install-harness.md`](install-harness.md).

Nur die Regeln in ein Projekt holen: folge [`install-checklist.md`](install-checklist.md). Hat dein Projekt schon `.claude/`, führe `/onboard` aus; der Befehl analysiert deine Struktur und fragt nach, bevor er etwas ändert.

## Das Zwei-Schichten-Modell

Die Foundation trennt sauber, was *persistiert*, von dem, was *läuft*:

| Schicht | Pfad | Rolle | Format |
|---------|------|-------|--------|
| **Governance + State + Memory** | `.ai-workspace/` | Regeln, Zustand, Wissen: die Wahrheit, die persistiert | Markdown-only (strikt) |
| **Execution** | `.claude/` + `src/harness/` | tool-nativer Code, der läuft: Skills + Engine | Code |

Die Grenze ist scharf: **Code, der läuft, lebt in `.claude/` und `src/`. Wahrheit, die persistiert, lebt in `.ai-workspace/`.** Keine Schicht schreibt die kanonischen Dateien der anderen. Skill-*Outputs* sind delegierte Arbeit (untrusted bis verifiziert) und folgen dem `scratch/`/`research/`-Lifecycle; `state/` ändern sie nur über den deklarierten State-Write-Contract (`.ai-workspace/skills-authoring-policy.md`). Details: `AGENTS.md` §2.5.

`.ai-workspace/` und `AGENTS.md` bleiben tool-neutral. `.claude/` ist Claude-Code-spezifisch; die Engine `src/harness/` ist tool-unabhängig und auch ohne `.claude/` nutzbar.

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
install-checklist.md           manueller Governance-Copy-Flow (inkl. Onboarding-Prompt)
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

## Upgrade von v2.0

v2.0 war eine reine Markdown-Kontroll- und Policy-Schicht („kein Agent-Harness, kein Skill-Pack"). v3.0 behält diese Schicht **unverändert in ihrer Rolle** und legt die Execution-Schicht daneben.

- **Nichts Bestehendes bricht.** `.ai-workspace/` und die Boot-Dateien funktionieren wie zuvor; die Markdown-only-Disziplin im Governance-Kern bleibt strikt.
- **Neu hinzugekommen:** `.claude/`, `src/harness/`, `tests/`, `examples/`, `sources/`, `pyproject.toml`, `.github/`, aktive `.gitignore`/`.claudeignore`, `NOTICE`, `CHANGELOG.md`.
- **Die Verfassung wurde nachgezogen:** `AGENTS.md` (§2.5 Zwei-Schichten-Modell, §3 Carve-outs), `setup-protocol.md`, `security-policy.md`, `adapter-policy.md` und die neue `skills-authoring-policy.md` legitimieren den Execution-Mount, ohne die Anti-Sprawl-Disziplin aufzugeben.
- **Migration eines bestehenden v2.0-Projekts:** Bleib rein bei der Governance-Schicht (nichts zu tun) oder übernimm die Harness-Schicht als Einheit. Siehe [`CHANGELOG.md`](CHANGELOG.md) und [`install-harness.md`](install-harness.md).

## Nächste Schritte

- Code ausführen: [`install-harness.md`](install-harness.md).
- Governance verstehen: `AGENTS.md`, dann `.ai-workspace/README.md` (vollständige Mount-Point-Map).
- Skills schreiben: `.ai-workspace/skills-authoring-policy.md`.
- Knowledge-Graph: `.ai-workspace/knowledge-graph-policy.md`.
- Attribution: [`NOTICE`](NOTICE) + [`sources/credits.md`](sources/credits.md).

## Lizenz

MIT, siehe [`LICENSE`](LICENSE). Patterns sind aus öffentlichen OSS-Ideen nachgebaut; kein Upstream-Code oder -Prosa wurde kopiert ([`NOTICE`](NOTICE)).

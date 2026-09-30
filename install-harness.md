# Running the harness (`.claude/` + `src/harness/`)

This is the **execution layer** of the universal-ai-workspace-foundation. It ships small,
dependency-light, teaching-grade reference implementations of agent-engineering patterns,
plus the Claude Code skills that wrap them. Everything runs **offline in mock mode** by
default — no API key, no network, no third-party agent library.

> For the Markdown governance layer (state, knowledge graph, policies), see
> [`install-checklist.md`](install-checklist.md). This document covers the runnable code only.

## Install

```bash
# bare install — pulls in ZERO third-party wheels, runs everything in mock mode
pip install -e .

# with developer tooling (pytest, ruff, mypy, pyyaml)
pip install -e ".[dev]"

# everything (adds numpy vector backend + anthropic live LLM)
pip install -e ".[all]"
```

Requires Python >= 3.10. Works identically on Windows, macOS, and Linux (invocation is
always `python -m harness.<area>`, never a shell script).

## Optional extras

| Extra | Adds | Needed for |
|-------|------|-----------|
| `yaml` | PyYAML | authoring suites/configs in YAML (JSON works without it) |
| `vector` | numpy | the real cosine memory backend (pure-Python default needs nothing) |
| `llm` | anthropic | live model calls (`UAW_LLM=live` + `ANTHROPIC_API_KEY`) |
| `test` / `lint` / `types` / `dev` | pytest / ruff / mypy | contributing |

## Try it (offline)

```bash
python examples/eval_demo.py                 # weighted eval gate
python -m harness.eval run --suite tests/goldens/repo.suite.json --threshold 0.9
```

## Mock vs live

- Default `UAW_LLM=mock`: deterministic canned responses → green CI without secrets.
- `UAW_LLM=live` (needs `[llm]` extra + `ANTHROPIC_API_KEY`): real model calls. LLM-graded
  eval assertions (`llm_rubric`) are **skipped** in mock mode and **scored** when live.
- Live model: `claude-opus-5-5` by default; override with `UAW_MODEL=<model-id>` or `model=`.
  On models that support it, a server-side refusal fallback (`fallbacks="default"`) is enabled;
  a remaining refusal raises `HarnessError`.

## The workspace memory needs no install

The memory engine `harness.mdmemory` and its hooks use the standard library only and run with any
Python >= 3.9 (including the stock macOS `/usr/bin/python3`), straight from the checkout:

```bash
python3 .claude/uaw/mdm.py lint          # same as: python -m harness.mdmemory lint
python3 .claude/uaw/mdm.py adopt ../other-project --dry-run
```

Hooks run as `sh .claude/hooks/run.sh <hook>.py`; the launcher picks `$UAW_PYTHON`, `python3` or
`python`. On by default: `now_init`, `index_refresh`, `memory_boot`, `journal_stub`,
`precompact_reminder` (see `.claude/AUTOMATION.md`). `adopt` copies the engine to
`.claude/uaw/` of another project, so that project needs no install either.

## Optional: session automation (opt-in)

The execution layer also ships **optional** session helpers, **off by default**; you opt in per
capability. Both are local and model-driven: *the hook reminds, the model writes*.

- **boot_reload** (`SessionStart`) re-injects `.ai-workspace/state/now.md` so a
  new / resumed / compacted session boots with the live state in view.
- **recitation_nudge** (`PostToolUse`) nudges you to keep `now.md` and the session journal current after a
  file edit, per `session-contract.md` section 3.

Toggle it through the `/uaw-automation` companion, or edit `.claude/automation.flags.json`:

```json
{ "boot_reload": true, "recitation_nudge": true }
```

The hooks are registered in `.claude/settings.json` but do nothing while their flag is `false`
(they exit immediately with no output), so a fresh clone stays silent until you opt in. Being
committed, they also run in web/cloud sessions; the launcher `run.sh` picks `python3` or
`python`. They touch only this repo, never your global `~/.claude/`. Full operator
docs: [`.claude/AUTOMATION.md`](.claude/AUTOMATION.md).

## Layout

```
src/harness/        the importable engine (pip-installable, tested)
  core/             shared primitives (state, types, jsonio, paths, llm, config)
  eval/ router/ hitl/ guardrails/ observability/ memory/ orchestrator/
.claude/skills/     Claude Code skills that wrap the engine (thin scripts/run.py)
examples/           one offline demo per area
tests/              pytest + golden eval suites (the repo dogfoods its own eval gate)
```

Patterns are reimplemented from public OSS ideas — see [`NOTICE`](NOTICE) and
[`sources/credits.md`](sources/credits.md). No upstream code is copied.

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

## Optional: session automation (opt-in)

The execution layer also ships an **optional, committed session-automation layer**, **off by
default**. Nothing fires on a fresh clone; you opt in per capability. Both are local and
model-driven: *the hook reminds, the model writes* — no script ever mutates state.

- **boot_reload** (`SessionStart`) re-injects `.ai-workspace/state/current-session.md` so a
  new / resumed / compacted session boots with the live state in view.
- **recitation_nudge** (`PostToolUse`) nudges you to keep `current-session.md` current after a
  file edit, per `session-contract.md` section 3.

Toggle it through the `/uaw-automation` companion, or edit `.claude/automation.flags.json`:

```json
{ "boot_reload": true, "recitation_nudge": true }
```

The hooks are registered in `.claude/settings.json` but do nothing while their flag is `false`
(they exit immediately with no output), so a fresh clone stays silent until you opt in. Being
committed, they also run in web/cloud sessions; the launcher is `python` (use `python3` where
that is the only name). They touch only this repo, never your global `~/.claude/`. Full operator
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

# Credits & Attribution

This harness reimplements **structural ideas** from public agent-engineering projects, papers, and
standards. It does **not** vendor, fork, or copy any upstream code or prose. Every module here was
written from scratch against a mental model of the pattern — not against the upstream source tree.

## How to read this file

- **"Idea borrowed"** describes the *shape* we reused (an enum, a topology, a workflow pattern), not
  any implementation detail.
- **No code or prose was copied** from any source listed below. Where a source is the canonical
  origin of a *name* (e.g. an OpenTelemetry attribute key), we reuse the **name only** as a
  string constant for interoperability — names are not copyrightable expression.
- **Licenses are stated as of this writing and should be re-verified at the source** before you rely
  on them. They describe the upstream project, not this repo (this repo is MIT — see `LICENSE`).
- We deliberately took **no dependency** on any of these projects. A bare `pip install -e .` pulls
  zero third-party wheels (see `pyproject.toml`).

## OSS projects — structural ideas, reimplemented with attribution

| Engine area | Inspiration | License (verify at source) | Idea borrowed (no code copied) |
|-------------|-------------|----------------------------|--------------------------------|
| `eval` | [promptfoo](https://github.com/promptfoo/promptfoo) | MIT | Declarative test-suite-as-config with per-case assertions and a pass-threshold gate |
| `eval` | [DeepEval](https://github.com/confident-ai/deepeval) | Apache-2.0 | Assertion taxonomy (exact/contains/regex vs. model-graded), eval-as-unit-test framing |
| `eval` (judge) | LLM-as-a-judge (general technique) | — (community practice) | Rubric scoring + reason-then-extract + categorical verdicts; reasoning discarded after the score |
| `guardrails` | [Guardrails AI](https://github.com/guardrails-ai/guardrails) | Apache-2.0 | Validator-with-`on_fail`-action shape (reask/fix/filter/refrain/exception) |
| `guardrails` | [NeMo Guardrails](https://github.com/NVIDIA/NeMo-Guardrails) | Apache-2.0 | Input/output rail separation as distinct policy stages |
| `observability` | [OpenTelemetry GenAI semantic conventions](https://github.com/open-telemetry/semantic-conventions) | Apache-2.0 | The `gen_ai.*` attribute **names**, reused as string constants for interop (no SDK dependency) |
| `observability` | [Langfuse](https://github.com/langfuse/langfuse) | MIT | Span-per-LLM-call tracing model with explicit, opt-in content capture |
| `observability` | [Arize Phoenix](https://github.com/Arize-ai/phoenix) | Elastic License 2.0 (source-available, **not** OSI-open) | High-level concept of LLM-app trace/eval observability only — concept reference, nothing reused; the actual attribute names come from OpenTelemetry above |
| `hitl` | [LangGraph](https://github.com/langchain-ai/langgraph) | MIT | `interrupt()`-style pause/resume where a run survives process exit and re-enters on approve/deny |
| `hitl` | [HumanLayer](https://github.com/humanlayer/humanlayer) | Apache-2.0 | Human-approval-as-a-gate around a delegated step |
| `router` | [LiteLLM](https://github.com/BerriAI/litellm) | MIT | Router + fallback-chain shape across providers/models on error/rate-limit |
| `router` (cost/latency) | Prompt-caching / batch / streaming / routing | — (vendor-documented techniques) | The four cost-latency levers as a checklist + a cache-breakpoint lint heuristic |
| `memory` | [mem0](https://github.com/mem0ai/mem0) | Apache-2.0 | Memory **scope** dimension (user / session / agent) |
| `memory` | [Letta / MemGPT](https://github.com/letta-ai/letta) | Apache-2.0 | Memory **type** dimension (core / recall / archival) |
| `orchestrator` (topologies) | [AutoGen](https://github.com/microsoft/autogen), [CrewAI](https://github.com/crewAIInc/crewAI), [OpenAI Agents SDK](https://github.com/openai/openai-agents-python), [LangGraph](https://github.com/langchain-ai/langgraph) | MIT (each) | Multi-agent topology vocabulary: supervisor / hierarchical / network / swarm; handoff-as-control-transfer |
| `orchestrator` (patterns) | ReAct (Yao et al., 2022) | academic paper ([arXiv:2210.03629](https://arxiv.org/abs/2210.03629)) | The reason→act→observe loop as one orchestration pattern (concept, not Anthropic) |
| `skills` | Skill-authoring conventions (general) | — (community/tooling practice) | Frontmatter contract, evals-first authoring, thin-wrapper discipline |

## Anthropic concepts — names only (proprietary docs, nothing copied)

Anthropic's published guidance is proprietary. We reuse **only concept names**, never prose or code:

- **"Building Effective Agents"** workflow *shape names*: prompt-chaining (sequential), routing,
  parallelization, orchestrator-workers, evaluator-optimizer — used as labels in
  `harness.orchestrator` and `agent-pattern-selector`. The simplicity-first framing ("use the
  simplest thing that works") informs the selector's bias. No text was reproduced.
- **Agent Skills / SKILL.md** frontmatter conventions (the `name`/`description` contract, progressive
  disclosure) inform `skills-authoring-policy.md` and the `skill-author` skill. The schema fields are
  reimplemented; no documentation prose was copied.

## What we did NOT do

- No `git clone`, no vendored source, no fork of any project above.
- No copied README sections, no copied code, no copied docstrings or prompts.
- No runtime dependency on any listed project (heavy agent libraries are intentionally absent — see
  `pyproject.toml`; the only optional third-party extras are PyYAML, numpy, anthropic, and dev tools).

## Maintenance

When a new borrowed pattern is added to the harness, add a row here **and** to `NOTICE` in the same
change. This is a documented quality gate (`.ai-workspace/quality-gates.md`).

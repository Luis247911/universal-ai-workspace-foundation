# reference — workflow patterns

The simplest-first catalogue. Each entry: what it is, when to use it, when it hurts, and the runnable command.

## Workflows vs agents

- **Workflow**: the steps are known ahead of time and orchestrated by code (chaining, routing, parallel). Predictable, debuggable, cheap.
- **Agent**: the model decides the steps dynamically in a loop (ReAct, evaluator-optimizer). Flexible, but costlier and harder to bound.

Prefer a workflow when you can enumerate the steps. Use an agentic loop only when you cannot.

## 1. Prompt chaining — `sequential`

Fixed ordered steps; each output is the next input. Use when a task cleanly decomposes
(outline → draft → polish). Add a check between steps to fail fast. Hurts when steps are not
actually sequential (then parallelize). `run --pattern sequential`.

## 2. Routing — `router`

Classify the input, then dispatch to a specialized handler/prompt. Use when inputs fall into
distinct kinds (billing vs technical). Keeps each handler simple. Hurts when the classifier is
wrong — measure it. `run --pattern router`.

## 3. Parallel: sectioning — `parallel`

Split into independent subtasks, run concurrently, join the parts. Use for latency wins or to
separate concerns (risks / tests / docs in parallel). Hurts when subtasks are not independent.
`run --pattern parallel`.

## 4. Parallel: voting — `vote`

Run the same task several times and aggregate (majority or best-of). Use to raise reliability
on a hard call or to reduce variance. Costs N×; reserve for high-stakes steps. `run --pattern vote`.

## 5. Orchestrator-workers — `orchestrator-workers`

A planner decomposes the task *dynamically* (unknown number of subtasks), workers execute each,
a synthesizer combines. Use when the decomposition depends on the input (e.g. multi-file edits).
Hurts when a fixed chain would do. `run --pattern orchestrator-workers`.

## 6. Evaluator-optimizer — `evaluator-optimizer`

Generate a draft, evaluate it against criteria, feed the critique back, repeat until it passes
or the round budget runs out. Use when there is a clear quality signal and iteration helps
(translation, code that must pass tests). Always bound the rounds. `run --pattern evaluator-optimizer`.

## 7. ReAct loop

The base loop of a tool-using agent: **reason → act (call a tool) → observe the result →
reason again**, until done. Everything above is a more structured specialization of this. Use
the raw loop when the path is genuinely open-ended; bound it with a step budget and stop
conditions. Build it from the `orchestrator` graph primitives (`add_node` / `add_conditional_edges`).

## Composition

Patterns nest: route first, then chain inside one branch; or run an evaluator-optimizer as one
worker of an orchestrator-workers plan. Compose the simplest shapes rather than inventing a new one.

# reference — multi-agent topologies

Each topology, when to choose it, how it fails, and the cheapest thing that often replaces it.

## Supervisor

A single supervisor agent owns the control loop: it inspects state, picks a worker, the
worker does its part and returns, the supervisor decides again. Workers do not talk to each
other.

- **Choose when**: the work decomposes into a few clear subtasks and you want one place that
  holds the plan.
- **Fails when**: the supervisor becomes a bottleneck or its routing prompt grows unbounded.
- **Runnable**: `python -m harness.orchestrator run --pattern supervisor`.

## Hierarchical

Supervisors of supervisors. A top supervisor delegates to mid-level supervisors that each own
a cluster of workers.

- **Choose when**: there are too many workers for one supervisor to route coherently, and they
  group into domains.
- **Fails when**: latency stacks up across layers and errors propagate upward; debugging spans
  many hops.
- Often a flat supervisor with better worker descriptions is enough — add layers last.

## Network

Any agent may call any other agent. Control is decentralized.

- **Choose when**: collaboration is genuinely dynamic and peer-to-peer (no natural hierarchy).
- **Fails when**: agents loop, re-invoke each other, and cost runs away. Hard to reason about
  termination.
- Add explicit step budgets and loop detection if you must use it.

## Swarm

Exactly one agent is active at a time; an agent *hands off* control to another by role
("transfer to the refunds agent"), passing the conversation along.

- **Choose when**: the task moves through distinct roles in sequence and only one role should
  be "holding the pen" at any moment.
- **Fails when**: context is lost or duplicated across handoffs; the receiving agent lacks what
  it needs.
- Make the handoff payload explicit and minimal.

## The honest default

Start with **one agent + tools**. Add a topology only when a concrete limit forces it
(context overflow, true parallelism, hard separation of concerns). Every added agent is added
coordination cost and a new way to fail.

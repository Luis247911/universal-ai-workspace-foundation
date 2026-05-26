"""uaw-harness — runnable reference implementations of agent-engineering patterns.

This is the EXECUTION layer of the universal-ai-workspace-foundation. Each subpackage is a
small, dependency-light, teaching-grade reference for one framework area:

    eval           weighted assertion gate (CI-usable; exits non-zero below threshold)
    guardrails     input/output validators with an on_fail policy
    observability  typed spans with OpenTelemetry gen_ai.* attribute names
    hitl           interrupt -> persist -> resume approval gates
    router         model-group routing + typed fallbacks + cache-breakpoint hints
    memory         scope x type memory with an in/out-of-context boundary
    orchestrator   node/edge graph + the canonical workflow shapes

Patterns are reimplemented from public OSS ideas (see /sources/credits.md and /NOTICE);
no third-party agent library is required. Everything runs offline in mock mode by default.
"""

__version__ = "3.0.0"

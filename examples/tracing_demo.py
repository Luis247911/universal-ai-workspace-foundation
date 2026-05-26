"""Offline observability demo: build a span tree, print it, show content is opt-in.

python examples/tracing_demo.py
"""

from __future__ import annotations

from harness.observability import Tracer, semconv


def main() -> int:
    tracer = Tracer(capture_content=False, session_id="demo")
    with tracer.span("agent", semconv.KIND_AGENT):
        with tracer.llm_call("classify", model="claude-haiku-4-5") as sp:
            sp.set_attribute(semconv.GEN_AI_USAGE_INPUT_TOKENS, 80)
            sp.set_attribute(semconv.GEN_AI_INPUT_MESSAGES, "secret prompt")  # dropped (opt-in off)
        with tracer.span("lookup", semconv.KIND_RETRIEVAL) as sp:
            sp.set_attribute("result_count", 2)

    for s in tracer.spans:
        depth = "  " if s.parent_id else ""
        keys = [k for k in s.attributes if k.startswith("gen_ai")]
        print(f"{depth}{s.kind:11} {s.name:9} gen_ai_attrs={keys}")
    leaked = any(semconv.GEN_AI_INPUT_MESSAGES in s.attributes for s in tracer.spans)
    print(f"content captured: {leaked} (opt-in is off, so message content is dropped)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

"""CLI: python -m harness.observability trace [--capture-content] [--out PATH]

Emits a small example trace as JSONL and prints where it was written.
"""

from __future__ import annotations

import argparse
import sys

from ..core import paths
from . import semconv
from .tracer import Tracer


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="harness.observability")
    sub = parser.add_subparsers(dest="cmd", required=True)
    t = sub.add_parser("trace", help="Emit an example trace as JSONL.")
    t.add_argument(
        "--capture-content", action="store_true", help="Include message content (opt-in)."
    )
    t.add_argument("--out", default=None)
    args = parser.parse_args(argv)

    if args.cmd == "trace":
        tracer = Tracer(capture_content=args.capture_content, session_id="demo-session")
        with tracer.span("agent-run", semconv.KIND_AGENT):
            with tracer.llm_call("plan", model="claude-haiku-4-5") as sp:
                sp.set_attribute(semconv.GEN_AI_USAGE_INPUT_TOKENS, 120)
                sp.set_attribute(semconv.GEN_AI_USAGE_OUTPUT_TOKENS, 35)
                sp.set_attribute(semconv.GEN_AI_INPUT_MESSAGES, "user: do the thing")
            with tracer.span("search", semconv.KIND_RETRIEVAL) as sp:
                sp.set_attribute("result_count", 3)
        out = args.out or str(paths.run_dir("trace-demo") / "trace.jsonl")
        tracer.export_jsonl(out)
        captured = "with" if args.capture_content else "without"
        print(f"wrote {len(tracer.spans)} spans ({captured} content) -> {out}")
        return 0
    return 2


if __name__ == "__main__":
    sys.exit(main())

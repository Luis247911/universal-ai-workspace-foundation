"""CLI: python -m harness.eval run      --suite <path> [--threshold F] [--quiet]
       python -m harness.eval scaffold --out <path> [--force]
       python -m harness.eval judge    --rubric "..." (--output "..." | --output-file P)

`run` exits non-zero when the suite score is below the threshold (CI gate). `scaffold`
writes a minimal runnable starter suite. `judge` grades one output against a rubric
(deterministic keyword grade offline; a real model when UAW_LLM=live), exiting non-zero
on FAIL.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from ..core import llm
from .assertions import run_assertion
from .runner import run_suite

_STARTER_SUITE = """\
{
  "suite": "my-eval",
  "threshold": 0.8,
  "cases": [
    {
      "id": "greeting-contains-hello",
      "input": { "kind": "inline", "output": "hello world" },
      "assertions": [{ "type": "contains", "value": "hello" }]
    },
    {
      "id": "output-is-nonempty",
      "input": { "kind": "inline", "output": "hello world" },
      "assertions": [{ "type": "regex", "pattern": "\\\\S" }]
    }
  ]
}
"""


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="harness.eval", description="Run a weighted eval suite and gate on a threshold."
    )
    sub = parser.add_subparsers(dest="cmd", required=True)
    run_p = sub.add_parser("run", help="Run a suite.")
    run_p.add_argument("--suite", required=True)
    run_p.add_argument("--threshold", type=float, default=None)
    run_p.add_argument("--quiet", action="store_true")
    sc = sub.add_parser("scaffold", help="Write a minimal runnable starter suite.")
    sc.add_argument("--out", required=True)
    sc.add_argument("--force", action="store_true")
    jp = sub.add_parser("judge", help="Grade one output against a rubric (LLM-as-judge).")
    jp.add_argument("--rubric", required=True)
    jp.add_argument("--output", default=None)
    jp.add_argument("--output-file", default=None)
    args = parser.parse_args(argv)

    if args.cmd == "run":
        result = run_suite(args.suite, args.threshold)
        if not args.quiet:
            for c in result.cases:
                mark = "ok " if c.score >= result.threshold else "LOW"
                print(f"[{mark}] {c.id}: {c.score:.2f}")
            verdict = "PASS" if result.passed else "FAIL"
            print(
                f"\nSuite score {result.score:.3f} (threshold {result.threshold:.2f}) -> {verdict}"
            )
        return result.exit_code

    if args.cmd == "scaffold":
        out = Path(args.out)
        if out.exists() and not args.force:
            print(f"refusing to overwrite {out} (use --force)")
            return 1
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(_STARTER_SUITE, encoding="utf-8")
        print(f"wrote starter suite -> {out}")
        print(f"run it: python -m harness.eval run --suite {out}")
        return 0

    if args.cmd == "judge":
        if args.output is None and args.output_file is None:
            print("judge needs --output or --output-file")
            return 2
        output = (
            args.output
            if args.output is not None
            else Path(args.output_file).read_text(encoding="utf-8")
        )
        # skip_if_mock=False so the judge always grades: keyword heuristic offline, model live.
        spec = {"type": "llm_rubric", "rubric": args.rubric, "skip_if_mock": False}
        oc = run_assertion(spec, output)
        print(
            json.dumps(
                {
                    "verdict": "PASS" if oc.passed else "FAIL",
                    "score": oc.score,
                    "detail": oc.detail,
                    "mock": llm.is_mock(),
                }
            )
        )
        return 0 if oc.passed else 1

    return 2


if __name__ == "__main__":
    sys.exit(main())

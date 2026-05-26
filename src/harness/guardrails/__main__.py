"""CLI: python -m harness.guardrails check --text "..." [--boundary output]

Demonstrates an output guard that filters emails and caps length.
"""

from __future__ import annotations

import argparse
import sys

from .guard import Guard
from .policies import OnFail
from .validator import MaxLength, NoEmail


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="harness.guardrails")
    sub = parser.add_subparsers(dest="cmd", required=True)
    c = sub.add_parser("check", help="Run a demo guard over some text.")
    c.add_argument("--text", default="contact me at a@b.com please")
    c.add_argument("--boundary", default="output", choices=["input", "output"])
    args = parser.parse_args(argv)

    if args.cmd == "check":
        guard = Guard(NoEmail(OnFail.FILTER), MaxLength(200, OnFail.FIX), boundary=args.boundary)
        result = guard.apply(args.text)
        print(f"passed={result.passed} action={result.action} reask={result.reask}")
        print(f"text: {result.text}")
        return 0
    return 2


if __name__ == "__main__":
    sys.exit(main())

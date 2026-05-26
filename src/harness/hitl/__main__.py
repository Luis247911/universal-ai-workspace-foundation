"""CLI: python -m harness.hitl request --payload "send email to X"
       python -m harness.hitl approve --run <id> [--feedback "..."]
       python -m harness.hitl deny    --run <id> [--feedback "..."]
       python -m harness.hitl resume  --run <id>

Run the verbs as separate processes to see that the pause survives process exit.
"""

from __future__ import annotations

import argparse
import sys

from ..core.errors import InterruptPending
from . import interrupt


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="harness.hitl")
    sub = parser.add_subparsers(dest="cmd", required=True)

    r = sub.add_parser("request")
    r.add_argument("--payload", required=True)
    r.add_argument("--run", default=None)
    for verb in ("approve", "deny"):
        d = sub.add_parser(verb)
        d.add_argument("--run", required=True)
        d.add_argument("--feedback", default=None)
    rs = sub.add_parser("resume")
    rs.add_argument("--run", required=True)

    args = parser.parse_args(argv)

    if args.cmd == "request":
        rec = interrupt.request({"action": args.payload}, run_id=args.run)
        print(f"run_id={rec['run_id']} status={rec['status']} (awaiting decision)")
        return 0
    if args.cmd == "approve":
        rec = interrupt.approve(args.run, args.feedback)
        print(f"run_id={rec['run_id']} status={rec['status']}")
        return 0
    if args.cmd == "deny":
        rec = interrupt.deny(args.run, args.feedback)
        print(f"run_id={rec['run_id']} status={rec['status']} feedback={rec['feedback']!r}")
        return 0
    if args.cmd == "resume":
        try:
            rec = interrupt.resume(args.run)
        except InterruptPending as e:
            print(f"PENDING: {e}")
            return 3
        verdict = (
            "proceed" if interrupt.is_approved(rec) else f"loop-with-feedback: {rec['feedback']!r}"
        )
        print(f"run_id={rec['run_id']} status={rec['status']} -> {verdict}")
        return 0
    return 2


if __name__ == "__main__":
    sys.exit(main())

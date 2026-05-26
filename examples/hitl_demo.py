"""Offline HITL demo: request -> deny-with-feedback -> the feedback re-enters the loop.

    python examples/hitl_demo.py

Uses a temporary runs dir so the demo leaves nothing behind.
"""

from __future__ import annotations

import os
import tempfile


def main() -> int:
    with tempfile.TemporaryDirectory() as d:
        os.environ["UAW_RUNS_DIR"] = d
        from harness import hitl

        rec = hitl.request({"action": "delete production table"}, run_id="demo")
        print(f"requested: status={rec['status']} (paused, state persisted to disk)")

        # a human reviews and rejects with guidance
        hitl.deny("demo", feedback="never delete prod; soft-delete instead")
        decision = hitl.resume("demo")
        if hitl.is_approved(decision):
            print("approved -> proceed")
        else:
            print(f"denied -> loop with feedback: {decision['feedback']!r}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

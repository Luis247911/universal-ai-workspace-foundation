"""Offline demo of the eval gate. Runs with a bare `pip install -e .` (no extras, no key).

python examples/eval_demo.py
"""

from __future__ import annotations

import tempfile
from pathlib import Path

from harness.core import jsonio
from harness.eval.runner import run_suite


def main() -> int:
    suite = {
        "suite": "eval-demo",
        "threshold": 0.8,
        "cases": [
            {
                "id": "greeting-contains-hello",
                "input": {"kind": "inline", "output": "hello, world"},
                "assertions": [{"type": "contains", "value": "hello"}],
            },
            {
                "id": "answer-is-numeric",
                "input": {"kind": "inline", "output": "the answer is 42"},
                "assertions": [{"type": "regex", "pattern": r"\d+", "weight": 2}],
            },
            {
                "id": "structured-output",
                "input": {"kind": "inline", "output": '{"ok": true, "n": 3}'},
                "assertions": [
                    {
                        "type": "json_schema",
                        "schema": {"type": "object", "required": ["ok", "n"]},
                    }
                ],
            },
        ],
    }
    with tempfile.TemporaryDirectory() as d:
        p = Path(d) / "demo.suite.json"
        jsonio.write_json(p, suite)
        result = run_suite(p)

    for c in result.cases:
        print(f"  {c.id}: {c.score:.2f}")
    print(
        f"score={result.score:.3f} threshold={result.threshold:.2f} "
        f"-> {'PASS' if result.passed else 'FAIL'} (exit {result.exit_code})"
    )
    return result.exit_code


if __name__ == "__main__":
    raise SystemExit(main())

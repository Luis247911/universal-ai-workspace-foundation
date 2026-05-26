"""Offline guardrail demo: an output guard that filters emails and caps length.

python examples/guardrail_demo.py
"""

from __future__ import annotations

from harness.guardrails import Guard, MaxLength, NoEmail, OnFail


def main() -> int:
    guard = Guard(NoEmail(OnFail.FILTER), MaxLength(60, OnFail.FIX), boundary="output")
    for text in ["reach me at jane@example.com tomorrow", "x" * 90, "a clean response"]:
        res = guard.apply(text)
        print(f"passed={res.passed} action={res.action!s:6} -> {res.text!r}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

"""Load a golden suite, run assertions per case, aggregate a weighted score, gate on a threshold.

An eval = dataset(cases) + typed assertions/rubric + runner + threshold gate. `run_suite`
returns a RunResult whose .exit_code is 0 when score >= threshold else 1 — that non-zero
exit is the load-bearing property that makes this usable as a CI gate.

Input kinds per case:
    inline  output is given directly in the suite
    file    output is the UTF-8 content of a file (relative to the suite's base)
    cmd     output is the stdout of a subprocess (list args, shell=False)
"""

from __future__ import annotations

import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path

from ..core.config import load_config
from ..core.errors import ConfigError
from ..core.types import Outcome
from .assertions import run_assertion


@dataclass
class CaseResult:
    id: str
    score: float
    outcomes: list[Outcome]


@dataclass
class RunResult:
    suite: str
    score: float
    threshold: float
    cases: list[CaseResult] = field(default_factory=list)

    @property
    def passed(self) -> bool:
        return self.score >= self.threshold

    @property
    def exit_code(self) -> int:
        return 0 if self.passed else 1


def _resolve_output(inp: dict, base: Path) -> str:
    kind = inp.get("kind", "inline")
    if kind == "inline":
        return str(inp.get("output", ""))
    if kind == "file":
        return (base / inp["path"]).read_text(encoding="utf-8")
    if kind == "cmd":
        args = inp.get("run")
        if not isinstance(args, list):
            raise ConfigError("cmd input 'run' must be a list of args (no shell).")
        # Map the literal token "python" to the interpreter running the eval, so cmd cases
        # are portable (on Windows a bare "python" may resolve to a different interpreter
        # that lacks the package). The repo convention is always `python -m harness.<area>`.
        if args and args[0] == "python":
            args = [sys.executable, *args[1:]]
        proc = subprocess.run(args, capture_output=True, text=True, shell=False, cwd=str(base))
        return proc.stdout
    raise ConfigError(f"Unknown input kind: {kind!r}")


def _aggregate(outcomes: list[Outcome]) -> float:
    scored = [o for o in outcomes if not o.skipped]
    total_w = sum(o.weight for o in scored)
    if total_w == 0:
        return 1.0  # nothing to score (e.g. all skipped) is not a failure
    return sum(o.score * o.weight for o in scored) / total_w


def run_suite(suite_path, threshold: float | None = None) -> RunResult:
    suite = load_config(suite_path)
    if not isinstance(suite, dict) or "cases" not in suite:
        raise ConfigError("Suite must be a mapping with a 'cases' list.")
    thr = threshold if threshold is not None else float(suite.get("threshold", 0.8))
    # file/cmd paths resolve relative to the suite's 'base' (default: current working dir,
    # i.e. the repo root when run from CI).
    base = Path(suite["base"]) if suite.get("base") else Path.cwd()
    cases: list[CaseResult] = []
    for case in suite["cases"]:
        inp = case.get("input", {"kind": "inline", "output": ""})
        output = _resolve_output(inp, base)
        outcomes = [run_assertion(a, output) for a in case.get("assertions", [])]
        cases.append(
            CaseResult(id=case.get("id", "?"), score=_aggregate(outcomes), outcomes=outcomes)
        )
    overall = sum(c.score for c in cases) / len(cases) if cases else 1.0
    return RunResult(suite=str(suite_path), score=overall, threshold=thr, cases=cases)

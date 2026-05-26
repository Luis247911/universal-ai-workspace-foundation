"""Typed assertions. Each returns an Outcome(score in [0, 1], weight, skipped).

Types: exact, contains, regex, json_schema, llm_rubric. Deterministic checks (the first
four) never need a model; llm_rubric is skipped by default in mock mode so suites stay
green offline and grade stricter when run live.

Idea attribution: the typed-assertion-list-with-weights shape is reimplemented from
promptfoo / DeepEval (MIT/Apache); no code copied. See /sources/credits.md.
"""

from __future__ import annotations

import json
import re

from ..core import llm
from ..core.errors import ConfigError
from ..core.types import Outcome

_JSON_TYPES = {
    "object": dict,
    "array": list,
    "string": str,
    "number": (int, float),
    "integer": int,
    "boolean": bool,
    "null": type(None),
}


def _exact(output: str, spec: dict) -> Outcome:
    want = str(spec.get("value", ""))
    ok = output.strip() == want.strip()
    return Outcome(passed=ok, score=1.0 if ok else 0.0, detail="" if ok else f"expected {want!r}")


def _contains(output: str, spec: dict) -> Outcome:
    needle = str(spec.get("value", ""))
    ok = needle in output
    return Outcome(passed=ok, score=1.0 if ok else 0.0, detail="" if ok else f"missing {needle!r}")


def _regex(output: str, spec: dict) -> Outcome:
    pattern = spec.get("pattern")
    if pattern is None:
        raise ConfigError("regex assertion requires 'pattern'")
    flags = re.MULTILINE if spec.get("multiline") else 0
    ok = re.search(pattern, output, flags) is not None
    return Outcome(passed=ok, score=1.0 if ok else 0.0, detail="" if ok else f"no match: {pattern}")


def _json_schema(output: str, spec: dict) -> Outcome:
    schema = spec.get("schema") or {}
    try:
        obj = json.loads(output)
    except (json.JSONDecodeError, TypeError) as e:
        return Outcome(passed=False, score=0.0, detail=f"output is not JSON: {e}")
    errs = _validate(obj, schema, "$")
    ok = not errs
    return Outcome(passed=ok, score=1.0 if ok else 0.0, detail="; ".join(errs))


def _validate(obj, schema: dict, path: str) -> list[str]:
    """Minimal JSON-schema check (type / required / properties / items). No external dep."""
    errs: list[str] = []
    t = schema.get("type")
    if t and not isinstance(obj, _JSON_TYPES[t]):
        return [f"{path}: expected {t}"]
    if t == "object":
        for key in schema.get("required", []):
            if key not in obj:
                errs.append(f"{path}.{key}: required")
        for key, sub in (schema.get("properties") or {}).items():
            if key in obj:
                errs += _validate(obj[key], sub, f"{path}.{key}")
    if t == "array" and "items" in schema:
        for i, item in enumerate(obj):
            errs += _validate(item, schema["items"], f"{path}[{i}]")
    return errs


def _llm_rubric(output: str, spec: dict) -> Outcome:
    if llm.is_mock() and spec.get("skip_if_mock", True):
        return Outcome.skip("llm_rubric skipped (mock mode)")
    rubric = str(spec.get("rubric", ""))
    if llm.is_mock():
        # deterministic offline grade: pass if a salient rubric keyword appears in output
        kws = [w for w in re.findall(r"\w+", rubric.lower()) if len(w) > 4]
        hit = any(k in output.lower() for k in kws)
        return Outcome(passed=hit, score=1.0 if hit else 0.0, detail="[mock rubric]")
    verdict = llm.complete(
        [
            {
                "role": "user",
                "content": f"Rubric: {rubric}\n\nOutput:\n{output}\n\nAnswer PASS or FAIL only.",
            }
        ],
        system="You are a strict evaluator. Reason internally, then answer exactly PASS or FAIL.",
    )
    ok = "PASS" in verdict.upper()
    return Outcome(passed=ok, score=1.0 if ok else 0.0, detail=verdict[:80])


ASSERTION_TYPES = {
    "exact": _exact,
    "contains": _contains,
    "regex": _regex,
    "json_schema": _json_schema,
    "llm_rubric": _llm_rubric,
}


def run_assertion(spec: dict, output: str) -> Outcome:
    atype = spec.get("type")
    if atype not in ASSERTION_TYPES:
        raise ConfigError(f"Unknown assertion type {atype!r}. Known: {sorted(ASSERTION_TYPES)}")
    out = ASSERTION_TYPES[atype](output, spec)
    if not out.skipped and "weight" in spec:
        out.weight = float(spec["weight"])
    return out

import json

from harness.core import jsonio
from harness.eval.assertions import run_assertion
from harness.eval.runner import run_suite


def test_exact_contains_regex():
    assert run_assertion({"type": "exact", "value": "hi"}, " hi ").passed
    assert not run_assertion({"type": "exact", "value": "hi"}, "bye").passed
    assert run_assertion({"type": "contains", "value": "ell"}, "hello").passed
    assert run_assertion({"type": "regex", "pattern": r"\d+"}, "abc123").passed


def test_json_schema_required_and_types():
    spec = {
        "type": "json_schema",
        "schema": {
            "type": "object",
            "required": ["name", "n"],
            "properties": {"n": {"type": "integer"}},
        },
    }
    assert run_assertion(spec, json.dumps({"name": "x", "n": 5})).passed
    assert not run_assertion(spec, json.dumps({"name": "x"})).passed  # missing 'n'
    assert not run_assertion(spec, json.dumps({"name": "x", "n": "five"})).passed  # wrong type
    assert not run_assertion(spec, "not json at all").passed


def test_llm_rubric_skipped_in_mock():
    o = run_assertion({"type": "llm_rubric", "rubric": "is polite", "skip_if_mock": True}, "x")
    assert o.skipped and o.weight == 0.0


def test_weight_is_applied():
    o = run_assertion({"type": "contains", "value": "x", "weight": 3}, "x")
    assert o.weight == 3.0


def test_suite_gate_passes_and_fails(tmp_path):
    suite = {
        "suite": "demo",
        "threshold": 0.8,
        "cases": [
            {
                "id": "c1",
                "input": {"kind": "inline", "output": "hello world"},
                "assertions": [{"type": "contains", "value": "hello"}],
            },
            {
                "id": "c2",
                "input": {"kind": "inline", "output": "answer is 42"},
                "assertions": [{"type": "regex", "pattern": r"\d+"}],
            },
        ],
    }
    p = tmp_path / "suite.json"
    jsonio.write_json(p, suite)

    res = run_suite(p)
    assert res.passed and res.exit_code == 0 and res.score == 1.0

    # the gate must actually gate: an impossible threshold fails with a non-zero exit
    res2 = run_suite(p, threshold=1.01)
    assert not res2.passed and res2.exit_code == 1


def test_skipped_assertions_do_not_sink_score(tmp_path):
    suite = {
        "threshold": 0.8,
        "cases": [
            {
                "id": "mix",
                "input": {"kind": "inline", "output": "polite hello"},
                "assertions": [
                    {"type": "contains", "value": "hello"},
                    {"type": "llm_rubric", "rubric": "tone is friendly", "skip_if_mock": True},
                ],
            }
        ],
    }
    p = tmp_path / "s.json"
    jsonio.write_json(p, suite)
    res = run_suite(p)
    assert res.score == 1.0  # skipped rubric excluded from aggregation

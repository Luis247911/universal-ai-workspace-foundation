from harness.core import jsonio
from harness.core.state import State
from harness.core.types import Message, Outcome


def test_state_set_get_history():
    s = State()
    s.set("a", 1).set("b", 2)
    assert s.get("a") == 1
    assert s.get("missing", "default") == "default"
    assert ("a", 1) in s.history and ("b", 2) in s.history


def test_state_update_and_route():
    s = State().update({"x": 10, "y": 20}).goto("worker")
    assert s.get("x") == 10 and s.get("y") == 20
    assert s.route == "worker"


def test_message_to_dict():
    assert Message("user", "hi").to_dict() == {"role": "user", "content": "hi"}


def test_outcome_skip_has_zero_weight():
    o = Outcome.skip("nope")
    assert o.skipped and o.weight == 0.0 and o.passed


def test_jsonl_roundtrip(tmp_path):
    p = tmp_path / "t.jsonl"
    jsonio.write_jsonl(p, [{"a": 1}, {"b": 2}])
    jsonio.append_jsonl(p, {"c": 3})
    assert list(jsonio.read_jsonl(p)) == [{"a": 1}, {"b": 2}, {"c": 3}]


def test_json_atomic_non_ascii(tmp_path):
    p = tmp_path / "x.json"
    jsonio.write_json(p, {"k": "ä-ü-ß"})
    assert jsonio.read_json(p) == {"k": "ä-ü-ß"}

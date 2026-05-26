import pytest

from harness.core.errors import ValidationError
from harness.guardrails.guard import Guard
from harness.guardrails.policies import REFUSAL_TEXT, OnFail
from harness.guardrails.validator import IsJSON, MaxLength, NoEmail


def test_filter_redacts_email():
    g = Guard(NoEmail(OnFail.FILTER), boundary="output")
    res = g.apply("reach me at a@b.com now")
    assert not res.passed and res.action == "filter"
    assert "a@b.com" not in res.text and "[redacted]" in res.text


def test_fix_truncates():
    g = Guard(MaxLength(5, OnFail.FIX))
    res = g.apply("0123456789")
    assert res.text == "01234" and res.action == "fix"


def test_raise_stops_hard():
    g = Guard(NoEmail(OnFail.RAISE))
    with pytest.raises(ValidationError):
        g.apply("x@y.com")


def test_refrain_replaces_output():
    g = Guard(NoEmail(OnFail.REFRAIN))
    res = g.apply("x@y.com")
    assert res.text == REFUSAL_TEXT and not res.passed


def test_reask_flagged():
    g = Guard(IsJSON(OnFail.REASK))
    res = g.apply("not json")
    assert res.reask and res.action == "reask"


def test_clean_input_passes():
    g = Guard(NoEmail(OnFail.FILTER), MaxLength(100, OnFail.FIX))
    res = g.apply("a perfectly fine sentence")
    assert res.passed and res.action is None

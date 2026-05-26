"""HITL persistence tests. UAW_RUNS_DIR is redirected to a tmp dir so runs are isolated."""

import pytest

from harness.core.errors import InterruptPending


@pytest.fixture
def isolated_runs(tmp_path, monkeypatch):
    monkeypatch.setenv("UAW_RUNS_DIR", str(tmp_path / "runs"))
    # re-import not needed: paths.runs_root() reads the env var at call time
    return tmp_path


def test_request_approve_resume(isolated_runs):
    from harness import hitl

    rec = hitl.request({"action": "send email"}, run_id="r1")
    assert rec["status"] == "pending"
    hitl.approve("r1", feedback="looks good")
    resumed = hitl.resume("r1")
    assert resumed["status"] == "approved" and hitl.is_approved(resumed)


def test_deny_returns_feedback_into_loop(isolated_runs):
    from harness import hitl

    hitl.request({"action": "delete db"}, run_id="r2")
    hitl.deny("r2", feedback="too risky, scope it down")
    resumed = hitl.resume("r2")
    assert resumed["status"] == "denied"
    assert not hitl.is_approved(resumed)
    assert resumed["feedback"] == "too risky, scope it down"


def test_resume_while_pending_raises(isolated_runs):
    from harness import hitl

    hitl.request({"action": "x"}, run_id="r3")
    with pytest.raises(InterruptPending):
        hitl.resume("r3")


def test_pause_survives_fresh_store_read(isolated_runs):
    # simulate a separate process: request, then read the record straight from disk via store
    from harness import hitl
    from harness.hitl import store

    hitl.request({"action": "y"}, run_id="r4")
    reloaded = store.load("r4")
    assert reloaded is not None and reloaded["status"] == "pending"

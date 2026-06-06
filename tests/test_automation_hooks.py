"""Tests for the opt-in automation hooks under ``.claude/hooks/``.

Each hook must be fail-safe inert (no stdout, exit 0) when its flag is off or its preconditions are
not met, and emit **exactly one** valid ``hookSpecificOutput`` JSON object when it should fire.
These mirror the manual self-tests in ``.claude/AUTOMATION.md``, gated in CI so a stray ``print()``
or a flipped default cannot regress silently.

Hooks are invoked the way Claude Code invokes them: as a subprocess with stdin ``{}`` and
``CLAUDE_PROJECT_DIR`` pointing at a throwaway sandbox, so no test ever touches the real repo state.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
from datetime import date
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
HOOKS = REPO_ROOT / ".claude" / "hooks"
ALL_HOOKS = ["boot_reload.py", "recitation_nudge.py", "first_run_onboarding.py", "daily_maintenance.py"]


def _run(hook_name: str, project_dir: Path, extra_env: dict[str, str] | None = None):
    """Run a hook as Claude Code would. Return (stdout, returncode)."""
    env = {k: v for k, v in os.environ.items() if k != "UAW_DISABLE_ONBOARDING"}
    env["CLAUDE_PROJECT_DIR"] = str(project_dir)
    if extra_env:
        env.update(extra_env)
    proc = subprocess.run(
        [sys.executable, str(HOOKS / hook_name)],
        input="{}",
        capture_output=True,
        text=True,
        env=env,
    )
    return proc.stdout, proc.returncode


def _sandbox(tmp_path: Path, flags: dict, *, placeholders: bool = True, marker: str | None = None) -> Path:
    """Build a throwaway workspace with the given flags / state for a hook to read."""
    claude = tmp_path / ".claude"
    claude.mkdir(parents=True, exist_ok=True)
    (claude / "automation.flags.json").write_text(json.dumps(flags), encoding="utf-8")
    state = tmp_path / ".ai-workspace" / "state"
    state.mkdir(parents=True, exist_ok=True)
    title = "<projekt-slug>" if placeholders else "my-real-project"
    (state / "project-index.md").write_text(f"title: {title}\n", encoding="utf-8")
    (state / "current-session.md").write_text("active task: real\n", encoding="utf-8")
    if marker is not None:
        (claude / ".onboarding-state.json").write_text(marker, encoding="utf-8")
    return tmp_path


def _assert_single_json(stdout: str) -> dict:
    """The whole stdout must parse as exactly one JSON object with a hookSpecificOutput block."""
    payload = json.loads(stdout)  # raises if empty or multiple objects -> catches double-print
    assert "hookSpecificOutput" in payload
    assert payload["hookSpecificOutput"]["additionalContext"].strip()
    return payload


# --- off-path: every hook is silent + exit 0 when all flags are off --------------------------------

@pytest.mark.parametrize("hook", ALL_HOOKS)
def test_all_hooks_inert_when_flags_off(tmp_path, hook):
    ws = _sandbox(tmp_path, flags={})  # empty flags -> every flag resolves False
    stdout, code = _run(hook, ws)
    assert code == 0
    assert stdout == ""


# --- first_run_onboarding --------------------------------------------------------------------------

def test_onboarding_fires_on_fresh_workspace(tmp_path):
    ws = _sandbox(tmp_path, flags={"first_run_onboarding": True}, placeholders=True)
    stdout, code = _run("first_run_onboarding.py", ws)
    assert code == 0
    _assert_single_json(stdout)


def test_onboarding_inert_when_marker_present(tmp_path):
    ws = _sandbox(tmp_path, flags={"first_run_onboarding": True}, marker='{"status": "done"}')
    stdout, code = _run("first_run_onboarding.py", ws)
    assert code == 0
    assert stdout == ""


def test_onboarding_inert_on_corrupt_marker(tmp_path):
    # A half-written marker still means /start ran -> stay silent (do not re-nag).
    ws = _sandbox(tmp_path, flags={"first_run_onboarding": True}, marker="{not valid json")
    stdout, code = _run("first_run_onboarding.py", ws)
    assert code == 0
    assert stdout == ""


def test_onboarding_inert_when_placeholders_filled(tmp_path):
    ws = _sandbox(tmp_path, flags={"first_run_onboarding": True}, placeholders=False)
    stdout, code = _run("first_run_onboarding.py", ws)
    assert code == 0
    assert stdout == ""


def test_onboarding_inert_with_env_optout(tmp_path):
    ws = _sandbox(tmp_path, flags={"first_run_onboarding": True}, placeholders=True)
    stdout, code = _run("first_run_onboarding.py", ws, extra_env={"UAW_DISABLE_ONBOARDING": "1"})
    assert code == 0
    assert stdout == ""


# --- daily_maintenance -----------------------------------------------------------------------------

def test_daily_maintenance_fires_and_writes_marker(tmp_path):
    ws = _sandbox(tmp_path, flags={"daily_maintenance": True})
    stdout, code = _run("daily_maintenance.py", ws)
    assert code == 0
    _assert_single_json(stdout)
    last = (ws / ".claude" / ".daily_maintenance_last").read_text(encoding="utf-8").strip()
    assert last == date.today().isoformat()


def test_daily_maintenance_inert_same_day(tmp_path):
    ws = _sandbox(tmp_path, flags={"daily_maintenance": True})
    (ws / ".claude" / ".daily_maintenance_last").write_text(date.today().isoformat(), encoding="utf-8")
    stdout, code = _run("daily_maintenance.py", ws)
    assert code == 0
    assert stdout == ""

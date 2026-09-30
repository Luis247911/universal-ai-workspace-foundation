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
import time
from datetime import date, datetime
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
HOOKS = REPO_ROOT / ".claude" / "hooks"
ALL_HOOKS = [
    "boot_reload.py",
    "recitation_nudge.py",
    "first_run_onboarding.py",
    "daily_maintenance.py",
    "prompt_optimizer.py",
    "external_content_guard.py",
    "compact_nudge.py",
    "session_state_guard.py",
    "now_init.py",
    "journal_stub.py",
    "memory_boot.py",
    "precompact_reminder.py",
    "index_refresh.py",
]


def _run(
    hook_name: str, project_dir: Path, extra_env: dict[str, str] | None = None, stdin: str = "{}"
):
    """Run a hook as Claude Code would. Return (stdout, returncode)."""
    env = {k: v for k, v in os.environ.items() if k != "UAW_DISABLE_ONBOARDING"}
    env["CLAUDE_PROJECT_DIR"] = str(project_dir)
    # The sandbox has no src/: point the hooks at this checkout's engine, not an installed one.
    env["PYTHONPATH"] = str(REPO_ROOT / "src")
    if extra_env:
        env.update(extra_env)
    proc = subprocess.run(
        [sys.executable, str(HOOKS / hook_name)],
        input=stdin,
        capture_output=True,
        text=True,
        env=env,
    )
    return proc.stdout, proc.returncode


def _sandbox(
    tmp_path: Path, flags: dict, *, placeholders: bool = True, marker: str | None = None
) -> Path:
    """Build a throwaway workspace with the given flags / state for a hook to read."""
    claude = tmp_path / ".claude"
    claude.mkdir(parents=True, exist_ok=True)
    (claude / "automation.flags.json").write_text(json.dumps(flags), encoding="utf-8")
    state = tmp_path / ".ai-workspace" / "state"
    state.mkdir(parents=True, exist_ok=True)
    title = "<projekt-slug>" if placeholders else "my-real-project"
    (state / "project-index.md").write_text(f"title: {title}\n", encoding="utf-8")
    (state / "now.md").write_text("active task: real\n", encoding="utf-8")
    if marker is not None:
        (claude / ".onboarding-state.json").write_text(marker, encoding="utf-8")
    return tmp_path


def _assert_single_json(stdout: str) -> dict:
    """The whole stdout must parse as exactly one JSON object with a hookSpecificOutput block."""
    payload = json.loads(stdout)  # raises if empty or multiple objects -> catches double-print
    assert "hookSpecificOutput" in payload
    assert payload["hookSpecificOutput"]["additionalContext"].strip()
    return payload


# --- off-path: every hook is silent + exit 0 when all flags are off ---

@pytest.mark.parametrize("hook", ALL_HOOKS)
def test_all_hooks_inert_when_flags_off(tmp_path, hook):
    ws = _sandbox(tmp_path, flags={})  # empty flags -> every flag resolves False
    stdout, code = _run(hook, ws)
    assert code == 0
    assert stdout == ""


# --- first_run_onboarding ---

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


# --- daily_maintenance ---

def test_daily_maintenance_fires_and_writes_marker(tmp_path):
    ws = _sandbox(tmp_path, flags={"daily_maintenance": True})
    stdout, code = _run("daily_maintenance.py", ws)
    assert code == 0
    _assert_single_json(stdout)
    last = (ws / ".claude" / ".daily_maintenance_last").read_text(encoding="utf-8").strip()
    assert last == date.today().isoformat()


def test_daily_maintenance_inert_same_day(tmp_path):
    ws = _sandbox(tmp_path, flags={"daily_maintenance": True})
    marker = ws / ".claude" / ".daily_maintenance_last"
    marker.write_text(date.today().isoformat(), encoding="utf-8")
    stdout, code = _run("daily_maintenance.py", ws)
    assert code == 0
    assert stdout == ""


# --- prompt_optimizer (opt-in, UserPromptSubmit) ---

def test_prompt_optimizer_fires_on_vague_prompt(tmp_path):
    ws = _sandbox(tmp_path, flags={"prompt_optimizer": True})
    stdout, code = _run(
        "prompt_optimizer.py", ws, stdin=json.dumps({"prompt": "fix it so it does the thing"})
    )
    assert code == 0
    _assert_single_json(stdout)


def test_prompt_optimizer_inert_on_clear_prompt(tmp_path):
    ws = _sandbox(tmp_path, flags={"prompt_optimizer": True})
    stdout, code = _run(
        "prompt_optimizer.py",
        ws,
        stdin=json.dumps({"prompt": "Refactor the login handler in src/auth.py to use bcrypt"}),
    )
    assert code == 0
    assert stdout == ""


def test_prompt_optimizer_inert_on_slash_command(tmp_path):
    ws = _sandbox(tmp_path, flags={"prompt_optimizer": True})
    stdout, code = _run("prompt_optimizer.py", ws, stdin=json.dumps({"prompt": "/uaw-automation"}))
    assert code == 0
    assert stdout == ""


def test_prompt_optimizer_inert_when_flag_off(tmp_path):
    ws = _sandbox(tmp_path, flags={})
    stdout, code = _run(
        "prompt_optimizer.py", ws, stdin=json.dumps({"prompt": "fix it so it does the thing"})
    )
    assert code == 0
    assert stdout == ""


# --- external_content_guard (opt-in, PostToolUse WebFetch|WebSearch) ---

def test_external_guard_fires_on_webfetch(tmp_path):
    ws = _sandbox(tmp_path, flags={"external_content_guard": True})
    stdin = json.dumps({"tool_name": "WebFetch", "tool_input": {"url": "https://example.com/x"}})
    stdout, code = _run("external_content_guard.py", ws, stdin=stdin)
    assert code == 0
    _assert_single_json(stdout)


def test_external_guard_inert_on_other_tool(tmp_path):
    ws = _sandbox(tmp_path, flags={"external_content_guard": True})
    stdin = json.dumps({"tool_name": "Read", "tool_input": {"file_path": "a.md"}})
    stdout, code = _run("external_content_guard.py", ws, stdin=stdin)
    assert code == 0
    assert stdout == ""


def test_external_guard_warns_on_denylist_hit(tmp_path):
    ws = _sandbox(tmp_path, flags={"external_content_guard": True})
    (ws / ".claude" / "external-content-denylist.txt").write_text(
        "# project deny terms\nsecret-internal-host\n", encoding="utf-8"
    )
    stdin = json.dumps(
        {"tool_name": "WebFetch", "tool_input": {"url": "https://api.x/?h=secret-internal-host"}}
    )
    stdout, code = _run("external_content_guard.py", ws, stdin=stdin)
    assert code == 0
    payload = _assert_single_json(stdout)
    assert "deny-list" in payload["hookSpecificOutput"]["additionalContext"]


# --- compact_nudge (opt-in, PostToolUse; threshold via env for a fast test) ---

def test_compact_nudge_inert_below_threshold(tmp_path):
    ws = _sandbox(tmp_path, flags={"compact_nudge": True})
    stdout, code = _run("compact_nudge.py", ws, extra_env={"UAW_COMPACT_NUDGE_THRESHOLD": "3"})
    assert code == 0
    assert stdout == ""
    assert (ws / ".claude" / ".compact_nudge_state").read_text(encoding="utf-8").strip() == "1"


def test_compact_nudge_fires_at_threshold(tmp_path):
    ws = _sandbox(tmp_path, flags={"compact_nudge": True})
    env = {"UAW_COMPACT_NUDGE_THRESHOLD": "3"}
    _run("compact_nudge.py", ws, extra_env=env)
    _run("compact_nudge.py", ws, extra_env=env)
    stdout, code = _run("compact_nudge.py", ws, extra_env=env)
    assert code == 0
    _assert_single_json(stdout)


def test_compact_nudge_inert_one_past_threshold(tmp_path):
    ws = _sandbox(tmp_path, flags={"compact_nudge": True})
    env = {"UAW_COMPACT_NUDGE_THRESHOLD": "3"}
    for _ in range(3):
        _run("compact_nudge.py", ws, extra_env=env)
    stdout, code = _run("compact_nudge.py", ws, extra_env=env)
    assert code == 0
    assert stdout == ""


# --- session_state_guard (opt-in, PostToolUse; staleness-gated + throttled) ---

def test_state_guard_inert_when_fresh(tmp_path):
    ws = _sandbox(tmp_path, flags={"session_state_guard": True})
    # _sandbox just wrote now.md -> mtime ~ now -> fresh -> silent.
    stdout, code = _run("session_state_guard.py", ws)
    assert code == 0
    assert stdout == ""


def test_state_guard_fires_when_stale(tmp_path):
    ws = _sandbox(tmp_path, flags={"session_state_guard": True})
    state = ws / ".ai-workspace" / "state" / "now.md"
    old = time.time() - 3600  # 1 hour ago -> stale past the 20-min default window
    os.utime(state, (old, old))
    stdout, code = _run("session_state_guard.py", ws)
    assert code == 0
    _assert_single_json(stdout)
    assert (ws / ".claude" / ".session_state_guard").exists()


def test_state_guard_throttled_after_recent_nudge(tmp_path):
    ws = _sandbox(tmp_path, flags={"session_state_guard": True})
    state = ws / ".ai-workspace" / "state" / "now.md"
    old = time.time() - 3600
    os.utime(state, (old, old))
    # A marker dated "now" means we already nudged within the window -> stay silent.
    (ws / ".claude" / ".session_state_guard").write_text(
        datetime.now().isoformat(), encoding="utf-8"
    )
    stdout, code = _run("session_state_guard.py", ws)
    assert code == 0
    assert stdout == ""


# --- now_init (default ON, SessionStart; creates + caps the per-worktree now.md) ---

def test_now_init_creates_now_md_and_names_journal(tmp_path):
    ws = _sandbox(tmp_path, flags={"now_init": True})
    (ws / ".ai-workspace" / "state" / "now.md").unlink()
    stdout, code = _run("now_init.py", ws, stdin='{"session_id": "abcdef12-3456"}')
    assert code == 0
    ctx = _assert_single_json(stdout)["hookSpecificOutput"]["additionalContext"]
    assert "abcdef12" in ctx and "journal/" in ctx
    assert (ws / ".ai-workspace" / "state" / "now.md").is_file()


def test_now_init_trims_overflow_into_session_journal(tmp_path):
    ws = _sandbox(tmp_path, flags={"now_init": True})
    now_md = ws / ".ai-workspace" / "state" / "now.md"
    actions = "\n".join(f"- aktion {i:03d} " + "x" * 80 for i in range(80))
    now_md.write_text(f"# Now\n\n## Letzte Aktionen (neueste oben)\n\n{actions}\n", "utf-8")
    stdout, code = _run("now_init.py", ws, stdin='{"session_id": "0badc0de"}')
    assert code == 0
    _assert_single_json(stdout)
    assert len(now_md.read_bytes()) <= 4096
    journals = list((ws / ".ai-workspace" / "journal").rglob("*-0badc0de.md"))
    assert len(journals) == 1
    moved = journals[0].read_text(encoding="utf-8")
    assert "- aktion 079 " in moved and "- aktion 000 " not in moved  # oldest (bottom) moved


def test_now_init_flags_legacy_current_session(tmp_path):
    ws = _sandbox(tmp_path, flags={"now_init": True})
    (ws / ".ai-workspace" / "state" / "current-session.md").write_text("old\n", "utf-8")
    stdout, _ = _run("now_init.py", ws, stdin='{"session_id": "cafe0001"}')
    assert "now migrate" in _assert_single_json(stdout)["hookSpecificOutput"]["additionalContext"]

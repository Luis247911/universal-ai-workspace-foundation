"""SessionStart hook (matcher ``startup``): offer first-run onboarding on a fresh workspace.

Self-gated on the ``first_run_onboarding`` flag (default ON, see ``automation.flags.json``) and
triple-guarded so it fires at most once per workspace and never for an already-set-up project:

  1. flag ``first_run_onboarding`` is true, and
  2. no onboarding marker ``.claude/.onboarding-state.json`` exists (``/start`` writes it on
     done/skipped; any existing marker -> stay silent, the user can re-run ``/start``), and
  3. the state templates still carry their placeholders (``<projekt-slug>`` in
     ``.ai-workspace/state/project-index.md``) -> a genuinely uninitialised workspace.

When all hold it returns a SessionStart ``additionalContext`` that tells the model to greet the
user and start ``/start``. It NEVER writes state or config; ``/start`` writes the marker. Any error
resolves to inert (return 0, no output) -- the fail-safe direction, identical to the other
automation hooks. Reads only repo-relative paths; never touches ``~/.claude/``.

Power-user / maintainer escape: set ``UAW_DISABLE_ONBOARDING`` in the environment to silence it.
That is not committed, so it never propagates to a clone.
"""

from __future__ import annotations

import json
import os
import sys

from _flags import flag, project_dir

PLACEHOLDER = "<projekt-slug>"


def _onboarding_marker_present() -> bool:
    """True if ``/start`` has already recorded an outcome (any marker -> stay silent).

    A fresh clone has no marker. ``/start`` writes done/skipped on completion; a half-written
    (corrupt) marker still means ``/start`` ran, so we stay silent either way -- consistent with
    the kit's "when unsure, stay inert" stance. The user can always re-run ``/start`` manually.
    """
    return (project_dir() / ".claude" / ".onboarding-state.json").exists()


def _is_fresh_workspace() -> bool:
    """True if the project-index still carries its template placeholder (never set up)."""
    index = project_dir() / ".ai-workspace" / "state" / "project-index.md"
    try:
        text = index.read_text(encoding="utf-8")
    except OSError:
        return False
    return PLACEHOLDER in text


def main() -> int:
    # Drain stdin so the caller never blocks on a broken pipe; SessionStart payload is unused.
    try:
        sys.stdin.read()
    except Exception:
        pass

    if not flag("first_run_onboarding"):
        return 0  # inert: flag off
    if os.environ.get("UAW_DISABLE_ONBOARDING"):
        return 0  # inert: maintainer/power-user opt-out (not committed, never propagates)
    if _onboarding_marker_present():
        return 0  # inert: onboarding already done or skipped
    if not _is_fresh_workspace():
        return 0  # inert: project already set up (placeholders gone)

    context = (
        "## Fresh UAW workspace detected\n"
        "This project has not been set up yet (the state templates still hold their placeholders). "
        "Greet the user briefly and start onboarding by running the `/start` command, which asks "
        "whether they (A) have an existing project to adopt, (B) want to start from scratch, or "
        "(C) want to be left alone for now. Do not set anything up before they choose."
    )
    out = {
        "hookSpecificOutput": {
            "hookEventName": "SessionStart",
            "additionalContext": context,
        }
    }
    print(json.dumps(out))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

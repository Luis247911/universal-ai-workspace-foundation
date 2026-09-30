"""PostToolUse hook (matcher ``Write|Edit|NotebookEdit``): a throttled, staleness-gated reminder to
keep the live session state fresh -- so an accidental CLI close loses as little as possible.

Self-gated on the ``session_state_guard`` flag (default OFF). Unlike a per-event nudge, it speaks
ONLY when ``.ai-workspace/state/now.md`` has gone stale -- not modified for at least
``STALE_MINUTES`` (default 20) of active work -- and then at most once per that interval (throttled
via its own gitignored marker ``.claude/.session_state_guard``). During diligent recitation it stays
completely silent, so it does not nag after every edit.

Honest limit: a hard kill / crash fires no hook. The durability guarantee is the session journal
(append-only, committed, written during the work; D-2026-09-30-01), not now.md, which is local and
gets overwritten. This only tightens the continuous-recitation net. Tunable
via ``UAW_STATE_GUARD_STALE_MINUTES``. Any error -> inert. Reads only repo-relative paths; never
touches ``~/.claude/``.
"""

from __future__ import annotations

import json
import os
import sys
from datetime import datetime, timedelta

from _flags import flag, project_dir


def _stale_minutes() -> int:
    try:
        n = int(os.environ.get("UAW_STATE_GUARD_STALE_MINUTES", "20"))
    except ValueError:
        return 20
    return n if n > 0 else 20


def main() -> int:
    try:
        sys.stdin.read()
    except Exception:
        pass

    if not flag("session_state_guard"):
        return 0  # inert: flag off

    state = project_dir() / ".ai-workspace" / "state" / "now.md"
    try:
        mtime = datetime.fromtimestamp(state.stat().st_mtime)
    except OSError:
        return 0  # no live-state file -> nothing to protect; stay silent

    now = datetime.now()
    window = timedelta(minutes=_stale_minutes())
    if now - mtime < window:
        return 0  # state is fresh -> silent (the diligent-work path)

    # Throttle: at most one nudge per window, tracked in our own gitignored marker.
    marker = project_dir() / ".claude" / ".session_state_guard"
    try:
        last = datetime.fromisoformat(marker.read_text(encoding="utf-8").strip())
        if now - last < window:
            return 0  # already nudged within this window
    except (OSError, ValueError):
        pass  # no / unreadable marker -> treat as "not nudged yet"

    try:
        marker.write_text(now.isoformat(), encoding="utf-8")
    except OSError:
        return 0  # cannot throttle -> stay silent rather than risk repeating

    nudge = (
        "## Session-state freshness\n"
        f"now.md has not been updated in ~{_stale_minutes()}+ min of edits. If the active "
        "task, the next step, or a decision changed: append a journal entry first (that is "
        "what survives an accidental close), then update now.md (Reboot-Test, "
        "session-contract.md section 3). If nothing material changed, ignore this."
    )
    out = {
        "hookSpecificOutput": {
            "hookEventName": "PostToolUse",
            "additionalContext": nudge,
        }
    }
    print(json.dumps(out))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

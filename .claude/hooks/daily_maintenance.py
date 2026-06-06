"""SessionStart hook (matchers ``startup`` + ``resume``): once-a-day maintenance nudge.

Opt-in via the ``daily_maintenance`` flag (default OFF). On the first session of a local calendar
day it reminds the model to run a maintenance pass, then records today's date in a gitignored
marker so it fires at most once per day. It only SUGGESTS -- it never edits files; the model
proposes and the user confirms (same "hook reminds, model writes" stance as ``recitation_nudge``).

Self-marker rule (decisions.md D-2026-06-06-03): a hook may write its own ephemeral, gitignored
run-marker under ``.claude/``; it never writes governance state (``.ai-workspace/**``) or config
(``automation.flags.json``). Today's date is written BEFORE the nudge is emitted, so a later crash
cannot cause a repeat nudge. If the marker cannot be written (e.g. a read-only sandbox) the hook
stays silent rather than nag every session. Any error resolves to inert (return 0, no output).
A "day" is the local calendar day of the executing machine; on multiple machines this may nudge
once per machine per day -- accepted by design. Reads only repo-relative paths; never touches
``~/.claude/``.
"""

from __future__ import annotations

import json
import sys
from datetime import date

from _flags import flag, project_dir


def main() -> int:
    # Drain stdin so the caller never blocks on a broken pipe; SessionStart payload is unused.
    try:
        sys.stdin.read()
    except Exception:
        pass

    if not flag("daily_maintenance"):
        return 0  # inert: flag off

    today = date.today().isoformat()
    marker = project_dir() / ".claude" / ".daily_maintenance_last"
    try:
        if marker.read_text(encoding="utf-8").strip() == today:
            return 0  # inert: already nudged today
    except OSError:
        pass  # no marker yet (or unreadable) -> treat as "not run today"

    # Record today's run first, so a crash after this point cannot cause a repeat nudge. If the
    # marker is not writable, stay silent (stricter fail-safe) instead of nagging every session.
    try:
        marker.write_text(today, encoding="utf-8")
    except OSError:
        return 0

    nudge = (
        "## Daily maintenance (first session today)\n"
        "Consider a maintenance pass -- propose changes, never auto-apply; the user confirms:\n"
        "1. scratch/: file anything worth keeping into its proper lifecycle zone.\n"
        "2. knowledge/: flag dead [[wiki-links]] and notes not touched in >180 days.\n"
        "3. state/artifact-index.md: flag orphaned or untracked artifacts.\n"
        "See knowledge-graph-policy.md section 12 (blueprints) and file-lifecycle.md section 7 "
        "(cadences). If nothing is due, say so briefly and move on."
    )
    out = {
        "hookSpecificOutput": {
            "hookEventName": "SessionStart",
            "additionalContext": nudge,
        }
    }
    print(json.dumps(out))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

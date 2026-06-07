"""PostToolUse hook: periodically suggest a strategic compaction on a long session.

Self-gated on the ``compact_nudge`` flag (default OFF). It counts context-growing tool calls in a
gitignored marker (``.claude/.compact_nudge_state``) and, every ``THRESHOLD`` calls, injects a brief
"consider compacting at the next task boundary" reminder -- the opt-in companion to
.claude/skills/strategic-compact/SKILL.md. Between thresholds it stays silent -- it never nags.

Marker rule (decisions.md D-2026-06-06-03): a hook may write its own gitignored run-marker
under ``.claude/``; never governance state or config. The threshold is tunable via
``UAW_COMPACT_NUDGE_THRESHOLD`` (default 60). Any error -> inert (exit 0, no output). If the marker
is unwritable it stays silent rather than nag. Reads only repo-relative paths; never ``~/.claude/``.
"""

from __future__ import annotations

import json
import os
import sys

from _flags import flag, project_dir


def _threshold() -> int:
    try:
        n = int(os.environ.get("UAW_COMPACT_NUDGE_THRESHOLD", "60"))
    except ValueError:
        return 60
    return n if n > 0 else 60


def main() -> int:
    try:
        sys.stdin.read()
    except Exception:
        pass

    if not flag("compact_nudge"):
        return 0  # inert: flag off

    marker = project_dir() / ".claude" / ".compact_nudge_state"
    try:
        count = int(marker.read_text(encoding="utf-8").strip())
    except (OSError, ValueError):
        count = 0
    count += 1
    try:
        marker.write_text(str(count), encoding="utf-8")
    except OSError:
        return 0  # cannot persist the counter -> stay silent rather than nudge every call

    if count % _threshold() != 0:
        return 0  # between thresholds: silent

    nudge = (
        "## Strategic-compact check\n"
        f"~{count} context-growing tool calls so far. If you are at a task boundary (a phase "
        "finished, a different task next, or a dead-end to clear), consider a manual /compact now: "
        "write the keepers first (state note, task list, files), then compact with a "
        "one-line focus. "
        "See .claude/skills/strategic-compact/SKILL.md. Mid-task: do not compact; ignore this."
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

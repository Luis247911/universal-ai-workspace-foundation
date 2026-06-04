"""SessionStart hook: re-inject the live session state at every boot.

Self-gated on the ``boot_reload`` flag (``.claude/automation.flags.json``). When the flag
is false or missing it prints nothing and exits 0 -> fully inert. When true it reads
``.ai-workspace/state/current-session.md`` and returns it as SessionStart
``additionalContext``, so a new / resumed / cleared / compacted session boots with the
current state already in view.

This is the deterministic half of the "Manus recitation" idea: the hook only RE-READS
state the model itself wrote; it never writes or fabricates state. It reads only
repo-relative paths and never touches ``~/.claude/``.
"""

from __future__ import annotations

import json
import sys

from _flags import flag, project_dir


def main() -> int:
    # Drain stdin so the caller never blocks on a broken pipe. SessionStart provides
    # ``source``/``session_id`` etc., but boot_reload needs none of it.
    try:
        sys.stdin.read()
    except Exception:
        pass

    if not flag("boot_reload"):
        return 0  # inert: flag off

    state = project_dir() / ".ai-workspace" / "state" / "current-session.md"
    try:
        text = state.read_text(encoding="utf-8")
    except OSError:
        return 0  # nothing to inject; stay silent

    context = (
        "## Live session state (auto-reloaded from .ai-workspace/state/current-session.md)\n"
        "Re-orient to this before continuing. It is the file-as-memory of this project; "
        "keep it current per session-contract.md section 3.\n\n"
    ) + text

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

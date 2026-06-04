"""PostToolUse hook (matcher ``Write|Edit|NotebookEdit``): nudge the model to keep the
live session state fresh after a file mutation.

Self-gated on the ``recitation_nudge`` flag. When false or missing -> inert (exit 0, no
output). When true it injects a short reminder (via ``additionalContext``) to update
``.ai-workspace/state/current-session.md`` if the working state changed, per
session-contract.md section 3.

The hook NEVER writes state itself -- it only reminds; the model decides and writes. This
is the continuous half of recitation: kept low-noise by firing only on mutation tools. It
reads only repo-relative paths and never touches ``~/.claude/``.
"""

from __future__ import annotations

import json
import sys

from _flags import flag


def main() -> int:
    # Drain stdin (PostToolUse provides tool_name/tool_input/tool_output); we don't need it.
    try:
        sys.stdin.read()
    except Exception:
        pass

    if not flag("recitation_nudge"):
        return 0  # inert: flag off

    reminder = (
        "Recitation check: if this edit changed the active task, the next step, or any "
        "decision, update .ai-workspace/state/current-session.md (active task + next step "
        "+ evidence) per session-contract.md section 3. If nothing material changed, "
        "ignore this."
    )
    out = {
        "hookSpecificOutput": {
            "hookEventName": "PostToolUse",
            "additionalContext": reminder,
        }
    }
    print(json.dumps(out))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

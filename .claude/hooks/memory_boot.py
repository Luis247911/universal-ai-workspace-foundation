"""SessionStart hook: point at journals that still wait for consolidation.

Self-gated on the ``memory_boot`` flag (default ON, D-2026-09-30-06). Read-only. It lists up to
five finished, unconsolidated journals of *other* sessions (oldest first; journals of sessions
that are still running elsewhere are left out) and suggests the skill
``merken``. After a compaction (``source: compact``) it adds a reminder to check the journal and
``now.md``, because a PreCompact hook can only message the user, not the model. Silent when there
is nothing to say. Output stays far below the context caps (Claude Code 10,000 characters, Codex
about 2,500 tokens). Any error -> exit 0, no output.
"""

from __future__ import annotations

import json
import sys

from _flags import flag, payload, project_dir

MAX_LISTED = 5


def main() -> int:
    data = payload()
    if not flag("memory_boot"):
        return 0
    lines: list[str] = []
    root = project_dir()
    sys.path.insert(0, str(root / "src"))
    try:
        from harness.mdmemory import consolidate, journal
        from harness.mdmemory.workspace import rel

        kurzid = journal.short_id(str(data.get("session_id") or ""))
        own = journal.session_journals(root, kurzid) if data.get("session_id") else []
        todo = consolidate.pending(root, exclude=own)
        if todo:
            lines.append(
                f"- {len(todo)} Journal(e) noch nicht konsolidiert. Bei passender Gelegenheit "
                "den Skill `merken` ausfuehren (`python -m harness.mdmemory pending`):"
            )
            for p in todo[:MAX_LISTED]:
                lines.append(f"  - `{rel(root, p.path)}` ({p.entries} Eintraege)")
            if len(todo) > MAX_LISTED:
                lines.append(f"  - … und {len(todo) - MAX_LISTED} weitere")
    except Exception:
        pass  # engine missing or broken: the compact reminder below still goes out
    if data.get("source") == "compact":
        lines.append(
            "- Kontext wurde gerade kompaktiert: pruefen, ob Journal und `state/now.md` den "
            "Stand enthalten; dauerhafte Erkenntnisse mit `merken` sichern."
        )
    if not lines:
        return 0
    out = {
        "hookSpecificOutput": {
            "hookEventName": "SessionStart",
            "additionalContext": "\n".join(["## Gedaechtnis: offene Konsolidierung", *lines]),
        }
    }
    print(json.dumps(out))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

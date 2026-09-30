"""SessionStart hook: make sure the per-worktree live state ``state/now.md`` exists and fits.

Self-gated on the ``now_init`` flag (default ON, D-2026-09-30-03). On every session start it

1. creates ``.ai-workspace/state/now.md`` from ``templates/session-state.md`` if it is missing
   (the file is gitignored, so a fresh clone or a new worktree has none),
2. trims it to 4 KB if it grew larger; overflow is appended to this session's journal, never
   dropped (D-2026-09-30-02),
3. tells the model its session short id and journal path, so journal entries can be written
   during the work, not only at the end,
4. flags a leftover pre-3.3 ``state/current-session.md`` and names the migration command.

It never edits anything else. Any error -> inert (exit 0, no output). Reads and writes only
repo-relative paths; never touches ``~/.claude/``. Codex can run the same script from
``.codex/hooks.json`` (same stdin shape).
"""

from __future__ import annotations

import json
import sys
from datetime import datetime

from _flags import flag, payload, project_dir, tool


def main() -> int:
    data = payload()
    if not flag("now_init"):
        return 0  # inert: flag off

    root = project_dir()
    sys.path.insert(0, str(root / "src"))
    try:
        from harness.mdmemory import journal, now
        from harness.mdmemory.workspace import legacy_session_path, rel
    except Exception:
        return 0  # engine not shipped in this project -> stay silent

    session_id = str(data.get("session_id") or journal.new_session_id())
    tool_name = tool()
    when = datetime.now()
    notes: list[str] = []
    try:
        if now.ensure(root):
            notes.append("`state/now.md` fehlte und wurde aus der Vorlage angelegt.")
        result = now.trim(root, session_id=session_id, when=when, tool=tool_name)
        if result.changed:
            notes.append(
                f"`state/now.md` war {result.before} B gross und wurde auf {result.after} B "
                "gekuerzt; der Ueberlauf steht im Journal dieser Session."
            )
        if legacy_session_path(root).exists():
            notes.append(
                "Alte `state/current-session.md` gefunden. Migration: "
                "`python -m harness.mdmemory now migrate --remove-legacy`, dann committen."
            )
        kurzid = journal.short_id(session_id)
        jpath = journal.session_journal(root, kurzid) or journal.journal_path(root, when, kurzid)
    except Exception:
        return 0

    lines = [
        "## Gedaechtnis: Session-Kontext",
        f"- Session-Kurz-ID: `{journal.short_id(session_id)}`",
        f"- Journal dieser Session: `{rel(root, jpath)}`"
        + ("" if jpath.exists() else " (noch nicht angelegt)"),
        "- Nach jedem relevanten Ergebnis einen Eintrag anhaengen, nicht erst am Ende "
        f"(`python -m harness.mdmemory journal new --session {session_id} --tool {tool_name}` "
        "legt die Datei an).",
        *[f"- {n}" for n in notes],
    ]
    out = {
        "hookSpecificOutput": {
            "hookEventName": "SessionStart",
            "additionalContext": "\n".join(lines),
        }
    }
    print(json.dumps(out))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

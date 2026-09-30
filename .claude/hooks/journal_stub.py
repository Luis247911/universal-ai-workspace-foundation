"""SessionEnd hook: close this session's journal with a short, deterministic stub entry.

Self-gated on the ``journal_stub`` flag (default ON, D-2026-09-30-06). If this session has a
journal (``journal/YYYY/MM/*-<kurzid>.md``) that is not consolidated yet, it appends one entry
``### HH:MM · uebergabe`` saying the session ended and the journal still needs consolidation
(skill ``merken``). Nothing else:

* no journal, or a journal without entries -> nothing is created or appended,
* consolidated (frozen) journal -> nothing is appended,
* last entry is already an ``uebergabe`` (resume/exit cycles, ``/clear``) -> nothing is appended,
* no content of the work, no transcript path (local paths would leak into a public repo).

Budget: Claude Code gives all SessionEnd hooks 1.5 s together, Codex 1 s by default (max 3 s).
The hook does one directory glob and one append; any error -> exit 0, no output.
"""

from __future__ import annotations

from datetime import datetime

from _flags import flag, load_engine, payload, project_dir, tool


def main() -> int:
    data = payload()
    if not flag("journal_stub"):
        return 0
    root = project_dir()
    if not load_engine(root):
        return 0
    try:
        from harness.mdmemory import frontmatter, journal
        from harness.mdmemory.rollup import _entries
    except Exception:
        return 0
    session_id = str(data.get("session_id") or "")
    if not session_id:
        return 0
    try:
        path = journal.session_journal(root, journal.short_id(session_id))
        if path is None:  # no journal, or consolidated already
            return 0
        _, body = frontmatter.parse(path.read_text(encoding="utf-8"))
        entries = _entries(body)
        if not entries or entries[-1][0] == "uebergabe":
            return 0  # nothing written yet, or already closed (resume/exit cycles)
        reason = str(data.get("reason") or "other")
        journal.append(
            path,
            "uebergabe",
            f"Session beendet ({tool()}, Grund: {reason}). Noch nicht konsolidiert: "
            "beim naechsten Start mit `merken` in Notizen ueberfuehren.",
            datetime.now(),
        )
    except Exception:
        return 0
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

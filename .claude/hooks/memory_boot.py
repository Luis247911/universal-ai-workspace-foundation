"""SessionStart hook: point at journals that still wait for consolidation.

Self-gated on the ``memory_boot`` flag (default ON, D-2026-09-30-09). It lists up to five
finished, unconsolidated journals of *other* sessions (oldest first; journals of sessions that are
still running elsewhere are left out) and suggests the skill ``merken``. After a compaction
(``source: compact``) it adds a reminder to check the journal and ``now.md``, because a PreCompact
hook can only message the user, not the model. On ``startup`` it nudges the weekly skill
``pflege`` when the last report is older than 7 days (at most once a day; its only write is the
gitignored marker ``.claude/.pflege_hint``). Silent when there is nothing to say.
Output stays far below the context caps (Claude Code 10,000 characters, Codex
about 2,500 tokens). Any error -> exit 0, no output.
"""

from __future__ import annotations

import json
from datetime import date
from pathlib import Path

from _flags import flag, load_engine, mdm_command, payload, project_dir

MAX_LISTED = 5
PFLEGE_DAYS = 7


def _pflege_due(root: Path) -> bool:
    """Weekly maintenance nudge: notes exist, no report in the last PFLEGE_DAYS days, and not yet
    nudged today (own gitignored marker ``.claude/.pflege_hint``, write doctrine (a))."""
    ws = root / ".ai-workspace"
    if not any((ws / "knowledge").glob("*/*.md")):
        return False
    today = date.today()
    reports = sorted((ws / "scratch" / "maintenance").glob("*-pflege.md"))
    if reports:
        try:
            last = date.fromisoformat(reports[-1].name[:10])
        except ValueError:
            last = date.min
        if (today - last).days < PFLEGE_DAYS:
            return False
    marker = root / ".claude" / ".pflege_hint"
    try:
        if marker.read_text(encoding="utf-8").strip() == today.isoformat():
            return False
    except OSError:
        pass
    try:
        marker.write_text(today.isoformat() + "\n", encoding="utf-8")
    except OSError:
        return False
    return True


def main() -> int:
    data = payload()
    if not flag("memory_boot"):
        return 0
    lines: list[str] = []
    root = project_dir()
    try:
        if not load_engine(root):
            raise ImportError("engine missing")
        from harness.mdmemory import consolidate, journal
        from harness.mdmemory.workspace import rel

        kurzid = journal.short_id(str(data.get("session_id") or ""))
        own = journal.session_journals(root, kurzid) if data.get("session_id") else []
        todo = consolidate.pending(root, exclude=own)
        if todo:
            lines.append(
                f"- {len(todo)} Journal(e) noch nicht konsolidiert. Bei passender Gelegenheit "
                f"den Skill `merken` ausfuehren (`{mdm_command()} pending`):"
            )
            for p in todo[:MAX_LISTED]:
                lines.append(f"  - `{rel(root, p.path)}` ({p.entries} Eintraege)")
            if len(todo) > MAX_LISTED:
                lines.append(f"  - … und {len(todo) - MAX_LISTED} weitere")
        if data.get("source") in (None, "startup") and _pflege_due(root):
            lines.append(
                "- Der letzte Pflege-Bericht ist aelter als 7 Tage (oder es gibt keinen): bei "
                f"Gelegenheit den Skill `pflege` ausfuehren (`{mdm_command()} report --write`)."
            )
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

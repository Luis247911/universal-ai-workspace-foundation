"""Keep the generated memory index current without the model having to remember it.

Self-gated on the ``index_refresh`` flag (default ON, D-2026-09-30-09).

* PostToolUse (Write|Edit|MultiEdit|NotebookEdit): when the edited file is a note under
  ``.ai-workspace/knowledge/<typ>/``, regenerate ``knowledge/INDEX.md``, ``knowledge/_typen/`` and
  the register views (``harness.mdmemory index``).
* SessionStart (startup|resume): regenerate when the index is out of date, e.g. after a
  ``git pull`` or a merge that combined generated files with ``merge=union``.

It writes only generated files (D-2026-09-30-05/-09), never a note. Silent on success; if a note
cannot be parsed it tells the model which one, so it can fix it. Any other error -> exit 0,
no output.
"""

from __future__ import annotations

import json
from pathlib import Path

from _flags import flag, load_engine, payload, project_dir


def _is_note(root: Path, file_path: str) -> bool:
    base = (root / ".ai-workspace" / "knowledge").resolve()
    try:
        rel = Path(file_path).resolve().relative_to(base)
    except (ValueError, OSError):
        return False
    parts = rel.parts
    return len(parts) == 2 and not parts[0].startswith("_") and parts[1].endswith(".md")


def _say(event: str, text: str) -> None:
    out = {"hookSpecificOutput": {"hookEventName": event, "additionalContext": text}}
    print(json.dumps(out))


def main() -> int:
    data = payload()
    if not flag("index_refresh"):
        return 0
    root = project_dir()
    event = str(data.get("hook_event_name") or "")
    if event == "PostToolUse":
        tool_input = data.get("tool_input") or {}
        target = str(tool_input.get("file_path") or tool_input.get("notebook_path") or "")
        if not target or not _is_note(root, target):
            return 0
    if not load_engine(root):
        return 0
    try:
        from harness.mdmemory import index
        from harness.mdmemory.frontmatter import FrontmatterError
    except Exception:
        return 0
    try:
        if event != "PostToolUse" and not index.stale(root):
            return 0
        index.write(root)
    except FrontmatterError as exc:
        _say(
            event or "PostToolUse",
            f"## Gedaechtnis-Index nicht aktualisiert\n- Notiz nicht lesbar: {exc}\n"
            "- Frontmatter reparieren; der Index wird danach automatisch neu erzeugt.",
        )
    except Exception:
        return 0
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

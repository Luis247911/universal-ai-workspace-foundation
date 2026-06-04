"""Shared helper for the opt-in automation hooks.

Resolves the kit repo root and reads ``.claude/automation.flags.json``. Reads ONLY
repo-relative paths; it never touches ``~/.claude/`` (the user's private global layer).
Pure stdlib so it runs identically on Windows, macOS, Linux and in the web sandbox.

Every hook self-gates on its flag via :func:`flag`. Any error (missing file, bad JSON,
missing key) resolves to OFF -- the fail-safe direction, so a broken config is inert,
never noisy.
"""

from __future__ import annotations

import json
import os
from pathlib import Path


def project_dir() -> Path:
    """Return the kit repo root.

    Prefer ``CLAUDE_PROJECT_DIR`` (set by Claude Code for project-level hooks); fall back
    to this file's own location (``.claude/hooks/_flags.py`` -> ``parents[2]``) so the
    helper still works when invoked outside a hook (e.g. a manual self-test).
    """
    env = os.environ.get("CLAUDE_PROJECT_DIR")
    if env:
        candidate = Path(env)
        if candidate.is_dir():
            return candidate
    return Path(__file__).resolve().parents[2]


def flag(name: str) -> bool:
    """Return the boolean automation flag ``name`` from ``.claude/automation.flags.json``.

    Missing file, unreadable JSON, or a missing key all mean OFF (fail-safe inert).
    """
    flags_path = project_dir() / ".claude" / "automation.flags.json"
    try:
        data = json.loads(flags_path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return False
    return bool(data.get(name, False))

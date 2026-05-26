"""Cross-platform path helpers.

NEVER hard-code '/tmp' or build paths by string concatenation. Run artifacts (HITL
state, traces) default to a project-relative ./.uaw-runs/ so they behave identically
on Windows and POSIX. Override the root with the UAW_RUNS_DIR env var.
"""

from __future__ import annotations

import os
from pathlib import Path

RUNS_DIRNAME = ".uaw-runs"


def runs_root() -> Path:
    override = os.environ.get("UAW_RUNS_DIR")
    return Path(override) if override else Path.cwd() / RUNS_DIRNAME


def run_dir(run_id: str) -> Path:
    d = runs_root() / run_id
    d.mkdir(parents=True, exist_ok=True)
    return d


def ensure_dir(path: str | os.PathLike) -> Path:
    p = Path(path)
    p.mkdir(parents=True, exist_ok=True)
    return p

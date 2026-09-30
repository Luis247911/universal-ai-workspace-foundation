"""Locate the workspace and its memory paths (repo-relative, no global state)."""

from __future__ import annotations

from pathlib import Path

WORKSPACE_DIR = ".ai-workspace"

#: Optional global namespace (memory contract, default 4): a SEPARATE workspace, ideally its own
#: private repo, for notes with ``scope: global``. Off unless this variable names a directory.
GLOBAL_ENV = "UAW_GLOBAL_MEMORY_DIR"


def global_root(environ: dict[str, str] | None = None) -> Path | None:
    """The global namespace's root (contains ``.ai-workspace/``), or None when switched off."""
    import os

    value = (environ if environ is not None else os.environ).get(GLOBAL_ENV, "").strip()
    if not value:
        return None
    path = Path(value).expanduser()
    return path if (path / WORKSPACE_DIR).is_dir() else None


def find_root(start: Path | str | None = None) -> Path:
    """Walk up from ``start`` (default: cwd) to the directory holding ``.ai-workspace/``."""
    here = Path(start or Path.cwd()).resolve()
    for candidate in (here, *here.parents):
        if (candidate / WORKSPACE_DIR).is_dir():
            return candidate
    raise FileNotFoundError(f"no {WORKSPACE_DIR}/ found above {here}")


def ws(root: Path) -> Path:
    return root / WORKSPACE_DIR


def state_dir(root: Path) -> Path:
    return ws(root) / "state"


def journal_dir(root: Path) -> Path:
    return ws(root) / "journal"


def knowledge_dir(root: Path) -> Path:
    return ws(root) / "knowledge"


def templates_dir(root: Path) -> Path:
    return ws(root) / "templates"


def now_path(root: Path) -> Path:
    return state_dir(root) / "now.md"


def legacy_session_path(root: Path) -> Path:
    """The pre-3.3 shared live state, kept only as a migration source."""
    return state_dir(root) / "current-session.md"


def rel(root: Path, path: Path) -> str:
    """Repo-relative POSIX path for messages and pointers."""
    try:
        return path.resolve().relative_to(root.resolve()).as_posix()
    except ValueError:
        return path.as_posix()

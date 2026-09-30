"""Import Claude Code auto-memory files as journal candidates (never as notes).

Claude Code keeps auto-memory outside the repo, per project, in
``~/.claude/projects/<project-path-with-dashes>/memory/*.md``. In a foundation repo auto-memory is
switched off (memory contract); existing files are carried over once with this importer:

* the source folder is only read, never changed or deleted,
* all files go into ONE new journal ``journal/YYYY/MM/YYYY-MM-DD-<hash>.md`` as ``notiz`` entries,
  each with its origin ``automemory:<file>`` and the text verbatim in a fenced block,
* the hash covers the imported content, so a second import of the same files is a no-op,
* turning a candidate into a note is the normal consolidation step (skill ``merken``); the
  importer makes no judgement about what is still true.

Auto-memory may hold personal data. Review the journal before committing it (security-policy).
"""

from __future__ import annotations

import hashlib
import re
import subprocess
from datetime import datetime
from pathlib import Path

from . import journal
from .workspace import journal_dir

INDEX_FILE = "MEMORY.md"


def project_slug(path: str) -> str:
    """Claude Code's folder name for a project path: every character except ASCII letters and
    digits becomes ``-`` (``/Users/a/My Proj/.x`` -> ``-Users-a-My-Proj--x``)."""
    return re.sub(r"[^A-Za-z0-9]", "-", path)


def _main_worktree(root: Path) -> Path:
    """Auto-memory is shared per git repository: map a linked worktree to the main checkout."""
    try:
        out = subprocess.run(
            ["git", "-C", str(root), "rev-parse", "--path-format=absolute", "--git-common-dir"],
            capture_output=True,
            text=True,
            timeout=5,
            check=True,
        ).stdout.strip()
    except (OSError, subprocess.SubprocessError):
        return root
    common = Path(out)
    return common.parent if common.name == ".git" else root


def default_source(root: Path, home: Path | None = None) -> Path:
    """Claude Code's auto-memory folder for the project at ``root`` (main checkout first)."""
    base = (home or Path.home()) / ".claude" / "projects"
    candidates = [_main_worktree(root.resolve()), root.resolve()]
    paths = [base / project_slug(str(c)) / "memory" for c in candidates]
    return next((p for p in paths if p.is_dir()), paths[0])


def collect(source: Path) -> list[tuple[str, str]]:
    """(file name, text) of every Markdown file in ``source``; the index MEMORY.md last."""
    files = sorted(p for p in source.glob("*.md") if p.is_file())
    files.sort(key=lambda p: p.name == INDEX_FILE)
    return [(p.name, p.read_text(encoding="utf-8")) for p in files]


def digest(items: list[tuple[str, str]]) -> str:
    h = hashlib.sha256()
    for name, text in items:
        h.update(name.encode("utf-8") + b"\0" + text.encode("utf-8") + b"\0")
    return h.hexdigest()


def _existing(root: Path, kurzid: str) -> Path | None:
    base = journal_dir(root)
    hits = sorted(base.rglob(f"*-{kurzid}.md")) if base.is_dir() else []
    return hits[0] if hits else None


def _fence(text: str) -> str:
    ticks = "````"
    while ticks in text:
        ticks += "`"
    return f"{ticks}markdown\n{text.rstrip()}\n{ticks}"


def import_dir(
    root: Path, source: Path, *, when: datetime | None = None, dry_run: bool = False
) -> tuple[Path | None, int, bool]:
    """Returns (journal path, number of files, created). ``None`` path if there is nothing."""
    items = collect(source) if source.is_dir() else []
    if not items:
        return None, 0, False
    full = digest(items)
    kurzid = full[:8]
    found = _existing(root, kurzid)
    if found:
        return found, len(items), False
    when = when or datetime.now()
    path = journal.journal_path(root, when, kurzid)
    if dry_run:
        return path, len(items), False
    path.parent.mkdir(parents=True, exist_ok=True)
    text = journal.render(
        root,
        session_id=f"automemory-{full[:16]}",
        when=when,
        tool="import-automemory",
    )
    with path.open("x", encoding="utf-8", newline="\n") as fh:
        fh.write(text)
    journal.append(
        path,
        "notiz",
        f"Import von {len(items)} Auto-Memory-Datei(en) als Kandidaten. Quelle unveraendert. "
        "Jeder Kandidat wird ueber `merken` geprueft (NOOP/ADD/UPDATE/SUPERSEDE/CONFLICT).",
        when,
    )
    for name, content in items:
        journal.append(
            path,
            "notiz",
            f"Kandidat · Quelle `automemory:{name}`\n\n{_fence(content)}",
            when,
        )
    return path, len(items), True

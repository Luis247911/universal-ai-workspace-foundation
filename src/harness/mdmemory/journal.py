"""Session journal: one append-only Markdown file per session.

Path: ``.ai-workspace/journal/YYYY/MM/YYYY-MM-DD-<kurzid>.md``. One writer per file, so parallel
sessions and worktrees never touch the same path. Entries are appended at the end of the file;
existing lines are never changed. After ``konsolidiert: true`` the file is frozen.
"""

from __future__ import annotations

import hashlib
import re
from datetime import datetime
from pathlib import Path

from . import frontmatter
from .workspace import journal_dir, templates_dir

TEMPLATE_NAME = "journal-entry.md"
KINDS = ("ergebnis", "entscheidung", "fakt", "korrektur", "offen", "uebergabe", "notiz")

BUILTIN_TEMPLATE = """---
id: j-<datum>-<session-kurzid>
type: journal
session: <session-id>
tool: <tool>
worktree: <worktree>
started: <start>
transcript: <transcript>
themen: []
konsolidiert: false
konsolidiert_zu: []
---
# Journal <datum> · <session-kurzid>

Eine Datei pro Session. **Nur anhaengen**, nie bestehende Eintraege aendern. Nach
`konsolidiert: true` unveraenderlich. Regeln: `../../README.md`.

## Ziel

<1-2 Saetze: was diese Session erreichen soll>

## Eintraege

<!-- Neue Eintraege unten anhaengen: "### HH:MM · <art>" plus 1-5 Zeilen.
     Arten: ergebnis | entscheidung | fakt | korrektur | offen | uebergabe | notiz -->
"""


class JournalFrozenError(RuntimeError):
    """Raised on an attempt to append to a consolidated (frozen) journal."""


def short_id(session_id: str) -> str:
    """Stable 8-char id for file names: the first 8 hex digits, else a hash of the id."""
    hexchars = re.sub(r"[^0-9a-f]", "", session_id.lower())
    if len(hexchars) >= 8:
        return hexchars[:8]
    return hashlib.sha1(session_id.encode("utf-8")).hexdigest()[:8]


def journal_path(root: Path, day: datetime, kurzid: str) -> Path:
    return journal_dir(root) / f"{day:%Y}" / f"{day:%m}" / f"{day:%Y-%m-%d}-{kurzid}.md"


def _template(root: Path) -> str:
    path = templates_dir(root) / TEMPLATE_NAME
    try:
        return path.read_text(encoding="utf-8")
    except OSError:
        return BUILTIN_TEMPLATE


def render(
    root: Path,
    *,
    session_id: str,
    when: datetime,
    tool: str = "unbekannt",
    worktree: str = "",
    transcript: str = "",
) -> str:
    text = _template(root)
    values = {
        "<datum>": f"{when:%Y-%m-%d}",
        "<session-kurzid>": short_id(session_id),
        "<session-id>": session_id,
        "<tool>": tool,
        "<worktree>": worktree,
        "<start>": f"{when:%Y-%m-%dT%H:%M}",
        "<transcript>": transcript,
    }
    raw, body = frontmatter.split(text)
    if raw is not None:
        for key, val in values.items():
            raw = raw.replace(key, val)
        for key in ("<datum>", "<session-kurzid>"):
            body = body.replace(key, values[key])
        text = f"---\n{raw}\n---\n{body}"
    return text


def ensure(
    root: Path,
    *,
    session_id: str,
    when: datetime | None = None,
    tool: str = "unbekannt",
    worktree: str = "",
    transcript: str = "",
) -> tuple[Path, bool]:
    """Create the session journal if it does not exist yet. Never overwrites. (path, created)."""
    when = when or datetime.now()
    path = journal_path(root, when, short_id(session_id))
    if path.exists():
        return path, False
    path.parent.mkdir(parents=True, exist_ok=True)
    text = render(
        root, session_id=session_id, when=when, tool=tool, worktree=worktree, transcript=transcript
    )
    with path.open("x", encoding="utf-8", newline="\n") as fh:
        fh.write(text)
    return path, True


def is_frozen(text: str) -> bool:
    meta, _ = frontmatter.parse(text)
    return meta is not None and str(meta.get("konsolidiert", "")).lower() == "true"


def append(path: Path, kind: str, lines: list[str] | str, when: datetime | None = None) -> None:
    """Append one entry ``### HH:MM · <kind>`` at the end of the journal."""
    when = when or datetime.now()
    text = path.read_text(encoding="utf-8")
    if is_frozen(text):
        raise JournalFrozenError(f"{path} is consolidated; write a new journal instead")
    body = lines if isinstance(lines, str) else "\n".join(lines)
    block = f"\n### {when:%H:%M} · {kind}\n\n{body.rstrip()}\n"
    with path.open("a", encoding="utf-8", newline="\n") as fh:
        if not text.endswith("\n"):
            fh.write("\n")
        fh.write(block)


def iter_journals(root: Path):
    """All journal files (sorted, oldest first). Skips README and generated rollups."""
    base = journal_dir(root)
    if not base.is_dir():
        return []
    return sorted(
        p for p in base.rglob("*.md") if p.name != "README.md" and not p.name.startswith("_")
    )

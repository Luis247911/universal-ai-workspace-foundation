"""Session journal: one append-only Markdown file per session.

Path: ``.ai-workspace/journal/YYYY/MM/YYYY-MM-DD-<kurzid>.md``. One writer per file, so parallel
sessions and worktrees never touch the same path. Entries are appended at the end of the file;
existing lines are never changed. After ``konsolidiert: true`` the file is frozen.
"""

from __future__ import annotations

import hashlib
import re
import uuid
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
    """Stable 8-char id for file names.

    UUIDv4 (Claude Code): the first 8 hex digits. UUIDv7 (Codex) starts with a millisecond
    timestamp, so two sessions started within about a minute share the first 8 digits; there the
    last 8 (random) digits are used. Anything else: a hash of the whole id.
    """
    hexchars = re.sub(r"[^0-9a-f]", "", session_id.lower())
    if len(hexchars) == 32 and hexchars[12] == "7":
        return hexchars[-8:]
    if len(hexchars) >= 8:
        return hexchars[:8]
    return hashlib.sha1(session_id.encode("utf-8")).hexdigest()[:8]


def new_session_id() -> str:
    """A random session id for manual CLI use (no hook, no tool session)."""
    return uuid.uuid4().hex


def journal_path(root: Path, day: datetime, kurzid: str) -> Path:
    return journal_dir(root) / f"{day:%Y}" / f"{day:%m}" / f"{day:%Y-%m-%d}-{kurzid}.md"


def session_journals(root: Path, kurzid: str) -> list[Path]:
    """All journals of one session, oldest first (continuations are ``<datum>-<kurzid>-<n>.md``)."""
    base = journal_dir(root)
    if not base.is_dir():
        return []
    hits = set(base.glob(f"*/*/*-{kurzid}.md")) | set(base.glob(f"*/*/*-{kurzid}-[0-9]*.md"))
    return sorted(hits, key=lambda p: (p.name[:10], p.stem))


def session_journal(root: Path, kurzid: str) -> Path | None:
    """The open (not consolidated) journal of this session, or None."""
    for path in reversed(session_journals(root, kurzid)):
        try:
            if not is_frozen(path.read_text(encoding="utf-8")):
                return path
        except OSError:
            continue
    return None


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
    """Return the open journal of this session, creating it if needed. (path, created).

    A session keeps its journal across midnight and month ends. If its journal is consolidated
    already, a continuation ``<datum>-<kurzid>-2.md`` (``-3`` ...) is started. Never overwrites.
    """
    when = when or datetime.now()
    kurzid = short_id(session_id)
    existing = session_journal(root, kurzid)
    if existing is not None:
        return existing, False
    path = journal_path(root, when, kurzid)
    n = 2
    while path.exists():
        path = path.with_name(f"{when:%Y-%m-%d}-{kurzid}-{n}.md")
        n += 1
    path.parent.mkdir(parents=True, exist_ok=True)
    text = render(
        root, session_id=session_id, when=when, tool=tool, worktree=worktree, transcript=transcript
    )
    try:
        with path.open("x", encoding="utf-8", newline="\n") as fh:
            fh.write(text)
    except FileExistsError:  # a second process of the same session was faster
        return path, False
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

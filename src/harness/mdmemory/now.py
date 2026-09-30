"""``state/now.md``: the per-worktree live state (gitignored, hard cap 4 KB).

``ensure`` creates it from ``templates/session-state.md``. ``trim`` keeps it under the cap without
losing anything: overflow moves into the session journal first, oldest actions first. ``migrate``
turns a pre-3.3 ``state/current-session.md`` into a migration journal plus a local ``now.md``.
"""

from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path

from . import journal
from .limits import NOW_MAX_BYTES
from .workspace import journal_dir, legacy_session_path, now_path, templates_dir

TEMPLATE_NAME = "session-state.md"
ACTIONS_HEADING = "## Letzte Aktionen"

BUILTIN_TEMPLATE = """---
id: now
type: now
title: "Live-Zustand dieses Worktrees"
updated: <YYYY-MM-DD HH:MM>
session: <session-kurzid>
journal: <journal-pfad>
---
# Now

Live-Zustand dieses Worktrees: gitignored, nicht geteilt, max. 4 KB. Episoden gehoeren ins
Journal, nicht hierher. Regeln: `../session-contract.md` §3.

## Aktive Aufgabe

<1 Satz>

## Status

<in_progress / blocked / waiting_for_user / paused / done>

## Reboot-Test

- **Wo bin ich?** <...>
- **Was ist das Ziel?** <...>
- **Was hat sich geaendert?** <...>
- **Was bleibt offen?** <...>
- **Welche Evidenz?** <...>

## Naechste Schritte

- <...>

## Offene Handoffs

(keine)

## Letzte Aktionen (neueste oben, max. 10)

(noch keine)
"""


def _size(text: str) -> int:
    return len(text.encode("utf-8"))


def template(root: Path) -> str:
    try:
        return (templates_dir(root) / TEMPLATE_NAME).read_text(encoding="utf-8")
    except OSError:
        return BUILTIN_TEMPLATE


def ensure(root: Path) -> bool:
    """Create ``state/now.md`` from the template if it is missing. Returns True if created."""
    path = now_path(root)
    if path.exists():
        return False
    path.parent.mkdir(parents=True, exist_ok=True)
    try:
        with path.open("x", encoding="utf-8", newline="\n") as fh:
            fh.write(template(root))
    except FileExistsError:  # a parallel session in this worktree was faster
        return False
    return True


@dataclass
class TrimResult:
    before: int
    after: int
    moved: list[str] = field(default_factory=list)
    snapshot: bool = False
    normalized: bool = False

    @property
    def changed(self) -> bool:
        return bool(self.moved) or self.snapshot or self.normalized


#: Smallest limit ``trim`` accepts: the fallback marker plus a little text must fit.
MIN_LIMIT = 256

_MARKER = "> (gekuerzt durch trim; vollstaendige Fassung im Journal)\n"


def _split_actions(lines: list[str]) -> tuple[int, int]:
    """Return [start, end) of the bullet lines under the actions heading, or (-1, -1)."""
    start = next((i for i, ln in enumerate(lines) if ln.startswith(ACTIONS_HEADING)), -1)
    if start == -1:
        return -1, -1
    end = next((i for i in range(start + 1, len(lines)) if lines[i].startswith("## ")), len(lines))
    return start + 1, end


def _action_blocks(lines: list[str], start: int, end: int) -> list[tuple[int, int]]:
    """[a, b) ranges of top-level bullets plus their indented continuation lines."""
    blocks: list[tuple[int, int]] = []
    i = start
    while i < end:
        if lines[i].startswith("- "):
            j = i + 1
            while j < end and lines[j].strip() and lines[j][:1] in (" ", "\t"):
                j += 1
            blocks.append((i, j))
            i = j
        else:
            i += 1
    return blocks


def _cut_bytes(text: str, max_bytes: int) -> str:
    return text.encode("utf-8")[: max(max_bytes, 0)].decode("utf-8", "ignore")


def trim_text(text: str, limit: int = NOW_MAX_BYTES) -> tuple[str, list[str], bool]:
    """Pure trim. Returns (new_text, moved_action_lines, snapshot_needed).

    1. Drop the oldest bullets under "Letzte Aktionen" (bottom first, each with its indented
       continuation lines) until the text fits.
    2. Still too big: every section body is cut to its first 3 lines and a marker is added. The
       caller must then store the full original as a snapshot in the journal.
    """
    if limit < MIN_LIMIT:
        raise ValueError(f"limit must be at least {MIN_LIMIT} bytes")
    if _size(text) <= limit:
        return text, [], False
    lines = text.split("\n")
    moved: list[str] = []
    start, end = _split_actions(lines)
    if start != -1:
        blocks = _action_blocks(lines, start, end)
        while blocks and _size("\n".join(lines)) > limit:
            a, b = blocks.pop()
            moved[:0] = lines[a:b]
            del lines[a:b]
    text2 = "\n".join(lines)
    if _size(text2) <= limit:
        return text2, moved, False
    # Fallback: keep the frontmatter and headings, cut each section body to its first 3 lines.
    meta_end = 0
    if lines and lines[0].lstrip("\ufeff").rstrip() == "---":
        closing = [i for i in range(1, len(lines)) if lines[i].rstrip() == "---"]
        meta_end = closing[0] + 1 if closing else 0
    out = lines[:meta_end]
    kept = 0
    fenced = False
    for ln in lines[meta_end:]:
        if ln.lstrip().startswith("```"):
            fenced = not fenced
        if ln.startswith("#") and not fenced:
            kept = 0
            out.append(ln)
        elif not ln.strip():
            if out and out[-1].strip():
                out.append(ln)
        elif kept < 3:
            out.append(ln)
            kept += 1

    def render(body: list[str]) -> str:
        return "\n".join(body).rstrip("\n") + "\n\n" + _MARKER

    while len(out) > 1 and _size(render(out)) > limit:
        out.pop()
    shortened = render(out)
    if _size(shortened) > limit:  # one very long line left: cut it by bytes
        room = limit - _size(_MARKER) - 2
        shortened = _cut_bytes("\n".join(out).rstrip("\n"), room) + "\n\n" + _MARKER
    return shortened, moved, True


def trim(
    root: Path,
    *,
    session_id: str,
    limit: int = NOW_MAX_BYTES,
    when: datetime | None = None,
    tool: str = "unbekannt",
    journal_file: Path | None = None,
) -> TrimResult:
    """Trim ``state/now.md`` to ``limit`` bytes; overflow is appended to the session journal."""
    when = when or datetime.now()
    path = now_path(root)
    raw = path.read_bytes()
    before = len(raw)
    text = raw.decode("utf-8").replace("\r\n", "\n").replace("\r", "\n")
    new, moved, snapshot = trim_text(text, limit)
    if not moved and not snapshot:
        if before > limit:  # only the CRLF line ends made it too big on disk
            _write_lf(path, new)
            return TrimResult(before, _size(new), normalized=True)
        return TrimResult(before, before)
    jpath = journal_file or journal.ensure(root, session_id=session_id, when=when, tool=tool)[0]
    if moved:
        journal.append(jpath, "notiz", ["Aus `state/now.md` ausgelagert (trim):", *moved], when)
    if snapshot:
        journal.append(
            jpath,
            "notiz",
            [
                "Snapshot von `state/now.md` vor dem Kuerzen (trim):",
                "",
                _fence(text) + "markdown",
                text.rstrip("\n"),
                _fence(text),
            ],
            when,
        )
    _write_lf(path, new)
    return TrimResult(before, _size(new), moved, snapshot)


def _write_lf(path: Path, text: str) -> None:
    with path.open("w", encoding="utf-8", newline="\n") as fh:
        fh.write(text)


def _fence(content: str) -> str:
    """A backtick fence longer than any backtick run inside ``content`` (at least four)."""
    longest = max((len(m) for m in re.findall(r"`+", content)), default=0)
    return "`" * max(4, longest + 1)


def _migration_block(content: bytes, when: datetime, digest: str) -> bytes:
    text = content.decode("utf-8", "replace")
    fence = _fence(text)
    tail = b"" if content.endswith(b"\n") else b"\n"
    note = "" if not tail else " (ohne abschliessenden Zeilenumbruch im Original)"
    head = (
        f"### {when:%H:%M} · notiz\n\n"
        f"Inhalt von `state/current-session.md` vor der Migration, byte-genau{note}.\n"
        f"sha256: `{digest}`\n\n"
        f"{fence}markdown\n"
    )
    return head.encode("utf-8") + content + tail + f"{fence}\n".encode()


def migrate(root: Path, *, when: datetime | None = None, remove_legacy: bool = False) -> Path:
    """Move a pre-3.3 ``state/current-session.md`` into the journal and seed ``now.md``.

    Writes ``journal/YYYY/MM/YYYY-MM-DD-migration.md`` containing the legacy file byte for byte
    (with its sha256), seeds ``now.md`` from the legacy content when ``now.md`` is missing or still
    the untouched template (then trims it), and only with ``remove_legacy`` deletes the legacy file
    after checking the journal holds it byte for byte. Idempotent: a second run with the same
    legacy content adds nothing; changed content is appended as a new entry.
    """
    when = when or datetime.now()
    legacy = legacy_session_path(root)
    content = legacy.read_bytes()
    digest = hashlib.sha256(content).hexdigest()
    base = journal_dir(root) / f"{when:%Y}" / f"{when:%m}"
    existing = [
        p
        for p in sorted(journal_dir(root).glob("*/*/*-migration*.md"))
        if digest in p.read_text(encoding="utf-8", errors="replace")
        and content in p.read_bytes()
    ]
    if existing:
        target = existing[0]
    else:
        target = base / f"{when:%Y-%m-%d}-migration.md"
        n = 2
        while target.exists() and journal.is_frozen(target.read_text(encoding="utf-8")):
            target = base / f"{when:%Y-%m-%d}-migration-{n}.md"
            n += 1
        target.parent.mkdir(parents=True, exist_ok=True)
        if not target.exists():
            header = (
                "---\n"
                f"id: j-{target.stem}\n"
                "type: journal\n"
                "session: migration\n"
                "tool: migration\n"
                "worktree:\n"
                f"started: {when:%Y-%m-%dT%H:%M}\n"
                "transcript:\n"
                "themen: [migration, now]\n"
                "konsolidiert: false\n"
                "konsolidiert_zu: []\n"
                "---\n"
                f"# Journal {when:%Y-%m-%d} · migration\n\n"
                "## Ziel\n\n"
                "Umzug von `state/current-session.md` (geteilt, getrackt) nach `state/now.md` "
                "(pro Worktree, gitignored). Der alte Inhalt steht unten unveraendert.\n\n"
                "## Eintraege\n\n"
            )
            target.write_bytes(header.encode("utf-8") + _migration_block(content, when, digest))
        else:
            old = target.read_bytes()
            sep = b"" if old.endswith(b"\n") else b"\n"
            target.write_bytes(old + sep + b"\n" + _migration_block(content, when, digest))
    if content not in target.read_bytes():
        raise RuntimeError(f"{target} does not contain the legacy state; refusing to continue")
    npath = now_path(root)
    seed = not npath.exists()
    if not seed:
        seed = npath.read_text(encoding="utf-8") == template(root)
    if seed:
        npath.parent.mkdir(parents=True, exist_ok=True)
        text = content.decode("utf-8", "replace").replace("\r\n", "\n").replace("\r", "\n")
        _write_lf(npath, text)
        trim(root, session_id="migration", when=when, journal_file=target)
    if remove_legacy:
        legacy.unlink()
    return target

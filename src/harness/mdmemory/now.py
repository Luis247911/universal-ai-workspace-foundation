"""``state/now.md``: the per-worktree live state (gitignored, hard cap 4 KB).

``ensure`` creates it from ``templates/session-state.md``. ``trim`` keeps it under the cap without
losing anything: overflow moves into the session journal first, oldest actions first. ``migrate``
turns a pre-3.3 ``state/current-session.md`` into a migration journal plus a local ``now.md``.
"""

from __future__ import annotations

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
    with path.open("x", encoding="utf-8", newline="\n") as fh:
        fh.write(template(root))
    return True


@dataclass
class TrimResult:
    before: int
    after: int
    moved: list[str] = field(default_factory=list)
    snapshot: bool = False

    @property
    def changed(self) -> bool:
        return bool(self.moved) or self.snapshot


def _split_actions(lines: list[str]) -> tuple[int, int]:
    """Return [start, end) of the bullet lines under the actions heading, or (-1, -1)."""
    start = next((i for i, ln in enumerate(lines) if ln.startswith(ACTIONS_HEADING)), -1)
    if start == -1:
        return -1, -1
    end = next((i for i in range(start + 1, len(lines)) if lines[i].startswith("## ")), len(lines))
    return start + 1, end


def trim_text(text: str, limit: int = NOW_MAX_BYTES) -> tuple[str, list[str], bool]:
    """Pure trim. Returns (new_text, moved_action_lines, snapshot_needed).

    1. Drop the oldest bullets under "Letzte Aktionen" (bottom first) until the text fits.
    2. Still too big: every section body is cut to its first 3 lines and a marker is added. The
       caller must then store the full original as a snapshot in the journal.
    """
    if _size(text) <= limit:
        return text, [], False
    lines = text.split("\n")
    moved: list[str] = []
    start, end = _split_actions(lines)
    if start != -1:
        bullets = [i for i in range(start, end) if lines[i].lstrip().startswith("- ")]
        while bullets and _size("\n".join(lines)) > limit:
            idx = bullets.pop()
            moved.insert(0, lines[idx])
            del lines[idx]
    text2 = "\n".join(lines)
    if _size(text2) <= limit:
        return text2, moved, False
    # Fallback: keep the frontmatter and headings, cut each section body to its first 3 lines.
    meta_end = 0
    if lines and lines[0] == "---" and "---" in lines[1:]:
        meta_end = lines.index("---", 1) + 1
    out = lines[:meta_end]
    kept = 0
    for ln in lines[meta_end:]:
        if ln.startswith("#"):
            kept = 0
            out.append(ln)
        elif not ln.strip():
            if out and out[-1].strip():
                out.append(ln)
        elif kept < 3:
            out.append(ln)
            kept += 1
    marker = "> (gekuerzt durch trim; vollstaendige Fassung im Journal)\n"
    shortened = "\n".join(out).rstrip("\n") + "\n\n" + marker
    while _size(shortened) > limit:
        head = shortened[: len(shortened) - len(marker) - 1].rstrip("\n")
        head = head.rsplit("\n", 1)[0] if "\n" in head else head[: limit // 2]
        shortened = head + "\n\n" + marker
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
    text = path.read_text(encoding="utf-8")
    before = _size(text)
    new, moved, snapshot = trim_text(text, limit)
    if not moved and not snapshot:
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
                "````markdown",
                text.rstrip("\n"),
                "````",
            ],
            when,
        )
    path.write_text(new, encoding="utf-8", newline="\n")
    return TrimResult(before, _size(new), moved, snapshot)


def migrate(root: Path, *, when: datetime | None = None, remove_legacy: bool = False) -> Path:
    """Move a pre-3.3 ``state/current-session.md`` into the journal and seed ``now.md``.

    Writes ``journal/YYYY/MM/YYYY-MM-DD-migration.md`` containing the legacy file verbatim, seeds
    ``now.md`` from the legacy content when no ``now.md`` exists (then trims it), and only with
    ``remove_legacy`` deletes the legacy file after checking the journal holds it byte for byte.
    """
    when = when or datetime.now()
    legacy = legacy_session_path(root)
    content = legacy.read_text(encoding="utf-8")
    target = journal_dir(root) / f"{when:%Y}" / f"{when:%m}" / f"{when:%Y-%m-%d}-migration.md"
    if not target.exists():
        target.parent.mkdir(parents=True, exist_ok=True)
        header = (
            "---\n"
            f"id: j-{when:%Y-%m-%d}-migration\n"
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
            f"### {when:%H:%M} · notiz\n\n"
            "Inhalt von `state/current-session.md` vor der Migration, byte-genau:\n\n"
            "````markdown\n"
        )
        target.write_text(header + content + "````\n", encoding="utf-8", newline="\n")
    if content not in target.read_text(encoding="utf-8"):
        raise RuntimeError(f"{target} does not contain the legacy state; refusing to continue")
    npath = now_path(root)
    if not npath.exists():
        npath.write_text(content, encoding="utf-8", newline="\n")
        trim(root, session_id="migration", when=when, journal_file=target)
    if remove_legacy:
        legacy.unlink()
    return target

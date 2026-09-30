"""Monthly journal rollup ``journal/YYYY/MM/_rollup.md`` (generated, deterministic).

One line per session journal of the month plus every still open ``offen`` entry. The rollup is a
reading aid for the weekly maintenance and for consolidation; it is never loaded at boot and adds
nothing that is not in the journals. File names starting with ``_`` are skipped by
``journal.iter_journals``, so a rollup is never mistaken for a journal.
"""

from __future__ import annotations

import re
from collections import Counter
from pathlib import Path

from . import frontmatter
from .index import GENERATED
from .journal import iter_journals
from .workspace import journal_dir, rel, write_lf

ENTRY_HEAD = re.compile(r"^### (\d{2}:\d{2}) · (\w+)\s*$")


def _entries(body: str) -> list[tuple[str, str]]:
    """(kind, text) of every ``### HH:MM · kind`` entry."""
    out: list[tuple[str, str]] = []
    kind = ""
    buf: list[str] = []
    for line in body.split("\n"):
        m = ENTRY_HEAD.match(line)
        if m or line.startswith("## "):
            if kind:
                out.append((kind, "\n".join(buf).strip()))
            kind, buf = (m.group(2) if m else ""), []
        elif kind:
            buf.append(line)
    if kind:
        out.append((kind, "\n".join(buf).strip()))
    return out


def months(root: Path) -> list[str]:
    return sorted({f"{p.parent.parent.name}-{p.parent.name}" for p in iter_journals(root)})


def render(root: Path, month: str) -> str:
    year, mon = month.split("-")
    files = [p for p in iter_journals(root) if p.parent == journal_dir(root) / year / mon]
    lines = [GENERATED, f"# Journal-Rollup {month}", "", f"{len(files)} Journale.", ""]
    lines += ["## Sessions", ""]
    open_items: list[str] = []
    for p in files:
        meta, body = frontmatter.parse(p.read_text(encoding="utf-8"))
        meta = meta or {}
        entries = _entries(body)
        kinds = Counter(k for k, _ in entries)
        themen = meta.get("themen", [])
        themen_s = ", ".join(themen) if isinstance(themen, list) else themen
        done = str(meta.get("konsolidiert", "")).lower() == "true"
        lines.append(
            f"- [{p.name}]({p.name}) · {meta.get('tool', '?')} · "
            + ("konsolidiert" if done else "**offen**")
            + (f" · {themen_s}" if themen_s else "")
            + " · "
            + (", ".join(f"{k} {c}" for k, c in sorted(kinds.items())) or "leer")
        )
        if not done:
            for kind, text in entries:
                if kind == "offen" and text:
                    first = " ".join(text.split())[:160]
                    open_items.append(f"- {first} ([{p.name}]({p.name}))")
    lines += ["", "## Offene Punkte aus nicht konsolidierten Journalen", ""]
    lines += open_items or ["(keine)"]
    return "\n".join(lines) + "\n"


def write(root: Path, month: str | None = None) -> list[Path]:
    """(Re)write the rollup of ``month`` (default: every month with journals). Changed paths."""
    changed: list[Path] = []
    for m in [month] if month else months(root):
        year, mon = m.split("-")
        path = journal_dir(root) / year / mon / "_rollup.md"
        text = render(root, m)
        if not path.exists() or path.read_text(encoding="utf-8") != text:
            path.parent.mkdir(parents=True, exist_ok=True)
            write_lf(path, text)
            changed.append(path)
    return changed


def describe(root: Path, paths: list[Path]) -> str:
    return "\n".join(rel(root, p) for p in paths)

"""Consolidation helpers: journal entries -> notes (skill ``merken``, procedure in AGENTS.md §6).

The judgement (NOOP / ADD / UPDATE / SUPERSEDE / CONFLICT) is made by the model following the
skill; these helpers do the mechanical, error-prone parts deterministically and idempotently:

* ``pending``     finished journals that are not consolidated yet (oldest first)
* ``candidates``  existing notes that look like the new statement (token overlap, stdlib)
* ``supersede``   set both sides of a supersede chain (a second call changes nothing)
* ``confirm``     NOOP with confirmation: ``last_confirmed`` only
* ``conflict``    a pinned ``question`` note of kind ``conflict`` linking both statements (once)
* ``mark``        freeze a journal: ``konsolidiert: true`` + ``konsolidiert_zu: [ids]``
"""

from __future__ import annotations

import re
from collections.abc import Iterable
from dataclasses import dataclass
from datetime import date
from pathlib import Path

from . import frontmatter
from .create import skeleton
from .journal import is_frozen, iter_journals
from .notes import Note, load_notes
from .rollup import _entries
from .workspace import rel

CHANGE = {"veraendert", "korrigiert"}
STOPWORDS = set(
    "der die das und oder ein eine einer eines ist sind wird werden mit fuer von zu im in am an auf"
    " nicht nur auch als bei aus dem den des the a an of to and or is are for with on in".split()
)


# --- pending journals ----------------------------------------------------------------------------


@dataclass(frozen=True)
class Pending:
    path: Path
    entries: int
    kinds: tuple[str, ...]


def pending(
    root: Path,
    *,
    exclude: Iterable[Path] = (),
    today: str | None = None,
    include_running: bool = False,
) -> list[Pending]:
    """Unconsolidated journals with at least one entry, oldest first.

    By default only *finished* journals count: with a closing ``uebergabe`` entry (hook
    ``journal_stub``) or started before ``today``. A journal of a session that is still running
    in another worktree is left alone, so a parallel session never freezes it.
    """
    today = today or date.today().isoformat()
    skip = {p.resolve() for p in exclude}
    out: list[Pending] = []
    for p in iter_journals(root):
        if p.resolve() in skip:
            continue
        text = p.read_text(encoding="utf-8")
        if is_frozen(text):
            continue
        _, body = frontmatter.parse(text)
        entries = _entries(body)
        if not entries:
            continue
        finished = entries[-1][0] == "uebergabe" or p.name[:10] < today
        if finished or include_running:
            out.append(Pending(p, len(entries), tuple(sorted({k for k, _ in entries}))))
    return out


# --- similar notes -------------------------------------------------------------------------------


def _tokens(text: str) -> set[str]:
    words = re.findall(r"[a-z0-9äöüß]+", text.lower())
    return {w for w in words if len(w) > 2 and w not in STOPWORDS}


def candidates(root: Path, text: str, limit: int = 5) -> list[tuple[float, Note]]:
    """Notes ranked by Jaccard overlap of title/summary/aliases with ``text`` (score > 0)."""
    want = _tokens(text)
    scored: list[tuple[float, Note]] = []
    for n in load_notes(root):
        have = _tokens(" ".join([n.get("title"), n.get("summary"), *n.items("aliases")]))
        if want and have:
            score = len(want & have) / len(want | have)
            if score > 0:
                scored.append((round(score, 3), n))
    scored.sort(key=lambda s: (-s[0], s[1].id))
    return scored[:limit]


# --- note edits ----------------------------------------------------------------------------------


def find(root: Path, ref: str) -> Note:
    """A note by id or alias."""
    for n in load_notes(root):
        if n.id == ref or ref in n.items("aliases"):
            return n
    raise KeyError(f"no note with id or alias {ref!r}")


def _save(n: Note) -> bool:
    new = n.render()
    old = n.path.read_text(encoding="utf-8") if n.path.exists() else None
    if new == old:
        return False
    n.path.write_text(new, encoding="utf-8", newline="\n")
    return True


def _history(n: Note, line: str) -> None:
    """Append ``line`` to the ``## Verlauf`` section (created if missing), once."""
    if line in n.body:
        return
    body = n.body.rstrip("\n")
    if "\n## Verlauf" not in "\n" + body:
        body += "\n\n## Verlauf\n"
    n.body = body + f"\n{line}\n"


def supersede(root: Path, old_ref: str, new_ref: str, *, change: str, day: str) -> list[Path]:
    """Link ``new`` -> ``old`` symmetrically. Returns the files that changed (empty = no-op)."""
    if change not in CHANGE:
        raise ValueError(f"change must be one of {sorted(CHANGE)}")
    old, new = find(root, old_ref), find(root, new_ref)
    if old.id == new.id:
        raise ValueError("a note cannot supersede itself")
    if old.get("superseded_by") not in ("", new.id):
        raise ValueError(f"{old.id} is already superseded by {old.get('superseded_by')}")
    if new.get("superseded_by"):
        raise ValueError(f"{new.id} is itself superseded by {new.get('superseded_by')}")
    if new.get("change") and new.get("change") != change:
        raise ValueError(f"{new.id} already has change: {new.get('change')} (one value per note)")
    changed: list[Path] = []
    if old.id not in new.items("supersedes"):
        new.meta["supersedes"] = [*new.items("supersedes"), old.id]
        new.meta["change"] = change
        new.meta["updated"] = max(new.get("updated"), day)
        _history(new, f"- {day} · ersetzt {old.id} ({change})")
    if old.get("superseded_by") != new.id or old.get("status") != "superseded":
        old.meta.update(status="superseded", superseded_by=new.id)
        old.meta["valid_until"] = old.get("valid_until") or new.get("valid_from") or day
        old.meta["updated"] = max(old.get("updated"), day)
        _history(old, f"- {day} · abgeloest durch {new.id} ({change})")
    for n in (new, old):
        if _save(n):
            changed.append(n.path)
    return changed


def confirm(root: Path, ref: str, *, day: str) -> list[Path]:
    """NOOP with confirmation: set ``last_confirmed`` (never ``updated``: nothing changed)."""
    n = find(root, ref)
    if n.get("last_confirmed") >= day:
        return []
    n.meta["last_confirmed"] = day
    return [n.path] if _save(n) else []


def conflict(
    root: Path, a_ref: str, b_ref: str, *, title: str, source: str, day: str
) -> Path:
    """A pinned question note (kind conflict) that links two contradicting notes or aliases.

    Idempotent: an active conflict note for the same pair is returned instead of a second one.
    """
    a, b = find(root, a_ref), find(root, b_ref)
    if a.id == b.id:
        raise ValueError("a conflict needs two different notes")
    for n in load_notes(root):
        if (
            n.type == "question"
            and n.get("kind") == "conflict"
            and n.active
            and set(n.items("links")) == {a.id, b.id}
        ):
            return n.path
    note = skeleton(root, "question", title, source=source, day=day, kind="conflict")
    note.meta["links"] = [a.id, b.id]
    note.meta["pinned"] = "true"
    note.meta["confidence"] = "unbestaetigt"
    note.body = (
        "## Frage\n\n"
        f"Widerspruch zwischen `{a.id}` und `{b.id}`. Welche Aussage gilt?\n\n"
        f"## Belege\n\n- {source}\n\n## Verlauf\n\n- {day} · angelegt (CONFLICT)\n"
    )
    note.path.parent.mkdir(parents=True, exist_ok=True)
    with note.path.open("x", encoding="utf-8", newline="\n") as fh:
        fh.write(note.render())
    return note.path


def mark(root: Path, journal_path: Path, note_ids: list[str]) -> bool:
    """Freeze a journal after consolidation. Idempotent; ids or aliases must exist.

    Returns True if the journal changed.
    """
    notes = load_notes(root)
    by_ref = {n.id: n.id for n in notes} | {a: n.id for n in notes for a in n.items("aliases")}
    missing = [i for i in note_ids if i not in by_ref]
    if missing:
        raise KeyError("unknown note ids: " + ", ".join(missing))
    note_ids = [by_ref[i] for i in note_ids]
    text = journal_path.read_text(encoding="utf-8")
    meta, _ = frontmatter.parse(text)
    if meta is None:
        raise frontmatter.FrontmatterError(f"{rel(root, journal_path)} has no frontmatter")
    before = meta.get("konsolidiert_zu", [])
    ids = sorted(set(before if isinstance(before, list) else []) | set(note_ids))
    new = frontmatter.set_scalar(text, "konsolidiert", "true")
    raw, body = frontmatter.split(new)
    assert raw is not None
    line = "konsolidiert_zu: [" + ", ".join(ids) + "]"
    lines = [ln for ln in raw.split("\n") if not ln.startswith("konsolidiert_zu:")]
    at = next(i for i, ln in enumerate(lines) if ln.startswith("konsolidiert:")) + 1
    lines.insert(at, line)
    new = "---\n" + "\n".join(lines) + "\n---\n" + body
    if new == text:
        return False
    journal_path.write_text(new, encoding="utf-8", newline="\n")
    return True


def journal_refs(root: Path) -> list[tuple[Path, str]]:
    """(journal, note id) pairs from ``konsolidiert_zu`` whose note does not exist (for lint)."""
    known = {n.id for n in load_notes(root)}
    out: list[tuple[Path, str]] = []
    for p in iter_journals(root):
        meta, _ = frontmatter.parse(p.read_text(encoding="utf-8"))
        refs = (meta or {}).get("konsolidiert_zu", [])
        for ref in refs if isinstance(refs, list) else []:
            if ref not in known:
                out.append((p, ref))
    return out

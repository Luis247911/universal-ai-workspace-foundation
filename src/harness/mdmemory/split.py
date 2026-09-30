"""Migration of the four legacy registers into atomic notes, and the way back.

``split`` (CLI ``split-decisions``) does, per register, in this order:

1. copy the register byte for byte to ``archive/<datum>/state-<datei>`` (never overwritten; an
   existing copy must be identical),
2. convert every entry to a note and check the round trip ``entry -> note -> entry`` before
   anything is written,
3. write the notes that do not exist yet (matched by id and by legacy alias -> idempotent),
4. regenerate the index and the register views (the registers become generated views).

A register that is already a generated view (it carries the GENERIERT marker) is skipped, so a
second run is a no-op.
``export_legacy`` renders the old full format from the notes again (for tools that need it).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

from . import frontmatter
from . import index as index_mod
from .legacy import (
    REGISTERS,
    Entry,
    Register,
    entry_from_note,
    normalize,
    parse_register,
    render_entry,
    to_notes,
)
from .notes import Note, load_notes
from .workspace import state_dir, write_lf, ws

KEY_ORDER: dict[str, list[str]] = {
    "decisions": [
        "ID",
        "Datum",
        "Entscheidung",
        "Begruendung",
        "Status",
        "Reversibilitaet",
        "Follow-up-Date",
        "Supersedes",
    ],
    "open-questions": [
        "ID",
        "Frage",
        "raised-by",
        "raised-date",
        "blockiert-Decision",
        "Research-Status",
        "Resolution-Datum",
    ],
    "assumptions": [
        "ID",
        "Annahme",
        "Confidence",
        "Abhaengige Decisions",
        "Invalidierungs-Trigger",
        "Status",
    ],
    "risks-and-constraints": [
        "ID",
        "Risiko",
        "Severity",
        "Probability",
        "Mitigation",
        "Owner",
        "Review-Date",
        "Constraint",
        "Quelle",
        "Konsequenz bei Verletzung",
    ],
}


class RoundTripError(RuntimeError):
    """An entry would not survive entry -> note -> entry; nothing was written."""


@dataclass
class SplitResult:
    register: str
    entries: int = 0
    written: list[Path] = field(default_factory=list)
    skipped: int = 0
    archived: Path | None = None


def archive_path(root: Path, reg: Register, day: str) -> Path:
    return ws(root) / "archive" / day / f"state-{reg.file}"


def _archive(root: Path, reg: Register, day: str) -> Path:
    src = state_dir(root) / reg.file
    dst = archive_path(root, reg, day)
    data = src.read_bytes()
    if dst.exists():
        if dst.read_bytes() != data:
            raise RuntimeError(f"{dst} exists with different content; refusing to overwrite")
        return dst
    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_bytes(data)
    return dst


def _zip_same(a: list, b: list) -> list:
    """``zip(..., strict=True)`` for Python 3.9."""
    if len(a) != len(b):
        raise ValueError(f"length mismatch: {len(a)} entries, {len(b)} notes")
    return list(zip(a, b))  # noqa: B905 (strict= needs Python 3.10)


def id_to_alias(notes: list[Note]) -> dict[str, str]:
    return {n.id: n.items("aliases")[0] for n in notes if n.items("aliases")}


def check_round_trip(reg: Register, entries: list[Entry], notes: list[Note]) -> None:
    """Raise if any entry changes on the way entry -> rendered note -> entry."""
    back_map = id_to_alias(notes)
    for entry, note in _zip_same(entries, notes):
        meta, body = frontmatter.parse(note.render())
        back = entry_from_note(reg, Note(note.path, meta or {}, body), back_map)
        if normalize(back) != normalize(entry):
            raise RoundTripError(f"{reg.file}: entry {entry.get('ID', '?')} would change")


def split(root: Path, day: str, only: list[str] | None = None) -> list[SplitResult]:
    existing = load_notes(root)
    known = {n.id for n in existing} | {a for n in existing for a in n.items("aliases")}
    results: list[SplitResult] = []
    for name, reg in REGISTERS.items():
        if only and name not in only:
            continue
        res = SplitResult(name)
        results.append(res)
        path = state_dir(root) / reg.file
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8")
        if index_mod.GENERATED in text:  # already a generated view
            continue
        res.archived = _archive(root, reg, day)  # also empty registers: the view replaces them
        entries = parse_register(text)
        res.entries = len(entries)
        notes = to_notes(root, reg, entries, day)
        check_round_trip(reg, entries, notes)
        for entry, note in _zip_same(entries, notes):
            alias = entry.get("ID", "")
            if note.id in known or (alias and alias in known) or note.path.exists():
                res.skipped += 1
                continue
            note.path.parent.mkdir(parents=True, exist_ok=True)
            write_lf(note.path, note.render())
            res.written.append(note.path)
    if any(r.archived for r in results):
        index_mod.write(root)
    return results


def export_legacy(root: Path, name: str) -> str:
    """The old full format of one register, rebuilt from the notes (newest first)."""
    reg = REGISTERS[name]
    _, _, pred, _ = index_mod.VIEWS[reg.file]
    notes = load_notes(root)
    back_map = id_to_alias(notes)
    selected = sorted(
        [n for n in notes if pred(n)],
        key=lambda n: (n.get("valid_from"), n.items("aliases")[:1], n.id),
        reverse=True,
    )
    blocks = [render_entry(entry_from_note(reg, n, back_map), KEY_ORDER[name]) for n in selected]
    head = f"# {reg.file} (Export aus den Notizen, nicht kanonisch)\n\n"
    return head + "\n\n".join(blocks) + ("\n" if blocks else "(keine Eintraege)\n")

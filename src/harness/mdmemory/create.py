"""Skeleton for a new note (``python -m harness.mdmemory new <typ> "<titel>"``).

Fills every schema key so the note lints right away once the body is written.

The id is ``<prefix>-<date>-<slug>-<4 hex>``. The random suffix keeps two worktrees that create a
note with a similar title on the same day from producing the same file (add/add conflict). For
the same reason no counter-based alias (``D-YYYY-MM-DD-NN``) is assigned automatically: two
parallel sessions would both take the next number. ``alias`` sets one explicitly; lint rejects
duplicates.
"""

from __future__ import annotations

import re
import secrets
from datetime import date
from pathlib import Path

from .limits import SUMMARY_MAX_CHARS
from .notes import (
    ENUMS,
    PREFIX,
    TYPES,
    Note,
    field_order,
    first_sentence,
    load_notes,
    note_path,
    slugify,
)

TYPE_DEFAULTS: dict[str, dict[str, str | list[str]]] = {
    "person": {"relation": "", "context": "arbeit", "sensitivity": "personal"},
    "preference": {"applies_to": "project"},
    "project": {"phase": "", "external_ref": ""},
    "decision": {"alternatives": [], "reversibility": "reversible", "decided_by": ""},
    "question": {"kind": "question", "blocks": [], "resolution": ""},
}
BODY = {
    "decision": ["Entscheidung", "Begruendung", "Belege", "Verlauf"],
    "question": ["Frage", "Belege", "Verlauf"],
}


def next_decision_alias(notes: list[Note], day: str) -> str:
    """Next free ``D-<day>-NN`` in this worktree (only safe without parallel sessions)."""
    pat = re.compile(rf"^D-{re.escape(day)}-(\d+)$")
    nums = [int(m.group(1)) for n in notes for a in n.items("aliases") if (m := pat.match(a))]
    return f"D-{day}-{max(nums, default=0) + 1:02d}"


def skeleton(
    root: Path,
    note_type: str,
    title: str,
    *,
    source: str,
    summary: str = "",
    day: str | None = None,
    alias: str = "",
    kind: str = "",
    suffix: str | None = None,
) -> Note:
    if note_type not in TYPES:
        raise ValueError(f"unknown type {note_type!r}")
    day = day or date.today().isoformat()
    suffix = suffix or secrets.token_hex(2)
    note_id = f"{PREFIX[note_type]}-{day}-{slugify(title, 40)}-{suffix}"
    meta: dict[str, str | list[str]] = {k: "" for k in field_order(note_type)}
    meta.update(
        {
            "id": note_id,
            "type": note_type,
            "title": title,
            "summary": summary or first_sentence(title, SUMMARY_MAX_CHARS),
            "aliases": [alias] if alias else [],
            "status": "active",
            "valid_from": day,
            "supersedes": [],
            "confidence": "bestaetigt",
            "sources": [source],
            "links": [],
            "scope": "project",
            "sensitivity": "normal",
            "origin": "internal",
            "pinned": "false",
            "updated": day,
            "last_confirmed": day,
        }
    )
    meta.update(TYPE_DEFAULTS.get(note_type, {}))
    if kind:
        if note_type != "question" or kind not in ENUMS["kind"]:
            raise ValueError(f"--kind needs type question and one of {sorted(ENUMS['kind'])}")
        meta["kind"] = kind
    heads = BODY.get(note_type, ["Inhalt", "Belege", "Verlauf"])
    body_lines: list[str] = []
    for h in heads:
        text = f"- {day} · angelegt" if h == "Verlauf" else f"<{h.lower()}>"
        body_lines += [f"## {h}", "", text, ""]
    return Note(note_path(root, note_type, note_id), meta, "\n".join(body_lines))


def create(root: Path, note_type: str, title: str, **kw: str) -> Path:
    if kw.get("alias") == "auto":
        day = kw.get("day") or date.today().isoformat()
        kw["alias"] = next_decision_alias(load_notes(root), day)
    note = skeleton(root, note_type, title, **kw)
    note.path.parent.mkdir(parents=True, exist_ok=True)
    with note.path.open("x", encoding="utf-8", newline="\n") as fh:
        fh.write(note.render())
    return note.path

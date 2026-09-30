"""Legacy registers in ``state/`` <-> atomic notes, losslessly.

The four pre-3.3 registers (``decisions.md``, ``open-questions.md``, ``assumptions.md``,
``risks-and-constraints.md``) hold entries as ``- Key: value`` blocks. ``parse_register`` reads
them, ``to_notes`` turns each entry into one note (legacy ID -> ``aliases``), and
``entry_from_note`` rebuilds the original key/value pairs from a note. The round-trip test
checks ``parse -> to_notes -> entry_from_note`` returns the same pairs for every entry.

Keys that map onto schema fields go to the frontmatter; every other key becomes a ``## <Key>``
body section with its text unchanged. A value that does not fit its schema field (unknown status,
malformed date, unresolvable Supersedes) also stays a body section, so nothing is lost.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path

from .limits import SUMMARY_MAX_CHARS
from .notes import DATE_RE, PREFIX, SCHEMA_SECTIONS, Note, body_sections, first_sentence, slugify
from .workspace import knowledge_dir, state_dir

REVERSIBILITY = {"", "reversible", "hard-to-reverse", "irreversible"}
ENTRY_START = re.compile(r"^- (ID|Constraint):\s?")
KV = re.compile(r"^- ([A-Za-z][\w-]*):\s?(.*)$")


@dataclass(frozen=True)
class Register:
    name: str
    file: str
    kind: str | None  # question kind; None for decisions
    title_keys: tuple[str, ...]
    fields: dict[str, str]  # legacy key -> schema field
    status_map: dict[str, str] = field(default_factory=dict)  # legacy value -> schema status

    @property
    def note_type(self) -> str:
        return "decision" if self.kind is None else "question"


REGISTERS = {
    "decisions": Register(
        "decisions",
        "decisions.md",
        None,
        ("Entscheidung",),
        {
            "ID": "aliases",
            "Datum": "valid_from",
            "Status": "status",
            "Reversibilitaet": "reversibility",
            "Follow-up-Date": "review_after",
            "Supersedes": "supersedes",
        },
        {"active": "active", "superseded": "superseded"},
    ),
    "open-questions": Register(
        "open-questions",
        "open-questions.md",
        "question",
        ("Frage",),
        {"ID": "aliases", "raised-date": "valid_from", "blockiert-Decision": "blocks"},
    ),
    "assumptions": Register(
        "assumptions",
        "assumptions.md",
        "assumption",
        ("Annahme",),
        {"ID": "aliases", "Status": "status"},
        {"active": "active", "invalidated": "retracted"},
    ),
    "risks-and-constraints": Register(
        "risks-and-constraints",
        "risks-and-constraints.md",
        "risk",
        ("Risiko", "Constraint"),
        {"ID": "aliases", "Review-Date": "review_after"},
    ),
}


Entry = dict[str, str]


def _entries_region(text: str) -> list[str]:
    """Lines outside fenced code blocks, ``## Format…`` sections and the Cross-Links section."""
    out, fenced, skip = [], False, False
    for line in text.replace("\r\n", "\n").split("\n"):
        if line.startswith("```"):
            fenced = not fenced
            continue
        if fenced:
            continue
        if line.startswith("## Cross-Links"):
            break
        if line.startswith("## "):
            skip = line[3:].strip().startswith("Format")
        if not skip:
            out.append(line)
    return out


def parse_register(text: str) -> list[Entry]:
    """All ``- Key: value`` entry blocks (starting with ``- ID:`` or ``- Constraint:``)."""
    entries: list[Entry] = []
    current: Entry | None = None
    last_key = ""
    for line in _entries_region(text):
        if ENTRY_START.match(line):
            current = {}
            entries.append(current)
        if current is None:
            continue
        if not line.strip() or line.startswith("#"):
            current, last_key = None, ""
            continue
        m = KV.match(line)
        if m:
            last_key = m.group(1)
            current[last_key] = m.group(2).strip()
        elif last_key:  # continuation line of a multi-line value
            current[last_key] += "\n" + line.rstrip()
    return entries


def _kind(reg: Register, entry: Entry) -> str | None:
    if reg.name == "risks-and-constraints" and "Constraint" in entry and "ID" not in entry:
        return "constraint"
    return reg.kind


def _title_text(reg: Register, entry: Entry) -> str:
    for key in reg.title_keys:
        if entry.get(key):
            return entry[key]
    return entry.get("ID", "Eintrag")


def to_notes(root: Path, reg: Register, entries: list[Entry], migrated_on: str) -> list[Note]:
    """Convert entries to notes (paths are set but nothing is written)."""
    alias_to_id: dict[str, str] = {}
    drafts: list[tuple[Entry, dict, dict[str, str]]] = []
    used_titles: set[str] = set()
    for n, entry in enumerate(entries, start=1):
        legacy_id = entry.get("ID", "")
        m = re.match(r"^[A-Z]-(\d{4}-\d{2}-\d{2})-(\w+)$", legacy_id)
        date = entry.get(_date_key(reg), "")
        day = m.group(1) if m else (date if DATE_RE.match(date) else migrated_on)
        seq = m.group(2).lower() if m else f"c{n:02d}"
        text = _title_text(reg, entry)
        title = first_sentence(text, 80)
        if title.lower() in used_titles:
            title = f"{title} ({legacy_id or seq})"
        used_titles.add(title.lower())
        note_id = f"{PREFIX[reg.note_type]}-{day}-{seq}-{slugify(title, 32)}"
        alias_to_id[legacy_id] = note_id
        meta: dict = {"id": note_id, "type": reg.note_type, "title": title}
        meta["summary"] = first_sentence(text, SUMMARY_MAX_CHARS)
        sections: dict[str, str] = {}
        mapped: list[str] = []
        for key, value in entry.items():
            target = reg.fields.get(key)
            ok = "\n" not in value  # frontmatter values are single-line; else keep as a section
            if not ok:
                sections[key] = value
            elif target == "aliases":
                meta["aliases"] = [value] if value else []
            elif target == "status" and value in reg.status_map:
                meta["status"] = reg.status_map[value]
            elif target in {"valid_from", "review_after"} and (not value or DATE_RE.match(value)):
                meta[target] = value
            elif target == "reversibility" and value in REVERSIBILITY:
                meta[target] = value
            elif target in {"supersedes", "blocks"}:
                meta[target] = [v.strip() for v in value.split(",") if v.strip()]
            else:
                ok = False
                sections[key] = value
            if ok:
                mapped.append(key)
        meta["legacy_keys"] = mapped
        drafts.append((entry, meta, sections))

    notes: list[Note] = []
    by_id: dict[str, dict] = {}
    for entry, meta, sections in drafts:
        legacy_sup = meta.pop("supersedes", [])
        resolved = [alias_to_id[a] for a in legacy_sup if a in alias_to_id]
        if len(resolved) != len(legacy_sup):  # unresolvable -> keep verbatim as a section
            sections["Supersedes"] = entry.get("Supersedes", "")
            meta["legacy_keys"].remove("Supersedes")
            resolved = []
        meta["supersedes"] = resolved
        meta.setdefault("aliases", [])
        meta.setdefault("status", "active")
        if not meta.get("valid_from"):
            meta["valid_from"] = migrated_on
        base = {
            "valid_until": "",
            "superseded_by": "",
            "change": "",
            "confidence": "bestaetigt",
            "sources": [f"legacy:state/{reg.file}#{entry.get('ID') or meta['id']}"],
            "links": [],
            "scope": "project",
            "sensitivity": "normal",
            "origin": "internal",
            "pinned": "false",
            "updated": meta["valid_from"],
            "last_confirmed": meta["valid_from"],
            "review_after": meta.get("review_after", ""),
        }
        for k, v in base.items():
            meta.setdefault(k, v)
        if reg.note_type == "decision":
            meta.setdefault("alternatives", [])
            meta.setdefault("reversibility", "")
            meta["decided_by"] = ""
        else:
            meta["kind"] = _kind(reg, entry) or "question"
            meta.setdefault("blocks", [])
            meta["resolution"] = ""
        body = [f"Migriert aus `state/{reg.file}` am {migrated_on}.", ""]
        for key, value in sections.items():
            body += [f"## {key}", "", value, ""]
        body += [
            "## Verlauf",
            "",
            f"- {migrated_on} · migriert aus `state/{reg.file}`"
            + (f" (Alt-ID {entry['ID']})" if entry.get("ID") else ""),
            "",
        ]
        path = knowledge_dir(root) / reg.note_type / f"{meta['id']}.md"
        notes.append(Note(path, meta, "\n".join(body)))
        by_id[meta["id"]] = meta
    for meta in by_id.values():  # symmetric supersede chain
        for old in meta["supersedes"]:
            by_id[old]["superseded_by"] = meta["id"]
            if not by_id[old]["valid_until"]:
                by_id[old]["valid_until"] = meta["valid_from"]
            by_id[old]["updated"] = max(by_id[old]["updated"], meta["valid_from"])
    return notes


def _date_key(reg: Register) -> str:
    return next((k for k, v in reg.fields.items() if v == "valid_from"), "")


def entry_from_note(reg: Register, note: Note, id_to_alias: dict[str, str]) -> Entry:
    """Rebuild the legacy key/value pairs of one note (inverse of ``to_notes``)."""
    entry: Entry = {}
    rev_status = {v: k for k, v in reg.status_map.items()}
    for key in note.items("legacy_keys"):
        target = reg.fields.get(key, "")
        if target == "aliases":
            aliases = note.items("aliases")
            entry[key] = aliases[0] if aliases else ""
        elif target == "status":
            entry[key] = rev_status.get(note.get("status"), note.get("status"))
        elif target == "supersedes":
            entry[key] = ", ".join(id_to_alias.get(i, i) for i in note.items("supersedes"))
        elif target == "blocks":
            entry[key] = ", ".join(note.items("blocks"))
        elif target:
            entry[key] = note.get(target)
    for heading, text in body_sections(note.body).items():
        if heading and heading not in SCHEMA_SECTIONS:
            entry[heading] = text
    return entry


def normalize(entry: Entry) -> Entry:
    """Comparison form: stripped values, empty values dropped."""
    return {k: "\n".join(ln.rstrip() for ln in v.strip().split("\n")) for k, v in entry.items()
            if v.strip()}


def render_entry(entry: Entry, order: list[str]) -> str:
    keys = [k for k in order if k in entry] + [k for k in entry if k not in order]
    return "\n".join(f"- {k}: {entry[k]}".rstrip() for k in keys)


def read_register(root: Path, reg: Register) -> list[Entry]:
    path = state_dir(root) / reg.file
    if not path.exists():
        return []
    return parse_register(path.read_text(encoding="utf-8"))

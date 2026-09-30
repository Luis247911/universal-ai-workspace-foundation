"""Atomic notes under ``knowledge/<typ>/<id>.md``: schema, loading, ids, slugs.

The schema (field names, enums, required keys) lives here and nowhere else; ``lint`` checks it,
``index`` renders from it, ``templates/knowledge-note.md`` documents it for humans.
"""

from __future__ import annotations

import re
import unicodedata
from dataclasses import dataclass
from pathlib import Path

from . import frontmatter
from .workspace import knowledge_dir

TYPES = ("person", "preference", "project", "decision", "reference", "concept", "question")
PREFIX = {
    "person": "per",
    "preference": "pref",
    "project": "proj",
    "decision": "dec",
    "reference": "ref",
    "concept": "con",
    "question": "q",
}

COMMON_FIELDS = [
    "id",
    "type",
    "title",
    "summary",
    "aliases",
    "status",
    "valid_from",
    "valid_until",
    "supersedes",
    "superseded_by",
    "change",
    "confidence",
    "sources",
    "links",
    "scope",
    "sensitivity",
    "origin",
    "pinned",
    "updated",
    "last_confirmed",
    "review_after",
]
TYPE_FIELDS: dict[str, list[str]] = {
    "person": ["relation", "context"],
    "preference": ["applies_to"],
    "project": ["phase", "external_ref"],
    "decision": ["alternatives", "reversibility", "decided_by"],
    "reference": [],
    "concept": [],
    "question": ["kind", "blocks", "resolution"],
}
LIST_FIELDS = {"aliases", "supersedes", "sources", "links", "alternatives", "blocks"}
DATE_FIELDS = {"valid_from", "valid_until", "updated", "last_confirmed", "review_after"}
ENUMS: dict[str, set[str]] = {
    "status": {"active", "superseded", "retracted", "archived"},
    "change": {"", "veraendert", "korrigiert"},
    "confidence": {"bestaetigt", "unbestaetigt"},
    "scope": {"project", "global"},
    "sensitivity": {"normal", "personal", "restricted"},
    "origin": {"internal", "external"},
    "pinned": {"true", "false"},
    "context": {"arbeit", "privat"},
    "reversibility": {"", "reversible", "hard-to-reverse", "irreversible"},
    "kind": {"question", "assumption", "risk", "constraint", "conflict"},
    "applies_to": {"tool", "project", "global"},
}
SCHEMA_SECTIONS = {"Belege", "Verlauf", "Beziehungen"}
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
ID_RE = re.compile(r"^(per|pref|proj|dec|ref|con|q)-\d{4}-\d{2}-\d{2}-[a-z0-9]+(-[a-z0-9]+)*$")
SOURCE_RE = re.compile(r"^(journal|url|legacy|automemory|system|note|user):\S+$")


def field_order(note_type: str) -> list[str]:
    return COMMON_FIELDS + TYPE_FIELDS.get(note_type, [])


@dataclass
class Note:
    path: Path
    meta: frontmatter.Meta
    body: str

    def get(self, key: str) -> str:
        val = self.meta.get(key, "")
        return val if isinstance(val, str) else ", ".join(val)

    def items(self, key: str) -> list[str]:
        val = self.meta.get(key, [])
        if isinstance(val, list):
            return val
        return [v.strip() for v in val.split(",") if v.strip()] if val else []

    @property
    def id(self) -> str:
        return self.get("id")

    @property
    def type(self) -> str:
        return self.get("type")

    @property
    def active(self) -> bool:
        return self.get("status") == "active"

    @property
    def pinned(self) -> bool:
        if self.get("pinned") == "true":
            return True
        return self.type == "question" and self.get("kind") == "conflict" and self.active

    @property
    def sensitive(self) -> bool:
        """True if title/summary must stay out of every generated index."""
        return self.get("sensitivity") in {"personal", "restricted"} or self.get(
            "origin"
        ) == "external"

    def render(self) -> str:
        return frontmatter.dump(self.meta, self.body, order=field_order(self.type))


def load_note(path: Path) -> Note:
    try:
        meta, body = frontmatter.parse(path.read_text(encoding="utf-8"))
    except (frontmatter.FrontmatterError, UnicodeDecodeError) as exc:
        raise frontmatter.FrontmatterError(f"{path.as_posix()}: {exc}") from exc
    return Note(path, meta or {}, body)


def note_files(root: Path) -> list[Path]:
    base = knowledge_dir(root)
    out: list[Path] = []
    for t in TYPES:
        d = base / t
        if d.is_dir():
            out.extend(sorted(p for p in d.glob("*.md") if p.name != "README.md"))
    return out


def load_notes(root: Path) -> list[Note]:
    return [load_note(p) for p in note_files(root)]


def slugify(text: str, max_len: int = 40) -> str:
    """ASCII kebab-case slug (umlauts transliterated), cut at a hyphen near ``max_len``."""
    text = text.replace("ä", "ae").replace("ö", "oe").replace("ü", "ue").replace("ß", "ss")
    text = text.replace("Ä", "Ae").replace("Ö", "Oe").replace("Ü", "Ue")
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("ascii")
    slug = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    if len(slug) > max_len:
        cut = slug[:max_len]
        slug = cut.rsplit("-", 1)[0] if "-" in cut else cut
    return slug or "notiz"


def first_sentence(text: str, max_len: int) -> str:
    """First sentence of ``text`` without Markdown emphasis, cut at a word near ``max_len``."""
    flat = " ".join(text.split())
    flat = re.sub(r"https?://\S+", "", flat)
    flat = flat.replace("**", "").replace("`", "")
    m = re.search(r"(?<=[.!?])\s", flat)
    sent = flat[: m.start()] if m else flat
    sent = sent.strip().rstrip(".")
    if len(sent) > max_len:
        sent = sent[: max_len - 1].rsplit(" ", 1)[0].rstrip(",;:") + "…"
    return sent


def body_sections(body: str) -> dict[str, str]:
    """``## Heading`` -> text (stripped), in file order. Text before the first heading is ''."""
    out: dict[str, str] = {}
    current = ""
    buf: list[str] = []
    for line in body.split("\n"):
        if line.startswith("## "):
            out[current] = "\n".join(buf).strip()
            current, buf = line[3:].strip(), []
        else:
            buf.append(line)
    out[current] = "\n".join(buf).strip()
    return out


def note_path(root: Path, note_type: str, note_id: str) -> Path:
    return knowledge_dir(root) / note_type / f"{note_id}.md"

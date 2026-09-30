"""Lint the atomic notes and the generated files. Errors fail CI, warnings are reported only.

Checks (E = error, W = warning):

* E schema: parseable frontmatter, every schema key present, no unknown keys (``legacy_keys`` is
  allowed for migrated notes), enums, dates, type == folder, id == file name with the type prefix
* E required values: title, summary, status, valid_from, updated, at least one ``sources`` entry
  of the form ``<kind>:<ref>``
* E summary: <= 120 characters, one line, no URL, no prompt-injection phrase (security-policy §2)
* E supersede chain: targets exist, both sides point at each other, ``status: superseded`` exactly
  when ``superseded_by`` is set, no cycles
* E at most one active note per type and title; aliases unique; links/blocks resolve
* E generated files (INDEX, sub indexes, register views) are up to date
* E/W boot budget: hard limit is an error, above target a warning
* E ``@path`` tokens in title/summary/aliases (Claude Code imports them from the boot index);
  INDEX.md above its byte/line cap
* W person note with ``sensitivity: normal``; sensitive note with a speaking id; active note past
  ``review_after``
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import date
from pathlib import Path

from . import budget, frontmatter
from . import index as index_mod
from .limits import INDEX_MAX_BYTES, INDEX_MAX_LINES, SUMMARY_MAX_CHARS
from .notes import (
    DATE_FIELDS,
    DATE_RE,
    ENUMS,
    ID_RE,
    LIST_FIELDS,
    PREFIX,
    SOURCE_RE,
    TYPES,
    Note,
    field_order,
    load_note,
    note_files,
)
from .workspace import rel

EXTRA_ALLOWED = {"legacy_keys"}
NONEMPTY = ("id", "type", "title", "summary", "status", "valid_from", "updated")
TITLE_MAX_CHARS = 100
ALIAS_MAX_CHARS = 60
AT_RE = re.compile(r"(^|\s)@\S")
NEUTRAL_ID_RE = re.compile(r"^[a-z]{3}-\d{4}-\d{2}-\d{2}-[0-9a-f]{4,8}$")
URL_RE = re.compile(r"https?://|www\.", re.I)
INJECTION_RE = re.compile(
    r"ignore (all )?previous instructions|vergiss (alle )?vorherigen? anweisungen"
    r"|aendere deine rolle|ändere deine rolle|du bist jetzt|you are now|system prompt",
    re.I,
)


@dataclass(frozen=True)
class Finding:
    level: str  # "E" or "W"
    path: str
    message: str

    def __str__(self) -> str:
        return f"{self.level} {self.path}: {self.message}"


def _check_note(root: Path, n: Note) -> list[Finding]:
    out: list[Finding] = []
    where = rel(root, n.path)

    def err(msg: str) -> None:
        out.append(Finding("E", where, msg))

    t = n.type
    if t not in TYPES:
        err(f"type {t!r} unknown (allowed: {', '.join(TYPES)})")
        return out
    if n.path.parent.name != t:
        err(f"type {t} but stored in folder {n.path.parent.name}/")
    order = field_order(t)
    missing = [k for k in order if k not in n.meta]
    if missing:
        err("missing keys: " + ", ".join(missing))
    unknown = sorted(k for k in n.meta if k not in order and k not in EXTRA_ALLOWED)
    if unknown:
        err("unknown keys: " + ", ".join(unknown))
    for k in NONEMPTY:
        if k in n.meta and not n.get(k):
            err(f"{k} is empty")
    if not ID_RE.match(n.id) or not n.id.startswith(PREFIX[t] + "-"):
        err(f"id {n.id!r} must look like {PREFIX[t]}-YYYY-MM-DD-<slug>")
    if n.id != n.path.stem:
        err(f"id {n.id!r} differs from file name {n.path.name}")
    for k, allowed in ENUMS.items():
        if k in n.meta and k in order and n.get(k) not in allowed:
            err(f"{k}={n.get(k)!r} not in {sorted(allowed)}")
    for k in DATE_FIELDS:
        v = n.get(k)
        if v and not DATE_RE.match(v):
            err(f"{k}={v!r} is not YYYY-MM-DD")
    for k in LIST_FIELDS & set(order):
        if k in n.meta and not isinstance(n.meta[k], list):
            err(f"{k} must be a list [..]")
    srcs = n.items("sources")
    if not srcs:
        err("sources is empty (every note needs at least one source)")
    for s in srcs:
        if not SOURCE_RE.match(s):
            err(f"source {s!r} needs a kind: journal|url|legacy|automemory|system|note|user")
    summary = n.get("summary")
    if len(summary) > SUMMARY_MAX_CHARS:
        err(f"summary has {len(summary)} > {SUMMARY_MAX_CHARS} characters")
    if URL_RE.search(summary):
        err("summary contains a URL (put it into sources)")
    for k in ("title", "summary"):
        if INJECTION_RE.search(n.get(k)):
            err(f"{k} contains a prompt-injection phrase (security-policy §2)")
    for k in ("title", "summary"):
        if AT_RE.search(n.get(k)):
            err(f"{k} contains an @path token (Claude Code would import it from the boot index)")
    for a in n.items("aliases"):
        if AT_RE.search(a) or len(a) > ALIAS_MAX_CHARS:
            err(f"alias {a[:50]!r} needs <= {ALIAS_MAX_CHARS} characters and no @path token")
    if n.get("sensitivity") in {"personal", "restricted"} and not NEUTRAL_ID_RE.match(n.id):
        out.append(
            Finding("W", where, "sensitive note with a speaking id (the id is shown in indexes)")
        )
    if len(n.get("title")) > TITLE_MAX_CHARS:
        err(f"title has more than {TITLE_MAX_CHARS} characters")
    if bool(n.get("superseded_by")) != (n.get("status") == "superseded"):
        err("status superseded and superseded_by must be set together")
    if t == "person" and n.get("sensitivity") == "normal":
        out.append(Finding("W", where, "person note with sensitivity normal (personal expected)"))
    return out


def _check_graph(root: Path, notes: list[Note], today: str) -> list[Finding]:
    out: list[Finding] = []
    by_id = {n.id: n for n in notes}
    aliases: dict[str, str] = {}
    for n in notes:
        for a in n.items("aliases"):
            if a in aliases or a in by_id:
                out.append(Finding("E", rel(root, n.path), f"alias {a!r} used twice"))
            aliases[a] = n.id
    known = set(by_id) | set(aliases)
    titles: dict[tuple[str, str], str] = {}
    for n in notes:
        where = rel(root, n.path)
        if n.active:
            key = (n.type, n.get("title").strip().lower())
            if key in titles:
                out.append(Finding("E", where, f"second active note with title of {titles[key]}"))
            titles[key] = n.id
        for old in n.items("supersedes"):
            if old not in by_id:
                out.append(Finding("E", where, f"supersedes unknown note {old}"))
            elif by_id[old].get("superseded_by") != n.id:
                out.append(Finding("E", where, f"{old} does not point back (superseded_by)"))
        new = n.get("superseded_by")
        if new:
            if new not in by_id:
                out.append(Finding("E", where, f"superseded_by unknown note {new}"))
            elif n.id not in by_id[new].items("supersedes"):
                out.append(Finding("E", where, f"{new} does not list this note in supersedes"))
        for k in ("links", "blocks"):
            for ref in n.items(k):
                if ref not in known:
                    out.append(Finding("E", where, f"{k}: unknown note or alias {ref}"))
        ra = n.get("review_after")
        if n.active and ra and DATE_RE.match(ra) and ra < today:
            out.append(Finding("W", where, f"review_after {ra} has passed"))
    for n in notes:  # cycles along superseded_by
        seen, cur = {n.id}, n.get("superseded_by")
        while cur and cur in by_id:
            if cur in seen:
                out.append(Finding("E", rel(root, n.path), "supersede chain has a cycle"))
                break
            seen.add(cur)
            cur = by_id[cur].get("superseded_by")
    return out


def run(root: Path, *, today: str | None = None, check_budget: bool = True) -> list[Finding]:
    today = today or date.today().isoformat()
    out: list[Finding] = []
    notes: list[Note] = []
    for path in note_files(root):
        try:
            n = load_note(path)
        except (frontmatter.FrontmatterError, UnicodeDecodeError) as exc:
            out.append(Finding("E", rel(root, path), f"frontmatter: {exc}"))
            continue
        if not n.meta:
            out.append(Finding("E", rel(root, path), "no frontmatter"))
            continue
        notes.append(n)
        out += _check_note(root, n)
    out += _check_graph(root, notes, today)
    index_file = root / ".ai-workspace" / "knowledge" / "INDEX.md"
    if index_file.exists():
        data = index_file.read_bytes()
        if len(data) > INDEX_MAX_BYTES or data.count(b"\n") > INDEX_MAX_LINES:
            out.append(
                Finding("E", rel(root, index_file), f"larger than {INDEX_MAX_BYTES} B / lines")
            )
    if not any(f.level == "E" for f in out):
        for p in index_mod.stale(root):
            out.append(
                Finding("E", rel(root, p), "generated file out of date: run mdmemory index")
            )
    if check_budget:
        rep = budget.measure(root)
        if rep.actual > rep.hard or rep.worst_case > rep.hard:
            out.append(Finding("E", "boot", rep.line()))
        elif rep.actual > rep.target:
            out.append(Finding("W", "boot", rep.line()))
    return out


def has_errors(findings: list[Finding]) -> bool:
    return any(f.level == "E" for f in findings)

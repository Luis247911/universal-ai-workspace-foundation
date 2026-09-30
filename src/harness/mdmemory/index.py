"""Generated, tiered index and register views.

Everything here is *derived* from the notes (D-2026-09-30-05): regenerating twice gives no diff.
There are no clocks in the output, only dates taken from the notes.

    knowledge/INDEX.md              boot index: pinned + recently changed + per-type pointers
    knowledge/_typen/<typ>.md       one line per note of that type (<= 50 per part, else split)
    state/decisions.md              view: one line per decision (old register, now generated)
    state/open-questions.md         view: kind question + conflict
    state/assumptions.md            view: kind assumption
    state/risks-and-constraints.md  view: kind risk + constraint

Sensitive notes (``sensitivity`` personal/restricted or ``origin: external``) appear only with
their id, never with title or summary, in every generated file.
"""

from __future__ import annotations

import re
from collections.abc import Callable
from pathlib import Path

from .limits import (
    INDEX_MAX_BYTES,
    INDEX_MAX_LINES,
    INDEX_MAX_PINNED,
    INDEX_MAX_RECENT,
    SUBINDEX_MAX_ENTRIES,
)
from .notes import TYPES, Note, load_notes
from .workspace import knowledge_dir, state_dir, write_lf

GENERATED = "<!-- GENERIERT von harness.mdmemory index · nicht von Hand editieren -->"
TYPE_DIR = "_typen"
STATUS_DE = {
    "active": "aktiv",
    "superseded": "abgeloest",
    "retracted": "zurueckgezogen",
    "archived": "archiviert",
}


def _sort_recent(notes: list[Note]) -> list[Note]:
    return sorted(notes, key=lambda n: (n.get("updated"), n.id), reverse=True)


#: Longest alias shown in an index line (aliases are free text; the cap keeps INDEX.md bounded).
ALIAS_MAX_CHARS = 40

_AT_TOKEN = re.compile(r"(^|\s)(@\S+)")


def safe(text: str) -> str:
    """Wrap ``@path`` tokens in backticks: Claude Code would import them from the boot index."""
    return _AT_TOKEN.sub(lambda m: f"{m.group(1)}`{m.group(2).replace('`', '')}`", text)


def _label(n: Note) -> str:
    alias = n.items("aliases")[0] if n.items("aliases") else ""
    if len(alias) > ALIAS_MAX_CHARS:
        alias = alias[: ALIAS_MAX_CHARS - 1] + "…"
    return f"{safe(alias)} · " if alias else ""


def entry_line(n: Note, link_prefix: str, *, brief: bool = False) -> str:
    """One index line. ``link_prefix`` is the relative path from the index file to knowledge/.

    ``brief`` (boot index): only the summary as link text, to keep the boot budget small.
    Sub indexes show title and summary.
    """
    href = f"{link_prefix}{n.type}/{n.id}.md"
    status = "" if n.active else f" · {STATUS_DE.get(n.get('status'), n.get('status'))}"
    date = n.get("updated") or n.get("valid_from")
    if n.sensitive:
        why = "extern" if n.get("origin") == "external" else n.get("sensitivity")
        return f"- [{n.id}]({href}) — ({why}, Inhalt nur in der Notiz) · {date}{status}"
    title, summary = n.get("title"), n.get("summary")
    if brief:
        return f"- [{safe(summary)}]({href}) · {_label(n)}{date}{status}"
    same = summary == title or title.endswith("…") and summary.startswith(title[:-1])
    text = "" if same else f"{safe(summary)} · "
    return f"- [{safe(title)}]({href}) — {_label(n)}{text}{date}{status}"


def render_index(notes: list[Note]) -> str:
    """Boot index. Drops the oldest "recent" lines, then pinned lines from the end, until
    INDEX_MAX_BYTES/LINES hold. Only active notes are pinned in the index."""
    pinned_all = [n for n in notes if n.pinned and n.active]
    recent_all = [n for n in _sort_recent([n for n in notes if n.active]) if not n.pinned]
    keep = min(len(recent_all), INDEX_MAX_RECENT)
    pin = min(len(pinned_all), INDEX_MAX_PINNED)
    while True:
        text = _render_index(notes, recent_all[:keep], pin)
        fits = len(text.encode("utf-8")) <= INDEX_MAX_BYTES and text.count("\n") <= INDEX_MAX_LINES
        if fits or keep == pin == 0:
            return text
        if keep:
            keep -= 1
        else:
            pin -= 1


def _render_index(notes: list[Note], recent: list[Note], pin_limit: int = INDEX_MAX_PINNED) -> str:
    active = [n for n in notes if n.active]
    pinned = sorted([n for n in notes if n.pinned and n.active], key=lambda n: (n.type, n.id))
    stand = max((n.get("updated") for n in notes), default="")
    lines = [
        GENERATED,
        "# INDEX",
        "",
        f"{len(active)} aktive von {len(notes)} Notizen"
        + (f", Stand {stand}" if stand else "")
        + ". Lade-Regel: AGENTS.md §9.",
        "",
        "## Angeheftet",
        "",
    ]
    lines += [entry_line(n, "", brief=True) for n in pinned[:pin_limit]] or ["(keine)"]
    if len(pinned) > pin_limit:
        lines.append(f"- … {len(pinned) - pin_limit} weitere in den Unterindizes")
    lines += ["", f"## Zuletzt geaendert ({len(recent)} neueste, ohne angeheftete)", ""]
    lines += [entry_line(n, "", brief=True) for n in recent] or ["(keine)"]
    counts = []
    for t in TYPES:
        of_type = [n for n in notes if n.type == t]
        n_active = sum(1 for n in of_type if n.active)
        if of_type:
            counts.append(f"{t} {n_active}/{len(of_type)}")
    lines += [
        "",
        "## Typen",
        "",
        f"Aktiv/gesamt: {' · '.join(counts) or 'keine'}. Unterindex je Typ:"
        f" `{TYPE_DIR}/<typ>.md` (Typen: {', '.join(TYPES)}).",
    ]
    return "\n".join(lines) + "\n"


def _type_lines(of_type: list[Note]) -> list[str]:
    ordered = _sort_recent([n for n in of_type if n.active]) + _sort_recent(
        [n for n in of_type if not n.active]
    )
    return [entry_line(n, "../") for n in ordered]


def render_type_files(notes: list[Note], note_type: str) -> dict[str, str]:
    """{file name under _typen/: content}. Split into parts of <= SUBINDEX_MAX_ENTRIES lines."""
    of_type = [n for n in notes if n.type == note_type]
    entries = _type_lines(of_type)
    head = [GENERATED, f"# {note_type}", ""]
    if len(entries) <= SUBINDEX_MAX_ENTRIES:
        body = [f"{len(of_type)} Notizen, aktive zuerst.", ""] + (entries or ["(keine Notizen)"])
        return {f"{note_type}.md": "\n".join(head + body) + "\n"}
    parts = [
        entries[i : i + SUBINDEX_MAX_ENTRIES] for i in range(0, len(entries), SUBINDEX_MAX_ENTRIES)
    ]
    out: dict[str, str] = {}
    toc = head + [f"{len(of_type)} Notizen in {len(parts)} Teilen, aktive zuerst.", ""]
    for k, part in enumerate(parts, start=1):
        name = f"{note_type}-{k:03d}.md"
        toc.append(f"- [Teil {k}]({name}): {len(part)} Eintraege")
        out[name] = "\n".join([GENERATED, f"# {note_type} · Teil {k}", ""] + part) + "\n"
    out[f"{note_type}.md"] = "\n".join(toc) + "\n"
    return out


# --- register views ------------------------------------------------------------------------------

VIEWS: dict[str, tuple[str, str, Callable[[Note], bool], str]] = {
    "decisions.md": (
        "decisions",
        "Decision Log",
        lambda n: n.type == "decision",
        "decision",
    ),
    "open-questions.md": (
        "open-questions",
        "Offene Fragen",
        lambda n: n.type == "question" and n.get("kind") in {"question", "conflict"},
        "question",
    ),
    "assumptions.md": (
        "assumptions",
        "Aktive Annahmen",
        lambda n: n.type == "question" and n.get("kind") == "assumption",
        "question",
    ),
    "risks-and-constraints.md": (
        "risks-and-constraints",
        "Risiken und Constraints",
        lambda n: n.type == "question" and n.get("kind") in {"risk", "constraint"},
        "question",
    ),
}


def _view_line(n: Note, alias_of: dict[str, str]) -> str:
    alias = alias_of.get(n.id, n.id)
    if n.sensitive and not re.fullmatch(r"[A-Z]-\d{4}-\d{2}-\d{2}-\d+", alias):
        alias = n.id
    alias = safe(alias)
    href = f"../knowledge/{n.type}/{n.id}.md"
    title = n.id if n.sensitive else safe(n.get("title"))
    tail = ""
    if n.get("superseded_by"):
        tail = f" → abgeloest durch {alias_of.get(n.get('superseded_by'), n.get('superseded_by'))}"
    elif n.items("supersedes"):
        tail = " · ersetzt " + ", ".join(alias_of.get(s, s) for s in n.items("supersedes"))
    return f"- {alias} · {n.get('valid_from')} · [{title}]({href}){tail}"


def render_view(notes: list[Note], file: str) -> str:
    vid, title, pred, note_type = VIEWS[file]
    selected = sorted(
        [n for n in notes if pred(n)],
        key=lambda n: (n.get("valid_from"), n.items("aliases")[:1], n.id),
        reverse=True,
    )
    alias_of = {n.id: n.items("aliases")[0] for n in notes if n.items("aliases")}
    act = [n for n in selected if n.active]
    rest = [n for n in selected if not n.active]
    lines = [
        "---",
        f"id: {vid}",
        f"type: {vid}",
        f'title: "{title} (generierte Sicht)"',
        "status: active",
        "generated: true",
        "---",
        GENERATED,
        "",
        f"# {title}",
        "",
        "**Generierte Sicht.** Kanonisch sind die Notizen unter "
        f"`../knowledge/{note_type}/` (D-2026-09-30-04). Neue Eintraege entstehen als Notiz "
        "(Vorlage `../templates/knowledge-note.md`), danach `python -m harness.mdmemory index`. "
        f"Das alte Vollformat liefert `python -m harness.mdmemory export-legacy {vid}`.",
        "",
        "## Aktiv",
        "",
        *([_view_line(n, alias_of) for n in act] or ["(noch keine)"]),
        "",
        "## Abgeloest, zurueckgezogen, archiviert",
        "",
        *([_view_line(n, alias_of) for n in rest] or ["(keine)"]),
        "",
    ]
    return "\n".join(lines)


# --- all derived files ---------------------------------------------------------------------------


def derived_files(root: Path, notes: list[Note] | None = None) -> dict[Path, str]:
    notes = load_notes(root) if notes is None else notes
    out: dict[Path, str] = {knowledge_dir(root) / "INDEX.md": render_index(notes)}
    for t in TYPES:
        for name, text in render_type_files(notes, t).items():
            out[knowledge_dir(root) / TYPE_DIR / name] = text
    for file in VIEWS:
        out[state_dir(root) / file] = render_view(notes, file)
    return out


def _stale_parts(root: Path, wanted: dict[Path, str]) -> list[Path]:
    tdir = knowledge_dir(root) / TYPE_DIR
    if not tdir.is_dir():
        return []
    return sorted(p for p in tdir.glob("*.md") if p not in wanted)


def write(root: Path) -> list[Path]:
    """Regenerate every derived file. Returns the paths that changed (written or removed)."""
    wanted = derived_files(root)
    changed: list[Path] = []
    for path, text in wanted.items():
        old = path.read_text(encoding="utf-8") if path.exists() else None
        if old != text:
            path.parent.mkdir(parents=True, exist_ok=True)
            write_lf(path, text)
            changed.append(path)
    for extra in _stale_parts(root, wanted):
        extra.unlink()
        changed.append(extra)
    return changed


def stale(root: Path) -> list[Path]:
    """Derived files whose content differs from a fresh render (lint: index up to date)."""
    wanted = derived_files(root)
    out = [
        p
        for p, text in wanted.items()
        if not p.exists() or p.read_text(encoding="utf-8").replace("\r\n", "\n") != text
    ]
    return out + _stale_parts(root, wanted)

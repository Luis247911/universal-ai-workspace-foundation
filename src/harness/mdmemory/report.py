"""Weekly maintenance report (skill ``pflege``): read-only findings plus the monthly rollup.

Sections: lint errors and warnings, stale notes, orphans, duplicate candidates, boot budget,
unconsolidated journals. The only files the maintenance run writes are generated ones (journal
rollups, D-2026-09-30-05) and, on request, the report itself under the gitignored
``scratch/maintenance/<datum>-pflege.md``. Everything else is a suggestion for the main session
or a PR; nothing is merged automatically.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, timedelta
from itertools import combinations
from pathlib import Path

from . import budget, consolidate, lint, rollup
from .consolidate import tokens
from .notes import DATE_RE, Note, load_notes
from .workspace import rel, ws

#: ``last_confirmed`` older than this -> stale (house rule, knowledge/README "Lifecycle").
STALE_DAYS = 180
#: Notes younger than this are never reported as orphans (they may simply be new).
ORPHAN_MIN_AGE_DAYS = 30
#: Jaccard overlap of title+summary tokens from which two active notes are duplicate candidates.
DUPLICATE_THRESHOLD = 0.6


@dataclass
class Report:
    today: str
    findings: list[lint.Finding] = field(default_factory=list)
    stale: list[tuple[Note, str]] = field(default_factory=list)
    orphans: list[Note] = field(default_factory=list)
    duplicates: list[tuple[float, Note, Note]] = field(default_factory=list)
    budget: budget.Report | None = None
    pending: list[consolidate.Pending] = field(default_factory=list)
    rollups: list[Path] = field(default_factory=list)

    @property
    def clean(self) -> bool:
        return not (
            self.findings or self.stale or self.orphans or self.duplicates or self.pending
        )


def _days_before(day: str, days: int) -> str:
    return (date.fromisoformat(day) - timedelta(days=days)).isoformat()


def stale(notes: list[Note], today: str) -> list[tuple[Note, str]]:
    cutoff = _days_before(today, STALE_DAYS)
    out: list[tuple[Note, str]] = []
    for n in notes:
        if not n.active:
            continue
        ra, lc = n.get("review_after"), n.get("last_confirmed")
        if ra and DATE_RE.match(ra) and ra < today:
            out.append((n, f"review_after {ra} ueberschritten"))
        elif lc and DATE_RE.match(lc) and lc < cutoff:
            out.append((n, f"zuletzt bestaetigt {lc} (> {STALE_DAYS} Tage)"))
    return out


def orphans(notes: list[Note], today: str) -> list[Note]:
    """Active, unpinned notes older than ORPHAN_MIN_AGE_DAYS that nothing links to and that link
    to nothing (no links, blocks, supersedes, superseded_by in either direction)."""
    by_ref = {n.id: n.id for n in notes} | {a: n.id for n in notes for a in n.items("aliases")}
    linked: set[str] = set()
    for n in notes:
        refs = n.items("links") + n.items("blocks") + n.items("supersedes")
        refs += [n.get("superseded_by")] if n.get("superseded_by") else []
        targets = {by_ref[r] for r in refs if r in by_ref}
        if targets:
            linked.add(n.id)
            linked |= targets
    cutoff = _days_before(today, ORPHAN_MIN_AGE_DAYS)
    return [
        n
        for n in notes
        if n.active and not n.pinned and n.id not in linked and n.get("valid_from") < cutoff
    ]


def duplicates(notes: list[Note]) -> list[tuple[float, Note, Note]]:
    active = [n for n in notes if n.active]
    toks = {n.id: tokens(n.get("title") + " " + n.get("summary")) for n in active}
    out: list[tuple[float, Note, Note]] = []
    for a, b in combinations(active, 2):
        if a.type != b.type or not toks[a.id] or not toks[b.id]:
            continue
        score = len(toks[a.id] & toks[b.id]) / len(toks[a.id] | toks[b.id])
        if score >= DUPLICATE_THRESHOLD:
            out.append((round(score, 2), a, b))
    return sorted(out, key=lambda t: (-t[0], t[1].id, t[2].id))


def build(root: Path, *, today: str | None = None, write_rollups: bool = True) -> Report:
    today = today or date.today().isoformat()
    notes = load_notes(root)
    rep = Report(today)
    rep.findings = lint.run(root, today=today, check_budget=False)
    rep.stale = stale(notes, today)
    rep.orphans = orphans(notes, today)
    rep.duplicates = duplicates(notes)
    rep.budget = budget.measure(root)
    rep.pending = consolidate.pending(root)
    if write_rollups:
        rep.rollups = rollup.write(root)
    return rep


def render(root: Path, rep: Report) -> str:
    def note_ref(n: Note) -> str:
        alias = f" ({n.items('aliases')[0]})" if n.items("aliases") else ""
        return f"`{n.id}`{alias}"

    lines = [f"# Pflege-Bericht {rep.today}", ""]
    lines.append("Nur Vorschlaege. Umsetzen in der Hauptsession oder per PR, nie auto-mergen.")
    lines += ["", "## Lint", ""]
    lines += [f"- {f}" for f in rep.findings] or ["- keine Befunde"]
    lines += ["", "## Veraltet (pruefen, bestaetigen oder ersetzen)", ""]
    lines += [f"- {note_ref(n)}: {why}" for n, why in rep.stale] or ["- nichts"]
    lines += ["", f"## Waisen (ohne Verbindung, aelter als {ORPHAN_MIN_AGE_DAYS} Tage)", ""]
    lines += [f"- {note_ref(n)}: {n.get('title')}" for n in rep.orphans] or ["- keine"]
    lines += ["", f"## Duplikat-Kandidaten (Aehnlichkeit >= {DUPLICATE_THRESHOLD})", ""]
    lines += [
        f"- {s:.2f}: {note_ref(a)} und {note_ref(b)} (pruefen: UPDATE, SUPERSEDE oder CONFLICT)"
        for s, a, b in rep.duplicates
    ] or ["- keine"]
    lines += ["", "## Nicht konsolidierte Journale (Skill `merken`)", ""]
    lines += [f"- `{rel(root, p.path)}` ({p.entries} Eintraege)" for p in rep.pending] or [
        "- keine"
    ]
    lines += ["", "## Boot-Budget", ""]
    if rep.budget:
        lines.append(f"- {rep.budget.line()}")
    lines += ["", "## Monats-Rollup", ""]
    lines += [f"- neu erzeugt: `{rel(root, p)}`" for p in rep.rollups] or ["- aktuell"]
    return "\n".join(lines) + "\n"


def default_path(root: Path, today: str) -> Path:
    return ws(root) / "scratch" / "maintenance" / f"{today}-pflege.md"

"""CLI: python -m harness.mdmemory <command>

    now ensure                      create state/now.md from the template if missing
    now trim [--session ID]         cap state/now.md at 4 KB; overflow goes to the session journal
    now migrate [--remove-legacy]   state/current-session.md -> migration journal + local now.md
    journal new --session ID        create the session journal (never overwrites), print its path
    journal append PATH KIND TEXT   append one entry at the end of a journal
    journal add KIND TEXT --session ID  append to this session's journal, creating it if needed
    index [--check]                 regenerate knowledge/INDEX.md, _typen/, register views
    lint [--no-budget]              check notes, supersede chains, generated files, boot budget
    budget                          boot budget in estimated tokens (per file, worst case)
    new TYPE TITLE [--alias A]      note skeleton knowledge/<typ>/<id>.md (--alias auto: next D-ID)
    split-decisions [--register R]  legacy registers -> notes (archive copy, round trip, views)
    export-legacy REGISTER          old full register format, rebuilt from the notes (stdout)
    rollup [--month YYYY-MM]        journal/YYYY/MM/_rollup.md
    import-automemory [--source D]  Claude auto-memory files -> one journal with candidates
    pending                         journals not consolidated yet (skill merken)
    candidates TEXT                 existing notes similar to TEXT (NOOP/UPDATE/SUPERSEDE check)
    supersede OLD NEW --change C    link both sides of a supersede chain (idempotent)
    confirm ID                      NOOP with confirmation: last_confirmed = today
    conflict A B TITLE --source S   pinned question note (kind conflict) linking A and B
    consolidated JOURNAL IDS...     freeze a journal: konsolidiert true + konsolidiert_zu
    adopt TARGET [--dry-run]        bring the memory into another project (idempotent, merges only)
    report [--write] [--no-rollup]  weekly maintenance report (skill pflege); stdout only reads,
                                    --write stores it in scratch/ and refreshes journal rollups

All commands take ``--root`` (default: nearest parent with ``.ai-workspace/``) or ``--global``
(the optional global namespace from $UAW_GLOBAL_MEMORY_DIR; off by default).

Pure stdlib.
"""

from __future__ import annotations

import argparse
import sys
from datetime import date
from pathlib import Path

from . import adopt as adopt_mod
from . import automemory, budget, consolidate, create, journal, lint, now, report, rollup, split
from . import index as index_mod
from .frontmatter import FrontmatterError
from .legacy import REGISTERS
from .limits import NOW_MAX_BYTES
from .notes import TYPES
from .workspace import (
    GLOBAL_ENV,
    GlobalNamespaceError,
    find_root,
    global_root,
    journal_dir,
    legacy_session_path,
    rel,
    write_lf,
)


def _root(args: argparse.Namespace) -> Path:
    if getattr(args, "use_global", False):
        if args.root:
            raise SystemExit("--global and --root exclude each other")
        try:
            project = find_root()
        except FileNotFoundError:
            project = None
        try:
            return global_root(project=project)
        except GlobalNamespaceError as exc:
            raise SystemExit(str(exc)) from None
    return find_root(args.root)


def _cmd_now(args: argparse.Namespace) -> int:
    root = _root(args)
    if args.action == "ensure":
        created = now.ensure(root)
        print(("created " if created else "exists  ") + "state/now.md")
        return 0
    if args.action == "trim":
        now.ensure(root)
        session = args.session or journal.new_session_id()
        res = now.trim(root, session_id=session, limit=args.limit, tool=args.tool)
        if not res.changed:
            print(f"ok: state/now.md {res.before} B <= {args.limit} B")
        else:
            print(
                f"trimmed: {res.before} B -> {res.after} B, {len(res.moved)} action line(s) moved"
                + (", snapshot stored" if res.snapshot else "")
            )
        return 0
    if args.action == "migrate":
        if not legacy_session_path(root).exists():
            print("nothing to migrate: state/current-session.md not found")
            return 0
        target = now.migrate(root, remove_legacy=args.remove_legacy)
        print(f"migration journal: {rel(root, target)}")
        if not args.remove_legacy:
            print("legacy file kept; rerun with --remove-legacy, then commit the removal")
        return 0
    return 2


def _cmd_journal(args: argparse.Namespace) -> int:
    root = _root(args)
    if args.action == "new":
        path, _ = journal.ensure(
            root,
            session_id=args.session or journal.new_session_id(),
            tool=args.tool,
            worktree=args.worktree,
        )
        print(rel(root, path))
        return 0
    if args.action == "append":
        path_arg, kind, text = args.rest
        journal.append(_journal_file(root, path_arg), kind, text)
        return 0
    if args.action == "add":
        kind, text = args.rest
        path, _ = journal.ensure(root, session_id=args.session, tool=args.tool)
        journal.append(path, kind, text)
        print(rel(root, path))
        return 0
    return 2


def _journal_file(root: Path, given: str) -> Path:
    """Resolve a journal path (relative to cwd, else to the root); it must lie in journal/."""
    path = Path(given)
    if not path.is_absolute() and not path.exists():
        path = root / path
    base = journal_dir(root).resolve()
    if base not in path.resolve().parents:
        raise SystemExit(f"not a journal file under {rel(root, base)}/: {given}")
    if not path.is_file():
        raise SystemExit(f"journal not found: {given}")
    return path


def _iso_date(value: str) -> str:
    try:
        return date.fromisoformat(value).isoformat()
    except ValueError:
        raise argparse.ArgumentTypeError(f"not a date YYYY-MM-DD: {value!r}") from None


def _limit(value: str) -> int:
    n = int(value)
    if n < now.MIN_LIMIT:
        raise argparse.ArgumentTypeError(f"must be at least {now.MIN_LIMIT}")
    return n


def _cmd_index(args: argparse.Namespace) -> int:
    root = _root(args)
    if args.check:
        stale = index_mod.stale(root)
        for p in stale:
            print(f"out of date: {rel(root, p)}")
        return 1 if stale else 0
    changed = index_mod.write(root)
    for p in changed:
        print(f"written: {rel(root, p)}")
    if not changed:
        print("index up to date")
    return 0


def _cmd_lint(args: argparse.Namespace) -> int:
    root = _root(args)
    findings = lint.run(root, check_budget=not args.no_budget)
    for f in findings:
        print(f)
    errors = sum(1 for f in findings if f.level == "E")
    print(f"{errors} error(s), {len(findings) - errors} warning(s)")
    return 1 if errors else 0


def _cmd_budget(args: argparse.Namespace) -> int:
    rep = budget.measure(_root(args))
    print(rep.table())
    return 1 if max(rep.actual, rep.worst_case) > rep.hard else 0


def _cmd_new(args: argparse.Namespace) -> int:
    root = _root(args)
    path = create.create(
        root,
        args.type,
        args.title,
        source=args.source,
        summary=args.summary,
        alias=args.alias,
        kind=args.kind,
    )
    print(rel(root, path))
    return 0


def _cmd_split(args: argparse.Namespace) -> int:
    root = _root(args)
    only = None if args.register == "all" else [args.register]
    for r in split.split(root, args.date, only):
        arch = f", archive {rel(root, r.archived)}" if r.archived else ""
        print(
            f"{r.register}: {r.entries} entries, {len(r.written)} written, "
            f"{r.skipped} skipped{arch}"
        )
    return 0


def _cmd_export(args: argparse.Namespace) -> int:
    sys.stdout.write(split.export_legacy(_root(args), args.register))
    return 0


def _cmd_rollup(args: argparse.Namespace) -> int:
    root = _root(args)
    changed = rollup.write(root, args.month)
    print(rollup.describe(root, changed) or "rollup up to date")
    return 0


def _cmd_import(args: argparse.Namespace) -> int:
    root = _root(args)
    source = Path(args.source) if args.source else automemory.default_source(root)
    path, count, created = automemory.import_dir(root, source, dry_run=args.dry_run)
    if path is None:
        print(f"nothing to import: no .md files in {source}")
    elif created:
        print(f"imported {count} file(s) -> {rel(root, path)} (review before commit)")
    elif args.dry_run:
        print(f"would import {count} file(s) -> {rel(root, path)}")
    else:
        print(f"already imported -> {rel(root, path)}")
    return 0


def _cmd_pending(args: argparse.Namespace) -> int:
    root = _root(args)
    items = consolidate.pending(root, include_running=args.all)
    for p in items:
        print(f"{rel(root, p.path)} · {p.entries} Eintraege · {', '.join(p.kinds)}")
    print(f"{len(items)} nicht konsolidierte Journale")
    return 0


def _cmd_candidates(args: argparse.Namespace) -> int:
    root = _root(args)
    for score, n in consolidate.candidates(root, args.text, args.limit):
        alias = f" ({', '.join(n.items('aliases'))})" if n.items("aliases") else ""
        print(f"{score:.2f} {n.id}{alias} · {n.get('status')} · {n.get('title')}")
    return 0


def _today(args: argparse.Namespace) -> str:
    return str(args.date or date.today().isoformat())


def _cmd_supersede(args: argparse.Namespace) -> int:
    root = _root(args)
    changed = consolidate.supersede(root, args.old, args.new, change=args.change, day=_today(args))
    print("\n".join(f"written: {rel(root, p)}" for p in changed) or "no change")
    return 0


def _cmd_confirm(args: argparse.Namespace) -> int:
    root = _root(args)
    changed = consolidate.confirm(root, args.ref, day=_today(args))
    print("\n".join(f"written: {rel(root, p)}" for p in changed) or "no change")
    return 0


def _cmd_conflict(args: argparse.Namespace) -> int:
    root = _root(args)
    path = consolidate.conflict(
        root, args.a, args.b, title=args.title, source=args.source, day=_today(args)
    )
    print(rel(root, path))
    return 0


def _cmd_consolidated(args: argparse.Namespace) -> int:
    root = _root(args)
    changed = consolidate.mark(root, _journal_file(root, args.journal), args.ids)
    print(("marked: " if changed else "unchanged: ") + args.journal)
    return 0


def _cmd_report(args: argparse.Namespace) -> int:
    root = _root(args)
    rep = report.build(root, today=args.date, write_rollups=args.write and not args.no_rollup)
    text = report.render(root, rep)
    if args.write:
        path = report.default_path(root, rep.today)
        path.parent.mkdir(parents=True, exist_ok=True)
        write_lf(path, text)
        print(f"report: {rel(root, path)}")
    else:
        sys.stdout.write(text)
    return 0 if rep.ok else 1


def _cmd_adopt(args: argparse.Namespace) -> int:
    target = Path(args.target)
    res = adopt_mod.adopt(
        target,
        source=Path(args.source) if args.source else None,
        dry_run=args.dry_run,
        import_automemory=args.import_automemory,
        ci=args.ci,
    )
    sys.stdout.write(adopt_mod.render(res, target.resolve()))
    return 0 if res.ok else 1


def _journal_options_last(argv: list[str]) -> list[str]:
    """Move ``journal`` options behind its positionals (``journal add --session X art text``).

    Before Python 3.12, argparse fills an ``nargs="*"`` positional with nothing when an option
    comes first and then rejects the rest; the hooks may run on 3.9.
    """
    if "journal" not in argv:
        return argv
    i = argv.index("journal") + 1
    head, tail = argv[:i], argv[i:]
    opts: list[str] = []
    rest: list[str] = []
    k = 0
    while k < len(tail):
        tok = tail[k]
        if tok in ("--session", "--tool", "--worktree") and k + 1 < len(tail):
            opts += tail[k : k + 2]
            k += 2
        elif tok.startswith(("--session=", "--tool=", "--worktree=")):
            opts.append(tok)
            k += 1
        else:
            rest.append(tok)
            k += 1
    return head + rest + opts


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="harness.mdmemory")
    parser.add_argument("--root", default=None, help="workspace root (default: auto-detect)")
    parser.add_argument(
        "--global", dest="use_global", action="store_true", help=f"use ${GLOBAL_ENV}"
    )
    sub = parser.add_subparsers(dest="cmd", required=True)

    np_ = sub.add_parser("now", help="Per-worktree live state state/now.md.")
    np_.add_argument("action", choices=["ensure", "trim", "migrate"])
    np_.add_argument(
        "--session", default=None, help="session id for the overflow journal (default: random)"
    )
    np_.add_argument("--tool", default="unbekannt")
    np_.add_argument("--limit", type=_limit, default=NOW_MAX_BYTES)
    np_.add_argument("--remove-legacy", action="store_true")

    jp = sub.add_parser("journal", help="Append-only session journal.")
    jp.add_argument("action", choices=["new", "append", "add"])
    jp.add_argument("rest", nargs="*", help="append: PATH KIND TEXT · add: KIND TEXT (--session)")
    jp.add_argument("--session", default=None, help="session id (default: random)")
    jp.add_argument("--tool", default="unbekannt")
    jp.add_argument("--worktree", default="")

    ip = sub.add_parser("index", help="Regenerate INDEX.md, sub indexes and register views.")
    ip.add_argument("--check", action="store_true", help="only report, exit 1 if out of date")
    lp = sub.add_parser("lint", help="Check notes and generated files.")
    lp.add_argument("--no-budget", action="store_true")
    sub.add_parser("budget", help="Boot budget in estimated tokens.")
    cp = sub.add_parser("new", help="Create a note skeleton.")
    cp.add_argument("type", choices=TYPES)
    cp.add_argument("title")
    cp.add_argument("--source", default=f"user:{date.today().isoformat()}")
    cp.add_argument("--summary", default="")
    cp.add_argument("--alias", default="", help='e.g. D-2031-01-01-01, or "auto" (next D-ID)')
    cp.add_argument(
        "--kind", default="", help="question only: question|assumption|risk|constraint|conflict"
    )
    sp = sub.add_parser("split-decisions", help="Legacy registers -> atomic notes.")
    sp.add_argument("--register", default="all", choices=["all", *REGISTERS])
    sp.add_argument(
        "--date", type=_iso_date, default=date.today().isoformat(), help="migration date"
    )
    ep = sub.add_parser("export-legacy", help="Old register format from the notes.")
    ep.add_argument("register", choices=list(REGISTERS))
    rp = sub.add_parser("rollup", help="Monthly journal rollup.")
    rp.add_argument("--month", default=None)
    ap = sub.add_parser("import-automemory", help="Auto-memory files -> journal candidates.")
    ap.add_argument("--source", default=None, help="folder (default: Claude's project memory)")
    ap.add_argument("--dry-run", action="store_true")

    pp = sub.add_parser("pending", help="Finished journals not consolidated yet.")
    pp.add_argument("--all", action="store_true", help="also journals of running sessions")
    cap = sub.add_parser("candidates", help="Notes similar to a statement.")
    cap.add_argument("text")
    cap.add_argument("--limit", type=int, default=5)
    sup = sub.add_parser("supersede", help="Link NEW as successor of OLD (both sides).")
    sup.add_argument("old")
    sup.add_argument("new")
    sup.add_argument("--change", required=True, choices=sorted(consolidate.CHANGE))
    sup.add_argument("--date", type=_iso_date, default=None)
    cfp = sub.add_parser("confirm", help="Set last_confirmed of a note.")
    cfp.add_argument("ref")
    cfp.add_argument("--date", type=_iso_date, default=None)
    cop = sub.add_parser("conflict", help="Record a contradiction as a pinned question.")
    cop.add_argument("a")
    cop.add_argument("b")
    cop.add_argument("title")
    cop.add_argument("--source", required=True)
    cop.add_argument("--date", type=_iso_date, default=None)
    cdp = sub.add_parser("consolidated", help="Freeze a journal after consolidation.")
    cdp.add_argument("journal")
    cdp.add_argument("ids", nargs="*")

    rpp = sub.add_parser("report", help="Weekly maintenance report (skill pflege).")
    rpp.add_argument(
        "--write", action="store_true", help="to scratch/maintenance/<datum>-pflege.md"
    )
    rpp.add_argument(
        "--no-rollup", action="store_true", help="with --write: do not (re)write journal rollups"
    )
    rpp.add_argument("--date", type=_iso_date, default=None)

    adp = sub.add_parser("adopt", help="Bring the workspace memory into another project.")
    adp.add_argument("target", help="project directory")
    adp.add_argument("--dry-run", action="store_true", help="only show what would change")
    adp.add_argument("--source", default=None, help="foundation checkout (default: this one)")
    adp.add_argument(
        "--import-automemory", action="store_true", help="import Claude auto-memory once"
    )
    ci = adp.add_mutually_exclusive_group()
    ci.add_argument("--ci", dest="ci", action="store_true", default=None, help="write CI template")
    ci.add_argument("--no-ci", dest="ci", action="store_false", help="no CI template")

    args = parser.parse_args(_journal_options_last(sys.argv[1:] if argv is None else argv))
    if args.cmd == "journal":
        want = {"new": 0, "append": 3, "add": 2}[args.action]
        if len(args.rest) != want:
            usage = {"new": "", "append": " PATH KIND TEXT", "add": " KIND TEXT --session ID"}
            parser.error(f"journal {args.action}{usage[args.action]}")
        if args.action == "add" and not args.session:
            parser.error("journal add needs --session ID (the hook now_init names it)")
        kind = args.rest[-2] if want else ""
        if want and kind not in journal.KINDS:
            parser.error(f"entry kind {kind!r} not in {', '.join(journal.KINDS)}")
    handlers = {
        "now": _cmd_now,
        "journal": _cmd_journal,
        "index": _cmd_index,
        "lint": _cmd_lint,
        "budget": _cmd_budget,
        "new": _cmd_new,
        "split-decisions": _cmd_split,
        "export-legacy": _cmd_export,
        "rollup": _cmd_rollup,
        "import-automemory": _cmd_import,
        "pending": _cmd_pending,
        "candidates": _cmd_candidates,
        "supersede": _cmd_supersede,
        "confirm": _cmd_confirm,
        "conflict": _cmd_conflict,
        "consolidated": _cmd_consolidated,
        "report": _cmd_report,
        "adopt": _cmd_adopt,
    }
    try:
        return handlers[args.cmd](args)
    except (FrontmatterError, KeyError, ValueError, adopt_mod.AdoptError) as exc:
        msg = exc.args[0] if isinstance(exc, KeyError) and exc.args else exc
        print(f"error: {msg}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())

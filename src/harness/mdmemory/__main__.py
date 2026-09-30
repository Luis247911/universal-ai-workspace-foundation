"""CLI: python -m harness.mdmemory <command>

    now ensure                      create state/now.md from the template if missing
    now trim [--session ID]         cap state/now.md at 4 KB; overflow goes to the session journal
    now migrate [--remove-legacy]   state/current-session.md -> migration journal + local now.md
    journal new --session ID        create the session journal (never overwrites), print its path
    journal append PATH KIND TEXT   append one entry at the end of a journal

All commands take ``--root`` (default: nearest parent with ``.ai-workspace/``). Pure stdlib.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from . import journal, now
from .limits import NOW_MAX_BYTES
from .workspace import find_root, journal_dir, legacy_session_path, rel


def _root(args: argparse.Namespace) -> Path:
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
        path = _journal_file(root, args.path)
        journal.append(path, args.kind, args.text)
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


def _limit(value: str) -> int:
    n = int(value)
    if n < now.MIN_LIMIT:
        raise argparse.ArgumentTypeError(f"must be at least {now.MIN_LIMIT}")
    return n


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="harness.mdmemory")
    parser.add_argument("--root", default=None, help="workspace root (default: auto-detect)")
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
    jp.add_argument("action", choices=["new", "append"])
    jp.add_argument("path", nargs="?", help="journal file (append)")
    jp.add_argument("kind", nargs="?", choices=journal.KINDS, help="entry kind (append)")
    jp.add_argument("text", nargs="?", help="entry text (append)")
    jp.add_argument("--session", default=None, help="session id (default: random)")
    jp.add_argument("--tool", default="unbekannt")
    jp.add_argument("--worktree", default="")

    args = parser.parse_args(argv)
    if args.cmd == "journal" and args.action == "append" and not (args.path and args.text):
        parser.error("journal append needs PATH KIND TEXT")
    handlers = {"now": _cmd_now, "journal": _cmd_journal}
    return handlers[args.cmd](args)


if __name__ == "__main__":
    sys.exit(main())

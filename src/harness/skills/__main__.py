"""CLI: python -m harness.skills lint  <path>   (a SKILL.md, a skill dir, or a dir of skills)
       python -m harness.skills audit <path>   (a skill dir, or a dir of skills)

`lint` exits non-zero on any error-level issue; `audit` exits non-zero on any high finding.
Both are pure-stdlib and offline.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .audit import audit_path, audit_tree
from .lint import lint_file, lint_tree


def _is_skill_dir(p: Path) -> bool:
    return (p / "SKILL.md").is_file()


def _lint(path: str) -> int:
    p = Path(path)
    if p.is_file():
        results = {p.parent.name: lint_file(p)}
    elif _is_skill_dir(p):
        results = {p.name: lint_file(p / "SKILL.md")}
    else:
        results = lint_tree(p)
    if not results:
        print(f"no SKILL.md found under {path}")
        return 1
    errs = 0
    for name, issues in results.items():
        if not issues:
            print(f"[ok ] {name}")
            continue
        for i in issues:
            tag = "ERR " if i.level == "error" else "warn"
            print(f"[{tag}] {name}: {i.code} {i.message}")
        errs += sum(1 for i in issues if i.level == "error")
    print(f"\n{len(results)} skill(s), {errs} error(s)")
    return 1 if errs else 0


def _audit(path: str) -> int:
    p = Path(path)
    if p.is_file() or _is_skill_dir(p):
        results = {p.name: audit_path(p)}
    else:
        results = audit_tree(p)
    highs = 0
    for name, findings in results.items():
        if not findings:
            print(f"[ok ] {name}")
            continue
        for f in findings:
            print(f"[{f.level}] {name}: {f.code} {f.file}:{f.line} {f.message}")
        highs += sum(1 for f in findings if f.level == "high")
    print(f"\n{len(results)} target(s), {highs} high finding(s)")
    return 1 if highs else 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="harness.skills")
    sub = parser.add_subparsers(dest="cmd", required=True)
    lp = sub.add_parser("lint", help="Validate SKILL.md frontmatter.")
    lp.add_argument("path")
    ap = sub.add_parser("audit", help="Scan skill scripts for risk patterns.")
    ap.add_argument("path")
    args = parser.parse_args(argv)
    if args.cmd == "lint":
        return _lint(args.path)
    if args.cmd == "audit":
        return _audit(args.path)
    return 2


if __name__ == "__main__":
    sys.exit(main())

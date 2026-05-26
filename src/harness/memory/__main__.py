"""CLI: python -m harness.memory demo

Walks through working memory -> promote to archival -> vector search, all in-memory.
"""

from __future__ import annotations

import argparse
import sys

from .store import MemoryStore, MemType, Scope


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="harness.memory")
    sub = parser.add_subparsers(dest="cmd", required=True)
    sub.add_parser("demo", help="Run an in-memory walkthrough.")
    args = parser.parse_args(argv)

    if args.cmd == "demo":
        m = MemoryStore()
        working = m.core_append("task", "user is debugging a flaky test", scope=Scope.SESSION)
        m.archival_insert("the user prefers pytest over unittest", MemType.SEMANTIC, Scope.USER)
        m.archival_insert(
            "last week we migrated CI to GitHub Actions", MemType.EPISODIC, Scope.USER
        )
        print(f"in-context working items: {len(m.core_view())}")
        hits = m.archival_search("which test framework does the user like", top_k=2)
        for item, score in hits:
            print(f"  archival[{item.mtype.value}] {score:.2f}: {item.content}")
        promoted = m.promote(working.id, MemType.EPISODIC, Scope.USER)
        print(f"promoted working -> {promoted.mtype.value} (in_context now {len(m.core_view())})")
        return 0
    return 2


if __name__ == "__main__":
    sys.exit(main())

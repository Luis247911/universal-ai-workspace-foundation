"""Offline memory demo: working memory -> archival -> vector search -> promote.

python examples/memory_demo.py
"""

from __future__ import annotations

from harness.memory import MemoryStore, MemType, Scope


def main() -> int:
    m = MemoryStore()
    note = m.core_append("task", "user is debugging a flaky integration test", scope=Scope.SESSION)
    m.archival_insert("the user prefers pytest over unittest", MemType.SEMANTIC, Scope.USER)
    m.archival_insert("CI moved to GitHub Actions last sprint", MemType.EPISODIC, Scope.USER)

    print(f"in-context (working) items: {len(m.core_view())}")
    for item, score in m.archival_search("which test runner does the user prefer", top_k=1):
        print(f"  archival hit [{item.mtype.value}] score={score:.2f}: {item.content}")

    m.promote(note.id, MemType.EPISODIC, Scope.USER)
    print(f"after promote, in-context items: {len(m.core_view())} (moved across the boundary)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

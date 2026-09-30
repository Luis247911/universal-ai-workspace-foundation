"""Boot budget: what the UAW share of every session start costs, in estimated tokens.

Boot files (AGENTS.md §1): AGENTS.md, CLAUDE.md, state/project-index.md, state/now.md,
knowledge/INDEX.md. ``actual`` measures the files as they are (``now.md`` falls back to its
template, which is what ``now_init`` creates in a fresh clone). ``worst_case`` replaces the two
growing files by their hard caps (now.md 4 KB, INDEX.md ``INDEX_MAX_BYTES``), so it cannot be
exceeded later without a failing test.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from .limits import (
    BOOT_HARD_TOKENS,
    BOOT_TARGET_TOKENS,
    CHARS_PER_TOKEN,
    INDEX_MAX_BYTES,
    NOW_MAX_BYTES,
    estimate_tokens,
)
from .workspace import knowledge_dir, now_path, state_dir, templates_dir

NOW_TEMPLATE = "session-state.md"


def boot_files(root: Path) -> dict[str, Path]:
    return {
        "AGENTS.md": root / "AGENTS.md",
        "CLAUDE.md": root / "CLAUDE.md",
        "project-index.md": state_dir(root) / "project-index.md",
        "now.md": now_path(root),
        "INDEX.md": knowledge_dir(root) / "INDEX.md",
    }


def _read(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except OSError:
        return ""


@dataclass(frozen=True)
class Report:
    tokens: dict[str, int]
    actual: int
    worst_case: int
    target: int = BOOT_TARGET_TOKENS
    hard: int = BOOT_HARD_TOKENS

    def line(self) -> str:
        return (
            f"boot {self.actual} tokens (target {self.target}, hard {self.hard}), "
            f"worst case {self.worst_case}"
        )

    def table(self) -> str:
        rows = [f"{name:18s} {tok:6d}" for name, tok in self.tokens.items()]
        return "\n".join(rows + [f"{'summe':18s} {self.actual:6d}", self.line()])


def measure(root: Path) -> Report:
    files = boot_files(root)
    texts = {name: _read(path) for name, path in files.items()}
    if not texts["now.md"]:
        texts["now.md"] = _read(templates_dir(root) / NOW_TEMPLATE)
    tokens = {name: estimate_tokens(t) for name, t in texts.items()}
    actual = sum(tokens.values())
    cap = int((NOW_MAX_BYTES + INDEX_MAX_BYTES) / CHARS_PER_TOKEN)
    worst = actual - tokens["now.md"] - tokens["INDEX.md"] + cap
    return Report(tokens, actual, worst)

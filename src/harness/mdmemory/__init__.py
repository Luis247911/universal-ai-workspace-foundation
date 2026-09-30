"""Markdown memory of the workspace: journal, live state, atomic notes and generated indexes.

Stdlib only. This package manages the *workspace* memory under ``.ai-workspace/`` (Markdown in
git). It is unrelated to ``harness.memory``, the in-memory demo store for agents you build.

CLI: ``python -m harness.mdmemory --help``.
"""

from .journal import JournalFrozenError, short_id
from .limits import estimate_tokens
from .workspace import find_root

__all__ = ["JournalFrozenError", "estimate_tokens", "find_root", "short_id"]

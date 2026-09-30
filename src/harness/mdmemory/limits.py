"""Budgets and tool limits of the Markdown memory, in one place.

Tool limits drift (Claude Code and Codex change them between releases). Keep every number that
comes from a tool here, next to the page it was read from, so an update is a one-file change.
Numbers without a link are house budgets chosen by this repo, not tool limits.
"""

from __future__ import annotations

# --- house budgets -------------------------------------------------------------------------------

#: Hard cap for the per-worktree live state ``state/now.md`` (bytes, UTF-8).
NOW_MAX_BYTES = 4096

#: Boot budget of the UAW share (AGENTS + CLAUDE + project-index + now + INDEX), in tokens.
BOOT_TARGET_TOKENS = 5_000
BOOT_HARD_TOKENS = 12_000

#: Generated boot index ``knowledge/INDEX.md``.
INDEX_MAX_LINES = 150
INDEX_MAX_BYTES = 16_384
INDEX_MAX_PINNED = 40
INDEX_MAX_RECENT = 30

#: Entries per generated sub index part ``knowledge/_typen/<typ>.md`` (more -> split into parts).
SUBINDEX_MAX_ENTRIES = 50

#: ``summary`` is copied 1:1 into the index, so it is short and plain.
SUMMARY_MAX_CHARS = 120

#: Files longer than this are never read in full at session start (grep instead).
LARGE_FILE_LINES = 1_000

# --- token estimate ------------------------------------------------------------------------------

#: Characters per token. Anthropic states "1M tokens ~ 2.5M Unicode characters" for current models
#: (https://platform.claude.com/docs/en/about-claude/models/overview). An estimate, roughly +-25 %.
CHARS_PER_TOKEN = 2.5

# --- tool limits ---------------------------------------------------------------------------------

#: Claude Code caps a hook's ``additionalContext`` / plain stdout at 10,000 characters; more is
#: spilled to a file (https://code.claude.com/docs/en/hooks).
CLAUDE_HOOK_CONTEXT_MAX_CHARS = 10_000

#: Claude Code: all SessionEnd hooks share a 1.5 s budget (https://code.claude.com/docs/en/hooks).
CLAUDE_SESSION_END_BUDGET_S = 1.5

#: Codex: SessionEnd defaults to 1 s and allows at most 3 s; SessionStart context is spilled above
#: roughly 2,500 tokens unless ``additionalContextLimit`` is raised
#: (https://learn.chatgpt.com/docs/hooks).
CODEX_SESSION_END_MAX_S = 3
CODEX_HOOK_CONTEXT_DEFAULT_TOKENS = 2_500


def estimate_tokens(text: str) -> int:
    """Rough token count of ``text`` (characters / :data:`CHARS_PER_TOKEN`, rounded up)."""
    return -(-len(text) * 10 // int(CHARS_PER_TOKEN * 10))

"""UserPromptSubmit hook: inject the prompt-optimizer disambiguation protocol on a vague prompt.

Self-gated on the ``prompt_optimizer`` flag (default OFF). When the submitted prompt looks vague --
short with no action verb, several antecedent-less pronouns, or a semantically open question -- it
returns the three-tier "expose-assumptions-first" protocol as ``additionalContext`` so the model
hardens a quickly-typed request without stalling the user. A clear prompt (slash-command, a path or
code block, or a precise instruction) -> inert (exit 0, no output). Any error resolves to inert --
the fail-safe direction. Reads only repo-relative paths; never touches ``~/.claude/``.

Mirrors .claude/skills/prompt-optimizer/SKILL.md: it injects the reminder, the model decides. It
NEVER blocks the prompt (no exit 2) -- advisory only, consistent with the other automation hooks.
"""

from __future__ import annotations

import json
import re
import sys

from _flags import flag

# A small, domain-neutral set of opening action verbs. Not exhaustive -- the goal is a cheap
# "does this read like an instruction?" check, biased toward NOT firing on clear prompts.
ACTION_VERBS = {
    "add", "analyze", "build", "change", "check", "clean", "compare", "configure", "convert",
    "create", "debug", "delete", "describe", "design", "document", "draft", "explain", "extend",
    "find", "fix", "format", "generate", "implement", "improve", "init", "install", "lint", "list",
    "make", "migrate", "move", "optimize", "plan", "refactor", "remove", "rename", "render",
    "replace", "review", "rewrite", "run", "scan", "search", "set", "show", "summarize", "test",
    "translate", "update", "validate", "verify", "write",
}
VAGUE_PRONOUNS = {"it", "this", "that", "these", "those", "them", "thing", "things", "stuff"}
OPEN_MARKERS = ("something", "anything", "somehow", "some way")


def _looks_vague(prompt: str) -> bool:
    text = prompt.strip()
    if not text:
        return False
    # Clear by construction: slash-command, a code block/backtick, or a path/filename token.
    if text.startswith("/"):
        return False
    if "`" in text:
        return False
    if re.search(r"\S+/\S+|\S+\.[A-Za-z]{1,5}\b", text):
        return False

    words = re.findall(r"[A-Za-z']+", text.lower())
    if not words:
        return False
    wc = len(words)
    has_action = bool(set(words[:4]) & ACTION_VERBS)
    pronoun_hits = sum(1 for w in words if w in VAGUE_PRONOUNS)
    lower = text.lower()
    open_q = text.endswith("?") and any(m in lower for m in OPEN_MARKERS)

    # Vague if ANY of the skill's three conditions holds (kept conservative to avoid noise).
    if wc <= 6 and not has_action:
        return True
    if pronoun_hits >= 2 and wc <= 12:
        return True
    if open_q and wc <= 12:
        return True
    return False


def main() -> int:
    try:
        raw = sys.stdin.read()
    except Exception:
        return 0

    if not flag("prompt_optimizer"):
        return 0  # inert: flag off

    try:
        prompt = str(json.loads(raw).get("prompt", "")) if raw.strip() else ""
    except (ValueError, AttributeError):
        return 0  # unreadable payload -> inert

    if not _looks_vague(prompt):
        return 0  # clear enough -> stay silent

    context = (
        "## Vague-request check (prompt-optimizer)\n"
        "This prompt reads as underspecified. Apply the prompt-optimizer protocol "
        "(.claude/skills/prompt-optimizer/SKILL.md), defaulting to Tier 1:\n"
        "1. Open with 1-3 explicit, checkable assumptions ('Assumption: you mean X, not Y; "
        "output = markdown.'), then proceed.\n"
        "2. Ask back only if two-plus readings are plausible AND a wrong guess is expensive "
        "(hours of work, an irreversible edit, an outbound send) -- one question, never a "
        "cascade.\n"
        "3. Before a big multi-file / sub-agent action, give a one-line understanding statement. "
        "Do not quote the whole prompt back."
    )
    out = {
        "hookSpecificOutput": {
            "hookEventName": "UserPromptSubmit",
            "additionalContext": context,
        }
    }
    print(json.dumps(out))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

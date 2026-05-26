"""Skills area: tooling that operates on `.claude/skills/<slug>/` directories.

Two concerns, both pure-stdlib and offline:
    lint   validate SKILL.md frontmatter against the repo's skill-format contract
    audit  scan a skill's executable scripts for supply-chain risk patterns

This is the engine the `skill-author` and `skill-supply-chain-check` skills wrap. The
repo dogfoods it: its own skills must pass `lint`, enforced in the test suite.
"""

from __future__ import annotations

from .audit import Finding, audit_path, audit_tree
from .lint import Issue, lint_file, lint_text, lint_tree, parse_frontmatter

__all__ = [
    "Issue",
    "lint_text",
    "lint_file",
    "lint_tree",
    "parse_frontmatter",
    "Finding",
    "audit_path",
    "audit_tree",
]

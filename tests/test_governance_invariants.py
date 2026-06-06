"""Governance-layer invariants: the two structural rules that are purely mechanical.

The Markdown core (`.ai-workspace/`) is otherwise enforced only by an agent reading the policies.
These two rules are objective, so they get a machine check in the normal pytest gate — deliberately
NOT a shipped maintenance routine (`knowledge-graph-policy.md` §12), just a repo test:

    C1  `.ai-workspace/**` is Markdown-only        (AGENTS.md §8)
    C2  no forbidden top-level dir under it         (setup-protocol.md §4, AGENTS.md §3)
"""

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
WORKSPACE = REPO_ROOT / ".ai-workspace"

# Blocklist verbatim from setup-protocol.md §4 (".ai-workspace/README.md" lists the same names).
FORBIDDEN_DIRS = {
    "agents", "skills", "commands", "hooks", "tasks", "responses", "runs", "memory",
    "sessions", "workflows", "prompts", "notes", "docs", "ai", "claude-system",
    "agent-system", "harness", "workspace", "context", "project-state", "wiki",
    "vector", "embeddings", "index", "rag", "cache", "logs", "infra", "mcp",
}


def test_workspace_is_markdown_only():
    """C1: every file under .ai-workspace/ is a .md file (AGENTS.md §8)."""
    offenders = sorted(
        str(p.relative_to(REPO_ROOT))
        for p in WORKSPACE.rglob("*")
        if p.is_file() and p.suffix != ".md"
    )
    assert not offenders, f"non-Markdown files in the governance layer: {offenders}"


def test_no_forbidden_top_level_dirs():
    """C2: no forbidden directory at the top of .ai-workspace/ (setup-protocol.md §4)."""
    present = {p.name for p in WORKSPACE.iterdir() if p.is_dir()}
    collisions = sorted(present & FORBIDDEN_DIRS)
    assert not collisions, f"forbidden top-level dirs under .ai-workspace/: {collisions}"

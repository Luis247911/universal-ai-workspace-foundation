"""Dogfood: the repo's own `.claude/skills/` must pass the repo's own skill tooling.

This is what makes the skill engine load-bearing rather than decorative — if a skill drifts
from the frontmatter contract or a script grows a risky pattern, this test goes red.
"""

from pathlib import Path

from harness.skills import audit_tree, lint_tree
from harness.skills.audit import has_high
from harness.skills.lint import has_errors

REPO_ROOT = Path(__file__).resolve().parents[1]
SKILLS = REPO_ROOT / ".claude" / "skills"

EXPECTED = {
    "eval-loop-builder",
    "guardrail-designer",
    "observability-tracer",
    "hitl-gate",
    "cost-latency-optimizer",
    "multi-agent-topology",
    "orchestrator-patterns",
    "memory-architect",
    "skill-author",
    "agent-pattern-selector",
    "eval-judge",
    "skill-supply-chain-check",
}


def _skill_dirs():
    return sorted(p for p in SKILLS.iterdir() if p.is_dir() and (p / "SKILL.md").is_file())


def test_skills_directory_present():
    assert SKILLS.is_dir(), "expected .claude/skills/ to exist"
    names = {p.name for p in _skill_dirs()}
    assert EXPECTED <= names, f"missing skills: {EXPECTED - names}"


def test_all_skills_lint_clean():
    results = lint_tree(SKILLS)
    failures = {
        name: [str(i) for i in issues if i.level == "error"]
        for name, issues in results.items()
        if has_errors(issues)
    }
    assert not failures, f"SKILL.md lint errors: {failures}"


def test_all_skills_audit_clean():
    results = audit_tree(SKILLS)
    failures = {
        name: [str(f) for f in finds if f.level == "high"]
        for name, finds in results.items()
        if has_high(finds)
    }
    assert not failures, f"high-severity audit findings: {failures}"


def test_script_skills_are_runnable_and_have_evals():
    for d in _skill_dirs():
        scripts = d / "scripts"
        if scripts.is_dir():
            assert (scripts / "run.py").is_file(), f"{d.name}: scripts/ without run.py"
            assert (d / "evaluate.md").is_file(), f"{d.name}: runnable skill must ship evaluate.md"


def test_runpy_shims_are_thin():
    # a shim must delegate to a harness CLI and carry no logic of its own
    for d in _skill_dirs():
        run = d / "scripts" / "run.py"
        if run.is_file():
            text = run.read_text(encoding="utf-8")
            assert "from harness." in text and ".__main__ import main" in text, (
                f"{d.name}: run.py must delegate to a harness.<area>.__main__:main"
            )

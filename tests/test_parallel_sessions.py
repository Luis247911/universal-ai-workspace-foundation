"""Merge test: two parallel sessions in two git worktrees, then both branches are merged.

Compares the pre-3.3 model (one tracked, overwritten ``state/current-session.md``) with the 3.3
model (gitignored ``state/now.md`` per worktree + one journal file per session). Real ``git merge``
runs, no mocks. Acceptance (D-2026-09-30-01): the 3.3 model has 0 conflicts on session state.

As a script it prints the measurement, e.g. ``python tests/test_parallel_sessions.py --runs 60``.
"""

from __future__ import annotations

import argparse
import random
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime, timedelta
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

from harness.mdmemory import journal, now  # noqa: E402

GIT_ID = ["-c", "user.name=merge-test", "-c", "user.email=merge-test@example.invalid"]


def _git(cwd: Path, *args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *GIT_ID, *args], cwd=cwd, capture_output=True, text=True, check=check
    )


def _seed_repo(base: Path, legacy: bool) -> Path:
    repo = base / "main"
    (repo / ".ai-workspace").mkdir(parents=True)
    for sub in ("state", "templates"):
        shutil.copytree(REPO_ROOT / ".ai-workspace" / sub, repo / ".ai-workspace" / sub)
    (repo / ".ai-workspace" / "journal").mkdir()
    (repo / ".ai-workspace" / "journal" / "README.md").write_text("# journal\n", encoding="utf-8")
    shutil.copy(REPO_ROOT / ".gitignore", repo / ".gitignore")
    if legacy:
        tpl = (repo / ".ai-workspace" / "templates" / "session-state.md").read_text("utf-8")
        (repo / ".ai-workspace" / "state" / "current-session.md").write_text(tpl, "utf-8")
    _git(repo, "init", "-q", "-b", "main")
    _git(repo, "add", "-A")
    _git(repo, "commit", "-q", "-m", "seed")
    return repo


def _session(repo: Path, wt: Path, branch: str, legacy: bool, rng: random.Random) -> None:
    """One session in its own worktree: work, record state, commit."""
    _git(repo, "worktree", "add", "-q", "-b", branch, str(wt))
    task = f"Aufgabe {branch} {rng.randrange(10**6)}"
    state_text = f"# Session state\n\n## Aktive Aufgabe\n\n{task}\n\n## Letzte Aktionen\n\n" + (
        "\n".join(f"- {branch} schritt {i}" for i in range(rng.randint(3, 10)))
    )
    when = datetime(2026, 9, 30, 9, 0) + timedelta(minutes=rng.randrange(600))
    if legacy:
        (wt / ".ai-workspace" / "state" / "current-session.md").write_text(state_text, "utf-8")
    else:
        now.ensure(wt)
        (wt / ".ai-workspace" / "state" / "now.md").write_text(state_text, "utf-8")
        sid = f"{rng.getrandbits(128):032x}"
        path, _ = journal.ensure(wt, session_id=sid, when=when, tool="test")
        journal.append(path, "ergebnis", task, when)
    # some ordinary work in the same commit, as a real session would
    (wt / f"work-{branch}.md").write_text(f"{task}\n", encoding="utf-8")
    _git(wt, "add", "-A")
    _git(wt, "commit", "-q", "-m", f"session {branch}")


def run_once(legacy: bool, seed: int) -> list[str]:
    """Return the conflicted paths after merging two parallel sessions into main."""
    rng = random.Random(seed)
    with tempfile.TemporaryDirectory() as tmp:
        base = Path(tmp)
        repo = _seed_repo(base, legacy)
        _session(repo, base / "wt-a", "a", legacy, rng)
        _session(repo, base / "wt-b", "b", legacy, rng)
        _git(repo, "merge", "-q", "--no-edit", "a")
        merged = _git(repo, "merge", "-q", "--no-edit", "b", check=False)
        conflicts = _git(repo, "diff", "--name-only", "--diff-filter=U").stdout.split()
        if merged.returncode != 0 and not conflicts:
            raise RuntimeError(merged.stderr)
        return conflicts


def measure(runs: int) -> dict[str, tuple[int, int]]:
    """{model: (runs with a session-state conflict, runs)}."""
    out = {}
    models = (("vorher: current-session.md", True), ("nachher: now.md + journal", False))
    for name, legacy in models:
        hits = sum(
            1
            for seed in range(runs)
            if any("state/" in p or "journal/" in p for p in run_once(legacy, seed))
        )
        out[name] = (hits, runs)
    return out


pytestmark = pytest.mark.skipif(shutil.which("git") is None, reason="git not installed")


def test_legacy_model_conflicts_on_session_state():
    assert run_once(legacy=True, seed=1) == [".ai-workspace/state/current-session.md"]


@pytest.mark.parametrize("seed", range(3))
def test_now_plus_journal_merges_without_conflict(seed):
    assert run_once(legacy=False, seed=seed) == []


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--runs", type=int, default=20)
    args = ap.parse_args()
    for model, (hits, total) in measure(args.runs).items():
        print(f"{model:30s} {hits:3d}/{total} Laeufe mit Konflikt ({100 * hits / total:.0f} %)")

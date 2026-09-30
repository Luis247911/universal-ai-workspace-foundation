"""End to end: both ways in, with the hooks run the way Claude Code runs them.

* Weg A: a fresh clone of this repo (tracked + new files, nothing gitignored), no ``pip install``.
* Weg B: a fictional project in v3.2 style (own AGENTS.md/CLAUDE.md, legacy registers,
  ``current-session.md``, own settings hook, a fictional auto-memory folder), adopted with
  ``adopt``: dry run, real run, second run without a diff, then a whole session through the hooks.

Hooks are started as ``sh .claude/hooks/run.sh <hook>.py`` with a PATH whose only Python is called
``python3`` (like stock macOS). All names and contents are fictional.
"""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

from harness.mdmemory import adopt, budget, lint
from harness.mdmemory.limits import BOOT_HARD_TOKENS, BOOT_TARGET_TOKENS

REPO_ROOT = Path(__file__).resolve().parents[1]
POSIX_SH = shutil.which("sh") is not None and os.name != "nt"
needs_sh = pytest.mark.skipif(not POSIX_SH, reason="hooks run through sh (POSIX)")

SID = "7d3c0a9e-1b2c-4d5e-8f60-718293a4b5c6"


# --- helpers -------------------------------------------------------------------------------------


def _fresh_clone(dest: Path) -> Path:
    """What a clone of this commit would contain: tracked + new files, no gitignored ones."""
    out = subprocess.run(
        [
            "git",
            "-C",
            str(REPO_ROOT),
            "ls-files",
            "-z",
            "--cached",
            "--others",
            "--exclude-standard",
        ],
        capture_output=True,
        check=True,
    ).stdout.decode("utf-8")
    for name in filter(None, out.split("\0")):
        src = REPO_ROOT / name
        if src.is_file():
            (dest / name).parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dest / name)
    return dest


def _python3_only_path(tmp: Path) -> str:
    """A PATH where the interpreter is reachable only as ``python3``."""
    bindir = tmp / "bin"
    bindir.mkdir(exist_ok=True)
    link = bindir / "python3"
    if not link.exists():
        link.symlink_to(sys.executable)
    return os.pathsep.join([str(bindir), "/usr/bin", "/bin"])


def _hook(root: Path, script: str, payload: dict, path_env: str) -> str:
    env = {k: v for k, v in os.environ.items() if k not in ("PYTHONPATH", "UAW_PYTHON")}
    env.update(CLAUDE_PROJECT_DIR=str(root), PATH=path_env, UAW_DISABLE_ONBOARDING="1")
    proc = subprocess.run(
        ["sh", str(root / ".claude" / "hooks" / "run.sh"), script],
        input=json.dumps(payload),
        capture_output=True,
        text=True,
        env=env,
        cwd=root,
        timeout=30,
    )
    assert proc.returncode == 0, proc.stderr
    return proc.stdout


def _ctx(out: str) -> str:
    return json.loads(out)["hookSpecificOutput"]["additionalContext"] if out.strip() else ""


def _mdm(root: Path, *args: str, path_env: str) -> subprocess.CompletedProcess:
    env = {k: v for k, v in os.environ.items() if k != "PYTHONPATH"}
    env["PATH"] = path_env
    return subprocess.run(
        ["python3", "-S", ".claude/uaw/mdm.py", *args],  # -S: never an installed harness
        capture_output=True,
        text=True,
        env=env,
        cwd=root,
        timeout=60,
    )


def _snapshot(root: Path) -> dict[str, bytes]:
    return {
        p.relative_to(root).as_posix(): p.read_bytes()
        for p in root.rglob("*")
        if p.is_file() and ".git" not in p.relative_to(root).parts and "__pycache__" not in p.parts
    }


def _session(root: Path, path_env: str) -> None:
    """One whole session through the hooks: start, journal, note, auto index, end, next start."""
    out = _ctx(
        _hook(
            root,
            "now_init.py",
            {"session_id": SID, "source": "startup", "hook_event_name": "SessionStart"},
            path_env,
        )
    )
    assert "journal add --session" in out and ".claude/uaw/mdm.py" in out
    assert (root / ".ai-workspace/state/now.md").is_file()
    r = _mdm(
        root,
        "journal",
        "add",
        "--session",
        SID,
        "ergebnis",
        "Beispielergebnis erreicht.",
        path_env=path_env,
    )
    assert r.returncode == 0, r.stderr
    journal = root / r.stdout.strip()
    assert "Beispielergebnis erreicht." in journal.read_text("utf-8")
    r = _mdm(
        root,
        "new",
        "decision",
        "Beispielteam nutzt Markdown fuer Protokolle",
        "--source",
        f"journal:{r.stdout.strip()}",
        path_env=path_env,
    )
    assert r.returncode == 0, r.stderr
    note = root / r.stdout.strip().split()[-1]
    assert note.is_file()
    _hook(
        root,
        "index_refresh.py",
        {
            "session_id": SID,
            "hook_event_name": "PostToolUse",
            "tool_name": "Write",
            "tool_input": {"file_path": str(note)},
        },
        path_env,
    )
    index_text = (root / ".ai-workspace/knowledge/INDEX.md").read_text("utf-8")
    assert note.stem in index_text
    _hook(
        root,
        "journal_stub.py",
        {"session_id": SID, "reason": "exit", "hook_event_name": "SessionEnd"},
        path_env,
    )
    assert journal.read_text("utf-8").count("· uebergabe") == 1
    nxt = _ctx(
        _hook(
            root,
            "memory_boot.py",
            {"session_id": "f" * 32, "source": "startup", "hook_event_name": "SessionStart"},
            path_env,
        )
    )
    assert journal.name in nxt  # the finished journal waits for merken
    r = _mdm(root, "lint", path_env=path_env)
    assert r.returncode == 0, r.stdout + r.stderr


# --- Weg A: fresh clone --------------------------------------------------------------------------


@needs_sh
def test_weg_a_fresh_clone_runs_without_install(tmp_path):
    root = _fresh_clone(tmp_path / "klon")
    path_env = _python3_only_path(tmp_path)
    assert not (root / ".ai-workspace/state/now.md").exists()  # gitignored, not in a clone
    start = {"session_id": SID, "source": "startup", "hook_event_name": "SessionStart"}
    assert _hook(root, "index_refresh.py", start, path_env) == ""  # committed index is current
    boot = _ctx(_hook(root, "memory_boot.py", start, path_env))
    assert "pflege" in boot  # no maintenance report yet
    assert "pflege" not in _ctx(_hook(root, "memory_boot.py", start, path_env))  # once a day
    _session(root, path_env)
    rep = budget.measure(root)
    assert rep.actual <= BOOT_TARGET_TOKENS + 200 and rep.worst_case <= BOOT_HARD_TOKENS


@needs_sh
def test_launcher_is_silent_without_any_python(tmp_path):
    root = _fresh_clone(tmp_path / "klon")
    empty = tmp_path / "leer"
    empty.mkdir()
    env = {"PATH": str(empty), "CLAUDE_PROJECT_DIR": str(root)}
    proc = subprocess.run(
        [shutil.which("sh") or "sh", str(root / ".claude/hooks/run.sh"), "now_init.py"],
        input="{}",
        capture_output=True,
        text=True,
        env=env,
    )
    assert proc.returncode == 0 and proc.stdout == "" and "no Python" in proc.stderr


# --- Weg B: existing v3.2-style project ----------------------------------------------------------

LEGACY_DECISIONS = """# Decisions

## Aktive Eintraege

- ID: D-2031-02-03-01
- Datum: 2031-02-03
- Entscheidung: Das Projekt Nordlicht speichert Protokolle als Markdown.
- Begruendung: Ein Format, einfache Suche.
- Status: active
- Reversibilitaet: reversible
- Follow-up-Date:
- Supersedes:
"""

LEGACY_QUESTIONS = """# Open Questions

## Aktive Fragen

- ID: Q-2031-02-04-01
- Frage: Wo liegen die Anhaenge des Projekts Nordlicht?
- raised-by: User
- raised-date: 2031-02-04
- blockiert-Decision: D-2031-02-03-01
- Research-Status: none
"""

CURRENT_SESSION = """---
id: current-session
---
# Current Session

## Aktive Aufgabe

Import der Beispieldaten fuer Nordlicht fertigstellen.

## Letzte Aktionen

- 2031-02-05 Parser geschrieben
"""

OWN_AGENTS = """# AGENTS.md — Projekt Nordlicht

Eigene Regeln dieses Projekts (fiktiv):

1. Tests mit `npm test` vor jedem Commit.
2. Boot: `.ai-workspace/state/current-session.md` lesen.
"""

OWN_CLAUDE = """# CLAUDE.md

@AGENTS.md
@.ai-workspace/state/current-session.md

Claude-spezifisch: Antworten auf Deutsch.
"""

OWN_SETTINGS = {
    "permissions": {"deny": ["Read(./.env)"]},
    "hooks": {
        "PostToolUse": [
            {"matcher": "Write|Edit", "hooks": [{"type": "command", "command": "npm run lint"}]}
        ]
    },
}


def _v32_project(root: Path, home: Path) -> Path:
    ws = root / ".ai-workspace"
    (ws / "state").mkdir(parents=True)
    (ws / "knowledge").mkdir()
    (root / "AGENTS.md").write_text(OWN_AGENTS, "utf-8")
    (root / "CLAUDE.md").write_text(OWN_CLAUDE, "utf-8")
    (root / "package.json").write_text('{"name": "nordlicht"}\n', "utf-8")
    (ws / "session-contract.md").write_text(
        "# Session Contract (v3.2, fiktiv angepasst)\n", "utf-8"
    )
    (ws / "state" / "project-index.md").write_text("# Project Index\n\nSlug: nordlicht\n", "utf-8")
    (ws / "state" / "decisions.md").write_text(LEGACY_DECISIONS, "utf-8")
    (ws / "state" / "open-questions.md").write_text(LEGACY_QUESTIONS, "utf-8")
    (ws / "state" / "current-session.md").write_bytes(CURRENT_SESSION.encode())
    (root / ".claude").mkdir()
    (root / ".claude" / "settings.json").write_text(json.dumps(OWN_SETTINGS, indent=2), "utf-8")
    (root / ".gitignore").write_text("node_modules/\n", "utf-8")
    subprocess.run(["git", "init", "-q", str(root)], check=True)
    subprocess.run(
        [
            "git",
            "-C",
            str(root),
            "remote",
            "add",
            "origin",
            "https://github.com/beispiel/nordlicht.git",
        ],
        check=True,
    )
    mem = home / ".claude" / "projects" / adopt.automemory.project_slug(str(root.resolve()))
    (mem / "memory").mkdir(parents=True)
    (mem / "memory" / "MEMORY.md").write_text("- [Kurz](kurz.md) — kurz antworten\n", "utf-8")
    (mem / "memory" / "kurz.md").write_text("Der Nutzer mag kurze Antworten.\n", "utf-8")
    return mem / "memory"


def test_weg_b_adopt_dry_run_changes_nothing(tmp_path):
    root, home = tmp_path / "nordlicht", tmp_path / "home"
    root.mkdir()
    _v32_project(root, home)
    before = _snapshot(root)
    res = adopt.adopt(root, dry_run=True, home=home)
    assert _snapshot(root) == before
    assert any(s.path == "AGENTS.md" and s.action == "merged" for s in res.steps)
    assert res.automemory is not None


def test_weg_b_adopt_is_complete_lossless_and_idempotent(tmp_path):
    root, home = tmp_path / "nordlicht", tmp_path / "home"
    root.mkdir()
    mem = _v32_project(root, home)
    mem_before = {p.name: p.read_bytes() for p in mem.iterdir()}
    res = adopt.adopt(root, import_automemory=True, home=home, today="2031-02-06")
    assert res.ok, adopt.render(res, root)
    ws = root / ".ai-workspace"

    # own content kept, block added once, v3.2 import switched to now.md
    agents = (root / "AGENTS.md").read_text("utf-8")
    assert agents.startswith(OWN_AGENTS) and agents.count(adopt.BEGIN) == 1
    claude = (root / "CLAUDE.md").read_text("utf-8")
    assert "Antworten auf Deutsch." in claude and claude.count("@AGENTS.md") == 1
    assert "current-session.md" not in claude and claude.count("@.ai-workspace/state/now.md") == 1
    assert "@.ai-workspace/knowledge/INDEX.md" in claude
    assert any(s.path == "AGENTS.md" and "current-session" in s.detail for s in res.steps)
    # the project's own policy and project index are kept and reported
    assert "fiktiv angepasst" in (ws / "session-contract.md").read_text("utf-8")
    assert any(s.action == "kept" and s.path.endswith("session-contract.md") for s in res.steps)
    assert "nordlicht" in (ws / "state/project-index.md").read_text("utf-8")
    # settings merged: own hook and permissions stay, memory hooks + auto-memory off added
    settings = json.loads((root / ".claude/settings.json").read_text("utf-8"))
    assert settings["permissions"] == OWN_SETTINGS["permissions"]
    assert settings["autoMemoryEnabled"] is False
    cmds = json.dumps(settings["hooks"])
    assert "npm run lint" in cmds and cmds.count("index_refresh.py") == 3
    # migrations: live state, registers, auto-memory
    assert "Import der Beispieldaten" in (ws / "state/now.md").read_text("utf-8")
    assert not (ws / "state/current-session.md").exists()
    migrated = list((ws / "journal").glob("*/*/*-migration.md"))
    assert len(migrated) == 1 and CURRENT_SESSION.encode() in migrated[0].read_bytes()
    assert list((ws / "knowledge/decision").glob("dec-*.md"))
    assert "GENERIERT" in (ws / "state/decisions.md").read_text("utf-8")
    assert list((ws / "archive").glob("*/state-decisions.md"))
    assert any("automemory:kurz.md" in p.read_text("utf-8") for p in (ws / "journal").rglob("*.md"))
    assert {p.name: p.read_bytes() for p in mem.iterdir()} == mem_before
    # git files, CI, engine, foundation content stays out
    assert ".ai-workspace/state/now.md" in (root / ".gitignore").read_text("utf-8")
    assert "node_modules/" in (root / ".gitignore").read_text("utf-8")
    assert "merge=union" in (root / ".gitattributes").read_text("utf-8")
    assert (root / ".github/workflows/uaw-memory.yml").is_file()
    assert (root / ".claude/uaw/harness/mdmemory/__main__.py").is_file()
    assert not list((ws / "knowledge/decision").glob("dec-2026-*"))
    # lint clean, budget inside the hard limit
    assert [f for f in lint.run(root) if f.level == "E"] == []
    assert res.budget is not None and res.budget.worst_case <= BOOT_HARD_TOKENS

    # second run: nothing changes
    snap = _snapshot(root)
    again = adopt.adopt(root, import_automemory=True, home=home, today="2031-02-07")
    assert again.changed == [], adopt.render(again, root)
    assert _snapshot(root) == snap


def test_weg_b_upgrade_updates_untouched_files_and_keeps_edited_ones(tmp_path):
    root, home = tmp_path / "nordlicht", tmp_path / "home"
    root.mkdir()
    _v32_project(root, home)
    adopt.adopt(root, home=home)
    manifest = root / adopt.MANIFEST
    data = json.loads(manifest.read_text("utf-8"))
    untouched, edited = ".claude/hooks/memory_boot.py", ".claude/skills/merken/SKILL.md"
    old = b"# aeltere Fassung (fiktiv)\n"
    (root / untouched).write_bytes(old)  # as shipped by an older adopt, never edited
    data["files"][untouched] = adopt._sha(old)
    manifest.write_text(json.dumps(data, indent=2) + "\n", "utf-8")
    (root / edited).write_text("# vom Projekt angepasst\n", "utf-8")
    res = adopt.adopt(root, home=home)
    assert (root / untouched).read_bytes() != old
    assert (root / edited).read_text("utf-8") == "# vom Projekt angepasst\n"
    assert any(s.action == "updated" and s.path == untouched for s in res.steps)
    assert any(s.action == "kept" and s.path == edited for s in res.steps)


@needs_sh
def test_weg_b_session_runs_on_the_vendored_engine(tmp_path):
    root, home = tmp_path / "nordlicht", tmp_path / "home"
    root.mkdir()
    _v32_project(root, home)
    assert adopt.adopt(root, home=home).ok
    assert not (root / "src").exists()  # no harness in the project: the vendored copy runs
    _session(root, _python3_only_path(tmp_path))


def test_adopt_refuses_the_foundation_itself():
    with pytest.raises(adopt.AdoptError):
        adopt.adopt(REPO_ROOT, dry_run=True)


# --- registrations stay consistent ---------------------------------------------------------------


def test_every_hook_command_goes_through_the_launcher():
    settings = json.loads((REPO_ROOT / ".claude/settings.json").read_text("utf-8"))
    registered = set()
    for event, entries in settings["hooks"].items():
        for entry in entries:
            for hook in entry["hooks"]:
                cmd = hook["command"]
                assert cmd.startswith('sh "$CLAUDE_PROJECT_DIR/.claude/hooks/run.sh" '), cmd
                script = cmd.rsplit(" ", 1)[-1]
                assert (REPO_ROOT / ".claude/hooks" / script).is_file()
                registered.add((event, entry.get("matcher"), script))
    assert set(adopt.HOOKS) <= registered  # adopt registers exactly what the foundation uses
    flags = json.loads((REPO_ROOT / ".claude/automation.flags.json").read_text("utf-8"))
    assert all(flags[name] is True for name in adopt.FLAGS)
    codex = (REPO_ROOT / ".codex/hooks.json").read_text("utf-8")
    assert 'python \\"' not in codex and "run.sh" in codex


def test_adopt_ships_every_file_the_hooks_import():
    for name in adopt.HOOK_FILES:
        assert (REPO_ROOT / ".claude/hooks" / name).is_file()
    hooks = {p.name for p in (REPO_ROOT / ".claude/hooks").glob("*.py")}
    for script in {s for _, _, s in adopt.HOOKS}:
        assert script in hooks and script in adopt.HOOK_FILES

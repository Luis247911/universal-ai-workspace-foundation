"""Phase 4: maintenance report (skill pflege), memory contract, global namespace, recall set.

All fixture content is fictional.
"""

from __future__ import annotations

import json
import re
import shutil
import sys
from datetime import datetime
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

from harness.mdmemory import create, index, journal, report  # noqa: E402
from harness.mdmemory.__main__ import main  # noqa: E402
from harness.mdmemory.workspace import (  # noqa: E402
    GLOBAL_ENV,
    GlobalNamespaceError,
    global_root,
)

TODAY = "2031-09-01"


def _ws(tmp_path: Path, name: str = "ws") -> Path:
    root = tmp_path / name
    shutil.copytree(REPO_ROOT / ".ai-workspace" / "templates", root / ".ai-workspace" / "templates")
    for d in ("state", "knowledge", "journal"):
        (root / ".ai-workspace" / d).mkdir(parents=True, exist_ok=True)
    return root


def _note(root: Path, title: str, typ: str = "preference", day: str = "2031-06-01", **meta):
    note = create.skeleton(root, typ, title, source="user:test", day=day)
    note.meta.update(meta)
    note.path.parent.mkdir(parents=True, exist_ok=True)
    note.path.write_text(note.render(), encoding="utf-8")
    return note.id


def _snapshot(root: Path, sub: str) -> dict[str, bytes]:
    base = root / ".ai-workspace" / sub
    return {str(p.relative_to(base)): p.read_bytes() for p in base.rglob("*") if p.is_file()}


def test_report_finds_stale_orphans_duplicates_and_pending(tmp_path):
    root = _ws(tmp_path)
    stale = _note(root, "Wochentreffen ist dienstags", review_after="2031-08-01")
    old = _note(root, "Ablage im Projektordner", last_confirmed="2030-12-01")
    dup_a = _note(root, "Antworten kurz halten bitte")
    dup_b = _note(root, "Antworten bitte kurz halten")
    linked = _note(root, "Verlinkte Notiz", links=[stale])
    young = _note(root, "Ganz neue Notiz", day="2031-08-25")
    when = datetime(2031, 8, 30, 9, 0)
    jpath, _ = journal.ensure(root, session_id="f" * 32, when=when, tool="test")
    journal.append(jpath, "offen", "Fiktive offene Frage.", when)
    index.write(root)
    rep = report.build(root, today=TODAY)
    assert {n.id for n, _ in rep.stale} == {stale, old}
    orphan_ids = {n.id for n in rep.orphans}
    assert linked not in orphan_ids and stale not in orphan_ids and young not in orphan_ids
    assert dup_a in orphan_ids
    assert [{a.id, b.id} for _, a, b in rep.duplicates] == [{dup_a, dup_b}]
    assert [p.path for p in rep.pending] == [jpath]
    assert rep.rollups == [jpath.parent / "_rollup.md"]
    text = report.render(root, rep)
    for heading in ("## Lint", "## Veraltet", "## Waisen", "## Duplikat", "## Nicht konsol",
                    "## Boot-Budget", "## Monats-Rollup"):
        assert heading in text


def test_report_never_changes_notes_and_second_run_is_stable(tmp_path):
    root = _ws(tmp_path)
    _note(root, "Wochentreffen ist dienstags", review_after="2031-08-01")
    index.write(root)
    before = _snapshot(root, "knowledge")
    first = report.render(root, report.build(root, today=TODAY))
    second = report.render(root, report.build(root, today=TODAY))
    assert _snapshot(root, "knowledge") == before
    assert first.replace("neu erzeugt", "") == second.replace("neu erzeugt", "")


def test_report_cli_writes_into_gitignored_scratch(tmp_path, capsys):
    root = _ws(tmp_path)
    assert main(["--root", str(root), "report", "--date", TODAY]) == 1  # INDEX.md missing
    assert "generated file out of date" in capsys.readouterr().out
    index.write(root)
    assert main(["--root", str(root), "report", "--write", "--date", TODAY]) == 0
    path = root / ".ai-workspace" / "scratch" / "maintenance" / f"{TODAY}-pflege.md"
    assert path.is_file()
    assert ".ai-workspace/scratch/" in (REPO_ROOT / ".gitignore").read_text("utf-8")


def test_global_namespace_is_off_by_default_and_separate_when_on(tmp_path, monkeypatch):
    with pytest.raises(GlobalNamespaceError, match="is off"):
        global_root({})
    with pytest.raises(GlobalNamespaceError, match="no workspace"):
        global_root({GLOBAL_ENV: str(tmp_path / "fehlt")})
    monkeypatch.delenv(GLOBAL_ENV, raising=False)
    try:
        main(["--global", "index"])
    except SystemExit as exc:
        assert "global namespace is off" in str(exc)
    else:  # pragma: no cover
        raise AssertionError("--global must fail while the namespace is off")
    project, glob = _ws(tmp_path, "projekt"), _ws(tmp_path, "global")
    monkeypatch.setenv(GLOBAL_ENV, str(glob))
    assert global_root() == glob
    assert main(["--global", "new", "preference", "Antworten kurz halten", "--source",
                 "user:test"]) == 0
    assert main(["--global", "index"]) == 0
    assert list((glob / ".ai-workspace" / "knowledge" / "preference").glob("*.md"))
    assert not (project / ".ai-workspace" / "knowledge" / "preference").exists()


def test_claude_auto_memory_is_off_in_project_settings():
    settings = json.loads((REPO_ROOT / ".claude" / "settings.json").read_text("utf-8"))
    assert settings["autoMemoryEnabled"] is False


def test_memory_contract_states_the_five_defaults():
    text = (REPO_ROOT / ".ai-workspace" / "memory-contract.md").read_text("utf-8")
    needles = (
        "Markdown in git ist kanonisch", "autoMemoryEnabled", "CLAUDE_CODE_DISABLE_AUTO_MEMORY",
        "separates Repo", "UAW_GLOBAL_MEMORY_DIR", "mcp-proposal", "Besitz-Tabelle",
        "Ladevertrag", "Schreibwege", "90 %",
    )
    for needle in needles:
        assert needle in text, needle
    for name in ("memory-contract.md",):
        assert name in (REPO_ROOT / "AGENTS.md").read_text("utf-8")
        assert name in (REPO_ROOT / ".ai-workspace" / "context-policy.md").read_text("utf-8")


def test_recall_set_template_has_thirty_questions():
    text = (REPO_ROOT / ".ai-workspace" / "templates" / "recall-set.md").read_text("utf-8")
    rows = re.findall(r"^\| (\d+) \|", text, flags=re.M)
    assert [int(r) for r in rows] == list(range(1, 31))
    assert "90 %" in text

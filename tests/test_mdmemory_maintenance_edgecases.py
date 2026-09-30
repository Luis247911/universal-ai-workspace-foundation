"""Edge cases of the phase-4 maintenance report and global namespace found in review: hard boot
limit in the exit code, sensitive titles, a read-only stdout report, note sources as links,
duplicates with an open conflict, and a global namespace that can never be the project.
All content is fictional."""

from __future__ import annotations

from datetime import datetime
from pathlib import Path

import pytest

from harness.mdmemory import consolidate, create, index, journal, report
from harness.mdmemory.__main__ import main
from harness.mdmemory.workspace import GLOBAL_ENV, GlobalNamespaceError, global_root

TODAY = "2031-08-30"
OLD = "2031-01-01"


def _ws(tmp_path: Path, name: str = "ws") -> Path:
    root = tmp_path / name
    for d in ("state", "knowledge", "journal", "templates"):
        (root / ".ai-workspace" / d).mkdir(parents=True, exist_ok=True)
    return root


def test_report_exit_code_reflects_the_hard_boot_limit(tmp_path):
    root = _ws(tmp_path)
    index.write(root)
    (root / "AGENTS.md").write_text("x" * 40_000, encoding="utf-8")
    assert main(["--root", str(root), "report", "--date", TODAY]) == 1


def test_report_shows_no_title_of_sensitive_notes(tmp_path, capsys):
    root = _ws(tmp_path)
    create.create(root, "person", "Erika Beispiel Arzttermin", source="user:x", day=OLD)
    index.write(root)
    main(["--root", str(root), "report", "--date", TODAY])
    assert "Erika" not in capsys.readouterr().out


def test_stdout_report_writes_nothing(tmp_path):
    root = _ws(tmp_path)
    j, _ = journal.ensure(root, session_id="a" * 32, when=datetime(2031, 8, 1, 9, 0))
    journal.append(j, "ergebnis", "Beispiel")
    index.write(root)
    before = sorted(p for p in root.rglob("*") if p.is_file())
    main(["--root", str(root), "report", "--date", TODAY])
    assert sorted(p for p in root.rglob("*") if p.is_file()) == before


def test_note_sources_count_as_links_and_conflicts_silence_duplicates(tmp_path):
    root = _ws(tmp_path)
    a = create.create(root, "concept", "Beispielbegriff Alpha", source="user:x", day=OLD).stem
    b = create.create(root, "concept", "Folgebegriff Beta", source=f"note:{a}", day=OLD).stem
    orphans = {n.id for n in report.orphans(consolidate.load_notes(root), TODAY)}
    assert a not in orphans and b not in orphans
    c = create.create(root, "preference", "Antworten kurz halten bitte", source="user:x", day=OLD)
    d = create.create(root, "preference", "Antworten bitte kurz halten", source="user:x", day=OLD)
    assert report.duplicates(consolidate.load_notes(root))
    consolidate.conflict(root, c.stem, d.stem, title="Welche gilt?", source="user:x", day=OLD)
    assert report.duplicates(consolidate.load_notes(root)) == []


def test_global_namespace_refuses_relative_paths_and_the_project(tmp_path):
    project = _ws(tmp_path, "projekt")
    with pytest.raises(GlobalNamespaceError, match="absolute"):
        global_root({GLOBAL_ENV: "."}, project=project)
    with pytest.raises(GlobalNamespaceError, match="outside the project"):
        global_root({GLOBAL_ENV: str(project)}, project=project)
    glob = _ws(tmp_path, "global")
    assert global_root({GLOBAL_ENV: str(glob)}, project=project) == glob.resolve()


def test_journal_can_point_at_a_global_note(tmp_path, monkeypatch):
    project, glob = _ws(tmp_path, "projekt"), _ws(tmp_path, "global")
    monkeypatch.setenv(GLOBAL_ENV, str(glob))
    note = create.create(glob, "preference", "Kurz antworten", source="user:x", day=OLD).stem
    j, _ = journal.ensure(project, session_id="b" * 32, when=datetime(2031, 8, 1, 9, 0))
    assert consolidate.mark(project, j, [f"global:{note}"])
    assert consolidate.journal_refs(project) == []
    with pytest.raises(KeyError):
        consolidate.mark(project, j, ["global:pref-2031-01-01-gibt-es-nicht-0000"])

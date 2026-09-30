"""Edge cases of the phase-3 consolidation helpers and memory hooks found in review: own journals
across midnight, journals of sessions still running elsewhere, idempotent ``conflict``, supersede
cycles, date validation, and a journal stub that is written once. All content is fictional."""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path

import pytest

from harness.mdmemory import consolidate, create, journal
from harness.mdmemory.__main__ import main

REPO_ROOT = Path(__file__).resolve().parents[1]
HOOKS = REPO_ROOT / ".claude" / "hooks"
DAY = "2031-05-01"


def _ws(tmp_path: Path, flags: dict | None = None) -> Path:
    root = tmp_path / "ws"
    for d in ("state", "knowledge", "journal"):
        (root / ".ai-workspace" / d).mkdir(parents=True, exist_ok=True)
    (root / ".claude").mkdir()
    (root / ".claude" / "automation.flags.json").write_text(json.dumps(flags or {}), "utf-8")
    shutil.copytree(REPO_ROOT / "src", root / "src")
    return root


def _note(root: Path, title: str) -> str:
    return create.create(root, "preference", title, source="user:2031-05-01", day=DAY).stem


def _hook(name: str, root: Path, payload: dict) -> str:
    env = dict(os.environ, CLAUDE_PROJECT_DIR=str(root))
    proc = subprocess.run(
        [sys.executable, str(HOOKS / name)],
        input=json.dumps(payload),
        capture_output=True,
        text=True,
        env=env,
        check=True,
    )
    return proc.stdout


def test_memory_boot_never_lists_the_own_journal_from_yesterday(tmp_path):
    root = _ws(tmp_path, {"memory_boot": True})
    sid = "abcd1234-0000-4000-8000-000000000000"
    own, _ = journal.ensure(root, session_id=sid, when=datetime(2031, 5, 1, 23, 50))
    journal.append(own, "ergebnis", "Beispielergebnis")
    journal.append(own, "uebergabe", "Session beendet.")  # finished: only the own-check hides it
    assert _hook("memory_boot.py", root, {"session_id": sid, "source": "resume"}) == ""
    assert "abcd1234" in _hook("memory_boot.py", root, {"session_id": "9" * 32, "source": "resume"})


def test_running_journal_of_another_session_is_not_pending(tmp_path):
    root = _ws(tmp_path)
    running, _ = journal.ensure(root, session_id="1" * 32, when=datetime(2031, 5, 1, 9, 0))
    journal.append(running, "ergebnis", "laeuft noch")
    assert consolidate.pending(root, today=DAY) == []
    assert [p.path for p in consolidate.pending(root, today="2031-05-02")] == [running]
    assert consolidate.pending(root, today=DAY, include_running=True)
    journal.append(running, "uebergabe", "Session beendet.")
    assert [p.path for p in consolidate.pending(root, today=DAY)] == [running]


def test_conflict_is_idempotent_and_needs_two_notes(tmp_path):
    root = _ws(tmp_path)
    a, b = _note(root, "Beispielteam trifft sich montags"), _note(root, "Treffen ist freitags")
    first = consolidate.conflict(root, a, b, title="Welcher Tag?", source="user:x", day=DAY)
    again = consolidate.conflict(root, b, a, title="Anderer Titel", source="user:x", day=DAY)
    assert first == again
    with pytest.raises(ValueError):
        consolidate.conflict(root, a, a, title="Selbst?", source="user:x", day=DAY)


def test_supersede_refuses_cycles_and_a_second_change_value(tmp_path):
    root = _ws(tmp_path)
    a, b, c = (_note(root, f"Beispielregel Variante {x}") for x in "ABC")
    consolidate.supersede(root, a, b, change="veraendert", day=DAY)
    with pytest.raises(ValueError):
        consolidate.supersede(root, b, a, change="veraendert", day=DAY)
    with pytest.raises(ValueError):
        consolidate.supersede(root, c, b, change="korrigiert", day=DAY)


def test_cli_rejects_bad_dates_and_reports_unknown_ids_cleanly(tmp_path, capsys):
    root = _ws(tmp_path)
    ref = _note(root, "Beispielpraeferenz kurz antworten")
    with pytest.raises(SystemExit):
        main(["--root", str(root), "confirm", ref, "--date", "2031-5-1"])
    j, _ = journal.ensure(root, session_id="2" * 32, when=datetime(2031, 5, 1, 9, 0))
    rel_j = j.relative_to(root).as_posix()
    assert main(["--root", str(root), "consolidated", rel_j, "dec-gibt-es-nicht"]) == 2
    assert "unknown note ids" in capsys.readouterr().err


def test_consolidated_accepts_aliases_and_root_relative_paths(tmp_path):
    root = _ws(tmp_path)
    p = create.create(
        root, "decision", "Beispielentscheidung", source="user:x", day=DAY, alias="D-2031-05-01-01"
    )
    j, _ = journal.ensure(root, session_id="3" * 32, when=datetime(2031, 5, 1, 9, 0))
    rel_j = j.relative_to(root).as_posix()
    assert main(["--root", str(root), "consolidated", rel_j, "D-2031-05-01-01"]) == 0
    assert f"konsolidiert_zu: [{p.stem}]" in j.read_text("utf-8")


def test_journal_stub_closes_a_journal_once_and_skips_empty_ones(tmp_path):
    root = _ws(tmp_path, {"journal_stub": True})
    sid = "4" * 32
    j, _ = journal.ensure(root, session_id=sid, when=datetime.now())
    before = j.read_text("utf-8")
    _hook("journal_stub.py", root, {"session_id": sid, "reason": "exit"})
    assert j.read_text("utf-8") == before  # no entries yet: nothing appended
    journal.append(j, "ergebnis", "Beispielergebnis")
    for _ in range(3):
        _hook("journal_stub.py", root, {"session_id": sid, "reason": "exit"})
    assert j.read_text("utf-8").count("· uebergabe") == 1


def test_memory_boot_compact_reminder_needs_no_engine(tmp_path):
    root = _ws(tmp_path, {"memory_boot": True})
    shutil.rmtree(root / "src")
    env = {k: v for k, v in os.environ.items() if k != "PYTHONPATH"}
    env["CLAUDE_PROJECT_DIR"] = str(root)
    proc = subprocess.run(
        [sys.executable, "-S", str(HOOKS / "memory_boot.py")],  # -S: no site-packages harness
        input=json.dumps({"session_id": "5" * 32, "source": "compact"}),
        capture_output=True,
        text=True,
        env=env,
        check=True,
    )
    assert "kompaktiert" in proc.stdout

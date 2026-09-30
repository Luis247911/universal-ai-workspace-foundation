"""Phase 3: consolidation helpers (skill ``merken``) and the memory hooks.

Acceptance: idempotent (a second run changes nothing), supersede chains symmetric, no note
without sources. Hooks run as subprocesses against a sandbox, the way Claude Code / Codex call
them. All content is fictional.
"""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

from harness.mdmemory import consolidate, create, index, journal, lint  # noqa: E402
from harness.mdmemory.limits import CLAUDE_SESSION_END_BUDGET_S  # noqa: E402
from harness.mdmemory.notes import load_notes  # noqa: E402

HOOKS = REPO_ROOT / ".claude" / "hooks"
DAY = "2031-05-01"


def _ws(tmp_path: Path, flags: dict | None = None) -> Path:
    root = tmp_path / "ws"
    shutil.copytree(REPO_ROOT / ".ai-workspace" / "templates", root / ".ai-workspace" / "templates")
    for d in ("state", "knowledge", "journal"):
        (root / ".ai-workspace" / d).mkdir(parents=True, exist_ok=True)
    (root / ".claude").mkdir()
    (root / ".claude" / "automation.flags.json").write_text(json.dumps(flags or {}), "utf-8")
    shutil.copytree(REPO_ROOT / "src", root / "src")
    return root


def _note(root: Path, title: str, typ: str = "preference") -> str:
    path = create.create(root, typ, title, source="journal:2031/05/2031-05-01-aaaaaaaa.md", day=DAY)
    return path.stem


def _snapshot(root: Path) -> dict[str, bytes]:
    base = root / ".ai-workspace"
    return {str(p.relative_to(base)): p.read_bytes() for p in base.rglob("*") if p.is_file()}


def _errors(root: Path) -> list[str]:
    index.write(root)
    return [str(f) for f in lint.run(root, today=DAY, check_budget=False) if f.level == "E"]


# --- helpers -------------------------------------------------------------------------------------


def test_supersede_is_symmetric_and_idempotent(tmp_path):
    root = _ws(tmp_path)
    old = _note(root, "Wochentreffen des Beispielteams ist dienstags")
    new = _note(root, "Wochentreffen des Beispielteams ist donnerstags")
    assert len(consolidate.supersede(root, old, new, change="veraendert", day="2031-05-02")) == 2
    before = _snapshot(root)
    assert consolidate.supersede(root, old, new, change="veraendert", day="2031-05-03") == []
    assert _snapshot(root) == before
    o, n = consolidate.find(root, old), consolidate.find(root, new)
    assert o.get("superseded_by") == new and o.get("status") == "superseded"
    assert o.get("valid_until") == DAY
    assert n.items("supersedes") == [old] and n.get("change") == "veraendert"
    assert f"abgeloest durch {new}" in o.body and f"ersetzt {old}" in n.body
    assert _errors(root) == []


def test_supersede_refuses_a_second_successor(tmp_path):
    root = _ws(tmp_path)
    old = _note(root, "Ablage im Projektordner")
    a = _note(root, "Ablage im Archivsystem")
    b = _note(root, "Ablage im Wiki")
    consolidate.supersede(root, old, a, change="korrigiert", day=DAY)
    with pytest.raises(ValueError, match="already superseded"):
        consolidate.supersede(root, old, b, change="korrigiert", day=DAY)
    with pytest.raises(ValueError):
        consolidate.supersede(root, a, b, change="irgendwie", day=DAY)


def test_confirm_touches_only_last_confirmed_once(tmp_path):
    root = _ws(tmp_path)
    ref = _note(root, "Antworten kurz halten")
    assert consolidate.confirm(root, ref, day="2031-06-01")
    n = consolidate.find(root, ref)
    assert n.get("last_confirmed") == "2031-06-01" and n.get("updated") == DAY
    assert consolidate.confirm(root, ref, day="2031-06-01") == []


def test_conflict_creates_a_pinned_question_and_changes_nothing_else(tmp_path):
    root = _ws(tmp_path)
    a = _note(root, "Ablage fuer Anhaenge ist der Projektordner", "concept")
    b = _note(root, "Anhaenge liegen im Archivsystem", "concept")
    before = _snapshot(root)
    path = consolidate.conflict(
        root, a, b, title="Wo liegen Anhaenge?", source="journal:2031/05/x.md", day=DAY
    )
    after = _snapshot(root)
    assert set(after) - set(before) == {str(path.relative_to(root / ".ai-workspace"))}
    assert all(after[k] == v for k, v in before.items())
    q = consolidate.find(root, path.stem)
    assert q.get("kind") == "conflict" and q.pinned and q.items("links") == [a, b]
    assert _errors(root) == []
    idx = (root / ".ai-workspace" / "knowledge" / "INDEX.md").read_text("utf-8")
    assert "Wo liegen Anhaenge?" in idx.split("## Zuletzt")[0]  # pinned section


def test_candidates_rank_the_similar_note_first(tmp_path):
    root = _ws(tmp_path)
    _note(root, "Protokolle des Beispielteams nur als Markdown", "decision")
    _note(root, "Antworten kurz halten")
    top = consolidate.candidates(root, "Beispielteam legt Protokolle in Markdown ab")
    assert top and top[0][1].get("title").startswith("Protokolle")


def _journal(root: Path, sid: str = "b" * 32) -> Path:
    when = datetime(2031, 5, 1, 9, 0)
    path, _ = journal.ensure(root, session_id=sid, when=when, tool="test")
    journal.append(path, "entscheidung", "Protokolle nur noch als Markdown.", when)
    return path


def test_pending_and_mark_are_idempotent(tmp_path):
    root = _ws(tmp_path)
    jpath = _journal(root)
    assert [p.path for p in consolidate.pending(root, today="2031-12-31")] == [jpath]
    ref = _note(root, "Protokolle nur als Markdown", "decision")
    assert consolidate.mark(root, jpath, [ref])
    text = jpath.read_text("utf-8")
    assert "konsolidiert: true" in text and f"konsolidiert_zu: [{ref}]" in text
    assert consolidate.mark(root, jpath, [ref]) is False
    assert jpath.read_text("utf-8") == text
    assert consolidate.pending(root, today="2031-12-31") == []
    with pytest.raises(journal.JournalFrozenError):
        journal.append(jpath, "notiz", "zu spaet")
    with pytest.raises(KeyError):
        consolidate.mark(root, jpath, ["dec-2031-01-01-gibt-es-nicht-0000"])


def test_lint_rejects_journal_pointing_at_missing_note(tmp_path):
    root = _ws(tmp_path)
    jpath = _journal(root)
    text = jpath.read_text("utf-8").replace("konsolidiert_zu: []", "konsolidiert_zu: [dec-x]")
    jpath.write_text(text, "utf-8")
    assert any("konsolidiert_zu: unknown note dec-x" in e for e in _errors(root))


def test_full_consolidation_run_twice_has_no_diff(tmp_path):
    """The mechanical part of one merken pass, run twice: second run is a no-op."""
    root = _ws(tmp_path)
    old = _note(root, "Wochentreffen ist dienstags")

    def run() -> None:
        for p in consolidate.pending(root):
            new = next((n.id for n in load_notes(root) if "donnerstags" in n.get("title")), None)
            new = new or _note(root, "Wochentreffen ist donnerstags")
            consolidate.supersede(root, old, new, change="veraendert", day=DAY)
            consolidate.mark(root, p.path, [new])
        index.write(root)

    _journal(root)
    run()
    first = _snapshot(root)
    run()
    assert _snapshot(root) == first
    assert _errors(root) == []
    assert all(n.items("sources") for n in load_notes(root))


# --- hooks ---------------------------------------------------------------------------------------


def _hook(name: str, root: Path, stdin: dict, *args: str) -> tuple[str, int, float]:
    env = {**os.environ, "CLAUDE_PROJECT_DIR": str(root)}
    t0 = time.perf_counter()
    proc = subprocess.run(
        [sys.executable, str(HOOKS / name), *args],
        input=json.dumps(stdin),
        capture_output=True,
        text=True,
        env=env,
    )
    return proc.stdout, proc.returncode, time.perf_counter() - t0


@pytest.mark.parametrize("name", ["journal_stub.py", "memory_boot.py", "precompact_reminder.py"])
def test_memory_hooks_inert_when_flag_off(tmp_path, name):
    root = _ws(tmp_path, flags={})
    _journal(root)
    before = _snapshot(root)
    out, code, _ = _hook(name, root, {"session_id": "b" * 32, "source": "compact"})
    assert (out, code) == ("", 0)
    assert _snapshot(root) == before


def test_journal_stub_appends_once_per_end_and_is_fast(tmp_path):
    root = _ws(tmp_path, flags={"journal_stub": True})
    jpath = _journal(root)
    out, code, took = _hook("journal_stub.py", root, {"session_id": "b" * 32, "reason": "exit"})
    assert (out, code) == ("", 0)
    text = jpath.read_text("utf-8")
    assert text.count("· uebergabe") == 1 and "Grund: exit" in text
    assert took < CLAUDE_SESSION_END_BUDGET_S  # includes interpreter start


def test_journal_stub_creates_nothing_and_respects_frozen_journals(tmp_path):
    root = _ws(tmp_path, flags={"journal_stub": True})
    before = _snapshot(root)
    _hook("journal_stub.py", root, {"session_id": "c" * 32})
    assert _snapshot(root) == before  # no journal -> nothing created
    jpath = _journal(root)
    ref = _note(root, "Protokolle nur als Markdown", "decision")
    consolidate.mark(root, jpath, [ref])
    frozen = jpath.read_text("utf-8")
    _hook("journal_stub.py", root, {"session_id": "b" * 32}, "--tool", "codex")
    assert jpath.read_text("utf-8") == frozen


def test_memory_boot_lists_other_pending_journals(tmp_path):
    root = _ws(tmp_path, flags={"memory_boot": True})
    other = _journal(root, sid="d" * 32)
    journal.append(other, "uebergabe", "Session beendet.")  # finished (journal_stub)
    out, code, _ = _hook("memory_boot.py", root, {"session_id": "e" * 32, "source": "startup"})
    assert code == 0
    ctx = json.loads(out)["hookSpecificOutput"]["additionalContext"]
    assert "1 Journal(e) noch nicht konsolidiert" in ctx and "dddddddd" in ctx
    assert len(ctx) < 2_000


def test_memory_boot_silent_without_pending_but_reminds_after_compact(tmp_path):
    root = _ws(tmp_path, flags={"memory_boot": True})
    out, _, _ = _hook("memory_boot.py", root, {"session_id": "e" * 32, "source": "startup"})
    assert out == ""
    out, _, _ = _hook("memory_boot.py", root, {"session_id": "e" * 32, "source": "compact"})
    assert "kompaktiert" in json.loads(out)["hookSpecificOutput"]["additionalContext"]


def test_precompact_reminder_only_messages_the_user(tmp_path):
    root = _ws(tmp_path, flags={"precompact_reminder": True})
    out, code, _ = _hook("precompact_reminder.py", root, {"trigger": "manual"})
    payload = json.loads(out)
    assert code == 0 and set(payload) == {"systemMessage"}  # never blocks, no model context
    assert "merken" in payload["systemMessage"]


def test_hook_registrations_match_flags_and_scripts():
    settings = json.loads((REPO_ROOT / ".claude" / "settings.json").read_text("utf-8"))
    codex = json.loads((REPO_ROOT / ".codex" / "hooks.json").read_text("utf-8"))
    flags = json.loads((REPO_ROOT / ".claude" / "automation.flags.json").read_text("utf-8"))
    for name in ("journal_stub", "memory_boot", "precompact_reminder"):
        assert flags[name] is True
        assert (HOOKS / f"{name}.py").is_file()
        assert name in json.dumps(settings["hooks"]) and name in json.dumps(codex["hooks"])
    for event in ("SessionStart", "SessionEnd", "PreCompact"):
        assert event in settings["hooks"] and event in codex["hooks"]
    for group in codex["hooks"]["SessionEnd"]:
        assert all(h["timeout"] <= 3 for h in group["hooks"])  # Codex SessionEnd max 3 s
    for group in codex["hooks"].values():
        for entry in group:
            for h in entry["hooks"]:
                assert "--tool codex" in h["command"] and "git rev-parse" in h["command"]

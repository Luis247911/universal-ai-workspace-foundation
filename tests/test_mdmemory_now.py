"""harness.mdmemory: frontmatter subset, session journal, per-worktree now.md (trim + migrate)."""

from __future__ import annotations

from datetime import datetime
from pathlib import Path

import pytest

from harness.mdmemory import frontmatter, journal, now
from harness.mdmemory.__main__ import main as cli
from harness.mdmemory.limits import NOW_MAX_BYTES, estimate_tokens

REPO_ROOT = Path(__file__).resolve().parents[1]
WHEN = datetime(2026, 9, 30, 14, 5)


def _ws(tmp_path: Path) -> Path:
    (tmp_path / ".ai-workspace" / "state").mkdir(parents=True)
    tpl = tmp_path / ".ai-workspace" / "templates"
    tpl.mkdir()
    for name in ("journal-entry.md", "session-state.md"):
        src = REPO_ROOT / ".ai-workspace" / "templates" / name
        (tpl / name).write_text(src.read_text(encoding="utf-8"), encoding="utf-8")
    return tmp_path


# --- frontmatter ---------------------------------------------------------------------------------

def test_frontmatter_round_trip_is_lossless_and_stable():
    meta = {
        "id": "dec-2026-09-30-x",
        "title": 'Ein "Zitat": mit Doppelpunkt',
        "aliases": ["D-2026-06-07-01", "a, b", ""],
        "empty": "",
        "flag": "true",
        "list0": [],
    }
    text = frontmatter.dump(meta, "Body\n", order=["id", "title"])
    parsed, body = frontmatter.parse(text)
    assert body == "Body\n"
    assert parsed == meta
    assert frontmatter.dump(parsed, body, order=["id", "title"]) == frontmatter.dump(
        frontmatter.parse(frontmatter.dump(parsed, body, order=["id", "title"]))[0],
        body,
        order=["id", "title"],
    )


def test_frontmatter_set_scalar_keeps_other_lines():
    text = "---\nid: x  # kommentar\nkonsolidiert: false\n---\nbody\n"
    out = frontmatter.set_scalar(text, "konsolidiert", "true")
    assert out == "---\nid: x  # kommentar\nkonsolidiert: true\n---\nbody\n"


def test_estimate_tokens_uses_2_5_chars_per_token():
    assert estimate_tokens("x" * 25) == 10
    assert estimate_tokens("x" * 26) == 11


# --- journal -------------------------------------------------------------------------------------

def test_journal_one_file_per_session_never_overwritten(tmp_path):
    root = _ws(tmp_path)
    path, created = journal.ensure(root, session_id="A1B2C3D4-0000", when=WHEN, tool="codex")
    assert created and path.name == "2026-09-30-a1b2c3d4.md"
    assert path.parent == root / ".ai-workspace" / "journal" / "2026" / "09"
    meta, _ = frontmatter.parse(path.read_text(encoding="utf-8"))
    assert meta and meta["id"] == "j-2026-09-30-a1b2c3d4" and meta["tool"] == "codex"
    path.write_text(path.read_text(encoding="utf-8") + "eigener Text\n", encoding="utf-8")
    again, created2 = journal.ensure(root, session_id="A1B2C3D4-0000", when=WHEN)
    assert again == path and not created2
    assert "eigener Text" in path.read_text(encoding="utf-8")


def test_journal_append_only_and_frozen_after_consolidation(tmp_path):
    root = _ws(tmp_path)
    path, _ = journal.ensure(root, session_id="deadbeef", when=WHEN)
    before = path.read_text(encoding="utf-8")
    journal.append(path, "entscheidung", "Index wird generiert.", WHEN)
    after = path.read_text(encoding="utf-8")
    assert after.startswith(before)
    assert after.endswith("### 14:05 · entscheidung\n\nIndex wird generiert.\n")
    path.write_text(frontmatter.set_scalar(after, "konsolidiert", "true"), encoding="utf-8")
    with pytest.raises(journal.JournalFrozenError):
        journal.append(path, "notiz", "zu spaet", WHEN)


def test_short_id_falls_back_to_hash():
    assert journal.short_id("0badc0de-1111") == "0badc0de"
    assert len(journal.short_id("manual")) == 8


# --- now.md --------------------------------------------------------------------------------------

def test_now_template_fits_the_cap():
    text = (REPO_ROOT / ".ai-workspace" / "templates" / "session-state.md").read_text("utf-8")
    assert len(text.encode("utf-8")) <= NOW_MAX_BYTES
    assert "## Letzte Aktionen" in text


def test_now_ensure_creates_once(tmp_path):
    root = _ws(tmp_path)
    assert now.ensure(root) is True
    (root / ".ai-workspace" / "state" / "now.md").write_text("mein stand\n", encoding="utf-8")
    assert now.ensure(root) is False
    assert (root / ".ai-workspace" / "state" / "now.md").read_text("utf-8") == "mein stand\n"


def test_now_trim_moves_oldest_actions_losslessly(tmp_path):
    root = _ws(tmp_path)
    head = (root / ".ai-workspace" / "templates" / "session-state.md").read_text("utf-8")
    head = head.split("## Letzte Aktionen")[0]
    actions = [f"- 2026-09-{i % 28 + 1:02d} aktion {i:03d} " + "y" * 60 for i in range(60)]
    text = head + "## Letzte Aktionen (neueste oben, max. 10)\n\n" + "\n".join(actions) + "\n"
    path = root / ".ai-workspace" / "state" / "now.md"
    path.write_text(text, encoding="utf-8")
    res = now.trim(root, session_id="feedface", when=WHEN)
    assert res.changed and not res.snapshot and res.after <= NOW_MAX_BYTES
    kept = path.read_text(encoding="utf-8")
    jtext = journal.journal_path(root, WHEN, "feedface").read_text(encoding="utf-8")
    for line in actions:  # every action is either still in now.md or in the journal
        assert (line in kept) != (line in jtext)
    assert actions[0] in kept and actions[-1] in jtext


def test_now_trim_snapshot_fallback_keeps_full_text(tmp_path):
    root = _ws(tmp_path)
    big = "---\nid: now\n---\n# Now\n\n## Aktive Aufgabe\n\n" + "\n".join(
        f"zeile {i} " + "z" * 90 for i in range(80)
    )
    path = root / ".ai-workspace" / "state" / "now.md"
    path.write_text(big, encoding="utf-8")
    res = now.trim(root, session_id="c0ffee00", when=WHEN)
    assert res.snapshot and res.after <= NOW_MAX_BYTES
    assert big in journal.journal_path(root, WHEN, "c0ffee00").read_text(encoding="utf-8")
    assert path.read_text(encoding="utf-8").startswith("---\nid: now\n---\n")


def test_now_trim_noop_when_small(tmp_path):
    root = _ws(tmp_path)
    now.ensure(root)
    res = now.trim(root, session_id="x", when=WHEN)
    assert not res.changed
    assert not (root / ".ai-workspace" / "journal").exists()


def test_migrate_legacy_current_session_round_trip(tmp_path):
    root = _ws(tmp_path)
    legacy = root / ".ai-workspace" / "state" / "current-session.md"
    content = "---\nid: current-session\n---\n# Current Session\n\n## 2. Active Task\n\nX\n"
    legacy.write_text(content, encoding="utf-8")
    target = now.migrate(root, when=WHEN, remove_legacy=True)
    assert target.name == "2026-09-30-migration.md"
    assert content in target.read_text(encoding="utf-8")  # byte-identical copy
    assert not legacy.exists()
    assert (root / ".ai-workspace" / "state" / "now.md").read_text("utf-8") == content


def test_cli_now_and_journal(tmp_path, capsys):
    root = _ws(tmp_path)
    assert cli(["--root", str(root), "now", "ensure"]) == 0
    assert cli(["--root", str(root), "now", "trim"]) == 0
    assert cli(["--root", str(root), "journal", "new", "--session", "12345678-aa"]) == 0
    out = capsys.readouterr().out
    assert "state/now.md" in out and "-12345678.md" in out

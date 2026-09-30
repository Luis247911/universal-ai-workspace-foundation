"""Edge cases of the phase-1 memory core found in review: frontmatter escapes, trim limits,
session ids, journals across midnight, and a byte-exact, idempotent ``now migrate``."""

from __future__ import annotations

import hashlib
import signal
from datetime import datetime
from pathlib import Path

import pytest

from harness.mdmemory import frontmatter, journal, now
from harness.mdmemory.workspace import journal_dir, legacy_session_path, now_path

START = datetime(2031, 3, 4, 23, 58)


def _ws(tmp_path: Path) -> Path:
    (tmp_path / ".ai-workspace" / "state").mkdir(parents=True)
    return tmp_path


@pytest.mark.parametrize(
    "value",
    ['Kabel 5" #2', 'a"b #c', "ende \\", "x # y", "'quoted' # z", 'mix "q" \\ # # ok'],
)
def test_frontmatter_round_trip_with_quotes_hashes_and_backslashes(value):
    meta = {"title": value, "tags": [value, "b"]}
    parsed, _ = frontmatter.parse(frontmatter.dump(meta, "body\n"))
    assert parsed == meta


def test_frontmatter_bom_and_blank_after_fence():
    text = "﻿--- \nid: a\n---  \nbody\n"
    meta, body = frontmatter.parse(text)
    assert meta == {"id": "a"} and body == "body\n"


def test_frontmatter_rejects_duplicate_keys_and_line_breaks():
    with pytest.raises(frontmatter.FrontmatterError):
        frontmatter.parse("---\nid: a\nid: b\n---\n")
    with pytest.raises(frontmatter.FrontmatterError):
        frontmatter.dump({"title": "a\nid: x"}, "")


def test_short_id_uses_random_part_of_uuid7():
    a = "0199a213-81c0-7abc-8def-0123456789ab"
    b = "0199a213-f3e1-7aaa-9bbb-fedcba987654"
    assert journal.short_id(a) != journal.short_id(b)
    assert journal.short_id("3f2a9c1e-0000-4000-8000-000000000000") == "3f2a9c1e"


def test_manual_session_ids_are_random():
    assert journal.new_session_id() != journal.new_session_id()


def test_journal_survives_midnight_and_continues_after_freeze(tmp_path):
    root = _ws(tmp_path)
    sid = "aaaabbbb-cccc-4ddd-8eee-ffff00001111"
    first, created = journal.ensure(root, session_id=sid, when=START)
    assert created
    again, created = journal.ensure(root, session_id=sid, when=datetime(2031, 3, 5, 0, 5))
    assert again == first and not created  # same file after midnight
    frozen = first.read_text(encoding="utf-8").replace("konsolidiert: false", "konsolidiert: true")
    first.write_text(frozen, encoding="utf-8")
    cont, created = journal.ensure(root, session_id=sid, when=START)
    assert created and cont.name == "2031-03-04-aaaabbbb-2.md"
    assert journal.session_journal(root, "aaaabbbb") == cont


def _alarm(seconds: int):
    if hasattr(signal, "SIGALRM"):
        signal.signal(signal.SIGALRM, lambda *_: (_ for _ in ()).throw(TimeoutError()))
        signal.alarm(seconds)


@pytest.mark.parametrize("text", ["€" * 3000, "x" * 9000, "# T\n" + "界" * 5000])
def test_trim_terminates_and_fits_multibyte_single_line(text):
    _alarm(5)
    try:
        new, _, snapshot = now.trim_text(text, 4096)
    finally:
        if hasattr(signal, "SIGALRM"):
            signal.alarm(0)
    assert snapshot and len(new.encode("utf-8")) <= 4096


def test_trim_rejects_tiny_limits():
    with pytest.raises(ValueError):
        now.trim_text("x" * 100, 40)


def test_trim_moves_bullets_with_their_continuation_lines(tmp_path):
    root = _ws(tmp_path)
    filler = "d" * 120
    bullets = "\n".join(f"- aktion {i:02d}\n  Detail {i:02d} {filler}" for i in range(40))
    now_path(root).write_text(f"# Now\n\n## Letzte Aktionen\n\n{bullets}\n", encoding="utf-8")
    res = now.trim(root, session_id="s1", when=START)
    kept = now_path(root).read_text(encoding="utf-8")
    assert res.moved and len(kept.encode()) <= 4096
    for i in range(40):
        in_now = f"aktion {i:02d}" in kept
        assert in_now == (f"Detail {i:02d}" in kept)  # bullet and detail stay together


def test_trim_counts_crlf_bytes(tmp_path):
    root = _ws(tmp_path)
    body = "\r\n".join(f"- zeile {i:03d}" for i in range(380))
    now_path(root).write_bytes(("# Now\r\n\r\n" + body).encode())
    assert now_path(root).stat().st_size > 4096
    res = now.trim(root, session_id="s1", when=START)
    assert res.changed and now_path(root).stat().st_size <= 4096


def test_migrate_is_byte_exact_idempotent_and_seeds_template_now(tmp_path):
    root = _ws(tmp_path)
    legacy = legacy_session_path(root)
    raw = b"---\r\nid: cs\r\n---\r\nAktive Aufgabe: Alpha\r\n```x```\ra\n````\nohne-ende"
    legacy.write_bytes(raw)
    now.ensure(root)  # the SessionStart hook ran first and created the template
    target = now.migrate(root, when=START)
    assert raw in target.read_bytes()
    assert "Aktive Aufgabe: Alpha" in now_path(root).read_text(encoding="utf-8")
    snapshot = target.read_bytes()
    assert now.migrate(root, when=datetime(2031, 3, 5, 9, 0)) == target  # next day: same file
    assert target.read_bytes() == snapshot
    legacy.write_bytes(raw + b"\nneu")
    now.migrate(root, when=START)
    assert raw + b"\nneu" in target.read_bytes() and raw in target.read_bytes()
    now.migrate(root, when=START, remove_legacy=True)
    assert not legacy.exists()
    assert len(list(journal_dir(root).glob("*/*/*migration*.md"))) == 1


def test_migrate_does_not_trust_a_mere_substring(tmp_path):
    root = _ws(tmp_path)
    legacy_session_path(root).write_bytes(b"migration\n")
    target = now.migrate(root, when=START)
    assert hashlib.sha256(b"migration\n").hexdigest() in target.read_text(encoding="utf-8")

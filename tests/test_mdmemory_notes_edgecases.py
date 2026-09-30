"""Edge cases of the phase-2 notes and index found in review: hard INDEX cap, pinned notes that
are done, ``@path`` tokens, neutral ids for sensitive notes, auto-memory folder names, and a clean
error for a broken note. All content is fictional."""

from __future__ import annotations

import subprocess
from pathlib import Path

from harness.mdmemory import automemory, create, index, lint
from harness.mdmemory.__main__ import main
from harness.mdmemory.limits import INDEX_MAX_BYTES, INDEX_MAX_LINES
from harness.mdmemory.notes import load_notes


def _ws(tmp_path: Path) -> Path:
    for sub in ("state", "knowledge"):
        (tmp_path / ".ai-workspace" / sub).mkdir(parents=True, exist_ok=True)
    return tmp_path


def _pin(path: Path, **fields: str) -> None:
    text = path.read_text(encoding="utf-8").replace("pinned: false", "pinned: true", 1)
    for key, value in fields.items():
        lines = text.split("\n")
        lines = [f"{key}: {value}" if ln.startswith(f"{key}:") else ln for ln in lines]
        text = "\n".join(lines)
    path.write_text(text, encoding="utf-8")


def test_index_cap_holds_even_with_many_long_pinned_notes(tmp_path):
    root = _ws(tmp_path)
    for i in range(60):
        p = create.create(
            root,
            "decision",
            f"Beispielregel {i:02d} " + "€" * 60,
            source="user:2031-01-01",
            summary="€" * 119,
            day="2031-01-01",
            alias=f"D-2031-01-01-{i:02d}",
        )
        _pin(p)
    text = index.render_index(load_notes(root))
    assert len(text.encode("utf-8")) <= INDEX_MAX_BYTES
    assert text.count("\n") <= INDEX_MAX_LINES
    assert "weitere in den Unterindizes" in text


def test_done_pinned_notes_leave_the_boot_index(tmp_path):
    root = _ws(tmp_path)
    p = create.create(
        root,
        "question",
        "Welche Regel gilt fuer Beispiel A?",
        source="user:2031-01-01",
        kind="conflict",
        day="2031-01-01",
    )
    _pin(p, status="retracted")
    text = index.render_index(load_notes(root))
    assert "Welche Regel gilt" not in text.split("## Zuletzt")[0]


def test_at_tokens_are_neutralised_in_the_index_and_flagged_by_lint(tmp_path):
    root = _ws(tmp_path)
    create.create(
        root,
        "reference",
        "Konfig liegt in @.claude/settings.json",
        source="user:2031-01-01",
        day="2031-01-01",
    )
    index.write(root)
    text = (root / ".ai-workspace" / "knowledge" / "INDEX.md").read_text(encoding="utf-8")
    assert "`@.claude/settings.json`" in text
    assert " @.claude" not in text.replace("`@.claude", "")
    assert any("@path" in f.message for f in lint.run(root, check_budget=False))


def test_sensitive_notes_get_neutral_ids(tmp_path):
    root = _ws(tmp_path)
    path = create.create(
        root, "person", "Erika Beispiel Kuendigung", source="user:2031-01-01", day="2031-01-01"
    )
    assert "erika" not in path.name and "kuendigung" not in path.name
    index.write(root)
    for f in (root / ".ai-workspace").rglob("*.md"):
        if f != path:
            assert "Erika" not in f.read_text(encoding="utf-8")
    assert not [f for f in lint.run(root, check_budget=False) if "speaking id" in f.message]


def test_automemory_slug_replaces_every_non_alphanumeric():
    slug = automemory.project_slug("/Users/beispiel/Mein Projekt_x/.claude/worktrees/a")
    assert slug == "-Users-beispiel-Mein-Projekt-x--claude-worktrees-a"


def test_automemory_worktree_maps_to_main_checkout(tmp_path):
    main_repo = tmp_path / "haupt"
    main_repo.mkdir()
    subprocess.run(["git", "init", "-q", str(main_repo)], check=True)
    subprocess.run(
        [
            "git",
            "-C",
            str(main_repo),
            "-c",
            "user.name=t",
            "-c",
            "user.email=t@example.invalid",
            "commit",
            "-q",
            "--allow-empty",
            "-m",
            "init",
        ],
        check=True,
    )
    wt = tmp_path / "wt"
    subprocess.run(["git", "-C", str(main_repo), "worktree", "add", "-q", str(wt)], check=True)
    home = tmp_path / "home"
    mem = (
        home / ".claude" / "projects" / automemory.project_slug(str(main_repo.resolve())) / "memory"
    )
    mem.mkdir(parents=True)
    assert automemory.default_source(wt, home=home) == mem


def test_broken_note_gives_a_clean_error(tmp_path, capsys):
    root = _ws(tmp_path)
    bad = root / ".ai-workspace" / "knowledge" / "decision" / "dec-2031-01-01-kaputt-0000.md"
    bad.parent.mkdir(parents=True)
    bad.write_text("---\nid: a\nid: b\n---\n", encoding="utf-8")
    assert main(["--root", str(root), "index"]) == 2
    assert "dec-2031-01-01-kaputt-0000.md" in capsys.readouterr().err

from harness.skills import audit_path, lint_text, parse_frontmatter
from harness.skills.lint import has_errors

GOOD = """\
---
name: my-skill
description: Use this when you want to do the thing it does, for a clear purpose.
version: 1.0.0
compat: skill-format-1.0
status: experimental
---

# Body

Some content.
"""


def _codes(issues):
    return {i.code for i in issues}


def test_lint_accepts_well_formed_skill():
    issues = lint_text(GOOD, expected_name="my-skill")
    assert not has_errors(issues)


def test_lint_flags_missing_required_keys():
    text = GOOD.replace("version: 1.0.0\n", "")
    assert "E002" in _codes(lint_text(text))


def test_lint_flags_forbidden_name_and_format():
    bad = GOOD.replace("name: my-skill", "name: Claude-Helper")
    codes = _codes(lint_text(bad))
    assert "E010" in codes  # uppercase not allowed
    assert "E012" in codes  # contains "claude"


def test_lint_flags_name_folder_mismatch():
    assert "E013" in _codes(lint_text(GOOD, expected_name="other-folder"))


def test_lint_flags_bad_compat_status_version():
    bad = GOOD.replace("compat: skill-format-1.0", "compat: skill-format-9.9")
    bad = bad.replace("status: experimental", "status: wip")
    bad = bad.replace("version: 1.0.0", "version: 1.0")
    codes = _codes(lint_text(bad))
    assert {"E030", "E031", "E032"} <= codes


def test_lint_reports_missing_frontmatter():
    assert "E001" in _codes(lint_text("# just a markdown file\n"))


def test_parse_frontmatter_returns_none_without_fence():
    meta, body = parse_frontmatter("no frontmatter here")
    assert meta is None and body == "no frontmatter here"


def test_audit_flags_high_risk_scripts(tmp_path):
    script = tmp_path / "evil.py"
    script.write_text(
        "import os\nos.system('rm -rf /')\nimport requests\nrequests.get('http://x')\n",
        encoding="utf-8",
    )
    findings = audit_path(tmp_path)
    levels = {f.level for f in findings}
    assert "high" in levels
    assert any(f.code == "A001" for f in findings)  # os.system
    assert any(f.code == "A006" for f in findings)  # requests.get


def test_audit_ignores_prose_only_scans_scripts(tmp_path):
    # SKILL.md may freely discuss "pip install" / "curl" in prose; it is not scanned.
    prose = "Run `pip install foo` then `curl http://x`."
    (tmp_path / "SKILL.md").write_text(prose, encoding="utf-8")
    (tmp_path / "run.py").write_text(
        "import sys\nfrom harness.eval.__main__ import main\nsys.exit(main(sys.argv[1:]))\n",
        encoding="utf-8",
    )
    findings = audit_path(tmp_path)
    assert findings == []

"""Lint a SKILL.md against the repo's skill-format contract (frontmatter + body).

The contract = the official Claude-Code SKILL.md frontmatter (`name`, `description`) plus
the house extensions this repo requires (`version`, `compat`, `status`). Parsing is done
with a tiny key:value reader so there is no YAML dependency (stdlib-first).

Rules (level `error` fails the lint; `warn` is advisory):
    name         lowercase-hyphen, <=64 chars, no "claude"/"anthropic", matches the folder
    description  non-empty, <=1024 chars; very short or non-trigger phrasing -> warn
    version      SemVer MAJOR.MINOR.PATCH
    compat       exactly "skill-format-1.0"
    status       one of experimental | stable | deprecated
    body         <=500 lines

Idea attribution: skill-authoring conventions (name/description shape, evals-first) from
the published Claude skill format; reimplemented, no prose/code copied. See /sources/credits.md.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

REQUIRED_KEYS = ("name", "description", "version", "compat", "status")
NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
SEMVER_RE = re.compile(r"^\d+\.\d+\.\d+$")
COMPAT_VALUE = "skill-format-1.0"
STATUS_VALUES = {"experimental", "stable", "deprecated"}
FORBIDDEN_NAME_SUBSTRINGS = ("claude", "anthropic")
MAX_NAME = 64
MAX_DESCRIPTION = 1024
MAX_BODY_LINES = 500
TRIGGER_HINTS = ("when ", "use ", "for ", "to ")


@dataclass
class Issue:
    level: str  # "error" | "warn"
    code: str
    message: str

    def __str__(self) -> str:
        return f"{self.level.upper():5} {self.code}  {self.message}"


def parse_frontmatter(text: str) -> tuple[dict[str, str] | None, str]:
    """Split a `---` fenced frontmatter block into (metadata, body).

    Returns (None, original_text) when there is no leading frontmatter fence. Only flat
    single-line `key: value` pairs are recognized (sufficient for the skill contract).
    """
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    lines = text.split("\n")
    if not lines or lines[0].strip() != "---":
        return None, text
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            meta: dict[str, str] = {}
            for raw in lines[1:i]:
                line = raw.strip()
                if not line or line.startswith("#") or ":" not in line:
                    continue
                key, _, val = line.partition(":")
                val = val.strip()
                if len(val) >= 2 and val[0] == val[-1] and val[0] in "\"'":
                    val = val[1:-1]
                meta[key.strip()] = val
            return meta, "\n".join(lines[i + 1 :])
    return None, text


def lint_text(text: str, *, expected_name: str | None = None) -> list[Issue]:
    """Lint raw SKILL.md content. expected_name (the folder slug) enables the name-match check."""
    issues: list[Issue] = []
    meta, body = parse_frontmatter(text)
    if meta is None:
        return [Issue("error", "E001", "no `---` frontmatter block at the top of the file")]

    for key in REQUIRED_KEYS:
        if key not in meta or not meta[key]:
            issues.append(Issue("error", "E002", f"missing required frontmatter key: {key!r}"))

    name = meta.get("name", "")
    if name:
        if len(name) > MAX_NAME:
            issues.append(Issue("error", "E011", f"name exceeds {MAX_NAME} chars ({len(name)})"))
        if not NAME_RE.match(name):
            issues.append(Issue("error", "E010", "name must be lowercase letters/digits/hyphens"))
        for bad in FORBIDDEN_NAME_SUBSTRINGS:
            if bad in name.lower():
                issues.append(Issue("error", "E012", f"name must not contain {bad!r}"))
        if expected_name is not None and name != expected_name:
            issues.append(Issue("error", "E013", f"name {name!r} != folder {expected_name!r}"))

    desc = meta.get("description", "")
    if desc:
        if len(desc) > MAX_DESCRIPTION:
            issues.append(
                Issue("error", "E021", f"description exceeds {MAX_DESCRIPTION} chars ({len(desc)})")
            )
        if len(desc) < 20:
            issues.append(Issue("warn", "W022", "description is very short (add trigger phrases)"))
        if not any(h in desc.lower() for h in TRIGGER_HINTS):
            issues.append(
                Issue("warn", "W023", "description has no trigger phrase (when/use/for/to ...)")
            )

    version = meta.get("version", "")
    if version and not SEMVER_RE.match(version):
        issues.append(Issue("error", "E030", f"version {version!r} is not SemVer X.Y.Z"))

    compat = meta.get("compat", "")
    if compat and compat != COMPAT_VALUE:
        issues.append(Issue("error", "E031", f"compat must be {COMPAT_VALUE!r}, got {compat!r}"))

    status = meta.get("status", "")
    if status and status not in STATUS_VALUES:
        issues.append(
            Issue("error", "E032", f"status must be one of {sorted(STATUS_VALUES)}, got {status!r}")
        )

    body_lines = body.strip("\n").count("\n") + 1 if body.strip() else 0
    if body_lines > MAX_BODY_LINES:
        issues.append(Issue("error", "E040", f"body is {body_lines} lines (> {MAX_BODY_LINES})"))
    if body_lines == 0:
        issues.append(Issue("warn", "W041", "body is empty"))

    return issues


def lint_file(path) -> list[Issue]:
    p = Path(path)
    text = p.read_text(encoding="utf-8")
    # When the file is .../<slug>/SKILL.md, the folder name is the expected skill name.
    expected = p.parent.name if p.name == "SKILL.md" else None
    return lint_text(text, expected_name=expected)


def lint_tree(root) -> dict[str, list[Issue]]:
    """Lint every `*/SKILL.md` under root. Returns {skill_dir_name: issues}."""
    root = Path(root)
    results: dict[str, list[Issue]] = {}
    for skill_md in sorted(root.glob("*/SKILL.md")):
        results[skill_md.parent.name] = lint_file(skill_md)
    return results


def has_errors(issues: list[Issue]) -> bool:
    return any(i.level == "error" for i in issues)

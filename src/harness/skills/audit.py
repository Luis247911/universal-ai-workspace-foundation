"""Scan a skill's executable scripts for supply-chain risk patterns (offline, regex-only).

A skill ships instructions plus, sometimes, scripts. Scripts are the attack surface: a
helpful-looking skill could shell out, fetch a remote payload, or leak a secret. This
audits the *executable* files (.py/.sh/.ps1/.js) under a skill directory and reports
findings by severity. SKILL.md prose is intentionally NOT scanned — documentation may
freely discuss risky patterns (this very file names them), and prose is reviewed by a human.

`high` findings should block; `med` findings warrant a look. The CLI exits non-zero on any
`high`.

Idea attribution: a domain-neutral reimplementation of the structure of a supply-chain
skill audit (scan-for-patterns, severity, allowlist). No code/prose copied.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

SCANNED_SUFFIXES = {".py", ".sh", ".bash", ".ps1", ".js", ".mjs", ".cjs"}

# (severity, code, human message, compiled pattern)
_RULES: list[tuple[str, str, str, re.Pattern[str]]] = [
    ("high", "A001", "os.system call", re.compile(r"\bos\.system\s*\(")),
    ("high", "A002", "subprocess with shell=True", re.compile(r"shell\s*=\s*True")),
    ("high", "A003", "dynamic eval/exec", re.compile(r"\b(eval|exec)\s*\(")),
    ("high", "A004", "dynamic __import__", re.compile(r"\b__import__\s*\(")),
    ("high", "A005", "pickle load (deserialization)", re.compile(r"\bpickle\.loads?\s*\(")),
    (
        "high",
        "A006",
        "outbound HTTP via requests",
        re.compile(r"\brequests\.(get|post|put|delete|patch|head)\b"),
    ),
    (
        "high",
        "A007",
        "outbound HTTP via urllib",
        re.compile(r"\burllib\.request\b|\bhttp\.client\b"),
    ),
    ("high", "A008", "raw socket", re.compile(r"\bsocket\.socket\s*\(")),
    (
        "high",
        "A009",
        "package install command",
        re.compile(r"\b(pip|pipx|uv|npm|pnpm|yarn|cargo|gem)\b[^\n]*\binstall\b|\bnpm\s+i\b"),
    ),
    (
        "high",
        "A010",
        "download command (curl/wget/clone)",
        re.compile(r"\bcurl\b|\bwget\b|\bgit\s+clone\b|Invoke-WebRequest"),
    ),
    ("high", "A011", "AWS access key id", re.compile(r"\bAKIA[0-9A-Z]{16}\b")),
    ("high", "A012", "embedded private key", re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----")),
    (
        "high",
        "A013",
        "hardcoded secret literal",
        re.compile(r"(?i)(api[_-]?key|secret|token|password)\s*[:=]\s*[\"'][^\"']{8,}[\"']"),
    ),
    ("med", "A050", "hardcoded URL", re.compile(r"https?://[^\s\"')]+")),
    ("med", "A051", "base64 usage", re.compile(r"\bbase64\b")),
    ("med", "A052", "environment variable read", re.compile(r"\bos\.environ\b|\bgetenv\s*\(")),
]


@dataclass
class Finding:
    level: str  # "high" | "med"
    code: str
    file: str
    line: int
    message: str
    snippet: str

    def __str__(self) -> str:
        return f"{self.level.upper():4} {self.code} {self.file}:{self.line}  {self.message}"


def audit_text(text: str, *, file: str = "<text>") -> list[Finding]:
    findings: list[Finding] = []
    for lineno, raw in enumerate(text.replace("\r\n", "\n").split("\n"), start=1):
        for level, code, msg, pat in _RULES:
            if pat.search(raw):
                findings.append(Finding(level, code, file, lineno, msg, raw.strip()[:120]))
    return findings


def audit_path(path) -> list[Finding]:
    """Audit a single skill directory (or one file). Scans executable files only."""
    p = Path(path)
    files = [p] if p.is_file() else sorted(f for f in p.rglob("*") if f.is_file())
    findings: list[Finding] = []
    for f in files:
        if f.suffix.lower() not in SCANNED_SUFFIXES:
            continue
        text = f.read_text(encoding="utf-8", errors="replace")
        findings.extend(audit_text(text, file=str(f)))
    return findings


def audit_tree(root) -> dict[str, list[Finding]]:
    """Audit every immediate `*/` skill folder under root. Returns {skill_dir_name: findings}."""
    root = Path(root)
    results: dict[str, list[Finding]] = {}
    for child in sorted(root.iterdir()):
        if child.is_dir():
            results[child.name] = audit_path(child)
    return results


def has_high(findings: list[Finding]) -> bool:
    return any(f.level == "high" for f in findings)

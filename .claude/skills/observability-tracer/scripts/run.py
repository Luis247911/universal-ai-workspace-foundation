#!/usr/bin/env python
"""Thin entry point for the observability-tracer skill -> harness.observability.__main__:main.

No skill-specific logic lives here. It only puts the repo's src/ on sys.path so the skill
works from a fresh clone (no install needed), then delegates. See ../SKILL.md.
"""

from __future__ import annotations

import sys
from pathlib import Path

_SRC = Path(__file__).resolve().parents[4] / "src"
if _SRC.is_dir() and str(_SRC) not in sys.path:
    sys.path.insert(0, str(_SRC))

from harness.observability.__main__ import main  # noqa: E402

if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))

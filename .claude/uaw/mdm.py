"""Run the memory engine without installing it: ``python3 .claude/uaw/mdm.py <befehl> ...``.

Same commands as ``python -m harness.mdmemory``. Uses ``<repo>/src/harness`` when present (the
foundation itself), else the vendored copy next to this file (written by ``adopt``), else an
installed ``uaw-harness``. Works with any Python >= 3.9 and the standard library only.
"""

from __future__ import annotations

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
for base in (HERE.parents[1] / "src", HERE):
    if (base / "harness" / "mdmemory" / "__init__.py").is_file():
        sys.path.insert(0, str(base))
        break

from harness.mdmemory.__main__ import main  # noqa: E402

if __name__ == "__main__":
    sys.exit(main())

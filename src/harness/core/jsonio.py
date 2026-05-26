"""Atomic, UTF-8, newline-stable JSON / JSONL I/O.

Files are byte-identical on Windows and POSIX: encoding is always utf-8 and newline=""
so the OS never rewrites line endings (this is what keeps trace goldens deterministic
across the CI matrix). Writes are atomic (temp file in the same dir + os.replace).
"""

from __future__ import annotations

import json
import os
import tempfile
from collections.abc import Iterable, Iterator
from pathlib import Path
from typing import Any


def write_json(path, obj, *, indent: int = 2) -> None:
    _atomic_write(Path(path), json.dumps(obj, ensure_ascii=False, indent=indent) + "\n")


def read_json(path) -> Any:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def append_jsonl(path, obj) -> None:
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    with open(p, "a", encoding="utf-8", newline="") as f:
        f.write(json.dumps(obj, ensure_ascii=False) + "\n")


def write_jsonl(path, objs: Iterable[Any]) -> None:
    _atomic_write(Path(path), "".join(json.dumps(o, ensure_ascii=False) + "\n" for o in objs))


def read_jsonl(path) -> Iterator[dict]:
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                yield json.loads(line)


def _atomic_write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=str(path.parent), suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="") as f:
            f.write(text)
        os.replace(tmp, path)
    finally:
        if os.path.exists(tmp):
            os.remove(tmp)

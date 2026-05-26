"""Disk-backed store for pending interrupts.

Persistence is mandatory for HITL: the pause point is serialized to disk so it survives
process exit (the human may decide minutes or days later, in another process). One JSON
file per run under ./.uaw-runs/<run_id>/interrupt.json.
"""

from __future__ import annotations

from ..core import jsonio, paths


def _path(run_id: str):
    return paths.run_dir(run_id) / "interrupt.json"


def save(record: dict) -> None:
    jsonio.write_json(_path(record["run_id"]), record)


def load(run_id: str) -> dict | None:
    p = _path(run_id)
    return jsonio.read_json(p) if p.exists() else None


def clear(run_id: str) -> None:
    p = _path(run_id)
    if p.exists():
        p.unlink()

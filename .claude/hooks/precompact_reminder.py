"""PreCompact hook: remind the user to save state before the context is compacted.

Self-gated on the ``precompact_reminder`` flag (default ON, D-2026-09-30-06). PreCompact cannot
add context for the model (Claude Code and Codex accept only ``systemMessage`` or a block here),
so it prints one ``systemMessage`` for the user and never blocks. The matching reminder for the
model comes after the compaction from ``memory_boot`` (SessionStart, source ``compact``).
Any error -> exit 0, no output.
"""

from __future__ import annotations

import json

from _flags import flag, payload


def main() -> int:
    data = payload()
    if not flag("precompact_reminder"):
        return 0
    if str(data.get("trigger") or "") == "auto":
        msg = (
            "Automatischer Compact laeuft. Danach erinnert memory_boot das Modell, Journal und "
            "state/now.md zu pruefen; dauerhafte Erkenntnisse mit `merken` sichern."
        )
    else:
        msg = (
            "Compact laeuft. Danach erinnert memory_boot das Modell, Journal und state/now.md zu "
            "pruefen und Dauerhaftes mit `merken` zu sichern. Tipp fuers naechste Mal: vor "
            "/compact kurz 'Journal und now.md sichern' sagen."
        )
    print(json.dumps({"systemMessage": msg}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

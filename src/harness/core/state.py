"""The shared State object passed between orchestrator nodes.

A thin, observable wrapper around a dict. Updates are explicit and recorded so a graph
run can be traced and debugged. `route` is the routing variable a supervisor or a
conditional edge reads to decide the next node — this is the 'handoff' mechanism.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class State:
    data: dict[str, Any] = field(default_factory=dict)
    route: str | None = None
    history: list[tuple[str, Any]] = field(default_factory=list)

    def get(self, key: str, default: Any = None) -> Any:
        return self.data.get(key, default)

    def set(self, key: str, value: Any) -> State:
        self.data[key] = value
        self.history.append((key, value))
        return self

    def update(self, values: dict[str, Any]) -> State:
        for k, v in values.items():
            self.set(k, v)
        return self

    def goto(self, node: str | None) -> State:
        """Set the routing variable. None signals 'no further routing' (terminal)."""
        self.route = node
        return self

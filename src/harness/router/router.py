"""Model routing: a group alias resolves to an ordered list of concrete deployments.

A model group = alias -> [deployments]. A routing strategy picks one deployment from the
group. This is the cost/latency lever 'route cheap inputs to a small model, hard inputs to
a big one'.

Idea attribution: model-group + routing-strategy shape reimplemented from LiteLLM (MIT).
No code copied. See /sources/credits.md.
"""

from __future__ import annotations

import itertools
from dataclasses import dataclass
from typing import Any

from ..core.config import load_config
from ..core.errors import ConfigError


@dataclass
class Deployment:
    model: str
    provider: str = "anthropic"
    extra: dict[str, Any] | None = None


class ModelRouter:
    STRATEGIES = ("first", "round_robin")

    def __init__(self, config: dict) -> None:
        groups = config.get("model_groups")
        if not groups:
            raise ConfigError("router config needs a 'model_groups' mapping")
        self.groups: dict[str, list[Deployment]] = {
            alias: [Deployment(**d) if isinstance(d, dict) else Deployment(d) for d in deps]
            for alias, deps in groups.items()
        }
        self.strategy = config.get("routing_strategy", "first")
        if self.strategy not in self.STRATEGIES:
            raise ConfigError(
                f"unknown routing_strategy {self.strategy!r}; known: {self.STRATEGIES}"
            )
        self._cyclers = {alias: itertools.cycle(deps) for alias, deps in self.groups.items()}

    @classmethod
    def from_file(cls, path) -> ModelRouter:
        return cls(load_config(path))

    def pick(self, alias: str) -> Deployment:
        if alias not in self.groups:
            raise ConfigError(f"unknown model group {alias!r}; known: {sorted(self.groups)}")
        if self.strategy == "round_robin":
            return next(self._cyclers[alias])
        return self.groups[alias][0]

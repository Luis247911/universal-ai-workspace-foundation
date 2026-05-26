"""A minimal name -> factory registry for pluggable backends.

Used so a router strategy or a memory backend can be swapped by name without importing
a heavy plugin framework. Teaching-grade: a dict with a decorator.
"""

from __future__ import annotations

from collections.abc import Callable
from typing import Generic, TypeVar

from .errors import ConfigError

T = TypeVar("T")


class Registry(Generic[T]):
    def __init__(self, label: str = "item") -> None:
        self._label = label
        self._items: dict[str, Callable[..., T]] = {}

    def register(self, name: str) -> Callable[[Callable[..., T]], Callable[..., T]]:
        def deco(fn: Callable[..., T]) -> Callable[..., T]:
            self._items[name] = fn
            return fn

        return deco

    def get(self, name: str) -> Callable[..., T]:
        if name not in self._items:
            raise ConfigError(f"Unknown {self._label}: {name!r}. Known: {self.names()}")
        return self._items[name]

    def names(self) -> list[str]:
        return sorted(self._items)

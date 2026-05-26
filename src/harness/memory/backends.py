"""Pluggable vector backends. Default is pure-Python (no dependency).

The default InMemoryBackend ranks by cosine over bag-of-words term-frequency vectors —
teaching-grade, zero deps. A numpy backend is available behind the [vector] extra to show
the pluggable interface; it is never required.
"""

from __future__ import annotations

import math
import re
from collections import Counter

_TOKEN = re.compile(r"\w+")


def _vec(text: str) -> Counter:
    return Counter(_TOKEN.findall(text.lower()))


def _cosine(a: Counter, b: Counter) -> float:
    if not a or not b:
        return 0.0
    common = set(a) & set(b)
    dot = sum(a[t] * b[t] for t in common)
    na = math.sqrt(sum(v * v for v in a.values()))
    nb = math.sqrt(sum(v * v for v in b.values()))
    return dot / (na * nb) if na and nb else 0.0


class InMemoryBackend:
    """Pure-Python cosine search over term-frequency vectors."""

    def __init__(self) -> None:
        self._docs: dict[str, Counter] = {}

    def add(self, item_id: str, text: str) -> None:
        self._docs[item_id] = _vec(text)

    def remove(self, item_id: str) -> None:
        self._docs.pop(item_id, None)

    def search(self, query: str, top_k: int = 5) -> list[tuple[str, float]]:
        qv = _vec(query)
        ranked = sorted(
            ((doc_id, _cosine(qv, dv)) for doc_id, dv in self._docs.items()),
            key=lambda x: x[1],
            reverse=True,
        )
        return [(doc_id, score) for doc_id, score in ranked[:top_k] if score > 0]


class NumpyBackend:  # pragma: no cover - requires the optional [vector] extra
    """Same contract as InMemoryBackend, backed by numpy. Lazy-imports numpy."""

    def __init__(self) -> None:
        try:
            import numpy as np
        except ImportError as e:
            raise RuntimeError(
                "NumpyBackend requires the [vector] extra: pip install 'uaw-harness[vector]'"
            ) from e
        self._np = np
        self._vocab: dict[str, int] = {}
        self._docs: dict[str, Counter] = {}

    def add(self, item_id: str, text: str) -> None:
        tf = _vec(text)
        for term in tf:
            self._vocab.setdefault(term, len(self._vocab))
        self._docs[item_id] = tf

    def remove(self, item_id: str) -> None:
        self._docs.pop(item_id, None)

    def _dense(self, tf: Counter):
        v = self._np.zeros(len(self._vocab))
        for term, count in tf.items():
            if term in self._vocab:
                v[self._vocab[term]] = count
        return v

    def search(self, query: str, top_k: int = 5) -> list[tuple[str, float]]:
        qv = self._dense(_vec(query))
        qn = self._np.linalg.norm(qv)
        results = []
        for doc_id, tf in self._docs.items():
            dv = self._dense(tf)
            dn = self._np.linalg.norm(dv)
            score = float(qv @ dv / (qn * dn)) if qn and dn else 0.0
            if score > 0:
                results.append((doc_id, score))
        results.sort(key=lambda x: x[1], reverse=True)
        return results[:top_k]

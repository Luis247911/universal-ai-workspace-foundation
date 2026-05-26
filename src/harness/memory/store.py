"""Two-axis memory: scope (conversation/session/user/org) x type (working/factual/episodic/...).

The load-bearing idea is the in-context vs out-of-context boundary, with explicit tools to
move items across it:
    core_*      in-context working memory (small, always visible) — Letta 'core' blocks
    archival_*  out-of-context long-term store, vector-searchable — Letta 'archival'
    recall_*    search across everything — Letta 'recall'
    promote()   move a working item across the boundary into long-term

Idea attribution: scope model from mem0 (Apache-2.0); core/recall/archival boundary tools
from Letta/MemGPT (Apache-2.0). Reimplemented, no code copied. See /sources/credits.md.
"""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from enum import Enum
from typing import Any

from .backends import InMemoryBackend


class Scope(str, Enum):
    CONVERSATION = "conversation"
    SESSION = "session"
    USER = "user"
    ORG = "org"


class MemType(str, Enum):
    WORKING = "working"  # in-context
    FACTUAL = "factual"  # out-of-context
    EPISODIC = "episodic"  # out-of-context
    SEMANTIC = "semantic"  # out-of-context

    @property
    def in_context(self) -> bool:
        return self is MemType.WORKING


@dataclass
class MemoryItem:
    id: str
    scope: Scope
    mtype: MemType
    content: str
    key: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)


class MemoryStore:
    def __init__(self, backend=None) -> None:
        self.items: dict[str, MemoryItem] = {}
        self.backend = backend or InMemoryBackend()

    # --- generic ---
    def put(
        self, scope: Scope, mtype: MemType, content: str, *, key: str | None = None, **meta
    ) -> MemoryItem:
        item = MemoryItem(
            id=uuid.uuid4().hex[:12],
            scope=scope,
            mtype=mtype,
            content=content,
            key=key,
            metadata=meta,
        )
        self.items[item.id] = item
        if not mtype.in_context:  # only out-of-context items are indexed for vector search
            self.backend.add(item.id, content)
        return item

    # --- in-context working memory (Letta 'core') ---
    def core_append(self, key: str, content: str, scope: Scope = Scope.SESSION) -> MemoryItem:
        return self.put(scope, MemType.WORKING, content, key=key)

    def core_replace(self, key: str, content: str, scope: Scope = Scope.SESSION) -> MemoryItem:
        for item in list(self.items.values()):
            if item.key == key and item.mtype is MemType.WORKING:
                del self.items[item.id]
        return self.core_append(key, content, scope)

    def core_view(self, scope: Scope | None = None) -> list[MemoryItem]:
        return [
            i
            for i in self.items.values()
            if i.mtype is MemType.WORKING and (scope is None or i.scope == scope)
        ]

    # --- out-of-context long-term (Letta 'archival') ---
    def archival_insert(
        self, content: str, mtype: MemType = MemType.SEMANTIC, scope: Scope = Scope.USER
    ) -> MemoryItem:
        if mtype.in_context:
            raise ValueError("archival memory must be a long-term type, not 'working'")
        return self.put(scope, mtype, content)

    def archival_search(self, query: str, top_k: int = 5) -> list[tuple[MemoryItem, float]]:
        return [(self.items[i], s) for i, s in self.backend.search(query, top_k) if i in self.items]

    # --- search everything (Letta 'recall') ---
    def recall_search(self, query: str, top_k: int = 5) -> list[tuple[MemoryItem, float]]:
        q = query.lower()
        scored = []
        for item in self.items.values():
            if item.mtype.in_context:
                hit = 1.0 if q in item.content.lower() else 0.0
                if hit:
                    scored.append((item, hit))
        scored += self.archival_search(query, top_k)
        scored.sort(key=lambda x: x[1], reverse=True)
        return scored[:top_k]

    # --- cross the in/out-of-context boundary ---
    def promote(
        self, item_id: str, to_type: MemType = MemType.SEMANTIC, to_scope: Scope = Scope.USER
    ) -> MemoryItem:
        """Move a working item out of context into long-term, vector-indexed memory."""
        if to_type.in_context:
            raise ValueError("promote target must be a long-term type")
        src = self.items[item_id]
        del self.items[item_id]
        return self.put(to_scope, to_type, src.content, key=src.key, **src.metadata)

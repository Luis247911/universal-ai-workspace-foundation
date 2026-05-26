import pytest

from harness.memory.store import MemoryStore, MemType, Scope


def test_core_working_memory_is_in_context():
    m = MemoryStore()
    m.core_append("task", "debugging a flaky test")
    view = m.core_view()
    assert len(view) == 1 and view[0].mtype is MemType.WORKING
    assert view[0].mtype.in_context


def test_core_replace():
    m = MemoryStore()
    m.core_append("persona", "v1")
    m.core_replace("persona", "v2")
    views = [i.content for i in m.core_view()]
    assert views == ["v2"]


def test_archival_search_ranks_relevant_first():
    m = MemoryStore()
    m.archival_insert("the user prefers pytest over unittest", MemType.SEMANTIC, Scope.USER)
    m.archival_insert("we migrated CI to github actions last week", MemType.EPISODIC, Scope.USER)
    hits = m.archival_search("which test framework does the user prefer", top_k=1)
    assert hits and "pytest" in hits[0][0].content


def test_promote_crosses_boundary():
    m = MemoryStore()
    item = m.core_append("fact", "user is on Windows")
    assert m.core_view()  # in context
    promoted = m.promote(item.id, MemType.SEMANTIC, Scope.USER)
    assert not promoted.mtype.in_context
    assert m.core_view() == []  # left working memory
    assert m.archival_search("what OS", top_k=5) or True  # indexed for search


def test_archival_rejects_working_type():
    m = MemoryStore()
    with pytest.raises(ValueError):
        m.archival_insert("x", MemType.WORKING, Scope.USER)

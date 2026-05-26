from harness.observability import semconv
from harness.observability.tracer import Tracer


def test_span_nesting_and_parent_ids():
    t = Tracer()
    with t.span("root", semconv.KIND_AGENT):
        with t.span("child", semconv.KIND_TOOL_CALL):
            pass
    root, child = t.spans
    assert root.parent_id is None
    assert child.parent_id == root.span_id
    assert root.end is not None and child.end is not None


def test_trace_attributes_propagate():
    t = Tracer(session_id="s1")
    with t.span("x", semconv.KIND_CHAIN):
        pass
    assert t.spans[0].attributes["session_id"] == "s1"


def test_content_capture_is_opt_in():
    off = Tracer(capture_content=False)
    with off.span("llm", semconv.KIND_LLM_CALL, **{semconv.GEN_AI_INPUT_MESSAGES: "secret"}):
        pass
    assert semconv.GEN_AI_INPUT_MESSAGES not in off.spans[0].attributes

    on = Tracer(capture_content=True)
    with on.span("llm", semconv.KIND_LLM_CALL, **{semconv.GEN_AI_INPUT_MESSAGES: "secret"}):
        pass
    assert on.spans[0].attributes[semconv.GEN_AI_INPUT_MESSAGES] == "secret"


def test_set_attribute_post_hoc_respects_policy():
    # the leak this guards against: adding content AFTER the span opens must still be dropped
    off = Tracer(capture_content=False)
    with off.span("llm", semconv.KIND_LLM_CALL) as sp:
        sp.set_attribute(semconv.GEN_AI_INPUT_MESSAGES, "secret")
        sp.set_attribute(semconv.GEN_AI_USAGE_INPUT_TOKENS, 10)  # non-content: kept
    assert semconv.GEN_AI_INPUT_MESSAGES not in off.spans[0].attributes
    assert off.spans[0].attributes[semconv.GEN_AI_USAGE_INPUT_TOKENS] == 10


def test_llm_call_uses_genai_keys():
    t = Tracer()
    with t.llm_call("gen", model="claude-haiku-4-5"):
        pass
    attrs = t.spans[0].attributes
    assert attrs[semconv.GEN_AI_REQUEST_MODEL] == "claude-haiku-4-5"
    assert attrs[semconv.GEN_AI_OPERATION_NAME] == "chat"


def test_export_jsonl(tmp_path):
    from harness.core import jsonio

    t = Tracer()
    with t.span("a", semconv.KIND_AGENT):
        pass
    p = tmp_path / "trace.jsonl"
    t.export_jsonl(p)
    rows = list(jsonio.read_jsonl(p))
    assert rows[0]["name"] == "a" and rows[0]["kind"] == semconv.KIND_AGENT

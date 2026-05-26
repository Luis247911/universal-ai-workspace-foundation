"""OpenTelemetry GenAI semantic-convention attribute names (verbatim string constants).

We take NO dependency on the OTel SDK — we only reuse the standardized attribute *names*
so traces are portable to any OTel-aware backend (Langfuse, Phoenix, ...). Names are not
code; reusing them is what keeps dashboards interoperable. See /sources/credits.md.

Spec: opentelemetry.io/docs/specs/semconv/gen-ai/ (Apache-2.0 / CC-BY).
"""

from __future__ import annotations

# --- span kinds (our taxonomy, mapped onto gen_ai operations) ---
KIND_LLM_CALL = "llm_call"
KIND_TOOL_CALL = "tool_call"
KIND_RETRIEVAL = "retrieval"
KIND_AGENT = "agent"
KIND_CHAIN = "chain"

# --- required-ish attributes ---
GEN_AI_OPERATION_NAME = "gen_ai.operation.name"
GEN_AI_PROVIDER_NAME = "gen_ai.provider.name"

# --- recommended attributes ---
GEN_AI_REQUEST_MODEL = "gen_ai.request.model"
GEN_AI_RESPONSE_MODEL = "gen_ai.response.model"
GEN_AI_USAGE_INPUT_TOKENS = "gen_ai.usage.input_tokens"
GEN_AI_USAGE_OUTPUT_TOKENS = "gen_ai.usage.output_tokens"
GEN_AI_RESPONSE_FINISH_REASONS = "gen_ai.response.finish_reasons"
GEN_AI_TOOL_NAME = "gen_ai.tool.name"

# --- opt-in, privacy-sensitive content (captured ONLY when explicitly enabled) ---
GEN_AI_INPUT_MESSAGES = "gen_ai.input.messages"
GEN_AI_OUTPUT_MESSAGES = "gen_ai.output.messages"
GEN_AI_SYSTEM_INSTRUCTIONS = "gen_ai.system_instructions"

CONTENT_ATTRIBUTES = frozenset(
    {GEN_AI_INPUT_MESSAGES, GEN_AI_OUTPUT_MESSAGES, GEN_AI_SYSTEM_INSTRUCTIONS}
)

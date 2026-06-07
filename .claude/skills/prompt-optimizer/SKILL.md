---
name: prompt-optimizer
description: Use this when a request is vague — short with no clear action verb, vague pronouns with no antecedent, or a semantically open question — to harden output quality by exposing assumptions and proceeding, asking back only when a wrong guess would be expensive. Triggers on "optimize my prompt", "sharpen this prompt", "senior prompt engineer pass", "this is vague", "what do you mean".
version: 1.0.0
compat: skill-format-1.0
status: experimental
---

# prompt-optimizer

A senior-prompt-engineer pass for vague requests. The goal is to harden the output of a quickly-typed
prompt **without** stalling the user with questions. Default to stating assumptions and proceeding;
ask back only when the ambiguity is both real and expensive to get wrong.

## When it applies

A request is "vague" when any of these hold:

- short with no clear action verb in the opening ("make that better");
- two or more vague pronouns with no antecedent ("fix it so it does the thing");
- a semantically open question ("can you do something with this?").

It does **not** apply to slash-commands, prompts carrying a file path or code block, or already-precise
multi-clause instructions — those are clear; do not second-guess them.

## Three-tier protocol

1. **Tier 1 (default) — expose assumptions, proceed.** Open with one to three explicit, checkable
   assumptions ("Assumption: you mean X, not Y. Assumption: output is markdown."), then act. Checkable
   beats vague: "you mean the login form" is worth stating; "we want clean code" is not.
2. **Tier 2 — one critical question.** Only when (a) two or more fundamentally different readings are
   plausible **and** (b) the wrong one is expensive (hours of work, an irreversible edit, an outbound
   send). One question, never a cascade.
3. **Tier 3 — understanding statement before big actions.** Before a substantial multi-file or
   sub-agent operation, one sentence: "I understand this as <restatement> — proceeding; stop me if off."

## Anti-patterns

- **Question cascade** — at most one clarifying question; never three in a row.
- **Quoting the whole vague prompt back** — too noisy; prefer two or three assumption bullets.
- **Mock assumptions** — assumptions must be falsifiable, not filler.
- **Triggering on clearly-structured prompts** — a precise request needs no pass.

## Boundaries

- This skill **owns** *request disambiguation* (assumptions-first, minimal-question protocol).
- For requiring a *human approval gate* before a risky step runs, use [[hitl-gate]] — that is approval,
  not disambiguation.
- For triaging *which skill* a problem needs, use [[agent-pattern-selector]].
- An opt-in hook can auto-detect vague prompts and inject this protocol — see the automation layer;
  default off.

## Attribution

General prompt-engineering practice (assumptions-first disambiguation; clarify only when costly); no
code or prose copied. See `/sources/credits.md`.

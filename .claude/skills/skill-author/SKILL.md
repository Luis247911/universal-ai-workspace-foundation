---
name: skill-author
description: Use this when you are creating or editing a skill for this harness — to follow the frontmatter contract, write an evals-first SKILL.md, and lint it before committing so it loads cleanly and stays domain-neutral. Triggers on "write a skill", "new skill", "SKILL.md", "author a skill", "skill frontmatter", "lint my skill".
version: 1.0.0
compat: skill-format-1.0
status: experimental
---

# skill-author

The meta-skill that builds other skills. It encodes this repo's skill-format contract and ships
the linter that enforces it — so a new skill loads, stays small, and is honest about its status.
This file is itself linted by the tool it documents (the repo dogfoods it).

## When to use

- Adding a new `.claude/skills/<slug>/` skill, or editing an existing one's frontmatter.
- Before committing a skill — lint it so CI does not bounce it.
- Deciding whether a skill needs a `scripts/` directory at all (usually it does not yet).

## Run the linter

```
python -m harness.skills lint .claude/skills                       # lint every skill
python -m harness.skills lint .claude/skills/eval-loop-builder      # lint one
python .claude/skills/skill-author/scripts/run.py lint .claude/skills
```

Exit is non-zero on any error-level issue.

## The frontmatter contract

```yaml
---
name: my-skill            # lowercase-hyphen, <=64 chars, no "claude"/"anthropic", == folder name
description: Use this when ...   # 3rd person, trigger phrases, <=1024 chars
version: 1.0.0            # SemVer
compat: skill-format-1.0  # the format this repo targets
status: experimental      # experimental | stable | deprecated
---
```

- **name** must equal the folder name (the linter checks this).
- **description** is the *only* thing the model sees before loading the body — front-load
  trigger phrases ("Use this when ...").
- **status** starts `experimental`; promote to `stable` only after the skill's `evaluate.md` passes.

## Authoring rules

1. **Evals-first**: if the skill has runnable behavior, write `evaluate.md` (rubric + ≥3
   scenarios with a no-skill baseline) before the body.
2. **No premature abstraction**: a skill starts as a single `SKILL.md`. Add a `scripts/`
   directory only when there is real code to run, and keep it a thin shim over the `harness`
   engine — never duplicate logic.
3. **Body < 500 lines**; push detail into `reference.md`. Bundle files one level deep.
4. **Declare boundaries**: name sibling skills and where this one stops, to avoid overlap.
5. **Domain-neutral**: no client, person, or private-project specifics — these skills ship publicly.

## Boundaries

- This skill **owns** the frontmatter contract and the `lint` tool.
- For scanning a skill's *scripts* for supply-chain risk, use [[skill-supply-chain-check]].
- For triaging which framework skill to reach for, use [[agent-pattern-selector]].

## Evals

See `evaluate.md` — 3 scenarios with a no-skill baseline.

## Attribution

Frontmatter shape (name/description) and evals-first authoring from the published Claude skill
format (concepts only). Reimplemented; no prose/code copied. See `/sources/credits.md`.

# CLAUDE.md — Tool-Delta für Claude Code

Ergänzt `AGENTS.md`, ersetzt sie nicht. Claude Code lädt automatisch nur diese Datei; die übrigen Boot-Dateien (`AGENTS.md` §1) kommen per `@`-Import, auch nach `/clear` und `/compact`:

@AGENTS.md
@.ai-workspace/state/project-index.md
@.ai-workspace/state/now.md
@.ai-workspace/knowledge/INDEX.md

## Claude-Code-Spezifika

- Vor `/compact`: Journal-Eintrag anhängen und `state/now.md` aktualisieren (`session-contract.md` §3). Fehlt `now.md`, legt der SessionStart-Hook `now_init` sie an.
- Slash-Commands aus Adaptern nicht ungefragt ausführen; Aktivierung pro Session bestätigen.
- Subagents: `delegation-policy.md`; ihre Outputs sind untrusted bis verifiziert.
- Skills/Hooks aus `~/.claude/` sind **keine** Projektpolitik; die lebt in `.ai-workspace/` und registrierten Adaptern.
- Execution-Schicht `.claude/` (`AGENTS.md` §2.5): Skills laden über ihre `description`, nicht beim Boot; Einstieg ist der Skill `agent-pattern-selector`. Skills schreiben nach `skills-authoring-policy.md`, linten mit `python -m harness.skills lint .claude/skills`. Hooks und Flags: `.claude/AUTOMATION.md`.
- Neue Projekte: `setup-protocol.md`; Frage 0 des Mount-Point-Decision-Trees routet Harness-Code nach `.claude/` bzw. `src/`.

Alle Pfade ohne Präfix liegen unter `.ai-workspace/`. Lade-Disziplin, Knowledge-Navigation und Critical-Claims-Regel: `AGENTS.md` §9–§10, `context-policy.md`, `knowledge-graph-policy.md`.

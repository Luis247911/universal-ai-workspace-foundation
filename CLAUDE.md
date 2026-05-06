# CLAUDE.md — Tool-Delta fuer Claude Code

Diese Datei ergaenzt `AGENTS.md`, sie ersetzt sie nicht. **Lies AGENTS.md zuerst.**

Sie enthaelt nur Claude-spezifische Hinweise. Operative Regeln, Boot-Order, Anti-Parallelstruktur und alle Policies stehen in `AGENTS.md` und den `.ai-workspace/`-Dateien.

## Claude-Code-Spezifika

- Vor `/compact`: aktualisiere `.ai-workspace/state/current-session.md` gemaess `.ai-workspace/session-contract.md`.
- Slash-Commands aus Adaptern werden nicht ungefragt ausgefuehrt; bestaetige Aktivierung pro Session.
- Bei Subagent-Spawn: folge `.ai-workspace/delegation-policy.md`. Outputs sind delegierte Arbeit (untrusted bis verifiziert).
- Skills/Hooks aus globalen User-Pfaden (z.B. `~/.claude/skills/`, `~/.claude/hooks/`) gelten **nicht** als Projektpolitik. Projektpolitik lebt in `.ai-workspace/` und in registrierten Adaptern.

## Setup-Protokoll bei neuen Projekten

Folge `.ai-workspace/setup-protocol.md`. Bevor irgendetwas ausserhalb der Foundation-Mount-Points entsteht, durchlaufe den Mount-Point-Decision-Tree (Section 6.2 dort).

## Context-Lade-Disziplin

`.ai-workspace/research/`, `.ai-workspace/scratch/`, `.ai-workspace/archive/`, einzelne `.ai-workspace/knowledge/<topic>/<slug>.md`, Inhalte unter `.ai-workspace/adapters/<slug>/` jenseits der `adapter.md`, Data-Space-Manifeste und Original-Binaerdateien werden **nicht automatisch geladen**. Siehe `.ai-workspace/context-policy.md`.

## Knowledge-Graph-Navigation

Bei Wissensanfragen:

1. Lies zuerst `.ai-workspace/knowledge/_index.md` (Root-MOC).
2. Identifiziere relevante Topic-MOCs (`.ai-workspace/knowledge/<topic>/_moc.md`).
3. Folge selektiv `[[wiki-links]]` zu konkreten Knowledge-Notes.
4. Lade nicht den ganzen Knowledge-Graph blind.

`[[wiki-links]]` werden beim Editieren erhalten oder bewusst aktualisiert. Tote Links werden nicht stillschweigend entfernt — markiere sie als `status: planned` im Frontmatter der Ziel-Note (auch als Stub erstellt) oder dokumentiere sie im naechsten Cleanup-Review.

## Bevorzugung verifizierter normalisierter Markdown

Im Arbeitsalltag bevorzugt verifiziertes normalisiertes Markdown nutzen — nicht standardmaessig die Original-Binaerdateien lesen. Originale bleiben Referenzquelle.

## Critical-Claims-Regel

Bei kritischen Aussagen muss auf das Originaldokument oder die Normalization Review zurueckverwiesen werden. Kritische Aussagen sind insbesondere:

- Zahlen, Daten, Fristen
- Namen, Tabellenwerte
- Definitionen, Anforderungen, Bewertungskriterien
- Negationen wie "nicht", "kein", "ausgeschlossen"
- Vertrags-, Regelungs- und Policy-Aussagen
- Alles, was Grundlage einer Entscheidung wird

Wenn die normalisierte Markdown-Version den `verification_status` `unverified` oder `partially_verified` hat, behandle die Inhalte mit entsprechendem Warnhinweis. `do_not_use`-Markdown wird nicht verwendet.

## Cross-Links

- Boot-Order und Prinzipien: `AGENTS.md`
- Setup neuer Projekte: `.ai-workspace/setup-protocol.md`
- Context-Loading: `.ai-workspace/context-policy.md`
- Session-Lifecycle: `.ai-workspace/session-contract.md`
- Knowledge-Graph + Normalization + Maintenance: `.ai-workspace/knowledge-graph-policy.md`

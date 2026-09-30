---
id: decisions
type: decisions
title: "Decision Log (generierte Sicht)"
status: active
generated: true
---
<!-- GENERIERT von harness.mdmemory index · nicht von Hand editieren -->

# Decision Log

**Generierte Sicht.** Kanonisch sind die Notizen unter `../knowledge/decision/` (D-2026-09-30-04). Neue Eintraege entstehen als Notiz (Vorlage `../templates/knowledge-note.md`), danach `python -m harness.mdmemory index`. Das alte Vollformat liefert `python -m harness.mdmemory export-legacy decisions`.

## Aktiv

- D-2026-09-30-08 · 2026-09-30 · [Memory-Vertrag: Besitz, Ladevertrag, Schreibwege und fuenf Festlegungen](../knowledge/decision/dec-2026-09-30-memory-vertrag-besitz-ladevertrag-2a34.md)
- D-2026-09-30-07 · 2026-09-30 · [.codex/ ist zweiter Execution-Mount, nur fuer die Hook-Konfiguration von Codex](../knowledge/decision/dec-2026-09-30-codex-ist-zweiter-execution-mount-nur-6a3b.md)
- D-2026-09-30-06 · 2026-09-30 · [Gedaechtnis-Hooks default AN; Hooks duerfen einen Abschluss-Eintrag ins eigene Journal schreiben](../knowledge/decision/dec-2026-09-30-gedaechtnis-hooks-sind-default-an-hooks-ec11.md) · ersetzt D-2026-09-30-02, D-2026-09-30-03
- D-2026-09-30-05 · 2026-09-30 · [Skripte unter src/ duerfen abgeleitete Markdown-Dateien in .ai-workspace/ schreiben](../knowledge/decision/dec-2026-09-30-05-skripte-unter-src-duerfen.md) · ersetzt D-2026-06-04-01
- D-2026-09-30-04 · 2026-09-30 · [Atomare Notizen unter knowledge/<typ>/ sind kanonisch; Register und Indizes werden generiert](../knowledge/decision/dec-2026-09-30-04-atomare-notizen-unter-knowledge.md)
- D-2026-09-30-01 · 2026-09-30 · [Der Live-Zustand liegt in state/now.md (gitignored, pro Worktree, harte Grenze…](../knowledge/decision/dec-2026-09-30-01-der-live-zustand-liegt-in-state.md) · ersetzt D-2026-06-07-01
- D-2026-06-07-02 · 2026-06-07 · [Vier zusaetzliche opt-in Execution-Hooks unter .claude/ (default AUS)…](../knowledge/decision/dec-2026-06-07-02-vier-zusaetzliche-opt-in.md)
- D-2026-06-06-02 · 2026-06-06 · [Eine optionale aktive Pflege-Routine (daily_maintenance) wird als opt-in…](../knowledge/decision/dec-2026-06-06-02-eine-optionale-aktive-pflege.md)
- D-2026-06-06-01 · 2026-06-06 · [Ein einmaliges Erst-Start-Onboarding feuert DEFAULT AN…](../knowledge/decision/dec-2026-06-06-01-ein-einmaliges-erst-start.md)

## Abgeloest, zurueckgezogen, archiviert

- D-2026-09-30-03 · 2026-09-30 · [Die Automatik-Schicht unter .claude/ bleibt opt-in und default AUS](../knowledge/decision/dec-2026-09-30-03-die-automatik-schicht-unter.md) → abgeloest durch D-2026-09-30-06
- D-2026-09-30-02 · 2026-09-30 · [Schreib-Doktrin fuer Execution-Hooks](../knowledge/decision/dec-2026-09-30-02-schreib-doktrin-fuer-execution.md) → abgeloest durch D-2026-09-30-06
- D-2026-06-07-01 · 2026-06-07 · [Durability-Modell von current-session.md ist kanonisch die lebende Datei +…](../knowledge/decision/dec-2026-06-07-01-durability-modell-von-current.md) → abgeloest durch D-2026-09-30-01
- D-2026-06-06-03 · 2026-06-06 · [Praezisierung der "Hook liest nur"-Doktrin: Execution-Hooks unter .claude/…](../knowledge/decision/dec-2026-06-06-03-praezisierung-der-hook-liest.md) → abgeloest durch D-2026-09-30-02
- D-2026-06-04-02 · 2026-06-04 · [Eine optionale, repo-committete Session-Automatik-Schicht (boot_reload +…](../knowledge/decision/dec-2026-06-04-02-eine-optionale-repo-committete.md) → abgeloest durch D-2026-09-30-03
- D-2026-06-04-01 · 2026-06-04 · [Der Governance-Core (.ai-workspace/) bleibt eingefroren markdown-only und…](../knowledge/decision/dec-2026-06-04-01-der-governance-core-ai.md) → abgeloest durch D-2026-09-30-05

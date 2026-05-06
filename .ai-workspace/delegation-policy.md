# delegation-policy.md — Generische Regeln fuer delegierte Arbeit

Diese Datei definiert den Vertrag fuer **delegierte Arbeit** unabhaengig vom konkreten Tool-Mechanismus. Sie definiert keine Agents.

## 1. Begriff

**Delegierte Arbeit** = jede Aktivitaet ausserhalb der Hauptsession, die einen Output zurueckliefert. Beispiele:

- Subagent-Aufruf (Tool-spezifisch).
- Hintergrundtask.
- Mehrminuetiger Tool-Call.
- Externe Analyse durch eine andere Session.
- Lookup in einem MCP-Server.
- Maintenance-Routine-Ausfuehrung.
- Document-Normalization-Schritt durch ein externes Tool.

Foundation definiert **keine Agents**. Sie definiert die Spielregeln, die fuer jede delegierte Arbeit gelten — egal ob sie tool-nativ als "Subagent" daherkommt oder als externer Service.

## 2. Sechs Pflicht-Regeln

Jede delegierte Arbeit folgt:

1. **Begrenzte Aufgabe.** Eine delegierte Arbeit hat genau einen Auftrag.
2. **Explizite Inputs.** Was die delegierte Arbeit lesen darf, wird benannt — kein implizites State-Lesen.
3. **Keine State-Mutations-Autoritaet.** Eine delegierte Arbeit darf keine Foundation-State-Files schreiben oder aendern. Sie liefert einen Report.
4. **Output-Report Pflicht.** Ergebnis wird in `templates/delegated-work-report.md`-Form geliefert.
5. **Verification-Status Pflicht.** Default: `unverified`. Erst nach Pruefung durch die Hauptsession kann der Status angehoben werden (siehe `quality-gates.md`).
6. **Hauptsession besitzt Integration.** Nur die Hauptsession entscheidet, ob und wie ein Report in `state/`/`knowledge/`/`deliverables/` einfliesst.

## 3. Untrusted-Output-Default

Jeder delegierte Output landet maximal in `research/` oder `scratch/`, nie direkt in `deliverables/`, `knowledge/` oder `state/`. Promote in hoehere Lifecycle-Zonen erfolgt nur ueber expliziten Quality-Gate-Schritt durch die Hauptsession (siehe `quality-gates.md`).

## 4. Adapter-Erweiterung

Adapter duerfen Subagents/Skills/Hooks/MCP-Configs/Maintenance-Routines/Normalization-Tools definieren. Diese Erweiterungen muessen die sechs Pflicht-Regeln respektieren und in `adapter.md` deklariert sein.

## 5. Verbotene Patterns

- Persistente Subagent-Mailboxes ohne Approval-Gate.
- "Latest-Run"-Auto-Resume ohne kanonischen Pointer in `state/current-session.md`.
- Subagent-Outputs ohne `templates/delegated-work-report.md`-Schema.
- Auto-Promote-zu-State (z.B. ein delegated Call der direkt `state/decisions.md` schreibt).
- Maintenance-Routines, die durable State direkt mutieren.
- RAG-Calls, die `do_not_load`-Direktiven ignorieren.
- Binaer-Verarbeitung ohne Sensitivity-Check.
- Outputs aus delegierter Arbeit, die ohne Verifikation in Knowledge-Notes oder Deliverables einfliessen.

## 6. Maintenance-Routine als delegierte Arbeit

Outputs einer Maintenance Routine (z.B. Link-Rot-Reports, Stale-Notes-Listen, Cleanup-Vorbereitungen, Source-Registry-Hygiene-Berichte, Document-Normalization-Status-Berichte):

- Werden via `templates/delegated-work-report.md` oder `templates/maintenance-routine.md`-Output-Sektion geliefert.
- Sind initial `unverified`.
- Mutieren niemals direkt durable State (Decisions, Source-Registry, Artifact-Index, Knowledge-Notes).
- Werden von der Hauptsession verifiziert; promovierte Findings landen in den entsprechenden State-/Knowledge-/Source-/Artifact-Dateien.

Maintenance Routines duerfen nicht:

- Eigenstaendig Secrets lesen.
- Externe Repos klonen oder downloaden.
- Binaerdateien automatisch verarbeiten, wenn Sensitivitaet ungeklaert ist.
- State-Dateien ohne Hauptsession-Review ueberschreiben.
- Findings direkt in durable State promoten.
- Neue Parallelstrukturen erzeugen.
- Aktive Hooks, MCP-Server oder Cronjobs im Core installieren.

## Cross-Links

- Output-Template: `templates/delegated-work-report.md`.
- Maintenance-Routine-Spezifikation: `templates/maintenance-routine.md`.
- Quality-Gates: `quality-gates.md`.
- Adapter: `adapter-policy.md`.
- Sicherheit: `security-policy.md`.

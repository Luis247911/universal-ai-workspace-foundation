---
name: pflege
description: Use this for the weekly maintenance of the workspace memory — lint, stale notes (review_after, last_confirmed), orphans, duplicate candidates, boot budget, unconsolidated journals and the monthly journal rollup; result is a report or a PR, never an auto-merge. Triggers on "pflege", "Wartung", "weekly maintenance", "memory health", "veraltete Notizen", "Gedaechtnis aufraeumen".
version: 1.0.0
compat: skill-format-1.0
status: experimental
---

# pflege

Woechentliche Pflege des Workspace-Gedaechtnisses (`memory-contract.md`). Der Skill findet
Probleme und schlaegt Loesungen vor. Er aendert keine Notiz ohne die Hauptsession, und nichts
wird automatisch gemergt.

## Wann

- Einmal pro Woche, manuell oder geplant (Planung: `reference.md`).
- Wenn `lint` Warnungen zeigt oder das Boot-Budget knapp wird.
- Vor einem Release oder einer groesseren Uebergabe.

## Ablauf

1. **Bericht erzeugen**: `python -m harness.mdmemory report --write`. Er landet unter
   `scratch/maintenance/<datum>-pflege.md` (gitignored). Dabei wird der Monats-Rollup
   `journal/YYYY/MM/_rollup.md` neu erzeugt; das ist eine generierte Datei (D-2026-09-30-05).
2. **Bericht lesen** und je Abschnitt entscheiden:

| Abschnitt | Vorschlag |
|---|---|
| Lint-Fehler | beheben; meist `mdmemory index` oder eine fehlende Rueckverknuepfung |
| Veraltet | Inhalt pruefen: noch wahr → `mdmemory confirm <id>`; nicht mehr wahr → Nachfolger + `supersede`; ungeklaert → Frage-Notiz |
| Waisen | verlinken (`links`), anheften, archivieren (`status: archived`) oder bewusst so lassen |
| Duplikat-Kandidaten | gleiche Aussage → UPDATE der einen und SUPERSEDE der anderen; Widerspruch → `conflict` |
| Nicht konsolidierte Journale | Skill `merken` ausfuehren |
| Boot-Budget ueber Ziel | Anheftungen pruefen (`pinned`), lange Summaries kuerzen; hart nie ueberschreiten |

3. **Rueckfragen** wie bei `merken`: Personen, globale Praeferenzen, Ersetzungen, Konflikte nur nach
   Bestaetigung.
4. **Ergebnis**: Aenderungen auf einem eigenen Branch (`pflege/<datum>`) committen und als PR
   vorschlagen, oder dem User den Bericht zeigen. **Kein Auto-Merge.** `lint` muss vor dem PR
   0 Fehler zeigen.
5. **Recall messen** (monatlich reicht): Recall-Set nach `templates/recall-set.md`. Unter 90 %
   Trefferquote erst Notizen und Summaries verbessern; Suche nur dokumentiert vorschlagen.

## Regeln

- Nichts loeschen. Archivieren, ersetzen oder zurueckziehen.
- Keine Notiz aendern, nur weil sie alt ist: Alter ist ein Anlass zu pruefen, kein Fehler.
- Berichte sind delegierte Arbeit (`delegation-policy.md`): `unverified`, bis die Hauptsession sie
  geprueft hat.
- Geplante Laeufe duerfen nur den Bericht und generierte Dateien erzeugen; alles andere braucht
  eine Session mit Mensch.

## Abgrenzung

- Konsolidierung Journal → Notiz: [[merken]]. `pflege` findet nur, was dort liegen geblieben ist.
- Der Hook `daily_maintenance` (opt-in) stupst einen Pflege-Pass an; `pflege` ist der Pass selbst.
- Boot-Budget-Optimierung jenseits des Gedaechtnisses: [[harness-optimizer]].

---
id: <delegated-work-slug>
type: delegated-work-report
title: "<aufgabe in 1 satz>"
status: draft
created: <YYYY-MM-DD>
updated: <YYYY-MM-DD>
owner: <delegated-instance-or-adapter-slug>
trust_level: external
lifecycle: research
verification_status: unverified
---

# Delegated Work Report

Generisches Template fuer Outputs jeder delegierten Arbeit. **Keine Agent-Namen, keine Rolle-Definitionen.** Diese Datei wird von der delegierten Instanz erzeugt; die Hauptsession verifiziert.

## 1. Aufgabe

`<1 satz: was war der konkrete auftrag>`

## 2. Scope

`<was war begrenzt; welche pfade durfte die delegierte arbeit lesen; welche nicht>`

## 3. Geprueefte Inputs

Liste der tatsaechlich gelesenen oder aufgerufenen Inputs:

- `<pfad-1 oder source-id-1>`
- `<pfad-2 oder source-id-2>`

## 4. Findings

Kurz, evidenz-basiert. Pro Finding eine Aussage + Verweis auf Input.

## 5. Unsicherheit

Was bleibt unklar? Welche Aussagen sind nur partiell gestuetzt?

## 6. Risiken

Was koennte schiefgehen, wenn die Findings ungeprueft uebernommen werden?

## 7. Empfehlungen

Konkrete Empfehlungen fuer die Hauptsession (was als naechstes tun, was zu pruefen).

## 8. Evidenz

Pointer zu Sources (`source-id`s aus `state/source-registry.md`), Files, Decisions.

## 9. Output Ownership

Dieser Report gehoert der **Hauptsession**. Die delegierte Instanz hat keine State-Mutations-Autoritaet (`delegation-policy.md` Regel 3).

## 10. Verification Status

- **Default:** `unverified`.
- Wird von Hauptsession ggf. auf `verified` oder `trusted` gehoben (siehe `quality-gates.md`).

## 11. Integrationsnotizen

Was muss die Hauptsession tun, um diesen Report zu integrieren? Wo sollen Findings landen (Decisions, Knowledge-Notes, Source-Registry-Updates, Artifact-Index)?

## Cross-Links

- Delegation-Policy: `../delegation-policy.md`.
- Quality-Gates: `../quality-gates.md`.
- Lifecycle: `../file-lifecycle.md`.

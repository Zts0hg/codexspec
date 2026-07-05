# Schnellstart

Diese Seite führt durch den kompletten **Requirements-First-SDD**-Ablauf in acht Schritten.
Bestätigte Anforderungen sind die höchstrangige Autorität, und nichts ist verbindlich, bis Sie es ausdrücklich bestätigen – jede Stufe endet an einem **Confirmation Gate**, das Sie steuern.

Bei kleinen, gut abgegrenzten Änderungen können Sie die ausführliche Wanderung überspringen und stattdessen `/codexspec:quick` verwenden.

## 1. Projekt initialisieren

Nach der Installation erstellen oder initialisieren Sie Ihr Projekt:

```bash
# Neues Projekt erstellen
codexspec init my-awesome-project

# Oder im aktuellen Verzeichnis initialisieren
codexspec init . --ai claude

# Mit chinesischer Ausgabe (legt die Ausgabebasis fest)
codexspec init my-project --lang zh-CN

# Vollständig nicht-interaktiv (CI/Skripte): zh-CN-Ausgabebasis, englische Commit-Nachrichten
codexspec init my-project --lang zh-CN --commit-lang en

# Jede Sprachdimension explizit setzen (skriptbar, keine Prompts)
codexspec init my-project \
  --interaction-lang zh-CN --document-lang en --commit-lang en
```

Wechseln Sie dann in das Projekt und starten Sie Claude Code:

```bash
cd my-awesome-project
claude
```

## 2. Projektprinzipien festlegen

Verwenden Sie den Constitution-Befehl, um die Standards festzulegen, gegen die jedes spätere Artefakt geprüft wird:

```
/codexspec:constitution Lege Prinzipien fest, die sich auf Codequalität und Testing konzentrieren
```

## 3. Anforderungen klären

Verwenden Sie `/codexspec:specify`, um Anforderungen zu erkunden:

```
/codexspec:specify Ich möchte eine Aufgabenverwaltungs-Anwendung bauen
```

Dieser Befehl stellt Klärungsfragen, deckt Randfälle auf und bittet Sie, eine finale Anforderungszusammenfassung zu bestätigen, die in `requirements.md` persistiert wird.

> **Confirmation Gate**: `/codexspec:specify` schreibt nur Einträge, die Sie ausdrücklich bestätigen. Die Zusammenfassung, die er Ihnen präsentiert, ist **nicht** verbindlich, bis Sie sie akzeptieren – lehnen Sie ab, ändern Sie oder öffnen Sie jeden Punkt neu, bevor Sie Ja sagen. Was Sie hier bestätigen, kann von nichts Downstream außer Kraft gesetzt werden.

## 4. Spezifikation generieren

Sobald die Anforderungszusammenfassung bestätigt ist, erzeugen Sie das Spec-Dokument:

```
/codexspec:generate-spec
```

`generate-spec` kompiliert die bestätigten Einträge in ein strukturiertes `spec.md` mit Quellverweisen für Nachvollziehbarkeit und führt dann ein automatisches Review aus (Mängel brauchen konkrete Beweise; empfehlende Hinweise lösen nie automatische Änderungen aus; verifizierte Mängel dürfen behoben und für höchstens zwei Runden erneut geprüft werden).

## 5. Überprüfen und validieren

**Empfohlen:** validieren Sie die Spec, bevor Sie fortfahren:

```
/codexspec:review-spec
```

Dies ist ein **evidenzbasiertes Review**: jeder gemeldete Mangel zitiert konkrete Beweise, und Design-Hinweise bleiben getrennt von der Akzeptanz.

## 6. Technischen Plan erstellen

```
/codexspec:spec-to-plan Verwende Python FastAPI für das Backend
```

Der Plan trägt `Covers`-Links zurück zu Spezifikationsanforderungen und prüft anwendbare Verfassungsprinzipien.

## 7. Aufgaben generieren

```
/codexspec:plan-to-tasks
```

Aufgaben sind um überprüfbare Ergebnisse herum organisiert, mit Traceability-Links zum Plan und zu den Anforderungen. Test-first-Reihenfolge wird **bedingt** angewendet – nur dort, wo Plan, Verfassung oder Aufgabenrisiko es erfordern. Nicht-testbare Aufgaben (Doku, Konfiguration) werden direkt implementiert.

## 8. Implementieren

```
/codexspec:implement-tasks
```

Die Implementierung folgt **Conditional TDD**: Code-Aufgaben nutzen den Red → Green → Verify → Refactor-Zyklus, wenn erforderlich; Dokumentations- und Konfigurationsaufgaben werden direkt implementiert.

## Kleine Änderungen: `/codexspec:quick`

Für eine kleine, gut abgegrenzte Änderung brauchen Sie nicht die vollständige achtstufige Wanderung. `/codexspec:quick` führt einen kompakten Requirements-First-SDD-Ablauf in einem einzigen Befehl aus:

```
/codexspec:quick Füge ein "Angemeldet bleiben"-Häkchen zum Login-Formular hinzu
```

Quick respektiert dieselben Schutzmaßnahmen wie der vollständige Ablauf:

- Es legt einen Feature-Workspace und eine `requirements.md` mit derselben Zeitstempel-Konvention wie `/codexspec:specify` an.
- Es präsentiert eine kompakte bestätigte Anforderungszusammenfassung (`NEED-*`, relevante `CON-*`/`DEC-*`, `OUT-*`, ungelöste `OPEN-*`) und wartet auf Ihre ausdrückliche Bestätigung – das **Confirmation Gate** greift weiterhin.
- Danach verkettet es `/codexspec:generate-spec` → `/codexspec:spec-to-plan` → `/codexspec:plan-to-tasks` → `/codexspec:implement-tasks` gegen dieses Feature-Verzeichnis, wobei jeder Generierungsbefehl seine eigene automatische Review-Schleife besitzt.

Stellt sich die Änderung als umfangreich heraus oder hat sie mehrere unabhängige Ergebnisse, pausiert Quick und empfiehlt stattdessen den Standard-Ablauf.

## Projektstruktur

Nach der Initialisierung:

```
my-project/
├── .codexspec/
│   ├── memory/
│   │   └── constitution.md    # Projektverfassung
│   ├── specs/
│   │   └── {feature-id}/
│   │       ├── spec.md        # Feature-Spezifikation
│   │       ├── plan.md        # Technischer Plan
│   │       ├── tasks.md       # Aufgaben-Aufteilung
│   │       └── checklists/    # Qualitäts-Checklisten
│   ├── templates/             # Eigene Vorlagen
│   ├── scripts/               # Hilfsskripte
│   └── extensions/            # Eigene Erweiterungen
├── .claude/
│   └── commands/              # Claude-Code-Slash-Befehle
├── .agents/
│   └── skills/                # Codex-Skills (wenn mit --ai codex oder both initialisiert)
├── CLAUDE.md                  # Claude-Code-Kontext
└── AGENTS.md                  # Codex-Kontext
```

## Nächste Schritte

[Vollständiger Workflow-Leitfaden](../user-guide/workflow.md)

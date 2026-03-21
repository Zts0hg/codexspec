# Workflow

CodexSpec strukturiert die Entwicklung in **überprüfbare Prüfpunkte** mit menschlicher Validierung in jeder Phase.

## Workflow-Übersicht

```
┌──────────────────────────────────────────────────────────────────────────┐
│                    CodexSpec Mensch-KI-Zusammenarbeit-Workflow            │
├──────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  1. Constitution  ──►  Projektprinzipien definieren                      │
│         │                                                                │
│         ▼                                                                │
│  2. Specify  ───────►  Interaktives Q&A zur Anforderungenklärung        │
│         │                                                                │
│         ▼                                                                │
│  3. Generate Spec  ─►  spec.md Dokument erstellen                        │
│         │               ✓ Automatische Überprüfung: review-spec.md       │
│         ▼                                                                │
│  4. Spec to Plan  ──►  Technischen Plan erstellen                        │
│         │               ✓ Automatische Überprüfung: review-plan.md       │
│         ▼                                                                │
│  5. Plan to Tasks  ─►  Atomare Aufgaben generieren                       │
│         │               ✓ Automatische Überprüfung: review-tasks.md      │
│         ▼                                                                │
│  6. Implement  ─────►  Ausführung mit bedingtem TDD-Workflow             │
│                                                                          │
└──────────────────────────────────────────────────────────────────────────┘
```

## Warum Überprüfung wichtig ist

| Ohne Überprüfung | Mit Überprüfung |
|-------------|------------|
| KI trifft falsche Annahmen | Mensch erfasst Fehlinterpretationen früh |
| Unvollständige Anforderungen verbreiten sich | Lücken vor der Implementierung identifiziert |
| Architektur driftet von der Absicht ab | Ausrichtung in jeder Phase verifiziert |
| **Ergebnis: Nachbesserung** | **Ergebnis: Beim ersten Mal richtig** |

## Automatische Überprüfung

Jeder Generierungsbefehl führt jetzt **automatisch eine Überprüfung durch**:

- `/codexspec:generate-spec` → ruft automatisch `review-spec` auf
- `/codexspec:spec-to-plan` → ruft automatisch `review-plan` auf
- `/codexspec:plan-to-tasks` → ruft automatisch `review-tasks` auf

Überprüfungsberichte werden zusammen mit den Artefakten erstellt, sodass Sie Probleme sofort sehen können.

## Iterative Qualitätsschleife

Wenn im Überprüfungsbericht Probleme gefunden werden, beschreiben Sie die Korrekturen in natürlicher Sprache und das System aktualisiert sowohl das Artefakt als auch den Bericht:

```
┌──────────────────────────────────────────────────────────────────────┐
│                    Iterative Qualitätsschleife                        │
├──────────────────────────────────────────────────────────────────────┤
│                                                                       │
│  Artefakt (spec/plan/tasks.md)                                        │
│         │                                                             │
│         ▼                                                             │
│  Automatische        Überprüfungsbericht                              │
│  Überprüfung  ───►  (review-*.md)                                     │
│         │                    │                                        │
│         │                    ▼                                        │
│         │             Probleme gefunden?                              │
│         │                    │                                        │
│         │              ┌─────┴─────┐                                  │
│         │              │           │                                  │
│         │             Ja        Nein                                   │
│         │              │           │                                  │
│         │              ▼           ▼                                  │
│         │     Korrektur im    Zum nächsten                            │
│         │     Gespräch        Schritt gehen                           │
│         │     beschreiben                                             │
│         │              │                                              │
│         │              ▼                                              │
│         │     Gleichzeitig aktualisieren:                             │
│         │       • Artefakt (spec/plan/tasks.md)                       │
│         │       • Überprüfungsbericht (review-*.md)                   │
│         │              │                                              │
│         └──────────────┘                                              │
│           (Wiederholen bis zufrieden)                                 │
│                                                                       │
│  Manuelle Neubewertung: Führen Sie /codexspec:review-*               │
│  jederzeit für eine neue Analyse aus                                  │
│                                                                       │
└──────────────────────────────────────────────────────────────────────┘
```

**Funktionsweise**:

1. **Automatische Überprüfung**: Jeder Generierungsbefehl führt automatisch die entsprechende Überprüfung durch
2. **Überprüfungsbericht**: Erstellt `review-*.md` Dateien mit gefundenen Problemen
3. **Iterative Korrektur**: Beschreiben Sie im Gespräch, was korrigiert werden muss, Artefakt und Bericht werden gemeinsam aktualisiert
4. **Manuelle Neubewertung**: Führen Sie `/codexspec:review-spec|plan|tasks` jederzeit für eine neue Analyse aus

## Kernbefehle

| Phase | Befehl | Zweck |
|-------|--------|-------|
| 1 | `/codexspec:constitution` | Projektprinzipien definieren |
| 2 | `/codexspec:specify` | Interaktives Q&A für Anforderungen |
| 3 | `/codexspec:generate-spec` | Spezifikationsdokument erstellen (★ Automatische Überprüfung) |
| - | `/codexspec:review-spec` | Automatisch aufgerufen, oder manuell neu validieren |
| 4 | `/codexspec:spec-to-plan` | Technischen Plan erstellen (★ Automatische Überprüfung) |
| - | `/codexspec:review-plan` | Automatisch aufgerufen, oder manuell neu validieren |
| 5 | `/codexspec:plan-to-tasks` | In Aufgaben aufteilen (★ Automatische Überprüfung) |
| - | `/codexspec:review-tasks` | Automatisch aufgerufen, oder manuell neu validieren |
| 6 | `/codexspec:implement-tasks` | Implementierung ausführen |

## Zwei-Phasen-Spezifikation

### specify vs clarify

| Aspekt | `/codexspec:specify` | `/codexspec:clarify` |
|--------|----------------------|----------------------|
| **Zweck** | Initiale Erkundung | Iterative Verfeinerung |
| **Wann** | Kein spec.md existiert | spec.md existiert, Lücken müssen gefüllt werden |
| **Eingabe** | Ihre ursprüngliche Idee | spec.md existent |
| **Ausgabe** | Keine (nur Dialog) | Aktualisiert spec.md |

## Bedingtes TDD

Die Implementierung folgt bedingtem TDD:

- **Code-Aufgaben**: Test-First (Rot → Grün → Verifizieren → Refaktorieren)
- **Nicht-testbare Aufgaben** (Dokumentation, Konfiguration): Direkte Implementierung

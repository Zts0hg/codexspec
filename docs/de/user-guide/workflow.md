# Workflow

CodexSpec strukturiert die Entwicklung in **ueberpruefbare Pruefpunkte** mit menschlicher Validierung in jeder Phase.

## Workflow-Uebersicht

```
+--------------------------------------------------------------------------+
|                    CodexSpec Mensch-KI-Zusammenarbeit-Workflow            |
+--------------------------------------------------------------------------+
|                                                                          |
|  1. Constitution  -->  Projektprinzipien definieren                      |
|         |                                                                |
|         v                                                                |
|  2. Specify  -------->  Interaktives Q&A zur Anforderungsklaerung        |
|         |                                                                |
|         v                                                                |
|  3. Generate Spec  ->  spec.md Dokument erstellen                        |
|         |                                                                |
|         v                                                                |
|  +---------------------------------------------------------------+      |
|  |  ★ REVIEW-GATE 1: /codexspec:review-spec ★                    |      |
|  +---------------------------------------------------------------+      |
|         |                                                                |
|         v                                                                |
|  4. Spec to Plan  -->  Technischen Plan erstellen                        |
|         |                                                                |
|         v                                                                |
|  +---------------------------------------------------------------+      |
|  |  ★ REVIEW-GATE 2: /codexspec:review-plan ★                    |      |
|  +---------------------------------------------------------------+      |
|         |                                                                |
|         v                                                                |
|  5. Plan to Tasks  ->  Atomare Aufgaben generieren                       |
|         |                                                                |
|         v                                                                |
|  +---------------------------------------------------------------+      |
|  |  ★ REVIEW-GATE 3: /codexspec:review-tasks ★                   |      |
|  +---------------------------------------------------------------+      |
|         |                                                                |
|         v                                                                |
|  6. Implement  ------->  Ausfuehrung mit bedingtem TDD-Workflow          |
|                                                                          |
+--------------------------------------------------------------------------+
```

## Warum Review wichtig ist

| Ohne Review | Mit Review |
|-------------|------------|
| KI trifft falsche Annahmen | Mensch erfasst Fehlinterpretationen frueh |
| Unvollstaendige Anforderungen verbreiten sich | Luecken vor der Implementierung identifiziert |
| Architektur driftet von der Absicht ab | Ausrichtung in jeder Phase verifiziert |
| **Ergebnis: Nachbesserung** | **Ergebnis: Beim ersten Mal richtig** |

## Kernbefehle

| Phase | Befehl | Zweck |
|-------|--------|-------|
| 1 | `/codexspec:constitution` | Projektprinzipien definieren |
| 2 | `/codexspec:specify` | Interaktives Q&A fuer Anforderungen |
| 3 | `/codexspec:generate-spec` | Spezifikationsdokument erstellen |
| - | `/codexspec:review-spec` | ★ Spezifikation validieren |
| 4 | `/codexspec:spec-to-plan` | Technischen Plan erstellen |
| - | `/codexspec:review-plan` | ★ Plan validieren |
| 5 | `/codexspec:plan-to-tasks` | In Aufgaben aufteilen |
| - | `/codexspec:review-tasks` | ★ Aufgaben validieren |
| 6 | `/codexspec:implement-tasks` | Implementierung ausfuehren |

## Zwei-Phasen-Spezifikation

### specify vs clarify

| Aspekt | `/codexspec:specify` | `/codexspec:clarify` |
|--------|----------------------|----------------------|
| **Zweck** | Initiale Erkundung | Iterative Verfeinerung |
| **Wann** | Kein spec.md existiert | spec.md existiert, Luecken muessen gefuellt werden |
| **Eingabe** | Ihre urspruengliche Idee | Existierendes spec.md |
| **Ausgabe** | Keine (nur Dialog) | Aktualisiert spec.md |

## Bedingtes TDD

Die Implementierung folgt bedingtem TDD:

- **Code-Aufgaben**: Test-First (Rot -> Gruen -> Verifizieren -> Refaktorieren)
- **Nicht-testbare Aufgaben** (Dokumentation, Konfiguration): Direkte Implementierung

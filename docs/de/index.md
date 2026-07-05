<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/images/codexspec-logo-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="assets/images/codexspec-logo-light.svg">
  <img alt="CodexSpec Logo" src="assets/images/codexspec-logo-light.svg" width="420">
</picture>

# Willkommen bei CodexSpec

[![PyPI version](https://img.shields.io/pypi/v/codexspec.svg)](https://pypi.org/project/codexspec/)
[![Python](https://img.shields.io/pypi/pyversions/codexspec.svg)](https://pypi.org/project/codexspec/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**Ein Requirements-First-SDD-Toolkit für Claude Code**

CodexSpec hilft Ihnen, hochwertige Software durch **Requirements-First Spec-Driven Development (SDD)** zu bauen – bestätigte Anforderungen sind die höchstrangige Autorität, und nichts ist verbindlich, bis Sie es ausdrücklich bestätigen. Anstatt sofort Code zu schreiben, legen Sie fest und bestätigen **was** Sie bauen und **warum**, bevor Sie entscheiden, **wie** es gebaut wird.

## Warum CodexSpec?

Warum CodexSpec zusätzlich zu Claude Code verwenden? Hier der Vergleich:

| Aspekt | Nur Claude Code | CodexSpec + Claude Code |
|--------|------------------|-------------------------|
| **Mehrsprachige Unterstützung** | Standardmäßig englische Interaktion | Team-Sprache konfigurieren für reibungslosere Zusammenarbeit und Reviews |
| **Nachvollziehbarkeit** | Entscheidungen nach Session-Ende schwer nachzuvollziehen | Alle Specs, Pläne und Aufgaben gespeichert in `.codexspec/specs/` |
| **Session-Wiederherstellung** | Unterbrochene Plan-Modus-Sessions lassen sich schwer wiederherstellen | Aufteilung auf mehrere Befehle + persistente Dokumente = einfache Wiederherstellung |
| **Team-Governance** | Keine einheitlichen Prinzipien, inkonsistente Stile | `constitution.md` setzt Team-Standards und Qualität durch |

### Was ist Requirements-First SDD?

**Requirements-First SDD** ist die Spec-Driven-Development-Methodik (SDD) mit einer Erweiterung: **Bestätigte Anforderungen sind die höchstrangige Autorität**. Sie definieren und bestätigen *was* gebaut wird und *warum*, bevor Sie entscheiden *wie* – und nichts wird verbindlich, bevor Sie es ausdrücklich bestätigen.

```
Traditionell:  Idee → Code → Debuggen → Neuschreiben
SDD:           Idee → Bestätigte Anforderungen → Spec → Plan → Aufgaben → Code
```

### Hauptmerkmale

- **Verfassungsbasierte Entwicklung** – Projektprinzipien festlegen, die alle Entscheidungen leiten
- **Persistente Anforderungen-Erfassung** – `/specify` speichert bestätigte Diskussionen in `requirements.md`, bevor Dokumente erzeugt werden
- **Automatische Reviews** – Jedes erzeugte Spec-, Plan- und Aufgaben-Artefakt enthält eingebaute Qualitätsprüfungen
- **Interaktive Klärung** – Q&A-basierte Anforderungsverfeinerung
- **Artefaktübergreifende Analyse** – Inkonsistenzen vor der Implementierung erkennen
- **Nachvollziehbare Aufgaben** – Aufgaben-Aufteilungen bewahren Anforderungs- und Planabdeckung und wenden **Conditional TDD** an (test-first-Reihenfolge nur dort, wo Plan, Verfassung oder Risiko es erfordern; nicht-testbare Aufgaben wie Doku/Konfiguration werden direkt implementiert)
- **Native Claude-Code-Integration** – Slash-Befehle funktionieren nahtlos
- **Mehrsprachige Unterstützung** – 13+ Sprachen über dynamische LLM-Übersetzung
- **Plattformübergreifend** – Bash- und PowerShell-Skripte inklusive
- **Erweiterbar** – Plugin-Architektur für eigene Befehle

## Schnellstart

```bash
# Installieren
uv tool install codexspec

# Neues Projekt erstellen
codexspec init my-project

# Oder in bestehendem Projekt initialisieren
codexspec init . --ai claude
```

[Vollständige Installationsanleitung](getting-started/installation.md)

## Workflow-Überblick

CodexSpec gliedert die Entwicklung in **überprüfbare Checkpoints**. Bestätigte Anforderungen fließen über Specs, Pläne und Aufgaben in den Code, mit einem Review an jedem Schritt.

```
Idee → Bestätigte Anforderungen → Spec → Plan → Aufgaben → Code
```

Jedes Artefakt wird von einem dedizierten Befehl erzeugt und validiert, bevor die nächste Stufe beginnt:

```
Idee → /specify → requirements.md → /generate-spec → spec.md → /spec-to-plan → plan.md → /plan-to-tasks → tasks.md → /implement
                                                   │                         │                            │
                                              Spec reviewen              Plan reviewen               Aufgaben reviewen
```

### Das Confirmation Gate

Das zentrale Abgrenzungsmerkmal ist das **Confirmation Gate**: Anforderungen, Specs, Pläne und Aufgaben werden erst nach Ihrer ausdrücklichen menschlichen Bestätigung verbindlich. Bestätigte Anforderungen sind die höchstrangige Feature-Autorität, sodass die AI Entscheidungen nicht stillschweigend festnageln kann – abgeleitete Artefakte tragen explizite Quellverweise, und Konflikte werden zurückverfolgt statt weitergetragen.

### Iterative Qualitätsschleife

Jeder Generierungsbefehl enthält ein **automatisches, evidenzbasiertes Review**: Mängel erfordern konkrete Beweise, empfehlende Hinweise lösen nie automatische Änderungen aus, und verifizierte Mängel dürfen behoben und für höchstens zwei Runden erneut geprüft werden. Diese Schleife hebt die Qualität, ohne dass Sie jedes Detail überwachen müssen.

[Workflow kennenlernen](user-guide/workflow.md)

## Lizenz

MIT-Lizenz – siehe [LICENSE](https://github.com/Zts0hg/codexspec/blob/main/LICENSE) für Details.

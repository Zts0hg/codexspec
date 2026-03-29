<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/images/codexspec-logo-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="assets/images/codexspec-logo-light.svg">
  <img alt="CodexSpec Logo" src="assets/images/codexspec-logo-light.svg" width="420">
</picture>

# Willkommen bei CodexSpec

[![PyPI version](https://img.shields.io/pypi/v/codexspec:svg)](https://pypi.org/project/codexspec/)
[![Python](https://img.shields.io/pypi/pyversions/codexspec:svg)](https://pypi.org/project/codexspec/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**Ein Spec-Driven Development (SDD) Toolkit fuer Claude Code**

CodexSpec ist ein Toolkit, das Ihnen hilft, qualitativ hochwertige Software mit einem strukturierten, spezifikationsgesteuerten Ansatz zu entwickeln. Es aendert die traditionelle Entwicklung, indem es Spezifikationen zu ausfuehrbaren Artefakten macht, die die Implementierung direkt leiten.

## Warum CodexSpec?

Warum CodexSpec zusaetzlich zu Claude Code verwenden? Hier ist der Vergleich:

| Aspekt | Nur Claude Code | CodexSpec + Claude Code |
|--------|-----------------|-------------------------|
| **Mehrsprachige Unterstuetzung** | Standardmaessig englische Interaktion | Team-Sprache konfigurieren fuer bessere Zusammenarbeit |
| **Nachverfolgbarkeit** | Schwer, Entscheidungen nach Sitzungsende zu verfolgen | Alle Specs, Plaene und Aufgaben in `.codexspec/specs/` gespeichert |
| **Sitzungswiederherstellung** | Schwer, nach Unterbrechungen im Plan-Modus wiederherzustellen | Multi-Command-Aufteilung + persistente Docs = einfache Wiederherstellung |
| **Team-Governance** | Keine einheitlichen Prinzipien, inkonsistente Stile | `constitution.md` setzt Team-Standards und Qualitaet durch |

### Mensch-KI-Zusammenarbeit

CodexSpec basiert auf der Ueberzeugung, dass **effektive KI-gestuetzte Entwicklung aktive menschliche Teilnahme in jeder Phase erfordert**.

| Problem | Loesung |
|---------|---------|
| Unklare Anforderungen | Interaktives Q&A zur Klaerung vor dem Erstellen |
| Unvollstaendige Spezifikationen | Dedizierte Review-Befehle mit Bewertung |
| Fehlausgerichtete technische Plaene | Verfassungsbasierte Validierung |
| Vage Aufgabenstellungen | TDD-erzwungene Aufgabenerstellung |

### Hauptfunktionen

- **Verfassungsbasiert** - Projektprinzipien festlegen, die alle Entscheidungen leiten
- **Interaktive Klaerung** - Q&A-basierte Anforderungsverfeinerung
- **Review-Befehle** - Artefakte in jeder Phase validieren
- **TDD-bereit** - Test-First-Methodik in Aufgaben integriert
- **i18n-Unterstützung** - 13+ Sprachen durch LLM-Uebersetzung

## Schnellstart

```bash
# Installation
uv tool install codexspec

# Neues Projekt erstellen
codexspec init mein-projekt

# Oder in bestehendem Projekt initialisieren
codexspec init . --ai claude
```

[Vollstaendige Installationsanleitung](getting-started/installation.md)

## Workflow-Uebersicht

```
Idee -> Klaeren -> Review -> Planen -> Review -> Aufgaben -> Review -> Implementieren
            ^              ^              ^
         Mensch prueft   Mensch prueft   Mensch prueft
```

Jedes Artefakt hat einen entsprechenden Review-Befehl zur Validierung der KI-Ausgabe vor dem Fortfahren.

[Workflow lernen](user-guide/workflow.md)

## Lizenz

MIT-Lizenz - siehe [LICENSE](https://github.com/Zts0hg/codexspec/blob/main/LICENSE) fuer Details.

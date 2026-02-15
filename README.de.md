# CodexSpec

[English](README.md) | [中文](README.zh-CN.md) | [日本語](README.ja.md) | [Español](README.es.md) | [Português](README.pt-BR.md) | [한국어](README.ko.md) | **Deutsch** | [Français](README.fr.md)

[![PyPI version](https://img.shields.io/pypi/v/codexspec.svg)](https://pypi.org/project/codexspec/)
[![Python](https://img.shields.io/pypi/pyversions/codexspec.svg)](https://pypi.org/project/codexspec/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**Ein Spec-Driven Development (SDD) Toolkit für Claude Code**

CodexSpec ist ein Toolkit, das Ihnen hilft, hochwertige Software mit einem strukturierten, spezifikationsgesteuerten Ansatz zu erstellen. Es kehrt die traditionelle Entwicklung um, indem es Spezifikationen in ausführbare Artefakte verwandelt, die die Implementierung direkt leiten.

## Funktionen

- **Strukturierter Workflow**: Klare Befehle für jede Entwicklungsphase
- **Claude Code Integration**: Native Slash-Befehle für Claude Code
- **Verfassungsbasiert**: Projektprinzipien leiten alle Entscheidungen
- **Spezifikation zuerst**: Definieren Sie was und warum vor dem wie
- **Plan-getrieben**: Technische Entscheidungen kommen nach den Anforderungen
- **Aufgabenorientiert**: Implementierung in ausführbare Aufgaben aufteilen
- **Qualitätssicherung**: Integrierte Review-, Analyse- und Checklisten-Befehle
- **Internationalisierung (i18n)**: Mehrsprachige Unterstützung durch LLM-Dynamische Übersetzung
- **Plattformübergreifend**: Unterstützung für Bash- und PowerShell-Skripte
- **Erweiterbar**: Plugin-Architektur für benutzerdefinierte Befehle

## Installation

### Voraussetzungen

- Python 3.11+
- [uv](https://docs.astral.sh/uv/) (empfohlen) oder pip

### Option 1: Mit uv installieren (Empfohlen)

Der einfachste Weg, CodexSpec zu installieren, ist mit uv:

```bash
uv tool install codexspec
```

### Option 2: Mit pip installieren

Alternativ können Sie pip verwenden:

```bash
pip install codexspec
```

### Option 3: Einmalige Verwendung

Direkt ausführen ohne Installation:

```bash
# Neues Projekt erstellen
uvx codexspec init my-project

# In einem bestehenden Projekt initialisieren
cd your-existing-project
uvx codexspec init . --ai claude
```

### Option 4: Von GitHub installieren (Entwicklungsversion)

Für die neueste Entwicklungsversion oder einen bestimmten Branch:

```bash
# Mit uv
uv tool install git+https://github.com/Zts0hg/codexspec.git

# Mit pip
pip install git+https://github.com/Zts0hg/codexspec.git

# Bestimmter Branch oder Tag
uv tool install git+https://github.com/Zts0hg/codexspec.git@main
uv tool install git+https://github.com/Zts0hg/codexspec.git@v0.2.0
```

## Schnellstart

Nach der Installation können Sie die CLI verwenden:

```bash
# Neues Projekt erstellen (deutsche Ausgabe)
codexspec init my-project --lang de

# In bestehendem Projekt initialisieren
codexspec init . --ai claude

# Installierte Tools überprüfen
codexspec check

# Version anzeigen
codexspec version
```

Upgrade auf die neueste Version:

```bash
# Mit uv
uv tool install codexspec --upgrade

# Mit pip
pip install --upgrade codexspec
```

## Verwendung

### 1. Projekt initialisieren

Nach der [Installation](#installation) erstellen oder initialisieren Sie Ihr Projekt:

```bash
codexspec init my-awesome-project --lang de
```

### 2. Projektprinzipien festlegen

Starten Sie Claude Code im Projektverzeichnis:

```bash
cd my-awesome-project
claude
```

Verwenden Sie den Befehl `/codexspec.constitution`, um die Governance-Prinzipien des Projekts zu erstellen:

```
/codexspec.constitution Prinzipien erstellen, die sich auf Codequalität, Teststandards und Clean Architecture konzentrieren
```

### 3. Spezifikation erstellen

Verwenden Sie `/codexspec.specify`, um zu definieren, was Sie erstellen möchten:

```
/codexspec.specify Eine Aufgabenverwaltungsanwendung mit folgenden Funktionen erstellen: Aufgaben erstellen, Benutzern zuweisen, Fälligkeitsdaten setzen und Fortschritt verfolgen
```

### 4. Anforderungen klären (Optional aber empfohlen)

Verwenden Sie `/codexspec.clarify`, um Unklarheiten vor der Planung zu klären:

```
/codexspec.clarify
```

### 5. Technischen Plan erstellen

Verwenden Sie `/codexspec.spec-to-plan`, um zu definieren, wie implementiert werden soll:

```
/codexspec.spec-to-plan Python mit FastAPI für das Backend, PostgreSQL für die Datenbank und React für das Frontend verwenden
```

### 6. Aufgaben generieren

Verwenden Sie `/codexspec.plan-to-tasks`, um den Plan aufzuteilen:

```
/codexspec.plan-to-tasks
```

### 7. Analysieren (Optional aber empfohlen)

Verwenden Sie `/codexspec.analyze` für artefaktübergreifende Konsistenzprüfung:

```
/codexspec.analyze
```

### 8. Implementieren

Verwenden Sie `/codexspec.implement-tasks`, um die Implementierung auszuführen:

```
/codexspec.implement-tasks
```

## Verfügbare Befehle

### CLI-Befehle

| Befehl | Beschreibung |
|--------|--------------|
| `codexspec init` | Neues CodexSpec-Projekt initialisieren |
| `codexspec check` | Installierte Tools überprüfen |
| `codexspec version` | Versionsinformationen anzeigen |
| `codexspec config` | Projektkonfiguration anzeigen oder ändern |

### `codexspec init` Optionen

| Option | Beschreibung |
|--------|--------------|
| `PROJECT_NAME` | Name für Ihr neues Projektverzeichnis |
| `--here`, `-h` | Im aktuellen Verzeichnis initialisieren |
| `--ai`, `-a` | Zu verwendender KI-Assistent (Standard: claude) |
| `--lang`, `-l` | Ausgabesprache (z.B. en, de, zh-CN, ja) |
| `--force`, `-f` | Bestehende Dateien überschreiben |
| `--no-git` | Git-Initialisierung überspringen |
| `--debug`, `-d` | Debug-Ausgabe aktivieren |

### `codexspec config` Optionen

| Option | Beschreibung |
|--------|--------------|
| `--set-lang`, `-l` | Ausgabesprache festlegen |
| `--list-langs` | Alle unterstützten Sprachen auflisten |

### Slash-Befehle

Nach der Initialisierung sind diese Slash-Befehle in Claude Code verfügbar:

#### Kernbefehle

| Befehl | Beschreibung |
|--------|--------------|
| `/codexspec.constitution` | Projekt-Governance-Prinzipien erstellen oder aktualisieren |
| `/codexspec.specify` | Definieren, was Sie erstellen möchten (Anforderungen) |
| `/codexspec.generate-spec` | Detaillierte Spezifikation aus Anforderungen generieren |
| `/codexspec.spec-to-plan` | Spezifikation in technischen Plan umwandeln |
| `/codexspec.plan-to-tasks` | Plan in ausführbare Aufgaben aufteilen |
| `/codexspec.implement-tasks` | Aufgaben gemäß Aufteilung ausführen |

#### Review-Befehle

| Befehl | Beschreibung |
|--------|--------------|
| `/codexspec.review-spec` | Vollständigkeit der Spezifikation überprüfen |
| `/codexspec.review-plan` | Machbarkeit des technischen Plans überprüfen |
| `/codexspec.review-tasks` | Vollständigkeit der Aufgabenverteilung überprüfen |

#### Erweiterte Befehle

| Befehl | Beschreibung |
|--------|--------------|
| `/codexspec.clarify` | Unklare Bereiche vor der Planung klären |
| `/codexspec.analyze` | Artefaktübergreifende Konsistenzanalyse |
| `/codexspec.checklist` | Qualitätschecklisten für Anforderungen generieren |
| `/codexspec.tasks-to-issues` | Aufgaben in GitHub-Issues umwandeln |

## Workflow-Übersicht

```
┌──────────────────────────────────────────────────────────────┐
│                    CodexSpec Workflow                        │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  1. Constitution  ──►  Projektprinzipien definieren          │
│         │                                                    │
│         ▼                                                    │
│  2. Specify  ───────►  Funktionsspezifikation erstellen      │
│         │                                                    │
│         ▼                                                    │
│  3. Clarify  ───────►  Unklarheiten klären (optional)        │
│         │                                                    │
│         ▼                                                    │
│  4. Review Spec  ───►  Spezifikation validieren              │
│         │                                                    │
│         ▼                                                    │
│  5. Spec to Plan  ──►  Technischen Plan erstellen            │
│         │                                                    │
│         ▼                                                    │
│  6. Review Plan  ───►  Technischen Plan validieren           │
│         │                                                    │
│         ▼                                                    │
│  7. Plan to Tasks  ─►  Aufgabenverteilung generieren         │
│         │                                                    │
│         ▼                                                    │
│  8. Analyze  ───────►  Artefaktübergreifende Konsistenz (optional) │
│         │                                                    │
│         ▼                                                    │
│  9. Review Tasks  ──►  Aufgabenverteilung validieren         │
│         │                                                    │
│         ▼                                                    │
│  10. Implement  ─────►  Implementierung ausführen            │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

## Projektstruktur

Nach der Initialisierung hat Ihr Projekt diese Struktur:

```
my-project/
├── .codexspec/
│   ├── memory/
│   │   └── constitution.md    # Projekt-Governance-Prinzipien
│   ├── specs/
│   │   └── {feature-id}/
│   │       ├── spec.md        # Funktionsspezifikation
│   │       ├── plan.md        # Technischer Plan
│   │       ├── tasks.md       # Aufgabenverteilung
│   │       └── checklists/    # Qualitätschecklisten
│   ├── templates/             # Benutzerdefinierte Vorlagen
│   ├── scripts/               # Hilfsskripte
│   │   ├── bash/              # Bash-Skripte
│   │   └── powershell/        # PowerShell-Skripte
│   └── extensions/            # Benutzerdefinierte Erweiterungen
├── .claude/
│   └── commands/              # Slash-Befehle für Claude Code
└── CLAUDE.md                  # Kontext für Claude Code
```

## Internationalisierung (i18n)

CodexSpec unterstützt mehrere Sprachen durch **LLM-Dynamische Übersetzung**. Anstatt übersetzte Vorlagen zu pflegen, lässt Claude Inhalte zur Laufzeit basierend auf Ihrer Sprachkonfiguration übersetzen.

### Sprache festlegen

**Während der Initialisierung:**
```bash
# Ein Projekt mit chinesischer Ausgabe erstellen
codexspec init my-project --lang zh-CN

# Ein Projekt mit japanischer Ausgabe erstellen
codexspec init my-project --lang ja
```

**Nach der Initialisierung:**
```bash
# Aktuelle Konfiguration anzeigen
codexspec config

# Spracheinstellung ändern
codexspec config --set-lang zh-CN

# Unterstützte Sprachen auflisten
codexspec config --list-langs
```

### Konfigurationsdatei

Die Datei `.codexspec/config.yml` speichert die Spracheinstellungen:

```yaml
version: "1.0"

language:
  # Ausgabesprache für Claude-Interaktionen und generierte Dokumente
  output: "zh-CN"

  # Vorlagensprache - als "en" belassen für Kompatibilität
  templates: "en"

project:
  ai: "claude"
  created: "2026-02-15"
```

### Unterstützte Sprachen

| Code | Sprache |
|------|---------|
| `en` | English (Standard) |
| `zh-CN` | 中文（简体） |
| `zh-TW` | 中文（繁體） |
| `ja` | 日本語 |
| `ko` | 한국어 |
| `es` | Español |
| `fr` | Français |
| `de` | Deutsch |
| `pt` | Português |
| `ru` | Русский |
| `it` | Italiano |
| `ar` | العربية |
| `hi` | हिन्दी |

### Funktionsweise

1. **Einzelne englische Vorlagen**: Alle Befehlsvorlagen bleiben auf Englisch
2. **Sprachkonfiguration**: Das Projekt gibt die bevorzugte Ausgabesprache an
3. **Dynamische Übersetzung**: Claude liest englische Anweisungen, gibt in der Zielsprache aus
4. **Kontextbewusst**: Technische Begriffe (JWT, OAuth, etc.) bleiben bei Bedarf auf Englisch

### Vorteile

- **Keine Übersetzungspflege**: Keine Notwendigkeit, mehrere Vorlagenversionen zu pflegen
- **Immer aktuell**: Vorlagen-Updates kommen automatisch allen Sprachen zugute
- **Kontextbewusste Übersetzung**: Claude liefert natürliche, kontextgerechte Übersetzungen
- **Unbegrenzte Sprachen**: Jede von Claude unterstützte Sprache funktioniert sofort

## Erweiterungssystem

CodexSpec unterstützt eine Plugin-Architektur für benutzerdefinierte Befehle:

### Erweiterungsstruktur

```
my-extension/
├── extension.yml          # Erweiterungs-Manifest
├── commands/              # Benutzerdefinierte Slash-Befehle
│   └── command.md
└── README.md
```

### Erweiterungen erstellen

1. Kopieren Sie die Vorlage aus `extensions/template/`
2. Modifizieren Sie `extension.yml` mit Ihren Erweiterungsdetails
3. Fügen Sie Ihre benutzerdefinierten Befehle in `commands/` hinzu
4. Testen Sie lokal und veröffentlichen Sie

Siehe `extensions/EXTENSION-DEVELOPMENT-GUIDE.md` für Details.

## Entwicklung

### Voraussetzungen

- Python 3.11+
- uv Paketmanager
- Git

### Lokale Entwicklung

```bash
# Repository klonen
git clone https://github.com/Zts0hg/codexspec.git
cd codexspec

# Entwicklungsabhängigkeiten installieren
uv sync --dev

# Lokal ausführen
uv run codexspec --help

# Tests ausführen
uv run pytest

# Code linten
uv run ruff check src/
```

### Bauen

```bash
# Paket bauen
uv build
```

## Vergleich mit spec-kit

CodexSpec ist von GitHub's spec-kit inspiriert, aber mit einigen wichtigen Unterschieden:

| Funktion | spec-kit | CodexSpec |
|----------|----------|-----------|
| Kernphilosophie | Spezifikationsgesteuerte Entwicklung | Spezifikationsgesteuerte Entwicklung |
| CLI-Name | `specify` | `codexspec` |
| Primäre KI | Multi-Agent-Unterstützung | Claude Code fokussiert |
| Befehlspräfix | `/speckit.*` | `/codexspec.*` |
| Workflow | specify → plan → tasks → implement | constitution → specify → clarify → plan → tasks → analyze → implement |
| Review-Schritte | Optional | Integrierte Review-Befehle |
| Clarify-Befehl | Ja | Ja |
| Analyze-Befehl | Ja | Ja |
| Checklist-Befehl | Ja | Ja |
| Erweiterungssystem | Ja | Ja |
| PowerShell-Skripte | Ja | Ja |
| i18n-Unterstützung | Nein | Ja (13+ Sprachen via LLM-Übersetzung) |

## Philosophie

CodexSpec folgt diesen Kernprinzipien:

1. **Absichtsgesteuerte Entwicklung**: Spezifikationen definieren das "Was" vor dem "Wie"
2. **Umfangreiche Spezifikationserstellung**: Guardrails und Organisationsprinzipien verwenden
3. **Mehrstufige Verfeinerung**: Statt One-Shot-Codegenerierung
4. **Hohe KI-Abhängigkeit**: KI für Spezifikationsinterpretation nutzen
5. **Review-orientiert**: Jedes Artefakt validieren, bevor weitergemacht wird
6. **Qualität zuerst**: Integrierte Checklisten und Analysen für Anforderungsqualität

## Mitwirken

Beiträge sind willkommen! Bitte lesen Sie unsere Mitwirkungsrichtlinien, bevor Sie einen Pull-Request einreichen.

## Lizenz

MIT-Lizenz - siehe [LICENSE](LICENSE) für Details.

## Danksagung

- Inspiriert von [GitHub spec-kit](https://github.com/github/spec-kit)
- Erstellt für [Claude Code](https://claude.ai/code)

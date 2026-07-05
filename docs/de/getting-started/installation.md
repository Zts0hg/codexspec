# Installation

## Voraussetzungen

- Python 3.11+
- [uv](https://docs.astral.sh/uv/) (empfohlen) oder pip

## Option 1: Installation mit uv (Empfohlen)

Der einfachste Weg, CodexSpec zu installieren, ist die Verwendung von uv:

```bash
uv tool install codexspec
```

## Option 2: Installation mit pip

Alternativ können Sie pip verwenden:

```bash
pip install codexspec
```

## Option 3: Einmalige Verwendung

Direkt ausführen ohne Installation:

```bash
# Neues Projekt erstellen
uvx codexspec init my-project

# In einem bestehenden Projekt für Claude Code initialisieren
cd your-existing-project
uvx codexspec init . --ai claude

# Für Codex CLI initialisieren
uvx codexspec init . --ai codex

# Für Claude Code und Codex CLI gleichzeitig initialisieren (schreibt .claude/ und .agents/)
uvx codexspec init . --ai both
```

## Option 4: Installation von GitHub

Für die neueste Entwicklungsversion:

```bash
# Mit uv
uv tool install git+https://github.com/Zts0hg/codexspec.git

# Mit pip
pip install git+https://github.com/Zts0hg/codexspec.git

# Bestimmter Branch oder Tag
uv tool install git+https://github.com/Zts0hg/codexspec.git@main
uv tool install git+https://github.com/Zts0hg/codexspec.git@v0.5.6
```

## Option 5: Installation über den Plugin-Marketplace (Alternative)

CodexSpec ist auch als Claude-Code-Plugin verfügbar. Diese Methode eignet sich, wenn Sie CodexSpecs Slash-Befehle direkt in Claude Code verwenden möchten, ohne das CLI-Tool zu installieren. Das CLI bietet das vollständige Requirements-First-SDD-Erlebnis; das Plugin liefert die Slash-Befehle obendrauf.

### Installationsschritte

In Claude Code:

```bash
# Marketplace hinzufügen
> /plugin marketplace add Zts0hg/codexspec

# Plugin installieren
> /plugin install codexspec@codexspec-market
```

### Sprachkonfiguration für Plugin-Nutzer

Konfigurieren Sie nach der Installation über den Plugin-Marketplace Ihre bevorzugte Sprache mit dem Slash-Befehl `/codexspec:config` (der CLI-Befehl `codexspec config` ist ohne CLI-Installation nicht verfügbar):

```bash
# Interaktive Konfiguration starten
> /codexspec:config

# Oder aktuelle Konfiguration anzeigen
> /codexspec:config --view
```

Der Config-Befehl führt Sie durch die Auswahl der Ausgabesprache (für erzeugte Dokumente) und der Commit-Nachrichten-Sprache und schreibt dann `.codexspec/config.yml`. Die mehrsprachige Unterstützung nutzt dieselbe dynamische LLM-Übersetzung wie das CLI.

### Vergleich der Installationsmethoden

| Methode | Am besten für | Funktionen |
|---------|---------------|------------|
| **CLI-Installation** (`uv tool install` oder `pip install`) | Voller Entwicklungs-Workflow | CLI-Befehle (`init`, `check`, `config`, `version`) + Slash-Befehle |
| **Plugin-Marketplace** | Schnellstart, bestehende Projekte | Nur Slash-Befehle (verwenden Sie `/codexspec:config` für die Spracheinstellung) |

**Hinweis**: Das Plugin verwendet den Modus `strict: false` und nutzt die bestehende mehrsprachige Unterstützung über dynamische LLM-Übersetzung.

## Installation überprüfen

```bash
codexspec --help
codexspec version
```

(Bei Installationen über den Plugin-Marketplace überprüfen Sie, indem Sie einen beliebigen Slash-Befehl wie `/codexspec:config --view` in Claude Code ausführen.)

## Upgrade

```bash
# Mit uv
uv tool install codexspec --upgrade

# Mit pip
pip install --upgrade codexspec
```

(Installationen über den Plugin-Marketplace werden vom Plugin-Manager von Claude Code aktualisiert.)

## Nächste Schritte

[Schnellstart](quick-start.md)

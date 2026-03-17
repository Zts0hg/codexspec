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

Alternativ koennen Sie pip verwenden:

```bash
pip install codexspec
```

## Option 3: Einmalige Verwendung

Direkt ausfuehren ohne Installation:

```bash
# Neues Projekt erstellen
uvx codexspec init mein-projekt

# In einem bestehenden Projekt initialisieren
cd ihr-bestehendes-projekt
uvx codexspec init . --ai claude
```

## Option 4: Installation von GitHub

Fuer die neueste Entwicklungsversion:

```bash
# Mit uv
uv tool install git+https://github.com/Zts0hg/codexspec:git

# Mit pip
pip install git+https://github.com/Zts0hg/codexspec:git

# Bestimmter Branch oder Tag
uv tool install git+https://github.com/Zts0hg/codexspec:git@main
uv tool install git+https://github.com/Zts0hg/codexspec:git@v0.2.0
```

## Installation ueberpruefen

```bash
codexspec --help
codexspec version
```

## Upgrade

```bash
# Mit uv
uv tool install codexspec --upgrade

# Mit pip
pip install --upgrade codexspec
```

## Naechste Schritte

[Schnellstart](quick-start.md)

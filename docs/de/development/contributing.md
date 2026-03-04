# Mitwirken

## Voraussetzungen

- Python 3.11+
- uv-Paketmanager
- Git

## Lokale Entwicklung

```bash
# Repository klonen
git clone https://github.com/Zts0hg/codexspec.git
cd codexspec

# Entwicklungsabhaengigkeiten installieren
uv sync --dev

# Lokal ausfuehren
uv run codexspec --help

# Tests ausfuehren
uv run pytest

# Code linten
uv run ruff check src/
```

## Dokumentation

```bash
# Dokumentationsabhaengigkeiten installieren
uv sync --extra docs

# Dokumentation lokal vorschauen
uv run mkdocs serve

# Dokumentation erstellen
uv run mkdocs build
```

## Erstellung

```bash
uv build
```

## Pull-Request-Prozess

1. Repository forken
2. Feature-Branch erstellen
3. Aenderungen vornehmen
4. Tests und Linting ausfuehren
5. Pull-Request einreichen

## Code-Stil

- Zeilenlaenge: maximal 120 Zeichen
- PEP 8 befolgen
- Type-Hints fuer oeffentliche Funktionen verwenden

# Beitragen

## Voraussetzungen

- Python 3.11+
- uv-Paketmanager
- Git

## Lokale Entwicklung

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

## Dokumentation

```bash
# Doku-Abhängigkeiten installieren
uv sync --extra docs

# Dokumentation lokal vorschauen
uv run mkdocs serve

# Dokumentation bauen
uv run mkdocs build
```

## Bauen

```bash
uv build
```

## Pull-Request-Prozess

1. Repository forken
2. Feature-Branch anlegen
3. Änderungen vornehmen
4. Tests und Linting ausführen
5. Pull-Request einreichen

## Code-Stil

- Zeilenlänge: maximal 120 Zeichen
- PEP 8 befolgen
- Type-Hints für öffentliche Funktionen verwenden

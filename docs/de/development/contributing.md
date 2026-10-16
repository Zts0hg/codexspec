# Beitragen

## Voraussetzungen

- Python 3.11+
- uv-Paketmanager
- Git

## Lokale Entwicklung

```bash
# Clone the repository
git clone https://github.com/Zts0hg/codexspec.git
cd codexspec

# Install development dependencies
uv sync --extra dev

# Run locally
uv run codexspec --help

# Run tests
uv run pytest

# Lint code
uv run ruff check src/
```

## Dokumentation

```bash
# Install docs dependencies
uv sync --extra dev --extra docs

# Preview documentation locally
uv run mkdocs serve

# Build documentation
uv run mkdocs build --strict
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

Lesen Sie [CLAUDE.md](https://github.com/Zts0hg/codexspec/blob/main/CLAUDE.md), [AGENTS.md](https://github.com/Zts0hg/codexspec/blob/main/AGENTS.md) und
[Repository-Struktur](https://github.com/Zts0hg/codexspec/blob/main/docs/internal/repository-layout.md), bevor Sie Vorlagen,
Paketierung oder Initialisierung ändern. Ausgelieferte Kopien von Befehlen und
Skills sind generierte Installationsartefakte. Bearbeiten Sie ihre maßgeblichen
Quellen und erzeugen Sie die Kopien erneut.

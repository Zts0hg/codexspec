# Contribuir

## Requisitos previos

- Python 3.11+
- Gestor de paquetes uv
- Git

## Desarrollo local

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

## Documentación

```bash
# Install docs dependencies
uv sync --extra dev --extra docs

# Preview documentation locally
uv run mkdocs serve

# Build documentation
uv run mkdocs build --strict
```

## Build

```bash
uv build
```

## Proceso de Pull Request

1. Haz fork del repositorio
2. Crea una rama de funcionalidad
3. Realiza tus cambios
4. Ejecuta pruebas y lint
5. Envía un pull request

## Estilo de código

- Longitud de línea: máximo 120 caracteres
- Sigue PEP 8
- Usa type hints en las funciones públicas

Antes de modificar las plantillas, el empaquetado o la inicialización, lee
[CLAUDE.md](https://github.com/Zts0hg/codexspec/blob/main/CLAUDE.md), [AGENTS.md](https://github.com/Zts0hg/codexspec/blob/main/AGENTS.md) y
[Distribución del repositorio](https://github.com/Zts0hg/codexspec/blob/main/docs/internal/repository-layout.md). Las copias
distribuidas de los comandos y las habilidades son artefactos de instalación
generados; modifica sus fuentes autorizadas y vuelve a generarlas.

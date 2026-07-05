# Contribuir

## Requisitos previos

- Python 3.11+
- Gestor de paquetes uv
- Git

## Desarrollo local

```bash
# Clonar el repositorio
git clone https://github.com/Zts0hg/codexspec.git
cd codexspec

# Instalar las dependencias de desarrollo
uv sync --dev

# Ejecutar en local
uv run codexspec --help

# Ejecutar las pruebas
uv run pytest

# Hacer lint del código
uv run ruff check src/
```

## Documentación

```bash
# Instalar las dependencias de documentación
uv sync --extra docs

# Previsualizar la documentación en local
uv run mkdocs serve

# Construir la documentación
uv run mkdocs build
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

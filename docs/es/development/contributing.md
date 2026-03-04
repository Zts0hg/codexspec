# Contribuir

## Requisitos Previos

- Python 3.11+
- Gestor de paquetes uv
- Git

## Desarrollo Local

```bash
# Clonar el repositorio
git clone https://github.com/Zts0hg/codexspec.git
cd codexspec

# Instalar dependencias de desarrollo
uv sync --dev

# Ejecutar localmente
uv run codexspec --help

# Ejecutar pruebas
uv run pytest

# Linting de codigo
uv run ruff check src/
```

## Documentacion

```bash
# Instalar dependencias de documentacion
uv sync --extra docs

# Previsualizar documentacion localmente
uv run mkdocs serve

# Construir documentacion
uv run mkdocs build
```

## Compilacion

```bash
uv build
```

## Proceso de Pull Request

1. Hacer fork del repositorio
2. Crear una rama de funcionalidad
3. Hacer tus cambios
4. Ejecutar pruebas y linting
5. Enviar un pull request

## Estilo de Codigo

- Longitud de linea: maximo 120 caracteres
- Seguir PEP 8
- Usar type hints para funciones publicas

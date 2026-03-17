# Instalacion

## Requisitos Previos

- Python 3.11+
- [uv](https://docs.astral.sh/uv/) (recomendado) o pip

## Opcion 1: Instalar con uv (Recomendado)

La forma mas facil de instalar CodexSpec es usando uv:

```bash
uv tool install codexspec
```

## Opcion 2: Instalar con pip

Alternativamente, puedes usar pip:

```bash
pip install codexspec
```

## Opcion 3: Uso Unico

Ejecuta directamente sin instalar:

```bash
# Crear un nuevo proyecto
uvx codexspec init my-project

# Inicializar en un proyecto existente
cd your-existing-project
uvx codexspec init . --ai claude
```

## Opcion 4: Instalar desde GitHub

Para obtener la ultima version de desarrollo:

```bash
# Usando uv
uv tool install git+https://github.com/Zts0hg/codexspec:git

# Usando pip
pip install git+https://github.com/Zts0hg/codexspec:git

# Rama o etiqueta especifica
uv tool install git+https://github.com/Zts0hg/codexspec:git@main
uv tool install git+https://github.com/Zts0hg/codexspec:git@v0.2.0
```

## Verificar Instalacion

```bash
codexspec --help
codexspec version
```

## Actualizar

```bash
# Usando uv
uv tool install codexspec --upgrade

# Usando pip
pip install --upgrade codexspec
```

## Proximos Pasos

[Inicio Rapido](quick-start.md)

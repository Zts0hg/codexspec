# Instalação

## Pré-requisitos

- Python 3.11+
- [uv](https://docs.astral.sh/uv/) (recomendado) ou pip

## Opção 1: Instalar com uv (Recomendado)

A maneira mais fácil de instalar o CodexSpec é usando uv:

```bash
uv tool install codexspec
```

## Opção 2: Instalar com pip

Alternativamente, você pode usar pip:

```bash
pip install codexspec
```

## Opção 3: Uso Único

Execute diretamente sem instalar:

```bash
# Criar um novo projeto
uvx codexspec init meu-projeto

# Inicializar em um projeto existente
cd seu-projeto-existente
uvx codexspec init . --ai claude
```

## Opção 4: Instalar do GitHub

Para a versão de desenvolvimento mais recente:

```bash
# Usando uv
uv tool install git+https://github.com/Zts0hg/codexspec:git

# Usando pip
pip install git+https://github.com/Zts0hg/codexspec:git

# Branch ou tag específica
uv tool install git+https://github.com/Zts0hg/codexspec:git@main
uv tool install git+https://github.com/Zts0hg/codexspec:git@v0.2.0
```

## Verificar Instalação

```bash
codexspec --help
codexspec version
```

## Atualizando

```bash
# Usando uv
uv tool install codexspec --upgrade

# Usando pip
pip install --upgrade codexspec
```

## Próximos Passos

[Início Rápido](quick-start.md)

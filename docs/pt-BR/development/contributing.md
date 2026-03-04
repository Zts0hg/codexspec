# Contribuindo

## Pré-requisitos

- Python 3.11+
- Gerenciador de pacotes uv
- Git

## Desenvolvimento Local

```bash
# Clonar o repositório
git clone https://github.com/Zts0hg/codexspec.git
cd codexspec

# Instalar dependências de desenvolvimento
uv sync --dev

# Executar localmente
uv run codexspec --help

# Executar testes
uv run pytest

# Verificar código com linter
uv run ruff check src/
```

## Documentação

```bash
# Instalar dependências de docs
uv sync --extra docs

# Visualizar documentação localmente
uv run mkdocs serve

# Construir documentação
uv run mkdocs build
```

## Build

```bash
uv build
```

## Processo de Pull Request

1. Faça fork do repositório
2. Crie uma branch de funcionalidade
3. Faça suas alterações
4. Execute testes e linting
5. Envie um pull request

## Estilo de Código

- Comprimento de linha: máximo 120 caracteres
- Siga PEP 8
- Use type hints para funções públicas

# Contribuindo

## Pré-requisitos

- Python 3.11+
- Gerenciador de pacotes uv
- Git

## Desenvolvimento local

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

## Documentação

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

## Processo de pull request

1. Faça um fork do repositório
2. Crie uma branch de funcionalidade
3. Faça suas alterações
4. Rode os testes e o lint
5. Envie um pull request

## Estilo de código

- Tamanho de linha: no máximo 120 caracteres
- Siga a PEP 8
- Use type hints em funções públicas

Leia [CLAUDE.md](https://github.com/Zts0hg/codexspec/blob/main/CLAUDE.md), [AGENTS.md](https://github.com/Zts0hg/codexspec/blob/main/AGENTS.md) e a
[Estrutura do repositório](https://github.com/Zts0hg/codexspec/blob/main/docs/internal/repository-layout.md) antes de alterar
modelos, empacotamento ou inicialização. As cópias distribuídas dos comandos e
das skills são artefatos de instalação gerados. Edite suas fontes oficiais e
regenere as cópias.

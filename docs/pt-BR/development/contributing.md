# Contribuindo

## Pré-requisitos

- Python 3.11+
- Gerenciador de pacotes uv
- Git

## Desenvolvimento local

```bash
# Clonar o repositório
git clone https://github.com/Zts0hg/codexspec.git
cd codexspec

# Instalar as dependências de desenvolvimento
uv sync --dev

# Executar localmente
uv run codexspec --help

# Rodar os testes
uv run pytest

# Lint do código
uv run ruff check src/
```

## Documentação

```bash
# Instalar as dependências de docs
uv sync --extra docs

# Pré-visualizar a documentação localmente
uv run mkdocs serve

# Construir a documentação
uv run mkdocs build
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

# Contribuer

## Prérequis

- Python 3.11+
- gestionnaire de paquets uv
- Git

## Développement local

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

## Documentation

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

## Processus de pull request

1. Forkez le dépôt
2. Créez une branche de fonctionnalité
3. Effectuez vos modifications
4. Lancez les tests et le linting
5. Soumettez une pull request

## Style de code

- Longueur de ligne : 120 caractères maximum
- Suivre PEP 8
- Utiliser des indications de type pour les fonctions publiques

Avant de modifier les modèles, le packaging ou l'initialisation, lisez
[CLAUDE.md](https://github.com/Zts0hg/codexspec/blob/main/CLAUDE.md), [AGENTS.md](https://github.com/Zts0hg/codexspec/blob/main/AGENTS.md) et
[Organisation du dépôt](https://github.com/Zts0hg/codexspec/blob/main/docs/internal/repository-layout.md). Les copies
distribuées des commandes et des compétences sont des artefacts d'installation
générés ; modifiez leurs sources faisant autorité, puis régénérez-les.

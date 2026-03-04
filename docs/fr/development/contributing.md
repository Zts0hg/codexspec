# Contribution

## Prerequis

- Python 3.11+
- Gestionnaire de paquets uv
- Git

## Developpement Local

```bash
# Cloner le depot
git clone https://github.com/Zts0hg/codexspec.git
cd codexspec

# Installer les dependances de developpement
uv sync --dev

# Executer localement
uv run codexspec --help

# Executer les tests
uv run pytest

# Linter le code
uv run ruff check src/
```

## Documentation

```bash
# Installer les dependances de documentation
uv sync --extra docs

# Previsualiser la documentation localement
uv run mkdocs serve

# Construire la documentation
uv run mkdocs build
```

## Construction

```bash
uv build
```

## Processus de Pull Request

1. Forker le depot
2. Creer une branche de fonctionnalite
3. Effectuer vos modifications
4. Executer les tests et le linting
5. Soumettre une pull request

## Style de Code

- Longueur de ligne : 120 caracteres maximum
- Suivre PEP 8
- Utiliser des indices de type pour les fonctions publiques

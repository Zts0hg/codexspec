# Contribuer

## Prérequis

- Python 3.11+
- gestionnaire de paquets uv
- Git

## Développement local

```bash
# Cloner le dépôt
git clone https://github.com/Zts0hg/codexspec.git
cd codexspec

# Installer les dépendances de développement
uv sync --dev

# Exécuter localement
uv run codexspec --help

# Lancer les tests
uv run pytest

# Linter le code
uv run ruff check src/
```

## Documentation

```bash
# Installer les dépendances de documentation
uv sync --extra docs

# Prévisualiser la documentation localement
uv run mkdocs serve

# Construire la documentation
uv run mkdocs build
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

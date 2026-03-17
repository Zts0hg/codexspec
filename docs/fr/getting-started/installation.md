# Installation

## Prerequis

- Python 3.11+
- [uv](https://docs.astral.sh/uv/) (recommande) ou pip

## Option 1 : Installer avec uv (Recommande)

La methode la plus simple pour installer CodexSpec est d'utiliser uv :

```bash
uv tool install codexspec
```

## Option 2 : Installer avec pip

Alternativement, vous pouvez utiliser pip :

```bash
pip install codexspec
```

## Option 3 : Utilisation Ponctuelle

Executer directement sans installation :

```bash
# Creer un nouveau projet
uvx codexspec init mon-projet

# Initialiser dans un projet existant
cd votre-projet-existant
uvx codexspec init . --ai claude
```

## Option 4 : Installer depuis GitHub

Pour la derniere version de developpement :

```bash
# Avec uv
uv tool install git+https://github.com/Zts0hg/codexspec:git

# Avec pip
pip install git+https://github.com/Zts0hg/codexspec:git

# Branche ou tag specifique
uv tool install git+https://github.com/Zts0hg/codexspec:git@main
uv tool install git+https://github.com/Zts0hg/codexspec:git@v0.2.0
```

## Verifier l'Installation

```bash
codexspec --help
codexspec version
```

## Mise a Jour

```bash
# Avec uv
uv tool install codexspec --upgrade

# Avec pip
pip install --upgrade codexspec
```

## Prochaines Etapes

[Demarrage Rapide](quick-start.md)

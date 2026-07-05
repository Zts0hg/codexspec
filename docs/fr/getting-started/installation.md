# Installation

## Prérequis

- Python 3.11+
- [uv](https://docs.astral.sh/uv/) (recommandé) ou pip

## Option 1 : installer avec uv (recommandé)

La façon la plus simple d'installer CodexSpec est d'utiliser uv :

```bash
uv tool install codexspec
```

## Option 2 : installer avec pip

Vous pouvez également utiliser pip :

```bash
pip install codexspec
```

## Option 3 : usage ponctuel

Lancez directement, sans installation préalable :

```bash
# Créer un nouveau projet
uvx codexspec init my-project

# Initialiser dans un projet existant pour Claude Code
cd your-existing-project
uvx codexspec init . --ai claude

# Initialiser pour Codex CLI
uvx codexspec init . --ai codex

# Initialiser pour Claude Code et Codex CLI à la fois (écrit à la fois .claude/ et .agents/)
uvx codexspec init . --ai both
```

## Option 4 : installer depuis GitHub

Pour la dernière version de développement :

```bash
# Avec uv
uv tool install git+https://github.com/Zts0hg/codexspec.git

# Avec pip
pip install git+https://github.com/Zts0hg/codexspec.git

# Branche ou tag spécifique
uv tool install git+https://github.com/Zts0hg/codexspec.git@main
uv tool install git+https://github.com/Zts0hg/codexspec.git@v0.5.6
```

## Option 5 : installation via le Plugin Marketplace (alternative)

CodexSpec est également disponible comme plugin Claude Code. Cette méthode est idéale si vous souhaitez utiliser les slash commands de CodexSpec directement dans Claude Code sans installer le CLI. Le CLI offre l'expérience Requirements-First SDD complète ; le plugin fournit le jeu de slash commands par-dessus Claude Code.

### Étapes d'installation

Dans Claude Code :

```bash
# Ajouter le marketplace
> /plugin marketplace add Zts0hg/codexspec

# Installer le plugin
> /plugin install codexspec@codexspec-market
```

### Configuration de la langue pour les utilisateurs du plugin

Après une installation via le Plugin Marketplace, configurez votre langue préférée avec la slash command `/codexspec:config` (la commande CLI `codexspec config` n'est pas disponible sans l'installation du CLI) :

```bash
# Lancer la configuration interactive
> /codexspec:config

# Ou afficher la configuration courante
> /codexspec:config --view
```

La commande `config` vous guide pour choisir la langue de sortie (des documents générés) et la langue des messages de commit, puis écrit `.codexspec/config.yml`. Le support multilingue utilise la même traduction dynamique par LLM que le CLI.

### Comparatif des méthodes d'installation

| Méthode | Idéale pour | Fonctionnalités |
|--------|-------------|-----------------|
| **Installation CLI** (`uv tool install` ou `pip install`) | Flux de développement complet | Commandes CLI (`init`, `check`, `config`, `version`) + slash commands |
| **Plugin Marketplace** | Démarrage rapide, projets existants | Slash commands uniquement (utilisez `/codexspec:config` pour la langue) |

**Note** : le plugin utilise le mode `strict: false` et réutilise le support multilingue existant via la traduction dynamique par LLM.

## Vérifier l'installation

```bash
codexspec --help
codexspec version
```

(Pour les installations via le Plugin Marketplace, vérifiez en exécutant n'importe quelle slash command telle que `/codexspec:config --view` dans Claude Code.)

## Mettre à jour

```bash
# Avec uv
uv tool install codexspec --upgrade

# Avec pip
pip install --upgrade codexspec
```

(Les installations via le Plugin Marketplace sont mises à jour par le gestionnaire de plugins de Claude Code.)

## Prochaines étapes

[Démarrage rapide](quick-start.md)

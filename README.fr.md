# CodexSpec

[English](README.md) | [中文](README.zh-CN.md) | [日本語](README.ja.md) | [Español](README.es.md) | [Português](README.pt-BR.md) | [한국어](README.ko.md) | [Deutsch](README.de.md) | **Français**

[![PyPI version](https://img.shields.io/pypi/v/codexspec.svg)](https://pypi.org/project/codexspec/)
[![Python](https://img.shields.io/pypi/pyversions/codexspec.svg)](https://pypi.org/project/codexspec/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**Une boîte à outils de Développement Piloté par les Spécifications (SDD) pour Claude Code**

CodexSpec est une boîte à outils qui vous aide à construire des logiciels de haute qualité en utilisant une approche structurée et pilotée par les spécifications. Elle redéfinit l'approche du développement traditionnel en transformant les spécifications en artefacts exécutables qui guident directement l'implémentation.

## Fonctionnalités

- **Flux de travail structuré**: Commandes claires pour chaque phase de développement
- **Intégration Claude Code**: Commandes slash natives pour Claude Code
- **Basé sur une constitution**: Les principes du projet guident toutes les décisions
- **Spécifications d'abord**: Définir le quoi et le pourquoi avant le comment
- **Piloté par les plans**: Les choix techniques viennent après les exigences
- **Orienté tâches**: Décomposer l'implémentation en tâches actionnables
- **Assurance qualité**: Commandes de révision, d'analyse et de checklists intégrées
- **Internationalisation (i18n)**: Support multilingue via traduction dynamique LLM
- **Multiplateforme**: Support pour les scripts Bash et PowerShell
- **Extensible**: Architecture de plugins pour les commandes personnalisées

## Installation

### Prérequis

- Python 3.11+
- [uv](https://docs.astral.sh/uv/) (recommandé) ou pip

### Option 1: Installer avec uv (Recommandé)

La façon la plus simple d'installer CodexSpec est d'utiliser uv :

```bash
uv tool install codexspec
```

### Option 2: Installer avec pip

Alternativement, vous pouvez utiliser pip :

```bash
pip install codexspec
```

### Option 3: Utilisation ponctuelle

Exécuter directement sans installation :

```bash
# Créer un nouveau projet
uvx codexspec init my-project

# Initialiser dans un projet existant
cd your-existing-project
uvx codexspec init . --ai claude
```

### Option 4: Installer depuis GitHub (Version de Développement)

Pour la dernière version de développement ou une branche spécifique :

```bash
# Avec uv
uv tool install git+https://github.com/Zts0hg/codexspec.git

# Avec pip
pip install git+https://github.com/Zts0hg/codexspec.git

# Branche ou tag spécifique
uv tool install git+https://github.com/Zts0hg/codexspec.git@main
uv tool install git+https://github.com/Zts0hg/codexspec.git@v0.2.0
```

## Démarrage Rapide

Après l'installation, vous pouvez utiliser la CLI :

```bash
# Créer un nouveau projet (sortie en français)
codexspec init my-project --lang fr

# Initialiser dans un projet existant
codexspec init . --ai claude

# Vérifier les outils installés
codexspec check

# Afficher la version
codexspec version
```

Mise à jour vers la dernière version :

```bash
# Avec uv
uv tool install codexspec --upgrade

# Avec pip
pip install --upgrade codexspec
```

## Utilisation

### 1. Initialiser un Projet

Après [l'installation](#installation), créez ou initialisez votre projet :

```bash
codexspec init my-awesome-project --lang fr
```

### 2. Établir les Principes du Projet

Lancez Claude Code dans le répertoire du projet :

```bash
cd my-awesome-project
claude
```

Utilisez la commande `/codexspec.constitution` pour créer les principes de gouvernance du projet :

```
/codexspec.constitution Créer des principes axés sur la qualité du code, les standards de test et l'architecture propre
```

### 3. Créer une Spécification

Utilisez `/codexspec.specify` pour définir ce que vous voulez construire :

```
/codexspec.specify Construire une application de gestion de tâches avec les fonctionnalités suivantes : créer des tâches, assigner à des utilisateurs, définir des dates d'échéance et suivre la progression
```

### 4. Clarifier les Exigences (Optionnel mais Recommandé)

Utilisez `/codexspec.clarify` pour résoudre les ambiguïtés avant la planification :

```
/codexspec.clarify
```

### 5. Créer un Plan Technique

Utilisez `/codexspec.spec-to-plan` pour définir comment l'implémenter :

```
/codexspec.spec-to-plan Utiliser Python avec FastAPI pour le backend, PostgreSQL pour la base de données et React pour le frontend
```

### 6. Générer les Tâches

Utilisez `/codexspec.plan-to-tasks` pour décomposer le plan :

```
/codexspec.plan-to-tasks
```

### 7. Analyser (Optionnel mais Recommandé)

Utilisez `/codexspec.analyze` pour la vérification de cohérence entre artefacts :

```
/codexspec.analyze
```

### 8. Implémenter

Utilisez `/codexspec.implement-tasks` pour exécuter l'implémentation :

```
/codexspec.implement-tasks
```

## Commandes Disponibles

### Commandes CLI

| Commande | Description |
|----------|-------------|
| `codexspec init` | Initialiser un nouveau projet CodexSpec |
| `codexspec check` | Vérifier les outils installés |
| `codexspec version` | Afficher les informations de version |
| `codexspec config` | Afficher ou modifier la configuration du projet |

### Options de `codexspec init`

| Option | Description |
|--------|-------------|
| `PROJECT_NAME` | Nom du nouveau répertoire de projet |
| `--here`, `-h` | Initialiser dans le répertoire actuel |
| `--ai`, `-a` | Assistant IA à utiliser (par défaut : claude) |
| `--lang`, `-l` | Langue de sortie (ex : en, fr, zh-CN, ja) |
| `--force`, `-f` | Forcer l'écrasement des fichiers existants |
| `--no-git` | Ignorer l'initialisation git |
| `--debug`, `-d` | Activer la sortie de débogage |

### Options de `codexspec config`

| Option | Description |
|--------|-------------|
| `--set-lang`, `-l` | Définir la langue de sortie |
| `--list-langs` | Lister toutes les langues supportées |

### Commandes Slash

Après l'initialisation, ces commandes slash sont disponibles dans Claude Code :

#### Commandes Principales

| Commande | Description |
|----------|-------------|
| `/codexspec.constitution` | Créer ou mettre à jour les principes de gouvernance du projet |
| `/codexspec.specify` | Définir ce que vous voulez construire (exigences) |
| `/codexspec.generate-spec` | Générer une spécification détaillée à partir des exigences |
| `/codexspec.spec-to-plan` | Convertir la spécification en plan technique |
| `/codexspec.plan-to-tasks` | Décomposer le plan en tâches actionnables |
| `/codexspec.implement-tasks` | Exécuter les tâches selon la décomposition |

#### Commandes de Révision

| Commande | Description |
|----------|-------------|
| `/codexspec.review-spec` | Réviser la complétude de la spécification |
| `/codexspec.review-plan` | Réviser la faisabilité du plan technique |
| `/codexspec.review-tasks` | Réviser la complétude de la décomposition des tâches |

#### Commandes Avancées

| Commande | Description |
|----------|-------------|
| `/codexspec.clarify` | Clarifier les zones sous-spécifiées avant la planification |
| `/codexspec.analyze` | Analyse de cohérence entre artefacts |
| `/codexspec.checklist` | Générer des checklists de qualité pour les exigences |
| `/codexspec.tasks-to-issues` | Convertir les tâches en GitHub issues |

## Aperçu du Flux de Travail

```
┌──────────────────────────────────────────────────────────────┐
│                    Flux de Travail CodexSpec                  │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  1. Constitution  ──►  Définir les principes du projet       │
│         │                                                    │
│         ▼                                                    │
│  2. Specify  ───────►  Créer la spécification de fonctionnalité │
│         │                                                    │
│         ▼                                                    │
│  3. Clarify  ───────►  Résoudre les ambiguïtés (optionnel)   │
│         │                                                    │
│         ▼                                                    │
│  4. Review Spec  ───►  Valider la spécification              │
│         │                                                    │
│         ▼                                                    │
│  5. Spec to Plan  ──►  Créer le plan technique               │
│         │                                                    │
│         ▼                                                    │
│  6. Review Plan  ───►  Valider le plan technique             │
│         │                                                    │
│         ▼                                                    │
│  7. Plan to Tasks  ─►  Générer la décomposition des tâches   │
│         │                                                    │
│         ▼                                                    │
│  8. Analyze  ───────►  Cohérence entre artefacts (optionnel) │
│         │                                                    │
│         ▼                                                    │
│  9. Review Tasks  ──►  Valider la décomposition des tâches   │
│         │                                                    │
│         ▼                                                    │
│  10. Implement  ─────►  Exécuter l'implémentation            │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

## Structure du Projet

Après l'initialisation, votre projet aura cette structure :

```
my-project/
├── .codexspec/
│   ├── memory/
│   │   └── constitution.md    # Principes de gouvernance du projet
│   ├── specs/
│   │   └── {feature-id}/
│   │       ├── spec.md        # Spécification de fonctionnalité
│   │       ├── plan.md        # Plan technique
│   │       ├── tasks.md       # Décomposition des tâches
│   │       └── checklists/    # Checklists de qualité
│   ├── templates/             # Modèles personnalisés
│   ├── scripts/               # Scripts d'aide
│   │   ├── bash/              # Scripts Bash
│   │   └── powershell/        # Scripts PowerShell
│   └── extensions/            # Extensions personnalisées
├── .claude/
│   └── commands/              # Commandes slash pour Claude Code
└── CLAUDE.md                  # Contexte pour Claude Code
```

## Internationalisation (i18n)

CodexSpec supporte plusieurs langues via la **traduction dynamique LLM**. Au lieu de maintenir des modèles traduits, nous laissons Claude traduire le contenu à l'exécution en fonction de votre configuration linguistique.

### Définir la Langue

**Pendant l'initialisation :**
```bash
# Créer un projet avec sortie en français
codexspec init my-project --lang fr

# Créer un projet avec sortie en japonais
codexspec init my-project --lang ja
```

**Après l'initialisation :**
```bash
# Afficher la configuration actuelle
codexspec config

# Modifier le paramètre de langue
codexspec config --set-lang fr

# Lister les langues supportées
codexspec config --list-langs
```

### Fichier de Configuration

Le fichier `.codexspec/config.yml` stocke les paramètres linguistiques :

```yaml
version: "1.0"

language:
  # Langue de sortie pour les interactions Claude et les documents générés
  output: "fr"

  # Langue des modèles - garder "en" pour la compatibilité
  templates: "en"

project:
  ai: "claude"
  created: "2026-02-15"
```

### Langues Supportées

| Code | Langue |
|------|--------|
| `en` | English (par défaut) |
| `zh-CN` | 中文（简体） |
| `zh-TW` | 中文（繁體） |
| `ja` | 日本語 |
| `ko` | 한국어 |
| `es` | Español |
| `fr` | Français |
| `de` | Deutsch |
| `pt` | Português |
| `ru` | Русский |
| `it` | Italiano |
| `ar` | العربية |
| `hi` | हिन्दी |

### Comment ça Fonctionne

1. **Modèles en anglais uniquement** : Tous les modèles de commandes restent en anglais
2. **Configuration linguistique** : Le projet spécifie la langue de sortie préférée
3. **Traduction dynamique** : Claude lit les instructions en anglais, produit le contenu dans la langue cible
4. **Sensibilisé au contexte** : Les termes techniques (JWT, OAuth, etc.) restent en anglais quand approprié

### Avantages

- **Zéro maintenance de traduction** : Pas besoin de maintenir plusieurs versions de modèles
- **Toujours à jour** : Les mises à jour des modèles bénéficient automatiquement à toutes les langues
- **Traduction sensibilisée au contexte** : Claude fournit des traductions naturelles et appropriées au contexte
- **Langues illimitées** : Toute langue supportée par Claude fonctionne immédiatement

## Système d'Extensions

CodexSpec supporte une architecture de plugins pour ajouter des commandes personnalisées :

### Structure d'une Extension

```
my-extension/
├── extension.yml          # Manifeste de l'extension
├── commands/              # Commandes slash personnalisées
│   └── command.md
└── README.md
```

### Créer des Extensions

1. Copier le modèle depuis `extensions/template/`
2. Modifier `extension.yml` avec les détails de votre extension
3. Ajouter vos commandes personnalisées dans `commands/`
4. Tester localement et publier

Voir `extensions/EXTENSION-DEVELOPMENT-GUIDE.md` pour plus de détails.

## Développement

### Prérequis

- Python 3.11+
- Gestionnaire de paquets uv
- Git

### Développement Local

```bash
# Cloner le dépôt
git clone https://github.com/Zts0hg/codexspec.git
cd codexspec

# Installer les dépendances de développement
uv sync --dev

# Exécuter localement
uv run codexspec --help

# Exécuter les tests
uv run pytest

# Linter le code
uv run ruff check src/
```

### Construction

```bash
# Construire le paquet
uv build
```

## Comparaison avec spec-kit

CodexSpec est inspiré par le spec-kit de GitHub mais avec quelques différences clés :

| Fonctionnalité | spec-kit | CodexSpec |
|----------------|----------|-----------|
| Philosophie Centrale | Développement piloté par les specs | Développement piloté par les specs |
| Nom CLI | `specify` | `codexspec` |
| IA Principale | Support multi-agents | Focus sur Claude Code |
| Préfixe de Commande | `/speckit.*` | `/codexspec.*` |
| Flux de Travail | specify → plan → tasks → implement | constitution → specify → clarify → plan → tasks → analyze → implement |
| Étapes de Révision | Optionnelles | Commandes de révision intégrées |
| Commande Clarify | Oui | Oui |
| Commande Analyze | Oui | Oui |
| Commande Checklist | Oui | Oui |
| Système d'Extensions | Oui | Oui |
| Scripts PowerShell | Oui | Oui |
| Support i18n | Non | Oui (13+ langues via traduction LLM) |

## Philosophie

CodexSpec suit ces principes fondamentaux :

1. **Développement piloté par les intentions**: Les spécifications définissent le "quoi" avant le "comment"
2. **Création de spécifications riches**: Utiliser des garde-fous et des principes organisationnels
3. **Raffinement en plusieurs étapes**: Plutôt que de la génération de code en une seule fois
4. **Forte dépendance à l'IA**: Tirer parti de l'IA pour l'interprétation des spécifications
5. **Orienté révision**: Valider chaque artefact avant de progresser
6. **Qualité d'abord**: Checklists et analyses intégrées pour la qualité des exigences

## Contribuer

Les contributions sont les bienvenues ! Veuillez lire nos directives de contribution avant de soumettre une pull request.

## Licence

Licence MIT - voir [LICENSE](LICENSE) pour plus de détails.

## Remerciements

- Inspiré par [GitHub spec-kit](https://github.com/github/spec-kit)
- Construit pour [Claude Code](https://claude.ai/code)

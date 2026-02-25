# CodexSpec

[English](README.md) | [中文](README.zh-CN.md) | [日本語](README.ja.md) | [Español](README.es.md) | [Português](README.pt-BR.md) | [한국어](README.ko.md) | [Deutsch](README.de.md) | **Français**

[![PyPI version](https://img.shields.io/pypi/v/codexspec.svg)](https://pypi.org/project/codexspec/)
[![Python](https://img.shields.io/pypi/pyversions/codexspec.svg)](https://pypi.org/project/codexspec/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**[📖 Documentation](https://zts0hg.github.io/codexspec/)**

**Une boîte à outils de Développement Piloté par les Spécifications (SDD) pour Claude Code**

CodexSpec est une boîte à outils qui vous aide à construire des logiciels de haute qualité en utilisant une approche structurée et pilotée par les spécifications. Elle redéfinit l'approche du développement traditionnel en transformant les spécifications en artefacts exécutables qui guident directement l'implémentation.

## Philosophie de Conception : Collaboration Humain-AI

CodexSpec est construit sur la conviction que **le développement efficace assisté par l'IA nécessite une participation humaine active à chaque étape**. La boîte à outils est conçue autour d'un principe fondamental :

> **Réviser et valider chaque artefact avant de progresser.**

### Pourquoi la Supervision Humaine est Importante

Dans le développement assisté par l'IA, sauter les étapes de révision entraîne :

| Problème | Conséquence |
|----------|-------------|
| Exigences floues | L'IA fait des suppositions qui divergent de votre intention |
| Spécifications incomplètes | Des fonctionnalités sont construites sans cas limites critiques |
| Plans techniques désalignés | L'architecture ne correspond pas aux besoins métier |
| Décomposition de tâches vague | L'implémentation dérive, nécessitant un retravail coûteux |

### L'Approche CodexSpec

CodexSpec structure le développement en **points de contrôle révisables** :

```
Idée → Clarifier → Réviser → Planifier → Réviser → Tâches → Réviser → Analyser → Implémenter
               ↑                 ↑                 ↑
            Vérification      Vérification      Vérification
              humaine           humaine           humaine
```

**Chaque artefact a une commande de révision correspondante :**
- `spec.md` → `/codexspec.review-spec`
- `plan.md` → `/codexspec.review-plan`
- `tasks.md` → `/codexspec.review-tasks`
- Tous les artefacts → `/codexspec.analyze`

Ce processus de révision systématique assure :
- **Détection précoce des erreurs** : Repérer les malentendus avant que le code ne soit écrit
- **Vérification de l'alignement** : Confirmer que l'interprétation de l'IA correspond à votre intention
- **Portes de qualité** : Valider la complétude, la clarté et la faisabilité à chaque étape
- **Réduction du retravail** : Investir des minutes en révision pour économiser des heures de réimplémentation

## Fonctionnalités

### Workflow SDD Central
- **Basé sur une Constitution** : Établir les principes du projet qui guident toutes les décisions ultérieures
- **Spécification en Deux Phases** : Clarification interactive (`/specify`) suivie de la génération de document (`/generate-spec`)
- **Développement Piloté par les Plans** : Les choix techniques viennent après la validation des exigences
- **Tâches Prêtes pour le TDD** : Les décompositions de tâches appliquent la méthodologie test-first

### Collaboration Humain-AI
- **Commandes de Révision** : Commandes de révision dédiées pour spec, plan et tasks pour valider la sortie de l'IA
- **Clarification Interactive** : Raffinement des exigences par Q&A avec retour immédiat
- **Analyse Inter-Artefacts** : Détecter les incohérences entre spec, plan et tasks avant l'implémentation
- **Checklists de Qualité** : Évaluation automatisée de la qualité des exigences

### Expérience Développeur
- **Intégration Claude Code** : Commandes slash natives pour Claude Code
- **Internationalisation (i18n)** : Support multilingue via traduction dynamique LLM
- **Multiplateforme** : Support pour les scripts Bash et PowerShell
- **Extensible** : Architecture de plugins pour les commandes personnalisées

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
# Créer un nouveau projet
codexspec init my-project

# Créer un projet avec sortie en français
codexspec init my-project --lang fr

# Initialiser dans un projet existant
codexspec init . --ai claude
# ou
codexspec init --here --ai claude

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
codexspec init my-awesome-project
# ou dans le répertoire actuel
codexspec init . --ai claude
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

### 3. Clarifier les Exigences

Utilisez `/codexspec.specify` pour **explorer et clarifier** vos exigences via un Q&A interactif :

```
/codexspec.specify Je veux construire une application de gestion de tâches
```

Cette commande va :
- Poser des questions de clarification pour comprendre votre idée
- Explorer les cas limites que vous n'avez peut-être pas envisagés
- Co-créer des exigences de haute qualité par le dialogue
- **NE PAS** générer de fichiers automatiquement - vous gardez le contrôle

### 4. Générer le Document de Spécification

Une fois les exigences clarifiées, utilisez `/codexspec.generate-spec` pour créer le document `spec.md` :

```
/codexspec.generate-spec
```

Cette commande agit comme un "compilateur d'exigences" qui transforme vos exigences clarifiées en un document de spécification structuré.

### 5. Réviser la Spécification (Recommandé)

**Avant de passer à la planification, validez votre spécification :**

```
/codexspec.review-spec
```

Cette commande génère un rapport de révision détaillé avec :
- Analyse de complétude des sections
- Évaluation de la clarté et de la testabilité
- Vérification de l'alignement avec la constitution
- Recommandations priorisées

### 6. Créer un Plan Technique

Utilisez `/codexspec.spec-to-plan` pour définir comment l'implémenter :

```
/codexspec.spec-to-plan Utiliser Python avec FastAPI pour le backend, PostgreSQL pour la base de données et React pour le frontend
```

La commande inclut une **révision de constitutionnalité** - vérifiant que votre plan s'aligne avec les principes du projet.

### 7. Réviser le Plan (Recommandé)

**Avant de décomposer en tâches, validez votre plan technique :**

```
/codexspec.review-plan
```

Cela vérifie :
- L'alignement avec la spécification
- La solidité de l'architecture
- La pertinence de la stack technique
- La conformité à la constitution

### 8. Générer les Tâches

Utilisez `/codexspec.plan-to-tasks` pour décomposer le plan :

```
/codexspec.plan-to-tasks
```

Les tâches sont organisées en phases standard avec :
- **Application du TDD** : Les tâches de test précèdent les tâches d'implémentation
- **Marqueurs parallèles `[P]`** : Identifier les tâches indépendantes
- **Spécifications de chemins de fichiers** : Livrables clairs par tâche

### 9. Réviser les Tâches (Recommandé)

**Avant l'implémentation, validez la décomposition des tâches :**

```
/codexspec.review-tasks
```

Cela vérifie :
- La couverture du plan
- La conformité au TDD
- L'exactitude des dépendances
- La granularité des tâches

### 10. Analyser (Optionnel mais Recommandé)

Utilisez `/codexspec.analyze` pour la vérification de cohérence inter-artefacts :

```
/codexspec.analyze
```

Cela détecte les problèmes entre spec, plan et tasks :
- Lacunes de couverture (exigences sans tâches)
- Duplications et incohérences
- Violations de la constitution
- Éléments sous-spécifiés

### 11. Implémenter

Utilisez `/codexspec.implement-tasks` pour exécuter l'implémentation :

```
/codexspec.implement-tasks
```

L'implémentation suit le **workflow TDD conditionnel** :
- Tâches de code : Test-first (Red → Green → Verify → Refactor)
- Tâches non-testables (docs, config) : Implémentation directe

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
| `--set-commit-lang`, `-c` | Définir la langue des messages de commit (par défaut : langue de sortie) |
| `--list-langs` | Lister toutes les langues supportées |

### Commandes Slash

Après l'initialisation, ces commandes slash sont disponibles dans Claude Code :

#### Commandes de Workflow Central

| Commande | Description |
|----------|-------------|
| `/codexspec.constitution` | Créer ou mettre à jour la constitution du projet avec validation inter-artefacts et rapport d'impact de synchronisation |
| `/codexspec.specify` | **Clarifier** les exigences via Q&A interactif (pas de génération de fichier) |
| `/codexspec.generate-spec` | **Générer** le document `spec.md` après clarification des exigences |
| `/codexspec.spec-to-plan` | Convertir la spécification en plan technique avec révision de constitutionnalité et graphe de dépendance des modules |
| `/codexspec.plan-to-tasks` | Décomposer le plan en tâches atomiques avec application du TDD et marqueurs parallèles `[P]` |
| `/codexspec.implement-tasks` | Exécuter les tâches avec workflow TDD conditionnel (TDD pour le code, direct pour docs/config) |

#### Commandes de Révision (Portes de Qualité)

| Commande | Description |
|----------|-------------|
| `/codexspec.review-spec` | Valider la spécification pour complétude, clarté, cohérence et testabilité avec scoring |
| `/codexspec.review-plan` | Réviser le plan technique pour faisabilité, qualité d'architecture et alignement avec la constitution |
| `/codexspec.review-tasks` | Valider la décomposition des tâches pour couverture du plan, conformité TDD, dépendances et granularité |

#### Commandes Avancées

| Commande | Description |
|----------|-------------|
| `/codexspec.clarify` | Scanner spec.md existant pour ambiguïtés en utilisant 4 catégories ciblées, intégration avec les résultats de révision |
| `/codexspec.analyze` | Analyse inter-artefacts non-destructive (spec, plan, tasks) avec détection de problèmes basée sur la sévérité |
| `/codexspec.checklist` | Générer des checklists de qualité pour la validation des exigences |
| `/codexspec.tasks-to-issues` | Convertir les tâches en GitHub issues pour l'intégration de gestion de projet |

#### Commandes de Flux de Travail Git

| Commande | Description |
|----------|-------------|
| `/codexspec.commit` | Générer des messages Conventional Commits basés sur l'état git et le contexte de session |
| `/codexspec.commit-staged` | Générer un message de commit uniquement à partir des changements indexés |

## Aperçu du Flux de Travail

```
┌──────────────────────────────────────────────────────────────────────────┐
│                    Flux de Travail Collaboration Humain-AI CodexSpec     │
├──────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  1. Constitution  ──►  Définir les principes du projet                   │
│         │                         avec validation inter-artefacts        │
│         ▼                                                                │
│  2. Specify  ───────►  Q&A interactif pour clarifier les exigences       │
│         │               (pas de fichier créé - contrôle humain)           │
│         ▼                                                                │
│  3. Generate Spec  ─►  Créer le document spec.md                         │
│         │                                                                │
│         ▼                                                                │
│  ╔═══════════════════════════════════════════════════════════════════╗   │
│  ║  ★ PORTE DE RÉVISION 1: /codexspec.review-spec ★                  ║   │
│  ║  Valider: Complétude, Clarté, Testabilité, Constitution           ║   │
│  ╚═══════════════════════════════════════════════════════════════════╝   │
│         │                                                                │
│         ▼                                                                │
│  4. Clarify  ───────►  Résoudre les ambiguïtés (itératif)                │
│         │               4 catégories ciblées, max 5 questions            │
│         ▼                                                                │
│  5. Spec to Plan  ──►  Créer le plan technique avec :                    │
│         │               • Révision de constitutionnalité (OBLIGATOIRE)   │
│         │               • Graphe de dépendance des modules               │
│         ▼                                                                │
│  ╔═══════════════════════════════════════════════════════════════════╗   │
│  ║  ★ PORTE DE RÉVISION 2: /codexspec.review-plan ★                  ║   │
│  ║  Valider: Alignement Spec, Architecture, Stack Tech, Phases       ║   │
│  ╚═══════════════════════════════════════════════════════════════════╝   │
│         │                                                                │
│         ▼                                                                │
│  6. Plan to Tasks  ─►  Générer des tâches atomiques avec :               │
│         │               • Application du TDD (tests avant impl)          │
│         │               • Marqueurs parallèles [P]                       │
│         │               • Spécifications de chemins de fichiers          │
│         ▼                                                                │
│  ╔═══════════════════════════════════════════════════════════════════╗   │
│  ║  ★ PORTE DE RÉVISION 3: /codexspec.review-tasks ★                 ║   │
│  ║  Valider: Couverture, Conformité TDD, Dépendances, Granularité    ║   │
│  ╚═══════════════════════════════════════════════════════════════════╝   │
│         │                                                                │
│         ▼                                                                │
│  7. Analyze  ───────►  Vérification de cohérence inter-artefacts         │
│         │               Détecter lacunes, duplications, problèmes const.  │
│         ▼                                                                │
│  8. Implement  ─────►  Exécuter avec workflow TDD conditionnel           │
│                          Code: Test-first | Docs/Config: Direct          │
│                                                                          │
└──────────────────────────────────────────────────────────────────────────┘
```

**Point Clé** : Chaque porte de révision (★) est un **point de contrôle humain** où vous validez la sortie de l'IA avant d'investir plus de temps. Sauter ces portes mène souvent à un retravail coûteux.

### Concept Clé: Workflow de Clarification des Exigences

CodexSpec fournit **deux commandes de clarification distinctes** pour différentes étapes du workflow :

#### specify vs clarify : Quand utiliser lequel ?

| Aspect | `/codexspec.specify` | `/codexspec.clarify` |
|--------|----------------------|----------------------|
| **Objectif** | Exploration initiale des exigences | Raffinement itératif des specs existantes |
| **Quand utiliser** | Démarrer avec une nouvelle idée, pas de spec.md | spec.md existe, besoin de combler les lacunes |
| **Entrée** | Votre idée ou exigence initiale | Fichier spec.md existant |
| **Sortie** | Aucune (dialogue uniquement) | Met à jour spec.md avec les clarifications |
| **Méthode** | Q&A ouvert | Scan d'ambiguïté structuré (4 catégories) |
| **Limite de questions** | Illimitée | Maximum 5 questions |
| **Usage typique** | "Je veux construire une app todo" | "La spec manque de détails sur la gestion d'erreurs" |

#### Spécification en Deux Phases

Avant de générer toute documentation :

| Phase | Commande | Objectif | Sortie |
|-------|----------|----------|--------|
| **Exploration** | `/codexspec.specify` | Q&A interactif pour explorer et affiner les exigences | Aucune (dialogue uniquement) |
| **Génération** | `/codexspec.generate-spec` | Compiler les exigences clarifiées en document structuré | `spec.md` |

#### Clarification Itérative

Après la création de spec.md :

```
spec.md ──► /codexspec.clarify ──► spec.md mis à jour (avec section Clarifications)
                │
                └── Scan les ambiguïtés dans 4 catégories ciblées :
                    • Lacunes de Complétude - Sections manquantes, contenu vide
                    • Problèmes de Spécificité - Termes vagues, contraintes non définies
                    • Clarté Comportementale - Gestion d'erreurs, transitions d'état
                    • Problèmes de Mesurabilité - Exigences non-fonctionnelles sans métriques
```

#### Avantages de ce Design

- **Collaboration humain-AI** : Vous participez activement à la découverte des exigences
- **Contrôle explicite** : Les fichiers ne sont créés que lorsque vous décidez
- **Focus qualité** : Les exigences sont pleinement explorées avant documentation
- **Raffinement itératif** : Les specs peuvent être améliorées incrémentalement

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
# Créer un projet avec sortie en chinois
codexspec init my-project --lang zh-CN

# Créer un projet avec sortie en japonais
codexspec init my-project --lang ja
```

**Après l'initialisation :**
```bash
# Afficher la configuration actuelle
codexspec config

# Modifier le paramètre de langue
codexspec config --set-lang zh-CN

# Lister les langues supportées
codexspec config --list-langs
```

### Langue des Messages de Commit

Vous pouvez configurer une langue différente pour les messages de commit que la langue de sortie :

```bash
# Utiliser le français pour les interactions mais l'anglais pour les commits
codexspec config --set-lang fr
codexspec config --set-commit-lang en
```

**Priorité de langue pour les messages de commit :**
1. Paramètre `language.commit` (si spécifié)
2. `language.output` (alternative)
3. `"en"` (par défaut)

**Note :** Le type de commit (feat, fix, docs, etc.) et la portée restent toujours en anglais. Seule la partie description utilise la langue configurée.

### Fichier de Configuration

Le fichier `.codexspec/config.yml` stocke les paramètres linguistiques :

```yaml
version: "1.0"

language:
  # Langue de sortie pour les interactions Claude et les documents générés
  output: "zh-CN"

  # Langue des messages de commit (par défaut : langue de sortie)
  # Définir comme "en" pour des messages de commit en anglais quelle que soit la langue de sortie
  commit: "zh-CN"

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

### Constitution et Documents Générés

Lorsque vous utilisez `/codexspec.constitution` pour créer la constitution de votre projet, elle sera générée dans la langue spécifiée dans votre configuration :

- **Approche Fichier Unique** : La constitution est générée dans une seule langue
- **Claude Comprend Toutes les Langues** : Claude peut travailler avec des fichiers de constitution dans n'importe quelle langue supportée
- **Collaboration d'Équipe** : Les équipes doivent utiliser une langue de travail cohérente

Cette conception évite les problèmes de synchronisation entre plusieurs versions linguistiques et réduit la charge de maintenance.

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
| Philosophie Centrale | Développement piloté par les specs | Développement piloté par les specs + collaboration humain-AI |
| Nom CLI | `specify` | `codexspec` |
| IA Principale | Support multi-agents | Focus sur Claude Code |
| Préfixe de Commande | `/speckit.*` | `/codexspec.*` |
| Système de Constitution | Basique | Constitution complète avec validation inter-artefacts |
| Spec en Deux Phases | Non | Oui (clarification + génération) |
| Commandes de Révision | Optionnelles | 3 commandes de révision dédiées avec scoring |
| Commande Clarify | Oui | 4 catégories ciblées, intégration avec révision |
| Commande Analyze | Oui | Lecture seule, basée sur la sévérité, sensibilisée à la constitution |
| TDD dans les Tâches | Optionnel | Appliqué (tests précèdent l'implémentation) |
| Implémentation | Standard | TDD conditionnel (code vs docs/config) |
| Système d'Extensions | Oui | Oui |
| Scripts PowerShell | Oui | Oui |
| Support i18n | Non | Oui (13+ langues via traduction LLM) |

### Différenciateurs Clés

1. **Culture Révision d'Abord** : Chaque artefact majeur a une commande de révision dédiée
2. **Gouvernance par Constitution** : Les principes sont validés, pas seulement documentés
3. **TDD par Défaut** : Méthodologie test-first appliquée dans la génération de tâches
4. **Points de Contrôle Humains** : Workflow conçu autour des portes de validation

## Philosophie

CodexSpec suit ces principes fondamentaux :

### Fondamentaux SDD

1. **Développement piloté par les intentions** : Les spécifications définissent le "quoi" avant le "comment"
2. **Création de spécifications riches** : Utiliser des garde-fous et des principes organisationnels
3. **Raffinement en plusieurs étapes** : Plutôt que de la génération de code en une seule fois
4. **Gouvernance par constitution** : Les principes du projet guident toutes les décisions

### Collaboration Humain-AI

5. **Humain-dans-la-boucle** : L'IA génère les artefacts, les humains les valident
6. **Orienté révision** : Valider chaque artefact avant de progresser
7. **Divulgation progressive** : L'information complexe révélée incrémentalement
8. **Explicite plutôt qu'implicite** : Les exigences doivent être claires, pas supposées

### Assurance Qualité

9. **Test-driven par défaut** : Workflow TDD intégré dans la génération de tâches
10. **Cohérence inter-artefacts** : Analyser spec, plan et tasks ensemble
11. **Alignement avec la constitution** : Tous les artefacts respectent les principes du projet

### Pourquoi la Révision est Importante

| Sans Révision | Avec Révision |
|---------------|---------------|
| L'IA fait des suppositions incorrectes | L'humain repère les mauvaises interprétations tôt |
| Les exigences incomplètes se propagent | Les lacunes identifiées avant implémentation |
| L'architecture dérive de l'intention | Alignement vérifié à chaque étape |
| Les tâches manquent des fonctionnalités critiques | Couverture validée systématiquement |
| **Résultat : Retravail, effort gaspillé** | **Résultat : Correct du premier coup** |

## Contribuer

Les contributions sont les bienvenues ! Veuillez lire nos directives de contribution avant de soumettre une pull request.

## Licence

Licence MIT - voir [LICENSE](LICENSE) pour plus de détails.

## Remerciements

- Inspiré par [GitHub spec-kit](https://github.com/github/spec-kit)
- Construit pour [Claude Code](https://claude.ai/code)

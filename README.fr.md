<div align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="codexspec-logo-dark.svg">
    <source media="(prefers-color-scheme: light)" srcset="codexspec-logo-light.svg">
    <img alt="CodexSpec Logo" src="codexspec-logo-light.svg" width="420">
  </picture>
</div>

<h1 align="center">CodexSpec</h1>

<p align="center">
  <a href="README.md">English</a> | <a href="README.zh-CN.md">中文</a> | <a href="README.ja.md">日本語</a> | <a href="README.es.md">Español</a> | <a href="README.pt-BR.md">Português</a> | <a href="README.ko.md">한국어</a> | <a href="README.de.md">Deutsch</a> | <b>Français</b>
</p>

<p align="center">
  <a href="https://pypi.org/project/codexspec/"><img src="https://img.shields.io/pypi/v/codexspec.svg?style=for-the-badge" alt="PyPI version"></a>
  <a href="https://pypi.org/project/codexspec/"><img src="https://img.shields.io/pypi/pyversions/codexspec.svg?style=for-the-badge" alt="Python versions"></a>
  <a href="https://opensource.org/licenses/MIT"><img src="https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge" alt="License: MIT"></a>
</p>

<p align="center">
  <strong>Des outils SDD avec priorité aux exigences pour Claude Code et OpenAI Codex</strong>
</p>

CodexSpec transforme les exigences confirmées en spécifications, documents de conception,
plans, tâches et implémentations dont la traçabilité est assurée. Vous décidez
**quoi** construire et **pourquoi** ; l'agent définit **comment** le réaliser
en respectant les exigences que vous avez confirmées. Il s'appuie sur des
étapes de revue et sur les connaissances du projet conservées entre les sessions.

Vous pouvez utiliser les commandes à barre oblique de Claude Code, les
compétences de Codex ou les deux intégrations. Par défaut, les fonctionnalités
du flux standard sont développées dans des worktrees Git distincts. Un blueprint
partagé facultatif permet aussi à l'agent de développer de façon autonome une
file d'exigences confirmées.

[📖 Documentation](https://zts0hg.github.io/codexspec/) | [中文文档](https://zts0hg.github.io/codexspec/zh/) | [日本語ドキュメント](https://zts0hg.github.io/codexspec/ja/) | [한국어 문서](https://zts0hg.github.io/codexspec/ko/) | [Documentación](https://zts0hg.github.io/codexspec/es/) | [Documentation](https://zts0hg.github.io/codexspec/fr/) | [Dokumentation](https://zts0hg.github.io/codexspec/de/) | [Documentação](https://zts0hg.github.io/codexspec/pt-BR/)

## Table des matières

- [Pourquoi choisir CodexSpec ?](#pourquoi-choisir-codexspec-)
- [Démarrage rapide en 30 secondes](#démarrage-rapide-en-30-secondes)
- [Installation](#installation)
- [Flux de travail principal](#flux-de-travail-principal)
- [Blueprint partagé et développement autonome](#blueprint-partagé-et-développement-autonome)
- [Développement avec les worktrees](#développement-avec-les-worktrees)
- [Travailler avec du code existant](#travailler-avec-du-code-existant)
- [Revue et débogage](#revue-et-débogage)
- [Connaissances du projet](#connaissances-du-projet)
- [Flux de travail Git](#flux-de-travail-git)
- [Commandes disponibles](#commandes-disponibles)
- [Configuration et internationalisation](#configuration-et-internationalisation)
- [Structure du projet](#structure-du-projet)
- [Ressources pour les extensions](#ressources-pour-les-extensions)
- [Développement](#développement)
- [Contribuer](#contribuer)
- [Licence](#licence)

## Pourquoi choisir CodexSpec ?

| Besoin | Ce qu'apporte CodexSpec |
|------|-------------------------|
| Définir clairement l'intention du produit | Confirmation explicite et consignation durable dans `requirements.md` avant la spécification |
| Assurer la traçabilité du développement | Références aux sources tout au long de la chaîne : exigences → spécification → conception → plan → tâches |
| Pouvoir examiner les décisions | Quatre commandes de revue des artefacts, une analyse entre artefacts et un contrôle de défauts distinct pour le code |
| Assurer la continuité entre sessions et équipes | Dossiers de fonctionnalités, principes du projet, connaissances réutilisables et décisions historiques pertinentes |
| Développer plusieurs fonctionnalités en parallèle | Un worktree Git par fonctionnalité du flux standard, avec réutilisation du même espace de travail |
| Automatiser davantage | Passage facultatif à l'étape suivante et développement autonome des exigences confirmées du blueprint |
| Respecter les langues de travail de l'équipe | Langues indépendantes pour les échanges, les documents et les commits |

### Que signifie SDD avec priorité aux exigences ?

Dans le développement piloté par les spécifications avec priorité aux exigences,
**les exigences confirmées priment sur toute autre référence pour la fonctionnalité**.
Avant d'élaborer les artefacts d'implémentation, l'agent consigne les objectifs,
les contraintes, les décisions, les exclusions, les questions en suspens et les
éléments attestant la confirmation des exigences.

```text
Idea → Confirmed Requirements → Spec → Design → Plan → Tasks → Code
```

L'intention du produit se définit et évolue grâce à la collaboration humaine.
Les revues automatiques vérifient que les artefacts dérivés respectent cette
intention. Lorsque l'automatisation est activée, le travail avance à mesure que
les étapes sont validées ; l'agent ne peut pas remplacer les exigences
confirmées sans le signaler.

## Démarrage rapide en 30 secondes

Installez CodexSpec et initialisez le projet pour l'assistant que vous utilisez :

```bash
uv tool install codexspec

# Create a new project for Claude Code
codexspec init my-project --ai claude

# Or initialize an existing project for Codex
cd your-existing-project
codexspec init . --ai codex

# Use --ai both when you want both integrations
```

Lancez l'assistant installé dans le projet que vous venez d'initialiser. Le
flux de travail est le même ; seule la forme des commandes change :

| Assistant | Commencer à définir les exigences |
|-----------|------------------------------|
| Claude Code (`claude`) | `/codexspec:specify I want to build a todo application` |
| Codex (`codex`) | `$codexspec:specify I want to build a todo application` |

Si nécessaire, adaptez les principes du projet avec `constitution`. Confirmez
le résumé final des exigences, puis poursuivez dans le dossier de la
fonctionnalité et l'espace de travail indiqués par la commande. Les étapes
suivantes sont décrites dans [Flux de travail principal](#flux-de-travail-principal).

Vous utilisez l'application de bureau Codex ? [Demandez à Codex d'installer et d'initialiser votre projet](#installer-depuis-lapplication-de-bureau-codex).

## Installation

### Installer depuis l'application de bureau Codex

Depuis l'application de bureau, vous pouvez demander à Codex d'installer CodexSpec et de configurer directement votre projet.

1. Ajoutez un projet local dans l'application de bureau Codex et sélectionnez le dossier dans lequel vous souhaitez travailler.
2. Ouvrez une conversation dans ce projet et collez l'instruction ci-dessous.
3. Si l'application vous demande l'autorisation de télécharger ou d'installer des dépendances, approuvez l'action demandée pour continuer.

```text
Please install and initialize CodexSpec in the current project.
Project: https://github.com/Zts0hg/codexspec

Complete the setup directly instead of asking me to run terminal commands.

Check the environment. If uv or Python 3.11+ is missing, install the required
tools in my user directory using their official installation instructions.
Install the latest stable release of CodexSpec.

For a new setup, initialize the current project for Codex in English:
codexspec init . --ai codex --lang en

If CodexSpec is already configured, check its version and configuration before
updating. Preserve existing requirements, project principles, user files,
and configuration settings.

Verify that the CLI works and that AGENTS.md and the CodexSpec skill files
under .agents/skills/ are installed. Explain the result and how to start
describing my requirements in plain English. If the skills are not yet
available in this chat, tell me whether to start a new chat or restart the app.
```

Pour recevoir les réponses et les documents en chinois, remplacez `--lang en` par `--lang zh-CN` et demandez à Codex d'expliquer le résultat en chinois.

Codex installe la même CLI et les mêmes compétences de projet que celles obtenues par la configuration manuelle décrite ci-dessous. Vous pouvez commencer avec une instruction telle que `$codexspec:specify I want to build a todo application`. Le [guide des compétences d'OpenAI](https://learn.chatgpt.com/docs/build-skills) explique comment les compétences locales sont détectées et actualisées.

### Prérequis

- Python 3.11+
- [uv](https://docs.astral.sh/uv/) (recommandé) ou pip
- L'assistant que vous souhaitez utiliser : Claude Code ou Codex
- Git pour le développement avec les worktrees et les flux de travail Git

### Installation de la CLI

```bash
uv tool install codexspec

# Or use pip
pip install codexspec

# Verify the CLI and inspect available commands
codexspec version
codexspec --help
codexspec list-commands
```

Pour créer un projet, exécutez `codexspec init my-project --ai claude` ; pour
initialiser le dossier courant, exécutez `codexspec init . --ai codex`.
`--ai both` installe les deux intégrations. L'assistant par défaut est `claude` :
vous devez choisir explicitement Codex ou les deux intégrations si vous les
souhaitez.

<details>
<summary>Autres méthodes d'installation</summary>

#### Initialisation ponctuelle

```bash
uvx codexspec init my-project --ai claude
uvx codexspec init . --ai codex
```

L'initialisation ponctuelle installe les commandes du projet et l'environnement
d'exécution autonome pour les commits. Le routage des worktrees, les flux
blueprint/auto-dev et la revue manuelle du profil continuent d'utiliser la CLI
CodexSpec ; veillez à la rendre disponible pour ces flux de travail.

#### Versions de développement

```bash
uv tool install git+https://github.com/Zts0hg/codexspec.git
uv tool install git+https://github.com/Zts0hg/codexspec.git@main

# Replace <tag> with the version you want
uv tool install git+https://github.com/Zts0hg/codexspec.git@<tag>
```

</details>

<details>
<summary>Installation sous Windows</summary>

Utilisez PowerShell :

```powershell
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
# Restart PowerShell, then:
uv tool install codexspec
codexspec version
```

Le [Guide de résolution des problèmes sous Windows](docs/en/WINDOWS-TROUBLESHOOTING.md)
explique comment résoudre les problèmes de PATH et d'installation.

</details>

### Mettre à jour CodexSpec et les fichiers du projet

La mise à jour de la CLI et celle des commandes installées dans un projet sont deux opérations distinctes :

```bash
uv tool install codexspec --upgrade
# Or: pip install --upgrade codexspec

# In the project you want to refresh; select its desired integration(s)
codexspec init . --force --ai both
```

Utilisez `--ai claude` ou `--ai codex` si vous ne souhaitez qu'une seule
intégration. `--force` régénère les commandes et scripts distribués et actualise
les ressources de revue. Il confirme aussi automatiquement les demandes de
migration, de mise à jour des commandes et de conformité à la constitution.
Les exigences et les principes du projet sont conservés. Dans les fichiers de
contexte, les consignes gérées sont mises à jour, tandis que le corps existant
est préservé. Les clés de configuration que vous n'avez pas explicitement
définies sont également conservées.

La commande de planification est `design-to-plan`. Lors d'une mise à jour de
l'installation, l'ancienne entrée `spec-to-plan` est supprimée sans être
conservée comme alias.

### Installation depuis le marketplace de plugins

Dans Claude Code, installez le plugin depuis son marketplace :

```text
/plugin marketplace add Zts0hg/codexspec
/plugin install codexspec@codexspec-market
/codexspec:config
```

Le plugin fournit des commandes et des consignes chargées au démarrage de la
session, y compris lors d'une reprise, pour analyser les changements préparés
pour un commit et consulter les exigences historiques. Son installation
n'initialise pas le projet. Utilisez `/codexspec:config` pour créer ou modifier
les paramètres de langue, de flux de travail et de revue ; si vous avez besoin
de la structure complète du projet, initialisez-le avec la CLI.

L'environnement d'exécution fourni permet de prévisualiser directement les
commits et de réaliser des commits autorisés dans le dossier courant avec
Python 3.11+ et Git, sans installation persistante de la CLI CodexSpec.
Le routage des worktrees, les flux blueprint/auto-dev et la revue manuelle du
profil continuent d'exiger la CLI. Le hook de démarrage du plugin nécessite Git
dans PATH et une version de Claude Code prenant en charge `args` dans les
hooks de commandes (forme exec). Ses consignes s'adressent à l'agent ; il
n'intercepte pas les commandes Git exécutées manuellement.

Consultez [Installation](docs/en/getting-started/installation.md) pour la procédure complète.

## Flux de travail principal

Dans le flux standard, les artefacts de chaque fonctionnalité conservent des références à leurs sources :

```text
/specify          → requirements.md
/generate-spec    → spec.md       → review-spec
/spec-to-design   → design.md     → review-design
/design-to-plan   → plan.md       → review-plan
/plan-to-tasks    → tasks.md      → review-tasks → analyze
/implement-tasks  → implementation and complete-feature code review
```

Les exemples suivants utilisent le préfixe `/codexspec:` de Claude. Dans
Codex, utilisez `$codexspec:` avec le même nom de commande et les mêmes arguments.

| Étape | Commande | Objectif et résultat |
|------|---------|--------------------|
| Principes du projet | `/codexspec:constitution` | Créer ou mettre à jour `constitution.md` et valider les artefacts concernés |
| Exigences | `/codexspec:specify <idea>` | Discuter de l'intention, confirmer le résumé final et enregistrer `requirements.md` |
| Spécification | `/codexspec:generate-spec <feature-dir>` | Élaborer `spec.md` à partir des exigences confirmées, avec des références aux sources |
| Conception du système | `/codexspec:spec-to-design <feature-dir>` | Élaborer `design.md` avec les composants, les interfaces et les principales décisions de conception |
| Plan d'implémentation | `/codexspec:design-to-plan <feature-dir>` | Élaborer `plan.md` avec les phases, leur ordre et les vérifications |
| Tâches | `/codexspec:plan-to-tasks <feature-dir>` | Élaborer un `tasks.md` traçable et vérifiable, puis analyser la cohérence entre les artefacts |
| Implémentation | `/codexspec:implement-tasks <feature-dir>` | Exécuter les tâches, vérifier les résultats et corriger les constats de revue vérifiés de façon indépendante |

Remplacez `<feature-dir>` par le dossier de la fonctionnalité indiqué lors de
la définition des exigences. Poursuivez dans son worktree ou fournissez son
chemin explicite pour conserver la même identité de fonctionnalité d'une
commande ou d'une session à l'autre.

### specify, clarify et analyze

- **specify** lance ou reprend la définition des exigences. Le résumé ne devient contraignant qu'après confirmation explicite.
- **clarify** résout les ambiguïtés des exigences ou de la spécification existantes : jusqu'à cinq questions par exécution, réparties entre quatre catégories. Il met d'abord à jour `requirements.md`, puis synchronise `spec.md`.
- **analyze** vérifie toute la chaîne : exigences → spécification → conception → plan → tâches. Il applique automatiquement des corrections déterministes aux artefacts dérivés lorsque ces corrections découlent des sources qui font autorité ; il ne modifie jamais `requirements.md`. Les constats non résolus sont signalés. Il s'exécute automatiquement après une revue des tâches validée et reste informatif, sans bloquer l'implémentation.

```text
/codexspec:clarify <feature-dir>
/codexspec:analyze <feature-dir>
```

### Petits changements avec Quick

Utilisez `quick` pour un changement limité et bien défini, comme une correction locale :

```text
/codexspec:quick Fix the empty-state message on the task list
```

Quick confirme et enregistre un résumé bref des exigences, puis coordonne
la spécification, la planification, les tâches et l'implémentation avec les
revues des commandes de génération. Les changements de grande ampleur et les
choix de produit ou de conception encore en suspens nécessitent le flux standard.
Quick s'arrête lorsqu'une nouvelle décision est nécessaire.

### Automatisation du flux de travail

La valeur par défaut de `workflow.auto_next` est **false**. Si elle est `true`
dans la configuration de l'espace de travail actif, la confirmation finale des
exigences lance l'étape de spécification. Chaque étape de génération avance
après un résultat `PASS` ou `PASS_WITH_WARNINGS` ; un résultat `NEEDS_REVISION`
ou `BLOCKED` arrête la chaîne. `implement-tasks` est la dernière étape.

La correction automatique des artefacts ne porte que sur les défauts vérifiés
dont la solution découle des éléments établis dans les artefacts en amont,
avec un maximum de deux cycles de correction et de revue. Les recommandations
sont traitées séparément. La revue et la correction de l'implémentation ont
leurs propres règles d'achèvement, décrites plus loin.

Le [guide du flux de travail](docs/en/user-guide/workflow.md) détaille les règles de chaque étape.

## Blueprint partagé et développement autonome

Utilisez `blueprint` pour préparer plusieurs exigences confirmées avant le
développement, puis `auto-dev` pour développer cette file :

```text
/codexspec:blueprint Add a confirmed requirement for task reminders
/codexspec:auto-dev
```

Avant qu'une exigence soit ajoutée à la file du blueprint, les orientations,
les choix et les contraintes qui relèvent de l'utilisateur sont résolus.
Le fichier partagé `.codexspec/blueprint.md` utilise les états `pending`,
`in_progress` et `completed`. Vous pouvez ajouter, remplacer, supprimer ou
réordonner les exigences en attente. Lors de la maintenance du blueprint,
les entrées en cours et terminées restent en lecture seule.

Auto-dev développe les exigences dans l'ordre du document. Il reprend la
fonctionnalité en cours avant d'en commencer une autre et relit la file après
chaque achèvement, ce qui permet aux nouvelles exigences en attente de rejoindre
l'exécution. Il réalise les étapes SDD, l'implémentation, la vérification, la
revue et les corrections dans le cadre des exigences confirmées. L'appel à
`auto-dev` active son automatisation indépendamment de `workflow.auto_next`,
sans modifier ce paramètre.

Les deux commandes partagent `worktree-for-codexspec-auto-dev`, sur la branche
`codexspec/auto-dev`. Elles peuvent s'exécuter simultanément grâce aux mécanismes
communs qui contrôlent l'attribution de l'espace de travail et protègent les
écritures ; les exigences y sont développées une à une. Si un choix de produit ne peut pas être résolu à
partir des exigences confirmées, l'exécution s'arrête en présentant les éléments
qui le justifient, au lieu de poser des questions pendant le fonctionnement
autonome normal.

Pour consulter le blueprint partagé sans le modifier :

```bash
codexspec show-blueprint
```

## Développement avec les worktrees

Un worktree Git est un autre dossier de travail du même dépôt, avec sa propre
branche active. Par défaut, CodexSpec en utilise un par fonctionnalité du flux
standard. Il le crée avant d'écrire la première exigence et y regroupe les
documents, l'implémentation, les tests et les corrections de cette fonctionnalité.

```text
projects/
├── my-project/
└── my-project-codexspec-worktrees/
    ├── <feature-id>-task-reminders/
    ├── <feature-id>-search/
    ├── worktree-for-codexspec-maintenance/
    └── worktree-for-codexspec-auto-dev/
```

Lorsque vous reprenez une fonctionnalité, son espace de travail est réutilisé.
Les modifications indépendantes de configuration, de constitution ou de profil
s'effectuent dans le worktree de maintenance ; celles d'une fonctionnalité
active restent dans son worktree. La configuration est **locale à chaque
checkout** : un paramètre modifié dans le worktree vers lequel l'opération est
dirigée y prend effet d'abord, puis se propage aux autres checkouts par
intégration Git. Exécutez les commandes de la CLI et les vérifications dans
l'espace de travail indiqué.

Pour établir la base d'une nouvelle fonctionnalité, CodexSpec compare
l'historique des commits de la branche principale locale à celui de la branche
principale distante récupéré par fetch, selon leurs liens d'ascendance Git.
Si les historiques ont divergé, ils sont fusionnés dans le nouveau worktree
et la fusion doit être vérifiée. Si fetch échoue, un avertissement est émis et
les références disponibles localement peuvent être utilisées. Un échec de
création n'autorise pas à écrire à la place dans le checkout principal.

La valeur par défaut de `workflow.worktrees` est **true**. Seul le booléen YAML
littéral `false` désactive l'isolation des fonctionnalités du flux standard
et de la maintenance. Blueprint/auto-dev conservent toujours leur worktree
partagé fixe. L'initialisation et les mises à jour d'installation s'effectuent
dans le checkout que vous sélectionnez explicitement. Les worktrees des
fonctionnalités terminées sont conservés ; l'achèvement ne les fusionne ni
ne les supprime automatiquement.

Consultez [Développement avec les worktrees](docs/en/user-guide/workflow.md#worktree-development)
et [configuration](docs/en/reference/configuration.md#workflowworktrees).

## Travailler avec du code existant

Ces deux commandes répondent à des besoins différents :

| Commande | Utilisation | Résultat et limites |
|---------|-----------|-----------------|
| `onboard [path]` | Constituer des connaissances réutilisables sur le projet à partir d'une base de code existante | Conventions candidates et contraintes étayées par des éléments précis dans le profil ; le code reste en lecture seule |
| `reverse-spec [path]` | Comprendre l'architecture existante ou comparer le code à l'intention confirmée | Brouillons d'artefacts ou rapport de dérive ; le code reste en lecture seule |

```text
/codexspec:onboard src/
/codexspec:reverse-spec
/codexspec:reverse-spec src/auth
```

Onboard déduit des conventions du code observable et ne propose des
contraintes qu'en présence d'interdictions explicites. Les conventions candidates
s'appliquent immédiatement dans le projet ; les contraintes candidates exigent
une décision dans la session pour les enregistrer, les modifier ou les
abandonner. Les connaissances existantes sont préservées. Un premier examen
du code ne sert pas à inventer les raisons de décisions passées ou des pièges
supposément rencontrés par expérience.

Reverse-spec propose trois modes :

- **Vue d'ensemble** : sans chemin, ou avec la racine du dépôt, la commande produit un `design.md` décrivant brièvement l'architecture et un `slices.md` pour choisir les modules à examiner.
- **Génération** : avec le chemin d'un module sans base confirmée, elle produit des brouillons de `spec.md` et de `design.md`, ainsi que des exigences en suspens ou inférées.
- **Réconciliation** : si le module dispose d'une base confirmée, elle produit `reconcile.md`. Ce rapport relève les comportements non documentés, les spécifications non implémentées et les divergences sémantiques par rapport aux spécifications et aux documents de conception confirmés ; les exigences font autorité sur l'intention du produit.

Les brouillons inférés doivent être confirmés par une personne avant de devenir
une base de référence. La réconciliation propose une marche à suivre — corriger
le code, mettre à jour les documents ou décider de l'intention — sans l'appliquer
automatiquement.

## Revue et débogage

Les quatre revues d'artefacts — `review-spec`, `review-design`, `review-plan`
et `review-tasks` — vérifient la fidélité, la couverture, la faisabilité et la
qualité interne. Elles s'exécutent automatiquement après la génération et
peuvent aussi être lancées manuellement. Les rapports distinguent les défauts
vérifiés des avertissements sur les risques qui ne bloquent pas la progression
et des possibilités de conception ; ils incluent un score de compatibilité.

`review-code` propose un contrôle de défauts distinct portant sur les changements,
ainsi qu'une évaluation explicite de la qualité du code dans son ensemble :

```text
/codexspec:review-code --feature <feature-dir>
/codexspec:review-code --uncommitted
/codexspec:review-code --audit src/
```

La revue par défaut couvre tous les changements de la branche de la
fonctionnalité : ceux déjà committés, ceux indexés, ceux non indexés et les
fichiers non suivis qui ne sont pas ignorés. Vous pouvez sélectionner
explicitement les changements committés, non committés ou ceux d'un seul commit.
`--feature` ajoute le contexte des exigences sans réduire le périmètre Git.
`--audit` évalue les chemins indiqués et produit une grille indicative de qualité
plutôt qu'un verdict d'achèvement.

Les revues chargent les normes communes depuis `.codexspec/review-code/` et
sélectionnent les dimensions de comportement ainsi que les vérifications de
langage ou de framework pertinentes. Chaque constat doit être étayé par des
éléments concrets, une condition qui peut se produire, un lien démontré avec
les changements sélectionnés et un impact. L'agent de revue signale les défauts
et les suggestions de maintenance étayées sans modifier les fichiers ; le
processus chargé des corrections les vérifie de façon indépendante.

Pour les tâches de code, l'implémentation commence par les tests. La documentation
et la configuration sont modifiées directement, avec les vérifications adaptées.
Après une correction, la revue incrémentale peut réutiliser la couverture qui
n'a pas été affectée. L'acceptation finale exige une nouvelle revue de toute
la fonctionnalité avec un résultat `PASS`, une couverture et une vérification
complètes, et aucun défaut P0–P3 admis. Les suggestions de maintenance étayées
sont présentées séparément.

La valeur par défaut de `workflow.auto_maintenance` est **true**. Ce paramètre
détermine si les processus de correction appliquent aussi des améliorations de
maintenance vérifiées et compatibles. Si vous le désactivez, ces suggestions
restent signalées et les corrections des défauts ainsi que les vérifications
requises restent obligatoires. Ce paramètre est indépendant du passage à
l'étape suivante et n'est pas un argument de `implement-tasks`.

Pour commencer le débogage par la recherche de la cause racine :

```text
/codexspec:debug Investigate intermittent failures when saving a task
```

Debug suit cette séquence : investigation → analyse des motifs récurrents →
vérification d'une seule hypothèse → correction précédée d'un test en échec.
Pendant l'implémentation, ce processus est utilisé lorsque les corrections
n'aboutissent pas, qu'un défaut de fonctionnement non trivial doit être retracé
ou que le même type de cause racine réapparaît au fil des revues. Trois tentatives
de correction infructueuses déclenchent une réévaluation de l'architecture.

Utilisez `checklist` pour évaluer la clarté, l'exhaustivité et la cohérence des exigences :

```text
/codexspec:checklist Check the authentication requirements for completeness
```

La [référence des commandes](docs/en/user-guide/commands.md) détaille les
sélecteurs de revue, les arguments et les procédures.

## Connaissances du projet

Le profil du projet conserve les connaissances réutilisables dans `.codexspec/profile/` :

| Catégorie | Contenu |
|----------|----------|
| `constraints/` | Interdictions explicites et limites strictes, à lire en premier |
| `conventions/` | Pratiques, nommage et consignes communes à plusieurs fonctionnalités |
| `pitfalls/` | Pièges rencontrés, causes, solutions de contournement et leçons |
| `decisions/` | Décisions d'architecture et autres décisions réutilisables d'une fonctionnalité à l'autre |
| `strategies/` | Signaux indiquant qu'il faut changer d'approche |
| `runbooks/` | Procédures ordonnées et reprise après échec |

`distill` recueille les connaissances réutilisables issues du travail effectué.
L'intention propre à chaque fonctionnalité reste dans ses exigences, sa
conception et son plan. L'initialisation installe des consignes dans CLAUDE.md
et/ou AGENTS.md pour lire toutes les contraintes et les connaissances pertinentes
avant tout travail substantiel. Les connaissances ajoutées par la suite peuvent
s'appliquer sans nouvelle initialisation. Les entrées candidates sont utilisées
avec prudence ; les entrées validées exigent des résultats vérifiés et une
approbation humaine.

```text
/codexspec:distill Capture the reusable lessons from this work
/codexspec:distill review
/codexspec:evolve
```

Lorsque vous lancez manuellement `distill review`, ou appelez directement
`distill` sans nouveau contenu à recueillir, un espace de travail local s'ouvre
dans le navigateur et fonctionne hors ligne. Vous pouvez réviser, valider,
abandonner, différer et consolider les entrées, prévisualiser le Markdown final,
puis sélectionner **Tout appliquer**. Les décisions restent dans un brouillon
récupérable jusqu'à leur application. Les contrôles de conflit empêchent une
application partielle ou un écrasement sans avertissement. Un mode texte
explicite est également disponible dans les environnements sans navigateur.

La valeur par défaut de `workflow.auto_distill` est **true**. Ce paramètre
contrôle trois hooks de fin : l'achèvement réussi de `implement-tasks`, les
commits exécutés via `commit-staged` et la génération de `pr`. La prévisualisation
d'un commit ne déclenche pas la capture.

Les consignes installées dans le projet demandent aussi à l'agent de recueillir
les connaissances réutilisables dès qu'elles apparaissent dans les conversations
courantes, les corrections hors SDD et les longues exécutions de `implement-tasks`.
Ces consignes s'appliquent indépendamment du paramètre de fin ; la capture en
fin de tâche offre une dernière occasion de conserver ces connaissances.

Dans une même session, les déclenchements répétés ne traitent que le nouveau
contenu. D'une session à l'autre, `distill` lit le profil et ignore les
connaissances qui y figurent déjà. S'il ne reste rien de réutilisable, la capture
se termine sans écrire. La capture automatique n'ouvre jamais la revue manuelle,
n'attend jamais une personne et ne bloque jamais le flux de travail qui l'appelle.

`evolve` ne sélectionne que des connaissances validées utiles au-delà du projet,
élabore un brouillon de commande ou de compétence et obtient une approbation
explicite avant d’effectuer un push ou d'ouvrir une PR de contribution
pour revue humaine.

Consultez [Connaissances du projet](docs/en/user-guide/commands.md#codexspecdistill)
pour les consignes détaillées.

### Réutiliser les décisions historiques

Avant tout jugement substantiel sur les exigences, la conception, l'implémentation,
le débogage ou la revue, l'agent consulte aussi l'historique pertinent dans
`.codexspec/specs/`, aussi bien dans les conversations courantes que dans les
flux SDD. Avant d'interroger l'utilisateur, il reconstitue les décisions toujours
en vigueur, les ajouts ultérieurs et les remplacements explicites.

Les exigences anciennes qui n'ont pas été modifiées restent applicables.
La dernière décision explicite de l'utilisateur prévaut toujours ; les propositions
en suspens ne valent pas intention confirmée. La recherche se limite aux éléments
pertinents pour la tâche et le contexte suffisant déjà préparé est réutilisé.
Actualisez les installations des projets existants pour recevoir ces consignes.

## Flux de travail Git

```text
/codexspec:commit-staged -p
/codexspec:pr --spec <feature-dir>/spec.md
/codexspec:release-notes --from <ref> --to HEAD
/codexspec:tasks-to-issues <feature-dir>
```

- **commit-staged** analyse exactement l'index et génère un message Conventional Commits ; `-p` affiche un aperçu sans créer de commit. Le flux qui l'appelle choisit et indexe les fichiers. L'exécution autorisée utilise un environnement protégé qui vérifie à nouveau que le contenu committé correspond à l'analyse. Les consignes de commit destinées à l'agent s'appliquent dans les conversations courantes et les flux SDD, blueprint et auto-dev ; la disponibilité de la commande ne vaut ni invocation ni autorisation de commit.
- **pr** génère une description structurée de PR GitHub ou de MR GitLab à partir du diff. `--spec` peut ajouter le contexte de la fonctionnalité depuis le chemin d'un fichier `spec.md`, ou depuis un nom ou préfixe de dossier de fonctionnalité résolu vers ce fichier. La sortie par défaut est du texte à utiliser sur la plateforme d'hébergement.
- **release-notes** produit à partir de l'historique Git une entrée Keep a Changelog et le texte d'une publication. La section par défaut est `[Unreleased]` ; `--version` utilise le libellé fourni. La commande n'indexe rien, ne crée pas de commit, n'incrémente pas les versions, ne crée pas de tag, ne publie rien et ne crée pas de release.
- **tasks-to-issues** crée des issues GitHub à partir des tâches existantes, avec leurs dépendances et leurs critères d'acceptation. Elle nécessite une CLI GitHub authentifiée et vérifie que le dépôt des issues correspond au dépôt distant configuré.

La prévisualisation directe des commits et les commits autorisés dans le dossier
courant nécessitent Python 3.11+ et Git. L'environnement d'exécution est installé
dans les projets initialisés par CLI et fourni avec le plugin Claude. Les
fusions créées par l'agent qui modifient le contenu passent également par
l'analyse des changements indexés. Les fusions qui relient seulement les
historiques conservent le message par défaut de Git tout en validant l'arbre
et les parents ; les avances rapides ne créent aucun commit.

## Commandes disponibles

La CLI possède six commandes publiques. Les intégrations d'agents distribuent
28 commandes : Claude utilise `/codexspec:<name>` et Codex, `$codexspec:<name>`.
Les tableaux suivants présentent la notation de Claude pour faciliter la lecture.

### Commandes CLI

| Commande | Objectif |
|---------|---------|
| `codexspec init` | Initialiser ou actualiser un projet pour Claude, Codex ou les deux |
| `codexspec check` | Vérifier les outils et dépendances installés |
| `codexspec version` | Afficher la version et les informations système |
| `codexspec config` | Consulter ou modifier la configuration du projet |
| `codexspec list-commands` | Afficher les commandes d'agent disponibles par catégorie |
| `codexspec show-blueprint` | Afficher le blueprint du worktree partagé sans le modifier |

### Commandes du flux de travail principal

| Commande | Objectif |
|---------|---------|
| `/codexspec:constitution` | Créer ou mettre à jour les principes du projet et les valider entre artefacts |
| `/codexspec:specify` | Discuter des exigences d'une fonctionnalité, les confirmer et les enregistrer |
| `/codexspec:blueprint` | Préparer ou maintenir les exigences confirmées en attente du blueprint |
| `/codexspec:generate-spec` | Élaborer une spécification traçable à partir des exigences confirmées, avec revue automatique |
| `/codexspec:spec-to-design` | Définir l'architecture, les composants, les interfaces et les décisions, avec revue automatique |
| `/codexspec:design-to-plan` | Planifier les phases d'implémentation, leur ordre et leur vérification, avec revue automatique |
| `/codexspec:plan-to-tasks` | Élaborer des tâches vérifiables couvrant les artefacts en amont, avec revue automatique et analyze |
| `/codexspec:implement-tasks` | Exécuter les tâches, vérifier les résultats, effectuer les revues et les corrections |
| `/codexspec:auto-dev` | Développer de façon autonome les exigences confirmées du blueprint dans l'ordre du document |

### Commandes de revue des artefacts

| Commande | Objectif |
|---------|---------|
| `/codexspec:review-spec` | Vérifier la fidélité et la qualité interne de la spécification |
| `/codexspec:review-design` | Vérifier la fidélité et la faisabilité de la conception, ainsi que sa préparation à la planification |
| `/codexspec:review-plan` | Vérifier la fidélité et la faisabilité du plan, ainsi que sa préparation à l'implémentation |
| `/codexspec:review-tasks` | Vérifier la fidélité, les dépendances, le caractère exécutable et la vérification des tâches |

### Exigences, code existant et débogage

| Commande | Objectif |
|---------|---------|
| `/codexspec:clarify` | Résoudre les ambiguïtés des exigences en les mettant à jour avant la spécification |
| `/codexspec:analyze` | Vérifier la traçabilité de bout en bout et aligner les artefacts dérivés sur les sources qui font autorité |
| `/codexspec:checklist` | Générer une liste de contrôle de la qualité des exigences |
| `/codexspec:tasks-to-issues` | Convertir les tâches existantes en issues GitHub avec des actions concrètes |
| `/codexspec:debug` | Rechercher la cause racine avant d'appliquer une correction |
| `/codexspec:reverse-spec` | Examiner l'architecture existante, rédiger des brouillons d'artefacts de modules ou signaler une dérive par rapport à la base confirmée |

### Commandes de gestion des connaissances du projet

| Commande | Objectif |
|---------|---------|
| `/codexspec:distill` | Recueillir des connaissances réutilisables ou examiner les entrées candidates dans l'espace de travail local |
| `/codexspec:evolve` | Élaborer un brouillon de contribution au projet amont à partir de connaissances validées |
| `/codexspec:onboard` | Déduire des conventions candidates et des contraintes étayées du code existant |

### Commandes Git et de revue du code

| Commande | Objectif |
|---------|---------|
| `/codexspec:commit-staged` | Générer des messages à partir des changements indexés ; prévisualiser ou exécuter un commit autorisé |
| `/codexspec:pr` | Générer une description structurée de PR/MR |
| `/codexspec:release-notes` | Maintenir une entrée du journal des changements et produire le texte d'une publication à partir de l'historique Git |
| `/codexspec:review-code` | Examiner les changements sélectionnés comme contrôle de défauts ; utiliser `--audit` pour évaluer la qualité dans les chemins indiqués |

### Commandes utilitaires

| Commande | Objectif |
|---------|---------|
| `/codexspec:config` | Créer, consulter, modifier ou réinitialiser la configuration du projet de façon interactive |
| `/codexspec:quick` | Exécuter un flux SDD bref avec priorité aux exigences pour les petits changements |

## Configuration et internationalisation

La configuration est enregistrée dans `.codexspec/config.yml`. Les modèles
restent en anglais ; l'agent rédige les échanges et les artefacts générés dans
les langues configurées. Les 13 codes de langue standard sont `en`, `zh-CN`,
`zh-TW`, `ja`, `ko`, `es`, `fr`, `de`, `pt`, `ru`, `it`, `ar` et `hi`.
Pour le portugais, la CLI utilise `pt` ; la documentation localisée et les
catalogues de traduction utilisent `pt-BR`.

### Langues des échanges, des documents et des commits

| Dimension | Clé de configuration | À l'initialisation | Modifier ensuite | Ce qu'elle contrôle |
|-----------|------------|-------------------|-----------|----------|
| Sortie/base | `language.output` | `--lang` | `config --set-lang` | Langue de repli pour les autres dimensions |
| Échanges | `language.interaction` | `--interaction-lang` | `config --set-interaction-lang` | Conversation et sortie de la CLI |
| Documents | `language.document` | `--document-lang` | `config --set-document-lang` | Exigences, spécifications, documents de conception, plans et tâches |
| Commits | `language.commit` | `--commit-lang` | `config --set-commit-lang` | Messages de commit et textes générés dans les flux de travail Git |

Si la langue d'une dimension n'est pas définie, `language.output` est utilisée,
puis `en` à défaut. Cette règle s'applique indépendamment à chaque dimension.
`language.templates` reste à `en`.

```bash
codexspec init my-project --ai both \
  --interaction-lang zh-CN --document-lang en --commit-lang en

codexspec config
codexspec config --set-document-lang en
codexspec config --list-langs
```

Lors de la première initialisation depuis un terminal TTY, la langue de base
vous est demandée, sauf si vous fournissez `--lang` ou les trois options de
langue spécifiques. `--force` confirme automatiquement les autres demandes
d'initialisation, mais ne supprime pas cette sélection. Sans TTY, l'anglais est
utilisé par défaut. Une nouvelle initialisation conserve les clés de langue
que vous n'avez pas explicitement définies.

### Paramètres du flux de travail et des revues

| Paramètre | Valeur par défaut | Effet | Commande CLI |
|---------|---------|--------|-------------|
| `workflow.auto_next` | `false` | Passer à l'étape suivante du flux SDD standard après validation | `config --auto-next on\|off` |
| `workflow.auto_distill` | `true` | Recueillir des connaissances sans interaction à l'issue d'un travail réussi | `config --auto-distill on\|off` |
| `workflow.auto_maintenance` | `true` | Appliquer une maintenance incrémentale vérifiée pendant les corrections automatiques | `config --auto-maintenance on\|off` |
| `workflow.worktrees` | `true` | Isoler les fonctionnalités du flux standard et la maintenance indépendante | `config --worktrees on\|off` |
| `review.decided_by` | `reviewer` | Déterminer qui statue sur les constats dont la condition se produit hors du contexte opérationnel du projet | `config --decided-by reviewer\|ask` |

Les options booléennes de la CLI acceptent `on/true/1/yes` et `off/false/0/no`,
sans distinction de casse et avec d'éventuels espaces autour de la valeur.
Une option booléenne sans valeur inverse la valeur actuelle du checkout de
destination ; les valeurs sont enregistrées sous forme de booléens dans YAML.

Avec `review.decided_by: reviewer`, l'agent de revue décide quels constats sont
admis comme défauts. Avec `ask`, lorsqu'une condition à l'origine d'un constat
se produit hors du contexte du projet, une décision sur ce scénario reste en
attente. L'utilisateur décide une fois s'il faut corriger le problème ou exclure
le scénario, puis sa décision confirmée est conservée pour les revues suivantes.
Les décisions en attente bloquent l'achèvement. Pour une exécution donnée de
`review-code`, vous pouvez remplacer le mode configuré avec `--decided-by`.

Les modifications de configuration suivent le routage des worktrees. Un
changement indépendant demandé depuis le checkout principal s'effectue dans
le worktree de maintenance et ne modifie pas immédiatement le paramètre effectif
du principal. Les changements effectués dans le worktree d'une fonctionnalité
y prennent effet.

<details>
<summary>Options d'initialisation de la CLI</summary>

| Option | Signification |
|--------|---------|
| `PROJECT_NAME` | Nom du nouveau dossier ; utiliser `.` pour le dossier courant |
| `--here`, `-h` | Initialiser le dossier courant |
| `--ai`, `-a` | `claude`, `codex` ou `both` ; valeur par défaut : `claude` |
| `--lang`, `-l` | Définir la langue de sortie de base |
| `--interaction-lang` | Définir la langue des échanges |
| `--document-lang` | Définir la langue des documents |
| `--commit-lang` | Définir la langue des messages de commit |
| `--force`, `-f` | Régénérer les artefacts installés et confirmer automatiquement les demandes de migration, de mise à jour et de conformité ; préserver le contexte rédigé pour le projet et les paramètres sans rapport |
| `--no-git` | Ne pas initialiser le dépôt Git |
| `--debug`, `-d` | Afficher des informations de débogage détaillées |

</details>

<details>
<summary>Options de configuration de la CLI</summary>

| Option | Signification |
|--------|---------|
| `--set-lang`, `-l` | Définir la langue de sortie de base |
| `--set-interaction-lang` | Définir la langue des échanges |
| `--set-document-lang` | Définir la langue des documents |
| `--set-commit-lang`, `-c` | Définir la langue des messages de commit |
| `--list-langs` | Afficher les codes de langue pris en charge |
| `--auto-next` | Inverser ou définir le passage automatique à l'étape suivante |
| `--auto-distill` | Inverser ou définir la capture automatique des connaissances |
| `--auto-maintenance` | Inverser ou définir la maintenance incrémentale automatique |
| `--worktrees` | Inverser ou définir l'isolation par worktree locale à chaque checkout |
| `--decided-by` | Définir le mode de décision de revue sur `reviewer` ou `ask` |

</details>

<details>
<summary>Exemple de configuration</summary>

```yaml
version: "1.0"

language:
  output: "en"
  interaction: "zh-CN"
  document: "en"
  commit: "en"
  templates: "en"

project:
  ai: "both"

workflow:
  auto_next: false
  auto_distill: true
  auto_maintenance: true
  worktrees: true

review:
  decided_by: reviewer
```

</details>

Consultez [Configuration](docs/en/reference/configuration.md) et
[Internationalisation](docs/en/user-guide/i18n.md) pour connaître en détail
le fonctionnement des langues et des paramètres.

## Structure du projet

L'initialisation installe les ressources communes et l'intégration de l'assistant sélectionné :

```text
my-project/
├── .codexspec/
│   ├── config.yml
│   ├── memory/
│   │   └── constitution.md
│   ├── profile/
│   │   ├── constraints/
│   │   ├── conventions/
│   │   ├── pitfalls/
│   │   ├── decisions/
│   │   ├── strategies/
│   │   └── runbooks/
│   ├── review-code/              # Shared review standards
│   ├── specs/
│   │   └── <feature-id>-<name>/   # Added by feature workflows
│   │       ├── requirements.md
│   │       ├── spec.md
│   │       ├── design.md
│   │       ├── plan.md
│   │       ├── tasks.md
│   │       ├── review-*.md
│   │       └── checklists/       # When requested
│   ├── templates/docs/
│   └── scripts/                 # Platform helpers and commit runtime
├── .claude/commands/codexspec/   # --ai claude or both
├── .agents/skills/              # --ai codex or both
├── CLAUDE.md                    # Claude project context
└── AGENTS.md                    # Codex project context
```

Le blueprint partagé est conservé dans le worktree dédié à auto-dev. Il n'en
existe pas de copie modifiable distincte dans chaque checkout du flux standard.
Les brouillons de revue manuelle des connaissances sont exclus de Git.

## Ressources pour les extensions

Le dépôt comprend un modèle de manifeste d'extension, un exemple de commande
et un [Guide de développement des extensions](extensions/EXTENSION-DEVELOPMENT-GUIDE.md).
Ces ressources servent à créer des extensions. La CLI actuelle ne propose
aucune commande pour installer, lister ou supprimer des extensions et ne charge
pas automatiquement les commandes ou hooks de `extension.yml`. Les ressources
de revue partagées permettent des ajouts propres au projet dans
`.codexspec/review-code/`. L'initialisation conserve les ressources déjà modifiées
et les fichiers supplémentaires, sauf si leur remplacement est demandé.

## Développement

```bash
git clone https://github.com/Zts0hg/codexspec.git
cd codexspec

# Development tools are an optional dependency extra
uv sync --extra dev
# For documentation builds too: uv sync --extra dev --extra docs

uv run codexspec --help
uv run pytest
uv run ruff check src/
uv build
```

Avant de modifier les modèles, le packaging ou l'initialisation, lisez
[CLAUDE.md](CLAUDE.md), [AGENTS.md](AGENTS.md) et
[Organisation du dépôt](docs/internal/repository-layout.md). Les copies
distribuées des commandes et des compétences sont des artefacts d'installation
générés ; modifiez leurs sources faisant autorité, puis régénérez-les.

## Contribuer

Le [guide de contribution](docs/en/development/contributing.md) explique
comment préparer l'environnement local et proposer des changements. Les
contributions doivent respecter les exigences confirmées, la traçabilité des
sources et la frontière du packaging entre utilisateurs et mainteneurs.

## Licence

MIT — voir [LICENSE](LICENSE).

## Remerciements

Inspiré de [GitHub spec-kit](https://github.com/github/spec-kit).
S'intègre à Claude Code et OpenAI Codex.

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
  <strong>Une boîte à outils SDD qui donne la priorité aux exigences pour Claude Code et OpenAI Codex</strong>
</p>

CodexSpec transforme les exigences confirmées en spécifications, conceptions,
plans, tâches et implémentations traçables. Vous décidez **quoi** construire et
**pourquoi** ; l'agent détermine **comment** le réaliser dans le cadre de ces
exigences confirmées, à l'aide de points de contrôle et de connaissances
persistantes sur le projet.

Utilisez-le avec les commandes à barre oblique de Claude Code, les compétences
Codex ou les deux. Par défaut, les fonctionnalités ordinaires utilisent des
worktrees Git séparés ; un blueprint partagé facultatif permet à l'agent de
développer de manière autonome une file d'exigences confirmées.

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

| Besoin | Ce que fournit CodexSpec |
|------|-------------------------|
| Intention produit claire | Confirmation explicite et fichier `requirements.md` persistant avant la spécification |
| Développement traçable | Références aux sources à travers exigences → spécification → conception → plan → tâches |
| Décisions examinables | Quatre commandes de revue des artefacts, une analyse entre artefacts et un contrôle de défauts distinct pour le code |
| Continuité entre sessions et équipes | Dossiers de fonctionnalités, principes du projet, connaissances réutilisables et décisions historiques pertinentes |
| Plusieurs fonctionnalités en cours | Un worktree Git par fonctionnalité ordinaire, avec réutilisation stable de l'espace de travail |
| Plus d'automatisation | Progression facultative entre les étapes et développement autonome des exigences confirmées du blueprint |
| Préférences linguistiques de l'équipe | Langues indépendantes pour les échanges, les documents et les commits |

### Qu'est-ce que le SDD qui donne la priorité aux exigences ?

Le développement piloté par les spécifications qui donne la priorité aux exigences
fait des **exigences confirmées l'autorité la plus haute pour une fonctionnalité**.
L'agent consigne les objectifs, contraintes, décisions, exclusions, questions
ouvertes et preuves de confirmation avant d'en dériver les artefacts d'implémentation.

```text
Idea → Confirmed Requirements → Spec → Design → Plan → Tasks → Code
```

La collaboration humaine établit et modifie l'intention produit. Les revues
automatiques vérifient les artefacts dérivés par rapport à cette intention.
Activer l'automatisation fait progresser le travail à travers les étapes validées ;
cela n'autorise pas l'agent à remplacer silencieusement les exigences confirmées.

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

Lancez votre assistant installé dans le projet initialisé. Le même flux de
travail utilise ces deux formes d'invocation :

| Assistant | Démarrer la découverte des exigences |
|-----------|------------------------------|
| Claude Code (`claude`) | `/codexspec:specify I want to build a todo application` |
| Codex (`codex`) | `$codexspec:specify I want to build a todo application` |

Personnalisez les principes du projet avec `constitution` si nécessaire.
Confirmez le résumé final des exigences, puis poursuivez en utilisant le dossier
de la fonctionnalité et l'espace de travail renvoyés. Consultez le
[Flux de travail principal](#flux-de-travail-principal) pour les autres commandes.

Vous utilisez l'application de bureau Codex ? [Demandez à Codex d'installer et d'initialiser votre projet](#installer-avec-lapplication-de-bureau-codex).

## Installation

### Installer avec l'application de bureau Codex

Vous pouvez demander à Codex d'installer CodexSpec et de configurer votre projet directement depuis l'application de bureau.

1. Ajoutez un projet local dans l'application de bureau Codex et sélectionnez le dossier dans lequel vous souhaitez travailler.
2. Ouvrez une conversation dans ce projet et collez l'instruction ci-dessous.
3. Si l'application demande l'autorisation de télécharger ou d'installer des dépendances, approuvez l'action demandée pour continuer.

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

Pour obtenir des réponses et des documents en chinois, remplacez `--lang en` par `--lang zh-CN` et demandez à Codex d'expliquer le résultat en chinois.

Codex installe la même CLI et les mêmes compétences de projet que la configuration manuelle ci-dessous. Vous pouvez commencer à les utiliser avec une instruction telle que `$codexspec:specify I want to build a todo application`. Consultez le [guide des compétences d'OpenAI](https://learn.chatgpt.com/docs/build-skills) pour connaître le fonctionnement de la découverte et de l'actualisation des compétences locales.

### Prérequis

- Python 3.11+
- [uv](https://docs.astral.sh/uv/) (recommandé) ou pip
- L'assistant que vous comptez utiliser : Claude Code ou Codex
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

Initialisez un nouveau projet avec `codexspec init my-project --ai claude`,
ou le dossier courant avec `codexspec init . --ai codex`. Utilisez `--ai both`
pour les deux intégrations. L'assistant sélectionné par défaut est `claude` ;
choisissez explicitement la valeur pour Codex ou les deux.

<details>
<summary>Autres méthodes d'installation</summary>

#### Initialisation ponctuelle

```bash
uvx codexspec init my-project --ai claude
uvx codexspec init . --ai codex
```

L'initialisation ponctuelle installe les commandes du projet et l'environnement
d'exécution autonome pour les commits. Le routage des worktrees,
blueprint/auto-dev et la revue manuelle du profil continuent d'invoquer la CLI
CodexSpec ; assurez-vous qu'elle est disponible pour ces flux de travail.

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

Consultez le [Guide de résolution des problèmes sous Windows](docs/en/WINDOWS-TROUBLESHOOTING.md)
pour résoudre les problèmes de PATH et d'installation.

</details>

### Mettre à niveau et actualiser un projet

Mettre à jour la CLI et actualiser les commandes installées d'un projet sont deux étapes distinctes :

```bash
uv tool install codexspec --upgrade
# Or: pip install --upgrade codexspec

# In the project you want to refresh; select its desired integration(s)
codexspec init . --force --ai both
```

Utilisez `--ai claude` ou `--ai codex` si vous ne souhaitez que cette intégration.
`--force` régénère les commandes et scripts distribués et actualise les ressources
de revue ; il confirme aussi automatiquement les demandes de migration, de mise
à jour des commandes et de conformité à la constitution. Les exigences et les
principes existants du projet sont conservés, le corps des fichiers de contexte
existants est préservé tandis que les instructions gérées sont mises à jour,
et les clés de configuration que vous n'avez pas explicitement définies sont conservées.

La commande de planification est `design-to-plan` ; les mises à jour
d'installation retirent l'ancienne entrée `spec-to-plan` sans alias.

### Installation depuis le marketplace de plugins

Pour Claude Code, installez le plugin depuis son marketplace :

```text
/plugin marketplace add Zts0hg/codexspec
/plugin install codexspec@codexspec-market
/codexspec:config
```

Le plugin fournit des commandes et des instructions en début de session pour
l'analyse des commits préparés dans l'index et la consultation des exigences
historiques, y compris lors de sessions reprises. L'installation du plugin
n'initialise pas de projet. Utilisez `/codexspec:config` pour créer ou modifier
les paramètres de langue, de flux de travail et de revue ; utilisez
l'initialisation par CLI lorsque vous avez besoin de la structure complète du projet.

L'aperçu direct des commits et les commits autorisés sur place peuvent utiliser
l'environnement d'exécution fourni avec Python 3.11+ et Git, sans installation
persistante de la CLI CodexSpec. Le routage des worktrees, blueprint/auto-dev
et la revue manuelle du profil conservent leurs exigences de CLI. Le hook de
démarrage du plugin nécessite Git dans PATH et une version de Claude Code qui
prend en charge `args` dans les hooks de commandes (forme exec). Ses instructions
s'adressent à l'agent ; il n'intercepte pas les commandes Git manuelles.

Consultez [Installation](docs/en/getting-started/installation.md) pour la configuration détaillée.

## Flux de travail principal

Le flux standard d'une fonctionnalité préserve une chaîne reliée aux sources :

```text
/specify          → requirements.md
/generate-spec    → spec.md       → review-spec
/spec-to-design   → design.md     → review-design
/design-to-plan   → plan.md       → review-plan
/plan-to-tasks    → tasks.md      → review-tasks → analyze
/implement-tasks  → implementation and complete-feature code review
```

Les exemples ci-dessous utilisent le préfixe `/codexspec:` de Claude. Dans Codex,
utilisez `$codexspec:` avec le même nom de commande et les mêmes arguments.

| Étape | Commande | Objectif et résultat |
|------|---------|--------------------|
| Principes du projet | `/codexspec:constitution` | Créer/mettre à jour `constitution.md` et valider les artefacts concernés |
| Exigences | `/codexspec:specify <idea>` | Discuter de l'intention, confirmer un résumé final et enregistrer `requirements.md` |
| Spécification | `/codexspec:generate-spec <feature-dir>` | Compiler les exigences confirmées dans `spec.md` avec des références aux sources |
| Conception du système | `/codexspec:spec-to-design <feature-dir>` | Produire `design.md` : composants, interfaces et décisions de conception clés |
| Plan d'implémentation | `/codexspec:design-to-plan <feature-dir>` | Produire `plan.md` : phases, ordre et vérification |
| Tâches | `/codexspec:plan-to-tasks <feature-dir>` | Produire un `tasks.md` traçable et vérifiable ; exécuter l'analyse entre artefacts |
| Implémentation | `/codexspec:implement-tasks <feature-dir>` | Exécuter les tâches, vérifier les résultats et corriger les constats de revue vérifiés indépendamment |

Remplacez `<feature-dir>` par le dossier de la fonctionnalité renvoyé lors de
la découverte. Poursuivez dans son worktree ou indiquez son chemin explicite ;
cela conserve l'identité de la fonctionnalité entre les commandes et les sessions.

### specify, clarify et analyze

- **specify** démarre ou reprend la découverte des exigences. Seule une confirmation
  explicite rend le résumé des exigences contraignant.
- **clarify** résout les ambiguïtés des exigences ou de la spécification existantes :
  jusqu'à cinq questions par exécution, réparties entre quatre catégories.
  Il met d'abord à jour `requirements.md`, puis synchronise `spec.md`.
- **analyze** vérifie toute la chaîne exigences → spécification → conception → plan →
  tâches. Il applique automatiquement des corrections déterministes aux artefacts
  en aval lorsque la correction découle de l'autorité des artefacts en amont ;
  il ne modifie jamais `requirements.md`. Les constats non résolus sont signalés.
  Il s'exécute automatiquement après une revue des tâches validée et reste
  informatif, sans constituer un contrôle bloquant pour l'implémentation.

```text
/codexspec:clarify <feature-dir>
/codexspec:analyze <feature-dir>
```

### Petits changements avec Quick

Utilisez `quick` pour un petit changement bien délimité, comme une correction locale :

```text
/codexspec:quick Fix the empty-state message on the task list
```

Quick confirme et enregistre un résumé compact des exigences, puis orchestre
la spécification, la planification, les tâches et l'implémentation avec les
revues des commandes de génération. Les changements étendus ou les choix de
produit ou de conception non résolus nécessitent le flux standard ; Quick
s'arrête lorsqu'une nouvelle décision est nécessaire.

### Automatisation du flux de travail

`workflow.auto_next` vaut **false** par défaut. Lorsqu'il vaut `true` dans la
configuration de l'espace de travail actif, la confirmation finale des exigences
fait passer à la spécification. Chaque étape de génération avance après `PASS`
ou `PASS_WITH_WARNINGS` ; `NEEDS_REVISION` ou `BLOCKED` arrête la chaîne.
`implement-tasks` est l'étape finale.

La correction automatique des artefacts se limite aux défauts vérifiés dont la
correction découle des preuves en amont, avec au maximum deux cycles de
correction et de revue. Les recommandations restent séparées. La boucle de
revue et de correction de l'implémentation dispose de ses propres règles de
fin, décrites ci-dessous.

Consultez le [guide du flux de travail](docs/en/user-guide/workflow.md) pour les contrats détaillés.

## Blueprint partagé et développement autonome

Utilisez `blueprint` pour préparer plusieurs exigences confirmées avant le
développement, puis `auto-dev` pour développer cette file :

```text
/codexspec:blueprint Add a confirmed requirement for task reminders
/codexspec:auto-dev
```

La découverte du blueprint résout les orientations, les choix et les contraintes
qui relèvent de l'utilisateur avant l'entrée d'une exigence dans la file.
Le fichier partagé `.codexspec/blueprint.md` utilise les états `pending`,
`in_progress` et `completed`. Vous pouvez ajouter, remplacer, supprimer ou
réordonner les exigences en attente ; les entrées actives et terminées sont en
lecture seule pour la maintenance du blueprint.

Auto-dev suit l'ordre du document, reprend une fonctionnalité en cours avant
d'en commencer une autre et relit la file après chaque achèvement afin que les
nouveaux travaux en attente puissent rejoindre l'exécution. Il effectue les
étapes SDD, l'implémentation, la vérification, la revue et la correction dans le
cadre des exigences confirmées. Invoquer `auto-dev` active son automatisation
indépendamment de `workflow.auto_next` et ne modifie pas ce paramètre.

Les deux commandes partagent `worktree-for-codexspec-auto-dev` sur la branche
`codexspec/auto-dev`. Elles peuvent fonctionner simultanément sous les
protections partagées de propriété et d'écriture ; les exigences sont développées
séquentiellement dans cet espace de travail. Les décisions produit qui ne
peuvent pas être résolues à partir des exigences confirmées arrêtent l'exécution
avec des preuves plutôt que de poser des questions pendant une exécution autonome normale.

Consultez le blueprint partagé actuel sans le modifier :

```bash
codexspec show-blueprint
```

## Développement avec les worktrees

Un worktree Git est un autre dossier de travail du même dépôt, avec sa propre
branche extraite. CodexSpec en utilise un par fonctionnalité ordinaire par défaut,
le crée avant la première écriture des exigences et regroupe les documents,
l'implémentation, les tests et les corrections de cette fonctionnalité.

```text
projects/
├── my-project/
└── my-project-codexspec-worktrees/
    ├── <feature-id>-task-reminders/
    ├── <feature-id>-search/
    ├── worktree-for-codexspec-maintenance/
    └── worktree-for-codexspec-auto-dev/
```

Poursuivre une fonctionnalité réutilise son espace de travail. Les modifications
indépendantes de configuration, de constitution et de profil utilisent le
worktree de maintenance ; celles effectuées dans une fonctionnalité active y
restent. La configuration est **locale à chaque checkout** : un paramètre modifié
dans un worktree vers lequel l'opération a été routée y prend effet d'abord,
puis atteint les autres checkouts par intégration Git. Exécutez les commandes
CLI et les vérifications dans l'espace de travail renvoyé.

Les bases des nouvelles fonctionnalités comparent, selon l'ascendance Git,
l'historique committé de la branche principale locale avec celui de la branche
principale distante récupéré par fetch. Les historiques divergents sont
fusionnés dans le nouveau worktree et nécessitent une vérification. Un échec
de fetch produit un avertissement et autorise les références disponibles
localement ; les échecs de création ne se rabattent pas sur des écritures dans
le checkout principal.

`workflow.worktrees` vaut **true** par défaut ; seul le booléen YAML littéral
`false` désactive l'isolation des fonctionnalités ordinaires et de la maintenance.
Blueprint/auto-dev conservent leur worktree partagé fixe dans les deux cas.
L'initialisation et les mises à jour d'installation opèrent dans le checkout
que vous sélectionnez explicitement. Les worktrees terminés sont conservés ;
l'achèvement ne les fusionne ni ne les supprime automatiquement.

Consultez [Développement avec les worktrees](docs/en/user-guide/workflow.md#worktree-development)
et [configuration](docs/en/reference/configuration.md#workflowworktrees).

## Travailler avec du code existant

Deux points d'entrée répondent à des objectifs différents :

| Commande | Utilisation | Résultat/limite |
|---------|-----------|-----------------|
| `onboard [path]` | Amorcer les connaissances réutilisables du projet à partir d'une base de code existante | Conventions candidates et contraintes précisément étayées dans le profil ; le code reste en lecture seule |
| `reverse-spec [path]` | Comprendre l'architecture existante ou comparer le code à l'intention confirmée | Brouillons d'artefacts ou rapport de dérive ; le code reste en lecture seule |

```text
/codexspec:onboard src/
/codexspec:reverse-spec
/codexspec:reverse-spec src/auth
```

Onboard infère les conventions à partir du code observable et ne propose des
contraintes qu'à partir d'interdictions explicites. Les conventions candidates
prennent effet localement immédiatement ; les contraintes candidates nécessitent
une décision dans la session : conserver, modifier ou abandonner. Il préserve
les connaissances existantes et n'invente ni la justification de décisions
passées ni des pièges issus de l'expérience à partir d'un premier examen du code.

Reverse-spec propose trois modes :

- **Vue d'ensemble** : sans chemin, ou avec la racine du dépôt, produit un
  `design.md` architectural succinct et un `slices.md` pour choisir les modules à examiner.
- **Génération** : un chemin de module sans base confirmée produit des brouillons
  de `spec.md`, de `design.md` et des exigences ouvertes ou inférées.
- **Réconciliation** : un module avec une base confirmée produit `reconcile.md`,
  qui signale les comportements non documentés, les spécifications non implémentées
  et les divergences sémantiques par rapport aux spécifications et conceptions
  confirmées, les exigences faisant autorité sur l'intention.

Les brouillons inférés nécessitent une confirmation humaine avant de devenir
une base. La réconciliation indique la direction proposée — corriger le code,
mettre à jour les documents ou décider de l'intention — sans l'appliquer automatiquement.

## Revue et débogage

Quatre revues d'artefacts vérifient la fidélité, la couverture, la faisabilité
et la qualité interne : `review-spec`, `review-design`, `review-plan` et
`review-tasks`. Elles s'exécutent automatiquement après la génération et peuvent
aussi être invoquées manuellement. Les rapports distinguent les défauts vérifiés
des recommandations de risque non bloquantes et des possibilités de conception,
avec un score de compatibilité.

`review-code` fournit un contrôle de défauts distinct limité aux changements
ainsi qu'une évaluation explicite de la qualité de l'ensemble du code :

```text
/codexspec:review-code --feature <feature-dir>
/codexspec:review-code --uncommitted
/codexspec:review-code --audit src/
```

La revue par défaut couvre tous les changements de la branche de fonctionnalité,
y compris les changements committés, indexés, non indexés et non suivis qui ne
sont pas ignorés. Vous pouvez sélectionner explicitement des preuves committées,
non committées ou limitées à un seul commit. `--feature` joint le contexte des
exigences sans restreindre le périmètre Git. `--audit` évalue les chemins indiqués
et produit une grille consultative plutôt qu'un verdict d'achèvement.

Les revues chargent les standards partagés depuis `.codexspec/review-code/`,
en sélectionnant les dimensions de comportement et les contrôles de langage
ou de framework pertinents. Les constats nécessitent des preuves concrètes,
des déclencheurs atteignables, une attribution aux changements sélectionnés et
un impact. L'agent de revue signale les défauts et les suggestions de maintenance
étayées sans modifier les fichiers ; le processus chargé des corrections les
vérifie indépendamment.

L'implémentation commence par les tests pour les tâches de code et se fait
directement, avec les vérifications appropriées, pour la documentation et la
configuration. Après les corrections, une nouvelle revue incrémentale peut
réutiliser la couverture non affectée ; l'acceptation finale exige un nouveau
`PASS` sur la fonctionnalité complète, une couverture et une vérification
terminées et aucun défaut P0–P3 admis. Les suggestions de maintenance étayées
sont signalées séparément.

`workflow.auto_maintenance` vaut **true** par défaut et détermine si les processus
de correction appliquent aussi les améliorations de maintenance vérifiées et
compatibles. Le désactiver maintient le signalement de ces suggestions et ne
dispense ni de corriger les défauts ni d'effectuer les vérifications obligatoires.
Ce paramètre est distinct de la progression entre étapes et n'est pas un argument
pour `implement-tasks`.

Pour un débogage qui commence par la cause racine :

```text
/codexspec:debug Investigate intermittent failures when saving a task
```

Debug suit investigation → analyse des motifs récurrents → vérification d'une
hypothèse unique → correction précédée d'un test en échec. L'implémentation
recourt à cette discipline lorsque les corrections stagnent, qu'un défaut non trivial
affectant le bon fonctionnement nécessite un traçage ou que la même classe de cause racine
réapparaît au fil des revues. Trois corrections échouées déclenchent une
réévaluation architecturale.

Utilisez `checklist` pour évaluer la clarté, l'exhaustivité et la cohérence des exigences :

```text
/codexspec:checklist Check the authentication requirements for completeness
```

Consultez la [référence des commandes](docs/en/user-guide/commands.md) pour les
sélecteurs de revue, les arguments et les procédures détaillées.

## Connaissances du projet

Le profil du projet stocke les connaissances réutilisables dans `.codexspec/profile/` :

| Catégorie | Contenu |
|----------|----------|
| `constraints/` | Interdictions explicites et limites strictes, à lire en premier |
| `conventions/` | Motifs, nommage et consignes communes à plusieurs fonctionnalités |
| `pitfalls/` | Pièges rencontrés, causes, solutions de contournement et leçons |
| `decisions/` | Décisions architecturales et interfonctionnelles réutilisables |
| `strategies/` | Signaux appelant une autre approche de travail |
| `runbooks/` | Procédures ordonnées et reprise après échec |

`distill` capture les connaissances réutilisables issues du travail ; l'intention
propre à une fonctionnalité reste dans ses exigences, sa conception et son plan.
Init installe dans CLAUDE.md et/ou AGENTS.md des consignes pour lire toutes les
contraintes et les connaissances pertinentes avant tout travail substantiel.
Les connaissances ajoutées ultérieurement peuvent prendre effet sans nouvelle
initialisation. Les entrées candidates sont utilisées avec prudence ; les entrées
validées nécessitent une vérification des résultats et une approbation humaine.

```text
/codexspec:distill Capture the reusable lessons from this work
/codexspec:distill review
/codexspec:evolve
```

Une exécution manuelle de `distill review`, ou une invocation directe de `distill`
sans nouveau contenu à capturer, ouvre un espace de travail local et hors ligne
dans le navigateur. Vous pouvez réviser, valider, abandonner, différer et
consolider les entrées, prévisualiser le Markdown final, puis sélectionner
**Tout appliquer**. Les décisions restent dans un brouillon récupérable jusqu'à
leur application ; les contrôles de conflit empêchent une application partielle
ou un écrasement silencieux. Un mode texte explicite est disponible pour les
environnements sans navigateur.

`workflow.auto_distill` vaut **true** par défaut et contrôle trois hooks de fin :
`implement-tasks` terminé avec succès, commits exécutés via `commit-staged` et
génération de `pr`. L'aperçu d'un commit ne déclenche pas la capture.

Les consignes installées du projet demandent aussi aux agents de capturer les
connaissances réutilisables dès qu'elles apparaissent dans les conversations
ordinaires, les corrections hors SDD et les longues exécutions de `implement-tasks`.
Ces consignes s'appliquent indépendamment du paramètre de fin ; la capture en
fin de tâche constitue une dernière protection.

Dans une session, les déclenchements répétés ne traitent que le nouveau contenu.
Entre les sessions, `distill` lit le profil et ignore les connaissances déjà
couvertes. La capture se termine sans écrire lorsqu'il ne reste rien de
réutilisable. La capture automatique n'ouvre jamais la revue manuelle,
n'attend jamais un humain et ne bloque jamais le flux qui l'invoque.

`evolve` ne sélectionne que les connaissances validées utiles au-delà du projet,
compile un brouillon de commande ou de compétence et obtient une approbation
explicite avant un push ou l'ouverture d'une PR de contribution soumise à revue humaine.

Consultez [Connaissances du projet](docs/en/user-guide/commands.md#codexspecdistill)
pour les consignes détaillées.

### Réutiliser les décisions historiques

L'historique pertinent dans `.codexspec/specs/` est aussi consulté avant tout
jugement substantiel sur les exigences, la conception, l'implémentation, le
débogage ou la revue, dans les conversations ordinaires comme dans les flux SDD.
Les agents reconstituent les décisions inchangées, les ajouts ultérieurs et les
remplacements explicites avant d'interroger l'utilisateur.

Les anciennes exigences inchangées restent applicables. La dernière décision
explicite de l'utilisateur prévaut toujours ; les propositions ouvertes ne sont
pas considérées comme une intention confirmée. La recherche se limite à la
tâche et le contexte suffisant est réutilisé. Actualisez les installations des
projets existants pour recevoir ces consignes.

## Flux de travail Git

```text
/codexspec:commit-staged -p
/codexspec:pr --spec <feature-dir>/spec.md
/codexspec:release-notes --from <ref> --to HEAD
/codexspec:tasks-to-issues <feature-dir>
```

- **commit-staged** analyse exactement la zone de préparation de l'index et génère
  un message Conventional Commits ; `-p` affiche un aperçu sans créer de commit.
  Le flux appelant choisit et indexe les fichiers. L'exécution autorisée utilise
  l'environnement d'exécution protégé et revérifie que le contenu committé
  correspond à l'analyse. Les consignes de commit pour l'agent s'appliquent dans
  les conversations ordinaires et les flux SDD, blueprint et auto-dev ; la seule
  disponibilité de la commande ne l'invoque pas et n'autorise pas de commit.
- **pr** génère une description structurée de PR GitHub ou de MR GitLab à partir
  du diff. `--spec` ajoute facultativement le contexte de la fonctionnalité depuis
  un chemin de fichier `spec.md`, ou un nom ou préfixe de dossier de fonctionnalité
  résolu vers ce fichier. La sortie par défaut est du texte destiné à la
  plateforme d'hébergement.
- **release-notes** dérive une entrée Keep a Changelog et le corps d'une publication
  à partir de l'historique Git. La section par défaut est `[Unreleased]` ;
  `--version` utilise un libellé fourni. Il n'indexe rien, ne crée pas de commit,
  n'incrémente pas les versions, ne crée pas de tag, ne publie rien et ne crée pas de release.
- **tasks-to-issues** crée des issues GitHub à partir de tâches existantes, avec
  les dépendances et les critères d'acceptation. Il nécessite une CLI GitHub
  authentifiée et vérifie que le dépôt des issues correspond au distant configuré.

L'aperçu direct des commits et les commits autorisés sur place nécessitent
Python 3.11+ et Git ; l'environnement d'exécution est installé avec les projets
CLI et inclus dans le plugin Claude. Les fusions créées par l'agent qui modifient
le contenu utilisent aussi l'analyse des changements indexés. Les fusions qui
ne font que relier les historiques conservent le message par défaut de Git tout
en validant l'arbre et les parents ; les avances rapides ne créent aucun commit.

## Commandes disponibles

La CLI comprend six commandes publiques. Les intégrations d'agents distribuent
28 commandes : Claude utilise `/codexspec:<name>` et Codex utilise `$codexspec:<name>`.
Les tableaux ci-dessous utilisent la notation de Claude pour faciliter la lecture.

### Commandes CLI

| Commande | Objectif |
|---------|---------|
| `codexspec init` | Initialiser ou actualiser un projet pour Claude, Codex ou les deux |
| `codexspec check` | Vérifier les outils et dépendances installés |
| `codexspec version` | Afficher la version et les informations système |
| `codexspec config` | Afficher ou modifier la configuration du projet |
| `codexspec list-commands` | Lister les commandes d'agent disponibles par catégorie |
| `codexspec show-blueprint` | Afficher le blueprint du worktree partagé sans le modifier |

### Commandes du flux de travail principal

| Commande | Objectif |
|---------|---------|
| `/codexspec:constitution` | Créer/mettre à jour les principes du projet avec validation entre artefacts |
| `/codexspec:specify` | Discuter, confirmer et enregistrer les exigences d'une fonctionnalité |
| `/codexspec:blueprint` | Préparer ou maintenir les exigences confirmées en attente du blueprint |
| `/codexspec:generate-spec` | Compiler les exigences confirmées en une spécification traçable ; revue automatique |
| `/codexspec:spec-to-design` | Définir l'architecture, les composants, les interfaces et les décisions ; revue automatique |
| `/codexspec:design-to-plan` | Planifier les phases d'implémentation, leur ordre et la vérification ; revue automatique |
| `/codexspec:plan-to-tasks` | Produire des tâches vérifiables couvrant les artefacts en amont ; revue automatique et analyze |
| `/codexspec:implement-tasks` | Exécuter les tâches, vérifier les résultats, effectuer les revues et corrections |
| `/codexspec:auto-dev` | Développer de façon autonome les exigences confirmées du blueprint dans l'ordre du document |

### Commandes de revue des artefacts

| Commande | Objectif |
|---------|---------|
| `/codexspec:review-spec` | Vérifier la fidélité et la qualité interne de la spécification |
| `/codexspec:review-design` | Vérifier la fidélité, la faisabilité et l'aptitude de la conception à passer à la planification |
| `/codexspec:review-plan` | Vérifier la fidélité, la faisabilité et l'aptitude du plan à passer à l'implémentation |
| `/codexspec:review-tasks` | Vérifier la fidélité, les dépendances, le caractère exécutable et la vérification des tâches |

### Exigences, code existant et débogage

| Commande | Objectif |
|---------|---------|
| `/codexspec:clarify` | Résoudre les ambiguïtés des exigences, en les mettant à jour avant la spécification |
| `/codexspec:analyze` | Vérifier la traçabilité de bout en bout et aligner les artefacts en aval sur l'autorité |
| `/codexspec:checklist` | Générer une liste de contrôle de la qualité des exigences |
| `/codexspec:tasks-to-issues` | Convertir les tâches existantes en issues GitHub exploitables |
| `/codexspec:debug` | Rechercher les causes racines avant d'appliquer une correction |
| `/codexspec:reverse-spec` | Examiner l'architecture existante, rédiger des artefacts de modules ou signaler une dérive par rapport à la base |

### Commandes de connaissances du projet

| Commande | Objectif |
|---------|---------|
| `/codexspec:distill` | Capturer des connaissances réutilisables ou examiner les candidats dans l'espace de travail local |
| `/codexspec:evolve` | Compiler les connaissances validées en un brouillon de contribution au projet amont |
| `/codexspec:onboard` | Amorcer des conventions candidates et des contraintes étayées à partir du code existant |

### Commandes Git et de revue du code

| Commande | Objectif |
|---------|---------|
| `/codexspec:commit-staged` | Générer des messages à partir des changements indexés ; prévisualiser ou exécuter un commit autorisé |
| `/codexspec:pr` | Générer une description structurée de PR/MR |
| `/codexspec:release-notes` | Maintenir une entrée du journal des changements et générer le corps d'une publication depuis l'historique Git |
| `/codexspec:review-code` | Examiner les changements sélectionnés comme contrôle de défauts ; utiliser `--audit` pour évaluer la qualité du code dans les chemins indiqués |

### Commandes utilitaires

| Commande | Objectif |
|---------|---------|
| `/codexspec:config` | Créer/afficher/modifier/réinitialiser interactivement la configuration du projet |
| `/codexspec:quick` | Exécuter un flux SDD compact qui donne la priorité aux exigences pour les petits changements |

## Configuration et internationalisation

La configuration se trouve dans `.codexspec/config.yml`. Les modèles restent
en anglais ; les agents rédigent les échanges et les artefacts générés dans
les langues configurées. Les 13 codes de langue standard sont `en`, `zh-CN`,
`zh-TW`, `ja`, `ko`, `es`, `fr`, `de`, `pt`, `ru`, `it`, `ar` et `hi`.
Le code portugais de la CLI est `pt` ; la documentation localisée et les
catalogues de traduction utilisent `pt-BR`.

### Dimensions linguistiques

| Dimension | Clé de configuration | À l'initialisation | Modifier ensuite | Contrôle |
|-----------|------------|-------------------|-----------|----------|
| Sortie/base | `language.output` | `--lang` | `config --set-lang` | Langue de repli pour les autres dimensions linguistiques |
| Échanges | `language.interaction` | `--interaction-lang` | `config --set-interaction-lang` | Conversation et sortie de la CLI |
| Document | `language.document` | `--document-lang` | `config --set-document-lang` | Exigences, spécifications, conceptions, plans et tâches |
| Commit | `language.commit` | `--commit-lang` | `config --set-commit-lang` | Messages de commit et contenu de livraison via Git |

Chaque langue spécifique se replie indépendamment sur `language.output`, puis
sur `en`. `language.templates` reste à `en`.

```bash
codexspec init my-project --ai both \
  --interaction-lang zh-CN --document-lang en --commit-lang en

codexspec config
codexspec config --set-document-lang en
codexspec config --list-langs
```

La première initialisation en TTY demande la langue de base, sauf si vous
fournissez `--lang` ou les trois options de langue spécifiques. `--force`
confirme automatiquement les autres demandes d'initialisation ; il ne supprime
pas cette sélection de langue. L'initialisation hors TTY utilise l'anglais par
défaut. Une nouvelle initialisation préserve les clés de langue que vous
n'avez pas explicitement définies.

### Paramètres de flux de travail et de revue

| Paramètre | Valeur par défaut | Effet | Commande CLI |
|---------|---------|--------|-------------|
| `workflow.auto_next` | `false` | Faire avancer les étapes SDD ordinaires validées | `config --auto-next on\|off` |
| `workflow.auto_distill` | `true` | Capture non interactive des connaissances après une conclusion réussie | `config --auto-distill on\|off` |
| `workflow.auto_maintenance` | `true` | Appliquer une maintenance incrémentale vérifiée pendant les corrections automatiques | `config --auto-maintenance on\|off` |
| `workflow.worktrees` | `true` | Isoler les fonctionnalités ordinaires et la maintenance indépendante | `config --worktrees on\|off` |
| `review.decided_by` | `reviewer` | Qui décide des constats déclenchés hors du contexte opérationnel du projet | `config --decided-by reviewer\|ask` |

Les options booléennes de la CLI acceptent `on/true/1/yes` et `off/false/0/no`
sans distinction de casse, y compris avec des espaces autour de la valeur.
Une option booléenne sans valeur inverse la valeur actuelle du checkout de
destination ; les valeurs stockées en YAML sont des booléens.

Avec `review.decided_by: reviewer`, l'agent de revue décide de l'admission des défauts.
Avec `ask`, un déclencheur hors contexte devient une décision de scénario en
attente : l'utilisateur décide une fois de corriger le problème ou d'exclure
ce scénario, et la décision confirmée est conservée pour les revues suivantes.
Les décisions en attente bloquent l'achèvement. Une exécution de `review-code`
peut remplacer le mode configuré avec `--decided-by`.

Les écritures de configuration suivent le routage des worktrees. Une modification
indépendante depuis le checkout principal s'effectue dans le worktree de
maintenance et ne modifie pas immédiatement le paramètre effectif du principal ;
les changements dans un worktree de fonctionnalité y prennent effet.

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
| `--force`, `-f` | Régénérer les artefacts installés et confirmer automatiquement les demandes de migration/mise à jour/conformité ; préserver le contexte rédigé pour le projet et les paramètres sans rapport |
| `--no-git` | Ne pas initialiser le dépôt Git |
| `--debug`, `-d` | Afficher les informations de débogage détaillées |

</details>

<details>
<summary>Options de configuration de la CLI</summary>

| Option | Signification |
|--------|---------|
| `--set-lang`, `-l` | Définir la langue de sortie de base |
| `--set-interaction-lang` | Définir la langue des échanges |
| `--set-document-lang` | Définir la langue des documents |
| `--set-commit-lang`, `-c` | Définir la langue des messages de commit |
| `--list-langs` | Lister les codes de langue pris en charge |
| `--auto-next` | Inverser/définir la progression automatique entre étapes |
| `--auto-distill` | Inverser/définir la capture automatique des connaissances |
| `--auto-maintenance` | Inverser/définir la maintenance incrémentale automatique |
| `--worktrees` | Inverser/définir l'isolation par worktree locale au checkout |
| `--decided-by` | Définir le mode de décision de revue `reviewer` ou `ask` |

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
[Internationalisation](docs/en/user-guide/i18n.md) pour le comportement détaillé
des langues et des paramètres.

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

Le blueprint partagé se trouve dans le worktree dédié à auto-dev, plutôt que
dans une copie modifiable distincte dans chaque checkout ordinaire. Les
brouillons de revue manuelle des connaissances sont exclus de Git.

## Ressources pour les extensions

Le dépôt comprend un modèle de manifeste d'extension, un exemple de commande
et un [Guide de développement des extensions](extensions/EXTENSION-DEVELOPMENT-GUIDE.md).
Ce sont des ressources de création. La CLI actuelle ne propose pas de commandes
pour installer, lister ou supprimer les extensions et ne charge pas automatiquement
les commandes ou hooks de `extension.yml`. Les ressources de revue partagées
permettent des ajouts propres au projet dans `.codexspec/review-code/` ;
l'initialisation conserve les modifications existantes des ressources et les
fichiers supplémentaires, sauf si leur remplacement est demandé.

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

Lisez [CLAUDE.md](CLAUDE.md), [AGENTS.md](AGENTS.md) et
[Organisation du dépôt](docs/internal/repository-layout.md) avant de modifier
les modèles, le packaging ou l'initialisation. Les copies des commandes et
compétences distribuées sont des artefacts d'installation générés ; modifiez
leurs sources faisant autorité et régénérez-les.

## Contribuer

Consultez le [guide de contribution](docs/en/development/contributing.md) pour
la configuration locale et les consignes de contribution. Les contributions
doivent préserver les exigences confirmées, la traçabilité des sources et la
frontière du packaging entre utilisateurs et mainteneurs.

## Licence

MIT — voir [LICENSE](LICENSE).

## Remerciements

Inspiré de [GitHub spec-kit](https://github.com/github/spec-kit).
S'intègre à Claude Code et OpenAI Codex.

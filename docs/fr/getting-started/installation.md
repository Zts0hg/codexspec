<a id="installation"></a>

# Installation

<a id="install-with-the-codex-desktop-app"></a>

## Installer depuis l'application de bureau Codex

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

<a id="prerequisites"></a>

## Prérequis

- Python 3.11+
- [uv](https://docs.astral.sh/uv/) (recommandé) ou pip
- L'assistant que vous souhaitez utiliser : Claude Code ou Codex
- Git pour le développement avec les worktrees et les flux de travail Git

<a id="cli-installation"></a>

## Installation de la CLI

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

<a id="one-time-initialization"></a>

### Initialisation ponctuelle

```bash
uvx codexspec init my-project --ai claude
uvx codexspec init . --ai codex
```

L'initialisation ponctuelle installe les commandes du projet et l'environnement
d'exécution autonome pour les commits. Le routage des worktrees, les flux
blueprint/auto-dev et la revue manuelle du profil continuent d'utiliser la CLI
CodexSpec ; veillez à la rendre disponible pour ces flux de travail.

<a id="development-versions"></a>

### Versions de développement

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

Le [Guide de résolution des problèmes sous Windows](../WINDOWS-TROUBLESHOOTING.md)
explique comment résoudre les problèmes de PATH et d'installation.

</details>

<a id="upgrade-and-refresh-a-project"></a>

## Mettre à jour CodexSpec et les fichiers du projet

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

<a id="plugin-marketplace-installation"></a>

## Installation depuis le marketplace de plugins

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

Consultez [Installation](installation.md) pour la procédure complète.

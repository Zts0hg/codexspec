# Référence de la CLI

<a id="cli-commands"></a>

## Commandes CLI

| Commande | Objectif |
|---------|---------|
| `codexspec init` | Initialiser ou actualiser un projet pour Claude, Codex ou les deux |
| `codexspec check` | Vérifier les outils et dépendances installés |
| `codexspec version` | Afficher la version et les informations système |
| `codexspec config` | Consulter ou modifier la configuration du projet |
| `codexspec list-commands` | Afficher les commandes d'agent disponibles par catégorie |
| `codexspec show-blueprint` | Afficher le blueprint du worktree partagé sans le modifier |

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

## `codexspec show-blueprint`

Affiche le fichier `.codexspec/blueprint.md` complet de la branche fixe `codexspec/auto-dev` et de
`worktree-for-codexspec-auto-dev` directement sur la sortie standard. Si le dépôt, la branche, le worktree ou le fichier manque, un diagnostic est envoyé
sur la sortie d’erreur et la commande se termine avec un code de sortie non nul. La commande est en lecture seule et
n'effectue aucun fetch, merge, verrouillage ou écriture.

```bash
codexspec show-blueprint
```

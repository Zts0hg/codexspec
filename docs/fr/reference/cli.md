# Référence CLI

## Commandes

### `codexspec show-blueprint`

Affiche le fichier `.codexspec/blueprint.md` complet de la branche fixe `codexspec/auto-dev` et de
`worktree-for-codexspec-auto-dev` directement sur la sortie standard. Les prérequis absents sont
signalés sur la sortie d'erreur avec un état non nul. La commande est en lecture seule et
n'effectue aucun fetch, merge, verrouillage ou écriture.

```bash
codexspec show-blueprint
```

---

### `codexspec init`

Initialise un nouveau projet CodexSpec.

```bash
codexspec init [PROJECT_NAME] [OPTIONS]
```

**Arguments :**

| Argument | Description |
|----------|-------------|
| `PROJECT_NAME` | Nom du nouveau répertoire de projet (utilisez `.` ou `--here` pour le répertoire courant) |

**Options :**

| Option | Raccourci | Description |
|--------|-----------|-------------|
| `--here` | `-h` | Initialiser dans le répertoire courant |
| `--ai` | `-a` | Assistant AI à utiliser : `claude`, `codex` ou `both` (par défaut : claude) |
| `--lang` | `-l` | Langue de sortie (base) ; interaction/document/commit s'y rapportent (ex. en, zh-CN, ja) |
| `--interaction-lang` | | Langue d'interaction (dialogue LLM + sortie CLI `codexspec`) ; surcharge `--lang` |
| `--document-lang` | | Langue des documents (exigences/spec/plan/tasks générés) ; surcharge `--lang` |
| `--commit-lang` | | Langue des messages de commit ; surcharge `--lang` |
| `--force` | `-f` | Écraser les fichiers existants et confirmer automatiquement les invites ; ne régénère jamais `config.yml` |
| `--no-git` | | Passer l'initialisation du dépôt git |
| `--debug` | `-d` | Activer la sortie de débogage |

`--lang` définit la langue de base `output` ; `--interaction-lang`, `--document-lang` et `--commit-lang` la surchargent pour leur dimension (chacune se rabat sur `output`, puis sur `en`). Voir [Internationalisation](../user-guide/i18n.md) pour le modèle complet.

La première initialisation dans un TTY sans `--lang` (et sans les trois indicateurs de dimension) demande une langue de base ; dans un environnement non-TTY (CI/scripts) elle utilise `en` par défaut — **entièrement non interactive**. Relancer `init` préserve toute clé de langue que vous n'avez pas explicitement fournie ; `--force` ne régénère jamais `config.yml`.

**Exemples :**

```bash
# Créer un nouveau projet
codexspec init my-project

# Initialiser dans le répertoire courant
codexspec init . --ai claude

# Usage ponctuel (sans installation) — initialiser pour Codex CLI ou les deux
uvx codexspec init . --ai codex
uvx codexspec init . --ai both

# Entièrement non interactif : base zh-CN, messages de commit en anglais
codexspec init my-project --lang zh-CN --commit-lang en

# Définir chaque dimension explicitement (scriptable, sans invite)
codexspec init my-project \
  --interaction-lang zh-CN --document-lang en --commit-lang en
```

`codexspec init` installe les ressources de revue communes à Claude Code et Codex dans `.codexspec/review-code/`. `--force` actualise les ressources distribuées et préserve les extensions ayant d’autres chemins. L’installation de la CLI seule ne crée aucun fichier de projet. Avec le plugin seul, sans arborescence installée dans le projet, la revue utilise les mêmes ressources depuis la racine résolue par l’hôte.

---

### `codexspec check`

Vérifie les outils installés.

```bash
codexspec check
```

---

### `codexspec version`

Affiche les informations de version.

```bash
codexspec version
```

---

### `codexspec config`

Affiche ou modifie la configuration du projet.

```bash
codexspec config [OPTIONS]
```

**Options :**

| Option | Raccourci | Description |
|--------|-----------|-------------|
| `--set-lang` | `-l` | Définir la langue de sortie (base) |
| `--set-interaction-lang` | | Définir la langue d'interaction (dialogue LLM + sortie CLI) |
| `--set-document-lang` | | Définir la langue des documents (spec/plan/tasks générés) |
| `--set-commit-lang` | `-c` | Définir la langue des messages de commit |
| `--list-langs` | | Lister toutes les langues prises en charge |
| `--auto-next` | | Basculer/définir `workflow.auto_next` (à nu bascule ; ou on/off) |
| `--auto-maintenance` |  | Basculer/définir `workflow.auto_maintenance` (on par défaut ; sans valeur = bascule ; ou on/off) |
| `--decided-by` | | Définir `review.decided_by` sur `reviewer` (par défaut) ou `ask` |

Chaque `--set-*-lang` met à jour une [dimension de langue](../user-guide/i18n.md) ; toute dimension que vous ne définissez pas se rabat sur `output`, puis sur `en`.

`codexspec config --auto-maintenance on|off` enregistre `workflow.auto_maintenance` comme booléen YAML dans `.codexspec/config.yml` ; une clé absente vaut `true`. Les deux options acceptent `on/true/1/yes` et `off/false/0/no` sans distinction de casse. `implement-tasks` lit ce réglage lors des corrections automatiques : `on` inclut les améliorations progressives de maintenance étayées ; `off` continue de les signaler. Les défauts réels et les vérifications nécessaires restent obligatoires. Ce réglage est indépendant d’`auto-next` et n’est pas un paramètre d’appel d’`implement-tasks`.

```bash
codexspec config --auto-maintenance on
codexspec config --auto-maintenance off
```

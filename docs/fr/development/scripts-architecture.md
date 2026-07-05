# Analyse de l'architecture des scripts

Ce document détaille la logique de code des scripts dans le projet CodexSpec et la façon dont ils sont utilisés dans Claude Code.

## 1. Vue d'ensemble de l'architecture

CodexSpec est une boîte à outils **Spec-Driven Development (SDD)** qui adopte une architecture en trois couches : CLI + modèles + scripts auxiliaires.

```
┌─────────────────────────────────────────────────────────────────┐
│                        Couche utilisateur (CLI)                  │
│  codexspec init | check | version | config                      │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                    Couche d'interaction Claude Code              │
│  /codexspec:specify | /codexspec:analyze | ...                  │
│  (.claude/commands/*.md)                                        │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                      Couche des scripts auxiliaires              │
│  .codexspec/scripts/*.sh (Bash) ou *.ps1 (PowerShell)          │
└─────────────────────────────────────────────────────────────────┘
```

## 2. Flux de déploiement des scripts

### Étape 1 : initialisation par `codexspec init`

Dans la fonction `init()` de `src/codexspec/__init__.py` (lignes 343-368), les scripts appropriés sont copiés automatiquement selon le système d'exploitation :

```python
# Copy helper scripts based on platform
scripts_source_dir = get_scripts_dir()
if scripts_source_dir.exists():
    if sys.platform == "win32":
        # Windows : copier les scripts PowerShell
        ps_scripts = scripts_source_dir / "powershell"
        for script_file in ps_scripts.glob("*.ps1"):
            dest_file = codexspec_dir / "scripts" / script_file.name
            dest_file.write_text(script_file.read_text(encoding="utf-8"), encoding="utf-8")
    else:
        # macOS/Linux : copier les scripts Bash
        bash_scripts = scripts_source_dir / "bash"
        for script_file in bash_scripts.glob("*.sh"):
            dest_file = codexspec_dir / "scripts" / script_file.name
            dest_file.write_text(script_file.read_text(encoding="utf-8"), encoding="utf-8")
```

**Résultat** : selon le système d'exploitation, les scripts de `scripts/bash/` ou `scripts/powershell/` sont copiés dans le répertoire `.codexspec/scripts/` du projet.

### Mécanisme de résolution des chemins

La fonction `get_scripts_dir()` (lignes 71-90) gère plusieurs scénarios d'installation :

```python
def get_scripts_dir() -> Path:
    # Path 1: Wheel install - scripts packaged inside codexspec package
    installed_scripts = Path(__file__).parent / "scripts"
    if installed_scripts.exists():
        return installed_scripts

    # Path 2: Development/editable install - scripts in project root
    dev_scripts = Path(__file__).parent.parent.parent / "scripts"
    if dev_scripts.exists():
        return dev_scripts

    # Path 3: Fallback
    return installed_scripts
```

## 3. Mécanisme d'appel des scripts depuis Claude Code

### Mécanisme central : déclaration YAML frontmatter

Les fichiers modèles déclarent leurs dépendances de scripts via le YAML frontmatter :

```yaml
---
description: Description de la commande
scripts:
  sh: .codexspec/scripts/check-prerequisites.sh --json --require-tasks --include-tasks
  ps: .codexspec/scripts/check-prerequisites.ps1 -Json -RequireTasks -IncludeTasks
---
```

### Remplacement de l'espace réservé

Le placeholder `{SCRIPT}` est utilisé dans les modèles :

```markdown
### 1. Initialize Context

Run `{SCRIPT}` from repo root and parse JSON for:
- `FEATURE_DIR` - Chemin du répertoire de fonctionnalité
- `AVAILABLE_DOCS` - Liste des documents disponibles
```

### Flux d'appel

1. L'utilisateur saisit `/codexspec:analyze` dans Claude Code
2. Claude lit le modèle `.claude/commands/codexspec:analyze.md`
3. Selon le système d'exploitation, Claude remplace `{SCRIPT}` par :
   - **macOS/Linux** : `.codexspec/scripts/check-prerequisites.sh --json --require-tasks --include-tasks`
   - **Windows** : `.codexspec/scripts/check-prerequisites.ps1 -Json -RequireTasks -IncludeTasks`
4. Claude exécute le script, analyse la sortie JSON et poursuit les opérations

## 4. Détail des fonctionnalités des scripts

### 4.1 `check-prerequisites.sh/ps1` — script de vérification préalable

C'est le script le plus important ; il valide l'état de l'environnement et renvoie des informations structurées.

#### Fonctionnalités principales

- Vérifie que l'on se trouve sur une branche feature (format : `2026-0613-1200ab-feature-name`)
- Détecte la présence des fichiers requis (`plan.md`, `tasks.md`)
- Renvoie les informations de chemin au format JSON

#### Options des paramètres

| Paramètre | Bash | PowerShell | Rôle |
|-----------|------|------------|------|
| Sortie JSON | `--json` | `-Json` | Sortie au format JSON |
| Exiger tasks.md | `--require-tasks` | `-RequireTasks` | Vérifie l'existence de tasks.md |
| Inclure tasks.md | `--include-tasks` | `-IncludeTasks` | Inclut tasks.md dans AVAILABLE_DOCS |
| Chemins uniquement | `--paths-only` | `-PathsOnly` | Saute la validation, ne sort que les chemins |

#### Exemple de sortie JSON

```json
{
  "FEATURE_DIR": "/path/to/.codexspec/specs/2026-0613-1200ab-my-feature",
  "AVAILABLE_DOCS": ["research.md", "data-model.md", "tasks.md"]
}
```

### 4.2 `common.sh/ps1` — fonctions utilitaires générales

Fournit des fonctionnalités génériques multi-plateformes.

#### Fonctions de la version Bash

| Fonction | Rôle |
|----------|------|
| `get_feature_id()` | Récupère le feature ID depuis la branche Git ou une variable d'environnement |
| `get_specs_dir()` | Renvoie le chemin du répertoire specs |
| `is_codexspec_project()` | Vérifie que l'on est dans un projet CodexSpec |
| `require_codexspec_project()` | Garantit que l'on est dans un projet CodexSpec, sinon quitte |
| `log_info/success/warning/error()` | Sortie de journal colorée |
| `command_exists()` | Vérifie l'existence d'une commande |

#### Fonctions de la version PowerShell

| Fonction | Rôle |
|----------|------|
| `Get-RepoRoot` | Renvoie la racine du dépôt Git |
| `Get-CurrentBranch` | Renvoie le nom de la branche courante |
| `Test-HasGit` | Détecte la présence d'un dépôt Git |
| `Test-FeatureBranch` | Vérifie que l'on est sur une branche feature |
| `Get-FeaturePathsEnv` | Renvoie tous les chemins liés à la feature |
| `Test-FileExists` | Vérifie l'existence d'un fichier |
| `Test-DirHasFiles` | Vérifie qu'un répertoire contient des fichiers |

### 4.3 `create-new-feature.sh/ps1` — créer une nouvelle fonctionnalité

#### Fonctionnalités

- Génère automatiquement un feature ID au format `YYYY-MMDD-HHMMxx`
- Crée le répertoire de feature et un `requirements.md` initial
- Crée la branche Git correspondante
- Exige que le nom court nettoyé contienne au moins une lettre ou un chiffre ASCII

#### Exemple d'utilisation

```bash
./create-new-feature.sh -n "user authentication"
```

#### Contrat de nommage des features

- Les identifiants séquentiels `NNN-name` ne sont pas pris en charge. Seuls les noms à horodatage sont autorisés.
- La compatibilité héritée s'applique aux artefacts : un `spec.md` existant peut être utilisé en l'absence de `requirements.md`. Cela ne valide aucun autre format de nommage de répertoire ou de branche.
- Le nom complet identifie un espace de travail : `YYYY-MMDD-HHMMxx-short-name`. Des espaces de travail créés indépendamment peuvent partager le même ID d'horodatage si leurs noms courts diffèrent.
- La résolution par short-ID n'est qu'une commodité locale. Si plusieurs répertoires correspondent, la résolution signale une ambiguïté plutôt que de sélectionner ou d'écraser un espace de travail.

## 5. Commandes utilisant les scripts

Les 4 commandes suivantes ont recours aux scripts :

| Commande | Paramètres des scripts | Rôle |
|----------|------------------------|------|
| `/codexspec:clarify` | `--json --paths-only` | Récupère les chemins sans valider les fichiers |
| `/codexspec:checklist` | `--json` | Vérifie l'existence de plan.md |
| `/codexspec:analyze` | `--json --require-tasks --include-tasks` | Vérifie plan.md + tasks.md |
| `/codexspec:tasks-to-issues` | `--json --require-tasks --include-tasks` | Vérifie plan.md + tasks.md |

## 6. Diagramme de flux complet

```
┌──────────────────────────────────────────────────────────────────────────┐
│                        Phase d'initialisation                            │
│                                                                          │
│  $ codexspec init my-project                                             │
│       │                                                                  │
│       ├── Crée la structure de répertoires .codexspec/                   │
│       ├── Copie scripts/*.sh → .codexspec/scripts/                       │
│       ├── Copie templates/commands/*.md → .claude/commands/              │
│       └── Crée constitution.md, config.yml, CLAUDE.md                    │
│                                                                          │
└──────────────────────────────────────────────────────────────────────────┘
                                    ↓
┌──────────────────────────────────────────────────────────────────────────┐
│                        Phase d'utilisation (Claude Code)                  │
│                                                                          │
│  Utilisateur : /codexspec:analyze                                        │
│       │                                                                  │
│       ├── Claude lit .claude/commands/codexspec:analyze.md              │
│       │                                                                  │
│       ├── Analyse la déclaration scripts du YAML frontmatter             │
│       │   scripts:                                                       │
│       │     sh: .codexspec/scripts/check-prerequisites.sh --json ...     │
│       │                                                                  │
│       ├── Remplace le placeholder {SCRIPT}                               │
│       │                                                                  │
│       ├── Exécute le script :                                            │
│       │   $ .codexspec/scripts/check-prerequisites.sh --json ...         │
│       │                                                                  │
│       ├── Analyse la sortie JSON :                                       │
│       │   {"FEATURE_DIR": "...", "AVAILABLE_DOCS": [...]}                │
│       │                                                                  │
│       ├── Lit spec.md, plan.md, tasks.md                                │
│       │                                                                  │
│       └── Génère le rapport d'analyse                                    │
│                                                                          │
└──────────────────────────────────────────────────────────────────────────┘
```

## 7. Atouts de conception

### 7.1 Compatibilité multi-plateformes

Les versions Bash et PowerShell sont maintenues simultanément, avec sélection automatique via `sys.platform` :

```python
if sys.platform == "win32":
    # Copier les scripts PowerShell
else:
    # Copier les scripts Bash
```

### 7.2 Configuration déclarative

Les dépendances de scripts sont déclarées via le YAML frontmatter, ce qui reste clair et intuitif :

```yaml
scripts:
  sh: .codexspec/scripts/check-prerequisites.sh --json
  ps: .codexspec/scripts/check-prerequisites.ps1 -Json
```

### 7.3 Sortie JSON

Les scripts produisent des données structurées faciles à analyser par Claude :

```json
{
  "FEATURE_DIR": "/path/to/.codexspec/specs/2026-0613-1200ab-feature",
  "AVAILABLE_DOCS": ["research.md", "data-model.md"]
}
```

### 7.4 Validation progressive

Différentes commandes utilisent différents paramètres, et valident selon leurs besoins :

| Étape | Commande | Niveau de validation |
|-------|----------|----------------------|
| Avant planification | `/codexspec:clarify` | Chemins uniquement |
| Après planification | `/codexspec:checklist` | plan.md |
| Après tâches | `/codexspec:analyze` | plan.md + tasks.md |

### 7.5 Intégration Git

- Extraction automatique du feature ID depuis le nom de branche
- Prise en charge de la validation du nommage de branche (format `^\d{3}-`)
- Prise en charge de la surcharge par variable d'environnement (`CODEXSPEC_FEATURE`)

## 8. Chemins de code clés

| Fichier | Lignes/position | Rôle |
|---------|-----------------|------|
| `src/codexspec/__init__.py` | 343-368 | Logique de copie des scripts |
| `src/codexspec/__init__.py` | 71-90 | Résolution de chemin `get_scripts_dir()` |
| `scripts/bash/check-prerequisites.sh` | tout le fichier | Script Bash principal de vérification préalable |
| `scripts/powershell/check-prerequisites.ps1` | 56-146 | Script PowerShell de vérification préalable |
| `scripts/bash/common.sh` | tout le fichier | Fonctions utilitaires Bash |
| `scripts/powershell/common.ps1` | tout le fichier | Fonctions utilitaires PowerShell |
| `templates/commands/*.md` | YAML frontmatter | Déclaration des scripts |

## 9. Inventaire des fichiers de scripts

### Scripts Bash (`scripts/bash/`)

```
scripts/bash/
├── check-prerequisites.sh   # Script principal de vérification préalable
├── common.sh                # Fonctions utilitaires générales
└── create-new-feature.sh    # Création d'une nouvelle fonctionnalité
```

### Scripts PowerShell (`scripts/powershell/`)

```
scripts/powershell/
├── check-prerequisites.ps1  # Script principal de vérification préalable
├── common.ps1               # Fonctions utilitaires générales
└── create-new-feature.ps1   # Création d'une nouvelle fonctionnalité
```

---

*Ce document décrit l'architecture complète et le flux d'utilisation des scripts dans le projet CodexSpec. En cas de mise à jour, merci de le modifier en conséquence.*

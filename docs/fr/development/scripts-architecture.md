# Analyse de l'Architecture des Scripts

Ce document detaille le flux logique du code des scripts dans le projet CodexSpec et comment ils sont utilises dans Claude Code.

## 1. Apercu de l'Architecture Globale

CodexSpec est une boite a outils **Spec-Driven Development (SDD)** adoptant une architecture a trois couches : CLI + modeles + scripts auxiliaires.

```
+-----------------------------------------------------------------+
|                        Couche Utilisateur (CLI)                  |
|  codexspec init | check | version | config                       |
+-----------------------------------------------------------------+
                              |
+-----------------------------------------------------------------+
|                    Couche d'Interaction Claude Code              |
|  /codexspec.specify | /codexspec.analyze | ...                  |
|  (.claude/commands/*.md)                                        |
+-----------------------------------------------------------------+
                              |
+-----------------------------------------------------------------+
|                      Couche Scripts Auxiliaires                  |
|  .codexspec/scripts/*.sh (Bash) ou *.ps1 (PowerShell)          |
+-----------------------------------------------------------------+
```

## 2. Flux de Deploiement des Scripts

### Etape 1 : Initialisation `codexspec init`

Dans la fonction `init()` de `src/codexspec/__init__.py` (lignes 343-368), les scripts appropries sont copies automatiquement selon le systeme d'exploitation :

```python
# Copy helper scripts based on platform
scripts_source_dir = get_scripts_dir()
if scripts_source_dir.exists():
    if sys.platform == "win32":
        # Windows: copier les scripts PowerShell
        ps_scripts = scripts_source_dir / "powershell"
        for script_file in ps_scripts.glob("*.ps1"):
            dest_file = codexspec_dir / "scripts" / script_file.name
            dest_file.write_text(script_file.read_text(encoding="utf-8"), encoding="utf-8")
    else:
        # macOS/Linux: copier les scripts Bash
        bash_scripts = scripts_source_dir / "bash"
        for script_file in bash_scripts.glob("*.sh"):
            dest_file = codexspec_dir / "scripts" / script_file.name
            dest_file.write_text(script_file.read_text(encoding="utf-8"), encoding="utf-8")
```

**Resultat** : Selon le systeme d'exploitation, les scripts de `scripts/bash/` ou `scripts/powershell/` sont copies dans le repertoire `.codexspec/scripts/` du projet.

### Mecanisme de Resolution de Chemin

La fonction `get_scripts_dir()` (lignes 71-90) gere plusieurs scenarios d'installation :

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

## 3. Mecanisme d'Appel des Scripts dans Claude Code

### Mecanisme Core : Declaration YAML Frontmatter

Les fichiers modeles declarent les dependances de scripts via YAML frontmatter :

```yaml
---
description: Description de la commande
scripts:
  sh: .codexspec/scripts/check-prerequisites.sh --json --require-tasks --include-tasks
  ps: .codexspec/scripts/check-prerequisites.ps1 -Json -RequireTasks -IncludeTasks
---
```

### Remplacement des Espaces Reserveurs

Utiliser l'espace reserveur `{SCRIPT}` dans les modeles :

```markdown
### 1. Initialize Context

Executez `{SCRIPT}` depuis la racine du depot et analysez le JSON pour :
- `FEATURE_DIR` - Chemin du repertoire de fonctionnalite
- `AVAILABLE_DOCS` - Liste des documents disponibles
```

### Flux d'Appel

1. L'utilisateur saisit `/codexspec.analyze` dans Claude Code
2. Claude lit le modele `.claude/commands/codexspec.analyze.md`
3. Selon le systeme d'exploitation, Claude remplace `{SCRIPT}` par :
   - **macOS/Linux** : `.codexspec/scripts/check-prerequisites.sh --json --require-tasks --include-tasks`
   - **Windows** : `.codexspec/scripts/check-prerequisites.ps1 -Json -RequireTasks -IncludeTasks`
4. Claude execute le script, analyse la sortie JSON, poursuit les operations

## 4. Details des Fonctionnalites des Scripts

### 4.1 `check-prerequisites.sh/ps1` - Script de Verification Prealable

C'est le script le plus important, utilise pour verifier l'etat de l'environnement et retourner des informations structurees.

#### Fonctionnalites Core

- Verifier si on est sur une branche feature (format : `001-feature-name`)
- Detecter si les fichiers requis existent (`plan.md`, `tasks.md`)
- Retourner les informations de chemin au format JSON

#### Options de Parametres

| Parametre | Bash | PowerShell | Effet |
|-----------|------|------------|-------|
| Sortie JSON | `--json` | `-Json` | Sortie au format JSON |
| Exiger tasks.md | `--require-tasks` | `-RequireTasks` | Verifier l'existence de tasks.md |
| Inclure tasks.md | `--include-tasks` | `-IncludeTasks` | Inclure tasks.md dans AVAILABLE_DOCS |
| Chemins uniquement | `--paths-only` | `-PathsOnly` | Passer la verification, retourner uniquement les chemins |

#### Exemple de Sortie JSON

```json
{
  "FEATURE_DIR": "/path/to/.codexspec/specs/001-my-feature",
  "AVAILABLE_DOCS": ["research.md", "data-model.md", "tasks.md"]
}
```

### 4.2 `common.sh/ps1` - Fonctions Utilitaires Generales

Fournit des fonctionnalites generiques multi-plateformes :

#### Fonctions Version Bash

| Fonction | Effet |
|----------|-------|
| `get_feature_id()` | Obtenir l'ID de feature depuis la branche Git ou variable d'environnement |
| `get_specs_dir()` | Obtenir le chemin du repertoire specs |
| `is_codexspec_project()` | Verifier si on est dans un projet CodexSpec |
| `require_codexspec_project()` | S'assurer qu'on est dans un projet CodexSpec, sinon quitter |
| `log_info/success/warning/error()` | Sortie de journal coloree |
| `command_exists()` | Verifier si une commande existe |

#### Fonctions Version PowerShell

| Fonction | Effet |
|----------|-------|
| `Get-RepoRoot` | Obtenir le repertoire racine du depot Git |
| `Get-CurrentBranch` | Obtenir le nom de la branche courante |
| `Test-HasGit` | Detecter s'il y a un depot Git |
| `Test-FeatureBranch` | Verifier si on est sur une branche feature |
| `Get-FeaturePathsEnv` | Obtenir tous les chemins lies a la feature |
| `Test-FileExists` | Verifier si un fichier existe |
| `Test-DirHasFiles` | Verifier si un repertoire a des fichiers |

### 4.3 `create-new-feature.sh/ps1` - Creer une Nouvelle Fonctionnalite

#### Fonctionnalites

- Generer automatiquement un ID de feature incrementiel (001, 002, ...)
- Creer le repertoire de feature et spec.md initial
- Creer la branche Git correspondante

#### Exemple d'Utilisation

```bash
./create-new-feature.sh -n "user authentication" -i 001
```

## 5. Commandes Utilisant les Scripts

Les 4 commandes suivantes utilisent les scripts :

| Commande | Parametres Scripts | Effet |
|----------|-------------------|-------|
| `/codexspec.clarify` | `--json --paths-only` | Obtenir les chemins, ne pas verifier les fichiers |
| `/codexspec.checklist` | `--json` | Verifier l'existence de plan.md |
| `/codexspec.analyze` | `--json --require-tasks --include-tasks` | Verifier plan.md + tasks.md |
| `/codexspec.tasks-to-issues` | `--json --require-tasks --include-tasks` | Verifier plan.md + tasks.md |

## 6. Diagramme de Flux Complet

```
+--------------------------------------------------------------------------+
|                        Phase d'Initialisation                             |
|                                                                          |
|  $ codexspec init mon-project                                            |
|       |                                                                  |
|       |-- Creer la structure de repertoire .codexspec/                   |
|       |-- Copier scripts/*.sh -> .codexspec/scripts/                    |
|       |-- Copier templates/commands/*.md -> .claude/commands/           |
|       |-- Creer constitution.md, config.yml, CLAUDE.md                  |
|                                                                          |
+--------------------------------------------------------------------------+
                                    |
+--------------------------------------------------------------------------+
|                        Phase d'Utilisation (Claude Code)                  |
|                                                                          |
|  Utilisateur : /codexspec.analyze                                        |
|       |                                                                  |
|       |-- Claude lit .claude/commands/codexspec.analyze.md              |
|       |                                                                  |
|       |-- Analyser la declaration scripts dans YAML frontmatter         |
|       |   scripts:                                                       |
|       |     sh: .codexspec/scripts/check-prerequisites.sh --json ...   |
|       |                                                                  |
|       |-- Remplacer l'espace reserveur {SCRIPT}                         |
|       |                                                                  |
|       |-- Executer le script :                                          |
|       |   $ .codexspec/scripts/check-prerequisites.sh --json ...       |
|       |                                                                  |
|       |-- Analyser la sortie JSON :                                    |
|       |   {"FEATURE_DIR": "...", "AVAILABLE_DOCS": [...]}              |
|       |                                                                  |
|       |-- Lire spec.md, plan.md, tasks.md                              |
|       |                                                                  |
|       |-- Generer le rapport d'analyse                                  |
|                                                                          |
+--------------------------------------------------------------------------+
```

## 7. Points Forts de la Conception

### 7.1 Compatibilite Multi-Plateformes

Maintenance simultanee des versions Bash et PowerShell, selection automatique via `sys.platform` :

```python
if sys.platform == "win32":
    # Copier les scripts PowerShell
else:
    # Copier les scripts Bash
```

### 7.2 Configuration Declarative

Declaration des dependances de scripts via YAML frontmatter, claire et intuitive :

```yaml
scripts:
  sh: .codexspec/scripts/check-prerequisites.sh --json
  ps: .codexspec/scripts/check-prerequisites.ps1 -Json
```

### 7.3 Sortie JSON

Les scripts produisent des donnees structurees, faciles a analyser par Claude :

```json
{
  "FEATURE_DIR": "/path/to/.codexspec/specs/001-feature",
  "AVAILABLE_DOCS": ["research.md", "data-model.md"]
}
```

### 7.4 Verification Progressive

Differentes commandes utilisent differents parametres, verification a la demande :

| Etape | Commande | Niveau de Verification |
|-------|----------|------------------------|
| Avant planification | `/codexspec.clarify` | Chemins uniquement |
| Apres planification | `/codexspec.checklist` | plan.md |
| Apres taches | `/codexspec.analyze` | plan.md + tasks.md |

### 7.5 Integration Git

- Extraction automatique de l'ID de feature depuis le nom de branche
- Prise en charge de la verification de nommage de branche (format `^\d{3}-`)
- Prise en charge du remplacement par variable d'environnement (`SPECIFY_FEATURE` / `CODEXSPEC_FEATURE`)

## 8. Chemins de Code Cles

| Fichier | Ligne/Position | Fonction |
|---------|----------------|----------|
| `src/codexspec/__init__.py` | 343-368 | Logique de copie de scripts |
| `src/codexspec/__init__.py` | 71-90 | Resolution de chemin `get_scripts_dir()` |
| `scripts/bash/check-prerequisites.sh` | Texte complet | Script principal de verification prealable Bash |
| `scripts/powershell/check-prerequisites.ps1` | 56-146 | Script de verification prealable PowerShell |
| `scripts/bash/common.sh` | Texte complet | Fonctions utilitaires generales Bash |
| `scripts/powershell/common.ps1` | Texte complet | Fonctions utilitaires generales PowerShell |
| `templates/commands/*.md` | YAML frontmatter | Declaration de scripts |

## 9. Liste des Fichiers Scripts

### Scripts Bash (`scripts/bash/`)

```
scripts/bash/
+-- check-prerequisites.sh   # Script principal de verification prealable
+-- common.sh                # Fonctions utilitaires generales
+-- create-new-feature.sh    # Creer une nouvelle fonctionnalite
```

### Scripts PowerShell (`scripts/powershell/`)

```
scripts/powershell/
+-- check-prerequisites.ps1  # Script principal de verification prealable
+-- common.ps1               # Fonctions utilitaires generales
+-- create-new-feature.ps1   # Creer une nouvelle fonctionnalite
```

---

*Ce document enregistre l'architecture complete et le flux d'utilisation des scripts dans le projet CodexSpec. En cas de mise a jour, veuillez modifier en consequence.*

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/images/codexspec-logo-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="assets/images/codexspec-logo-light.svg">
  <img alt="CodexSpec Logo" src="assets/images/codexspec-logo-light.svg" width="420">
</picture>

# Bienvenue dans CodexSpec

[![Version PyPI](https://img.shields.io/pypi/v/codexspec:svg)](https://pypi.org/project/codexspec/)
[![Python](https://img.shields.io/pypi/pyversions/codexspec:svg)](https://pypi.org/project/codexspec/)
[![Licence : MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**Une boite a outils de Developpement Pilot par les Specifications (SDD) pour Claude Code**

CodexSpec est une boite a outils qui vous aide a construire des logiciels de haute qualite en utilisant une approche structuree et pilotee par les specifications. Elle revoit les methodes traditionnelles de developpement en faisant des specifications des artefacts executables qui guident directement l'implementation.

## Pourquoi CodexSpec ?

Pourquoi utiliser CodexSpec en plus de Claude Code ? Voici la comparaison :

| Aspect | Claude Code seulement | CodexSpec + Claude Code |
|--------|----------------------|-------------------------|
| **Support multilingue** | Interaction en anglais par defaut | Configurez la langue de l'equipe pour une meilleure collaboration |
| **Tracabilite** | Difficile de tracer les decisions apres la session | Tous les specs, plans et taches sauvegardes dans `.codexspec/specs/` |
| **Recuperation de session** | Difficile de recuperer apres interruptions en mode plan | Division en plusieurs commandes + docs persistants = recuperation facile |
| **Gouvernance d'equipe** | Pas de principes unifies, styles incoherents | `constitution.md` applique les standards et qualite de l'equipe |

### Collaboration Humain-AI

CodexSpec repose sur la conviction que **un developpement assiste par AI efficace necessite une participation humaine active a chaque etape**.

| Probleme | Solution |
|----------|----------|
| Exigences floues | Q&R interactives pour clarifier avant de construire |
| Specifications incompletes | Commandes de revision dediees avec notation |
| Plans techniques desalignes | Validation basee sur la constitution |
| Decompositions de taches vagues | Generation de taches avec application TDD |

### Fonctionnalites cles

- **Base sur la Constitution** - Etablissez des principes de projet qui guident toutes les decisions
- **Clarification Interactive** - Raffinement des exigences par Q&R
- **Commandes de Revision** - Validez les artefacts a chaque etape
- **Pret pour TDD** - Methodologie test-first integree dans les taches
- **Support i18n** - Plus de 13 langues via traduction LLM

## Demarrage Rapide

```bash
# Installer
uv tool install codexspec

# Creer un nouveau projet
codexspec init mon-projet

# Ou initialiser dans un projet existant
codexspec init . --ai claude
```

[Guide d'Installation Complet](getting-started/installation.md)

## Apercu du Workflow

```
Idee -> Clarifier -> Reverifier -> Planifier -> Reverifier -> Taches -> Reverifier -> Implementer
              ^                  ^                   ^
          Verifications humaines  Verifications humaines  Verifications humaines
```

Chaque artefact a une commande de revision correspondante pour valider la sortie de l'AI avant de poursuivre.

[Apprendre le Workflow](user-guide/workflow.md)

## Licence

Licence MIT - voir [LICENSE](https://github.com/Zts0hg/codexspec/blob/main/LICENSE) pour plus de details.

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/images/codexspec-logo-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="assets/images/codexspec-logo-light.svg">
  <img alt="CodexSpec Logo" src="assets/images/codexspec-logo-light.svg" width="420">
</picture>

# Bienvenue sur CodexSpec

[![PyPI version](https://img.shields.io/pypi/v/codexspec.svg)](https://pypi.org/project/codexspec/)
[![Python](https://img.shields.io/pypi/pyversions/codexspec.svg)](https://pypi.org/project/codexspec/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**Une boîte à outils Requirements-First SDD pour Claude Code**

CodexSpec vous aide à produire un logiciel de qualité grâce au **Requirements-First Spec-Driven Development (SDD)** — les exigences confirmées constituent l'autorité de priorité la plus haute, et rien n'est définitif tant que vous ne l'avez pas explicitement confirmé. Au lieu de vous précipiter sur le code, vous confirmez le **quoi** et le **pourquoi** avant de décider du **comment**.

## Pourquoi CodexSpec ?

Pourquoi utiliser CodexSpec par-dessus Claude Code ? Voici la comparaison :

| Aspect | Claude Code seul | CodexSpec + Claude Code |
|--------|------------------|-------------------------|
| **Support multilingue** | Interaction en anglais par défaut | Configurez la langue de l'équipe pour une collaboration et des revues plus fluides |
| **Traçabilité** | Difficile de retrouver les décisions après la fin de la session | Toutes les spécifications, plans et tâches sont sauvegardés dans `.codexspec/specs/` |
| **Reprise de session** | Les interruptions du mode plan sont difficiles à rattraper | Décomposition en plusieurs commandes + documents persistants = reprise facile |
| **Gouvernance d'équipe** | Aucun principe unifié, styles incohérents | `constitution.md` impose les standards et le niveau de qualité de l'équipe |

### Qu'est-ce que Requirements-First SDD ?

**Requirements-First SDD** est la méthodologie Spec-Driven Development (SDD) avec une amélioration majeure : **les exigences confirmées sont l'autorité de priorité la plus haute**. Vous définissez et confirmez le *quoi* à construire et le *pourquoi* avant de décider du *comment* — et rien ne devient définitif tant que vous ne l'avez pas explicitement confirmé.

```
Traditionnel :  Idée → Code → Débogage → Réécriture
SDD :           Idée → Exigences confirmées → Spec → Plan → Tâches → Code
```

### Fonctionnalités clés

- **Développement fondé sur une constitution** — établissez des principes de projet qui guident toutes les décisions
- **Capture persistante des exigences** — `/specify` enregistre les échanges confirmés dans `requirements.md` avant la génération des documents
- **Revues automatiques** — chaque artefact de spécification, plan ou tâche généré intègre des contrôles qualité intégrés
- **Clarification interactive** — raffinement des exigences sous forme de questions/réponses
- **Analyse inter-artefacts** — détectez les incohérences avant l'implémentation
- **Tâches traçables** — la décomposition en tâches préserve la couverture des exigences et du plan, en appliquant le **TDD conditionnel** (ordonnancement test-first uniquement lorsque le plan, la constitution ou le risque l'exige ; les tâches non testables comme la doc et la configuration sont implémentées directement)
- **Intégration native à Claude Code** — les slash commands fonctionnent de manière transparente
- **Support multilingue** — plus de 13 langues grâce à la traduction dynamique par LLM
- **Multiplateforme** — scripts Bash et PowerShell inclus
- **Extensible** — architecture de plugins pour des commandes personnalisées

## Démarrage rapide

```bash
# Installer
uv tool install codexspec

# Créer un nouveau projet
codexspec init my-project

# Ou initialiser dans un projet existant
codexspec init . --ai claude
```

[Guide d'installation complet](getting-started/installation.md)

## Vue d'ensemble du flux de travail

CodexSpec structure le développement en **points de contrôle consultables**. Les exigences confirmées traversent les spécifications, plans et tâches jusqu'au code, avec une revue à chaque étape.

```
Idée → Exigences confirmées → Spec → Plan → Tâches → Code
```

Chaque artefact est produit par une commande dédiée et validé avant de passer à l'étape suivante :

```
Idée → /specify → requirements.md → /generate-spec → spec.md → /spec-to-plan → plan.md → /plan-to-tasks → tasks.md → /implement
                                                   │                         │                            │
                                              Revue spec                 Revue plan                   Revue tasks
```

### La porte de confirmation (Confirmation Gate)

Le différenciateur déterminant est la **Confirmation Gate** : les exigences, spécifications, plans et tâches ne deviennent définitifs qu'après votre confirmation humaine explicite. Les exigences confirmées sont l'autorité de priorité la plus haute concernant les fonctionnalités, l'IA ne peut donc pas verrouiller de décisions en silence — les artefacts dérivés comportent des liens explicites vers leurs sources, et les conflits sont retracés au lieu d'être propagés.

### Boucle de qualité itérative

Chaque commande de génération inclut une **revue automatique fondée sur des preuves** : les défauts nécessitent des preuves concrètes, les suggestions consultatives ne déclenchent jamais de modifications automatiques, et les défauts vérifiés peuvent être corrigés puis soumis à une nouvelle revue pendant deux tours au maximum. Cette boucle fait monter la qualité sans que vous ayez à surveiller chaque détail.

[Apprendre le flux de travail](user-guide/workflow.md)

## Licence

Licence MIT — voir [LICENSE](https://github.com/Zts0hg/codexspec/blob/main/LICENSE) pour les détails.

# CodexSpec

![CodexSpec](assets/images/codexspec-logo-light.svg#only-light){ width="420" }

![CodexSpec](assets/images/codexspec-logo-dark.svg#only-dark){ width="420" }

**Des outils SDD avec priorité aux exigences pour Claude Code et OpenAI Codex**

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

<a id="why-choose-codexspec"></a>

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

<a id="what-is-requirements-first-sdd"></a>

### Que signifie SDD avec priorité aux exigences ?

Dans le développement piloté par les spécifications avec priorité aux exigences,
**les exigences confirmées priment sur toute autre référence pour la fonctionnalité**.
Avant d'élaborer les artefacts d'implémentation, l'agent consigne les objectifs,
les contraintes, les décisions, les exclusions, les questions en suspens et les
éléments attestant la confirmation des exigences.

```text
Idea → Confirmed Requirements →     Spec    →     Design    →     Plan    →    Tasks     →     Code
                 ↓                   ↓              ↓              ↓             ↓              ↓
         User confirmation      review-spec   review-design   review-plan   review-tasks   review-code
```

Vous confirmez les exigences ; chaque artefact dérivé fait ensuite l’objet
d’une revue, de la spécification jusqu’au code.

L'intention du produit se définit et évolue grâce à la collaboration humaine.
Les revues automatiques vérifient que les artefacts dérivés respectent cette
intention. Lorsque l'automatisation est activée, le travail avance à mesure que
les étapes sont validées ; l'agent ne peut pas remplacer les exigences
confirmées sans le signaler.

[![CodexSpec : développement guidé par les exigences, revues par étape et réutilisation de l’expérience](../../assets/workflow/workflow-fr-light.png#only-light)](../../assets/workflow/workflow-fr-light.png#only-light)

[![CodexSpec : développement guidé par les exigences, revues par étape et réutilisation de l’expérience](../../assets/workflow/workflow-fr-dark.png#only-dark)](../../assets/workflow/workflow-fr-dark.png#only-dark)

Ouvrir le diagramme en pleine taille : [☀️](../../assets/workflow/workflow-fr-light.png) · [🌙](../../assets/workflow/workflow-fr-dark.png)

<a id="30-second-quick-start"></a>

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
suivantes sont décrites dans [Flux de travail principal](user-guide/workflow.md#core-workflow).

Vous utilisez l'application de bureau Codex ? [Demandez à Codex d'installer et d'initialiser votre projet](getting-started/installation.md#install-with-the-codex-desktop-app).

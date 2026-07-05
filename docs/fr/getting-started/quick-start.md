# Démarrage rapide

Cette page parcourt le flux **Requirements-First SDD** complet en huit étapes.
Les exigences confirmées sont l'autorité de priorité la plus haute, et rien n'est définitif tant que vous ne l'avez pas explicitement confirmé — chaque étape se termine par une **Confirmation Gate** que vous contrôlez.

Pour des changements petits et bien délimités, vous pouvez sauter la walkthrough complète et lancer `/codexspec:quick` à la place.

## 1. Initialiser un projet

Après l'installation, créez ou initialisez votre projet :

```bash
# Créer un nouveau projet
codexspec init my-awesome-project

# Ou initialiser dans le répertoire courant
codexspec init . --ai claude

# Avec une sortie en chinois (définit la base de sortie)
codexspec init my-project --lang zh-CN

# Entièrement non interactif (CI/scripts) : base zh-CN, messages de commit en anglais
codexspec init my-project --lang zh-CN --commit-lang en

# Définir chaque dimension linguistique explicitement (scriptable, sans invite)
codexspec init my-project \
  --interaction-lang zh-CN --document-lang en --commit-lang en
```

Ensuite, placez-vous dans le projet et lancez Claude Code :

```bash
cd my-awesome-project
claude
```

## 2. Établir les principes du projet

Utilisez la commande constitution pour fixer les standards auxquels tous les artefacts ultérieurs seront confrontés :

```
/codexspec:constitution Create principles focused on code quality and testing
```

## 3. Clarifier les exigences

Utilisez `/codexspec:specify` pour explorer les exigences :

```
/codexspec:specify I want to build a task management application
```

Cette commande pose des questions de clarification, fait émerger les cas limites, et vous demande de confirmer un résumé final des exigences qui est persisté dans `requirements.md`.

> **Confirmation Gate** : `/codexspec:specify` n'écrit que les entrées que vous confirmez explicitement. Le résumé des exigences qu'il présente n'est **pas** définitif tant que vous ne l'acceptez pas — refusez, modifiez ou rouvrez n'importe quel élément avant de dire oui. Rien en aval ne peut outrepasser ce que vous confirmez ici.

## 4. Générer la spécification

Une fois le résumé des exigences confirmé, générez le document de spécification :

```
/codexspec:generate-spec
```

`generate-spec` compile les entrées confirmées en un `spec.md` structuré avec des références aux sources pour la traçabilité, puis lance une revue automatique (les défauts nécessitent des preuves concrètes ; les suggestions consultatives ne déclenchent jamais de modifications automatiques ; les défauts vérifiés peuvent être corrigés puis soumis à une nouvelle revue pendant deux tours au maximum).

## 5. Valider et revérifier

**Recommandé** : validez la spec avant de poursuivre :

```
/codexspec:review-spec
```

Il s'agit d'une **revue fondée sur des preuves** : chaque défaut signalé cite une preuve concrète, et les avis de conception restent séparés de l'acceptation.

## 6. Créer le plan technique

```
/codexspec:spec-to-plan Use Python FastAPI for backend
```

Le plan enregistre les liens `Covers` vers les exigences de la spécification et vérifie les principes applicables de la constitution.

## 7. Générer les tâches

```
/codexspec:plan-to-tasks
```

Les tâches sont organisées autour de résultats vérifiables, avec des liens de traçabilité vers le plan et les exigences. L'ordonnancement test-first est appliqué **conditionnellement** — uniquement lorsque le plan, la constitution ou le risque de la tâche l'exige. Les tâches non testables (doc, configuration) sont implémentées directement.

## 8. Implémenter

```
/codexspec:implement-tasks
```

L'implémentation suit le **TDD conditionnel** : les tâches de code utilisent le cycle Red → Green → Verify → Refactor lorsque c'est requis ; les tâches de documentation et de configuration sont implémentées directement.

## Petits changements : `/codexspec:quick`

Pour un petit changement bien délimité, vous n'avez pas besoin de la walkthrough complète en huit étapes. `/codexspec:quick` exécute un flux Requirements-First SDD compact en une seule commande :

```
/codexspec:quick Add a "remember me" checkbox to the login form
```

Quick respecte les mêmes garde-fous que le flux complet :

- Il crée un espace de travail pour la fonctionnalité et un `requirements.md` en utilisant la même convention d'horodatage que `/codexspec:specify`.
- Il présente un résumé concis des exigences confirmées (`NEED-*`, `CON-*`/`DEC-*` pertinentes, `OUT-*`, `OPEN-*` non résolus) et attend votre confirmation explicite — la **Confirmation Gate** s'applique toujours.
- Il enchaîne ensuite `/codexspec:generate-spec` → `/codexspec:spec-to-plan` → `/codexspec:plan-to-tasks` → `/codexspec:implement-tasks` sur ce répertoire de fonctionnalité, chaque commande de génération ayant sa propre boucle de revue automatique.

Si le changement se révèle large ou qu'il a plusieurs résultats indépendants, Quick s'interrompt et recommande le flux standard à la place.

## Structure du projet

Après l'initialisation :

```
my-project/
├── .codexspec/
│   ├── memory/
│   │   └── constitution.md    # Constitution du projet
│   ├── specs/
│   │   └── {feature-id}/
│   │       ├── spec.md        # Spécification de la fonctionnalité
│   │       ├── plan.md        # Plan technique
│   │       ├── tasks.md       # Décomposition en tâches
│   │       └── checklists/    # Checklists qualité
│   ├── templates/             # Modèles personnalisés
│   ├── scripts/               # Scripts utilitaires
│   └── extensions/            # Extensions personnalisées
├── .claude/
│   └── commands/              # Slash commands Claude Code
├── .agents/
│   └── skills/                # Skills Codex (si initialisé avec --ai codex ou both)
├── CLAUDE.md                  # Contexte Claude Code
└── AGENTS.md                  # Contexte Codex
```

## Prochaines étapes

[Guide complet du flux de travail](../user-guide/workflow.md)

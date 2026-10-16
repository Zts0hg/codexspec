# Démarrage rapide

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
suivantes sont décrites dans [Flux de travail principal](../user-guide/workflow.md#core-workflow).

Vous utilisez l'application de bureau Codex ? [Demandez à Codex d'installer et d'initialiser votre projet](installation.md#install-with-the-codex-desktop-app).

<a id="core-workflow"></a>

## Flux de travail principal

Dans le flux standard, les artefacts de chaque fonctionnalité conservent des références à leurs sources :

```text
/specify          → requirements.md
/generate-spec    → spec.md       → review-spec
/spec-to-design   → design.md     → review-design
/design-to-plan   → plan.md       → review-plan
/plan-to-tasks    → tasks.md      → review-tasks → analyze
/implement-tasks  → implementation and complete-feature code review
```

Les exemples suivants utilisent le préfixe `/codexspec:` de Claude. Dans
Codex, utilisez `$codexspec:` avec le même nom de commande et les mêmes arguments.

| Étape | Commande | Objectif et résultat |
|------|---------|--------------------|
| Principes du projet | `/codexspec:constitution` | Créer ou mettre à jour `constitution.md` et valider les artefacts concernés |
| Exigences | `/codexspec:specify <idea>` | Discuter de l'intention, confirmer le résumé final et enregistrer `requirements.md` |
| Spécification | `/codexspec:generate-spec <feature-dir>` | Élaborer `spec.md` à partir des exigences confirmées, avec des références aux sources |
| Conception du système | `/codexspec:spec-to-design <feature-dir>` | Élaborer `design.md` avec les composants, les interfaces et les principales décisions de conception |
| Plan d'implémentation | `/codexspec:design-to-plan <feature-dir>` | Élaborer `plan.md` avec les phases, leur ordre et les vérifications |
| Tâches | `/codexspec:plan-to-tasks <feature-dir>` | Élaborer un `tasks.md` traçable et vérifiable, puis analyser la cohérence entre les artefacts |
| Implémentation | `/codexspec:implement-tasks <feature-dir>` | Exécuter les tâches, vérifier les résultats et corriger les constats de revue vérifiés de façon indépendante |

Remplacez `<feature-dir>` par le dossier de la fonctionnalité indiqué lors de
la définition des exigences. Poursuivez dans son worktree ou fournissez son
chemin explicite pour conserver la même identité de fonctionnalité d'une
commande ou d'une session à l'autre.

<a id="specify-clarify-and-analyze"></a>

### specify, clarify et analyze

- **specify** lance ou reprend la définition des exigences. Le résumé ne devient contraignant qu'après confirmation explicite.
- **clarify** résout les ambiguïtés des exigences ou de la spécification existantes : jusqu'à cinq questions par exécution, réparties entre quatre catégories. Il met d'abord à jour `requirements.md`, puis synchronise `spec.md`.
- **analyze** vérifie toute la chaîne : exigences → spécification → conception → plan → tâches. Il applique automatiquement des corrections déterministes aux artefacts dérivés lorsque ces corrections découlent des sources qui font autorité ; il ne modifie jamais `requirements.md`. Les constats non résolus sont signalés. Il s'exécute automatiquement après une revue des tâches validée et reste informatif, sans bloquer l'implémentation.

```text
/codexspec:clarify <feature-dir>
/codexspec:analyze <feature-dir>
```

<a id="small-changes-with-quick"></a>

### Petits changements avec Quick

Utilisez `quick` pour un changement limité et bien défini, comme une correction locale :

```text
/codexspec:quick Fix the empty-state message on the task list
```

Quick confirme et enregistre un résumé bref des exigences, puis coordonne
la spécification, la planification, les tâches et l'implémentation avec les
revues des commandes de génération. Les changements de grande ampleur et les
choix de produit ou de conception encore en suspens nécessitent le flux standard.
Quick s'arrête lorsqu'une nouvelle décision est nécessaire.

<a id="workflow-automation"></a>

### Automatisation du flux de travail

La valeur par défaut de `workflow.auto_next` est **false**. Si elle est `true`
dans la configuration de l'espace de travail actif, la confirmation finale des
exigences lance l'étape de spécification. Chaque étape de génération avance
après un résultat `PASS` ou `PASS_WITH_WARNINGS` ; un résultat `NEEDS_REVISION`
ou `BLOCKED` arrête la chaîne. `implement-tasks` est la dernière étape.

La correction automatique des artefacts ne porte que sur les défauts vérifiés
dont la solution découle des éléments établis dans les artefacts en amont,
avec un maximum de deux cycles de correction et de revue. Les recommandations
sont traitées séparément. La revue et la correction de l'implémentation ont
leurs propres règles d'achèvement, décrites plus loin.

Le [guide du flux de travail](../user-guide/workflow.md) détaille les règles de chaque étape.

<a id="project-structure"></a>

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

Le blueprint partagé est conservé dans le worktree dédié à auto-dev. Il n'en
existe pas de copie modifiable distincte dans chaque checkout du flux standard.
Les brouillons de revue manuelle des connaissances sont exclus de Git.

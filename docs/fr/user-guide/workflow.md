# Workflow

CodexSpec structure le développement en **points de vérification examinables** avec validation humaine à chaque étape.

## Aperçu du Workflow

```
┌──────────────────────────────────────────────────────────────────────────┐
│                    Workflow de Collaboration Humain-AI CodexSpec          │
├──────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  1. Constitution  ──►  Définir les principes du projet                    │
│         │                                                                │
│         ▼                                                                │
│  2. Specify  ───────►  Q&R interactives pour clarifier les exigences     │
│         │                                                                │
│         ▼                                                                │
│  3. Generate Spec  ─►  Créer le document spec.md                          │
│         │               ✓ Révision automatique: génère review-spec.md     │
│         ▼                                                                │
│  4. Spec to Plan  ──►  Créer le plan technique                            │
│         │               ✓ Révision automatique: génère review-plan.md     │
│         ▼                                                                │
│  5. Plan to Tasks  ─►  Générer des tâches atomiques                       │
│         │               ✓ Révision automatique: génère review-tasks.md    │
│         ▼                                                                │
│  6. Implement  ─────►  Exécuter avec le workflow TDD conditionnel         │
│                                                                          │
└──────────────────────────────────────────────────────────────────────────┘
```

## Pourquoi la Révision est Importante

| Sans Révision | Avec Révision |
|---------------|---------------|
| L'AI fait des suppositions incorrectes | L'humain détecte les mauvaises interprétations tôt |
| Les exigences incomplètes se propagent | Les lacunes sont identifiées avant l'implémentation |
| L'architecture s'éloigne de l'intention | L'alignement est vérifié à chaque étape |
| **Résultat : Retravail** | **Résultat : Réussite du premier coup** |

## Révision Automatique

Chaque commande de génération **exécute automatiquement une révision** :

- `/codexspec:generate-spec` → invoque automatiquement `review-spec`
- `/codexspec:spec-to-plan` → invoque automatiquement `review-plan`
- `/codexspec:plan-to-tasks` → invoque automatiquement `review-tasks`

Les rapports de révision sont générés avec les artefacts, vous permettant de voir immédiatement les problèmes.

## Boucle de Qualité Itérative

Lorsque des problèmes sont trouvés dans les rapports de révision, décrivez les corrections en langage naturel et le système mettra à jour l'artefact et le rapport :

```
┌──────────────────────────────────────────────────────────────────────┐
│                    Boucle de Qualité Itérative                        │
├──────────────────────────────────────────────────────────────────────┤
│                                                                       │
│  Artefact (spec/plan/tasks.md)                                        │
│         │                                                             │
│         ▼                                                             │
│  Révision automatique  ───►  Rapport de révision (review-*.md)        │
│         │                       │                                     │
│         │                       ▼                                     │
│         │                Problèmes détectés ?                          │
│         │                       │                                     │
│         │                 ┌─────┴─────┐                               │
│         │                 │           │                               │
│         │                Oui        Non                               │
│         │                 │           │                               │
│         │                 ▼           ▼                               │
│         │       Décrire la       Passer à                             │
│         │       correction       l'étape suivante                     │
│         │       en conversation                                           │
│         │                 │                                           │
│         │                 ▼                                           │
│         │       Mise à jour simultanée :                               │
│         │         • Artefact (spec/plan/tasks.md)                     │
│         │         • Rapport de révision (review-*.md)                  │
│         │                 │                                           │
│         └─────────────────┘                                           │
│           (Répéter jusqu'à satisfaction)                              │
│                                                                       │
│  Réexamen manuel : Exécutez /codexspec:review-* à tout moment         │
│  pour obtenir une nouvelle analyse                                    │
│                                                                       │
└──────────────────────────────────────────────────────────────────────┘
```

**Fonctionnement** :

1. **Révision automatique** : Chaque commande de génération exécute automatiquement la révision correspondante
2. **Rapport de révision** : Génère des fichiers `review-*.md` contenant les problèmes détectés
3. **Correction itérative** : Décrivez ce qui doit être corrigé dans la conversation, l'artefact et le rapport se mettent à jour ensemble
4. **Réexamen manuel** : Exécutez `/codexspec:review-spec|plan|tasks` à tout moment pour une nouvelle analyse

## Commandes Principales

| Étape | Commande | Objectif |
|-------|----------|----------|
| 1 | `/codexspec:constitution` | Définir les principes du projet |
| 2 | `/codexspec:specify` | Q&R interactives pour les exigences |
| 3 | `/codexspec:generate-spec` | Créer le document de spécification (★ Révision automatique) |
| - | `/codexspec:review-spec` | Invoquée automatiquement, ou revalider manuellement |
| 4 | `/codexspec:spec-to-plan` | Créer le plan technique (★ Révision automatique) |
| - | `/codexspec:review-plan` | Invoquée automatiquement, ou revalider manuellement |
| 5 | `/codexspec:plan-to-tasks` | Décomposer en tâches (★ Révision automatique) |
| - | `/codexspec:review-tasks` | Invoquée automatiquement, ou revalider manuellement |
| 6 | `/codexspec:implement-tasks` | Exécuter l'implémentation |

## Spécification en Deux Phases

### specify vs clarify

| Aspect | `/codexspec:specify` | `/codexspec:clarify` |
|--------|----------------------|----------------------|
| **Objectif** | Exploration initiale | Raffinement itératif |
| **Quand** | Aucun spec.md n'existe | spec.md existe, nécessite des compléments |
| **Entrée** | Votre idée initiale | spec.md existant |
| **Sortie** | Aucune (dialogue uniquement) | Met à jour spec.md |

## TDD Conditionnel

L'implémentation suit le TDD conditionnel :

- **Tâches de code** : Test-first (Rouge → Vert → Vérifier → Refactorer)
- **Tâches non testables** (docs, config) : Implémentation directe

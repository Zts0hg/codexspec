# Workflow

CodexSpec structure le developpement en **points de verification examinables** avec validation humaine a chaque etape.

## Apercu du Workflow

```
+--------------------------------------------------------------------------+
|                    Workflow de Collaboration Humain-AI CodexSpec          |
+--------------------------------------------------------------------------+
|                                                                           |
|  1. Constitution  -->  Definir les principes du projet                    |
|         |                                                                 |
|         v                                                                 |
|  2. Specify  --------->  Q&R interactives pour clarifier les exigences    |
|         |                                                                 |
|         v                                                                 |
|  3. Generate Spec  -->  Creer le document spec.md                         |
|         |                                                                 |
|         v                                                                 |
|  +====================================================================+   |
|  |  ★ PORTE DE REVISION 1 : /codexspec:review-spec ★                   |   |
|  +====================================================================+   |
|         |                                                                 |
|         v                                                                 |
|  4. Spec to Plan  -->  Creer le plan technique                            |
|         |                                                                 |
|         v                                                                 |
|  +====================================================================+   |
|  |  ★ PORTE DE REVISION 2 : /codexspec:review-plan ★                   |   |
|  +====================================================================+   |
|         |                                                                 |
|         v                                                                 |
|  5. Plan to Tasks  -->  Generer des taches atomiques                      |
|         |                                                                 |
|         v                                                                 |
|  +====================================================================+   |
|  |  ★ PORTE DE REVISION 3 : /codexspec:review-tasks ★                  |   |
|  +====================================================================+   |
|         |                                                                 |
|         v                                                                 |
|  6. Implement  -------->  Executer avec le workflow TDD conditionnel      |
|                                                                           |
+--------------------------------------------------------------------------+
```

## Pourquoi la Revision est Importante

| Sans Revision | Avec Revision |
|---------------|---------------|
| L'AI fait des suppositions incorrectes | L'humain detecte les mauvaises interpretations tot |
| Les exigences incompletes se propagent | Les lacunes sont identifiees avant l'implementation |
| L'architecture s'eloigne de l'intention | L'alignement est verifie a chaque etape |
| **Resultat : Retravail** | **Resultat : Reussite du premier coup** |

## Commandes Principales

| Etape | Commande | Objectif |
|-------|----------|----------|
| 1 | `/codexspec:constitution` | Definir les principes du projet |
| 2 | `/codexspec:specify` | Q&R interactives pour les exigences |
| 3 | `/codexspec:generate-spec` | Creer le document de specification |
| - | `/codexspec:review-spec` | ★ Valider la specification |
| 4 | `/codexspec:spec-to-plan` | Creer le plan technique |
| - | `/codexspec:review-plan` | ★ Valider le plan |
| 5 | `/codexspec:plan-to-tasks` | Decomposer en taches |
| - | `/codexspec:review-tasks` | ★ Valider les taches |
| 6 | `/codexspec:implement-tasks` | Executer l'implementation |

## Specification en Deux Phases

### specify vs clarify

| Aspect | `/codexspec:specify` | `/codexspec:clarify` |
|--------|----------------------|----------------------|
| **Objectif** | Exploration initiale | Raffinement iteratif |
| **Quand** | Aucun spec.md n'existe | spec.md existe, necessite des complements |
| **Entree** | Votre idee initiale | spec.md existant |
| **Sortie** | Aucune (dialogue uniquement) | Met a jour spec.md |

## TDD Conditionnel

L'implementation suit le TDD conditionnel :

- **Taches de code** : Test-first (Rouge -> Vert -> Verifier -> Refactorer)
- **Taches non testables** (docs, config) : Implementation directe

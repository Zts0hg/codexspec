# Étude de cas CodexSpec : ajouter un générateur de descriptions de PR au projet

> Cas historique : la conversation, les décisions intermédiaires, la suite de commandes et les scores ci-dessous retracent le workflow de l’époque, pas le contrat actuel des commandes. Le flux standard comporte désormais une étape de conception distincte et `review-design` ; `clarify` met à jour les exigences confirmées avant la spécification. Consultez le [workflow actuel](../user-guide/workflow.md) et la [référence de la commande PR](../user-guide/commands.md#codexspecpr).

> Ce document retrace le processus complet d'utilisation de la chaîne d'outils CodexSpec pour ajouter une nouvelle fonctionnalité au projet CodexSpec lui-même, et illustre le Spec-Driven Development (SDD) en pratique.

## Vue d'ensemble

**Fonctionnalité cible** : ajouter la commande `/codexspec:pr`, qui génère des descriptions structurées de PR GitHub / MR GitLab. (Voir l'[entrée README `/codexspec:pr`](https://github.com/Zts0hg/codexspec/blob/main/README.md) pour le résumé orienté utilisateur de la commande livrée.)

**Flux de développement** : `specify → generate-spec → review-spec → clarify → design-to-plan`

**Caractéristique clé** : une exigence problématique est remontée en cours de route et corrigée via la commande `clarify`, illustrant la flexibilité du SDD. C'est un exemple concret de la **Confirmation Gate** de CodexSpec — rien n'est définitif tant que vous ne l'avez pas explicitement confirmé, et une décision précédemment acceptée peut être rouverte et inversée au point de contrôle clarify.

---

## Étape 1 : clarification initiale des exigences (`/codexspec:specify`)

### Entrée utilisateur initiale

```
I want to add a feature to the project: a new Git-related command that generates accurate, detailed, and standards-compliant GitHub PR descriptions (or MR descriptions, for GitLab). Below are two PR commands I have used in other projects, provided for reference.

[Reference Example 1 - Structured Description]
Now, acting as a project maintainer, based on all the work we have done so far, write a clear Pull Request description for this submission.
The PR description should be aimed at the other reviewers on the team and include the following sections:
1. Context
2. Implementation
3. Testing
4. How to Verify

[Reference Example 2 - Simple Description]
Based on the code diff between the current branch and origin/main, use Markdown to produce a Merge Request title and description that comply with Git conventions. (Describe in Chinese.)
```

### Processus de clarification

**Q1 : Langue de sortie**

- Options : Suivre la configuration du projet / Chinois / Détection automatique
- **Choix utilisateur** : Suivre la configuration du projet (actuel : en)

**Q2 : Support des plateformes**

- Options : GitHub et GitLab toutes les deux / GitHub uniquement / Détection automatique
- **Choix utilisateur** : Détection automatique

**Q3 : Contenu de la description de PR**

- Options : Description structurée détaillée / Description concise / Modèle personnalisable
- **Choix utilisateur** : Description structurée détaillée (recommandé)

**Q4 : Condition de déclenchement**

- Options : Branche courante vs origin/main / Commits non poussés / Branche cible configurable
- **Choix utilisateur** : Branche cible configurable

**Q5 : Source Spec**

- Options : Privilégier spec.md / Informations git uniquement / Combiner toutes les sources
- **Choix utilisateur** : Combiner toutes les sources (recommandé)

**Q6 : Nommage**

- Options : codexspec.pr / codexspec.create-pr / codexspec.create-mr
- **Choix utilisateur** : codexspec.pr (recommandé)

**Q7 : Gestion d'une spec manquante**

- Options : Continuer la génération en sautant Context / Inviter l'utilisateur à créer d'abord une spec / Avertir et continuer
- **Choix utilisateur** : Continuer la génération en sautant Context

**Q8 : Mode de sortie**

- Options : Sortie terminal / Sauvegarde dans un fichier / Terminal + fichier optionnel
- **Choix utilisateur** : Terminal + fichier optionnel (recommandé)

**Q9 : Sections par défaut**

- Options : Context, Implementation, Testing, How to Verify (toutes sélectionnées)
- **Choix utilisateur** : Les quatre sections

**Q10 : Paramètres de la commande**

- **Choix utilisateur** : tous les paramètres sont optionnels
  - `--target-branch` : par défaut origin/main
  - `--output` : par défaut, sortie terminal uniquement si non précisé
  - `--sections` : par défaut si non précisé
  - `--no-spec` : sauter la recherche de spec.md

### Correction de la configuration de langue

**Retour utilisateur** : le comportement de langue doit correspondre à celui de la commande `/commit-staged` — honorer d'abord `language.commit` depuis `config.yml`, et ne se rabattre sur `language.output` que lorsque `language.commit` n'est pas défini.

**Résumé des exigences mis à jour** :

```
Language priority: language.commit > language.output > English (default)
```

---

## Étape 2 : générer le document de spécification (`/codexspec:generate-spec`)

### Structure du document généré

Le `spec.md` généré contient les sections suivantes :

- **Overview** : vue d'ensemble de la fonctionnalité
- **Goals** : 4 objectifs
- **User Stories** : 4 récits utilisateur avec critères d'acceptation
- **Functional Requirements** : 8 exigences (REQ-001 à REQ-008)
- **Command Parameters** : 4 définitions de paramètres
- **Non-Functional Requirements** : 3 exigences (performance, compatibilité, gestion des erreurs)
- **Acceptance Criteria (Test Cases)** : 10 cas de test
- **Edge Cases** : 6 cas limites
- **Output Format Example** : exemples PR GitHub et MR GitLab
- **Out of Scope** : fonctionnalités explicitement exclues
- **Dependencies** : dépendances
- **Related Commands** : commandes connexes

### Extrait d'exigence clé

```markdown
### REQ-003: Language Configuration
The command shall determine output language in the following priority order:
1. `language.commit` in `.codexspec/config.yml` (highest priority)
2. `language.output` in `.codexspec/config.yml` (fallback)
3. English (default if no configuration)
```

---

## Étape 3 : revue de la spécification (`/codexspec:review-spec`)

### Résultat de la revue

- **Statut global** : ✅ Pass
- **Score qualité** : 92/100
- **Disponibilité** : Ready for Planning

### Problèmes détectés

**Avertissements (Should Fix)** :

1. **SPEC-001** : la logique de découverte des fichiers de test n'est pas explicitement spécifiée
2. **SPEC-002** : en présence de plusieurs spec.md, choisir « le plus récemment modifié » peut être inexact

**Suggestions (Nice to Have)** :

1. Envisager l'ajout d'un paramètre `--title`
2. Ajouter une exigence de validation du format de sortie
3. Envisager le support des modèles d'URL GitHub Enterprise

### Emplacement du rapport de revue

`.codexspec/specs/2026-0613-1200ab-pr-description-generator/review-spec.md`

Il s'agit d'une **revue fondée sur des preuves** : chaque avertissement et suggestion ci-dessus est lié à une lacune concrète et identifiable de la spec, et les éléments consultatifs (Nice to Have) n'affectent ni l'acceptation ni les modifications automatiques.

---

## Étape 4 : clarification et ajustement des exigences (`/codexspec:clarify`) — tournant critique

### Problème découvert

**Retour utilisateur** :
> Je me suis rendu compte d’un problème dans l’utilisation de spec.md. Un utilisateur peut, par exemple, effectuer une modification très limitée sans suivre le flux standard de CodexSpec, specify → plan → tasks → implement. Il peut avoir travaillé directement par conversation ou avec le mode plan intégré à Claude Code, puis vouloir appeler séparément une commande CodexSpec pour produire une description de PR conforme aux conventions. Dans ce cas, choisir par défaut le fichier spec.md modifié le plus récemment risque d’intégrer le contenu d’une ancienne spécification sans rapport avec la modification en cours.

C'est la **Confirmation Gate** en action : la décision antérieure (« par défaut, le spec.md le plus récemment modifié ») avait été enregistrée, mais elle n'était pas définitive au sens d'irréversible — l'utilisateur l'a rouverte au point de contrôle clarify avec une nouvelle information sur un cas d'usage réel, et la valeur par défaut précédemment acceptée a été inversée.

### Processus de Q&R de clarification

**Q1 : Stratégie de sélection de spec**

**Contexte** : l'EC-004 actuel dit « plusieurs spec.md → utiliser le plus récemment modifié ». Mais lorsqu'un utilisateur fait un petit changement sans suivre le flux SDD, le spec.md le plus récent peut n'avoir aucun lien avec le changement courant.

| Option | Description |
|--------|-------------|
| A | Ne pas utiliser spec.md par défaut, sauf si l'utilisateur passe explicitement `--spec` |
| B | Correspondance par nom de branche |
| C | Inviter l'utilisateur à choisir |
| D | Correspondance par changements de fichiers |

**Choix utilisateur** : Option A
**Raison** : évite les références erronées ; le paramètre `--spec` permet aux utilisateurs qui veulent l'intégration SDD de l'acter explicitement.

---

**Q2 : Stratégie d'extraction du contenu de spec**

**Contexte** : lorsque l'utilisateur passe `--spec`, que se passe-t-il si la structure de spec.md est incomplète ?

| Option | Description |
|--------|-------------|
| A | Extraction au mieux, sauter les sections manquantes |
| B | Avertir et sauter Context |
| C | Exiger une structure complète, sinon échouer |

**Choix utilisateur** : Option A
**Raison** : éviter qu'un problème de format de spec ne bloque le flux de travail.

---

**Q3 : Découverte des fichiers de test**

**Contexte** : comment la section Testing doit-elle découvrir les fichiers de test ?

| Option | Description |
|--------|-------------|
| A | Motifs de répertoires courants (tests/, test/) |
| B | Heuristiques indépendantes du langage (répertoire + motifs de noms de fichiers) |
| C | Pas de découverte active ; inférer uniquement depuis les messages de commit |

**Choix utilisateur** : Option B
**Raison** : couvre une variété de structures de projet dans différents langages.

---

**Q4 : Génération du titre de PR**

**Contexte** : comment le titre de PR doit-il être généré ?

| Option | Description |
|--------|-------------|
| A | D'abord l'analyse du nom de branche |
| B | D'abord le premier message de commit |
| C | Synthèse (git diff + nom de branche + messages de commit) |

**Choix utilisateur** : Option C
**Raison utilisateur** : le premier commit peut ne représenter qu'une petite partie du changement, et les noms de branche supposent une forte discipline de nommage. Avec des informations git substantielles et des changements de code disponibles comme référence, l'analyse synthétisée est plus précise.

---

**Q5 : Génération des commandes de vérification**

**Contexte** : comment la section « How to Verify » doit-elle générer les commandes de vérification ?

| Option | Description |
|--------|-------------|
| A | Modèles génériques |
| B | Détection de projet (pyproject.toml → pytest, package.json → npm test) |
| C | Inférer depuis les messages de commit |

**Choix utilisateur** : Option B
**Raison** : la détection de projet produit des commandes de vérification plus pratiques.

---

### Résumé de la session de clarification

| Question | Décision | Impact |
|----------|----------|--------|
| Stratégie de sélection de spec | Opt-in via `--spec` | REQ-007, EC-004, table des paramètres |
| Extraction du contenu de spec | Extraction au mieux | REQ-005b, EC-004c |
| Découverte des fichiers de test | Heuristiques indépendantes du langage | REQ-006b |
| Génération du titre de PR | Analyse synthétisée | REQ-008a |
| Génération des commandes de vérification | Détection des fichiers projet | REQ-010 |

### Changement clé : inversion de la logique des paramètres

```
Original design: --no-spec (skip spec)
New design:      --spec (enable spec, opt-in)
```

Cette inversion est l'illustration la plus claire de la Confirmation Gate dans cette étude de cas : une valeur par défaut à l'origine « engageante » (`--no-spec`, i.e. spec activée par défaut) a été rouverte, inversée et re-confirmée comme opt-in une fois que l'utilisateur a fait émerger un flux de travail réel qu'elle aurait cassé.

---

## Étape 5 : plan d'implémentation technique (`/codexspec:design-to-plan`)

### Vue d'ensemble du plan

**Approche d'implémentation** : fichier de modèle Markdown (cohérent avec `/codexspec:commit-staged`)

**Aucune nouvelle dépendance** — la fonctionnalité est livrée via un modèle de slash command et ne nécessite aucun code Python.

### Résumé des décisions techniques

| Décision | Choix | Raison |
|----------|-------|--------|
| Approche d'implémentation | Modèle Markdown | Cohérent avec les commandes existantes, facile à maintenir |
| Priorité de langue | commit > output > en | Cohérent avec `/commit-staged` |
| Détection de plateforme | Analyse de l'URL distante | Simple et fiable |
| Intégration spec | Opt-in (`--spec`) | Évite les références erronées |
| Extraction du contenu | Au mieux | Ne bloque pas le flux de travail |
| Découverte des tests | Motifs répertoire + nom de fichier | Indépendant du langage |
| Génération du titre | Analyse synthétisée | La plus précise |
| Détection de commande | Détection des fichiers projet | Plus pratique |
| Mode de sortie | Terminal d'abord, fichier optionnel | Flexible |

### Phases d'implémentation

1. **Phase 1** : création du modèle (YAML frontmatter, configuration de langue, contexte Git)
2. **Phase 2** : fonctionnalité principale (intégration spec, découverte des tests, détection de commande, génération du titre)
3. **Phase 3** : gestion des cas limites
4. **Phase 4** : tests
5. **Phase 5** : mise à jour de la documentation

### Manifeste des fichiers

**Créés** :

- `templates/commands/pr.md`

**Modifiés** :

- `CLAUDE.md` - ajouter la description de la commande
- `README.md` - ajouter la commande à la liste

**Tests** :

- `tests/test_pr_template.py`

---

## Diagramme de flux complet

```
┌─────────────────────────────────────────────────────────────────────────┐
│                   CodexSpec SDD Development Flow                        │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│  /codexspec:specify                                                     │
│  ├─ Clarify requirements through Q&A                                    │
│  ├─ User provides reference examples                                    │
│  └─ 10 questions covering language, platform, content, parameters, etc. │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│  /codexspec:generate-spec                                               │
│  ├─ Generate a complete spec.md                                         │
│  ├─ 4 user stories, 8 functional requirements, 10 test cases            │
│  └─ Saved to .codexspec/specs/2026-0613-1200ab-pr-description-generator/spec.md │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│  /codexspec:review-spec                                                 │
│  ├─ Quality score: 92/100                                               │
│  ├─ Found 2 warnings (test-file discovery, multi-spec handling)         │
│  └─ Status: Pass, can proceed to planning                               │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│  /codexspec:clarify  (Critical adjustment)                              │
│  ├─ User surfaces a real-world usage issue                              │
│  ├─ 5 clarification questions, all answered                             │
│  ├─ Key change: --no-spec → --spec (opt-in)                             │
│  └─ Added 5 requirements (REQ-005b, 006b, 008a, 010, updated 007)       │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│  /codexspec:design-to-plan                                                │
│  ├─ Update the technical implementation plan                            │
│  ├─ 9 technical decisions, including 5 new ones                         │
│  ├─ 5 implementation phases                                             │
│  └─ Saved to .codexspec/specs/2026-0613-1200ab-pr-description-generator/plan.md │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│  Subsequent steps (not completed in this session)                       │
│  ├─ /codexspec:review-plan - Validate plan quality                      │
│  ├─ /codexspec:plan-to-tasks - Break down into executable tasks         │
│  └─ /codexspec:implement-tasks - Execute the implementation             │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## Enseignements clés

### 1. La valeur de l'étape clarify

Ce cas montre le rôle pivot de la commande `clarify` :

- **L'utilisateur découvre un vrai problème à l'usage** — le risque d'un mauvais usage de spec.md dans les scénarios de petits changements
- **Un défaut de conception est corrigé par Q&R de clarification** — passage de l'auto-détection à l'opt-in
- **Les changements d'exigences sont enregistrés systématiquement** — toutes les modifications sont sauvegardées dans la section Clarifications de spec.md

### 2. Flexibilité du flux SDD

- Ce n'est pas un flux linéaire ; vous pouvez revenir en arrière et ajuster à n'importe quelle étape
- `clarify` peut être inséré après `review-spec` et avant `design-to-plan`
- Le document de spécification et le plan technique sont tous deux mis à jour pour refléter le changement

### 3. Évolution de la conception des paramètres

```
Initial design:
  --no-spec: skip spec.md (used by default)

Final design:
  --spec: enable spec.md (not used by default)
```

Ce changement reflète un recentrage de la conception, passant d'un « flux SDD par défaut » à un dispositif qui « prend aussi en charge les flux non-SDD », rendant l'outil plus généraliste.

### 4. Sorties documentaires

| Étape | Fichier produit | Contenu |
|-------|-----------------|---------|
| generate-spec | spec.md | Document de spécification complet |
| review-spec | review-spec.md | Rapport de revue qualité |
| clarify | (met à jour spec.md) | Enregistrements de clarification + mises à jour d'exigences |
| design-to-plan | plan.md | Plan d'implémentation technique |

---

## Annexe : aide-mémoire des commandes

```bash
# 1. Initial requirement clarification
/codexspec:specify

# 2. Generate the specification document
/codexspec:generate-spec

# 3. Review the specification quality
/codexspec:review-spec

# 4. Clarify/adjust requirements (optional; use when an issue is found)
/codexspec:clarify [issue description]

# 5. Generate the technical plan
/codexspec:design-to-plan

# 6. Review the plan quality (optional)
/codexspec:review-plan

# 7. Break down into tasks
/codexspec:plan-to-tasks

# 8. Execute the implementation
/codexspec:implement-tasks
```

---

*Ce document a été généré par le flux de travail SDD de CodexSpec et retrace une véritable conversation de développement.*

<a id="available-commands"></a>

# Commandes disponibles

La CLI possède six commandes publiques. Les intégrations d'agents distribuent
28 commandes : Claude utilise `/codexspec:<name>` et Codex, `$codexspec:<name>`.
Les tableaux suivants présentent la notation de Claude pour faciliter la lecture.

<a id="cli-commands"></a>

## Commandes CLI

| Commande | Objectif |
|---------|---------|
| `codexspec init` | Initialiser ou actualiser un projet pour Claude, Codex ou les deux |
| `codexspec check` | Vérifier les outils et dépendances installés |
| `codexspec version` | Afficher la version et les informations système |
| `codexspec config` | Consulter ou modifier la configuration du projet |
| `codexspec list-commands` | Afficher les commandes d'agent disponibles par catégorie |
| `codexspec show-blueprint` | Afficher le blueprint du worktree partagé sans le modifier |

<a id="core-workflow-commands"></a>

## Commandes du flux de travail principal

| Commande | Objectif |
|---------|---------|
| `/codexspec:constitution` | Créer ou mettre à jour les principes du projet et les valider entre artefacts |
| `/codexspec:specify` | Discuter des exigences d'une fonctionnalité, les confirmer et les enregistrer |
| `/codexspec:blueprint` | Préparer ou maintenir les exigences confirmées en attente du blueprint |
| `/codexspec:generate-spec` | Élaborer une spécification traçable à partir des exigences confirmées, avec revue automatique |
| `/codexspec:spec-to-design` | Définir l'architecture, les composants, les interfaces et les décisions, avec revue automatique |
| `/codexspec:design-to-plan` | Planifier les phases d'implémentation, leur ordre et leur vérification, avec revue automatique |
| `/codexspec:plan-to-tasks` | Élaborer des tâches vérifiables couvrant les artefacts en amont, avec revue automatique et analyze |
| `/codexspec:implement-tasks` | Exécuter les tâches, vérifier les résultats, effectuer les revues et les corrections |
| `/codexspec:auto-dev` | Développer de façon autonome les exigences confirmées du blueprint dans l'ordre du document |

<a id="artifact-review-commands"></a>

## Commandes de revue des artefacts

| Commande | Objectif |
|---------|---------|
| `/codexspec:review-spec` | Vérifier la fidélité et la qualité interne de la spécification |
| `/codexspec:review-design` | Vérifier la fidélité et la faisabilité de la conception, ainsi que sa préparation à la planification |
| `/codexspec:review-plan` | Vérifier la fidélité et la faisabilité du plan, ainsi que sa préparation à l'implémentation |
| `/codexspec:review-tasks` | Vérifier la fidélité, les dépendances, le caractère exécutable et la vérification des tâches |

<a id="requirements-existing-code-and-debugging"></a>

## Exigences, code existant et débogage

| Commande | Objectif |
|---------|---------|
| `/codexspec:clarify` | Résoudre les ambiguïtés des exigences en les mettant à jour avant la spécification |
| `/codexspec:analyze` | Vérifier la traçabilité de bout en bout et aligner les artefacts dérivés sur les sources qui font autorité |
| `/codexspec:checklist` | Générer une liste de contrôle de la qualité des exigences |
| `/codexspec:tasks-to-issues` | Convertir les tâches existantes en issues GitHub avec des actions concrètes |
| `/codexspec:debug` | Rechercher la cause racine avant d'appliquer une correction |
| `/codexspec:reverse-spec` | Examiner l'architecture existante, rédiger des brouillons d'artefacts de modules ou signaler une dérive par rapport à la base confirmée |

<a id="project-knowledge-commands"></a>

## Commandes de gestion des connaissances du projet

| Commande | Objectif |
|---------|---------|
| `/codexspec:distill` | Recueillir des connaissances réutilisables ou examiner les entrées candidates dans l'espace de travail local |
| `/codexspec:evolve` | Élaborer un brouillon de contribution au projet amont à partir de connaissances validées |
| `/codexspec:onboard` | Déduire des conventions candidates et des contraintes étayées du code existant |

<a id="git-and-code-review-commands"></a>

## Commandes Git et de revue du code

| Commande | Objectif |
|---------|---------|
| `/codexspec:commit-staged` | Générer des messages à partir des changements indexés ; prévisualiser ou exécuter un commit autorisé |
| `/codexspec:pr` | Générer une description structurée de PR/MR |
| `/codexspec:release-notes` | Maintenir une entrée du journal des changements et produire le texte d'une publication à partir de l'historique Git |
| `/codexspec:review-code` | Examiner les changements sélectionnés comme contrôle de défauts ; utiliser `--audit` pour évaluer la qualité dans les chemins indiqués |

<a id="utility-commands"></a>

## Commandes utilitaires

| Commande | Objectif |
|---------|---------|
| `/codexspec:config` | Créer, consulter, modifier ou réinitialiser la configuration du projet de façon interactive |
| `/codexspec:quick` | Exécuter un flux SDD bref avec priorité aux exigences pour les petits changements |

Les anciennes entrées de revue Python/React sont conservées pour la compatibilité du plugin et ne font pas partie des 28 commandes installées. Utilisez `review-code`, qui charge les critères pertinents du langage ou du framework, et `--audit` pour évaluer des chemins.

## Référence des commandes

### `/codexspec:constitution`

Crée ou met à jour la constitution du projet. La constitution définit les principes architecturaux, la pile technologique, les standards de code et les règles de gouvernance qui guident toutes les décisions de développement ultérieures.

**Syntaxe :**

```
/codexspec:constitution [principles description]
```

**Arguments :**

| Argument | Requis | Description |
|----------|--------|-------------|
| `principles description` | Non | Description des principes à inclure (vous serez sollicité si non fournie) |

**Ce qu'elle fait :**

- Crée `.codexspec/memory/constitution.md` s'il n'existe pas
- Met à jour la constitution existante avec les nouveaux principes
- Valide la cohérence entre artefacts avec les templates
- Génère un rapport d'impact de synchronisation montrant les changements et les fichiers affectés
- Inclut une revue de constitutionnalité pour les templates dépendants

**Ce qu'elle crée :**

```
.codexspec/
└── memory/
    └── constitution.md    # Project governance document
```

**Exemple :**

```text
You: /codexspec:constitution Focus on code quality, testing standards, and clean architecture

AI:  Creating constitution...

     ✓ Created .codexspec/memory/constitution.md
     Version: 1.0.0

     Sync Impact Report:
     - plan-template-*.md: ✅ aligned
     - spec-template-*.md: ✅ aligned
     - tasks-template-*.md: ✅ aligned

     Core Principles:
     1. Code Quality First
     2. Test-Driven Development
     3. Clean Architecture

     Suggested commit: docs: create constitution v1.0.0
```

**Conseils :**

- Définissez les principes tôt dans le projet pour des décisions cohérentes
- Incluez à la fois des principes techniques et de processus
- Revoyez la constitution avant toute fonctionnalité majeure
- Les changements de constitution déclenchent une validation entre artefacts

---

### `/codexspec:specify`

Clarifie les exigences via un échange interactif de questions/réponses, confirme le résumé qui en résulte et le conserve pour les sessions suivantes.

**Syntaxe :**

```
/codexspec:specify [your idea or requirement]
```

**Arguments :**

| Argument | Requis | Description |
|----------|--------|-------------|
| `your idea or requirement` | Non | Description initiale de ce que vous souhaitez construire (vous serez sollicité si non fournie) |

**Ce qu'elle fait :**

- Pose des questions de clarification pour comprendre votre idée
- Explore les cas limites auxquels vous n'auriez peut-être pas pensé
- Co-crée des exigences de haute qualité via le dialogue
- Se concentre sur le « quoi » et le « pourquoi », pas sur l'implémentation technique
- Attribue des identifiants stables aux besoins, contraintes, décisions, exclusions et questions ouvertes confirmés
- Consigne les preuves de l'utilisateur et un journal de confirmation
- Crée l'espace de travail de la fonctionnalité et `requirements.md`

**Ce qu'elle crée :**

```text
.codexspec/specs/{feature-id}-{feature-name}/requirements.md
```

Seuls les éléments confirmés deviennent des exigences faisant autorité. Les questions ouvertes restent explicitement ouvertes. Il s'agit de la Confirmation Gate pour les exigences : rien n'engage tant que vous n'avez pas explicitement confirmé le résumé final.

**Exemple :**

```text
You: /codexspec:specify I want to build a task management app

AI:  Great! Let me help you clarify the requirements.

     First, who are the target users for this app?
     - Individual professionals
     - Small teams
     - Enterprise organizations
     - All of the above

You: Small teams, mainly software development teams

AI:  Got it. For small dev teams:
     - Do you need real-time collaboration features?
     - Should tasks support sub-tasks or just flat lists?
     - Any integration requirements (GitHub, Slack, etc.)?

You: Real-time is important. Sub-tasks yes. GitHub integration would be nice.

AI:  [Continues exploring requirements...]

     Summary of clarified requirements:
     - Target: Small dev teams (5-20 people)
     - Core: Tasks with sub-tasks, real-time updates
     - Integration: GitHub (optional)
     - Priority: Real-time collaboration > Sub-tasks > GitHub

     Ready to generate the spec document?
     Use /codexspec:generate-spec to create spec.md
```

**Conseils :**

- À utiliser pour l'exploration initiale des exigences
- Ne cherchez pas l'exhaustivité — l'affinage est itératif
- Posez des questions si l'IA fait des suppositions
- Revoyez le résumé avant de générer la spec

---

### `/codexspec:blueprint`

Utilisez `blueprint` pour préparer plusieurs exigences confirmées avant le
développement, puis `auto-dev` pour développer cette file :

```text
/codexspec:blueprint Add a confirmed requirement for task reminders
/codexspec:auto-dev
```

Avant qu'une exigence soit ajoutée à la file du blueprint, les orientations,
les choix et les contraintes qui relèvent de l'utilisateur sont résolus.
Le fichier partagé `.codexspec/blueprint.md` utilise les états `pending`,
`in_progress` et `completed`. Vous pouvez ajouter, remplacer, supprimer ou
réordonner les exigences en attente. Lors de la maintenance du blueprint,
les entrées en cours et terminées restent en lecture seule.

Auto-dev développe les exigences dans l'ordre du document. Il reprend la
fonctionnalité en cours avant d'en commencer une autre et relit la file après
chaque achèvement, ce qui permet aux nouvelles exigences en attente de rejoindre
l'exécution. Il réalise les étapes SDD, l'implémentation, la vérification, la
revue et les corrections dans le cadre des exigences confirmées. L'appel à
`auto-dev` active son automatisation indépendamment de `workflow.auto_next`,
sans modifier ce paramètre.

Les deux commandes partagent `worktree-for-codexspec-auto-dev`, sur la branche
`codexspec/auto-dev`. Elles peuvent s'exécuter simultanément grâce aux mécanismes
communs qui contrôlent l'attribution de l'espace de travail et protègent les
écritures ; les exigences y sont développées une à une. Si un choix de produit ne peut pas être résolu à
partir des exigences confirmées, l'exécution s'arrête en présentant les éléments
qui le justifient, au lieu de poser des questions pendant le fonctionnement
autonome normal.

Pour consulter le blueprint partagé sans le modifier :

```bash
codexspec show-blueprint
```

---

### `/codexspec:generate-spec`

Élaborer une spécification traçable à partir des exigences confirmées, avec revue automatique.

**Syntaxe :**

```
/codexspec:generate-spec
```

**Arguments :**

| Argument | Requis | Description |
|----------|--------|-------------|
| Chemin de la fonctionnalité | Non | Répertoire de fonctionnalité explicite, `requirements.md` ou `spec.md` cible ; requis lorsque la résolution est ambiguë |

**Ce qu'elle fait :**

- Lit les exigences confirmées depuis l'espace de travail de fonctionnalité sélectionné
- Prend en charge les espaces de travail hérités ne contenant que `spec.md`, avec un avertissement explicite de traçabilité
- Génère un `spec.md` complet avec :
  - Vue d'ensemble et objectifs de la fonctionnalité
  - User stories avec critères d'acceptation
  - Exigences fonctionnelles (format REQ-XXX)
  - Exigences non fonctionnelles (format NFR-XXX)
  - Cas limites et approches de traitement
  - Éléments hors périmètre
- Ajoute des références `Sources` vers les identifiants d'exigence
- S'arrête pour confirmation utilisateur au lieu de résoudre les conflits d'autorité par supposition
- Examine automatiquement et peut corriger les défauts étayés par des preuves pendant deux tours au maximum

**Ce qu'elle crée :**

```
.codexspec/
└── specs/
    └── 2026-0613-1200ab-task-management/
        └── spec.md
```

**Exemple :**

```text
You: /codexspec:generate-spec

AI:  Generating specification...

     ✓ Created .codexspec/specs/2026-0613-1200ab-task-management/spec.md

     Sections included:
     - Overview: Task management for small dev teams
     - 4 User Stories with acceptance criteria
     - 12 Functional Requirements (REQ-001 to REQ-012)
     - 3 Non-Functional Requirements (NFR-001 to NFR-003)
     - 5 Edge Cases documented
     - Out of Scope: Mobile apps, Enterprise SSO

     Next steps:
     - Review the spec with /codexspec:review-spec
     - Or proceed to /codexspec:spec-to-design
```

---

### `/codexspec:spec-to-design`

Lit les fichiers `requirements.md` et `spec.md` confirmés, les principes du projet et les faits pertinents du dépôt. Produit un `design.md` décrivant composants, interfaces, flux de données, alternatives et décisions, avec des liens vers les exigences en amont. Lance automatiquement `review-design`. Le travail s’arrête si un choix modifie l’intention confirmée ou exige une nouvelle décision de l’utilisateur.

```text
/codexspec:spec-to-design <feature-dir>
```

---

### `/codexspec:design-to-plan`

Transforme la conception confirmée en plan de mise en œuvre. Exécutez d’abord `spec-to-design` pour définir l’architecture, les composants, les interfaces et les choix technologiques.

```text
/codexspec:design-to-plan [design.md | spec.md | feature-directory]
```

Lit `requirements.md`, `spec.md`, `design.md` et la constitution. Planifie les phases, leur ordre et la vérification en s’appuyant sur la conception, sans redéfinir le système. Chaque composant du plan porte `Covers: REQ-xxx; Design: <design component>`.

Produit `plan.md` et lance `review-plan`. Si `auto_next` est activé, une revue réussie déclenche `plan-to-tasks`. Toute décision modifiant l’intention confirmée exige une confirmation. Un chemin explicite prime sur la branche de fonctionnalité courante ; toute ambiguïté exige une sélection. Les anciennes fonctionnalités sans `design.md` peuvent toujours être planifiées à partir de `spec.md`.

---

### `/codexspec:plan-to-tasks`

Découpe le plan technique en tâches actionnables avec une couverture explicite et des résultats vérifiables.

**Syntaxe :**

```
/codexspec:plan-to-tasks [path_to_spec.md path_to_plan.md]
```

**Arguments :**

| Argument | Requis | Description |
|----------|--------|-------------|
| `paths` | Non | Chemins vers spec et plan (détectés automatiquement si non fournis) |

**Ce qu'elle fait :**

- Crée des tâches avec un résultat vérifiable unique ; une tâche peut toucher plusieurs fichiers liés
- N'utilise un ordre test-first que lorsque le plan, la constitution, les besoins confirmés ou le risque l'exigent
- Marque les tâches `[P]` uniquement lorsqu'elles sont réellement indépendantes
- Spécifie les chemins exacts des fichiers pour chaque tâche
- Ajoute des liens `Covers` vers le plan et les identifiants d'exigence

**Ce qu'elle crée :**

```
.codexspec/
└── specs/
    └── 2026-0613-1200ab-task-management/
        └── tasks.md    # Task breakdown
```

**Structure des tâches :**

```markdown
### Task 2.1: Write Tests for Entity A [P]
- **Type**: Testing
- **Files**: `tests/test_entity_a.py`
- **Description**: Write unit tests for Entity A
- **Dependencies**: Task 1.3
- **Est. Complexity**: Low
```

**Exemple :**

```text
You: /codexspec:plan-to-tasks

AI:  Breaking down plan into tasks...

     ✓ Created tasks.md
     Total: 24 tasks
     Parallelizable: 8 tasks (33%)

     Phase 1: Foundation (4 tasks)
     Phase 2: Core Implementation - TDD (10 tasks)
     Phase 3: Integration (4 tasks)
     Phase 4: Interface Layer (3 tasks)
     Phase 5: Testing & Documentation (3 tasks)

     Execution Order:
     Phase 1 → [Phase 2 tasks in parallel groups] → Phase 3 → Phase 4 → Phase 5

     Checkpoints defined at each phase boundary.
```

**Conseils :**

- Chaque tâche doit produire un résultat vérifiable unique et peut toucher des fichiers étroitement liés
- Les tâches de test précèdent l'implémentation uniquement lorsque le test-first est requis
- `[P]` marque les tâches réellement indépendantes et parallélisables
- Revoyez les dépendances avant l'implémentation

Après la rédaction des tâches, `review-tasks` est exécuté. Un résultat `PASS` ou `PASS_WITH_WARNINGS` déclenche `analyze` une seule fois ; cette analyse n’ajoute pas de condition bloquante à l’achèvement. Les tâches couvrent les exigences confirmées, la spécification, la conception et le plan.

---

### `/codexspec:implement-tasks`

Exécuter les tâches, vérifier les résultats, effectuer les revues et les corrections.

```text
/codexspec:implement-tasks <feature-dir>
```

Les quatre revues d'artefacts — `review-spec`, `review-design`, `review-plan`
et `review-tasks` — vérifient la fidélité, la couverture, la faisabilité et la
qualité interne. Elles s'exécutent automatiquement après la génération et
peuvent aussi être lancées manuellement. Les rapports distinguent les défauts
vérifiés des avertissements sur les risques qui ne bloquent pas la progression
et des possibilités de conception ; ils incluent un score de compatibilité.

`review-code` propose un contrôle de défauts distinct portant sur les changements,
ainsi qu'une évaluation explicite de la qualité du code dans son ensemble :

```text
/codexspec:review-code --feature <feature-dir>
/codexspec:review-code --uncommitted
/codexspec:review-code --audit src/
```

La revue par défaut couvre tous les changements de la branche de la
fonctionnalité : ceux déjà committés, ceux indexés, ceux non indexés et les
fichiers non suivis qui ne sont pas ignorés. Vous pouvez sélectionner
explicitement les changements committés, non committés ou ceux d'un seul commit.
`--feature` ajoute le contexte des exigences sans réduire le périmètre Git.
`--audit` évalue les chemins indiqués et produit une grille indicative de qualité
plutôt qu'un verdict d'achèvement.

Les revues chargent les normes communes depuis `.codexspec/review-code/` et
sélectionnent les dimensions de comportement ainsi que les vérifications de
langage ou de framework pertinentes. Chaque constat doit être étayé par des
éléments concrets, une condition qui peut se produire, un lien démontré avec
les changements sélectionnés et un impact. L'agent de revue signale les défauts
et les suggestions de maintenance étayées sans modifier les fichiers ; le
processus chargé des corrections les vérifie de façon indépendante.

Pour les tâches de code, l'implémentation commence par les tests. La documentation
et la configuration sont modifiées directement, avec les vérifications adaptées.
Après une correction, la revue incrémentale peut réutiliser la couverture qui
n'a pas été affectée. L'acceptation finale exige une nouvelle revue de toute
la fonctionnalité avec un résultat `PASS`, une couverture et une vérification
complètes, et aucun défaut P0–P3 admis. Les suggestions de maintenance étayées
sont présentées séparément.

La valeur par défaut de `workflow.auto_maintenance` est **true**. Ce paramètre
détermine si les processus de correction appliquent aussi des améliorations de
maintenance vérifiées et compatibles. Si vous le désactivez, ces suggestions
restent signalées et les corrections des défauts ainsi que les vérifications
requises restent obligatoires. Ce paramètre est indépendant du passage à
l'étape suivante et n'est pas un argument de `implement-tasks`.

Pour commencer le débogage par la recherche de la cause racine :

```text
/codexspec:debug Investigate intermittent failures when saving a task
```

Debug suit cette séquence : investigation → analyse des motifs récurrents →
vérification d'une seule hypothèse → correction précédée d'un test en échec.
Pendant l'implémentation, ce processus est utilisé lorsque les corrections
n'aboutissent pas, qu'un défaut de fonctionnement non trivial doit être retracé
ou que le même type de cause racine réapparaît au fil des revues. Trois tentatives
de correction infructueuses déclenchent une réévaluation de l'architecture.

Utilisez `checklist` pour évaluer la clarté, l'exhaustivité et la cohérence des exigences :

```text
/codexspec:checklist Check the authentication requirements for completeness
```

La [référence des commandes](commands.md) détaille les
sélecteurs de revue, les arguments et les procédures.

---

### `/codexspec:auto-dev`

Développer de façon autonome les exigences confirmées du blueprint dans l'ordre du document.

Voir [`blueprint`](#codexspecblueprint).

```text
/codexspec:auto-dev
```

---

### `/codexspec:review-spec`

Valide la spécification vis-à-vis des exigences confirmées et de sa propre qualité interne.

**Syntaxe :**

```
/codexspec:review-spec [path_to_spec.md]
```

**Arguments :**

| Argument | Requis | Description |
|----------|--------|-------------|
| `path_to_spec.md` | Non | Chemin vers le fichier spec (détecté automatiquement si non fourni) |

**Ce qu'elle fait :**

- Vérifie la fidélité aux entrées confirmées de `requirements.md`
- Contrôle la cohérence interne, la clarté et la vérifiabilité
- Ne traite l'absence d'une section de template comme un défaut que lorsque le contenu faisant autorité l'exige
- Exige de chaque défaut qu'il inclue `Evidence`, `Location`, `Mismatch`, `Impact` et `Remediation`
- Sépare les `Risk Advisories / Design Opportunities` des défauts
- Génère un statut ainsi qu'un score de compatibilité dérivé des constats classés

**Contrat de revue partagé :**

| Catégorie | Signification |
|-----------|---------------|
| Défaut de fidélité | Conflit avec une source faisant autorité ou omission de celle-ci |
| Défaut intrinsèque | Contradiction interne, infaisabilité ou non-vérifiabilité |
| Avis consultatif | Amélioration facultative sans preuve d'un défaut actuel |

Le statut est `PASS`, `PASS_WITH_WARNINGS`, `NEEDS_REVISION` ou `BLOCKED`. Les avis ne modifient jamais le statut ni le score.

**Exemple :**

```text
You: /codexspec:review-spec

AI:  Overall Status: NEEDS_REVISION
     Compatibility Score: 79/100

     Warning SPEC-001
     Evidence: CON-002 requires a measurable response-time limit.
     Location: spec.md, REQ-006
     Mismatch: "Respond quickly" has no measurable threshold.
     Impact: Acceptance cannot be verified.
     Remediation: Ask the user to confirm a threshold, update requirements.md,
                  then synchronize REQ-006.

     Risk Advisories / Design Opportunities:
     - None
```

**Conseils :**

- Lancez-la avant `/codexspec:spec-to-design`
- Considérez `BLOCKED` et `NEEDS_REVISION` comme non prêts à continuer
- Ne transformez pas les avis en exigences
- Relancez après avoir appliqué des correctifs

---

### `/codexspec:review-design`

Vérifie la fidélité et la faisabilité de `design.md`, ainsi que son aptitude à servir de base à la planification, au regard des exigences confirmées et de la spécification. Sépare les défauts étayés des améliorations de conception facultatives et applique les mêmes statuts et limites de correction que les autres revues d’artefacts.

```text
/codexspec:review-design <feature-dir>
```

---

### `/codexspec:review-plan`

Examine le plan technique d'implémentation sous l'angle de la fidélité, de la faisabilité et de la justification des décisions techniques.

**Syntaxe :**

```
/codexspec:review-plan [path_to_plan.md]
```

**Arguments :**

| Argument | Requis | Description |
|----------|--------|-------------|
| `path_to_plan.md` | Non | Chemin vers le fichier plan (détecté automatiquement si non fourni) |

**Ce qu'elle fait :**

- Vérifie les liens `Covers` et la couverture obligatoire de la spec
- Contrôle les règles de constitution applicables et les faits du dépôt
- Signale une complexité injustifiée uniquement lorsqu'elle crée un coût ou un conflit concret
- Exige les champs de preuve pour chaque défaut et fusionne les constats partageant la même cause racine
- Rapporte les améliorations architecturales facultatives sous forme d'avis
- Utilise le contrat partagé de statut et de score de compatibilité

**Exemple :**

```text
You: /codexspec:review-plan

AI:  Overall Status: PASS
     Compatibility Score: 100/100
     Verified defects: none

     Risk Advisories / Design Opportunities:
     - A caching layer may become useful if production measurements exceed
       the confirmed latency target. It is not required by the current plan.
```

**Conseils :**

- Lancez-la avant `/codexspec:plan-to-tasks`
- Résolvez les défauts étayés par des preuves avant la génération des tâches
- Conservez les idées architecturales spéculatives dans la section des avis
- Vérifiez que la pile technologique correspond aux compétences de l'équipe

Le plan met en œuvre le `design.md` confirmé, sans rouvrir les choix d’architecture. La revue vérifie ses références à la conception ainsi que la couverture des exigences.

---

### `/codexspec:review-tasks`

Valide le découpage en tâches sous l'angle de la couverture, des résultats vérifiables, de l'ordonnancement correct et de la faisabilité des dépendances.

**Syntaxe :**

```
/codexspec:review-tasks [path_to_tasks.md]
```

**Arguments :**

| Argument | Requis | Description |
|----------|--------|-------------|
| `path_to_tasks.md` | Non | Chemin vers le fichier tasks (détecté automatiquement si non fourni) |

**Ce qu'elle fait :**

- Vérifie que tous les éléments requis du plan et des exigences disposent d'une couverture par tâche
- Ne valide l'ordre test-first que lorsqu'une source faisant autorité l'exige
- Vérifie que chaque tâche a un résultat unique contrôlable
- Valide les dépendances (pas de cycles, ordre correct)
- Revoyez les marqueurs de parallélisation
- Valide les chemins de fichiers
- Exige les champs de preuve pour chaque défaut
- Rapporte les affinages de processus facultatifs sous forme d'avis
- Utilise le contrat partagé de statut et de score de compatibilité

**Exemple :**

```text
You: /codexspec:review-tasks

AI:  Overall Status: NEEDS_REVISION
     Compatibility Score: 79/100

     Warning TASK-001
     Evidence: Task 2.5 declares a dependency on Task 2.4.
     Location: tasks.md, Task 2.5
     Mismatch: Task 2.5 is also marked [P].
     Impact: Parallel execution can start before its prerequisite completes.
     Remediation: Remove [P] or remove the dependency if the plan proves independence.
```

**Conseils :**

- Lancez-la avant `/codexspec:implement-tasks`
- Les constats d'ordre des tests ne sont des défauts que lorsqu'une source faisant autorité requiert le test
- Vérifiez l'exactitude des marqueurs de parallélisation
- Contrôlez que les chemins de fichiers correspondent à la structure du projet

---

### `/codexspec:clarify`

Scanne une spécification existante pour détecter les ambiguïtés et les lacunes. À utiliser pour l'affinage itératif après la création initiale de la spec.

**Syntaxe :**

```
/codexspec:clarify [path_to_spec.md]
```

**Arguments :**

| Argument | Requis | Description |
|----------|--------|-------------|
| `path_to_spec.md` | Non | Chemin vers le fichier spec (détecté automatiquement si non fourni) |

**Ce qu'elle fait :**

- Scanne les exigences et la spec en utilisant des catégories d'ambiguïté ciblées
- Pose des questions de clarification précises (5 max)
- Met d'abord à jour `requirements.md` après confirmation utilisateur, puis synchronise `spec.md`
- S'intègre aux constats de review-spec si disponibles

**Catégories d'ambiguïté :**

| Catégorie | Ce qu'elle détecte |
|-----------|--------------------|
| **Lacunes de complétude** | Sections manquantes, contenu vide, critères d'acceptation absents |
| **Problèmes de spécificité** | Termes vagues (« rapide », « scalable »), contraintes non définies |
| **Clarté comportementale** | Lacunes de gestion d'erreur, transitions d'état non définies |
| **Problèmes de mesurabilité** | Exigences non fonctionnelles sans métriques |

**Exemple :**

```text
You: /codexspec:clarify

AI:  Scanning spec.md for ambiguities...

     Found issues in 3 categories.

     ## Question 1/5: Specificity

     **Context**: NFR-001 states "System should respond quickly"

     **Question**: What is the target response time?

     | Option | Description | Impact |
     |--------|-------------|--------|
     | A | < 100ms for all operations | High performance requirement |
     | B | < 500ms for reads, < 1s for writes | Balanced approach |
     | Custom | Provide a different answer | - |

     **Recommendation**: Option B - balanced for typical web app

You: B

AI:  ✓ Updated NFR-001: Response time < 500ms reads, < 1s writes
     Added to Clarifications section in spec.md
```

**Conseils :**

- À utiliser lorsque spec.md existe mais nécessite un affinage
- S'intègre aux constats de `/codexspec:review-spec`
- 5 questions maximum par exécution
- Lancez-la plusieurs fois pour les spécifications complexes

---

### `/codexspec:analyze`

- **specify** lance ou reprend la définition des exigences. Le résumé ne devient contraignant qu'après confirmation explicite.
- **clarify** résout les ambiguïtés des exigences ou de la spécification existantes : jusqu'à cinq questions par exécution, réparties entre quatre catégories. Il met d'abord à jour `requirements.md`, puis synchronise `spec.md`.
- **analyze** vérifie toute la chaîne : exigences → spécification → conception → plan → tâches. Il applique automatiquement des corrections déterministes aux artefacts dérivés lorsque ces corrections découlent des sources qui font autorité ; il ne modifie jamais `requirements.md`. Les constats non résolus sont signalés. Il s'exécute automatiquement après une revue des tâches validée et reste informatif, sans bloquer l'implémentation.

```text
/codexspec:clarify <feature-dir>
/codexspec:analyze <feature-dir>
```

Pour une ancienne fonctionnalité sans `requirements.md`, l’analyse commence à `spec.md`, signale l’absence de preuves de la discussion d’origine et rapporte les constats sans modifier les artefacts. L’absence d’un ancien `design.md` n’empêche pas non plus l’analyse.

---

### `/codexspec:checklist`

Génère des checklists qualité pour valider la complétude, la clarté et la cohérence des exigences. Il s'agit en quelque sorte de « tests unitaires pour la rédaction d'exigences ».

**Syntaxe :**

```
/codexspec:checklist [focus_area]
```

**Arguments :**

| Argument | Requis | Description |
|----------|--------|-------------|
| `focus_area` | Non | Domaine ciblé (par ex. « ux », « api », « security », « performance ») |

**Ce qu'elle fait :**

- Génère des checklists organisées par dimensions de qualité
- Crée les checklists dans le répertoire `FEATURE_DIR/checklists/`
- Les items se concentrent sur la qualité des exigences, pas sur les tests d'implémentation

**Dimensions de qualité :**

- **Complétude des exigences** : toutes les exigences nécessaires sont-elles présentes ?
- **Clarté des exigences** : les exigences sont-elles spécifiques et non ambiguës ?
- **Cohérence des exigences** : les exigences s'alignent-elles sans conflit ?
- **Qualité des critères d'acceptation** : les critères de succès sont-ils mesurables ?
- **Couverture des scénarios** : tous les flux/cas sont-ils traités ?
- **Couverture des cas limites** : les conditions aux bornes sont-elles définies ?
- **Exigences non fonctionnelles** : performance, sécurité, accessibilité sont-elles spécifiées ?
- **Dépendances et hypothèses** : sont-elles documentées ?

**Exemples de types de checklists :**

- `ux.md` - Hiérarchie visuelle, états d'interaction, accessibilité
- `api.md` - Formats d'erreur, rate limiting, authentification
- `security.md` - Protection des données, modèle de menaces, réponse aux fuites
- `performance.md` - Métriques, conditions de charge, dégradation

**Exemple :**

```text
You: /codexspec:checklist security

AI:  Generating security checklist...

     ✓ Created .codexspec/specs/2026-0613-1200ab-task-management/checklists/security.md

     ## Security Requirements Quality Checklist

     ### Authentication Requirements
     - [ ] CHK001 - Are authentication requirements defined for all protected endpoints? [Completeness]
     - [ ] CHK002 - Is password complexity explicitly specified? [Clarity]
     - [ ] CHK003 - Are session timeout requirements quantified? [Measurability]

     ### Data Protection
     - [ ] CHK004 - Are data encryption requirements specified at rest? [Completeness]
     - [ ] CHK005 - Are data encryption requirements specified in transit? [Completeness]
     - [ ] CHK006 - Is PII handling explicitly documented? [Clarity]

     Total: 15 items across 4 categories
```

**Conseils :**

- Les checklists valident la qualité des exigences, pas la correction de l'implémentation
- À utiliser pour la revue et l'amélioration des exigences
- Créez des checklists spécifiques à un domaine pour une validation ciblée
- Lancez-la avant de passer à la planification technique

---

### `/codexspec:tasks-to-issues`

Convertit les tâches de `tasks.md` en issues GitHub pour le suivi et la collaboration sur le projet.

**Syntaxe :**

```
/codexspec:tasks-to-issues
```

**Arguments :**

| Argument | Requis | Description |
|----------|--------|-------------|
| Aucun | - | Convertit toutes les tâches de la fonctionnalité courante |

**Ce qu'elle fait :**

- Analyse les identifiants de tâche, descriptions, dépendances et chemins de fichiers
- Crée des issues GitHub avec un corps structuré
- Ajoute des labels selon le type de tâche (setup, implementation, testing, documentation)
- Relie les dépendances entre issues
- Rapporte les issues créées avec leurs URLs

**Prérequis :**

- Dépôt Git avec remote GitHub
- GitHub CLI (`gh`) installée et authentifiée
- Le fichier `tasks.md` existe

**Exemple :**

```text
You: /codexspec:tasks-to-issues

AI:  Converting tasks to GitHub issues...

     Repository: github.com/example/taskman

     Creating issues:
     ✓ #42: Task 1.1 - Setup Project Structure (setup)
     ✓ #43: Task 2.1 - Write Tests for Task Entity (testing)
     ✓ #44: Task 2.2 - Implement Task Entity (implementation)
     ...

     Summary:
     - Issues created: 24
     - Labels applied: setup(4), implementation(12), testing(5), documentation(3)
     - Dependencies linked: 18

     View issues: https://github.com/example/taskman/issues
```

**Conseils :**

- Requiert l'authentification GitHub CLI (`gh auth login`)
- Ne fonctionne qu'avec les dépôts GitHub
- Crée les issues dans la configuration par défaut du dépôt
- Vérifiez l'absence de doublons avant exécution

Avant de créer des issues, vérifiez le dépôt cible par rapport à son remote et obtenez une autorisation explicite. La génération d’une liste de tâches n’autorise pas, à elle seule, sa publication.

---

### `/codexspec:debug`

Rechercher la cause racine avant d'appliquer une correction.

Voir [Flux de travail](workflow.md#review-and-debugging).

```text
/codexspec:debug Investigate intermittent failures when saving a task
```

---

### `/codexspec:reverse-spec`

Ces deux commandes répondent à des besoins différents :

| Commande | Utilisation | Résultat et limites |
|---------|-----------|-----------------|
| `onboard [path]` | Constituer des connaissances réutilisables sur le projet à partir d'une base de code existante | Conventions candidates et contraintes étayées par des éléments précis dans le profil ; le code reste en lecture seule |
| `reverse-spec [path]` | Comprendre l'architecture existante ou comparer le code à l'intention confirmée | Brouillons d'artefacts ou rapport de dérive ; le code reste en lecture seule |

```text
/codexspec:onboard src/
/codexspec:reverse-spec
/codexspec:reverse-spec src/auth
```

Onboard déduit des conventions du code observable et ne propose des
contraintes qu'en présence d'interdictions explicites. Les conventions candidates
s'appliquent immédiatement dans le projet ; les contraintes candidates exigent
une décision dans la session pour les enregistrer, les modifier ou les
abandonner. Les connaissances existantes sont préservées. Un premier examen
du code ne sert pas à inventer les raisons de décisions passées ou des pièges
supposément rencontrés par expérience.

Reverse-spec propose trois modes :

- **Vue d'ensemble** : sans chemin, ou avec la racine du dépôt, la commande produit un `design.md` décrivant brièvement l'architecture et un `slices.md` pour choisir les modules à examiner.
- **Génération** : avec le chemin d'un module sans base confirmée, elle produit des brouillons de `spec.md` et de `design.md`, ainsi que des exigences en suspens ou inférées.
- **Réconciliation** : si le module dispose d'une base confirmée, elle produit `reconcile.md`. Ce rapport relève les comportements non documentés, les spécifications non implémentées et les divergences sémantiques par rapport aux spécifications et aux documents de conception confirmés ; les exigences font autorité sur l'intention du produit.

Les brouillons inférés doivent être confirmés par une personne avant de devenir
une base de référence. La réconciliation propose une marche à suivre — corriger
le code, mettre à jour les documents ou décider de l'intention — sans l'appliquer
automatiquement.

---

### `/codexspec:distill`

Capture les connaissances réutilisables transverses dans `.codexspec/profile/` et passe en revue les candidats en attente sans modifier leurs fichiers Markdown à la main.

**Syntaxe :**

```text
/codexspec:distill [interaction segment]
/codexspec:distill review
```

**Revue manuelle :**

- `/codexspec:distill review`, ou un appel direct sans nouveau segment à extraire, ouvre une page HTML hors ligne servie uniquement depuis `127.0.0.1`. Son en-tête nomme le répertoire de projet dans lequel la session écrira, afin que deux revues ouvertes côte à côte ne puissent pas être confondues.
- La page prend en charge la révision structurée, la validation, le rejet, le report, la consolidation, un récapitulatif complet de ce qui est préparé et un **Tout appliquer** explicite. Une révision ou une fusion doit afficher sa prévisualisation Markdown finale exacte avant que la même action puisse être préparée ; la page indique dans lequel des trois états de prévisualisation se trouve chaque enregistrement — pas de prévisualisation, conforme aux modifications actuelles, ou modifié depuis la prévisualisation — avant que vous n'utilisiez une commande de décision.
- Toute action qui supprime des fichiers d'enregistrement demande une seconde confirmation énonçant sa conséquence : le rejet nomme le fichier que l'application supprimera, une fusion nomme le nombre d'enregistrements membres qu'elle supprimera, et l'abandon du brouillon nomme le nombre de décisions préparées qui seront perdues.
- Un enregistrement ne devient `vetted` qu'avec une approbation humaine **et** une preuve de vérification fondée sur un résultat. La page indique, avant que vous ne choisissiez la validation, si les preuves enregistrées satisfont déjà cette exigence.
- La file regroupe les enregistrements selon ce qui est décidé et indique combien des enregistrements en attente sont déjà réglés. Préparer une décision fait passer à l'enregistrement suivant non décidé ; un interrupteur dans l'en-tête le désactive.
- La page s'utilise au clavier : appuyez sur `?` pour voir les touches. Aucune touche seule n'applique le lot, n'annule la session ni n'abandonne le brouillon.
- Les décisions préparées utilisent un brouillon de projet récupérable et exclu de Git. Une seule revue en écriture est active par projet.
- Un brouillon structurellement endommagé est conservé avec un diagnostic exploitable et n'est supprimé que par une action d'abandon explicite.
- L'application revérifie les empreintes source et rejette la totalité du lot si un enregistrement a changé ; elle n'écrase jamais une modification concurrente et ne signale jamais un succès partiel.
- Toutes les ressources de la page sont livrées avec CodexSpec. La page n'utilise ni CDN, ni appel de modèle distant, ni télémétrie.
- Si aucun navigateur ne peut être ouvert, la commande affiche l'URL locale protégée par jeton. Demandez le mode texte explicite lorsqu'un navigateur ne convient pas ; il utilise la même validation et le même chemin d'écriture.

La distillation automatique reste non interactive et non bloquante : elle n'ouvre jamais la page, ne démarre jamais la revue en mode texte et n'attend jamais un brouillon enregistré.

---

### `/codexspec:evolve`

`evolve` ne sélectionne que des connaissances validées utiles au-delà du projet,
élabore un brouillon de commande ou de compétence et obtient une approbation
explicite avant d’effectuer un push ou d'ouvrir une PR de contribution
pour revue humaine.

```text
/codexspec:evolve
```

---

### `/codexspec:onboard`

Déduire des conventions candidates et des contraintes étayées du code existant.

Voir [`reverse-spec`](#codexspecreverse-spec).

```text
/codexspec:onboard src/
```

---

### `/codexspec:commit-staged`

```text
/codexspec:commit-staged -p
/codexspec:pr --spec <feature-dir>/spec.md
/codexspec:release-notes --from <ref> --to HEAD
/codexspec:tasks-to-issues <feature-dir>
```

- **commit-staged** analyse exactement l'index et génère un message Conventional Commits ; `-p` affiche un aperçu sans créer de commit. Le flux qui l'appelle choisit et indexe les fichiers. L'exécution autorisée utilise un environnement protégé qui vérifie à nouveau que le contenu committé correspond à l'analyse. Les consignes de commit destinées à l'agent s'appliquent dans les conversations courantes et les flux SDD, blueprint et auto-dev ; la disponibilité de la commande ne vaut ni invocation ni autorisation de commit.
- **pr** génère une description structurée de PR GitHub ou de MR GitLab à partir du diff. `--spec` peut ajouter le contexte de la fonctionnalité depuis le chemin d'un fichier `spec.md`, ou depuis un nom ou préfixe de dossier de fonctionnalité résolu vers ce fichier. La sortie par défaut est du texte à utiliser sur la plateforme d'hébergement.
- **release-notes** produit à partir de l'historique Git une entrée Keep a Changelog et le texte d'une publication. La section par défaut est `[Unreleased]` ; `--version` utilise le libellé fourni. La commande n'indexe rien, ne crée pas de commit, n'incrémente pas les versions, ne crée pas de tag, ne publie rien et ne crée pas de release.
- **tasks-to-issues** crée des issues GitHub à partir des tâches existantes, avec leurs dépendances et leurs critères d'acceptation. Elle nécessite une CLI GitHub authentifiée et vérifie que le dépôt des issues correspond au dépôt distant configuré.

La prévisualisation directe des commits et les commits autorisés dans le dossier
courant nécessitent Python 3.11+ et Git. L'environnement d'exécution est installé
dans les projets initialisés par CLI et fourni avec le plugin Claude. Les
fusions créées par l'agent qui modifient le contenu passent également par
l'analyse des changements indexés. Les fusions qui relient seulement les
historiques conservent le message par défaut de Git tout en validant l'arbre
et les parents ; les avances rapides ne créent aucun commit.

Le helper partagé `.codexspec/scripts/commit-staged-helper.py` (ou sa copie incluse dans le plugin) nécessite Python 3.11+ et Git. Il n’appelle aucun LLM, conserve les Git hooks et refuse un contenu indexé qui a changé après l’analyse. L’initialisation ponctuelle fournit ce runtime ; le routage des espaces de travail, blueprint et auto-dev nécessitent toujours la CLI.

---

### `/codexspec:pr`

Génère une description structurée de Pull Request GitHub / Merge Request GitLab à partir du diff git. S'intègre facultativement à `spec.md` pour un contexte tracé par SDD.

**Syntaxe :**

```
/codexspec:pr [--target-branch <branch>] [--sections <list>] [--spec <id-or-path>] [--output <file>]
```

**Arguments :**

| Argument | Requis | Description |
|----------|--------|-------------|
| `--target-branch <branch>` | Non | Branche de comparaison (par défaut : `origin/main`) |
| `--sections <list>` | Non | Sous-ensemble séparé par des virgules parmi `summary, changes, testing, verify, checklist, notes` (par défaut : `all`) |
| `--spec <id-or-path>` | Non | Intégration opt-in de spec : un identifiant de fonctionnalité (par ex. `2025-0321-1430k7-auth`) résolu sous `.codexspec/specs/`, ou un chemin explicite `path/to/spec.md`. Omettre pour générer uniquement depuis git |
| `--output <file>` | Non | Enregistrer la description dans un fichier plutôt que dans le terminal |

**Ce qu'elle fait :**

- Collecte le contexte git (branche courante, URL distante, commits en avance, changements de fichiers, diff complet, messages de commit) par rapport à la branche cible
- Détecte automatiquement la plateforme depuis l'URL distante : GitHub → « Pull Request », GitLab → « Merge Request », autre/aucune → terminologie GitHub par défaut avec avertissement
- Charge `.codexspec/memory/constitution.md` lorsqu'il est présent et aligne la description sur les standards de documentation/revue de code
- Respecte `language.commit` (puis `language.output`, puis l'anglais) pour la langue de la description ; les termes techniques (API, JWT, PR, MR) restent en anglais lorsque c'est approprié
- Lorsque `--spec` est fourni, ajoute une section Contexte avec les user stories et exigences tirées de spec.md ; sinon génère uniquement à partir du diff
- Émet les sections selon `--sections` (Summary, Changes, Testing, Verification Steps, Pre-merge Checklist, Notes / Breaking Changes)

**Exemple :**

```text
You: /codexspec:pr --spec 2026-0613-1200ab-task-management

AI:  Generating Pull Request description...

     Platform: GitHub (github.com/example/taskman)
     Branch:   feature/task-management  →  origin/main
     Commits:  8 ahead

     ## Pull Request: Task management for small dev teams

     ### Context
     - User stories and REQ-* pulled from spec.md

     ### Summary
     - Adds task CRUD, sub-tasks, and real-time updates

     ### Changes
     - src/taskman/models/task.py (new)
     - src/taskman/api/tasks.py (new)
     - ...

     ### Verification Steps
     1. `uv run pytest`
     2. `uv run codexspec check`
```

**Conseils :**

- Omettez `--spec` pour les petits correctifs ou les changements sans spécification formelle
- Combinez avec `/codexspec:commit-staged` pour produire à la fois un message de commit et une description de PR depuis le même travail
- Consultez l'[étude de cas du générateur de descriptions de PR](../case-studies/case-study-pr-description-generator.md) pour un exemple complet et bout-en-bout de cette commande (notamment la façon dont le contexte spec.md est intégré)

---

### `/codexspec:release-notes`

```text
/codexspec:commit-staged -p
/codexspec:pr --spec <feature-dir>/spec.md
/codexspec:release-notes --from <ref> --to HEAD
/codexspec:tasks-to-issues <feature-dir>
```

- **commit-staged** analyse exactement l'index et génère un message Conventional Commits ; `-p` affiche un aperçu sans créer de commit. Le flux qui l'appelle choisit et indexe les fichiers. L'exécution autorisée utilise un environnement protégé qui vérifie à nouveau que le contenu committé correspond à l'analyse. Les consignes de commit destinées à l'agent s'appliquent dans les conversations courantes et les flux SDD, blueprint et auto-dev ; la disponibilité de la commande ne vaut ni invocation ni autorisation de commit.
- **pr** génère une description structurée de PR GitHub ou de MR GitLab à partir du diff. `--spec` peut ajouter le contexte de la fonctionnalité depuis le chemin d'un fichier `spec.md`, ou depuis un nom ou préfixe de dossier de fonctionnalité résolu vers ce fichier. La sortie par défaut est du texte à utiliser sur la plateforme d'hébergement.
- **release-notes** produit à partir de l'historique Git une entrée Keep a Changelog et le texte d'une publication. La section par défaut est `[Unreleased]` ; `--version` utilise le libellé fourni. La commande n'indexe rien, ne crée pas de commit, n'incrémente pas les versions, ne crée pas de tag, ne publie rien et ne crée pas de release.
- **tasks-to-issues** crée des issues GitHub à partir des tâches existantes, avec leurs dépendances et leurs critères d'acceptation. Elle nécessite une CLI GitHub authentifiée et vérifie que le dépôt des issues correspond au dépôt distant configuré.

La prévisualisation directe des commits et les commits autorisés dans le dossier
courant nécessitent Python 3.11+ et Git. L'environnement d'exécution est installé
dans les projets initialisés par CLI et fourni avec le plugin Claude. Les
fusions créées par l'agent qui modifient le contenu passent également par
l'analyse des changements indexés. Les fusions qui relient seulement les
historiques conservent le message par défaut de Git tout en validant l'arbre
et les parents ; les avances rapides ne créent aucun commit.

#### Options des notes de version

| Commandes | Référence |
|---|---|
| `--version <X.Y.Z>` | Libellé de version fourni ; sinon `[Unreleased]` |
| `--from <ref>` | Référence de départ ; sinon dernier tag accessible, puis version du changelog pouvant être rattachée à un commit, puis historique complet |
| `--to <ref>` | Référence de fin ; par défaut `HEAD` |
| `--output <file>` | Fichier de sortie du texte de publication ; sinon sortie dans le terminal |
| `--spec <feature>` | Contexte facultatif de la fonctionnalité ; si elle est introuvable, le problème est signalé et la génération continue avec Git |

---

### `/codexspec:review-code`

Examine la modification Git sélectionnée comme un contrôle de défauts strict avant fusion. La cible par défaut comprend l'écart complet de la fonctionnalité ; les sélecteurs explicites choisissent les changements enregistrés dans des commits, changements sans commit ou un commit unique, sans accepter de filtre de chemin.

<!-- REVIEW-CODE-BREAKING: DEFAULT-GATE -->
<!-- REVIEW-CODE-BREAKING: PATH-AUDIT -->

**Mode de revue par défaut :**

- La commande par défaut est un contrôle de défauts limité au changement, et non un score général de qualité.
- Les chemins positionnels ne sont plus valides. Utilisez explicitement `--audit` pour le score consultatif de qualité par chemin.

**Syntaxe du contrôle de défauts :**

```text
/codexspec:review-code
/codexspec:review-code --committed [--base <branch>] [--feature <feature-dir>] [--focus <instructions>]
/codexspec:review-code --uncommitted [--feature <feature-dir>] [--focus <instructions>]
/codexspec:review-code --commit <sha> [--parent <n>] [--feature <feature-dir>] [--focus <instructions>]
/codexspec:review-code [--committed] --incremental-from <fingerprint> [--feature <feature-dir>]
```

Chaque forme du contrôle de défauts accepte aussi `--decided-by reviewer|ask`, qui remplace `review.decided_by` pour cette exécution.

<!-- REVIEW-CODE-SYSTEM-CONTRACT -->
<!-- REVIEW-CODE-VARIANT-SEARCH -->
<!-- REVIEW-CODE-NEUTRAL-HANDOFF -->

Le contrôle inventorie tous les artefacts sélectionnés, évalue les exigences applicables et exécute cinq phases dans cet ordre : Scope, System Contract, Behavior, Risk et Verification. Il consigne les contrats intermodules étayés par des preuves et les partitions de revue sémantiques ; chaque cause racine répétable et validée déclenche, avant la fin du passage, une recherche bornée des occurrences apparentées. Les six sections du rapport sont suivies d'un bloc de résultat unique `<review-code-result>` lisible par machine avec `schema_version: "3"`. Le bloc de résultat transmet l'identité de la cible, la couverture et les obligations objectives à revérifier après réparation. L'appelant conserve ces obligations neutres pour une nouvelle revue complète, sans transmettre le raisonnement de réparation ni les conclusions précédentes sur la correction. Le verdict est `PASS`, `FAIL` ou `INCONCLUSIVE` : tout défaut P0-P3 produit `FAIL` ; l'absence de preuve obligatoire ou une couverture incomplète produit `INCONCLUSIVE`.

**Tours incrémentaux.** Après une correction, `--incremental-from <fingerprint>` ne réexamine que ce qui a changé depuis ce résultat antérieur : les fichiers modifiés, les partitions de revue et les contrats qu'ils touchent, ainsi que les obligations reportées. La couverture des fichiers inchangés et non affectés est réutilisée, et le relecteur signale tout de même chaque défaut qu'il trouve ailleurs. Un `PASS` incrémental ne termine jamais une fonctionnalité : `implement-tasks` lance d'abord une revue complète, puis des revues incrémentales après chaque correction, et enfin une nouvelle revue complète comme acceptation finale. Les enregistrements de revue sont écrits hors du dépôt, dans votre répertoire de cache utilisateur (`~/.cache/codexspec/review/` ou `%LOCALAPPDATA%\codexspec\review\`) ; seuls le rapport et le bloc de résultat apparaissent dans la conversation.

**Mode de décision.** `review.decided_by` dans `.codexspec/config.yml` détermine qui tranche sur un constat dont le déclencheur sort du contexte d'utilisation réel du projet, par exemple une entrée que le projet ne reçoit jamais. Avec la valeur par défaut `reviewer`, la revue se comporte exactement comme avant. Avec `ask`, la revue signale ce point comme une décision de scénario en attente au lieu d'échouer, et `implement-tasks` vous demande une seule fois : le corriger, ou accepter que le scénario est hors périmètre. Votre réponse est consignée dans `requirements.md` comme une entrée `CON` ou `OUT` confirmée, afin que les tours suivants ne la soulèvent plus.

```text
You: /codexspec:review-code --feature .codexspec/specs/2026-0714-example

AI:  ## Verdict
     **PASS** — all required review and verification completed with no findings.
```

**Critères applicables et maintenance.** Chaque revue lit les règles communes et le mode choisi, évalue les sept dimensions, puis charge les détails pertinents pour le comportement, le contrat ou les dépendances. Les dépendances inchangées découvertes pendant le suivi peuvent aussi activer les listes propres aux langages ou frameworks. Une proposition de maintenance exige des preuves d’un problème actuel et une amélioration locale compatible avec le comportement existant. Une complexité future hypothétique ou un seuil de style seul ne justifie pas de correction. Le résultat des défauts conserve la version 3 ; un `<review-code-maintenance>` distinct de version 1 rapporte les propositions liées à la même empreinte cible. La revue autonome ne fait que les signaler. `implement-tasks` les vérifie et les applique selon `workflow.auto_maintenance` (par défaut `true`). Les corrections se poursuivent tant qu’elles produisent des progrès substantiels et respectent les conditions d’arrêt existantes. Il n’y a pas de limite fixe de cycles ; la validation finale exige une nouvelle revue complète.

Les options booléennes de la CLI acceptent `on/true/1/yes` et `off/false/0/no`,
sans distinction de casse et avec d'éventuels espaces autour de la valeur.
Une option booléenne sans valeur inverse la valeur actuelle du checkout de
destination ; les valeurs sont enregistrées sous forme de booléens dans YAML.

`codexspec init` installe les ressources de revue communes à Claude Code et Codex dans `.codexspec/review-code/`. `--force` actualise les ressources distribuées et préserve les extensions ayant d’autres chemins. L’installation de la CLI seule ne crée aucun fichier de projet. Avec le plugin seul, sans arborescence installée dans le projet, la revue utilise les mêmes ressources depuis la racine résolue par l’hôte.

<!-- REVIEW-CODE-AUDIT -->

#### Audit de qualité par chemin

La branche audit explicite examine le contenu actuel complet des fichiers pour la clarté idiomatique, la correction, la robustesse, l'architecture et l'alignement constitutionnel. Ce score est consultatif et ne peut pas terminer `implement-tasks`.

**Syntaxe :**

```
/codexspec:review-code --audit [paths...]
```

**Arguments :**

| Argument | Requis | Description |
|----------|--------|-------------|
| `path...` | Non | Un ou plusieurs fichiers ou répertoires sources à examiner (séparés par des espaces). Par défaut `src/` si omis |

**Ce qu'elle fait :**

- Détecte le ou les langages principaux à partir des extensions de fichiers et exécute un passage par langage pour les cibles multi-langages
- Lance les outils d'analyse statique lorsque leur config est présente (`ruff`/`mypy`, `eslint`/`tsc`, `go vet`/`gofmt`, `cargo check`/`cargo clippy`, `shellcheck`) ; omet ces contrôles et signale une couverture dégradée sinon
- Note quatre dimensions : Clarté et simplicité idiomatiques, Correction et contrats explicites, Robustesse d'exécution et discipline des ressources, Intégrité architecturale et de conception
- Injecte des sous-sections obligatoires pour les frameworks détectés (par ex. Hooks Compliance pour React, Ownership & Borrowing pour Rust, Goroutine & Context Discipline pour Go, Memory & Lifetime Safety pour C/C++, Execution Safety pour Shell)
- Recoupe les constats avec `.codexspec/memory/constitution.md` lorsqu'il est présent ; en son absence, l'axe constitution est abandonné et son poids redistribué
- Classe les constats par sévérité : CRITICAL, HIGH, MEDIUM, LOW (les suggestions LOW sont plafonnées à une déduction totale de 5 points)

**Exemple :**

```text
You: /codexspec:review-code --audit src/

AI:  # Code Review Report

     ## Summary
     - Overall Status: Needs Work
     - Quality Score: 78/100
     - Detected Language: Python

     ## Static Analysis Results
     | Tool   | Status | Issues | Details                |
     |--------|--------|--------|------------------------|
     | ruff   | Warn   | 3      | Unused imports, line length |
     | mypy   | Pass   | 0      | No type errors         |

     ## Detailed Findings
     ### Critical Issues (CRITICAL)
     - [ ] [CODE-001] src/auth/service.py:42 - bare `except Exception:` swallows the original cause
       Impact: Original error context is lost during debugging.
       Suggestion: narrow the exception and re-raise with `raise ... from err`.

     ### Suggestions (LOW)
     - [ ] [CODE-004] src/auth/service.py:120 - manual loop where a comprehension suffices

     ## Recommendations
     1. Priority 1: Fix CODE-001 before merge.
     2. Priority 2: Apply LOW suggestions opportunistically.
```

**Conseils :**

- Passez plusieurs chemins pour examiner une partie ciblée, par ex. `src/ tests/`
- Le score est consultatif ; les constats CRITICAL/HIGH constituent le base pour décider des corrections à apporter

---

### `/codexspec:config`

Gère la configuration du projet de façon interactive (créer/consulter/modifier/réinitialiser). Il s'agit de l'équivalent en slash command du CLI `codexspec config`, idéal pour les installations via Plugin Marketplace.

**Syntaxe :**

```
/codexspec:config [--view]
```

**Arguments :**

| Argument | Requis | Description |
|----------|--------|-------------|
| `--view` | Non | Affiche la configuration courante sans la modifier. Sans argument, ouvre le menu de gestion interactif |

**Ce qu'elle fait :**

- Cible exclusivement `.codexspec/config.yml`
- `--view` (ou l'option de menu « View current config ») affiche le fichier dans un format lisible ; signale « Configuration Not Found » en son absence
- En mode interactif, lorsqu'une config existe, propose : Consulter, Modifier, Réinitialiser aux valeurs par défaut, Annuler
- En l'absence de config, lance le flux de création qui écrit une config minimale ne contenant que `output` (interaction/document/commit retombent sur `output`, puis `en`, si bien qu'un fichier limité à `output` est pleinement fonctionnel)
- Permet de régler chaque dimension de langue indépendamment (output, interaction, document, commit) et de basculer des options de flux telles que `auto_next`

**Ce qu'elle crée/modifie :**

```
.codexspec/config.yml
```

**Exemple :**

```text
You: /codexspec:config

AI:  ## Configuration Manager

     Configuration file found at .codexspec/config.yml.
     What would you like to do?
     - View current config
     - Modify config
     - Reset to defaults
     - Cancel

You: Modify config

AI:  Select a dimension to change:
     - Output language (base)
     - Interaction language
     - Document language
     - Commit-message language
     - workflow.auto_next
     - workflow.auto_distill
     - workflow.auto_maintenance
     - workflow.worktrees (default on; checkout-local)
     - review.decided_by

You: Output language (base) → zh-CN

AI:  ✓ Updated language.output: "zh-CN"
     (interaction and document fall back to output, then en.)
```

**Conseils :**

- Utilisez `/codexspec:config --view` pour inspecter l'état courant avant toute modification
- Une config neuve ou réinitialisée n'écrit que `output` ; ne réglez `interaction`/`document` que lorsqu'ils doivent différer de `output`
- Pour des changements scriptés dans un terminal, préférez le CLI `codexspec config` (`--set-lang`, `--set-interaction-lang`, `--set-document-lang`, `--set-commit-lang`, `--auto-next`)

Le menu interactif gère aussi `workflow.auto_distill`, `workflow.auto_maintenance`, `workflow.worktrees` et `review.decided_by`. Les modifications de configuration suivent le routage des worktrees et prennent effet dans chaque checkout séparément.

---

### `/codexspec:quick`

Exécute un flux Requirements-First SDD allégé pour les petits changements.

**Syntaxe :**

```
/codexspec:quick [describe a small requirement]
```

**Arguments :**

| Argument | Requis | Description |
|----------|--------|-------------|
| `describe a small requirement` | Non | Brève description du petit changement bien délimité (vous serez sollicité si non fournie) |

**Ce qu'elle fait :**

- Évalue le périmètre (fichiers touchés, étendue des modules, nouvelles dépendances, décisions produit non tranchées) et, si le changement est large ou a plusieurs résultats indépendants, recommande le flux standard
- Crée un espace de travail de fonctionnalité et `requirements.md` en utilisant la même convention d'horodatage que `/codexspec:specify`
- Résout uniquement les ambiguïtés qui ont un effet concret sur l’implémentation ; présente un résumé concis des éléments confirmés (`NEED-*`, `CON-*`/`DEC-*` pertinents, `OUT-*`, `OPEN-*` non résolus)
- S'arrête à la Confirmation Gate : rien n'est généré tant que vous n'avez pas confirmé le résumé
- Enchaîne les commandes de génération sur le nouveau répertoire de fonctionnalité : `/codexspec:generate-spec`, `/codexspec:design-to-plan`, `/codexspec:plan-to-tasks`, `/codexspec:implement-tasks`
- S'en remet à la propre boucle d'auto-review de chaque commande de génération ; s'interrompt et demande à l'utilisateur si une revue requiert une nouvelle décision produit ou architecture
- Rapporte séparément le répertoire de la fonctionnalité, les chemins des artefacts, les résultats des revues, la vérification de l'implémentation et les avis non résolus

**Ce qu'elle crée :**

```text
.codexspec/specs/{timestamp}-{feature-name}/
├── requirements.md
├── spec.md
├── plan.md
└── tasks.md
```

**Exemple :**

```text
You: /codexspec:quick Add a "remember me" checkbox to the login form

AI:  Scope check: 1 component, 1 form field, no new dependencies. Quick is appropriate.

     Confirmed requirements:
     - NEED-1: "Remember me" checkbox on the login form (default unchecked)
     - DEC-1: Persist a long-lived refresh token only when checked
     OUT-1: SSO / social login (unchanged)

     Confirm this summary to start the automated flow. [y/N]

You: y

AI:  Running generate-spec → design-to-plan → plan-to-tasks → implement-tasks ...

     ✓ Feature dir: .codexspec/specs/2026-0713-0915ab-remember-me/
     ✓ All reviews PASS_WITH_WARNINGS or higher
     ✓ Implementation verified
     Open advisories: none
```

**Conseils :**

- Réservez Quick à des changements réellement petits et à résultat unique ; sinon lancez `/codexspec:specify` et le flux standard
- La confirmation reste obligatoire — Quick ne déduit jamais une décision produit pour faire avancer l'automatisation
- Si une revue de génération renvoie `NEEDS_REVISION`/`BLOCKED`, Quick s'arrête et vous rend la main

---

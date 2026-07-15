# Commandes

Il s'agit de la référence des slash commands de CodexSpec. Ces commandes sont invoquées dans l'interface de chat de Claude Code.

Pour les motifs de flux de travail et savoir quand utiliser chaque commande, consultez [Flux de travail](workflow.md). Pour les commandes CLI, voir [CLI](../reference/cli.md).

## Référence rapide

Regroupées par catégorie, en miroir du catalogue du README. Au sein de chaque groupe, les commandes apparaissent dans l'ordre du flux de travail.

### Commandes du flux de travail principal

| Commande | Objectif |
|----------|----------|
| `/codexspec:constitution` | Créer ou mettre à jour la constitution du projet avec validation inter-artifacts |
| `/codexspec:specify` | Clarifier, confirmer et persister les exigences dans `requirements.md` |
| `/codexspec:generate-spec` | Générer le document `spec.md` à partir des exigences clarifiées (★ Auto-review) |
| `/codexspec:spec-to-plan` | Convertir la spécification en plan technique d'implémentation (★ Auto-review) |
| `/codexspec:plan-to-tasks` | Découper le plan en tâches traçables et vérifiables (★ Auto-review) |
| `/codexspec:implement-tasks` | Exécuter les tâches avec un flux de travail TDD conditionnel |

### Commandes de revue (portes qualité)

| Commande | Objectif |
|----------|----------|
| `/codexspec:review-spec` | Valider la spécification en termes de complétude et de qualité |
| `/codexspec:review-plan` | Examiner le plan technique sous l'angle de la faisabilité et de l'alignement |
| `/codexspec:review-tasks` | Valider la couverture, l'ordonnancement et la faisabilité des tâches |

### Commandes d'enrichissement

| Commande | Objectif |
|----------|----------|
| `/codexspec:config` | Gérer la configuration du projet de façon interactive (créer/consulter/modifier/réinitialiser) |
| `/codexspec:clarify` | Scanner une spec existante pour détecter les ambiguïtés (4 catégories, 5 questions max) |
| `/codexspec:analyze` | Analyse de cohérence inter-artifacts (en lecture seule, fondée sur la sévérité) |
| `/codexspec:checklist` | Générer des checklists de qualité des exigences |
| `/codexspec:tasks-to-issues` | Convertir les tâches en issues GitHub |

### Commandes de flux Git

| Commande | Objectif |
|----------|----------|
| `/codexspec:commit-staged` | Générer un message de commit à partir des changements stagés (sensible au contexte de session) |
| `/codexspec:pr` | Générer une description de PR/MR à partir du diff git (détection auto de la plateforme) |

### Commandes de revue de code

| Commande | Objectif |
|----------|----------|
| `/codexspec:review-code` | Contrôle de défauts limité au changement ; score par chemin avec `--audit` |
| `/codexspec:review-python-code` | Examiner du code Python (PEP 8, sécurité des types, robustesse, cohérence avec la constitution) |
| `/codexspec:review-react-code` | Examiner du code React/TypeScript (architecture des composants, règles des Hooks, état, performance) |

### Voie rapide

| Commande | Objectif |
|----------|----------|
| `/codexspec:quick` | Exécuter un flux Requirements-First SDD allégé pour les petits changements |

---

## Catégories de commandes

### Commandes du flux de travail principal

Les commandes du flux Requirements-First SDD principal : Constitution → Exigences confirmées → Spécification → Plan → Tâches → Implémentation. Les exigences confirmées constituent ici l'autorité de plus haute priorité — rien dans la chaîne n'engage tant que vous ne le confirmez pas explicitement à la Confirmation Gate.

### Commandes de revue (portes qualité)

Des commandes qui valident les artifacts à chaque étape du flux selon un contrat de **revue fondée sur les preuves** : chaque défaut doit contenir un `Evidence`, une `Location`, un `Mismatch`, un `Impact` et une `Remediation` concrets. Les suggestions de conception consultatives sont rapportées séparément et ne modifient jamais le statut ni ne déclenchent de changement automatique. Les défauts vérifiés peuvent être corrigés puis ré-examinés pendant deux tours au maximum ; les avis restent facultatifs tout au long du processus.

### Commandes d'enrichissement

Des commandes pour l'affinage itératif, la validation inter-artifacts, la configuration et l'intégration avec la gestion de projet.

### Commandes de flux Git

Des commandes qui transforment le travail achevé en artifacts partageables : des messages de commit tirés du diff stagé et des descriptions structurées de PR/MR tirées du diff de branche.

### Commandes de revue de code

Des commandes qui examinent le code source (tout langage, spécifique à Python, spécifique à React/TypeScript) sous l'angle de la clarté idiomatique, de la correction, de la robustesse, de l'architecture et de l'alignement avec la constitution. Les constats appliquent la même discipline de sévérité que les revues d'artifacts : les problèmes CRITICAL/HIGH doivent citer des preuves concrètes ; les suggestions LOW restent purement consultatives.

### Voie rapide

Une commande allégée qui exécute le flux Requirements-First SDD de bout en bout pour des changements petits et bien délimités.

---

## Référence des commandes

### `/codexspec:constitution`

Crée ou met à jour la constitution du projet. La constitution définit les principes architecturaux, la pile technologique, les standards de code et les règles de gouvernance qui guident toutes les décisions de développement ultérieures.

**Syntaxe :**

```
/codexspec:constitution [description des principes]
```

**Arguments :**

| Argument | Requis | Description |
|----------|--------|-------------|
| `description des principes` | Non | Description des principes à inclure (vous serez sollicité si non fournie) |

**Ce qu'elle fait :**

- Crée `.codexspec/memory/constitution.md` s'il n'existe pas
- Met à jour la constitution existante avec les nouveaux principes
- Valide la cohérence inter-artifacts avec les templates
- Génère un rapport d'impact de synchronisation montrant les changements et les fichiers affectés
- Inclut une revue de constitutionnalité pour les templates dépendants

**Ce qu'elle crée :**

```
.codexspec/
└── memory/
    └── constitution.md    # Document de gouvernance du projet
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
- Les changements de constitution déclenchent une validation inter-artifacts

---

### `/codexspec:specify`

Clarifie les exigences via un échange interactif de questions/réponses, confirme le résumé qui en résulte et le persiste pour les sessions ultérieures.

**Syntaxe :**

```
/codexspec:specify [votre idée ou exigence]
```

**Arguments :**

| Argument | Requis | Description |
|----------|--------|-------------|
| `votre idée ou exigence` | Non | Description initiale de ce que vous souhaitez construire (vous serez sollicité si non fournie) |

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

Seuls les éléments confirmés deviennent des exigences authentiques. Les questions ouvertes restent explicitement ouvertes. Il s'agit de la Confirmation Gate pour les exigences : rien n'engage tant que vous n'avez pas explicitement confirmé le résumé final.

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

### `/codexspec:generate-spec`

Génère le document `spec.md` à partir des exigences clarifiées. Cette commande agit comme un « compilateur d'exigences » qui transforme vos exigences clarifiées en une spécification structurée.

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
     - Or proceed to /codexspec:spec-to-plan
```

**Conseils :**

- Lancez-la après que `/codexspec:specify` a clarifié les exigences
- Revoyez la spec générée avant de continuer
- Utilisez `/codexspec:review-spec` pour une validation qualité
- Éditez spec.md directement si de petits ajustements sont nécessaires

---

### `/codexspec:clarify`

Scanne une spécification existante pour détecter les ambiguïtés et les lacunes. À utiliser pour l'affinage itératif après la création initiale de la spec.

**Syntaxe :**

```
/codexspec:clarify [chemin_vers_spec.md]
```

**Arguments :**

| Argument | Requis | Description |
|----------|--------|-------------|
| `chemin_vers_spec.md` | Non | Chemin vers le fichier spec (détecté automatiquement si non fourni) |

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
- 5 questions maximum par session
- Lancez-la plusieurs fois pour les spécifications complexes

---

### `/codexspec:spec-to-plan`

Convertit la spécification de la fonctionnalité en un plan technique d'implémentation. C'est ici que vous définissez **comment** la fonctionnalité sera construite.

**Syntaxe :**

```
/codexspec:spec-to-plan [chemin_vers_spec.md]
```

**Arguments :**

| Argument | Requis | Description |
|----------|--------|-------------|
| `chemin_vers_spec.md` | Non | Chemin vers le fichier spec (détecté automatiquement depuis `.codexspec/specs/` si non fourni) |

**Ce qu'elle fait :**

- Lit la spécification et la constitution
- N'inclut que les détails techniques réellement requis par les exigences confirmées et les contraintes du dépôt
- Vérifie les règles de constitution applicables sans traiter les conventions facultatives comme des exigences fonctionnelles
- Ajoute des liens `Covers` vers les exigences de la spécification
- Documente les décisions techniques avec leur justification
- S'arrête lorsqu'une décision modifierait une intention confirmée

**Ce qu'elle crée :**

```
.codexspec/
└── specs/
    └── 2026-0613-1200ab-task-management/
        └── plan.md    # Plan technique d'implémentation
```

**Exemple :**

```text
You: /codexspec:spec-to-plan Use Python FastAPI for backend, React for frontend, PostgreSQL for database

AI:  Generating technical plan...

     Constitutionality Review:
     ✓ Clean Architecture: Modular design with clear boundaries
     ✓ TDD: Test-first approach enforced in phases
     ✓ Code Quality: Linting and type hints required

     Architecture:
     - Backend: FastAPI with layered architecture
     - Frontend: React with component structure
     - Database: PostgreSQL with migration strategy

     Module Dependency Graph:
     ┌─────────────┐
     │    API      │
     └──────┬──────┘
            │
     ┌──────▼──────┐
     │  Services   │
     └──────┬──────┘
            │
     ┌──────▼──────┐
     │    Data     │
     └─────────────┘

     ✓ Created plan.md
     5 Implementation Phases defined
```

**Conseils :**

- Lancez-la après que la spec a été revue et stabilisée
- Les règles de constitution applicables sont obligatoires ; les conventions de template non pertinentes ne le sont pas
- Incluez les sections pertinentes selon le type de projet
- Revoyez le plan avant de passer aux tâches

---

### `/codexspec:plan-to-tasks`

Découpe le plan technique en tâches actionnables avec une couverture explicite et des résultats vérifiables.

**Syntaxe :**

```
/codexspec:plan-to-tasks [chemin_vers_spec.md chemin_vers_plan.md]
```

**Arguments :**

| Argument | Requis | Description |
|----------|--------|-------------|
| `chemins` | Non | Chemins vers spec et plan (détectés automatiquement si non fournis) |

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
        └── tasks.md    # Découpage en tâches
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

---

### `/codexspec:implement-tasks`

Exécute les tâches d'implémentation avec un flux de travail TDD conditionnel. Parcourt la liste des tâches de façon systématique.

**Syntaxe :**

```
/codexspec:implement-tasks [chemin_tasks]
/codexspec:implement-tasks [chemin_spec chemin_plan chemin_tasks]
```

**Arguments :**

| Argument | Requis | Description |
|----------|--------|-------------|
| `chemin_tasks` | Non | Chemin vers tasks.md (détecté automatiquement si non fourni) |
| `chemin_spec chemin_plan chemin_tasks` | Non | Chemins explicites vers les trois documents |

**Résolution des fichiers :**

- **Aucun argument** : détection auto depuis `.codexspec/specs/`
- **Un argument** : traité comme chemin vers `tasks.md`, les autres déduits du même répertoire
- **Trois arguments** : chemins explicites vers spec.md, plan.md et tasks.md

**Ce qu'elle fait :**

- Lit tasks.md et identifie les tâches incomplètes
- Applique le flux TDD pour les tâches de code :
  - **Red** : écrire d'abord les tests en échec
  - **Green** : implémenter pour faire passer les tests
  - **Verify** : exécuter tous les tests
  - **Refactor** : améliorer tout en gardant les tests au vert
- Implémentation directe pour les tâches non testables (docs, config)
- Met à jour les cases à cocher des tâches au fil de l'avancement
- Consigne les blocages dans issues.md le cas échéant

**Flux TDD pour les tâches de code :**

```
Red → Green → Verify → Refactor → Mark Complete
```

**Implémentation directe pour le non-testable :**

- Fichiers de documentation
- Fichiers de configuration
- Assets statiques
- Fichiers d'infrastructure

**Exemple :**

```text
You: /codexspec:implement-tasks

AI:  Starting implementation...

     Loading context:
     - spec.md ✓
     - plan.md ✓
     - tasks.md ✓
     - constitution.md ✓

     Tech Stack: Python 3.11+ / FastAPI / PostgreSQL / pytest

     Working on Task 1.1: Setup Project Structure
     ✓ Created src/taskman/__init__.py
     ✓ Created pyproject.toml
     [x] Task 1.1 Complete

     Working on Task 2.1: Write Tests for Task Entity [P]
     ✓ Created tests/test_task.py
     Running tests... 5 passed (all expected failures)
     [x] Task 2.1 Complete

     Working on Task 2.2: Implement Task Entity
     ✓ Created src/taskman/models/task.py
     Running tests... 5 passed
     [x] Task 2.2 Complete

     ...
```

**Conseils :**

- Peut reprendre là où elle s'était arrêtée en cas d'interruption
- Les blocages sont consignés dans issues.md
- Les commits sont effectués après des tâches/phases significatives
- Lancez d'abord `/codexspec:review-tasks` pour validation

---

### `/codexspec:review-spec`

Valide la spécification vis-à-vis des exigences confirmées et de sa propre qualité interne.

**Syntaxe :**

```
/codexspec:review-spec [chemin_vers_spec.md]
```

**Arguments :**

| Argument | Requis | Description |
|----------|--------|-------------|
| `chemin_vers_spec.md` | Non | Chemin vers le fichier spec (détecté automatiquement si non fourni) |

**Ce qu'elle fait :**

- Vérifie la fidélité aux entrées confirmées de `requirements.md`
- Contrôle la cohérence interne, la clarté et la vérifiabilité
- Ne traite l'absence d'une section de template comme un défaut que lorsque le contenu authentique l'exige
- Exige de chaque défaut qu'il inclue `Evidence`, `Location`, `Mismatch`, `Impact` et `Remediation`
- Sépare les `Risk Advisories / Design Opportunities` des défauts
- Génère un statut ainsi qu'un score de compatibilité dérivé des constats classés

**Contrat de revue partagé :**

| Catégorie | Signification |
|-----------|---------------|
| Défaut de fidélité | Conflit avec une source authentique ou omission de celle-ci |
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

- Lancez-la avant `/codexspec:spec-to-plan`
- Considérez `BLOCKED` et `NEEDS_REVISION` comme non prêts à continuer
- Ne transformez pas les avis en exigences
- Relancez après avoir appliqué des correctifs

---

### `/codexspec:review-plan`

Examine le plan technique d'implémentation sous l'angle de la fidélité, de la faisabilité et de la justification des décisions techniques.

**Syntaxe :**

```
/codexspec:review-plan [chemin_vers_plan.md]
```

**Arguments :**

| Argument | Requis | Description |
|----------|--------|-------------|
| `chemin_vers_plan.md` | Non | Chemin vers le fichier plan (détecté automatiquement si non fourni) |

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

---

### `/codexspec:review-tasks`

Valide le découpage en tâches sous l'angle de la couverture, des résultats vérifiables, de l'ordonnancement correct et de la faisabilité des dépendances.

**Syntaxe :**

```
/codexspec:review-tasks [chemin_vers_tasks.md]
```

**Arguments :**

| Argument | Requis | Description |
|----------|--------|-------------|
| `chemin_vers_tasks.md` | Non | Chemin vers le fichier tasks (détecté automatiquement si non fourni) |

**Ce qu'elle fait :**

- Vérifie que tous les éléments requis du plan et des exigences disposent d'une couverture par tâche
- Ne valide l'ordre test-first que lorsqu'une source authentique l'exige
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
- Les constats d'ordre des tests ne sont des défauts que lorsqu'une source authentique requiert le test
- Vérifiez l'exactitude des marqueurs de parallélisation
- Contrôlez que les chemins de fichiers correspondent à la structure du projet

---

### `/codexspec:analyze`

Effectue une analyse de cohérence non destructrice entre requirements.md, spec.md, plan.md et tasks.md. Identifie les conflits d'autorité, les lacunes de traçabilité, les doublons et les couvertures manquantes.

**Syntaxe :**

```
/codexspec:analyze
```

**Arguments :**

| Argument | Requis | Description |
|----------|--------|-------------|
| Aucun | - | Analyse les artifacts de la fonctionnalité courante |

**Ce qu'elle fait :**

- Détecte les doublons entre artifacts
- Identifie les ambiguïtés dépourvues de critères mesurables
- Repère les éléments sous-spécifiés
- Vérifie l'alignement avec la constitution
- Cartographie la couverture des exigences vers les tâches
- Rapporte les incohérences de terminologie et d'ordonnancement

**Niveaux de sévérité :**

| Niveau | Définition |
|--------|------------|
| **CRITICAL** | Violation de constitution, artifact central manquant, couverture nulle |
| **HIGH** | Exigence en doublon/en conflit, attribut de sécurité ambigu |
| **MEDIUM** | Dérive terminologique, couverture non fonctionnelle manquante |
| **LOW** | Améliorations de style/formulation |

**Exemple :**

```text
You: /codexspec:analyze

AI:  Analyzing artifacts...

     # Specification Analysis Report

     ## Coverage Summary
     | Requirement Key | Has Task? | Task IDs |
     |-----------------|-----------|----------|
     | REQ-001 | ✅ | 2.1, 2.2 |
     | REQ-002 | ✅ | 2.3, 2.4 |
     | REQ-003 | ❌ | None |

     ## Issues Found

     | ID | Category | Severity | Summary |
     |----|----------|----------|---------|
     | A1 | Coverage | CRITICAL | REQ-003 has no task coverage |
     | A2 | Duplication | HIGH | REQ-005 and REQ-008 overlap |
     | A3 | Ambiguity | MEDIUM | NFR-002 "secure" not defined |

     ## Metrics
     - Total Requirements: 12
     - Total Tasks: 24
     - Coverage: 92% (11/12 requirements)
     - Critical Issues: 1

     ## Next Actions
     1. Add tasks for REQ-003 (CRITICAL)
     2. Consider merging REQ-005 and REQ-008
     3. Define "secure" in NFR-002

     Resolve CRITICAL issues before /codexspec:implement-tasks
```

**Conseils :**

- Lancez-la après `/codexspec:plan-to-tasks`, avant l'implémentation
- Les problèmes CRITICAL doivent bloquer l'implémentation
- Analyse en lecture seule — aucun fichier n'est modifié
- Utilisez les constats pour améliorer la qualité des artifacts

---

### `/codexspec:checklist`

Génère des checklists qualité pour valider la complétude, la clarté et la cohérence des exigences. Il s'agit en quelque sorte de « tests unitaires pour la rédaction d'exigences ».

**Syntaxe :**

```
/codexspec:checklist [domaine_cible]
```

**Arguments :**

| Argument | Requis | Description |
|----------|--------|-------------|
| `domaine_cible` | Non | Domaine ciblé (par ex. « ux », « api », « security », « performance ») |

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

---

### `/codexspec:commit-staged`

Génère un message de commit conforme à Conventional Commits à partir des changements git stagés, avec conscience du contexte de session. Cette commande comprend votre session de développement pour produire des messages de commit pertinents.

**Syntaxe :**

```
/codexspec:commit-staged [-p]
```

**Arguments :**

| Argument | Requis | Description |
|----------|--------|-------------|
| `-p` | Non | Mode aperçu — affiche le message sans committer |

**Ce qu'elle fait :**

- Exécute `git diff --staged` pour récupérer les changements stagés
- Analyse les changements et le contexte de session pour comprendre l'intention
- Suit la spécification Conventional Commits
- En mode exécution (par défaut) : commit directement après génération du message
- En mode aperçu (`-p`) : affiche le message sans committer
- Signale une erreur si aucun changement n'est stagé

**Exemple :**

```text
You: /codexspec:commit-staged

AI:  Analyzing staged changes...

     Files staged:
     - src/auth/service.py
     - tests/test_auth.py

     Generated commit message:
     feat(auth): implement token refresh logic

     - Add refresh token generation
     - Include token expiration handling
     - Add tests for refresh flow

     Executing commit...

     ✓ Committed: def5678
```

**Exemple en mode aperçu :**

```text
You: /codexspec:commit-staged -p

AI:  Preview mode - no commit will be executed

     Suggested commit message:
     feat(auth): implement token refresh logic

     - Add refresh token generation
     - Include token expiration handling
     - Add tests for refresh flow
```

**Conseils :**

- Stagez d'abord les changements avec `git add`
- N'analyse que le contenu stagé — respecte le flux de commit en deux étapes de Git
- Prend en compte le contexte de session pour des messages pertinents
- Utilisez le flag `-p` pour un aperçu avant de committer
- Suit la spécification Conventional Commits par défaut

---

### `/codexspec:review-code`

Examine la modification Git sélectionnée comme un contrôle de défauts strict avant fusion. La cible par défaut comprend l'écart complet de la fonctionnalité ; les sélecteurs explicites choisissent les changements validés, non validés ou un commit unique, sans accepter de filtre de chemin.

<!-- REVIEW-CODE-BREAKING: DEFAULT-GATE -->
<!-- REVIEW-CODE-BREAKING: PATH-AUDIT -->

**Changement incompatible dans la prochaine version :**

- La commande par défaut devient un contrôle de défauts limité au changement, et non un score général de qualité.
- Les chemins positionnels ne sont plus valides. Utilisez explicitement `--audit` pour le score consultatif de qualité par chemin.

**Syntaxe du contrôle de défauts :**

```text
/codexspec:review-code
/codexspec:review-code --committed [--base <branch>] [--feature <feature-dir>] [--focus <instructions>]
/codexspec:review-code --uncommitted [--feature <feature-dir>] [--focus <instructions>]
/codexspec:review-code --commit <sha> [--parent <n>] [--feature <feature-dir>] [--focus <instructions>]
```

Le contrôle inventorie tous les artefacts sélectionnés, évalue les exigences applicables et exécute les phases Scope, Behavior, Risk et Verification. Le verdict est `PASS`, `FAIL` ou `INCONCLUSIVE`. Les six sections du rapport sont suivies d'un unique envelope `<review-code-result>` lisible par machine. Tout défaut P0-P3 produit `FAIL` ; l'absence de preuve obligatoire produit `INCONCLUSIVE`.

```text
You: /codexspec:review-code --feature .codexspec/specs/2026-0714-example

AI:  ## Verdict
     **PASS** — les revues et vérifications obligatoires sont terminées sans défaut.
```

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
| `chemin...` | Non | Un ou plusieurs fichiers ou répertoires sources à examiner (séparés par des espaces). Par défaut `src/` si omis |

**Ce qu'elle fait :**

- Détecte le ou les langages principaux à partir des extensions de fichiers et exécute un passage par langage pour les cibles multi-langages
- Lance les outils d'analyse statique lorsque leur config est présente (`ruff`/`mypy`, `eslint`/`tsc`, `go vet`/`gofmt`, `cargo check`/`cargo clippy`, `shellcheck`) ; les ignore gracieusement et signale une couverture dégradée sinon
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

- Passez plusieurs chemins pour examiner une tranche ciblée, par ex. `src/ tests/`
- Le score est consultatif ; les constats CRITICAL/HIGH constituent le signal actionnable
- Pour des projets exclusivement Python ou React, préférez les commandes dédiées `/codexspec:review-python-code` ou `/codexspec:review-react-code` pour des vérifications plus profondes et spécifiques au langage
- Relancez après corrections pour confirmer la remontée du score (≥ 95 attendu une fois les problèmes CRITICAL/HIGH résolus)

---

### `/codexspec:review-python-code`

Examine du code Python sous l'angle de la conformité PEP 8, de la sécurité des types, de la robustesse d'ingénierie et de la cohérence avec la constitution.

**Syntaxe :**

```
/codexspec:review-python-code [chemin...]
```

**Arguments :**

| Argument | Requis | Description |
|----------|--------|-------------|
| `chemin...` | Non | Un ou plusieurs fichiers ou répertoires Python à examiner (séparés par des espaces). Par défaut `src/` si omis |

**Ce qu'elle fait :**

- Lance `ruff check` pour les résultats PEP 8 / linting et `mypy` pour le contrôle de types
- Examine quatre dimensions spécifiques à Python : Principe Pythonic & KISS, Sécurité et explicité des types, Robustesse d'ingénierie, Alignement avec la constitution
- Vérifie la complétude des annotations de type, la gestion large des exceptions et la préservation du contexte via `raise ... from err`
- Valide la gestion des ressources (`with` context managers), la correction async/await et la discipline du `logging` structuré
- Recoupe les constats avec les principes MUST/SHOULD de `.codexspec/memory/constitution.md` lorsqu'il est présent
- Classe les constats par sévérité : CRITICAL (violations MUST de la constitution, bugs de logique, failles de sécurité), HIGH (lacunes de sécurité des types, erreurs ruff/mypy, fuites de ressources), MEDIUM (opportunités de design/refactor, annotations manquantes), LOW (lisibilité, sucre syntaxique Pythonic)

**Exemple :**

```text
You: /codexspec:review-python-code src/codexspec/

AI:  # Python Code Review Report

     ## Static Analysis
     | Tool  | Status | Issues |
     |-------|--------|--------|
     | ruff  | Pass   | 0      |
     | mypy  | Pass   | 0      |

     ## Findings
     ### Warnings (HIGH)
     - [ ] [CODE-002] src/codexspec/__init__.py:218 - public function missing return type annotation
       Suggestion: add the return type and verify with mypy.

     ### Suggestions (LOW)
     - [ ] [CODE-004] src/codexspec/cli.py:140 - use `pathlib.Path` instead of `os.path` string concatenation
```

**Conseils :**

- À utiliser à la place de `/codexspec:review-code` lorsque la cible est uniquement Python et que vous souhaitez la profondeur PEP 8 / sécurité des types
- `ruff` et `mypy` doivent être installés et configurés dans le projet cible pour une couverture complète ; la commande signale une couverture dégradée en leur absence
- Les principes MUST de la constitution sont notés ; les méta-principes agnostiques du langage (testabilité, simplicité) s'appliquent en l'absence de constitution

---

### `/codexspec:review-react-code`

Examine du code React/TypeScript sous l'angle de l'architecture des composants, des règles des Hooks, de la gestion d'état, de la performance et de la cohérence avec la constitution.

**Syntaxe :**

```
/codexspec:review-react-code [chemin...]
```

**Arguments :**

| Argument | Requis | Description |
|----------|--------|-------------|
| `chemin...` | Non | Un ou plusieurs fichiers ou répertoires React/TypeScript à examiner (séparés par des espaces ; attend `.tsx`, `.ts`, `.jsx`, `.js`). Par défaut `src/` si omis |

**Ce qu'elle fait :**

- Lance `npx eslint` (lorsqu'une config ESLint existe) et `npx tsc --noEmit` (lorsqu'un `tsconfig.json` existe)
- Examine quatre dimensions spécifiques à React : Atomicité et responsabilité unique des composants, Conformité aux Hooks et gestion des effets de bord, Gestion d'état et flux de données, Performance et robustesse
- Vérifie que les tableaux de dépendances des `useEffect` sont exhaustifs, détecte l'usage abusif d'état dérivé comme état, et signale les effets superflus
- Détecte les risques de closure périmée, les nettoyages d'effet manquants, le prop drilling, les rendus coûteux non mémoïsés, ainsi que les états de chargement/erreur manquants
- Recoupe les constats avec `.codexspec/memory/constitution.md` lorsqu'il est présent
- Classe les constats par sévérité : CRITICAL (violations des règles des Hooks, conditions de course), HIGH (nettoyage manquant, promesses rejetées non gérées), MEDIUM (candidats au refactor), LOW (lisibilité)

**Exemple :**

```text
You: /codexspec:review-react-code src/components/

AI:  # React Code Review Report

     ## Static Analysis
     | Tool  | Status | Issues |
     |-------|--------|--------|
     | eslint| Warn   | 2      |
     | tsc   | Pass   | 0      |

     ## Findings
     ### Critical Issues (CRITICAL)
     - [ ] [CODE-001] src/components/UserProfile.tsx:38 - `useEffect` missing `userId` in dependency array
       Impact: stale closure fetches the wrong user after navigation.
       Suggestion: add `userId` to the dependency array or extract to a custom hook.

     ### Suggestions (LOW)
     - [ ] [CODE-004] src/components/Button.tsx:12 - extract derived value instead of `useState`
```

**Conseils :**

- À utiliser à la place de `/codexspec:review-code` lorsque la cible est uniquement React/TypeScript et que vous souhaitez de la profondeur sur les Hooks et l'architecture composant
- ESLint et un `tsconfig.json` doivent être présents pour une couverture complète ; la commande signale une couverture dégradée en leur absence
- Les constats React se superposent aux vérifications TypeScript de base, de sorte que les problèmes de sécurité des types restent remontés

---

### `/codexspec:quick`

Exécute un flux Requirements-First SDD allégé pour les petits changements.

**Syntaxe :**

```
/codexspec:quick [décrivez une petite exigence]
```

**Arguments :**

| Argument | Requis | Description |
|----------|--------|-------------|
| `décrivez une petite exigence` | Non | Brève description du petit changement bien délimité (vous serez sollicité si non fournie) |

**Ce qu'elle fait :**

- Évalue le périmètre (fichiers touchés, étendue des modules, nouvelles dépendances, décisions produit non tranchées) et, si le changement est large ou a plusieurs résultats indépendants, recommande le flux standard
- Crée un espace de travail de fonctionnalité et `requirements.md` en utilisant la même convention d'horodatage que `/codexspec:specify`
- Résout uniquement les ambiguïtés qui modifient matériellement l'implémentation ; présente un résumé concis des éléments confirmés (`NEED-*`, `CON-*`/`DEC-*` pertinents, `OUT-*`, `OPEN-*` non résolus)
- S'arrête à la Confirmation Gate : rien n'est généré tant que vous n'avez pas confirmé le résumé
- Enchaîne les commandes de génération sur le nouveau répertoire de fonctionnalité : `/codexspec:generate-spec`, `/codexspec:spec-to-plan`, `/codexspec:plan-to-tasks`, `/codexspec:implement-tasks`
- S'en remet à la propre boucle d'auto-review de chaque commande de génération ; s'interrompt et demande à l'utilisateur si une revue requiert une nouvelle décision produit ou architecture
- Rapporte séparément le répertoire de la fonctionnalité, les chemins d'artifacts, les résultats des revues, la vérification de l'implémentation et les avis non résolus

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

AI:  Running generate-spec → spec-to-plan → plan-to-tasks → implement-tasks ...

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

### `/codexspec:pr`

Génère une description structurée de Pull Request GitHub / Merge Request GitLab à partir du diff git. S'intègre facultativement à `spec.md` pour un contexte tracé par SDD.

**Syntaxe :**

```
/codexspec:pr [--target-branch <branche>] [--sections <liste>] [--spec <id-ou-chemin>] [--output <fichier>]
```

**Arguments :**

| Argument | Requis | Description |
|----------|--------|-------------|
| `--target-branch <branche>` | Non | Branche de comparaison (par défaut : `origin/main`) |
| `--sections <liste>` | Non | Sous-ensemble séparé par des virgules parmi `summary, changes, testing, verify, checklist, notes` (par défaut : `all`) |
| `--spec <id-ou-chemin>` | Non | Intégration opt-in de spec : un identifiant de fonctionnalité (par ex. `2025-0321-1430k7-auth`) résolu sous `.codexspec/specs/`, ou un chemin explicite `path/to/spec.md`. Omettre pour générer uniquement depuis git |
| `--output <fichier>` | Non | Enregistrer la description dans un fichier plutôt que dans le terminal |

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
- Consultez l'[étude de cas du générateur de descriptions de PR](../case-studies/case-study-pr-description-generator.md) pour un exemple complet et bout-en-bout de cette commande (notamment la façon dont le contexte spec.md est câblé)

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

You: Output language (base) → zh-CN

AI:  ✓ Updated language.output: "zh-CN"
     (interaction and document fall back to output, then en.)
```

**Conseils :**

- Utilisez `/codexspec:config --view` pour inspecter l'état courant avant toute modification
- Une config neuve ou réinitialisée n'écrit que `output` ; ne réglez `interaction`/`document` que lorsqu'ils doivent différer de `output`
- Pour des changements scriptés dans un terminal, préférez le CLI `codexspec config` (`--set-lang`, `--set-interaction-lang`, `--set-document-lang`, `--set-commit-lang`, `--auto-next`)

---

## Vue d'ensemble du flux de travail

```text
Idea → /specify → requirements.md → /generate-spec → spec.md → /spec-to-plan → plan.md → /plan-to-tasks → tasks.md → /implement
                                                   │                         │                            │
                                              Review spec               Review plan                  Review tasks
```

Chaque revue est un point de contrôle humain. Elle valide la fidélité et la qualité intrinsèque à l'aide de constats étayés par des preuves. Les suggestions de conception consultatives restent séparées et ne bloquent jamais la progression. Les défauts vérifiés peuvent être corrigés puis ré-examinés pendant deux tours au maximum.

---

## Dépannage

### « Feature directory not found »

La commande n'a pas pu localiser le répertoire de la fonctionnalité.

**Solutions :**

- Lancez d'abord `codexspec init` pour initialiser le projet
- Vérifiez que le répertoire `.codexspec/specs/` existe
- Assurez-vous d'être dans le bon répertoire de projet
- Passez un répertoire de fonctionnalité explicite ou un chemin d'artifact lorsque plusieurs candidats existent

### « No spec.md found »

Le fichier de spécification n'existe pas encore.

**Solutions :**

- Lancez `/codexspec:specify` pour clarifier d'abord les exigences
- Puis lancez `/codexspec:generate-spec` pour créer spec.md

### « Constitution not found »

Aucune constitution de projet n'existe.

**Solutions :**

- Lancez `/codexspec:constitution` pour en créer une
- La constitution est facultative mais recommandée pour des décisions cohérentes

### « Tasks file not found »

Le découpage en tâches n'existe pas.

**Solutions :**

- Assurez-vous d'avoir lancé `/codexspec:spec-to-plan` d'abord
- Puis lancez `/codexspec:plan-to-tasks` pour créer tasks.md

### « GitHub CLI not authenticated »

La commande `/codexspec:tasks-to-issues` requiert l'authentification GitHub.

**Solutions :**

- Installez GitHub CLI : `brew install gh` (macOS) ou équivalent
- Authentifiez-vous : `gh auth login`
- Vérifiez : `gh auth status`

---

## Prochaines étapes

- [Flux de travail](workflow.md) - Motifs courants et moment d'utiliser chaque commande
- [CLI](../reference/cli.md) - Commandes terminal pour l'initialisation du projet

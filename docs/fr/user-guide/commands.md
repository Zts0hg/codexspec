# Commandes

Ceci est la reference des commandes slash de CodexSpec. Ces commandes sont invoquees dans l'interface de chat de Claude Code.

Pour les patterns de workflow et quand utiliser chaque commande, voir [Workflow](workflow.md). Pour les commandes CLI, voir [CLI](../reference/cli.md).

## Reference Rapide

| Commande | Objectif |
|----------|----------|
| `/codexspec:constitution` | Creer ou mettre a jour la constitution du projet avec validation croisee des artefacts |
| `/codexspec:specify` | Clarifier les exigences via Q&R interactives |
| `/codexspec:generate-spec` | Generer le document spec.md a partir des exigences clarifiees |
| `/codexspec:clarify` | Scanner un spec existant pour les ambiguites (raffinement iteratif) |
| `/codexspec:spec-to-plan` | Convertir la specification en plan d'implementation technique |
| `/codexspec:plan-to-tasks` | Decomposer le plan en taches atomiques avec application TDD |
| `/codexspec:implement-tasks` | Executer les taches avec le workflow TDD conditionnel |
| `/codexspec:review-spec` | Valider la specification pour completude et qualite |
| `/codexspec:review-plan` | Reverifier le plan technique pour faisabilite et alignement |
| `/codexspec:review-tasks` | Valider la decomposition des taches pour conformite TDD |
| `/codexspec:analyze` | Analyse de coherence croisee des artefacts (lecture seule) |
| `/codexspec:checklist` | Generer des listes de controle de qualite des exigences |
| `/codexspec:tasks-to-issues` | Convertir les taches en issues GitHub |
| `/codexspec:commit-staged` | Generer un message de commit a partir des changements stages (avec conscience du contexte de session) |

---

## Categories de Commandes

### Commandes de Workflow Principal

Commandes pour le workflow SDD principal : Constitution -> Specification -> Plan -> Taches -> Implementation.

### Commandes de Revision (Portes Qualite)

Commandes qui valident les artefacts a chaque etape du workflow. **Recommande avant de passer a l'etape suivante.**

### Commandes Avancees

Commandes pour le raffinement iteratif, la validation croisee des artefacts et l'integration de gestion de projet.

---

## Reference des Commandes

### `/codexspec:constitution`

Creer ou mettre a jour la constitution du projet. La constitution definit les principes architecturaux, la pile technologique, les standards de code et les regles de gouvernance qui guident toutes les decisions de developpement subsequentes.

**Syntaxe :**

```
/codexspec:constitution [description des principes]
```

**Arguments :**

| Argument | Requis | Description |
|----------|--------|-------------|
| `description des principes` | Non | Description des principes a inclure (sera demande si non fourni) |

**Ce qu'il fait :**

- Cree `.codexspec/memory/constitution.md` s'il n'existe pas
- Met a jour la constitution existante avec de nouveaux principes
- Valide la coherence croisee des artefacts avec les modeles
- Genere un Rapport d'Impact de Synchronisation montrant les changements et fichiers affectes
- Inclut une revue de constitutionnalite pour les modeles dependants

**Ce qu'il cree :**

```
.codexspec/
+-- memory/
    +-- constitution.md    # Document de gouvernance du projet
```

**Exemple :**

```text
Vous : /codexspec:constitution Axer sur la qualite du code, les standards de test et l'architecture propre

AI  : Creation de la constitution...

     + Cree .codexspec/memory/constitution.md
     Version : 1.0.0

     Rapport d'Impact de Synchronisation :
     - plan-template-*.md : + aligne
     - spec-template-*.md : + aligne
     - tasks-template-*.md : + aligne

     Principes Core :
     1. Qualite du Code d'Abord
     2. Developpement Pilote par les Tests
     3. Architecture Propre

     Commit suggere : docs: create constitution v1.0.0
```

**Conseils :**

- Definir les principes tot dans le projet pour une prise de decision coherente
- Inclure a la fois les principes techniques et de processus
- Reverifier la constitution avant le developpement de fonctionnalites majeures
- Les changements de constitution declenchent une validation croisee des artefacts

---

### `/codexspec:specify`

Clarifier les exigences via Q&R interactives. Cette commande explore votre idee initiale sans creer aucun fichier - vous gardez un controle total.

**Syntaxe :**

```
/codexspec:specify [votre idee ou exigence]
```

**Arguments :**

| Argument | Requis | Description |
|----------|--------|-------------|
| `votre idee ou exigence` | Non | Description initiale de ce que vous voulez construire (sera demande si non fourni) |

**Ce qu'il fait :**

- Pose des questions de clarification pour comprendre votre idee
- Explore les cas limites que vous n'avez peut-etre pas envisages
- Co-cree des exigences de haute qualite via le dialogue
- Se concentre sur le "quoi" et le "pourquoi", pas l'implementation technique
- **Ne genere PAS de fichiers** - vous decidez quand creer la documentation

**Ce qu'il ne cree PAS :**

- Aucun fichier n'est cree pendant cette commande
- Les exigences restent dans la conversation jusqu'a votre approbation

**Exemple :**

```text
Vous : /codexspec:specify Je veux construire une application de gestion de taches

AI  : Super ! Laissez-moi vous aider a clarifier les exigences.

     D'abord, qui sont les utilisateurs cibles de cette application ?
     - Professionnels individuels
     - Petites equipes
     - Organisations d'entreprise
     - Tous les precedents

Vous : Petites equipes, principalement des equipes de developpement logiciel

AI  : Compris. Pour les petites equipes de dev :
     - Avez-vous besoin de fonctionnalites de collaboration en temps reel ?
     - Les taches doivent-elles prendre en charge les sous-taches ou juste des listes plates ?
     - Des exigences d'integration (GitHub, Slack, etc.) ?

Vous : Le temps reel est important. Sous-taches oui. L'integration GitHub serait bien.

AI  : [Continue a explorer les exigences...]

     Resume des exigences clarifiees :
     - Cible : Petites equipes de dev (5-20 personnes)
     - Core : Taches avec sous-taches, mises a jour en temps reel
     - Integration : GitHub (optionnel)
     - Priorite : Collaboration temps reel > Sous-taches > GitHub

     Pret a generer le document de spec ?
     Utilisez /codexspec:generate-spec pour creer spec.md
```

**Conseils :**

- Utiliser pour l'exploration initiale des exigences
- Ne vous inquietez pas d'etre complet - le raffinement est iteratif
- Posez des questions si l'AI fait des suppositions
- Reverifier le resume avant de generer le spec

---

### `/codexspec:generate-spec`

Generer le document `spec.md` a partir des exigences clarifiees. Cette commande agit comme un "compilateur d'exigences" qui transforme vos exigences clarifiees en une specification structuree.

**Syntaxe :**

```
/codexspec:generate-spec
```

**Arguments :**

| Argument | Requis | Description |
|----------|--------|-------------|
| Aucun | - | Utilise le contexte de la session `/codexspec:specify` precedente |

**Ce qu'il fait :**

- Cree le repertoire `.codexspec/specs/{NNN}-{nom-fonctionnalite}/`
- Genere un `spec.md` complet avec :
  - Apercu de la fonctionnalite et objectifs
  - Recits utilisateur avec criteres d'acceptation
  - Exigences fonctionnelles (format REQ-XXX)
  - Exigences non-fonctionnelles (format NFR-XXX)
  - Cas limites et approches de gestion
  - Elements hors du cadre

**Ce qu'il cree :**

```
.codexspec/
+-- specs/
    +-- 001-task-management/
        +-- spec.md
```

**Exemple :**

```text
Vous : /codexspec:generate-spec

AI  : Generation de la specification...

     + Cree .codexspec/specs/001-task-management/spec.md

     Sections incluses :
     - Apercu : Gestion de taches pour petites equipes de dev
     - 4 Recits Utilisateur avec criteres d'acceptation
     - 12 Exigences Fonctionnelles (REQ-001 a REQ-012)
     - 3 Exigences Non-Fonctionnelles (NFR-001 a NFR-003)
     - 5 Cas Limites documentes
     - Hors du Cadre : Applications mobiles, SSO Entreprise

     Prochaines etapes :
     - Reverifier le spec avec /codexspec:review-spec
     - Ou passer a /codexspec:spec-to-plan
```

**Conseils :**

- Executer apres que `/codexspec:specify` ait clarifie les exigences
- Reverifier le spec genere avant de poursuivre
- Utiliser `/codexspec:review-spec` pour la validation de qualite
- Modifier spec.md directement si des ajustements mineurs sont necessaires

---

### `/codexspec:clarify`

Scanner une specification existante pour les ambiguites et lacunes. Utilisez ceci pour le raffinement iteratif apres la creation initiale du spec.

**Syntaxe :**

```
/codexspec:clarify [chemin_vers_spec.md]
```

**Arguments :**

| Argument | Requis | Description |
|----------|--------|-------------|
| `chemin_vers_spec.md` | Non | Chemin vers le fichier spec (auto-detecte si non fourni) |

**Ce qu'il fait :**

- Scanne le spec en utilisant 4 categories d'ambiguite ciblees
- Pose des questions de clarification ciblees (max 5)
- Met a jour spec.md avec les reponses de clarification
- S'integre avec les resultats de review-spec si disponibles

**Categories d'Ambiguite :**

| Categorie | Ce qu'elle Detecte |
|-----------|-------------------|
| **Lacunes de Completude** | Sections manquantes, contenu vide, criteres d'acceptation absents |
| **Problemes de Specificite** | Termes vagues ("rapide", "evolutif"), contraintes non definies |
| **Clarte Comportementale** | Lacunes de gestion d'erreurs, transitions d'etat non definies |
| **Problemes de Mesurabilite** | Exigences non-fonctionnelles sans metriques |

**Exemple :**

```text
Vous : /codexspec:clarify

AI  : Scan de spec.md pour les ambiguites...

     Problemes trouves dans 3 categories.

     ## Question 1/5 : Specificite

     **Contexte** : NFR-001 stipule "Le systeme doit repondre rapidement"

     **Question** : Quel est le temps de reponse cible ?

     | Option | Description | Impact |
     |--------|-------------|--------|
     | A | < 100ms pour toutes les operations | Exigence de haute performance |
     | B | < 500ms pour les lectures, < 1s pour les ecritures | Approche equilibree |
     | Personnalise | Fournir une reponse differente | - |

     **Recommandation** : Option B - equilibree pour une application web typique

Vous : B

AI  : + Mis a jour NFR-001 : Temps de reponse < 500ms lectures, < 1s ecritures
     Ajoute a la section Clarifications dans spec.md
```

**Conseils :**

- Utiliser quand spec.md existe mais necessite un raffinement
- S'integre avec les resultats de `/codexspec:review-spec`
- Maximum 5 questions par session
- Executer plusieurs fois pour les specifications complexes

---

### `/codexspec:spec-to-plan`

Convertir la specification de fonctionnalite en plan d'implementation technique. C'est ici que vous definissez **comment** la fonctionnalite sera construite.

**Syntaxe :**

```
/codexspec:spec-to-plan [chemin_vers_spec.md]
```

**Arguments :**

| Argument | Requis | Description |
|----------|--------|-------------|
| `chemin_vers_spec.md` | Non | Chemin vers le fichier spec (auto-detecte depuis `.codexspec/specs/` si non fourni) |

**Ce qu'il fait :**

- Lit la specification et la constitution
- Definit la pile technologique avec contraintes de version
- Effectue une revue de constitutionnalite (obligatoire si une constitution existe)
- Cree une architecture avec graphe de dependance de modules
- Documente les decisions techniques avec justification
- Planifie les phases d'implementation

**Ce qu'il cree :**

```
.codexspec/
+-- specs/
    +-- 001-task-management/
        +-- plan.md    # Plan d'implementation technique
```

**Exemple :**

```text
Vous : /codexspec:spec-to-plan Utiliser Python FastAPI pour le backend, React pour le frontend, PostgreSQL pour la base de donnees

AI  : Generation du plan technique...

     Revue de Constitutionnalite :
     + Architecture Propre : Conception modulaire avec limites claires
     + TDD : Approche test-first appliquee dans les phases
     + Qualite du Code : Linting et indices de type requis

     Architecture :
     - Backend : FastAPI avec architecture en couches
     - Frontend : React avec structure de composants
     - Base de donnees : PostgreSQL avec strategie de migration

     Graphe de Dependance des Modules :
     +-------------+
     |    API      |
     +------+------+
            |
     +------v------+
     |  Services   |
     +------+------+
            |
     +------v------+
     |    Data     |
     +-------------+

     + Cree plan.md
     5 Phases d'Implementation definies
```

**Conseils :**

- Executer apres que le spec est revu et stable
- La revue de constitutionnalite est obligatoire si une constitution existe
- Inclure les sections pertinentes selon le type de projet
- Reverifier le plan avant de passer aux taches

---

### `/codexspec:plan-to-tasks**

Decomposer le plan technique en taches atomiques et actionnables avec application TDD.

**Syntaxe :**

```
/codexspec:plan-to-tasks [chemin_vers_spec.md chemin_vers_plan.md]
```

**Arguments :**

| Argument | Requis | Description |
|----------|--------|-------------|
| `chemins` | Non | Chemins vers spec et plan (auto-detectes si non fournis) |

**Ce qu'il fait :**

- Cree des taches atomiques (un fichier principal par tache)
- Applique TDD : taches de test precedent les taches d'implementation
- Marque les taches parallelisables avec `[P]`
- Specifie les chemins de fichiers exacts pour chaque tache
- Definit des points de controle de phase

**Ce qu'il cree :**

```
.codexspec/
+-- specs/
    +-- 001-task-management/
        +-- tasks.md    # Decomposition des taches
```

**Structure de Tache :**

```markdown
### Tache 2.1 : Ecrire les Tests pour l'Entite A [P]
- **Type** : Testing
- **Fichiers** : `tests/test_entity_a.py`
- **Description** : Ecrire les tests unitaires pour l'Entite A
- **Dependances** : Tache 1.3
- **Complexite Est.** : Faible
```

**Exemple :**

```text
Vous : /codexspec:plan-to-tasks

AI  : Decomposition du plan en taches...

     + Cree tasks.md
     Total : 24 taches
     Parallelisables : 8 taches (33%)

     Phase 1 : Fondation (4 taches)
     Phase 2 : Implementation Core - TDD (10 taches)
     Phase 3 : Integration (4 taches)
     Phase 4 : Couche Interface (3 taches)
     Phase 5 : Test et Documentation (3 taches)

     Ordre d'Execution :
     Phase 1 -> [Phase 2 taches en groupes paralleles] -> Phase 3 -> Phase 4 -> Phase 5

     Points de controle definis a chaque limite de phase.
```

**Conseils :**

- Chaque tache devrait impliquer un seul fichier principal
- Les taches de test precedent toujours les taches d'implementation
- `[P]` marque les taches vraiment independantes parallelisables
- Reverifier les dependances avant l'implementation

---

### `/codexspec:implement-tasks`

Executer les taches d'implementation avec le workflow TDD conditionnel. Travaille systematiquement a travers la liste des taches.

**Syntaxe :**

```
/codexspec:implement-tasks [chemin_taches]
/codexspec:implement-tasks [chemin_spec chemin_plan chemin_taches]
```

**Arguments :**

| Argument | Requis | Description |
|----------|--------|-------------|
| `chemin_taches` | Non | Chemin vers tasks.md (auto-detecte si non fourni) |
| `chemin_spec chemin_plan chemin_taches` | Non | Chemins explicites vers les trois documents |

**Resolution de Fichier :**

- **Aucun argument** : Auto-detection depuis `.codexspec/specs/`
- **Un argument** : Traite comme chemin `tasks.md`, derive les autres du meme repertoire
- **Trois arguments** : Chemins explicites vers spec.md, plan.md et tasks.md

**Ce qu'il fait :**

- Lit tasks.md et identifie les taches incompletes
- Applique le workflow TDD pour les taches de code :
  - **Rouge** : Ecrire les tests echouants d'abord
  - **Vert** : Implementer pour passer les tests
  - **Verifier** : Executer tous les tests
  - **Refactorer** : Ameliorer tout en gardant les tests verts
- Implementation directe pour les taches non testables (docs, config)
- Met a jour les cases a cocher des taches au fur et a mesure de la progression
- Enregistre les bloqueurs dans issues.md si rencontres

**Workflow TDD pour Taches de Code :**

```
Rouge -> Vert -> Verifier -> Refactorer -> Marquer Complet
```

**Implementation Directe pour Non-Testables :**

- Fichiers de documentation
- Fichiers de configuration
- Ressources statiques
- Fichiers d'infrastructure

**Exemple :**

```text
Vous : /codexspec:implement-tasks

AI  : Demarrage de l'implementation...

     Chargement du contexte :
     - spec.md +
     - plan.md +
     - tasks.md +
     - constitution.md +

     Pile Tech : Python 3.11+ / FastAPI / PostgreSQL / pytest

     Travail sur la Tache 1.1 : Configuration de la Structure du Projet
     + Cree src/taskman/__init__.py
     + Cree pyproject.toml
     [x] Tache 1.1 Complete

     Travail sur la Tache 2.1 : Ecrire les Tests pour l'Entite Tache [P]
     + Cree tests/test_task.py
     Execution des tests... 5 passes (tous echecs attendus)
     [x] Tache 2.1 Complete

     Travail sur la Tache 2.2 : Implementer l'Entite Tache
     + Cree src/taskman/models/task.py
     Execution des tests... 5 passes
     [x] Tache 2.2 Complete

     ...
```

**Conseils :**

- Peut reprendre la ou il s'est arrete si interrompu
- Les bloqueurs sont enregistres dans issues.md
- Les commits sont faits apres des taches/phases significatives
- Executer `/codexspec:review-tasks` d'abord pour validation

---

### `/codexspec:review-spec`

Valider la specification pour completude, clarte, coherence et pretitude a la planification technique.

**Syntaxe :**

```
/codexspec:review-spec [chemin_vers_spec.md]
```

**Arguments :**

| Argument | Requis | Description |
|----------|--------|-------------|
| `chemin_vers_spec.md` | Non | Chemin vers le fichier spec (auto-detecte si non fourni) |

**Ce qu'il fait :**

- Verifie la completude de toutes les sections requises
- Evalue la clarte et la specificite
- Verifie la coherence interne
- Evalue la testabilite des exigences
- Verifie l'alignement avec la constitution
- Genere un rapport de revue note

**Dimensions de Revue :**

| Dimension | Poids | Ce qu'elle Valide |
|-----------|-------|-------------------|
| Completude | 25% | Toutes sections presentes et substantives |
| Clarte | 25% | Pas de langage vague, interpretations uniques |
| Coherence | 20% | Pas de contradictions internes |
| Testabilite | 20% | Les exigences peuvent etre verifiees |
| Alignement Constitution | 10% | Aligne avec les principes du projet |

**Exemple :**

```text
Vous : /codexspec:review-spec

AI  : Revision de la specification...

     # Rapport de Revision de Specification

     ## Resume
     - **Statut Global** : ! Necessite du Travail
     - **Score de Qualite** : 72/100
     - **Pretitude** : Necessite une Revision

     ## Analyse des Sections
     | Section | Statut | Completude | Qualite |
     |---------|--------|------------|---------|
     | Apercu | + | 100% | Haute |
     | Objectifs | + | 100% | Haute |
     | Recits Utilisateur | ! | 80% | Moyenne |
     | Exigences Fonctionnelles | + | 100% | Haute |
     | Exigences Non-Fonctionnelles | ! | 50% | Moyenne |
     | Cas Limites | - | 0% | N/A |

     ## Problemes Critiques (A Corriger)
     - [SPEC-001] : La section Cas Limites est vide
       - Impact : Peut manquer des scenarios d'echec importants
       - Suggestion : Documenter au moins 3-5 cas limites

     ## Avertissements (Devraient Corriger)
     - [SPEC-002] : NFR-001 utilise le terme vague "rapide"
       - Impact : Impossible a verifier sans metriques
       - Suggestion : Specifier un temps de reponse concret

     ## Recommandations
     1. Ajouter une section Cas Limites avec approches de gestion
     2. Quantifier les exigences non-fonctionnelles
     3. Ajouter des criteres d'acceptation au Recit Utilisateur 3

     Suivi disponible :
     - /codexspec:clarify - pour adresser les ambiguites
     - /codexspec:spec-to-plan - si les problemes sont resolus
```

**Conseils :**

- Executer avant `/codexspec:spec-to-plan`
- Adresser les problemes Critiques avant de poursuivre
- Les Avertissements ne bloquent pas mais indiquent un risque
- Re-executer apres avoir fait des corrections

---

### `/codexspec:review-plan`

Reverifier le plan d'implementation technique pour faisabilite, qualite d'architecture et alignement avec la specification.

**Syntaxe :**

```
/codexspec:review-plan [chemin_vers_plan.md]
```

**Arguments :**

| Argument | Requis | Description |
|----------|--------|-------------|
| `chemin_vers_plan.md` | Non | Chemin vers le fichier plan (auto-detecte si non fourni) |

**Ce qu'il fait :**

- Verifie que les exigences du spec ont une couverture dans le plan
- Evalue les choix de pile technologique
- Evalue les decisions d'architecture
- Valide les phases d'implementation
- Verifie l'alignement avec la constitution
- Genere un rapport de revue note

**Dimensions de Revue :**

| Dimension | Poids | Ce qu'elle Valide |
|-----------|-------|-------------------|
| Alignement Spec | 30% | Toutes les exigences ont une implementation |
| Pile Technologique | 15% | Choix de technologies appropriees |
| Qualite Architecture | 25% | Conception et patterns sains |
| Planification Phases | 15% | Phases logiques et realistes |
| Alignement Constitution | 15% | Suit les principes du projet |

**Exemple :**

```text
Vous : /codexspec:review-plan

AI  : Revision du plan technique...

     # Rapport de Revision de Plan

     ## Resume
     - **Statut Global** : + Reussite
     - **Score de Qualite** : 85/100
     - **Pretitude** : Pret pour la Decomposition en Taches

     ## Alignement Spec
     | Exigence | Couverture | Statut |
     |----------|------------|--------|
     | REQ-001 a REQ-012 | + Complete | Toutes couvertes |
     | US-001 a US-004 | + Complete | Toutes couvertes |
     | NFR-001 a NFR-003 | ! Partielle | Cache non detaille |

     ## Revue d'Architecture
     Forces :
     - Separation claire des preoccupations
     - Limites de modules bien definies
     - Patterns de conception appropriees

     Preoccupations :
     - Documentation manquante de la strategie de gestion d'erreurs

     ## Alignement Constitution
     | Principe | Conformite |
     |----------|------------|
     | Architecture Propre | + |
     | TDD | + |
     | Qualite du Code | + |

     Pret pour /codexspec:plan-to-tasks
```

**Conseils :**

- Executer avant `/codexspec:plan-to-tasks`
- Les problemes critiques devraient etre resolus
- Utiliser pour detecter les problemes d'architecture tot
- Verifier que la pile tech s'aligne avec les competences de l'equipe

---

### `/codexspec:review-tasks`

Valider la decomposition des taches pour completude, conformite TDD, ordonnancement correct et dependances appropriees.

**Syntaxe :**

```
/codexspec:review-tasks [chemin_vers_tasks.md]
```

**Arguments :**

| Argument | Requis | Description |
|----------|--------|-------------|
| `chemin_vers_tasks.md` | Non | Chemin vers le fichier tasks (auto-detecte si non fourni) |

**Ce qu'il fait :**

- Verifie que tous les elements du plan ont une couverture de tache
- Valide la conformite TDD (tests avant implementation)
- Verifie la granularite des taches (atomiques, focus sur fichier unique)
- Valide les dependances (pas de cycles, ordonnancement correct)
- Reveut les marqueurs de parallelisation
- Valide les chemins de fichiers

**Dimensions de Revue :**

| Dimension | Poids | Ce qu'elle Valide |
|-----------|-------|-------------------|
| Couverture Plan | 30% | Tous les elements du plan ont des taches |
| Conformite TDD | 25% | Workflow test-first applique |
| Dependances et Ordonnancement | 20% | Dependances correctes, pas de cycles |
| Granularite Taches | 15% | Atomiques, portee appropriee |
| Parallelisation et Fichiers | 10% | Marqueurs et chemins corrects |

**Exemple :**

```text
Vous : /codexspec:review-tasks

AI  : Revision de la decomposition des taches...

     # Rapport de Revision des Taches

     ## Resume
     - **Statut Global** : ! Necessite du Travail
     - **Score de Qualite** : 78/100
     - **Total Taches** : 24
     - **Parallelisables** : 8 (33%)

     ## Conformite TDD
     | Composant | Tache Test | Test Avant Impl | Statut |
     |-----------|------------|-----------------|--------|
     | Entite Tache | + | + | + |
     | Entite Utilisateur | + | + | + |
     | TaskService | - Manquant | N/A | - |

     ## Violations TDD
     - [TDD-001] : TaskService manque une tache de test

     ## Problemes de Dependances
     - [DEP-001] : Tache 2.5 marquee [P] mais depend de 2.4

     ## Recommandations
     1. Ajouter une tache de test pour TaskService avant l'implementation
     2. Corriger le marqueur de parallelisation sur la Tache 2.5

     Corriger les problemes avant /codexspec:implement-tasks
```

**Conseils :**

- Executer avant `/codexspec:implement-tasks`
- Les violations TDD sont critiques pour la qualite du code
- Verifier que les marqueurs de parallelisation sont exacts
- Verifier que les chemins de fichiers correspondent a la structure du projet

---

### `/codexspec:analyze`

Effectuer une analyse de coherence croisee non destructive des artefacts a travers spec.md, plan.md et tasks.md. Identifie les incoherences, duplications et lacunes de couverture.

**Syntaxe :**

```
/codexspec:analyze
```

**Arguments :**

| Argument | Requis | Description |
|----------|--------|-------------|
| Aucun | - | Analyse les artefacts de la fonctionnalite courante |

**Ce qu'il fait :**

- Detecte les duplications a travers les artefacts
- Identifie les ambiguites manquant de criteres mesurables
- Trouve les elements sous-specifies
- Verifie l'alignement avec la constitution
- Mappe la couverture des exigences aux taches
- Rapporte les incoherences dans la terminologie et l'ordonnancement

**Niveaux de Severite :**

| Niveau | Definition |
|--------|------------|
| **CRITIQUE** | Violation de constitution, artefact core manquant, couverture nulle |
| **ELEVEE** | Exigence dupliquee/conflictuelle, attribut de securite ambigu |
| **MOYENNE** | Derive de terminologie, couverture non-fonctionnelle manquante |
| **FAIBLE** | Ameliorations de style/formulation |

**Exemple :**

```text
Vous : /codexspec:analyze

AI  : Analyse des artefacts...

     # Rapport d'Analyse de Specification

     ## Resume de Couverture
     | Cle Exigence | A une Tache ? | IDs Taches |
     |--------------|---------------|------------|
     | REQ-001 | + | 2.1, 2.2 |
     | REQ-002 | + | 2.3, 2.4 |
     | REQ-003 | - | Aucun |

     ## Problemes Trouves

     | ID | Categorie | Severite | Resume |
     |----|-----------|----------|--------|
     | A1 | Couverture | CRITIQUE | REQ-003 n'a pas de couverture de tache |
     | A2 | Duplication | ELEVEE | REQ-005 et REQ-008 se chevauchent |
     | A3 | Ambiguite | MOYENNE | NFR-002 "securise" non defini |

     ## Metriques
     - Total Exigences : 12
     - Total Taches : 24
     - Couverture : 92% (11/12 exigences)
     - Problemes Critiques : 1

     ## Prochaines Actions
     1. Ajouter des taches pour REQ-003 (CRITIQUE)
     2. Considerer la fusion de REQ-005 et REQ-008
     3. Definir "securise" dans NFR-002

     Resoudre les problemes CRITIQUES avant /codexspec:implement-tasks
```

**Conseils :**

- Executer apres `/codexspec:plan-to-tasks`, avant l'implementation
- Les problemes CRITIQUES devraient bloquer l'implementation
- Analyse en lecture seule - aucun fichier n'est modifie
- Utiliser les resultats pour ameliorer la qualite des artefacts

---

### `/codexspec:checklist`

Generer des listes de controle de qualite pour valider la completude, clarte et coherence des exigences. Ce sont des "tests unitaires pour l'ecriture d'exigences".

**Syntaxe :**

```
/codexspec:checklist [domaine_focus]
```

**Arguments :**

| Argument | Requis | Description |
|----------|--------|-------------|
| `domaine_focus` | Non | Focus domaine (ex. "ux", "api", "securite", "performance") |

**Ce qu'il fait :**

- Genere des listes de controle organisees par dimensions de qualite
- Cree des listes de controle dans le repertoire `FEATURE_DIR/checklists/`
- Les elements se concentrent sur la qualite des exigences, pas les tests d'implementation

**Dimensions de Qualite :**

- **Completude des Exigences** : Toutes les exigences necessaires sont-elles presentes ?
- **Clarte des Exigences** : Les exigences sont-elles specifiques et non ambigues ?
- **Coherence des Exigences** : Les exigences s'alignent-elles sans conflits ?
- **Qualite des Criteres d'Acceptation** : Les criteres de succes sont-ils mesurables ?
- **Couverture des Scenarios** : Tous les flux/cas sont-ils adresses ?
- **Couverture des Cas Limites** : Les conditions aux limites sont-elles definies ?
- **Exigences Non-Fonctionnelles** : Performance, Securite, Accessibilite specifiees ?
- **Dependances et Hypotheses** : Sont-elles documentees ?

**Exemples de Types de Listes de Controle :**

- `ux.md` - Hierarchie visuelle, etats d'interaction, accessibilite
- `api.md` - Formats d'erreur, limitation de debit, authentification
- `security.md` - Protection des donnees, modele de menace, reponse aux violations
- `performance.md` - Metriques, conditions de charge, degradation

**Exemple :**

```text
Vous : /codexspec:checklist securite

AI  : Generation de la liste de controle securite...

     + Cree .codexspec/specs/001-task-management/checklists/security.md

     ## Liste de Controle de Qualite des Exigences de Securite

     ### Exigences d'Authentification
     - [ ] CHK001 - Les exigences d'authentification sont-elles definies pour tous les points de terminaison proteges ? [Completude]
     - [ ] CHK002 - La complexite du mot de passe est-elle explicitement specifiee ? [Clarte]
     - [ ] CHK003 - Les exigences de delai d'expiration de session sont-elles quantifiees ? [Mesurabilite]

     ### Protection des Donnees
     - [ ] CHK004 - Les exigences de chiffrement des donnees au repos sont-elles specifiees ? [Completude]
     - [ ] CHK005 - Les exigences de chiffrement des donnees en transit sont-elles specifiees ? [Completude]
     - [ ] CHK006 - La gestion des PII est-elle explicitement documentee ? [Clarte]

     Total : 15 elements a travers 4 categories
```

**Conseils :**

- Les listes de controle valident la qualite des exigences, pas l'exactitude de l'implementation
- Utiliser pour la revue et l'amelioration des exigences
- Creer des listes de controle specifiques au domaine pour une validation ciblee
- Executer avant de passer a la planification technique

---

### `/codexspec:tasks-to-issues`

Convertir les taches de `tasks.md` en issues GitHub pour le suivi de projet et la collaboration.

**Syntaxe :**

```
/codexspec:tasks-to-issues
```

**Arguments :**

| Argument | Requis | Description |
|----------|--------|-------------|
| Aucun | - | Convertit toutes les taches de la fonctionnalite courante |

**Ce qu'il fait :**

- Analyse les IDs de tache, descriptions, dependances et chemins de fichiers
- Cree des issues GitHub avec un corps structure
- Ajoute des labels bases sur le type de tache (setup, implementation, testing, documentation)
- Lie les dependances entre les issues
- Rapporte les issues creees avec leurs URLs

**Prerequis :**

- Depot Git avec remote GitHub
- GitHub CLI (`gh`) installe et authentifie
- Fichier `tasks.md` existant

**Exemple :**

```text
Vous : /codexspec:tasks-to-issues

AI  : Conversion des taches en issues GitHub...

     Depot : github.com/example/taskman

     Creation des issues :
     + #42 : Tache 1.1 - Configuration de la Structure du Projet (setup)
     + #43 : Tache 2.1 - Ecrire les Tests pour l'Entite Tache (testing)
     + #44 : Tache 2.2 - Implementer l'Entite Tache (implementation)
     ...

     Resume :
     - Issues creees : 24
     - Labels appliques : setup(4), implementation(12), testing(5), documentation(3)
     - Dependances liees : 18

     Voir les issues : https://github.com/example/taskman/issues
```

**Conseils :**

- Necessite une authentification GitHub CLI (`gh auth login`)
- Fonctionne uniquement avec les depots GitHub
- Cree des issues dans la configuration par defaut du depot
- Verifier les doublons avant d'executer

---

### `/codexspec:commit-staged`

Generer un message de commit conforme a Conventional Commits base sur les changements git stages, avec conscience du contexte de session. Cette commande comprend votre session de developpement pour generer des messages de commit significatifs.

**Syntaxe :**

```
/codexspec:commit-staged [-p]
```

**Arguments :**

| Argument | Requis | Description |
|----------|--------|-------------|
| `-p` | Non | Mode apercu - afficher le message sans commiter |

**Ce qu'il fait :**

- Execute `git diff --staged` pour recuperer les changements stages
- Analyse les changements et le contexte de session pour comprendre l'intention
- Suit la specification Conventional Commits
- Mode execution (par defaut) : commite directement apres avoir genere le message
- Mode apercu (`-p`) : affiche le message sans commiter
- Rapporte une erreur si aucun changement stage n'existe

**Exemple :**

```text
Vous : /codexspec:commit-staged

AI  : Analyse des changements stages...

     Fichiers stages :
     - src/auth/service.py
     - tests/test_auth.py

     Message de commit genere :
     feat(auth): implementer la logique de rafraichissement des tokens

     - Ajouter la generation de token de rafraichissement
     - Inclure la gestion de l'expiration des tokens
     - Ajouter des tests pour le flux de rafraichissement

     Execution du commit...

     + Commit : def5678
```

**Exemple de Mode Apercu :**

```text
Vous : /codexspec:commit-staged -p

AI  : Mode apercu - aucun commit ne sera execute

     Message de commit suggere :
     feat(auth): implementer la logique de rafraichissement des tokens

     - Ajouter la generation de token de rafraichissement
     - Inclure la gestion de l'expiration des tokens
     - Ajouter des tests pour le flux de rafraichissement
```

**Conseils :**

- Stager les changements d'abord avec `git add`
- Analyse uniquement le contenu stage - respectant le flux de commit en deux etapes de Git
- Considere le contexte de session pour des messages de commit significatifs
- Utilisez le flag `-p` pour previsualiser avant de commiter
- Suit la specification Conventional Commits par defaut

---

## Apercu du Workflow

```
+--------------------------------------------------------------------------+
|                    Workflow de Collaboration Humain-AI CodexSpec          |
+--------------------------------------------------------------------------+
|                                                                           |
|  1. Constitution  -->  Definir les principes du projet                    |
|         |                         avec validation croisee des artefacts   |
|         v                                                                 |
|  2. Specify  --------->  Q&R interactives pour clarifier les exigences    |
|         |                (aucun fichier cree - controle humain)            |
|         v                                                                 |
|  3. Generate Spec  -->  Creer le document spec.md                         |
|         |                                                                 |
|         v                                                                 |
|  +====================================================================+   |
|  |  ★ PORTE DE REVISION 1 : /codexspec:review-spec ★                   |   |
|  |  Valider : Completude, Clarte, Testabilite, Constitution            |   |
|  +====================================================================+   |
|         |                                                                 |
|         v                                                                 |
|  4. Clarify  --------->  Resoudre les ambiguites (iteratif)               |
|         |                4 categories ciblees, max 5 questions            |
|         v                                                                 |
|  5. Spec to Plan  -->  Creer le plan technique avec :                     |
|         |                * Revue de constitutionnalite (OBLIGATOIRE)      |
|         |                * Graphe de dependance des modules               |
|         v                                                                 |
|  +====================================================================+   |
|  |  ★ PORTE DE REVISION 2 : /codexspec:review-plan ★                   |   |
|  |  Valider : Alignement Spec, Architecture, Pile Tech, Phases          |   |
|  +====================================================================+   |
|         |                                                                 |
|         v                                                                 |
|  6. Plan to Tasks  -->  Generer des taches atomiques avec :               |
|         |                * Application TDD (tests avant impl)             |
|         |                * Marqueurs paralleles [P]                       |
|         |                * Specifications des chemins de fichiers         |
|         v                                                                 |
|  +====================================================================+   |
|  |  ★ PORTE DE REVISION 3 : /codexspec:review-tasks ★                  |   |
|  |  Valider : Couverture, Conformite TDD, Dependances, Granularite     |   |
|  +====================================================================+   |
|         |                                                                 |
|         v                                                                 |
|  7. Analyze  --------->  Verification de coherence croisee des artefacts  |
|         |                Detecter lacunes, duplications, problemes const. |
|         v                                                                 |
|  8. Implement  -------->  Executer avec le workflow TDD conditionnel      |
|                          Code : Test-first | Docs/Config : Direct          |
|                                                                           |
+--------------------------------------------------------------------------+
```

**Point Cle** : Chaque porte de revision (*) est un **point de controle humain** ou vous validez la sortie de l'AI avant d'investir plus de temps. Sauter ces portes mene souvent a un retravail couteux.

---

## Resolution de Problemes

### "Repertoire de fonctionnalite non trouve"

La commande n'a pas pu localiser le repertoire de fonctionnalite.

**Solutions :**

- Executer `codexspec init` d'abord pour initialiser le projet
- Verifier que le repertoire `.codexspec/specs/` existe
- Verifier que vous etes dans le bon repertoire de projet

### "Aucun spec.md trouve"

Le fichier de specification n'existe pas encore.

**Solutions :**

- Executer `/codexspec:specify` pour clarifier les exigences d'abord
- Puis executer `/codexspec:generate-spec` pour creer spec.md

### "Constitution non trouvee"

Aucune constitution de projet n'existe.

**Solutions :**

- Executer `/codexspec:constitution` pour en creer une
- La constitution est optionnelle mais recommandee pour des decisions coherentes

### "Fichier de taches non trouve"

La decomposition des taches n'existe pas.

**Solutions :**

- S'assurer d'avoir execute `/codexspec:spec-to-plan` d'abord
- Puis executer `/codexspec:plan-to-tasks` pour creer tasks.md

### "GitHub CLI non authentifie"

La commande `/codexspec:tasks-to-issues` necessite une authentification GitHub.

**Solutions :**

- Installer GitHub CLI : `brew install gh` (macOS) ou equivalent
- S'authentifier : `gh auth login`
- Verifier : `gh auth status`

---

## Prochaines Etapes

- [Workflow](workflow.md) - Patterns courants et quand utiliser chaque commande
- [CLI](../reference/cli.md) - Commandes terminal pour l'initialisation de projet

# Etude de Cas CodexSpec : Ajout d'une Fonctionnalite de Generation de Descriptions PR au Projet

> Ce document enregistre le processus complet d'utilisation de la chaine d'outils CodexSpec pour ajouter une nouvelle fonctionnalite au projet CodexSpec lui-meme, demontrant l'application pratique du Developpement Pilote par les Specifications (SDD).

## Apercu

**Fonctionnalite Cible** : Ajouter une commande `/codexspec:pr` pour generer des descriptions de PR GitHub / MR GitLab structurees.

**Flux de Developpement** : `specify -> generate-spec -> review-spec -> clarify -> spec-to-plan`

**Caracteristique Cle** : Decouverte de problemes d'exigences pendant le developpement et ajustement via la commande `clarify`, demontrant la flexibilite du SDD.

---

## Etape 1 : Clarification des Exigences Initiales (`/codexspec:specify`)

### Entree Initiale de l'Utilisateur

```
Je souhaite ajouter une fonctionnalite au projet : fournir une nouvelle instruction liee a Git pour generer des informations de PR GitHub precises, detaillees et conformes aux normes (ou informations MR, pour GitLab). Voici le contenu de deux instructions PR que j'ai utilisees dans d'autres projets, fournies pour reference.

[Exemple de reference 1 - Description structuree]
Maintenant, jouez le role de mainteneur du projet, et base sur tout notre travail jusqu'a present, redigez une description claire de Pull Request pour cette soumission.
La description de la PR doit etre orientee vers les autres relecteurs de l'equipe et inclure les sections suivantes :
1. Contexte (Context)
2. Schema d'implementation (Implementation)
3. Tests (Testing)
4. Comment verifier manuellement (How to Verify)

[Exemple de reference 2 - Description simple]
Veuillez baser sur la difference de code entre la branche actuelle et la branche origin/main, et utiliser le format Markdown pour organiser un titre et une description de Merge Request conformes aux normes Git. (Utiliser la description en chinois)
```

### Processus de Clarification

**Q1 : Langue de sortie**

- Options : Suivre la configuration du projet / Chinois / Detection automatique
- **Choix de l'utilisateur** : Suivre la configuration du projet (actuel : en)

**Q2 : Support de plateforme**

- Options : Supporter GitHub et GitLab simultanement / GitHub uniquement / Detection automatique de plateforme
- **Choix de l'utilisateur** : Detection automatique de plateforme

**Q3 : Contenu de description PR**

- Options : Description structuree detaillee / Description concise / Modele personnalisable
- **Choix de l'utilisateur** : Description structuree detaillee (recommande)

**Q4 : Condition de declenchement**

- Options : Branche courante vs origin/main / Commits non pousses / Specification possible de la branche cible
- **Choix de l'utilisateur** : Specification possible de la branche cible

**Q5 : Source Spec**

- Options : Prioriser spec.md / Uniquement informations git / Combiner toutes les sources
- **Choix de l'utilisateur** : Combiner toutes les sources (recommande)

**Q6 : Nom**

- Options : codexspec.pr / codexspec.create-pr / codexspec.create-mr
- **Choix de l'utilisateur** : codexspec.pr (recommande)

**Q7 : Gestion sans Spec**

- Options : Continuer la generation, sauter le contexte / Prompter l'utilisateur a creer d'abord un spec / Avertir et continuer
- **Choix de l'utilisateur** : Continuer la generation, sauter le contexte

**Q8 : Mode de sortie**

- Options : Sortie terminal / Sauvegarder dans fichier / Terminal + fichier optionnel
- **Choix de l'utilisateur** : Terminal + fichier optionnel (recommande)

**Q9 : Sections par defaut**

- Options : Contexte, Schema d'implementation, Tests, Comment verifier (tout selectionner)
- **Choix de l'utilisateur** : Les quatre sections

**Q10 : Parametres d'instruction**

- **Choix de l'utilisateur** : Tous les parametres sont optionnels
  - `--target-branch` : Defaut origin/main
  - `--output` : Defaut sortie terminal uniquement si non specifie
  - `--sections` : Defaut si non specifie
  - `--no-spec` : Sauter la recherche de fichier spec.md

### Correction de Configuration de Langue

**Retour utilisateur** : La langue devrait suivre la meme priorite que l'instruction `/commit` selon le parametre `language.commit` dans `config.yml`, et seulement si `language.commit` n'est pas defini, alors selon `language.output`.

**Resume des exigences mis a jour** :

```
Priorite de langue : language.commit > language.output > English (defaut)
```

---

## Etape 2 : Generation du Document de Specification (`/codexspec:generate-spec`)

### Structure du Document Genere

Le `spec.md` genere contient les sections suivantes :

- **Overview** : Apercu de la fonctionnalite
- **Goals** : 4 objectifs
- **User Stories** : 4 recits utilisateur avec criteres d'acceptation
- **Functional Requirements** : 8 exigences (REQ-001 a REQ-008)
- **Command Parameters** : 4 definitions de parametres
- **Non-Functional Requirements** : 3 exigences (performance, compatibilite, gestion d'erreurs)
- **Acceptance Criteria (Test Cases)** : 10 cas de test
- **Edge Cases** : 6 cas limites
- **Output Format Example** : Exemples PR GitHub et MR GitLab
- **Out of Scope** : Fonctionnalites explicitement exclues
- **Dependencies** : Dependances
- **Related Commands** : Commandes connexes

### Extrait des Exigences Cles

```markdown
### REQ-003 : Configuration de Langue
La commande doit determiner la langue de sortie dans l'ordre de priorite suivant :
1. `language.commit` dans `.codexspec/config.yml` (plus haute priorite)
2. `language.output` dans `.codexspec/config.yml` (fallback)
3. English (defaut si aucune configuration)
```

---

## Etape 3 : Revision de Specification (`/codexspec:review-spec`)

### Resultats de Revision

- **Statut Global** : + Reussite
- **Score de Qualite** : 92/100
- **Etat de Pretitude** : Ready for Planning

### Problemes Detectes

**Avertissements (Should Fix)** :

1. **SPEC-001** : Logique de decouverte de fichiers de test non explicitement specifiee
2. **SPEC-002** : Selection du spec.md "le plus recemment modifie" peut etre inexact quand il y en a plusieurs

**Suggestions (Nice to Have)** :

1. Considerer l'ajout d'un parametre `--title`
2. Ajouter une exigence de validation de format de sortie
3. Considerer le support des modeles d'URL GitHub Enterprise

### Emplacement de Sauvegarde du Rapport de Revision

`.codexspec/specs/001-pr-description-generator/review-spec.md`

---

## Etape 4 : Clarification et Ajustement des Exigences (`/codexspec:clarify`) : AVERTISSEMENT - Tournant Critique

### Probleme Detecte

**Retour utilisateur** :
> J'ai realise qu'il y a un probleme concernant l'utilisation de spec.md. Par exemple, l'utilisateur fait en fait une tres petite modification, donc n'a pas utilise le flux standardise codexspec specify->plan->tasks->implement, mais a directement effectue des modifications via dialogue ou le mode plan integre de claude code, puis apres avoir termine les modifications, souhaite appeler separement la commande codexspec pour generer des informations de pr conformes. Dans ce cas, utiliser directement le spec.md modifie le plus recemment pourrait utiliser le contenu d'un spec.md precedent non lie a cette modification.

### Processus de Q&R de Clarification

**Q1 : Strategie de Selection Spec**

**Contexte** : L'actuel EC-004 stipule "plusieurs spec.md -> utiliser le plus recemment modifie". Mais quand l'utilisateur fait des petites modifications, il peut ne pas avoir utilise le flux SDD, et le spec.md le plus recent peut ne pas etre lie a la modification courante.

| Option | Description |
|--------|-------------|
| A | Ne pas utiliser spec.md par defaut, sauf si l'utilisateur specifie explicitement le parametre `--spec` |
| B | Correspondance basee sur le nom de branche |
| C | Prompter l'utilisateur a choisir |
| D | Correspondance basee sur les changements de fichiers |

**Choix de l'utilisateur** : Option A
**Raison** : Eviter les references erronees, le parametre `--spec` permet aux utilisateurs ayant besoin de l'integration SDD de specifier explicitement.

---

**Q2 : Strategie d'Extraction de Contenu Spec**

**Contexte** : Quand l'utilisateur utilise `--spec`, que faire si la structure de spec.md est incomplete ?

| Option | Description |
|--------|-------------|
| A | Extraire au mieux, sauter les parties manquantes |
| B | Avertir et sauter le Contexte |
| C | Exiger une structure complete, sinon erreur |

**Choix de l'utilisateur** : Option A
**Raison** : Eviter de bloquer le workflow a cause de problemes de format spec.

---

**Q3 : Decouverte de Fichiers de Test**

**Contexte** : Comment decouvrir les fichiers de test pour la section Testing ?

| Option | Description |
|--------|-------------|
| A | Modeles de repertoires courants (tests/, test/) |
| B | Heuristiques independantes du langage (repertoire + modeles de noms de fichiers) |
| C | Pas de decouverte active, uniquement inferer depuis les messages de commit |

**Choix de l'utilisateur** : Option B
**Raison** : Couvrir diverses structures de projet dans differentes langues.

---

**Q4 : Generation de Titre PR**

**Contexte** : Comment le titre PR devrait-il etre genere ?

| Option | Description |
|--------|-------------|
| A | Priorite au parsage de nom de branche |
| B | Priorite au premier message de commit |
| C | Generation combinee (git diff + nom de branche + messages de commit) |

**Choix de l'utilisateur** : Option C
**Raison utilisateur** : Le premier commit peut n'etre qu'une petite partie des modifications; le nom de branche exige des normes de nommage strictes. Puisqu'il y a beaucoup d'informations git et changements de code de reference, l'analyse combinee est plus precise.

---

**Q5 : Generation de Commandes de Verification**

**Contexte** : Comment generer les commandes de verification pour la section "How to Verify" ?

| Option | Description |
|--------|-------------|
| A | Modele generique |
| B | Detection de projet (pyproject.toml -> pytest, package.json -> npm test) |
| C | Inferer depuis les messages de commit |

**Choix de l'utilisateur** : Option B
**Raison** : La detection de projet peut generer des commandes de verification plus utiles.

---

### Resume de la Session de Clarification

| Question | Decision | Impact |
|----------|----------|--------|
| Strategie de Selection Spec | Opt-in via `--spec` | REQ-007, EC-004, Table des parametres |
| Extraction de Contenu Spec | Extraction au mieux | REQ-005b, EC-004c |
| Decouverte de Fichiers de Test | Heuristiques independantes du langage | REQ-006b |
| Generation de Titre PR | Analyse combinee | REQ-008a |
| Generation de Commandes de Verification | Detection de fichiers projet | REQ-010 |

### Changement Cle : Inversion de la Logique de Parametres

```
Conception originale : --no-spec (sauter spec)
Nouvelle conception : --spec (activer spec, opt-in)
```

---

## Etape 5 : Plan d'Implementation Technique (`/codexspec:spec-to-plan`)

### Apercu du Plan

**Methode d'implementation** : Fichier modele Markdown (conforme a `/codexspec:commit`)

**Aucune nouvelle dependance** - La fonctionnalite est implementee via le modele de commande slash, ne necessite pas de code Python.

### Resume des Decisions Techniques

| Decision | Choix | Raison |
|----------|-------|--------|
| Methode d'implementation | Modele Markdown | Conforme aux commandes existantes, facile a maintenir |
| Priorite de langue | commit > output > en | Conforme a la commande `/commit` |
| Detection de plateforme | Parsing d'URL remote | Simple et fiable |
| Integration Spec | Opt-in (`--spec`) | Eviter les references erronees |
| Extraction de contenu | Au mieux | Ne pas bloquer le workflow |
| Decouverte de tests | Modeles repertoire + nom de fichier | Independant du langage |
| Generation de titre | Analyse combinee | Plus precise |
| Detection de commandes | Detection de fichiers projet | Plus utile |
| Mode de sortie | Terminal priorite, fichier optionnel | Flexible |

### Phases d'Implementation

1. **Phase 1** : Creation de modele (YAML frontmatter, configuration de langue, contexte Git)
2. **Phase 2** : Fonctionnalite core (Integration Spec, decouverte de tests, detection de commandes, generation de titre)
3. **Phase 3** : Gestion des cas limites
4. **Phase 4** : Tests
5. **Phase 5** : Mise a jour de la documentation

### Liste des Fichiers

**Crees** :

- `templates/commands/pr.md`

**Modifies** :

- `CLAUDE.md` - Ajouter la description de commande
- `README.md` - Ajouter la commande a la liste

**Tests** :

- `tests/test_pr_template.py`

---

## Diagramme de Flux Complet

```
+-------------------------------------------------------------------------+
|                         Flux de Developpement SDD CodexSpec              |
+-------------------------------------------------------------------------+
                                    |
                                    v
+-------------------------------------------------------------------------+
|  /codexspec:specify                                                      |
|  |-- Clarifier les exigences via Q&R                                    |
|  |-- L'utilisateur a fourni des exemples de reference                   |
|  |-- 10 questions, couvrant langue, plateforme, contenu, parametres     |
+-------------------------------------------------------------------------+
                                    |
                                    v
+-------------------------------------------------------------------------+
|  /codexspec:generate-spec                                                |
|  |-- Generer le spec.md complet                                         |
|  |-- 4 recits utilisateur, 8 exigences fonctionnelles, 10 cas de test   |
|  |-- Sauvegarde dans .codexspec/specs/001-pr-description-generator/spec.md |
+-------------------------------------------------------------------------+
                                    |
                                    v
+-------------------------------------------------------------------------+
|  /codexspec:review-spec                                                  |
|  |-- Score de qualite : 92/100                                          |
|  |-- Detection de 2 avertissements (decouverte fichiers test, multi spec) |
|  |-- Statut : Reussite, peut passer a la phase de planification         |
+-------------------------------------------------------------------------+
                                    |
                                    v
+-------------------------------------------------------------------------+
|  /codexspec:clarify  : AVERTISSEMENT - Ajustement Critique               |
|  |-- L'utilisateur a detecte un probleme de scenario d'usage reel       |
|  |-- 5 questions de clarification, toutes repondues                     |
|  |-- Changement cle : --no-spec -> --spec (opt-in)                      |
|  |-- 5 nouvelles exigences (REQ-005b, 006b, 008a, 010, mise a jour 007) |
+-------------------------------------------------------------------------+
                                    |
                                    v
+-------------------------------------------------------------------------+
|  /codexspec:spec-to-plan                                                 |
|  |-- Mise a jour du plan d'implementation technique                     |
|  |-- 9 decisions techniques, incluant 5 nouvelles decisions             |
|  |-- 5 phases d'implementation                                          |
|  |-- Sauvegarde dans .codexspec/specs/001-pr-description-generator/plan.md |
+-------------------------------------------------------------------------+
                                    |
                                    v
+-------------------------------------------------------------------------+
|  Etapes Suivantes (non completees dans cette session)                   |
|  |-- /codexspec:review-plan - Valider la qualite du plan                |
|  |-- /codexspec:plan-to-tasks - Decomposer en taches executables        |
|  |-- /codexspec:implement-tasks - Executer l'implementation             |
+-------------------------------------------------------------------------+
```

---

## Points d'Apprentissage Cles

### 1. Valeur de la Phase de Clarification

Cette etude de cas demontre le role critique de la commande `clarify` :

- **L'utilisateur a detecte des problemes reels pendant l'utilisation** - Risque d'utilisation erronee de spec.md dans les scenarios de petites modifications
- **Resolution des defauts de conception via Q&R de clarification** - Passage de la detection automatique au mode opt-in
- **Les changements d'exigences sont systematiquement enregistres** - Tous les changements sont sauvegardes dans la section Clarifications de spec.md

### 2. Flexibilite du Flux SDD

- Pas un flux lineaire, peut retourner et ajuster a n'importe quelle etape
- `clarify` peut etre insere apres `review-spec`, avant `spec-to-plan`
- Les documents de specification et plan technique sont mis a jour pour refleter les changements

### 3. Evolution de la Conception des Parametres

```
Conception initiale :
  --no-spec : Sauter spec.md (utilise par defaut)

Conception finale :
  --spec : Activer spec.md (non utilise par defaut)
```

Ce changement reflete le passage de la conception d'un "workflow SDD par defaut" a "support de workflows non-SDD", rendant l'outil plus universel.

### 4. Production de Documents

| Etape | Fichier Produit | Contenu |
|-------|-----------------|---------|
| generate-spec | spec.md | Document de specification complet |
| review-spec | review-spec.md | Rapport de revue de qualite |
| clarify | (mise a jour spec.md) | Enregistrement de clarification + mise a jour des exigences |
| spec-to-plan | plan.md | Plan d'implementation technique |

---

## Annexe : Aide-Memoire des Commandes

```bash
# 1. Clarification des exigences initiales
/codexspec:specify

# 2. Generation du document de specification
/codexspec:generate-spec

# 3. Revision de la qualite de specification
/codexspec:review-spec

# 4. Clarification/ajustement des exigences (optionnel, utiliser apres detection de probleme)
/codexspec:clarify [description du probleme]

# 5. Generation du plan technique
/codexspec:spec-to-plan

# 6. Revision de la qualite du plan (optionnel)
/codexspec:review-plan

# 7. Decomposition en taches
/codexspec:plan-to-tasks

# 8. Execution de l'implementation
/codexspec:implement-tasks
```

---

*Ce document a ete genere automatiquement par le workflow SDD CodexSpec, enregistrant le processus de dialogue de developpement reel.*

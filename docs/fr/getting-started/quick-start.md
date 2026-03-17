# Demarrage Rapide

## 1. Initialiser un Projet

Apres l'installation, creez ou initialisez votre projet :

```bash
# Creer un nouveau projet
codexspec init mon-super-projet

# Ou initialiser dans le repertoire courant
codexspec init . --ai claude

# Avec sortie en chinois
codexspec init mon-projet --lang zh-CN
```

## 2. Etablir les Principes du Projet

Lancez Claude Code dans le repertoire du projet :

```bash
cd mon-super-projet
claude
```

Utilisez la commande constitution :

```
/codexspec:constitution Creer des principes axes sur la qualite du code et les tests
```

## 3. Clarifier les Exigences

Utilisez `/codexspec:specify` pour explorer les exigences :

```
/codexspec:specify Je veux construire une application de gestion de taches
```

## 4. Generer la Specification

Une fois clarifie, genere le document de specification :

```
/codexspec:generate-spec
```

## 5. Valider et Reverifier

**Recommande :** Validez avant de poursuivre :

```
/codexspec:review-spec
```

## 6. Creer le Plan Technique

```
/codexspec:spec-to-plan Utiliser Python FastAPI pour le backend
```

## 7. Generer les Taches

```
/codexspec:plan-to-tasks
```

## 8. Implementer

```
/codexspec:implement-tasks
```

## Structure du Projet

Apres l'initialisation :

```
mon-projet/
+-- .codexspec/
|   +-- memory/
|   |   +-- constitution.md
|   +-- specs/
|   |   +-- {identifiant-fonctionnalite}/
|   |       +-- spec.md
|   |       +-- plan.md
|   |       +-- tasks.md
|   +-- scripts/
+-- .claude/
|   +-- commands/
+-- CLAUDE.md
```

## Prochaines Etapes

[Guide Complet du Workflow](../user-guide/workflow.md)

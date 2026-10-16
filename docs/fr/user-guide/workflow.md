# Flux de travail

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

<a id="shared-blueprint-and-autonomous-development"></a>

## Blueprint partagé et développement autonome

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

<a id="worktree-development"></a>

## Développement avec les worktrees

Un worktree Git est un autre dossier de travail du même dépôt, avec sa propre
branche active. Par défaut, CodexSpec en utilise un par fonctionnalité du flux
standard. Il le crée avant d'écrire la première exigence et y regroupe les
documents, l'implémentation, les tests et les corrections de cette fonctionnalité.

```text
projects/
├── my-project/
└── my-project-codexspec-worktrees/
    ├── <feature-id>-task-reminders/
    ├── <feature-id>-search/
    ├── worktree-for-codexspec-maintenance/
    └── worktree-for-codexspec-auto-dev/
```

Lorsque vous reprenez une fonctionnalité, son espace de travail est réutilisé.
Les modifications indépendantes de configuration, de constitution ou de profil
s'effectuent dans le worktree de maintenance ; celles d'une fonctionnalité
active restent dans son worktree. La configuration est **locale à chaque
checkout** : un paramètre modifié dans le worktree vers lequel l'opération est
dirigée y prend effet d'abord, puis se propage aux autres checkouts par
intégration Git. Exécutez les commandes de la CLI et les vérifications dans
l'espace de travail indiqué.

Pour établir la base d'une nouvelle fonctionnalité, CodexSpec compare
l'historique des commits de la branche principale locale à celui de la branche
principale distante récupéré par fetch, selon leurs liens d'ascendance Git.
Si les historiques ont divergé, ils sont fusionnés dans le nouveau worktree
et la fusion doit être vérifiée. Si fetch échoue, un avertissement est émis et
les références disponibles localement peuvent être utilisées. Un échec de
création n'autorise pas à écrire à la place dans le checkout principal.

La valeur par défaut de `workflow.worktrees` est **true**. Seul le booléen YAML
littéral `false` désactive l'isolation des fonctionnalités du flux standard
et de la maintenance. Blueprint/auto-dev conservent toujours leur worktree
partagé fixe. L'initialisation et les mises à jour d'installation s'effectuent
dans le checkout que vous sélectionnez explicitement. Les worktrees des
fonctionnalités terminées sont conservés ; l'achèvement ne les fusionne ni
ne les supprime automatiquement.

Consultez [Développement avec les worktrees](workflow.md#worktree-development)
et [configuration](../reference/configuration.md#workflow-and-review-settings).

<a id="work-with-existing-code"></a>

## Travailler avec du code existant

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

<a id="review-and-debugging"></a>

## Revue et débogage

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

<a id="project-knowledge"></a>

## Connaissances du projet

Le profil du projet conserve les connaissances réutilisables dans `.codexspec/profile/` :

| Catégorie | Contenu |
|----------|----------|
| `constraints/` | Interdictions explicites et limites strictes, à lire en premier |
| `conventions/` | Pratiques, nommage et consignes communes à plusieurs fonctionnalités |
| `pitfalls/` | Pièges rencontrés, causes, solutions de contournement et leçons |
| `decisions/` | Décisions d'architecture et autres décisions réutilisables d'une fonctionnalité à l'autre |
| `strategies/` | Signaux indiquant qu'il faut changer d'approche |
| `runbooks/` | Procédures ordonnées et reprise après échec |

`distill` recueille les connaissances réutilisables issues du travail effectué.
L'intention propre à chaque fonctionnalité reste dans ses exigences, sa
conception et son plan. L'initialisation installe des consignes dans CLAUDE.md
et/ou AGENTS.md pour lire toutes les contraintes et les connaissances pertinentes
avant tout travail substantiel. Les connaissances ajoutées par la suite peuvent
s'appliquer sans nouvelle initialisation. Les entrées candidates sont utilisées
avec prudence ; les entrées validées exigent des résultats vérifiés et une
approbation humaine.

```text
/codexspec:distill Capture the reusable lessons from this work
/codexspec:distill review
/codexspec:evolve
```

Lorsque vous lancez manuellement `distill review`, ou appelez directement
`distill` sans nouveau contenu à recueillir, un espace de travail local s'ouvre
dans le navigateur et fonctionne hors ligne. Vous pouvez réviser, valider,
abandonner, différer et consolider les entrées, prévisualiser le Markdown final,
puis sélectionner **Tout appliquer**. Les décisions restent dans un brouillon
récupérable jusqu'à leur application. Les contrôles de conflit empêchent une
application partielle ou un écrasement sans avertissement. Un mode texte
explicite est également disponible dans les environnements sans navigateur.

La valeur par défaut de `workflow.auto_distill` est **true**. Ce paramètre
contrôle trois hooks de fin : l'achèvement réussi de `implement-tasks`, les
commits exécutés via `commit-staged` et la génération de `pr`. La prévisualisation
d'un commit ne déclenche pas la capture.

Les consignes installées dans le projet demandent aussi à l'agent de recueillir
les connaissances réutilisables dès qu'elles apparaissent dans les conversations
courantes, les corrections hors SDD et les longues exécutions de `implement-tasks`.
Ces consignes s'appliquent indépendamment du paramètre de fin ; la capture en
fin de tâche offre une dernière occasion de conserver ces connaissances.

Dans une même session, les déclenchements répétés ne traitent que le nouveau
contenu. D'une session à l'autre, `distill` lit le profil et ignore les
connaissances qui y figurent déjà. S'il ne reste rien de réutilisable, la capture
se termine sans écrire. La capture automatique n'ouvre jamais la revue manuelle,
n'attend jamais une personne et ne bloque jamais le flux de travail qui l'appelle.

`evolve` ne sélectionne que des connaissances validées utiles au-delà du projet,
élabore un brouillon de commande ou de compétence et obtient une approbation
explicite avant d’effectuer un push ou d'ouvrir une PR de contribution
pour revue humaine.

Consultez [Connaissances du projet](commands.md#codexspecdistill)
pour les consignes détaillées.

<a id="reusing-historical-decisions"></a>

### Réutiliser les décisions historiques

Avant de vous interroger sur un changement, l’agent consulte l’historique des
fonctionnalités concernées dans `.codexspec/specs/`. Il lit les décisions
confirmées dans `requirements.md`, suit les ajouts ultérieurs et les remplacements
explicites, puis consulte au besoin les raisons des choix de conception ou les
éléments qui attestent l’état de l’implémentation. Cette préparation précède aussi
tout jugement substantiel sur la conception, l’implémentation, le débogage ou la
revue, dans les conversations courantes comme dans les flux SDD.

Les horodatages des dossiers de fonctionnalités aident à reconstituer l’ordre
des itérations ; un document plus récent n’invalide pas à lui seul une décision
antérieure. Les exigences anciennes qui n’ont pas été modifiées restent
applicables, et les propositions en suspens ne valent pas intention confirmée.
La recherche reste centrée sur la tâche en cours et s’arrête dès que le contexte
est suffisant. Ce contexte est ensuite réutilisé aux étapes suivantes.

Par exemple, pour modifier une interface, un agent qui n’a pas consulté
l’historique pourrait demander :

> « Comment cette fonctionnalité doit-elle gérer la rétrocompatibilité ? »

Après avoir vérifié les décisions pertinentes et l’implémentation actuelle,
il peut poser une question plus précise :

> « Vous aviez confirmé le maintien de l’ancienne interface, qui est toujours
> prise en charge par l’implémentation actuelle. Je propose de la conserver pour
> ce changement. Souhaitez-vous maintenir ce choix ? »

Une information déjà établie dont l’applicabilité ne fait aucun doute peut être
réutilisée sans poser à nouveau la question. Si vous avez déjà dit « Supprimez
l’ancienne interface dans ce changement », l’agent suit cette décision et
explique les conséquences de la migration. **Votre dernière décision explicite
prévaut toujours** ; l’historique permet de préparer des questions plus précises
et d’éviter les répétitions.

Actualisez les installations des projets existants pour recevoir ces consignes.

<a id="git-workflow"></a>

## Flux de travail Git

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

## Traçabilité et reprise

Le fichier `requirements.md` confirmé fait autorité sur l’intention de la fonctionnalité ; la chaîne en aval est `spec.md` → `design.md` → `plan.md` → `tasks.md`, interprétée avec les principes applicables du projet et les faits vérifiés du dépôt. Les exigences ont des ID stables, les éléments de spécification citent `Sources` et les travaux en aval citent `Covers`. Un artefact en aval ne peut pas redéfinir silencieusement une décision en amont. Un conflit entre sources faisant autorité ou une nouvelle décision produit doit être résolu par l’utilisateur. Les anciennes fonctionnalités sans exigences signalent l’absence de confirmation initiale ; celles sans conception utilisent le repli documenté.

Indiquez un chemin de fonctionnalité explicite si la sélection est ambiguë ; les commandes ne choisissent pas silencieusement le répertoire le plus récent. Le parent des worktrees est déterminé à partir du dépôt principal, même depuis un sous-répertoire ou un autre worktree lié. Pour un dépôt bare, il s’agit d’un répertoire voisin nommé `<bare-repository-name>-codexspec-worktrees`. La maintenance indépendante utilise la branche `codexspec/maintenance`.

Une préparation de worktree échouée conserve son identité pour permettre la reprise. Les fusions de bases divergentes doivent réussir les contrôles du projet avant l’écriture des exigences ou le début du développement. L’inspection en lecture seule conserve sa source ; les rapports utilisent le checkout de sortie résolu. L’exécution d’un commit conserve l’index sélectionné et ne transfère jamais les changements indexés de main vers un autre worktree. Si un nouveau worktree ne dispose pas des ressources installées nécessaires, initialisez cette destination avant de poursuivre.

## Modèle de revue

Les revues séparent trois types de sorties :

- **Défauts de fidélité** : conflit avec une source faisant autorité ou couverture obligatoire manquante.
- **Défauts intrinsèques** : l'artefact est contradictoire en lui-même, invérifiable ou irréalisable.
- **Avis de risque / opportunités de conception** : améliorations facultatives sans preuve d'un défaut actuel.

Chaque défaut doit identifier sa preuve, son emplacement, la non-concordance, son impact et la remédiation minimale. Les constats partageant la même cause racine sont fusionnés. Les avis n'affectent ni le statut, ni le score, ni les corrections automatiques.

Le statut de revue est :

- `PASS` : aucun défaut critique, avertissement ou mineur.
- `PASS_WITH_WARNINGS` : seuls des défauts mineurs subsistent.
- `NEEDS_REVISION` : un ou plusieurs avertissements subsistent.
- `BLOCKED` : un conflit critique empêche toute poursuite fiable.

Le score de compatibilité est dérivé des mêmes constats classés plutôt que de déductions fixes par section de template. Le statut fait autorité ; le score n'existe que pour les intégrations qui attendent encore un nombre.

## Revue auto bornée

Les commandes de génération lancent automatiquement la revue correspondante. C'est la discipline de **revue fondée sur des preuves** en action : elles ne peuvent réparer que les défauts étayés par des preuves et reprendre la revue pendant deux tours au maximum. Elles s'arrêtent plus tôt sur `PASS`, et s'interrompent pour une entrée utilisateur lorsque :

- une source faisant autorité entre en conflit avec une autre source ;
- une correction modifierait une intention confirmée ;
- l'élément restant est consultatif plutôt qu'un défaut ;
- deux tours de réparation ont déjà été utilisés.

Les commandes manuelles `/codexspec:review-*` peuvent être lancées à tout moment pour obtenir un rapport neuf.

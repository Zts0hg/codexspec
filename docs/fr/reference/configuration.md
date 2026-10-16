<a id="configuration-and-internationalization"></a>

# Configuration et internationalisation

La configuration est enregistrée dans `.codexspec/config.yml`. Les modèles
restent en anglais ; l'agent rédige les échanges et les artefacts générés dans
les langues configurées. Les 13 codes de langue standard sont `en`, `zh-CN`,
`zh-TW`, `ja`, `ko`, `es`, `fr`, `de`, `pt`, `ru`, `it`, `ar` et `hi`.
Pour le portugais, la CLI utilise `pt` ; la documentation localisée et les
catalogues de traduction utilisent `pt-BR`.

<a id="language-dimensions"></a>

## Langues des échanges, des documents et des commits

| Dimension | Clé de configuration | À l'initialisation | Modifier ensuite | Ce qu'elle contrôle |
|-----------|------------|-------------------|-----------|----------|
| Sortie/base | `language.output` | `--lang` | `config --set-lang` | Langue de repli pour les autres dimensions |
| Échanges | `language.interaction` | `--interaction-lang` | `config --set-interaction-lang` | Conversation et sortie de la CLI |
| Documents | `language.document` | `--document-lang` | `config --set-document-lang` | Exigences, spécifications, documents de conception, plans et tâches |
| Commits | `language.commit` | `--commit-lang` | `config --set-commit-lang` | Messages de commit et textes générés dans les flux de travail Git |

Si la langue d'une dimension n'est pas définie, `language.output` est utilisée,
puis `en` à défaut. Cette règle s'applique indépendamment à chaque dimension.
`language.templates` reste à `en`.

```bash
codexspec init my-project --ai both \
  --interaction-lang zh-CN --document-lang en --commit-lang en

codexspec config
codexspec config --set-document-lang en
codexspec config --list-langs
```

Lors de la première initialisation depuis un terminal TTY, la langue de base
vous est demandée, sauf si vous fournissez `--lang` ou les trois options de
langue spécifiques. `--force` confirme automatiquement les autres demandes
d'initialisation, mais ne supprime pas cette sélection. Sans TTY, l'anglais est
utilisé par défaut. Une nouvelle initialisation conserve les clés de langue
que vous n'avez pas explicitement définies.

<a id="workflow-and-review-settings"></a>

## Paramètres du flux de travail et des revues

| Paramètre | Valeur par défaut | Effet | Commande CLI |
|---------|---------|--------|-------------|
| `workflow.auto_next` | `false` | Passer à l'étape suivante du flux SDD standard après validation | `config --auto-next on\|off` |
| `workflow.auto_distill` | `true` | Recueillir des connaissances sans interaction à l'issue d'un travail réussi | `config --auto-distill on\|off` |
| `workflow.auto_maintenance` | `true` | Appliquer une maintenance incrémentale vérifiée pendant les corrections automatiques | `config --auto-maintenance on\|off` |
| `workflow.worktrees` | `true` | Isoler les fonctionnalités du flux standard et la maintenance indépendante | `config --worktrees on\|off` |
| `review.decided_by` | `reviewer` | Déterminer qui statue sur les constats dont la condition se produit hors du contexte opérationnel du projet | `config --decided-by reviewer\|ask` |

Les options booléennes de la CLI acceptent `on/true/1/yes` et `off/false/0/no`,
sans distinction de casse et avec d'éventuels espaces autour de la valeur.
Une option booléenne sans valeur inverse la valeur actuelle du checkout de
destination ; les valeurs sont enregistrées sous forme de booléens dans YAML.

Avec `review.decided_by: reviewer`, l'agent de revue décide quels constats sont
admis comme défauts. Avec `ask`, lorsqu'une condition à l'origine d'un constat
se produit hors du contexte du projet, une décision sur ce scénario reste en
attente. L'utilisateur décide une fois s'il faut corriger le problème ou exclure
le scénario, puis sa décision confirmée est conservée pour les revues suivantes.
Les décisions en attente bloquent l'achèvement. Pour une exécution donnée de
`review-code`, vous pouvez remplacer le mode configuré avec `--decided-by`.

Les modifications de configuration suivent le routage des worktrees. Un
changement indépendant demandé depuis le checkout principal s'effectue dans
le worktree de maintenance et ne modifie pas immédiatement le paramètre effectif
du principal. Les changements effectués dans le worktree d'une fonctionnalité
y prennent effet.

<details>
<summary>Options d'initialisation de la CLI</summary>

| Option | Signification |
|--------|---------|
| `PROJECT_NAME` | Nom du nouveau dossier ; utiliser `.` pour le dossier courant |
| `--here`, `-h` | Initialiser le dossier courant |
| `--ai`, `-a` | `claude`, `codex` ou `both` ; valeur par défaut : `claude` |
| `--lang`, `-l` | Définir la langue de sortie de base |
| `--interaction-lang` | Définir la langue des échanges |
| `--document-lang` | Définir la langue des documents |
| `--commit-lang` | Définir la langue des messages de commit |
| `--force`, `-f` | Régénérer les artefacts installés et confirmer automatiquement les demandes de migration, de mise à jour et de conformité ; préserver le contexte rédigé pour le projet et les paramètres sans rapport |
| `--no-git` | Ne pas initialiser le dépôt Git |
| `--debug`, `-d` | Afficher des informations de débogage détaillées |

</details>

<details>
<summary>Options de configuration de la CLI</summary>

| Option | Signification |
|--------|---------|
| `--set-lang`, `-l` | Définir la langue de sortie de base |
| `--set-interaction-lang` | Définir la langue des échanges |
| `--set-document-lang` | Définir la langue des documents |
| `--set-commit-lang`, `-c` | Définir la langue des messages de commit |
| `--list-langs` | Afficher les codes de langue pris en charge |
| `--auto-next` | Inverser ou définir le passage automatique à l'étape suivante |
| `--auto-distill` | Inverser ou définir la capture automatique des connaissances |
| `--auto-maintenance` | Inverser ou définir la maintenance incrémentale automatique |
| `--worktrees` | Inverser ou définir l'isolation par worktree locale à chaque checkout |
| `--decided-by` | Définir le mode de décision de revue sur `reviewer` ou `ask` |

</details>

<details>
<summary>Exemple de configuration</summary>

```yaml
version: "1.0"

language:
  output: "en"
  interaction: "zh-CN"
  document: "en"
  commit: "en"
  templates: "en"

project:
  ai: "both"

workflow:
  auto_next: false
  auto_distill: true
  auto_maintenance: true
  worktrees: true

review:
  decided_by: reviewer
```

</details>

Consultez [Configuration](configuration.md) et
[Internationalisation](../user-guide/i18n.md) pour connaître en détail
le fonctionnement des langues et des paramètres.

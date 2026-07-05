# Configuration

## Emplacement du fichier de configuration

`.codexspec/config.yml`

## Schéma de configuration

```yaml
version: "1.0"

language:
  output: "zh-CN"        # Langue de base ; les trois ci-dessous se rabattent sur elle, puis "en"
  interaction: "zh-CN"   # Dialogue LLM + sortie CLI codexspec (optionnel → par défaut output)
  document: "en"         # Exigences/spec/plan/tasks générés (optionnel → par défaut output)
  commit: "en"           # Messages de commit git (optionnel → par défaut output)
  templates: "en"        # Conserver "en"

project:
  ai: "claude"
  created: "2025-02-15"

workflow:
  auto_next: false       # Avance automatique entre les étapes du workflow (opt-in)
```

## Paramètres de langue

CodexSpec décompose la langue en quatre dimensions configurables indépendamment. `output` est la base ; `interaction`, `document` et `commit` la surchargent et se rabattent sur elle (puis sur `en`) lorsqu'elles ne sont pas définies. Cela vous permet, par exemple, de converser avec Claude dans une langue tout en conservant les artefacts générés ou les messages de commit dans une autre.

| Dimension | Clé | À l'init | Plus tard | Contrôle | Se rabat sur |
|-----------|-----|----------|-----------|----------|---------------|
| Output (base) | `output` | `--lang` | `config --set-lang` | base pour les trois autres | `en` |
| Interaction | `interaction` | `--interaction-lang` | `config --set-interaction-lang` | dialogue LLM + sortie CLI | output → `en` |
| Document | `document` | `--document-lang` | `config --set-document-lang` | spec/plan/tasks générés | output → `en` |
| Commit | `commit` | `--commit-lang` | `config --set-commit-lang` | messages de commit git | output → `en` |
| Templates | `templates` | — | — | source des modèles de commandes (toujours `en`) | — |

**Valeurs prises en charge :** voir [Internationalisation](../user-guide/i18n.md#supported-languages)

### `language.output`

La langue de sortie de base. Les autres dimensions s'y rapportent lorsqu'elles ne sont pas définies explicitement.

### `language.interaction`

Langue de la conversation entre vous et le LLM, ainsi que de la sortie terminal de la CLI `codexspec`. Optionnel — par défaut `output`.

### `language.document`

Langue des fichiers d'artefacts générés (exigences/spec/plan/tasks). Optionnel — par défaut `output`.

### `language.commit`

Langue des messages de commit git. Optionnel — par défaut `output`.

### `language.templates`

Langue des modèles. Doit rester `"en"` pour la compatibilité.

## Paramètres du projet

### `project.ai`

L'assistant AI utilisé. Contrôle les fichiers de contexte d'agent déposés par `codexspec init` :

- `claude` (par défaut) — écrit `CLAUDE.md` (et `.claude/commands/`).
- `codex` — écrit `AGENTS.md` et `.agents/skills/` à la place.
- `both` — écrit tout ce qui précède afin que le projet soit prêt pour Claude Code et Codex CLI.

`CLAUDE.md` est toujours créé (le projet reste utilisable depuis Claude Code) ; `AGENTS.md` et `.agents/skills/` ne sont créés que lorsque `project.ai` vaut `codex` ou `both`.

### `project.created`

Date à laquelle le projet a été initialisé.

## Paramètres du workflow

### `workflow.auto_next`

Contrôle si le pipeline Requirements-First SDD **avance automatiquement** vers la prochaine étape du workflow une fois l'étape courante validée, au lieu d'exiger que vous déclenchiez manuellement la commande suivante.

- **Par défaut :** `false` (opt-in). Seule la valeur littérale `true` active l'avance automatique.
- **Basculer / définir avec :** `codexspec config --auto-next` (l'indicateur seul bascule la valeur courante ; passez `on`/`off` pour la définir explicitement).

**Chaîne :**

```
specify → generate-spec → spec-to-plan → plan-to-tasks → implement-tasks
```

**Porte de réussite :**

- `generate-spec`, `spec-to-plan`, `plan-to-tasks` : la boucle de revue intégrée à la commande doit renvoyer un Overall Status `PASS` ou `PASS_WITH_WARNINGS`.
- `specify` : aucune boucle de revue, la porte est donc votre confirmation explicite que la découverte des exigences est terminée (le résumé **final** de l'étape, pas chaque résumé intermédiaire).
- `implement-tasks` : étape terminale — rien ne se déclenche automatiquement après elle.

Quand la boucle de revue renvoie `NEEDS_REVISION` ou `BLOCKED`, la chaîne s'interrompt et le contrôle vous revient. Avant chaque avance, l'agent émet une ligne de notification (par exemple : `auto_next: review passed → invoking /codexspec:spec-to-plan`).

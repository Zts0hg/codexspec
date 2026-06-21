# Configuration

## Emplacement du Fichier de Configuration

`.codexspec/config.yml`

## Schema de Configuration

```yaml
version: "1.0"

language:
  output: "zh-CN"        # Langue de base ; les trois suivantes se rabattent sur elle, puis "en"
  interaction: "zh-CN"   # Dialogue LLM + sortie CLI codexspec (optionnel → par defaut : output)
  document: "en"         # Exigences/spec/plan/taches generes (optionnel → par defaut : output)
  commit: "en"           # Messages de commit git (optionnel → par defaut : output)
  templates: "en"        # Langue des modeles (conserver comme "en")

project:
  ai: "claude"      # Assistant AI
  created: "2025-02-15"
```

## Parametres de Langue

CodexSpec decompose la langue en quatre dimensions configurables independamment. `output` est la base ; `interaction`, `document` et `commit` la remplacent et se rabattent sur elle (puis `en`) lorsqu'elles ne sont pas definies. Cela vous permet, par exemple, de converser avec Claude dans une langue tout en conservant les artefacts generes ou les messages de commit dans une autre.

| Dimension | Cle | Definir a l'init | Definir plus tard | Controle | Se rabat sur |
|-----------|-----|------------------|-------------------|----------|---------------|
| Output (base) | `output` | `--lang` | `config --set-lang` | base pour les trois autres | `en` |
| Interaction | `interaction` | `--interaction-lang` | `config --set-interaction-lang` | dialogue LLM + sortie CLI | output → `en` |
| Document | `document` | `--document-lang` | `config --set-document-lang` | spec/plan/taches generes | output → `en` |
| Commit | `commit` | `--commit-lang` | `config --set-commit-lang` | messages de commit git | output → `en` |
| Templates | `templates` | — | — | source des modeles de commandes (toujours `en`) | — |

**Valeurs prises en charge :** Voir [Internationalisation](../user-guide/i18n.md#supported-languages)

### `language.output`

La langue de sortie de base. Les autres dimensions se rabattent sur elle lorsqu'elles ne sont pas definies explicitement.

### `language.interaction`

Langue pour la conversation entre vous et le LLM, ainsi que pour la sortie terminal de la CLI `codexspec`. Optionnel — par defaut `output`.

### `language.document`

Langue pour les fichiers d'artefacts generes (exigences/spec/plan/taches). Optionnel — par defaut `output`.

### `language.commit`

Langue pour les messages de commit git. Optionnel — par defaut `output`.

### `language.templates`

Langue des modeles. Doit rester comme `"en"` pour la compatibilite.

## Parametres du Projet

### `project.ai`

L'assistant AI utilise. Prend actuellement en charge :

- `claude` (par defaut)

### `project.created`

Date d'initialisation du projet.

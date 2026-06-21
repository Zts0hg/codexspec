# Reference CLI

## Commandes

### `codexspec init`

Initialiser un nouveau projet CodexSpec.

```bash
codexspec init [NOM_PROJET] [OPTIONS]
```

**Arguments :**

| Argument | Description |
|----------|-------------|
| `NOM_PROJET` | Nom de votre nouveau repertoire de projet (utilisez `.` ou `--here` pour le repertoire courant) |

**Options :**

| Option | Raccourci | Description |
|--------|-----------|-------------|
| `--here` | `-h` | Initialiser dans le repertoire courant |
| `--ai` | `-a` | Assistant AI a utiliser (par defaut : claude) |
| `--lang` | `-l` | Langue de sortie (base) ; interaction/document/commit se rabattent sur elle (ex. en, zh-CN, ja) |
| `--interaction-lang` | | Langue d'interaction (dialogue LLM + sortie CLI `codexspec`) ; remplace `--lang` |
| `--document-lang` | | Langue des documents (exigences/spec/plan/taches generes) ; remplace `--lang` |
| `--commit-lang` | | Langue des messages de commit ; remplace `--lang` |
| `--force` | `-f` | Ecraser les fichiers existants et confirmer automatiquement les invites ; ne regenere jamais `config.yml` |
| `--no-git` | | Passer l'initialisation git |
| `--debug` | `-d` | Activer la sortie de debogage |

`--lang` definit la langue de base `output` ; `--interaction-lang`, `--document-lang` et `--commit-lang` la remplacent pour leur dimension (chacune se rabat sur `output`, puis `en`). Voir [Internationalisation](../user-guide/i18n.md) pour le modele complet.

La premiere initialisation dans un TTY sans `--lang` (et sans les trois indicateurs de dimension) demande une langue de base ; dans un environnement non-TTY (CI/scripts), elle utilise `en` par defaut — **entierement non-interactif**. Relancer `init` preserve toute cle de langue que vous n'avez pas specifiee ; `--force` ne regenere jamais `config.yml`.

**Exemples :**

```bash
# Creer un nouveau projet
codexspec init mon-projet

# Initialiser dans le repertoire courant
codexspec init . --ai claude

# Entierement non-interactif : base zh-CN, messages de commit en anglais
codexspec init mon-projet --lang zh-CN --commit-lang en

# Definir chaque dimension explicitement (scriptable, sans invite)
codexspec init mon-projet \
  --interaction-lang zh-CN --document-lang en --commit-lang en
```

---

### `codexspec check`

Verifier les outils installes.

```bash
codexspec check
```

---

### `codexspec version`

Afficher les informations de version.

```bash
codexspec version
```

---

### `codexspec config`

Afficher ou modifier la configuration du projet.

```bash
codexspec config [OPTIONS]
```

**Options :**

| Option | Raccourci | Description |
|--------|-----------|-------------|
| `--set-lang` | `-l` | Definir la langue de sortie (base) |
| `--set-interaction-lang` | | Definir la langue d'interaction (dialogue LLM + sortie CLI) |
| `--set-document-lang` | | Definir la langue des documents (spec/plan/taches generes) |
| `--set-commit-lang` | `-c` | Definir la langue des messages de commit |
| `--list-langs` | | Lister toutes les langues prises en charge |

Chaque `--set-*-lang` met a jour une [dimension de langue](../user-guide/i18n.md) ; toute dimension que vous ne definissez pas se rabat sur `output`, puis `en`.

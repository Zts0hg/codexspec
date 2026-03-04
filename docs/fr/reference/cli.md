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
| `NOM_PROJET` | Nom de votre nouveau repertoire de projet |

**Options :**

| Option | Raccourci | Description |
|--------|-----------|-------------|
| `--here` | `-h` | Initialiser dans le repertoire courant |
| `--ai` | `-a` | Assistant AI a utiliser (par defaut : claude) |
| `--lang` | `-l` | Langue de sortie (ex. en, zh-CN, ja) |
| `--force` | `-f` | Forcer l'ecrasement des fichiers existants |
| `--no-git` | | Passer l'initialisation git |
| `--debug` | `-d` | Activer la sortie de debogage |

**Exemples :**

```bash
# Creer un nouveau projet
codexspec init mon-projet

# Initialiser dans le repertoire courant
codexspec init . --ai claude

# Avec sortie en chinois
codexspec init mon-projet --lang zh-CN
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
| `--set-lang` | `-l` | Definir la langue de sortie |
| `--list-langs` | | Lister toutes les langues prises en charge |

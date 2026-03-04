# Configuration

## Emplacement du Fichier de Configuration

`.codexspec/config.yml`

## Schema de Configuration

```yaml
version: "1.0"

language:
  output: "en"      # Langue de sortie pour les documents
  templates: "en"   # Langue des modeles (conserver comme "en")

project:
  ai: "claude"      # Assistant AI
  created: "2025-02-15"
```

## Parametres de Langue

### `language.output`

La langue pour les interactions Claude et les documents generes.

**Valeurs prises en charge :** Voir [Internationalisation](../user-guide/i18n.md#supported-languages)

### `language.templates`

Langue des modeles. Doit rester comme `"en"` pour la compatibilite.

## Parametres du Projet

### `project.ai`

L'assistant AI utilise. Prend actuellement en charge :

- `claude` (par defaut)

### `project.created`

Date d'initialisation du projet.

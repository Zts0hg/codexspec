# Configuração

## Localização do Arquivo de Configuração

`.codexspec/config.yml`

## Schema de Configuração

```yaml
version: "1.0"

language:
  output: "en"      # Idioma de saída para documentos
  templates: "en"   # Idioma dos templates (mantenha como "en")

project:
  ai: "claude"      # Assistente AI
  created: "2025-02-15"
```

## Configurações de Idioma

### `language.output`

O idioma para interações do Claude e documentos gerados.

**Valores suportados:** Consulte [Internacionalização](../user-guide/i18n.md#idiomas-suportados)

### `language.templates`

Idioma dos templates. Deve permanecer como `"en"` para compatibilidade.

## Configurações do Projeto

### `project.ai`

O assistente AI sendo usado. Atualmente suporta:

- `claude` (padrão)

### `project.created`

Data em que o projeto foi inicializado.

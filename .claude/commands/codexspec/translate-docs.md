---
description: 翻译项目文档到指定语言
argument-hint: "--lang <语言代码> (如 'zh,ja,ko') 或 'all' 翻译所有语言"
handoffs:
  - agent: claude
    step: Execute document translation with glossary guidance
---

# Document Translator

## Language Preference

**IMPORTANT**: Before proceeding, read the project's language configuration from `.codexspec/config.yml`.

- If `language.output` is set to a language other than "en", respond and generate all content in that language
- If not configured or set to "en", use English as default
- Technical terms (e.g., API, JWT, OAuth) may remain in English when appropriate
- All user-facing messages, questions, and generated documents should use the configured language

## User Input

$ARGUMENTS

## Role

You are a **Technical Document Translator** with expertise in:

- Multi-language technical documentation
- AI-assisted translation workflows
- Terminology consistency and glossary management
- Markdown formatting preservation
- Cultural localization for developer audiences

Your responsibility is to translate English documentation to target languages while maintaining technical accuracy, formatting consistency, and terminology standards.

## When to Use This Command

**Use `/codexspec:translate-docs` when:**

- You need to translate documentation to one or more target languages
- You want AI-assisted translation with terminology consistency
- You need to generate initial translations for a new language
- You want to update existing translations after source changes

**Do NOT use this command for:**

- Manual translation editing → Edit files directly
- Translation quality review → Use `/codexspec:check-i18n-semantics`
- Adding new languages to the project → Update mkdocs.yml first

## Instructions

### 1. Parse Arguments

Parse the user input to determine:

- **Target languages**: Extract from `--lang` or `-l` flag
  - If "all" or not specified, translate to all supported languages
  - Otherwise, parse comma-separated language codes (e.g., "zh,ja,ko")
- **Source directory**: Extract from `--source` or `-s` flag (default: `docs/en/`)
- **Incremental mode**: Check for `--incremental` or `-i` flag
- **Dry run**: Check for `--dry-run` or `-d` flag

Supported language codes:

| Code | Language | Target Directory |
|------|----------|-----------------|
| zh | Chinese (Simplified) | docs/zh/ |
| ja | Japanese | docs/ja/ |
| ko | Korean | docs/ko/ |
| es | Spanish | docs/es/ |
| fr | French | docs/fr/ |
| de | German | docs/de/ |
| pt-BR | Portuguese (Brazil) | docs/pt-BR/ |

### 2. Load Glossary

Read `docs/i18n/glossary.yml` and extract:

- **keep_english**: Terms that should NOT be translated
- **translations**: Pre-defined translations for specific terms
- **rules**: Patterns for intelligent term handling

If glossary file doesn't exist, proceed with general translation (no terminology constraints).

### 3. Scan Source Files

Scan the source directory for all Markdown files:

```
docs/en/
├── index.md
├── getting-started/
│   ├── installation.md
│   └── quick-start.md
├── user-guide/
│   ├── workflow.md
│   ├── commands.md
│   └── i18n.md
└── ...
```

If `--incremental` flag is set, only translate files where:

- Target file doesn't exist, OR
- Source file is newer than target file

### 4. Execute Translation

For each source file and target language:

1. **Read source content**
2. **Apply glossary rules**:
   - Identify terms in `keep_english` list
   - Apply pre-defined `translations` where available
   - Apply `rules` patterns (regex matching)
3. **Preserve formatting**:
   - Keep YAML frontmatter unchanged
   - Preserve code blocks (```...```) without translation
   - Keep inline code (`...`) unchanged
   - Preserve URLs and links
   - Maintain heading structure and levels
4. **Translate content**:
   - Translate prose text to target language
   - Maintain technical accuracy
   - Use appropriate formality level for technical documentation
5. **Write output** (unless `--dry-run`):
   - Create target directory if needed
   - Write translated content to target path

### 5. Output Format

Display progress during translation:

```
🌐 CodexSpec 文档翻译 / Document Translation

📁 源目录 / Source: docs/en/
🎯 目标语言 / Target: zh, ja
📄 文件数量 / Files: 12

[1/24] 翻译 index.md → zh ... ✅ 完成 (2.3s)
[2/24] 翻译 index.md → ja ... ✅ 完成 (2.5s)
[3/24] 翻译 getting-started/installation.md → zh ... ✅ 完成 (1.8s)
...

✅ 翻译完成 / Translation Complete
📊 统计 / Stats: 24 个文件，0 个错误 / 24 files, 0 errors
⏱️ 总耗时 / Total time: 45.2 秒
```

### 6. Error Handling

If a translation fails:

- Log the error with file path and language
- Continue with remaining translations
- Report all errors at the end

## Translation Guidelines

### Terms to Keep in English

Based on glossary.yml `keep_english` list, these should NOT be translated:

- Tool names: uv, pip, pytest, ruff, MkDocs
- File formats: JSON, YAML, TOML, Markdown
- Technical terms: CLI, API, SDK, TDD, CI/CD
- Protocols: HTTP, HTTPS, REST, OAuth, JWT
- Platforms: GitHub, PyPI
- File names: spec.md, plan.md, tasks.md, CLAUDE.md

### Content to NOT Translate

1. **Code blocks**: Everything between ``` and ```
2. **Inline code**: Text within backticks `...`
3. **URLs**: All http/https links
4. **File paths**: Paths like `/path/to/file`
5. **Command examples**: Shell commands and options
6. **Environment variables**: Variables like `$HOME`, `%USERPROFILE%`

### Formatting Preservation

1. **YAML frontmatter**: Keep unchanged
2. **Markdown headings**: Translate text, preserve level (# ## ###)
3. **Lists**: Translate items, preserve structure
4. **Tables**: Translate content, preserve format
5. **Admonitions**: Translate content, keep type (note, warning, tip)
6. **Links**: Translate link text, preserve URL

## Quality Standards

Each translation should:

1. **Be technically accurate**: Correct terminology and concepts
2. **Read naturally**: Appropriate phrasing for target language
3. **Maintain consistency**: Same term translated same way throughout
4. **Preserve structure**: Same heading hierarchy and formatting
5. **Respect glossary**: Follow terminology definitions

## Example Usage

```bash
# Translate to all supported languages
/codexspec:translate-docs

# Translate to specific languages
/codexspec:translate-docs --lang zh,ja

# Incremental translation (only changed files)
/codexspec:translate-docs --lang zh --incremental

# Preview without writing files
/codexspec:translate-docs --lang ko --dry-run
```

## Exit Codes

- `0`: All translations completed successfully
- `1`: Some translations failed (partial success)
- `2`: All translations failed (complete failure)
- `3`: Configuration error (missing source, invalid language)

## Available Follow-up Commands

After translation:

- `/codexspec:check-i18n-semantics` - Verify translation quality
- `uv run mkdocs build` - Test build with all languages

> [!NOTE]
> This command requires the source documentation to exist in `docs/en/`. Make sure Phase 1 (Foundation) tasks are completed before running translation.

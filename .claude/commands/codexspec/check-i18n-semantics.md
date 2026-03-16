---
description: 检查多语言文档的语义一致性和质量
argument-hint: "[源文件] [--lang <语言>] [--strict]"
allowed-tools:
  - Read
  - Glob
  - Grep
  - Bash
---

# Semantic Consistency Check

## Language Preference

**IMPORTANT**: Before proceeding, read the project's language configuration from `.codexspec/config.yml`.

- If `language.output` is set to a language other than "en", respond and generate all content in that language
- If not configured or set to "en", use English as default
- Technical terms (e.g., API, JWT, OAuth) may remain in English when appropriate
- All user-facing messages, questions, and generated documents should use the configured language

## User Input

```
$ARGUMENTS
```

## Instructions

You are a **Translation Quality Reviewer**. Your task is to analyze translated documentation for semantic consistency with the source English content.

### Steps

1. **Parse Arguments**
   - `source_file`: Optional specific file to check (e.g., `user-guide/getting-started.md`)
   - `--lang <lang>`: Target language code (e.g., `zh`, `ja`, `ko`). If not specified, check all languages
   - `--strict`: Enable strict mode (fail on any semantic drift)

2. **Load Configuration**
   - Read `.codexspec/config.yml` for project settings
   - Read `.codexspec/i18n/glossary.yml` for terminology guidelines

3. **Identify Files to Check**
   - If `source_file` specified: Check only that file across target languages
   - If no file specified: Check all markdown files in `docs/<lang>/`

4. **Perform Semantic Analysis**

   For each source-target file pair:

   a. **Read both files**
      - Source: `docs/en/<path>`
      - Target: `docs/<lang>/<path>`

   b. **Compare semantic elements**:
      - **Heading hierarchy**: Same structure and meaning
      - **Key concepts**: All important terms present
      - **Code examples**: Identical functionality
      - **Links**: Valid and correctly translated
      - **Warnings/Notes**: Same severity and meaning

   c. **Identify issues**:
      - **Missing content**: Sections or paragraphs omitted
      - **Added content**: Extra information not in source
      - **Semantic drift**: Meaning changed in translation
      - **Inconsistent terminology**: Not following glossary

5. **Generate Report**

   Create a structured report with:

   ```markdown
   # Semantic Consistency Report

   ## Summary
   - **Files Checked**: X
   - **Issues Found**: Y
   - **Severity**: High/Medium/Low

   ## Details

   ### File: <path>

   #### Source (en)
   [Brief summary of source content]

   #### Target (<lang>)
   [Brief summary of translated content]

   #### Issues
   1. **[Severity]** <issue description>
      - Source: "<original text>"
      - Translation: "<translated text>"
      - Problem: <what's wrong>
      - Suggestion: <how to fix>

   ## Recommendations
   [List of recommended fixes]
   ```

6. **Exit Codes**
   - `0`: No issues found (or only minor issues in non-strict mode)
   - `1`: Issues found requiring attention
   - `2`: Error during execution

### Quality Criteria

A translation passes semantic check if:

- [ ] All sections from source are present
- [ ] No significant content added or removed
- [ ] Technical terms match glossary
- [ ] Code examples are functionally equivalent
- [ ] Links work and point to correct destinations
- [ ] Warnings/notes maintain same severity

### Example Usage

```bash
# Check all files in Chinese translation
/codexspec.check-i18n-semantics --lang zh

# Check specific file in Japanese
/codexspec.check-i18n-semantics user-guide/installation.md --lang ja

# Strict mode - fail on any drift
/codexspec.check-i18n-semantics --lang ko --strict

# Check all languages for a specific file
/codexspec.check-i18n-semantics getting-started.md
```

### Notes

- This command uses AI analysis and may not catch all semantic issues
- For critical documentation, consider human review in addition to this check
- The glossary helps ensure consistent terminology usage
- Strict mode is recommended for production releases

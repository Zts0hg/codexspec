---
description: Generate a detailed specification document from high-level requirements
handoffs:
  - agent: claude
    step: Transform requirements into detailed specification
---

# Specification Generator

## Language Preference

**IMPORTANT**: Before proceeding, read the project's language configuration from `.codexspec/config.yml`.
- If `language.output` is set to a language other than "en", respond and generate all content in that language
- If not configured or set to "en", use English as default
- Technical terms (e.g., API, JWT, OAuth) may remain in English when appropriate
- All user-facing messages, questions, and generated documents should use the configured language

## User Input

$ARGUMENTS

## Instructions

Generate a detailed specification document from the provided high-level requirements. This command is useful when you have rough ideas and want to expand them into a complete specification.

### Steps

1. **Analyze Input**: Parse and understand the high-level requirements provided by the user.

2. **Expand Requirements**: Convert high-level ideas into detailed, actionable specifications by:
   - Identifying implied user stories
   - Deriving functional requirements
   - Considering non-functional requirements
   - Identifying potential edge cases

3. **Add Context**: Include relevant context, assumptions, and constraints.

4. **Structure Document**: Organize the specification following the standard template.

5. **Generate Document**: Create a structured specification document.

### Expansion Guidelines

When expanding requirements, consider:

1. **User Perspectives**: Who will use this feature? What are their goals?
2. **Use Cases**: What are the main workflows?
3. **Data Requirements**: What data is needed? How is it structured?
4. **Integration Points**: What external systems are involved?
5. **Error Handling**: What could go wrong? How should errors be handled?
6. **Performance**: What are the performance expectations?
7. **Security**: What security considerations apply?

### Reference Templates

Use the following templates as reference for generating the specification:

- **Detailed**: `.codexspec/templates/docs/spec-template-detailed.md` - Full format with user stories, acceptance criteria, requirements, and success metrics
- **Simple**: `.codexspec/templates/docs/spec-template-simple.md` - Lightweight format for simpler features

### Output

A comprehensive specification document following the standard spec template, saved to the appropriate location in `.codexspec/specs/`.

> [!NOTE]
> This is a placeholder command. The full implementation will be added in future versions.

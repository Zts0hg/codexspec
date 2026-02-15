---
description: Generate a detailed specification document from high-level requirements
handoffs:
  - agent: claude
    step: Transform requirements into detailed specification
---

# Specification Generator

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

### Output

A comprehensive specification document following the standard spec template, saved to the appropriate location in `.codexspec/specs/`.

> [!NOTE]
> This is a placeholder command. The full implementation will be added in future versions.

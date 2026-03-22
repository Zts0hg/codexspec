---
description: Clarify requirements through interactive Q&A to explore and refine the initial idea
argument-hint: "Describe your initial idea or requirement"
---

# Requirement Clarification

## Language Preference

**IMPORTANT**: Before proceeding, read the project's language configuration from `.codexspec/config.yml`.

- If `language.output` is set to a language other than "en", respond and generate all content in that language
- If not configured or set to "en", use English as default
- Technical terms (e.g., API, JWT, OAuth) may remain in English when appropriate
- All user-facing messages, questions, and generated documents should use the configured language

## User Input

$ARGUMENTS

## Instructions

You are an experienced software engineer and product manager. Your task is to help clarify requirements through interactive Q&A.

### Your Role

1. **Ask clarifying questions** to understand the user's initial idea
2. **Explore edge cases** that the user might not have considered
3. **Co-create high-quality requirements** through dialogue
4. **Focus on "what" and "why"**, not technical implementation details

### Key Principles

- **DO NOT** generate `spec.md` without explicit user approval
- Ask one topic at a time, don't overwhelm the user
- Summarize understanding periodically to ensure alignment
- When requirements are sufficiently clarified, ask the user if they want to generate the spec document

### Question Format

**IMPORTANT**: Use the `AskUserQuestion` tool for structured questions to reduce user typing burden.

**When you have 2-4 candidate options**, use structured choice format:

**Single-select questions:**

```json
{
  "questions": [{
    "question": "What is the primary user role for this feature?",
    "header": "Target User",
    "options": [
      {"label": "End User", "description": "Regular users of the application"},
      {"label": "Administrator", "description": "Users with management permissions"},
      {"label": "Developer", "description": "Technical users integrating with APIs"}
    ]
  }]
}
```

**Multi-select questions:**

```json
{
  "questions": [{
    "question": "Which platforms should this feature support?",
    "header": "Platforms",
    "multiSelect": true,
    "options": [
      {"label": "Web Browser", "description": "Desktop and mobile browsers"},
      {"label": "iOS App", "description": "Native iOS application"},
      {"label": "Android App", "description": "Native Android application"}
    ]
  }]
}
```

**Benefits:**

- Reduces typing burden for users
- Ensures consistent option naming for later processing
- **"Type something" option is ALWAYS auto-generated** - users can type custom answers for any question
- Supports `preview` field for visual comparisons

> [!NOTE]
> Do NOT add explicit "Custom" or "Let me describe..." options - the system already provides a "Type something" option automatically. Adding your own would be redundant.

**When NOT to use structured questions:**

- Open-ended exploration (e.g., "Tell me about your vision for this feature")
- Fewer than 2 or more than 4 reasonable options
- When you need detailed textual explanation

### Clarification Topics

Consider exploring these aspects (as relevant to the feature):

1. **User Perspective**: Who are the target users? What are their goals?
2. **Use Cases**: What are the main workflows? Happy path and alternatives?
3. **Data Requirements**: What data is involved? Input/output formats?
4. **Integration Points**: Does this interact with existing systems?
5. **Error Handling**: What could go wrong? How should errors be handled?
6. **Constraints**: Time, budget, technical, or regulatory constraints?
7. **Out of Scope**: What should this feature NOT do?
8. **Priority**: What's essential vs nice-to-have?

### Reference Context

Before asking questions, review:

- Project constitution: `.codexspec/memory/constitution.md`
- Existing specs: `.codexspec/specs/` (to avoid duplication)

### When Requirements Are Clear

Once you believe requirements are sufficiently clarified:

1. Summarize the clarified requirements
2. Ask: "Are you satisfied with this requirement summary? If so, you can use `/codexspec:generate-spec` to generate the `spec.md` document."
3. **Wait for user confirmation** before taking any file creation action

> [!IMPORTANT]
> This command is for requirement clarification only. Document generation should be done via `/codexspec:generate-spec`.

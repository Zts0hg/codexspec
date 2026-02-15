# CodexSpec Extension Development Guide

This guide explains how to create, test, and publish extensions for CodexSpec.

## What is a CodexSpec Extension?

Extensions allow you to add custom commands, hooks, and configurations to CodexSpec without modifying the core codebase.

## Extension Structure

```
my-extension/
├── extension.yml          # Extension manifest (required)
├── commands/              # Custom slash commands
│   ├── command1.md
│   └── command2.md
├── config-template.yml    # Optional configuration template
└── README.md              # Extension documentation
```

## Creating an Extension

### 1. Create the Extension Directory

```bash
mkdir my-extension
cd my-extension
mkdir commands
```

### 2. Create the Manifest (extension.yml)

```yaml
schema_version: "1.0"

extension:
  id: "my-extension"
  name: "My Extension"
  version: "1.0.0"
  description: "What this extension does"
  author: "Your Name"
  repository: "https://github.com/your-org/codexspec-my-extension"
  license: "MIT"

requires:
  codexspec_version: ">=0.1.0"

provides:
  commands:
    - name: "codexspec.my-extension.command1"
      file: "commands/command1.md"
      description: "Description of command1"
```

### 3. Create Command Files

Each command is a Markdown file with YAML frontmatter:

```markdown
---
description: Description of what this command does
---

# Command Title

## User Input

\`\`\`text
$ARGUMENTS
\`\`\`

## Instructions

1. Step 1
2. Step 2
...
```

### 4. Test Your Extension

Test locally by copying to your project:

```bash
cp -r my-extension /path/to/your/project/.codexspec/extensions/
```

## Extension Manifest Reference

### Required Fields

| Field | Description |
|-------|-------------|
| `schema_version` | Always "1.0" |
| `extension.id` | Unique identifier (lowercase, hyphens) |
| `extension.name` | Human-readable name |
| `extension.version` | Semantic version (X.Y.Z) |
| `extension.description` | Brief description |

### Optional Fields

| Field | Description |
|-------|-------------|
| `extension.author` | Author name |
| `extension.repository` | Git repository URL |
| `extension.license` | License identifier |
| `extension.homepage` | Documentation URL |

### Commands

```yaml
provides:
  commands:
    - name: "codexspec.my-extension.command"
      file: "commands/command.md"
      description: "Command description"
      aliases: ["codexspec.cmd"]  # Optional
```

### Hooks

Hooks allow commands to run automatically after specific events:

```yaml
hooks:
  after_tasks:
    command: "codexspec.my-extension.validate"
    optional: true
    prompt: "Run validation?"
    description: "Validates generated tasks"
```

Available hook points:
- `after_constitution` - After running /codexspec.constitution
- `after_specify` - After running /codexspec.specify
- `after_spec_to_plan` - After running /codexspec.spec-to-plan
- `after_plan_to_tasks` - After running /codexspec.plan-to-tasks
- `after_implement` - After running /codexspec.implement-tasks

### Configuration

```yaml
provides:
  config:
    - name: "my-extension-config.yml"
      template: "config-template.yml"
      description: "Extension settings"
      required: true

defaults:
  setting1: value1
  setting2: value2
```

## Best Practices

1. **Naming Convention**: Use `codexspec.{extension-id}.{command}` for command names
2. **Documentation**: Include a README.md with usage examples
3. **Versioning**: Follow semantic versioning
4. **Dependencies**: Clearly document any external requirements
5. **Testing**: Test your extension with different project types

## Publishing Extensions

1. Create a Git repository for your extension
2. Tag releases with semantic versions
3. Submit to the CodexSpec extension catalog (coming soon)

## Example Extensions

See the `extensions/template/` directory for a complete example.

---

For more information, visit: https://github.com/your-org/codexspec

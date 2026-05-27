# Contributing to CodexSpec

Thank you for your interest in contributing to CodexSpec! This guide will help you get started.

## Code of Conduct

By participating in this project, you agree to abide by our [Code of Conduct](CODE_OF_CONDUCT.md).

## How to Contribute

### Reporting Bugs

- Use the [Bug Report](https://github.com/Zts0hg/codexspec/issues/new?template=bug_report.yml) issue template
- Include your Python version, OS, and CodexSpec version
- Provide clear steps to reproduce the issue

### Suggesting Features

- Use the [Feature Request](https://github.com/Zts0hg/codexspec/issues/new?template=feature_request.yml) issue template
- Describe the problem you're trying to solve
- Explain your proposed solution

### Submitting Pull Requests

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/my-feature`)
3. Make your changes
4. Run tests and linting
5. Commit using [Conventional Commits](https://www.conventionalcommits.org/) format
6. Submit a pull request

## Development Setup

### Prerequisites

- Python 3.11+
- [uv](https://docs.astral.sh/uv/) package manager
- Git

### Local Development

```bash
# Clone the repository
git clone https://github.com/Zts0hg/codexspec.git
cd codexspec

# Install development dependencies
uv sync --dev

# Run locally
uv run codexspec --help

# Run tests
uv run pytest

# Lint code
uv run ruff check src/
```

### Documentation

```bash
# Install docs dependencies
uv sync --extra docs

# Preview documentation locally
uv run mkdocs serve

# Build documentation
uv run mkdocs build
```

### Building

```bash
uv build
```

## Code Style

- **Line length**: 120 characters max
- **Formatting**: Follow PEP 8
- **Imports**: Use absolute imports
- **Type hints**: Required for public functions
- **Commit messages**: Use [Conventional Commits](https://www.conventionalcommits.org/) (e.g., `feat:`, `fix:`, `docs:`, `refactor:`)

## Pull Request Guidelines

- Keep PRs focused on a single change
- Include tests for new functionality
- Update documentation if needed
- Ensure all CI checks pass before requesting review

## Questions?

Feel free to open a [Discussion](https://github.com/Zts0hg/codexspec/discussions) if you have questions or want to discuss ideas before contributing.

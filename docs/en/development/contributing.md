# Contributing

## Prerequisites

- Python 3.11+
- uv package manager
- Git

## Local Development

```bash
# Clone the repository
git clone https://github.com/Zts0hg/codexspec.git
cd codexspec

# Install development dependencies
uv sync --extra dev

# Run locally
uv run codexspec --help

# Run tests
uv run pytest

# Lint code
uv run ruff check src/
```

## Documentation

```bash
# Install docs dependencies
uv sync --extra dev --extra docs

# Preview documentation locally
uv run mkdocs serve

# Build documentation
uv run mkdocs build --strict
```

## Building

```bash
uv build
```

## Pull Request Process

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests and linting
5. Submit a pull request

## Code Style

- Line length: 120 characters max
- Follow PEP 8
- Use type hints for public functions

Read [CLAUDE.md](https://github.com/Zts0hg/codexspec/blob/main/CLAUDE.md), [AGENTS.md](https://github.com/Zts0hg/codexspec/blob/main/AGENTS.md), and
[Repository Layout](https://github.com/Zts0hg/codexspec/blob/main/docs/internal/repository-layout.md) before changing templates,
packaging, or initialization. Distributed command and skill copies are generated
installation artifacts; edit their authoritative sources and regenerate them.

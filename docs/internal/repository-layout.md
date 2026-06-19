# Repository Layout & Audience Separation

> ⚠️ **SCOPE**: This document governs the **CodexSpec repository layout** — how the repo's top-level paths are organized, and which of them ship to end users vs. are maintainer-internal. Read it **before** adding, moving, or deleting files, or changing packaging. It is imported into `CLAUDE.md` via `@`.

## Core Principle

CodexSpec is a tool that end users **install** (`uv tool install` / Claude Code plugin marketplace). Therefore every top-level path belongs to exactly one of two audiences:

- **USER-facing** — reaches users: appears in the wheel/sdist, and/or is copied into a user's project by `codexspec init`.
- **MAINTAINER-internal** — used only to develop, test, publish, or operate CodexSpec itself. **Never** reaches end users.

Keeping the two physically separated — and enforcing the boundary via explicit packaging config — is what prevents leaks of maintainer tooling, **secrets**, and internal assets into user packages. This is a deliberate, load-bearing design, not an accident.

## Top-level Path Classification

| Path | Audience | In wheel/sdist? | Copied by `init`? | Notes |
|---|---|---|---|---|
| `src/codexspec/` | USER | wheel (=the package) + sdist | — | CLI implementation |
| `templates/` | USER | wheel + sdist | yes (commands/docs) | Slash-command templates — **source of truth** for commands |
| `scripts/bash/*.sh` | USER | wheel + sdist | yes (mac/linux) | The ONLY scripts `init` copies on unix |
| `scripts/powershell/*.ps1` | USER | wheel + sdist | yes (windows) | The ONLY scripts `init` copies on windows |
| `scripts/python/` | **MAINTAINER** | ❌ excluded | ❌ | Claude Code automation; contains `.env` (secrets), `.venv/`, `logs/` |
| `internal/` | **MAINTAINER** | ❌ (outside every include) | ❌ | Maintainer ops scripts (e.g. `google_search_console.py`) |
| `docs/` | MAINTAINER (site build source) | ❌ | ❌ | mkdocs `docs_dir`; builds the Pages site — **not** a docs store |
| `docs/internal/` | MAINTAINER | ❌ (site + pkg) | ❌ | internal reference assets; listed in mkdocs `exclude_docs` |
| `.codexspec/memory/` | MAINTAINER | ❌ | ❌ | repo governance (`constitution.md`, this file) |
| `.claude/commands/codexspec/` | **derived** | — | — | self-bootstrap install artifact — do NOT edit (see constitution) |
| `tests/` · `hooks/` · `.github/` | MAINTAINER | ❌ | ❌ | dev & CI |
| `extensions/` | dev-facing | ❌ | ❌ | extension system (contributors) |
| root `README*.md` · `LICENSE` · logo SVGs | USER-facing (repo) | README/LICENSE auto-added to sdist | — | README translations stay at **root** (GitHub convention) |

## The Packaging Boundary (critical)

Defined in `pyproject.toml`:

```toml
[tool.hatch.build.targets.wheel]
# Only the two script subdirs that `codexspec init` actually copies.
force-include = { "templates" = "codexspec/templates",
                  "scripts/bash" = "codexspec/scripts/bash",
                  "scripts/powershell" = "codexspec/scripts/powershell" }

[tool.hatch.build.targets.sdist]
include = ["/src", "/templates", "/scripts/bash", "/scripts/powershell",
           "/codexspec-icon.svg", "/codexspec-logo-dark.svg", "/codexspec-logo-light.svg"]
```

**Why only `bash/` + `powershell/` subdirs are listed (not all of `scripts/`)**: `force-include` does **NOT** respect `.gitignore`. Including the whole `scripts/` dir would sweep in `scripts/python/.env` (a live Telegram bot token), notify logs, and maintainer automation scripts. Listing only the two user subdirs **is** the enforced boundary.

`codexspec init` (see `src/codexspec/__init__.py`) then copies `scripts/bash/*.sh` (unix) / `scripts/powershell/*.ps1` (windows) into the user's `.codexspec/scripts/`. **Nothing else under `scripts/` is ever read by `init`.**

**Verification** — run before any packaging change, confirm the result shows ONLY `bash/` and `powershell/`:

```bash
uv build
python3 -c "import glob,zipfile; \
print([n for n in zipfile.ZipFile(glob.glob('dist/*.whl')[0]).namelist() if 'scripts/' in n])"
```

## `docs/` is a mkdocs build source, NOT a docs store

- `docs_dir: docs` (`mkdocs.yml`). Everything published at <https://zts0hg.github.io/codexspec/> comes from `mkdocs build` of `docs/`.
- `exclude_docs` (`mkdocs.yml`) keeps non-language folders off the site: `/plans/`, `/i18n/`, `/internal/`.
- i18n plugin (`docs_structure: folder`): each `docs/<lang>/` is one language; **`en` is `default: true` → served at the site root** (no `/en/` prefix); other languages at `/<lang>/`.
- Consequence: **README translations do NOT belong in `docs/`.** They are GitHub repo-level READMEs and stay at the repo **root**. Placing them in `docs/` would be conceptually wrong and risk them being built as site pages.

## Google Search Console verification

Only `docs/en/google*.html` is effective — `en` is the default language, so it is served at the site **root**, which is where Google verifies. A repo-**root** copy of the same file is **dead** (outside `docs_dir`, never built or deployed) — do not re-add one.

## Decision Rule: where should a new file go?

Ask: **"Will an end user of `codexspec` need this at runtime?"**

- **Yes** (CLI behavior, a template, a script they receive via `init`) → a shipping path: `src/codexspec/`, `templates/`, or `scripts/bash/`·`scripts/powershell/`.
- **No** (only for developing / testing / publishing / operating CodexSpec) → an internal path: `internal/` (ops), `scripts/python/` (automation), `docs/internal/` (reference assets), `.codexspec/memory/` (governance), `tests/`, `hooks/`, etc.

**Caveat**: the include/force-include lists above are **explicit, not wildcards**. Adding a new internal subdir under `scripts/` or `templates/` does NOT auto-exclude it — but adding a new *user* subdir will NOT auto-ship either; you must extend the include lists deliberately. Adding a new non-language folder under `docs/` requires adding it to `exclude_docs` to keep it off the site.

## Known Gotchas

- **`scripts/python/.env` holds a live Telegram bot token** (plus `.venv/`, `logs/`). It must NEVER appear in a package. The narrowed `force-include`/`include` is what guarantees this — do **not** widen them to all of `scripts/`.
- **`force-include` ignores `.gitignore`** — a file being gitignored does NOT keep it out of the wheel if its parent dir is force-included.
- **Logo SVGs** (`codexspec-logo-dark.svg` / `codexspec-logo-light.svg`) must stay at repo **root**: README `<picture srcset="…">` resolves relative to the README's directory, so moving them breaks the logo on GitHub/PyPI.
- **`.claude/commands/codexspec/`** is a self-bootstrap install artifact — edit `templates/commands/` instead (see constitution → "Self-Bootstrap").
- **The sdist is a strict allowlist** (its `include` is restrictive), but hatchling still auto-adds metadata files (`pyproject.toml`, `README.md`, `LICENSE`, `PKG-INFO`, `.gitignore`).
- **`scripts/python/` tooling is heavily test-coupled**: `tests/scripts/python/` (400+ tests) import these modules via `sys.path` pointing at `scripts/python`, and the `.venv` lives there too. Relocating `scripts/python/` is a dedicated migration, not a casual move.

---

*This document is the authority on repository layout and the user/maintainer packaging boundary. Keep it updated whenever top-level paths or `pyproject.toml` includes change.*

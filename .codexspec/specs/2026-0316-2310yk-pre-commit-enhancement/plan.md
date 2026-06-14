# Implementation Plan: Pre-commit 配置增强

**Related Spec**: `.codexspec/specs/2026-0316-2310yk-pre-commit-enhancement/spec.md`
**Created**: 2026-03-16
**Status**: Draft

## Context

项目已有基础的 pre-commit 配置（Ruff + 通用文件检查），需要增强以引入更多工程最佳实践。当前配置缺少类型检查、文档检查、测试验证、提交信息规范、拼写检查、脚本检查和安全检查等功能。

## Goals / Non-Goals

**Goals:**

- 增强现有 pre-commit 配置，添加 8 种新检查
- 确保每次提交前自动执行质量门禁
- 保持与现有工具链（uv、Ruff）的兼容性
- 提供清晰的错误信息和修复建议

**Non-Goals:**

- 不涉及 CI/CD 流程配置（已有单独配置）
- 不添加其他语言的检查（JavaScript、TypeScript 等）
- 不开发自定义 pre-commit hook
- 不集成 Pre-commit CI 云服务

## Tech Stack

| Category | Technology | Version | Notes |
|----------|------------|---------|-------|
| Language | Python | 3.11+ | 项目主要语言 |
| Package Manager | uv | latest | 依赖管理 |
| Linter/Formatter | Ruff | 0.9.10+ | 已有配置 |
| Type Checker | mypy | 1.15.0+ | 新增 |
| Markdown Linter | markdownlint-cli | 0.42.0+ | 新增 |
| Test Framework | pytest | 7.0+ | 已有配置 |
| Commit Linter | commitizen | 3.30.0+ | 新增 |
| Spell Checker | codespell | 2.3.0+ | 新增 |
| Shell Linter | shellcheck | 0.10.0+ | 新增 |
| Security Scanner | bandit | 1.8.0+ | 新增 |
| Dependency Scanner | safety | latest | 新增 |

## Constitutionality Review

| Principle | Compliance | Notes |
|-----------|------------|-------|
| Code Quality | ✅ | 添加 linter、formatter、type checker 直接提升代码质量 |
| Testing Standards | ✅ | 将 pytest 集成到 pre-commit 确保测试始终通过 |
| Documentation | ✅ | markdownlint 确保文档格式一致性 |
| Architecture | ✅ | 配置模块化，每个检查独立配置，易于维护 |
| Performance | ⚠️ | 需监控 pre-commit 执行时间，已在 NFR-001 中定义 < 60秒 |
| Security | ✅ | bandit 和 safety 检查代码和依赖安全 |

## Architecture Overview

Pre-commit 作为 Git hooks 的管理框架，在提交前自动执行配置的检查工具。

```
┌─────────────────────────────────────────────────────────────────────┐
│                        Git Commit Workflow                           │
└─────────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────────┐
│                      Pre-commit Framework                            │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                    .pre-commit-config.yaml                   │   │
│  └─────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────┘
                                │
        ┌───────────────────────┼───────────────────────┐
        ▼                       ▼                       ▼
┌───────────────┐     ┌───────────────┐     ┌───────────────┐
│  Code Quality │     │  Security     │     │   Standards   │
├───────────────┤     ├───────────────┤     ├───────────────┤
│ • Ruff        │     │ • bandit      │     │ • markdownlint│
│ • mypy        │     │ • safety      │     │ • codespell   │
│ • shellcheck  │     │               │     │ • commitlint  │
│ • pytest      │     │               │     │               │
└───────────────┘     └───────────────┘     └───────────────┘
        │                       │                       │
        └───────────────────────┼───────────────────────┘
                                ▼
                    ┌───────────────────┐
                    │  Pass / Block     │
                    │  Commit           │
                    └───────────────────┘
```

## Component Structure

### 文件变更清单

```
codexspec/
├── .pre-commit-config.yaml    # [修改] 添加新 hooks
├── .markdownlint.json         # [新增] Markdown 规则配置
├── .codespellrc               # [新增] 拼写检查配置
├── pyproject.toml             # [修改] 添加 bandit 配置
└── .pre-commit-hooks-README.md # [新增] 使用文档
```

## Module Dependency Graph

```
┌─────────────────────────────────────────────────────────────────┐
│                    .pre-commit-config.yaml                       │
│                     (主配置文件)                                  │
└───────────────────────────┬─────────────────────────────────────┘
                            │
        ┌───────────────────┼───────────────────┐
        │                   │                   │
        ▼                   ▼                   ▼
┌───────────────┐   ┌───────────────┐   ┌───────────────┐
│ .markdownlint │   │  .codespellrc │   │ pyproject.toml│
│    .json      │   │               │   │  (bandit)     │
└───────────────┘   └───────────────┘   └───────────────┘
```

## Module Specifications

### Module: .pre-commit-config.yaml

- **Responsibility**: 定义所有 pre-commit hooks 配置
- **Dependencies**: 无
- **Interface**: pre-commit 框架读取此文件
- **Files**: `.pre-commit-config.yaml` (修改)

### Module: .markdownlint.json

- **Responsibility**: 定义 Markdown 文件的检查规则
- **Dependencies**: 被 markdownlint-cli 读取
- **Interface**: JSON 配置文件
- **Files**: `.markdownlint.json` (新增)

### Module: .codespellrc

- **Responsibility**: 定义拼写检查的忽略列表和配置
- **Dependencies**: 被 codespell 读取
- **Interface**: TOML/INI 配置文件
- **Files**: `.codespellrc` (新增)

### Module: pyproject.toml (bandit section)

- **Responsibility**: 定义 bandit 安全检查配置
- **Dependencies**: 被 bandit 读取
- **Interface**: TOML 配置段
- **Files**: `pyproject.toml` (修改)

## Configuration Details

### .pre-commit-config.yaml 新增内容

```yaml
repos:
  # === 新增 Hooks ===

  # mypy - Type checking
  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.15.0
    hooks:
      - id: mypy
        args: [--ignore-missing-imports, --python-version=3.11]
        additional_dependencies: [types-PyYAML]
        files: ^src/

  # markdownlint-cli - Markdown linting
  - repo: https://github.com/igorshubovych/markdownlint-cli
    rev: v0.42.0
    hooks:
      - id: markdownlint
        args: [--fix]

  # codespell - Spell checking
  - repo: https://github.com/codespell-project/codespell
    rev: v2.3.0
    hooks:
      - id: codespell
        args: [--config, .codespellrc]

  # shellcheck - Shell script linting
  - repo: https://github.com/shellcheck-py/shellcheck-py
    rev: v0.10.0
    hooks:
      - id: shellcheck
        args: [--severity=warning]

  # bandit - Security linting
  - repo: https://github.com/PyCQA/bandit
    rev: 1.8.0
    hooks:
      - id: bandit
        args: [-c, pyproject.toml]
        additional_dependencies: ["bandit[toml]"]
        files: ^src/

  # pytest - Testing (local hook)
  - repo: local
    hooks:
      - id: pytest
        name: pytest
        entry: uv run pytest -x --tb=short
        language: system
        pass_filenames: false
        files: \.py$
        stages: [pre-commit]

  # commitizen - Commit message linting
  - repo: https://github.com/commitizen-tools/commitizen
    rev: v3.30.0
    hooks:
      - id: commitizen
        stages: [commit-msg]
```

### .markdownlint.json

```json
{
  "default": true,
  "MD001": true,
  "MD003": { "style": "atx" },
  "MD004": { "style": "dash" },
  "MD007": { "indent": 2 },
  "MD013": { "line_length": 120, "code_blocks": false },
  "MD024": { "siblings_only": true },
  "MD033": false,
  "MD034": false,
  "MD040": false,
  "MD041": false
}
```

### .codespellrc

```toml
[codespell]
skip = .git,.venv,*.lock,*.pyc,__pycache__,local-ref
ignore-words-list = nd,fo,hte,cmn
check-filenames = false
```

### pyproject.toml bandit 配置

```toml
[tool.bandit]
exclude_dirs = ["tests", ".venv", "local-ref"]
skips = ["B101"]  # Skip assert_used check (pytest uses assert)
```

## Technical Decisions

### Decision 1: pytest 作为 local hook

**Context**: pytest 需要在项目虚拟环境中运行，且需要访问项目依赖

**Options Considered**:

1. 使用 `pre-commit/mirrors-pytest` - 需要单独安装依赖
2. 使用 local hook 直接调用 `uv run pytest` - 复用项目环境

**Decision**: 使用 local hook

**Rationale**:

- 复用 uv 管理的虚拟环境，避免重复安装
- 确保测试运行环境与开发环境一致
- 简化配置，减少维护成本

### Decision 2: markdownlint-cli 而非 markdownlint

**Context**: 需要选择 Markdown linting 工具

**Options Considered**:

1. `markdownlint` (Ruby) - 需要 Ruby 环境
2. `markdownlint-cli2` - 更现代但配置复杂
3. `markdownlint-cli` - Node.js 工具，pre-commit 直接支持

**Decision**: 使用 markdownlint-cli

**Rationale**:

- pre-commit 有官方支持的 repo
- 配置简单，社区使用广泛
- 支持 `--fix` 自动修复

### Decision 3: commitizen 而非 commitlint

**Context**: 需要选择 commit message linting 工具

**Options Considered**:

1. `@commitlint/cli` - Node.js 工具，需要额外配置
2. `commitizen` - Python 工具，pre-commit 直接支持

**Decision**: 使用 commitizen

**Rationale**:

- Python 生态工具，与项目技术栈一致
- pre-commit 有官方支持的 repo
- 同时支持 commit message 生成和验证

### Decision 4: safety 使用 pre-commit-hooks-safety

**Context**: 需要选择依赖安全检查工具

**Options Considered**:

1. 直接使用 `safety` CLI - 需要手动配置
2. `pre-commit-hooks-safety` - 封装好的 pre-commit hook

**Decision**: 使用 pre-commit-hooks-safety

**Rationale**:

- 专为 pre-commit 设计
- 自动检测 requirements.txt 或 pyproject.toml
- 配置简单

### Decision 5: shellcheck severity=warning

**Context**: shellcheck 有多个严重级别

**Options Considered**:

1. `--severity=error` - 仅报告错误
2. `--severity=warning` - 报告警告和错误
3. `--severity=style` - 报告所有问题

**Decision**: 使用 `--severity=warning`

**Rationale**:

- 平衡严格性和实用性
- 捕获潜在问题但不阻塞非关键修复
- 可根据实际情况调整

## Risks / Trade-offs

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| 检查时间过长影响开发效率 | Medium | High | 优化配置，仅检查变更文件；使用 `SKIP` 环境变量跳过 |
| markdownlint 规则与现有文档冲突 | High | Medium | 配置宽松规则，渐进式修复现有文档 |
| bandit 误报阻塞提交 | Medium | Medium | 配置 skips 排除已知误报 |
| mypy 缺少类型存根 | Medium | Low | 使用 `--ignore-missing-imports` |
| safety 检查需要网络 | Low | Medium | CI 环境通常有网络；本地可跳过 |

## Implementation Phases

### Phase 1: 基础配置 (Foundation)

- [ ] 创建 `.markdownlint.json` 配置文件
- [ ] 创建 `.codespellrc` 配置文件
- [ ] 在 `pyproject.toml` 中添加 bandit 配置
- [ ] 更新 `.pre-commit-config.yaml` 添加新 hooks

### Phase 2: 核心功能 (Core Implementation)

- [ ] 添加 mypy 类型检查 hook
- [ ] 添加 markdownlint 文档检查 hook
- [ ] 添加 codespell 拼写检查 hook
- [ ] 添加 shellcheck 脚本检查 hook
- [ ] 添加 bandit 安全检查 hook
- [ ] 添加 safety 依赖检查 hook

### Phase 3: 高级功能 (Advanced Features)

- [ ] 添加 pytest 测试 hook (local hook)
- [ ] 添加 commitizen 提交信息检查 hook
- [ ] 配置 hook 执行顺序和依赖关系

### Phase 4: 验证和文档 (Testing & Documentation)

- [ ] 运行 `pre-commit run --all-files` 验证所有检查
- [ ] 修复现有代码中的问题
- [ ] 创建 `.pre-commit-hooks-README.md` 使用文档
- [ ] 更新项目 CLAUDE.md 说明 pre-commit 使用方式

### Phase 5: 渐进式启用 (Gradual Rollout)

- [ ] 团队成员安装新的 pre-commit hooks
- [ ] 监控首次全量检查结果
- [ ] 根据反馈调整规则配置
- [ ] 更新 CI 配置（如需要）

## Security Considerations

- **bandit**: 检查 Python 代码中的安全漏洞模式
- **safety**: 检查依赖的已知 CVE 漏洞
- **配置隔离**: 安全检查配置在独立的配置文件中，便于审计
- **排除测试**: bandit 排除 tests 目录，避免误报

## Performance Considerations

- **增量检查**: pre-commit 默认仅检查变更文件
- **pytest 优化**: 使用 `-x` 在首个失败时停止
- **并行执行**: pre-commit 默认并行执行不相关的 hooks
- **目标**: 增量提交检查 < 60 秒

## Rollback Plan

如果新配置导致问题：

1. **临时跳过**: 使用 `SKIP=hook-id git commit` 跳过特定检查
2. **完全跳过**: 使用 `git commit --no-verify` 跳过所有检查
3. **回滚配置**: 恢复到之前的 `.pre-commit-config.yaml`
4. **禁用特定 hook**: 在配置中注释掉问题 hook

---

*Generated by CodexSpec on 2026-03-16*

# Feature: Pre-commit 配置增强

## Overview

增强项目现有的 pre-commit 配置，引入软件工程最佳实践，提高代码的可维护性和质量。通过添加类型检查、文档检查、测试验证、提交信息规范、拼写检查、脚本检查和安全检查等多维度的质量门禁，确保每次提交的代码都符合项目标准。

## Goals

- 在提交前自动检测代码质量问题
- 确保代码符合类型安全要求
- 保持文档格式一致性
- 强制执行 Conventional Commits 规范
- 提前发现安全漏洞
- 提高整体代码可维护性

## User Stories

### Story 1: 类型安全检查

**作为** 开发者
**我希望** 在提交代码前自动进行类型检查
**以便** 及早发现类型错误，避免运行时问题

**Acceptance Criteria:**

- [ ] 使用 mypy 进行静态类型检查
- [ ] 类型错误会阻止提交
- [ ] 支持忽略缺失导入的第三方库

### Story 2: 文档格式一致性

**作为** 项目维护者
**我希望** 所有 Markdown 文档遵循统一的格式规范
**以便** 保持项目文档的专业性和可读性

**Acceptance Criteria:**

- [ ] 使用 markdownlint 检查 Markdown 文件
- [ ] 不符合规范的文档会阻止提交
- [ ] 配置合理的规则以适应项目现有文档风格

### Story 3: 测试质量门禁

**作为** 开发者
**我希望** 在提交前确保所有测试通过
**以便** 防止有问题的代码进入代码库

**Acceptance Criteria:**

- [ ] 使用 pytest 运行测试
- [ ] 测试失败会阻止提交
- [ ] 在每次提交前执行

### Story 4: 提交信息规范

**作为** 团队成员
**我希望** 所有提交信息遵循 Conventional Commits 规范
**以便** 便于自动化工具处理和生成变更日志

**Acceptance Criteria:**

- [ ] 使用 commitlint 检查提交信息格式
- [ ] 不符合规范的提交信息会被拒绝
- [ ] 支持 feat, fix, docs, style, refactor, test, chore 等类型

### Story 5: 拼写错误检测

**作为** 开发者
**我希望** 自动检测代码和文档中的拼写错误
**以便** 保持专业性并避免低级错误

**Acceptance Criteria:**

- [ ] 使用 codespell 检查拼写错误
- [ ] 支持自定义词典以忽略项目特定术语
- [ ] 检测常见拼写错误

### Story 6: Shell 脚本质量

**作为** 开发者
**我希望** Bash 脚本在提交前经过静态分析
**以便** 避免脚本语法错误和潜在问题

**Acceptance Criteria:**

- [ ] 使用 shellcheck 检查 Bash 脚本
- [ ] 检测常见错误（如未引用变量、未使用变量等）
- [ ] 仅检查 .sh 文件

### Story 7: 代码安全检查

**作为** 安全意识强的开发者
**我希望** 在提交前检测代码中的安全漏洞
**以便** 及早发现和修复安全问题

**Acceptance Criteria:**

- [ ] 使用 bandit 检查 Python 代码安全漏洞
- [ ] 检测常见安全问题（如硬编码密码、不安全的函数调用等）
- [ ] 安全问题会阻止提交

### Story 8: 依赖安全检查

**作为** 项目维护者
**我希望** 检查项目依赖是否有已知安全漏洞
**以便** 及时更新不安全的依赖

**Acceptance Criteria:**

- [ ] 使用 safety 检查依赖安全
- [ ] 读取 pyproject.toml 和 uv.lock 中的依赖信息
- [ ] 发现漏洞时阻止提交

## Functional Requirements

### REQ-001: 类型检查集成

- 启用 mypy 作为 pre-commit hook
- 配置 `--ignore-missing-imports` 以处理无类型存根的第三方库
- 配置 `--python-version 3.11` 与项目要求一致

### REQ-002: Markdown 检查集成

- 启用 markdownlint-cli 作为 pre-commit hook
- 配置 `.markdownlint.json` 或在 `.pre-commit-config.yaml` 中内联配置
- 设置合理的规则：行长度、标题风格、列表格式等

### REQ-003: 测试集成

- 启用 pytest 作为 pre-commit hook
- 配置仅在 Python 文件变更时运行测试
- 使用 `pytest -x` 在第一个失败时停止

### REQ-004: Commit Message 检查集成

- 启用 commitlint 作为 commit-msg hook
- 配置 Conventional Commits 规范
- 支持 @commitlint/config-conventional 预设

### REQ-005: 拼写检查集成

- 启用 codespell 作为 pre-commit hook
- 配置忽略列表（如项目特定术语）
- 检查 .py, .md, .sh 等文本文件

### REQ-006: Shell 脚本检查集成

- 启用 shellcheck 作为 pre-commit hook
- 仅检查 .sh 文件
- 配置合理的检查级别

### REQ-007: 代码安全检查集成

- 启用 bandit 作为 pre-commit hook
- 配置检查级别（建议使用默认级别）
- 排除测试目录

### REQ-008: 依赖安全检查集成

- 启用 safety 作为 pre-commit hook
- 配置读取 uv.lock 或 requirements.txt
- 设置安全漏洞检查

### REQ-009: 保留现有配置

- 保留 Ruff linter 和 formatter
- 保留通用文件检查（trailing-whitespace, end-of-file-fixer 等）
- 保持 CI 配置（autofix_prs, autoupdate 等）

## Non-Functional Requirements

### NFR-001: 提交性能

- 所有检查的总执行时间应控制在合理范围内（建议 < 60 秒）
- 考虑使用 `--from-ref` 和 `--to-ref` 仅检查变更的文件
- 测试运行可考虑只运行相关测试

### NFR-002: 兼容性

- 与现有的 uv 包管理器兼容
- 支持 Python 3.11+
- 跨平台兼容（macOS, Linux, Windows）

### NFR-003: 可配置性

- 允许通过 `SKIP` 环境变量跳过特定检查
- 支持 `--no-verify` 跳过所有检查（紧急情况）
- 各检查可独立启用/禁用

### NFR-004: 开发者体验

- 提供清晰的错误信息
- 错误信息应包含修复建议
- 提供安装和配置文档

## Acceptance Criteria (Test Cases)

### TC-001: mypy 类型检查

**Given** 一个包含类型错误的 Python 文件
**When** 执行 `pre-commit run`
**Then** mypy 应报告类型错误并阻止提交

### TC-002: markdownlint 文档检查

**Given** 一个格式不符合规范的 Markdown 文件
**When** 执行 `pre-commit run`
**Then** markdownlint 应报告格式问题并阻止提交

### TC-003: pytest 测试运行

**Given** 存在失败的测试用例
**When** 执行 `git commit`
**Then** pytest 应报告测试失败并阻止提交

### TC-004: commitlint 提交信息检查

**Given** 一个不符合 Conventional Commits 规范的提交信息
**When** 执行 `git commit`
**Then** commitlint 应拒绝该提交

### TC-005: codespell 拼写检查

**Given** 一个包含拼写错误的文件
**When** 执行 `pre-commit run`
**Then** codespell 应报告拼写错误

### TC-006: shellcheck 脚本检查

**Given** 一个包含潜在问题的 Bash 脚本
**When** 执行 `pre-commit run`
**Then** shellcheck 应报告问题

### TC-007: bandit 安全检查

**Given** 一个包含安全漏洞模式的 Python 文件
**When** 执行 `pre-commit run`
**Then** bandit 应报告安全问题

### TC-008: safety 依赖检查

**Given** 项目依赖中存在已知漏洞
**When** 执行 `pre-commit run`
**Then** safety 应报告依赖漏洞

### TC-009: 全量检查通过

**Given** 所有代码符合规范
**When** 执行 `pre-commit run --all-files`
**Then** 所有检查应通过

## Edge Cases

### EC-001: 无 Python 文件变更

- **场景**: 提交仅包含 Markdown 或其他非 Python 文件
- **处理**: pytest hook 应跳过运行（通过 `files` 配置）

### EC-002: 合并提交

- **场景**: 执行 git merge 产生的提交
- **处理**: commitlint 应允许合并提交格式

### EC-003: 修复提交

- **场景**: 使用 `git commit --amend` 修复提交
- **处理**: 所有检查应正常执行

### EC-004: 大型提交

- **场景**: 提交大量文件
- **处理**: 考虑检查超时设置，确保合理时间内完成

### EC-005: 第三方库无类型存根

- **场景**: mypy 遇到无类型存根的第三方库
- **处理**: 使用 `--ignore-missing-imports` 忽略

### EC-006: 项目特定术语

- **场景**: codespell 将项目特定术语标记为拼写错误
- **处理**: 配置忽略列表

## Output Examples

### 更新后的 .pre-commit-config.yaml 结构

```yaml
repos:
  # Ruff - Fast Python linter and formatter (保留)
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.9.10
    hooks:
      - id: ruff
        args: [--fix, --exit-non-zero-on-fix]
      - id: ruff-format

  # mypy - Type checking (新增)
  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.15.0
    hooks:
      - id: mypy
        args: [--ignore-missing-imports]

  # markdownlint - Markdown linting (新增)
  - repo: https://github.com/igorshubovych/markdownlint-cli
    rev: v0.42.0
    hooks:
      - id: markdownlint

  # pytest - Testing (新增)
  - repo: local
    hooks:
      - id: pytest
        name: pytest
        entry: uv run pytest -x
        language: system
        pass_filenames: false
        files: \.py$

  # codespell - Spell checking (新增)
  - repo: https://github.com/codespell-project/codespell
    rev: v2.3.0
    hooks:
      - id: codespell

  # shellcheck - Shell script linting (新增)
  - repo: https://github.com/shellcheck-py/shellcheck-py
    rev: v0.10.0
    hooks:
      - id: shellcheck

  # bandit - Security linting (新增)
  - repo: https://github.com/PyCQA/bandit
    rev: 1.8.0
    hooks:
      - id: bandit
        args: [-c, pyproject.toml]

  # safety - Dependency security (新增)
  - repo: https://github.com/Lucas-C/pre-commit-hooks-safety
    rev: v1.3.3
    hooks:
      - id: python-safety-dependencies-check

  # commitlint - Commit message linting (新增)
  - repo: https://github.com/commitizen-tools/commitizen
    rev: v3.30.0
    hooks:
      - id: commitizen
        stages: [commit-msg]

  # General file checks (保留)
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v5.0.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
        args: [--unsafe]
      - id: check-added-large-files
        args: ['--maxkb=500']
      - id: check-merge-conflict
      - id: debug-statements
      - id: requirements-txt-fixer
        files: requirements.*\.txt$
```

## Out of Scope

- CI/CD 流程中的 pre-commit 配置（已有单独的 CI 配置）
- 其他语言的检查（如 JavaScript、TypeScript）
- Docker 相关检查（项目当前无 Dockerfile）
- 性能基准测试
- 自动修复所有问题的功能（部分检查支持自动修复，但非全部）
- Pre-commit CI 云服务集成（使用本地 pre-commit）
- 自定义 pre-commit hook 开发

## Dependencies

- Python 3.11+
- uv 包管理器
- pre-commit >= 3.0.0
- 所有新增检查工具的依赖

## Risks and Mitigations

| 风险 | 影响 | 缓解措施 |
|------|------|---------|
| 检查时间过长 | 降低开发效率 | 优化配置，仅检查变更文件 |
| 误报影响开发 | 挫败感 | 配置合理的规则，允许临时跳过 |
| 工具版本冲突 | 安装失败 | 使用 pre-commit 管理工具版本 |
| 跨平台兼容性 | 部分开发者无法使用 | 选择跨平台兼容的工具 |

---

*Generated by CodexSpec on 2026-03-16*

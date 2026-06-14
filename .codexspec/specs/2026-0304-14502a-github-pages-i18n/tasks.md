# Task Breakdown: GitHub Pages 文档多语言支持

## Overview

- **Total tasks**: 35
- **Parallelizable tasks**: 14
- **Estimated phases**: 5

## Phase 1: Foundation (基础架构)

### Task 1.1: 更新 pyproject.toml 添加 mkdocs-i18n 依赖

- **Type**: Setup
- **Files**: `pyproject.toml`
- **Description**: 在 `[project.optional-dependencies].docs` 中添加 `mkdocs-i18n>=0.4.0` 依赖
- **Dependencies**: None
- **Est. Complexity**: Low
- **Verification**: `uv sync --extra docs` 成功执行

### Task 1.2: 创建 docs/en/ 目录并移动现有文档

- **Type**: Setup
- **Files**: `docs/en/` (目录结构)
- **Description**:
  - 创建 `docs/en/` 目录
  - 移动 `docs/*.md` 到 `docs/en/`
  - 移动 `docs/getting-started/` 到 `docs/en/getting-started/`
  - 移动 `docs/user-guide/` 到 `docs/en/user-guide/`
  - 移动 `docs/case-studies/` 到 `docs/en/case-studies/`
  - 移动 `docs/reference/` 到 `docs/en/reference/`
  - 移动 `docs/development/` 到 `docs/en/development/`
  - 移动 `docs/assets/` 到 `docs/en/assets/`
- **Dependencies**: Task 1.1
- **Est. Complexity**: Low
- **Verification**: 文件结构正确，无遗漏

### Task 1.3: 创建其他语言目录结构 [P]

- **Type**: Setup
- **Files**: `docs/zh/`, `docs/ja/`, `docs/ko/`, `docs/es/`, `docs/fr/`, `docs/de/`, `docs/pt-BR/`
- **Description**: 创建 7 个翻译目标语言的目录结构，每个目录包含空的 `.gitkeep` 文件
- **Dependencies**: Task 1.2
- **Est. Complexity**: Low
- **Verification**: 所有目录存在，结构正确

### Task 1.4: 创建 .codexspec/i18n/ 目录

- **Type**: Setup
- **Files**: `.codexspec/i18n/`
- **Description**: 创建术语表配置目录
- **Dependencies**: None
- **Est. Complexity**: Low
- **Verification**: 目录存在

### Task 1.5: 更新 mkdocs.yml 添加 i18n 插件配置

- **Type**: Configuration
- **Files**: `mkdocs.yml`
- **Description**:
  - 添加 `i18n` 插件配置
  - 配置 8 种语言
  - 配置 `default_language: en`
  - 添加 `extra.alternate` 语言切换器配置
- **Dependencies**: Task 1.2, Task 1.3
- **Est. Complexity**: Medium
- **Verification**: `uv run mkdocs build` 成功

### Task 1.6: 添加中文导航翻译映射

- **Type**: Configuration
- **Files**: `mkdocs.yml`
- **Description**: 在 `nav_translations.zh` 中添加所有导航项的中文翻译
- **Dependencies**: Task 1.5
- **Est. Complexity**: Low
- **Verification**: 构建后中文导航显示正确

### Task 1.7: 添加日文导航翻译映射 [P]

- **Type**: Configuration
- **Files**: `mkdocs.yml`
- **Description**: 在 `nav_translations.ja` 中添加所有导航项的日文翻译
- **Dependencies**: Task 1.5
- **Est. Complexity**: Low
- **Verification**: 构建后日文导航显示正确

### Task 1.8: 添加韩文导航翻译映射 [P]

- **Type**: Configuration
- **Files**: `mkdocs.yml`
- **Description**: 在 `nav_translations.ko` 中添加所有导航项的韩文翻译
- **Dependencies**: Task 1.5
- **Est. Complexity**: Low
- **Verification**: 构建后韩文导航显示正确

### Task 1.9: 添加其他语言导航翻译映射 [P]

- **Type**: Configuration
- **Files**: `mkdocs.yml`
- **Description**: 添加 es, fr, de, pt-BR 的导航翻译映射
- **Dependencies**: Task 1.5
- **Est. Complexity**: Low
- **Verification**: 构建后各语言导航显示正确

### Task 1.10: 验证本地构建成功

- **Type**: Verification
- **Files**: None (验证任务)
- **Description**: 执行 `uv run mkdocs build` 验证所有配置正确
- **Dependencies**: Task 1.6, Task 1.7, Task 1.8, Task 1.9
- **Est. Complexity**: Low
- **Verification**: 构建成功，无错误

---

## Phase 2: Core Implementation (核心功能)

### Task 2.1: 编写术语表验证测试 (TDD)

- **Type**: Testing
- **Files**: `tests/test_i18n_glossary.py`
- **Description**: 编写术语表配置文件的验证测试，定义：
  - 有效的 YAML 结构要求
  - 必需字段 (keep_english, translations, rules)
  - 翻译映射的完整性检查
  - 规则模式的合法性验证
- **Dependencies**: Task 1.4
- **Est. Complexity**: Low
- **Verification**: 测试文件创建完成，测试用例定义清晰

### Task 2.2: 创建术语表配置文件 glossary.yml

- **Type**: Configuration
- **Files**: `.codexspec/i18n/glossary.yml`
- **Description**: 创建完整的术语表配置，满足 Task 2.1 定义的测试要求，包含：
  - `keep_english` 列表
  - `translations` 多语言映射
  - `rules` 智能判断规则
- **Dependencies**: Task 2.1
- **Est. Complexity**: Medium
- **Verification**: `uv run pytest tests/test_i18n_glossary.py` 通过

### Task 2.3: 创建翻译斜杠命令模板 translate-docs.md

- **Type**: Implementation
- **Files**: `templates/commands/translate-docs.md`
- **Description**: 创建 Claude Code 斜杠命令模板，包含：
  - YAML frontmatter (description, argument-hint, allowed-tools)
  - 语言偏好检查
  - 术语表加载指令
  - 翻译执行步骤
  - 输出格式规范
- **Dependencies**: Task 2.2
- **Est. Complexity**: Medium
- **Verification**: 命令模板符合 CodexSpec 规范

### Task 2.4: 手动执行翻译 - 生成中文文档

- **Type**: Execution
- **Files**: `docs/zh/` (所有文件)
- **Description**: 使用 `/codexspec.translate-docs --lang zh` 生成中文翻译
- **Dependencies**: Task 2.3, Task 1.10
- **Est. Complexity**: Medium
- **Verification**: 中文文档生成，内容正确

### Task 2.5: 手动执行翻译 - 生成日文文档 [P]

- **Type**: Execution
- **Files**: `docs/ja/` (所有文件)
- **Description**: 使用 `/codexspec.translate-docs --lang ja` 生成日文翻译
- **Dependencies**: Task 2.3, Task 1.10
- **Est. Complexity**: Medium
- **Verification**: 日文文档生成，内容正确

### Task 2.6: 手动执行翻译 - 生成韩文文档 [P]

- **Type**: Execution
- **Files**: `docs/ko/` (所有文件)
- **Description**: 使用 `/codexspec.translate-docs --lang ko` 生成韩文翻译
- **Dependencies**: Task 2.3, Task 1.10
- **Est. Complexity**: Medium
- **Verification**: 韩文文档生成，内容正确

### Task 2.7: 手动执行翻译 - 生成其他语言文档 [P]

- **Type**: Execution
- **Files**: `docs/es/`, `docs/fr/`, `docs/de/`, `docs/pt-BR/` (所有文件)
- **Description**: 生成西班牙文、法文、德文、葡萄牙文翻译
- **Dependencies**: Task 2.3, Task 1.10
- **Est. Complexity**: Medium
- **Verification**: 所有语言文档生成，内容正确

### Task 2.8: 验证多语言构建成功

- **Type**: Verification
- **Files**: None (验证任务)
- **Description**: 执行 `uv run mkdocs build` 验证所有语言版本构建成功
- **Dependencies**: Task 2.4, Task 2.5, Task 2.6, Task 2.7
- **Est. Complexity**: Low
- **Verification**: 构建成功，8 种语言站点正常

---

## Phase 3: Automation (自动化)

### Task 3.1: 创建 CI 工作流文件 docs-i18n.yml

- **Type**: Implementation
- **Files**: `.github/workflows/docs-i18n.yml`
- **Description**: 创建 GitHub Actions 工作流基础结构
- **Dependencies**: Task 2.8
- **Est. Complexity**: Medium
- **Verification**: 工作流语法正确

### Task 3.2: 配置工作流触发条件

- **Type**: Configuration
- **Files**: `.github/workflows/docs-i18n.yml`
- **Description**: 配置 `on.push.paths` 和 `on.workflow_dispatch`
- **Dependencies**: Task 3.1
- **Est. Complexity**: Low
- **Verification**: 触发条件正确

### Task 3.3: 配置并行翻译任务 (matrix strategy)

- **Type**: Configuration
- **Files**: `.github/workflows/docs-i18n.yml`
- **Description**: 配置 matrix 策略并行执行 7 种语言翻译
- **Dependencies**: Task 3.2
- **Est. Complexity**: Medium
- **Verification**: matrix 配置正确

### Task 3.4: 配置 Claude Code Action 集成

- **Type**: Configuration
- **Files**: `.github/workflows/docs-i18n.yml`
- **Description**: 配置 `anthropics/claude-code-action` 步骤
- **Dependencies**: Task 3.3
- **Est. Complexity**: Medium
- **Verification**: Action 配置正确

### Task 3.5: 实现翻译结果提交逻辑

- **Type**: Configuration
- **Files**: `.github/workflows/docs-i18n.yml`
- **Description**: 配置 git commit 和 push 步骤
- **Dependencies**: Task 3.4
- **Est. Complexity**: Low
- **Verification**: 提交逻辑正确

### Task 3.6: 添加工作流手动触发支持

- **Type**: Configuration
- **Files**: `.github/workflows/docs-i18n.yml`
- **Description**: 添加 `workflow_dispatch` 输入参数支持指定语言
- **Dependencies**: Task 3.5
- **Est. Complexity**: Low
- **Verification**: 手动触发可用

---

## Phase 4: Quality Assurance (质量保证)

### Task 4.1: 编写结构检查脚本测试 (TDD) [P]

- **Type**: Testing
- **Files**: `tests/scripts/bash/test_check_i18n_structure.py`
- **Description**: 编写结构检查脚本的测试用例，定义：
  - 正确结构的测试场景
  - 缺少文件的测试场景
  - 多余文件的测试场景
  - 目录结构不一致的测试场景
- **Dependencies**: Task 2.8
- **Est. Complexity**: Medium
- **Verification**: 测试文件创建完成，测试用例定义清晰

### Task 4.2: 编写完整性检查脚本测试 (TDD) [P]

- **Type**: Testing
- **Files**: `tests/scripts/bash/test_check_i18n_completeness.py`
- **Description**: 编写完整性检查脚本的测试用例，定义：
  - 完全翻译的测试场景
  - 部分未翻译的测试场景
  - 遗留英文段落的测试场景
  - 边界情况测试
- **Dependencies**: Task 2.8
- **Est. Complexity**: Medium
- **Verification**: 测试文件创建完成，测试用例定义清晰

### Task 4.3: 创建结构一致性检查脚本

- **Type**: Implementation
- **Files**: `scripts/bash/check-i18n-structure.sh`
- **Description**: 创建 bash 脚本满足 Task 4.1 定义的测试，检查所有语言版本的页面数量和目录结构一致
- **Dependencies**: Task 4.1
- **Est. Complexity**: Medium
- **Verification**: `uv run pytest tests/scripts/bash/test_check_i18n_structure.py` 通过

### Task 4.4: 创建完整性检查脚本

- **Type**: Implementation
- **Files**: `scripts/bash/check-i18n-completeness.sh`
- **Description**: 创建 bash 脚本满足 Task 4.2 定义的测试，检测未翻译的段落（遗留的英文）
- **Dependencies**: Task 4.2
- **Est. Complexity**: Medium
- **Verification**: `uv run pytest tests/scripts/bash/test_check_i18n_completeness.py` 通过

### Task 4.5: 创建语义一致性检查斜杠命令

- **Type**: Implementation
- **Files**: `templates/commands/check-i18n-semantics.md`
- **Description**: 创建斜杠命令使用 AI 比对翻译内容与原文的语义一致性
- **Dependencies**: Task 2.8
- **Est. Complexity**: Medium
- **Verification**: 命令模板符合规范

### Task 4.6: 集成质量检查到 CI 工作流

- **Type**: Configuration
- **Files**: `.github/workflows/docs-i18n.yml`
- **Description**: 在翻译步骤后添加质量检查步骤
- **Dependencies**: Task 4.3, Task 4.4, Task 3.6
- **Est. Complexity**: Medium
- **Verification**: 质量检查在 CI 中执行

### Task 4.7: 实现检查报告生成

- **Type**: Configuration
- **Files**: `.github/workflows/docs-i18n.yml`
- **Description**: 配置检查失败时生成 GitHub Issue 或 PR 评论
- **Dependencies**: Task 4.6
- **Est. Complexity**: Medium
- **Verification**: 报告生成正确

### Task 4.8: 配置部署阻止条件

- **Type**: Configuration
- **Files**: `.github/workflows/docs-i18n.yml`
- **Description**: 配置质量检查失败时阻止部署
- **Dependencies**: Task 4.7
- **Est. Complexity**: Low
- **Verification**: 阻止条件生效

---

## Phase 5: Documentation & Final Verification (文档与最终验证)

### Task 5.1: 更新英文用户文档 - i18n 章节

- **Type**: Documentation
- **Files**: `docs/en/user-guide/i18n.md`
- **Description**: 添加多语言文档使用说明
- **Dependencies**: Task 2.8
- **Est. Complexity**: Medium
- **Verification**: 文档内容完整

### Task 5.2: 更新 README 添加多语言文档链接

- **Type**: Documentation
- **Files**: `README.md`, `README.zh-CN.md`, `README.ja.md`, `README.ko.md`, 等
- **Description**: 在各语言 README 中添加对应语言文档链接
- **Dependencies**: Task 2.8
- **Est. Complexity**: Low
- **Verification**: 链接正确

### Task 5.3: 翻译用户文档到所有目标语言 [P]

- **Type**: Documentation
- **Files**: `docs/*/user-guide/i18n.md` (所有语言)
- **Description**: 翻译 i18n 章节到 7 种目标语言
- **Dependencies**: Task 5.1
- **Est. Complexity**: Medium
- **Verification**: 所有语言文档完整

### Task 5.4: 验证部署和语言切换功能

- **Type**: Verification
- **Files**: None (E2E 验证)
- **Description**:
  - 部署到 GitHub Pages
  - 验证浏览器语言自动检测
  - 验证语言切换器功能
  - 验证 URL 路由正确
- **Dependencies**: Task 5.3, Task 4.8
- **Est. Complexity**: Medium
- **Verification**: 所有功能正常

---

## Execution Order

```
Phase 1: Foundation
├── Task 1.1 ──► Task 1.2 ──► Task 1.3 [P]
│               │
│               └──► Task 1.4 [P]
│
├── Task 1.5 (depends on 1.2, 1.3)
│   │
│   ├──► Task 1.6 ──┐
│   ├──► Task 1.7 [P]──┼──► Task 1.10
│   ├──► Task 1.8 [P]──┤
│   └──► Task 1.9 [P]──┘

Phase 2: Core (TDD)
├── Task 1.4 ──► Task 2.1 (测试) ──► Task 2.2 (实现)
│                                   │
│                                   ▼
│                               Task 2.3
│                                   │
│   ┌───────────────────────────────┼───────────────────────┐
│   │                               │                       │
│   ├──► Task 2.4                   ├──► Task 2.5 [P]       ├──► Task 2.6 [P]
│   │                               │                       │
│   └──► Task 2.7 [P] ──────────────┴───────────────────────┘
│                                       │
│                                       ▼
│                                   Task 2.8

Phase 3: Automation
└── Task 2.8 ──► Task 3.1 ──► Task 3.2 ──► Task 3.3 ──► Task 3.4
                                            │
                                            ▼
                                        Task 3.5 ──► Task 3.6

Phase 4: Quality (TDD)
├── Task 2.8 ──► Task 4.1 (测试) [P]
│               │
│               ├──► Task 4.2 (测试) [P]
│               │
│               └──► Task 4.5 (命令模板)
│
├── Task 4.1 ──► Task 4.3 (实现)
│
├── Task 4.2 ──► Task 4.4 (实现)
│
├── Task 4.3, Task 4.4, Task 3.6 ──► Task 4.6 ──► Task 4.7 ──► Task 4.8

Phase 5: Docs & Final Verification
├── Task 2.8 ──► Task 5.1 ──► Task 5.3 [P]
│               │
│               └──► Task 5.2 [P]
│
└── Task 5.3 + Task 4.8 ──► Task 5.4
```

## Checkpoints

- [ ] **Checkpoint 1**: After Phase 1 - 本地构建成功，8 种语言配置完成
- [ ] **Checkpoint 2**: After Phase 2 - 所有语言翻译生成，多语言构建成功，术语表测试通过
- [ ] **Checkpoint 3**: After Phase 3 - CI 工作流可手动触发，自动翻译正常
- [ ] **Checkpoint 4**: After Phase 4 - 质量检查集成，所有脚本测试通过，部署保护生效
- [ ] **Checkpoint 5**: After Phase 5 - 文档完整，部署验证成功

## Task Summary by Type

| Type | Count | Tasks |
|------|-------|-------|
| Setup | 4 | 1.1, 1.2, 1.3, 1.4 |
| Configuration | 13 | 1.5-1.9, 3.2-3.6, 4.6-4.8 |
| Implementation | 5 | 2.3, 3.1, 4.3, 4.4, 4.5 |
| Execution | 4 | 2.4-2.7 |
| Testing | 3 | 2.1, 4.1, 4.2 |
| Documentation | 3 | 5.1-5.3 |
| Verification | 3 | 1.10, 2.8, 5.4 |

## TDD Compliance Summary

| Component | Test Task | Implementation Task | Compliance |
|-----------|-----------|---------------------|------------|
| 术语表配置 | Task 2.1 | Task 2.2 | ✅ Test First |
| 结构检查脚本 | Task 4.1 | Task 4.3 | ✅ Test First |
| 完整性检查脚本 | Task 4.2 | Task 4.4 | ✅ Test First |

---

*Generated by CodexSpec on 2026-03-04*
*Updated for TDD Compliance - Test tasks precede implementation tasks*

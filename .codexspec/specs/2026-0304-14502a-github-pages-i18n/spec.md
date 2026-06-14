# Feature: GitHub Pages 文档多语言支持

## Overview

为 CodexSpec 的 GitHub Pages 文档网站添加多语言国际化支持，使其能够以 8 种语言向全球用户提供文档。系统将基于 MkDocs i18n 插件实现自动语言切换、AI 辅助翻译和 CI 自动化工作流。

## Goals

- **提升全球用户体验**：用户可以以其母语阅读文档，通过浏览器自动检测或手动切换访问 8 种语言版本
- **自动化翻译流程**：通过 Claude Code 斜杠命令实现 AI 辅助翻译，减少手动翻译工作量
- **保持内容一致性**：CI 自动检查各语言版本的完整性和语义一致性，确保翻译质量
- **降低维护成本**：英文文档更新后自动触发翻译流程，减少人工介入

> **衡量方式**：通过用户故事中的验收标准（Acceptance Criteria）和测试用例验证功能完成度。非功能需求（NFR）中的技术指标（如性能、兼容性）用于验证系统质量。

## Target Languages

| 语言 | 代码 | URL 路径 |
|------|------|----------|
| English | `en` | `/en/` |
| 中文简体 | `zh` | `/zh/` |
| 日本語 | `ja` | `/ja/` |
| 한국어 | `ko` | `/ko/` |
| Español | `es` | `/es/` |
| Français | `fr` | `/fr/` |
| Deutsch | `de` | `/de/` |
| Português | `pt-BR` | `/pt-BR/` |

## User Stories

### Story 1: 访问多语文档

**As a** 非英语母语的用户
**I want** 访问以我母语编写的文档
**So that** 我能更轻松地理解和使用 CodexSpec

**Acceptance Criteria:**

- [ ] 访问网站时自动检测浏览器语言并重定向到对应语言版本
- [ ] 用户可通过语言切换器手动选择语言
- [ ] 所有 8 种语言的文档内容完整可用
- [ ] URL 结构清晰（`/en/`, `/zh/`, `/ja/` 等）

### Story 2: 翻译文档

**As a** 项目维护者
**I want** 通过一个简单的斜杠命令翻译所有文档
**So that** 我能高效地维护多语言文档

**Acceptance Criteria:**

- [ ] `/codexspec.translate-docs` 命令可用于翻译文档
- [ ] 命令自动检测需要翻译的文件
- [ ] 翻译结果保存到正确的语言目录
- [ ] 翻译过程中提供进度反馈

### Story 3: 自动化翻译流程

**As a** 项目维护者
**I want** 当英文文档更新时自动触发翻译
**So that** 所有语言版本保持同步

**Acceptance Criteria:**

- [ ] CI 检测到 `docs/en/` 目录变更时触发翻译
- [ ] 翻译任务并行执行以提高效率
- [ ] 翻译失败时有明确的错误提示
- [ ] 翻译完成后自动创建 PR 或直接提交

### Story 4: 验证翻译质量

**As a** 项目维护者
**I want** 自动检查翻译的一致性和完整性
**So that** 确保所有语言版本的文档质量

**Acceptance Criteria:**

- [ ] 结构检查：验证所有语言版本的页面数量和目录结构一致
- [ ] 完整性检查：检测未翻译的段落（如遗留的英文）
- [ ] 语义检查：使用 AI 比对翻译内容与原文的语义一致性
- [ ] 检查失败时阻止部署并报告问题

## Functional Requirements

### REQ-001: MkDocs i18n 插件配置

- [REQ-001.1] 安装并配置 `mkdocs-i18n` 插件
- [REQ-001.2] 配置 8 种语言支持
- [REQ-001.3] 设置 URL 结构为全部子目录模式（所有语言在 `/xx/` 下）
- [REQ-001.4] 配置浏览器语言自动检测和重定向

### REQ-002: 文档目录结构重组

- [REQ-002.1] 将现有 `docs/` 内容移动到 `docs/en/`
- [REQ-002.2] 创建其他 7 种语言的目录（`docs/zh/`, `docs/ja/` 等）
- [REQ-002.3] 更新 `mkdocs.yml` 中的导航配置以支持多语言

### REQ-003: 翻译斜杠命令

- [REQ-003.1] 创建 `/codexspec.translate-docs` 斜杠命令模板
- [REQ-003.2] 命令支持指定目标语言（默认全部）
- [REQ-003.3] 命令支持增量翻译（仅翻译变更的文件）
- [REQ-003.4] 翻译时保留 Markdown 格式和代码块

### REQ-004: CI 自动化工作流

- [REQ-004.1] 创建 GitHub Actions 工作流文件 `.github/workflows/docs-i18n.yml`
- [REQ-004.2] 监听 `docs/en/` 目录的变更触发翻译
- [REQ-004.3] 使用 `claude code -p` 执行翻译任务
- [REQ-004.4] 并行执行多语言翻译以提高效率

### REQ-005: 翻译质量检查

- [REQ-005.1] 实现结构一致性检查（页面数量、目录结构）
- [REQ-005.2] 实现完整性检查（检测未翻译内容）
- [REQ-005.3] 实现语义一致性检查（AI 比对）
- [REQ-005.4] 生成检查报告，包含问题详情和建议

### REQ-006: 语言切换器

- [REQ-006.1] 在导航栏显示语言切换器
- [REQ-006.2] 切换器显示所有 8 种语言选项
- [REQ-006.3] 当前语言高亮显示
- [REQ-006.4] 切换时保持当前页面位置（相同页面的不同语言版本）

## Non-Functional Requirements

### NFR-001: 性能

- [NFR-001.1] 单个文件翻译时间不超过 30 秒
- [NFR-001.2] 完整翻译所有文档（8 种语言）不超过 15 分钟
- [NFR-001.3] 网站加载时间不受 i18n 插件显著影响（增量不超过 10%）

### NFR-002: 可维护性

- [NFR-002.1] 翻译命令模板遵循现有 CodexSpec 模板规范
- [NFR-002.2] CI 工作流配置清晰、有注释
- [NFR-002.3] 新增语言只需修改配置，无需修改代码

### NFR-003: 兼容性

- [NFR-003.1] 与现有 MkDocs Material 主题功能完全兼容
- [NFR-003.2] 与现有搜索功能兼容（支持多语言搜索）
- [NFR-003.3] 与现有 `mkdocstrings` 插件兼容

### NFR-004: 用户体验

- [NFR-004.1] 语言切换响应即时，无需页面刷新
- [NFR-004.2] 浏览器语言检测准确率 > 95%
- [NFR-004.3] 翻译质量通过 AI 语义检查评分 ≥ 80/100
- [NFR-004.4] 术语表中的技术术语翻译一致性 = 100%
- [NFR-004.5] 代码块、命令、路径等技术内容保持原样（不被翻译）

## Acceptance Criteria (Test Cases)

### TC-001: 浏览器语言自动检测

**前置条件：** 浏览器语言设置为中文
**步骤：**

1. 访问 `https://zts0hg.github.io/codexspec/`
**预期结果：** 自动重定向到 `https://zts0hg.github.io/codexspec/zh/`

### TC-002: 语言切换器功能

**前置条件：** 用户在英文文档页面
**步骤：**

1. 点击语言切换器
2. 选择 "中文简体"
**预期结果：** 页面切换到对应的中文版本，URL 更新为 `/zh/` 路径

### TC-003: 翻译命令执行

**前置条件：** 项目已初始化，`docs/en/` 有内容
**步骤：**

1. 在 Claude Code 中执行 `/codexspec.translate-docs --lang zh`
**预期结果：** 生成 `docs/zh/` 目录，内容为中文翻译

### TC-004: CI 翻译触发

**前置条件：** CI 工作流已配置
**步骤：**

1. 修改 `docs/en/index.md`
2. 推送到 main 分支
**预期结果：** CI 自动触发翻译，更新其他语言版本

### TC-005: 结构一致性检查

**前置条件：** 存在 `docs/en/` 和 `docs/zh/`
**步骤：**

1. 删除 `docs/zh/user-guide/workflow.md`
2. 运行一致性检查
**预期结果：** 检查失败，报告缺少的文件

### TC-006: 完整性检查

**前置条件：** 存在翻译文档
**步骤：**

1. 在 `docs/zh/index.md` 中保留一段英文未翻译
2. 运行完整性检查
**预期结果：** 检测到未翻译段落并报告

### TC-007: 语义一致性检查

**前置条件：** 存在原文和翻译
**步骤：**

1. 运行语义检查
**预期结果：** AI 比对翻译内容与原文，报告语义偏差

## Edge Cases

### EC-001: 代码块和命令

**问题：** 代码块中的命令、路径不应被翻译
**处理方式：** 翻译时识别并保留代码块（`` ``` ``）和行内代码（`` ` ``）内容

### EC-002: 技术术语

**问题：** 某些术语（如 "CLI", "TDD", "Constitution"）可能需要保留英文
**处理方式：**

- 术语表列出核心技术术语的翻译规则（保留英文或指定翻译）
- AI 翻译时参考术语表，但同时根据上下文智能判断
- 术语表采用"建议性"而非"限制性"原则，允许 AI 对未列出术语做出合理判断

### EC-003: 链接引用

**问题：** 文档间链接需要正确指向对应语言版本
**处理方式：** 使用相对链接，MkDocs i18n 插件自动处理跨语言链接

### EC-004: 图片资源

**问题：** 图片通常不需要翻译，但包含文字的图片可能需要
**处理方式：** 共享图片放在 `docs/assets/`，语言特定图片放在 `docs/{lang}/assets/`

### EC-005: 新语言添加

**问题：** 未来可能需要添加新语言
**处理方式：** 只需在 `mkdocs.yml` 添加语言配置，运行翻译命令即可

### EC-006: 翻译失败恢复

**问题：** 某个语言翻译失败不应影响其他语言
**处理方式：** CI 中每个语言翻译独立执行，失败仅影响该语言

## Output Examples

### mkdocs.yml 配置示例

```yaml
site_name: CodexSpec
site_url: https://zts0hg.github.io/codexspec/

theme:
  name: material

plugins:
  - i18n:
      default_language: en
      languages:
        en: English
        zh: 中文简体
        ja: 日本語
        ko: 한국어
        es: Español
        fr: Français
        de: Deutsch
        pt-BR: Português (Brasil)
      nav_translations:
        zh:
          Getting Started: 快速开始
          User Guide: 用户指南
          # ...

nav:
  - Home: index.md
  - Getting Started:
    - Installation: getting-started/installation.md
    # ...
```

### 翻译命令输出示例

```
$ /codexspec.translate-docs --lang zh,ja

🌐 CodexSpec 文档翻译

📁 源目录: docs/en/
🎯 目标语言: zh, ja
📄 文件数量: 12

[1/24] 翻译 index.md → zh ... ✅ 完成 (2.3s)
[2/24] 翻译 index.md → ja ... ✅ 完成 (2.5s)
[3/24] 翻译 getting-started/installation.md → zh ... ✅ 完成 (1.8s)
...

✅ 翻译完成
📊 统计: 24 个文件，0 个错误
⏱️ 总耗时: 45.2 秒
```

### CI 工作流示例

```yaml
name: Docs i18n

on:
  push:
    paths:
      - 'docs/en/**'
  workflow_dispatch:

jobs:
  translate:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        lang: [zh, ja, ko, es, fr, de, pt-BR]
    steps:
      - uses: anthropics/claude-code-action@v1
        with:
          prompt: |
            Translate docs from English to ${{ matrix.lang }}
            Source: docs/en/
            Target: docs/${{ matrix.lang }}/
```

## Appendix A: Terminology Glossary (术语表)

术语表定义翻译时技术术语的处理规则。术语表采用**扩展性设计**：

- **核心术语**：列出必须保留英文或指定翻译的术语
- **智能扩展**：AI 在翻译时根据上下文智能判断未列出术语的处理方式
- **持续更新**：术语表可在技术规划阶段补充完善

### A.1 保留英文的术语（不翻译）

| 类别 | 术语 | 说明 |
|------|------|------|
| 工具名称 | `uv`, `pip`, `pytest`, `ruff`, `MkDocs` | 包管理器、测试框架、工具名 |
| 文件格式 | `JSON`, `YAML`, `TOML`, `Markdown` | 配置和文档格式 |
| 代码相关 | `CLI`, `API`, `SDK`, `TDD` | 软件开发术语 |
| 协议标准 | `HTTP`, `REST`, `OAuth`, `JWT` | 网络和安全协议 |
| 平台服务 | `GitHub`, `GitHub Actions`, `PyPI` | 平台和服务名称 |
| 文件路径 | `spec.md`, `plan.md`, `tasks.md`, `CLAUDE.md` | 项目特定文件名 |
| 命令 | `codexspec init`, `/codexspec.specify` | CLI 命令和斜杠命令 |

### A.2 建议翻译的术语

| 英文 | 中文 | 日文 | 韩文 | 说明 |
|------|------|------|------|------|
| Constitution | 项目宪法 | プロジェクト憲法 | 프로젝트 헌법 | 核心概念，建议统一翻译 |
| Specification | 规格文档 | 仕様書 | 명세서 | 可根据上下文调整 |
| Task | 任务 | タスク | 태스크 | 建议翻译 |
| Workflow | 工作流 | ワークフロー | 워크플로우 | 建议翻译 |
| Repository | 仓库 | リポジトリ | 리포지토리 | 建议翻译 |

### A.3 根据上下文判断的术语

以下术语由 AI 根据上下文智能判断是否翻译：

- **技术概念**：`architecture`, `module`, `component`, `interface`
- **开发流程**：`review`, `deploy`, `merge`, `commit`
- **质量相关**：`test`, `coverage`, `validation`

**判断原则**：

1. 出现在代码块或命令中 → 保持英文
2. 作为专有名词或品牌名 → 保持英文
3. 作为普通名词描述 → 可翻译
4. 技术术语首次出现时可保留英文并附翻译

### A.4 术语表配置文件

术语表将在技术规划阶段实现为配置文件（如 `.codexspec/i18n/glossary.yml`），支持：

```yaml
# 术语表配置示例
version: "1.0"

# 保留英文的术语
keep_english:
  - uv
  - pip
  - CLI
  - API
  # ... 可扩展

# 指定翻译的术语
translations:
  Constitution:
    zh: 项目宪法
    ja: プロジェクト憲法
    ko: 프로젝트 헌법
  # ... 可扩展

# AI 智能判断规则
rules:
  - pattern: "^[A-Z]{2,}$"  # 全大写缩写通常保留
    action: keep
  - pattern: "^/[a-z-]+"    # 斜杠命令保留
    action: keep
```

## Out of Scope

- **社区翻译平台集成**：不集成 Crowdin、Transifex 等外部翻译平台
- **实时机器翻译**：不提供网站前端的实时翻译功能
- **部分页面翻译**：不支持只翻译部分页面，必须翻译全部内容
- **翻译记忆库**：不实现翻译记忆库功能
- **术语库管理界面**：不提供 GUI 术语管理，术语表通过配置文件维护
- **多语言搜索优化**：暂不优化跨语言搜索功能

## Dependencies

- `mkdocs-i18n` 插件
- Claude Code CLI（用于 AI 翻译）
- GitHub Actions（用于 CI 自动化）

## Risks and Mitigations

| 风险 | 影响 | 缓解措施 |
|------|------|----------|
| AI 翻译质量不稳定 | 中 | 实现语义检查，人工审核关键页面 |
| CI 执行时间过长 | 低 | 并行执行翻译任务，增量翻译 |
| 语言切换器 UI 问题 | 低 | 使用 MkDocs Material 内置支持 |
| 翻译成本（API 调用） | 低 | 使用增量翻译，避免重复翻译 |

## Timeline Estimate

- **Phase 1**：MkDocs 配置和目录重组（基础架构）
- **Phase 2**：翻译斜杠命令实现（核心功能）
- **Phase 3**：CI 自动化工作流（自动化）
- **Phase 4**：质量检查功能（质量保证）

---

*Generated by CodexSpec on 2026-03-04*
*Updated: 2026-03-04 - Fixed SPEC-001, SPEC-002, SPEC-003*

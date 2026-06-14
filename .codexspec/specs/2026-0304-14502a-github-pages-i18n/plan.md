# Implementation Plan: GitHub Pages 文档多语言支持

## 1. Tech Stack

| Category | Technology | Version | Notes |
|----------|------------|---------|-------|
| Language | Python | 3.11+ | 现有项目语言 |
| Documentation | MkDocs | >=1.5.0 | 现有文档框架 |
| Theme | MkDocs Material | >=9.5.0 | 现有主题 |
| i18n Plugin | mkdocs-i18n | >=0.4.0 | 新增依赖 |
| CI/CD | GitHub Actions | N/A | 现有 CI 平台 |
| Translation | Claude Code CLI | Latest | AI 翻译引擎 |

### 依赖更新

```toml
# pyproject.toml 新增
[project.optional-dependencies]
docs = [
    "mkdocs>=1.5.0",
    "mkdocs-material>=9.5.0",
    "mkdocstrings[python]>=0.24.0",
    "mkdocs-i18n>=0.4.0",  # 新增
]
```

## 2. Constitutionality Review

| Principle | Compliance | Notes |
|-----------|------------|-------|
| Code Quality | ✅ | 翻译命令模板遵循现有 CodexSpec 模板规范（YAML frontmatter + Markdown） |
| Testing Standards | ✅ | 计划包含单元测试和集成测试；CI 包含翻译质量检查 |
| Documentation | ✅ | 新增 i18n 用户文档；更新 README 多语言链接 |
| Architecture | ✅ | 可扩展设计：新增语言只需配置，无需代码修改 |
| Performance | ✅ | 并行翻译执行；增量翻译支持；性能指标监控 |
| Security | ✅ | 无敏感数据处理；API 密钥通过 GitHub Secrets 管理 |
| Maintainability | ✅ | 配置驱动；术语表独立维护；CI 自动化 |
| Clarity | ✅ | 代码注释完整；配置文件有详细说明 |
| Stability | ✅ | 翻译失败不影响其他语言；回滚机制 |

## 3. Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        GitHub Pages i18n Architecture                        │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌─────────────┐     ┌─────────────────────────────────────────────────┐   │
│  │   docs/en/  │     │              Translation Pipeline                │   │
│  │  (Source)   │────▶│  ┌─────────────┐    ┌─────────────┐              │   │
│  └─────────────┘     │  │  /translate │───▶│ Claude Code │              │   │
│         │            │  │    -docs    │    │     CLI     │              │   │
│         │            │  └─────────────┘    └──────┬──────┘              │   │
│         │            │                            │                      │   │
│         │            │                            ▼                      │   │
│         │            │  ┌──────────────────────────────────────────┐   │   │
│         │            │  │     Target Language Directories          │   │   │
│         │            │  │  ┌────┐ ┌────┐ ┌────┐ ┌────┐ ┌────┐     │   │   │
│         │            │  │  │ zh │ │ ja │ │ ko │ │ es │ │...│      │   │   │
│         │            │  │  └────┘ └────┘ └────┘ └────┘ └────┘     │   │   │
│         │            │  └──────────────────────────────────────────┘   │   │
│         │            └─────────────────────────────────────────────────┘   │
│         │                                                                   │
│         ▼                                                                   │
│  ┌─────────────────────────────────────────────────────────────────────┐  │
│  │                         Quality Checks                               │  │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐              │  │
│  │  │  Structure   │  │ Completeness │  │   Semantic   │              │  │
│  │  │    Check     │  │    Check     │  │    Check     │              │  │
│  │  └──────────────┘  └──────────────┘  └──────────────┘              │  │
│  └─────────────────────────────────────────────────────────────────────┘  │
│         │                                                                   │
│         ▼                                                                   │
│  ┌─────────────────────────────────────────────────────────────────────┐  │
│  │                      MkDocs Build & Deploy                           │  │
│  │  ┌─────────────────────────────────────────────────────────────┐   │  │
│  │  │                    mkdocs-i18n Plugin                        │   │  │
│  │  │  • Language switcher                                        │   │  │
│  │  │  • Browser language detection                               │   │  │
│  │  │  • URL routing (/en/, /zh/, /ja/, ...)                      │   │  │
│  │  └─────────────────────────────────────────────────────────────┘   │  │
│  └─────────────────────────────────────────────────────────────────────┘  │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

## 4. Component Structure

### 文件结构变更

```
codexspec/
├── docs/
│   ├── en/                          # 英文（源语言）
│   │   ├── index.md
│   │   ├── getting-started/
│   │   │   ├── installation.md
│   │   │   └── quick-start.md
│   │   ├── user-guide/
│   │   │   ├── workflow.md
│   │   │   ├── commands.md
│   │   │   └── i18n.md
│   │   ├── case-studies/
│   │   ├── reference/
│   │   ├── development/
│   │   └── assets/
│   │       └── stylesheets/
│   │           └── extra.css
│   ├── zh/                          # 中文（翻译）
│   ├── ja/                          # 日文（翻译）
│   ├── ko/                          # 韩文（翻译）
│   ├── es/                          # 西班牙文（翻译）
│   ├── fr/                          # 法文（翻译）
│   ├── de/                          # 德文（翻译）
│   └── pt-BR/                       # 葡萄牙文（翻译）
├── templates/
│   └── commands/
│       └── translate-docs.md        # 新增：翻译斜杠命令
├── .codexspec/
│   └── i18n/
│       └── glossary.yml             # 新增：术语表配置
├── .github/
│   └── workflows/
│       ├── ci.yml                   # 现有 CI
│       └── docs-i18n.yml            # 新增：翻译自动化工作流
├── mkdocs.yml                       # 更新：i18n 配置
└── pyproject.toml                   # 更新：新增依赖
```

## 5. Module Dependency Graph

```
┌─────────────────────────────────────────────────────────────────────┐
│                        User Interaction                              │
│  ┌──────────────────┐         ┌──────────────────┐                 │
│  │ /translate-docs  │         │  GitHub Push     │                 │
│  │    (Manual)      │         │   (Trigger)      │                 │
│  └────────┬─────────┘         └────────┬─────────┘                 │
└───────────┼─────────────────────────────┼───────────────────────────┘
            │                             │
            ▼                             ▼
┌─────────────────────────────────────────────────────────────────────┐
│                     Translation Layer                                │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │                    translate-docs.md                          │  │
│  │  ┌────────────┐  ┌────────────┐  ┌────────────┐             │  │
│  │  │  Glossary  │  │  Source    │  │   Claude   │             │  │
│  │  │  Config    │──│  Scanner   │──│   Code     │             │  │
│  │  │  Loader    │  │            │  │   Client   │             │  │
│  │  └────────────┘  └────────────┘  └─────┬──────┘             │  │
│  └───────────────────────────────────────────┼──────────────────┘  │
└──────────────────────────────────────────────┼─────────────────────┘
                                               │
                                               ▼
┌─────────────────────────────────────────────────────────────────────┐
│                      Quality Check Layer                             │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐             │
│  │  Structure   │  │ Completeness │  │   Semantic   │             │
│  │  Validator   │  │  Validator   │  │  Validator   │             │
│  └──────────────┘  └──────────────┘  └──────────────┘             │
└──────────────────────────────┬──────────────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────────────┐
│                       Build Layer                                    │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │                      mkdocs.yml                               │  │
│  │  ┌────────────┐  ┌────────────┐  ┌────────────┐             │  │
│  │  │  mkdocs    │  │  mkdocs-   │  │ mkdocstrings│             │  │
│  │  │  core      │──│   i18n     │──│  (existing) │             │  │
│  │  └────────────┘  └────────────┘  └────────────┘             │  │
│  └──────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────┘
```

## 6. Module Specifications

### Module 1: mkdocs.yml 配置

- **Responsibility**: 配置 MkDocs i18n 插件，定义语言支持和导航翻译
- **Dependencies**: mkdocs-i18n 插件
- **Interface**: YAML 配置文件
- **Files**: `mkdocs.yml`（修改）

### Module 2: 翻译斜杠命令 (translate-docs.md)

- **Responsibility**: 提供 Claude Code 斜杠命令，执行文档翻译
- **Dependencies**:
  - `glossary.yml`（术语表）
  - Claude Code CLI
  - 源文档目录 `docs/en/`
- **Interface**: Markdown 模板文件
- **Files**: `templates/commands/translate-docs.md`（新增）

### Module 3: 术语表配置 (glossary.yml)

- **Responsibility**: 定义技术术语的翻译规则
- **Dependencies**: 无
- **Interface**: YAML 配置文件
- **Files**: `.codexspec/i18n/glossary.yml`（新增）

### Module 4: CI 工作流 (docs-i18n.yml)

- **Responsibility**: 自动化翻译流程，监听源文档变更并触发翻译
- **Dependencies**:
  - GitHub Actions
  - Claude Code Action
  - 翻译斜杠命令
- **Interface**: YAML 工作流文件
- **Files**: `.github/workflows/docs-i18n.yml`（新增）

### Module 5: 质量检查脚本

- **Responsibility**: 验证翻译的结构一致性、完整性和语义质量
- **Dependencies**: 翻译后的文档目录
- **Interface**: CI 集成 + 命令行输出
- **Files**: 内嵌于 `docs-i18n.yml` 或独立脚本

## 7. Configuration Specifications

### 7.1 mkdocs.yml i18n 配置

```yaml
# mkdocs.yml 新增/修改部分

plugins:
  - search
  - mkdocstrings:
      handlers:
        python:
          paths: [src]
          options:
            show_source: true
            show_root_heading: true
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
      # 导航翻译
      nav_translations:
        zh:
          Home: 首页
          Getting Started: 快速开始
          Installation: 安装
          Quick Start: 快速入门
          User Guide: 用户指南
          Workflow: 工作流程
          Commands: 命令参考
          Internationalization: 国际化
          Case Studies: 案例研究
          Reference: 参考
          CLI: 命令行
          Configuration: 配置
          Development: 开发
          Contributing: 贡献指南
        ja:
          Home: ホーム
          Getting Started: はじめに
          Installation: インストール
          Quick Start: クイックスタート
          # ... 其他翻译
        ko:
          Home: 홈
          Getting Started: 시작하기
          # ... 其他翻译

# 更新 extra 配置
extra:
  alternate:
    - name: English
      link: /en/
      lang: en
    - name: 中文简体
      link: /zh/
      lang: zh
    - name: 日本語
      link: /ja/
      lang: ja
    - name: 한국어
      link: /ko/
      lang: ko
    - name: Español
      link: /es/
      lang: es
    - name: Français
      link: /fr/
      lang: fr
    - name: Deutsch
      link: /de/
      lang: de
    - name: Português (Brasil)
      link: /pt-BR/
      lang: pt-BR
```

### 7.2 术语表配置 (glossary.yml)

```yaml
# .codexspec/i18n/glossary.yml

version: "1.0"
description: "CodexSpec 文档翻译术语表"

# 保留英文的术语（不翻译）
keep_english:
  # 工具名称
  - uv
  - pip
  - pytest
  - ruff
  - MkDocs

  # 文件格式
  - JSON
  - YAML
  - TOML
  - Markdown

  # 代码相关
  - CLI
  - API
  - SDK
  - TDD

  # 协议标准
  - HTTP
  - REST
  - OAuth
  - JWT

  # 平台服务
  - GitHub
  - GitHub Actions
  - PyPI

  # 项目文件
  - spec.md
  - plan.md
  - tasks.md
  - CLAUDE.md

# 指定翻译的术语
translations:
  Constitution:
    zh: 项目宪法
    ja: プロジェクト憲法
    ko: 프로젝트 헌법
    es: Constitución del Proyecto
    fr: Constitution du Projet
    de: Projektverfassung
    pt-BR: Constituição do Projeto

  Specification:
    zh: 规格文档
    ja: 仕様書
    ko: 명세서
    es: Especificación
    fr: Spécification
    de: Spezifikation
    pt-BR: Especificação

  Task:
    zh: 任务
    ja: タスク
    ko: 태스크
    es: Tarea
    fr: Tâche
    de: Aufgabe
    pt-BR: Tarefa

  Workflow:
    zh: 工作流
    ja: ワークフロー
    ko: 워크플로우
    es: Flujo de trabajo
    fr: Flux de travail
    de: Workflow
    pt-BR: Fluxo de trabalho

  Repository:
    zh: 仓库
    ja: リポジトリ
    ko: 리포지토리
    es: Repositorio
    fr: Dépôt
    de: Repository
    pt-BR: Repositório

# AI 智能判断规则
rules:
  - pattern: "^[A-Z]{2,}$"
    description: "全大写缩写通常保留"
    action: keep
  - pattern: "^/[a-z-]+"
    description: "斜杠命令保留"
    action: keep
  - pattern: "^[a-z]+\\.[a-z]+$"
    description: "文件扩展名保留"
    action: keep
```

## 8. API Contracts (CLI Commands)

### Command: `/codexspec.translate-docs`

**Description**: 翻译文档到指定语言

**Arguments**:

- `--lang`, `-l`: 目标语言代码（逗号分隔），默认全部
- `--source`, `-s`: 源目录，默认 `docs/en/`
- `--incremental`, `-i`: 仅翻译变更的文件
- `--dry-run`, `-d`: 预览模式，不写入文件

**Options**:

```
--lang, -l      Target language(s), e.g., "zh,ja,ko"
--source, -s    Source directory (default: docs/en/)
--incremental   Only translate changed files
--dry-run       Preview without writing files
--help          Show help message
```

**Output**:

```
🌐 CodexSpec 文档翻译

📁 源目录: docs/en/
🎯 目标语言: zh, ja
📄 文件数量: 12

[1/24] 翻译 index.md → zh ... ✅ 完成 (2.3s)
[2/24] 翻译 index.md → ja ... ✅ 完成 (2.5s)
...

✅ 翻译完成
📊 统计: 24 个文件，0 个错误
⏱️ 总耗时: 45.2 秒
```

**Exit Codes**:

- `0`: 成功
- `1`: 部分失败（有错误但部分成功）
- `2`: 完全失败（所有翻译失败）

## 9. Implementation Phases

### Phase 1: Foundation (基础架构)

**目标**: 搭建 i18n 基础设施，重组文档目录

- [ ] **P1-1**: 更新 `pyproject.toml`，添加 `mkdocs-i18n` 依赖
- [ ] **P1-2**: 创建 `docs/en/` 目录，移动现有文档
- [ ] **P1-3**: 创建其他语言目录结构（`docs/zh/`, `docs/ja/`, 等）
- [ ] **P1-4**: 更新 `mkdocs.yml` 配置 i18n 插件
- [ ] **P1-5**: 配置导航翻译映射
- [ ] **P1-6**: 验证本地构建成功

### Phase 2: Core Implementation (核心功能)

**目标**: 实现翻译斜杠命令和术语表

- [ ] **P2-1**: 创建 `.codexspec/i18n/glossary.yml` 术语表配置
- [ ] **P2-2**: 创建 `templates/commands/translate-docs.md` 斜杠命令
- [ ] **P2-3**: 实现术语表加载逻辑
- [ ] **P2-4**: 实现源文件扫描逻辑
- [ ] **P2-5**: 实现翻译提示词模板（包含术语表指令）
- [ ] **P2-6**: 实现增量翻译检测
- [ ] **P2-7**: 手动执行翻译，生成初始翻译文档

### Phase 3: Automation (自动化)

**目标**: 实现 CI 自动化工作流

- [ ] **P3-1**: 创建 `.github/workflows/docs-i18n.yml` 工作流
- [ ] **P3-2**: 配置触发条件（push 到 `docs/en/`）
- [ ] **P3-3**: 配置并行翻译任务（matrix strategy）
- [ ] **P3-4**: 配置 Claude Code Action 集成
- [ ] **P3-5**: 实现翻译结果提交/PR 创建逻辑
- [ ] **P3-6**: 添加工作流手动触发支持

### Phase 4: Quality Assurance (质量保证)

**目标**: 实现翻译质量检查

- [ ] **P4-1**: 实现结构一致性检查脚本
- [ ] **P4-2**: 实现完整性检查脚本（检测未翻译内容）
- [ ] **P4-3**: 实现语义一致性检查（AI 比对）
- [ ] **P4-4**: 集成质量检查到 CI 工作流
- [ ] **P4-5**: 实现检查报告生成
- [ ] **P4-6**: 配置部署阻止条件（检查失败时不部署）

### Phase 5: Testing & Documentation (测试与文档)

**目标**: 完善测试和用户文档

- [ ] **P5-1**: 编写翻译命令单元测试
- [ ] **P5-2**: 编写 CI 工作流集成测试
- [ ] **P5-3**: 更新 `docs/en/user-guide/i18n.md` 添加多语文档说明
- [ ] **P5-4**: 更新 README 添加多语言文档链接
- [ ] **P5-5**: 翻译用户文档到所有目标语言
- [ ] **P5-6**: 验证部署和语言切换功能

## 10. Technical Decisions

### Decision 1: 选择 mkdocs-i18n 插件

- **Choice**: 使用 `mkdocs-i18n` 官方推荐插件
- **Rationale**:
  - 与 MkDocs Material 主题深度集成
  - 支持浏览器语言自动检测
  - 支持语言切换器
  - 活跃维护，社区支持好
- **Alternatives**:
  - `mkdocs-static-i18n`: 静态站点方案，灵活性较低
  - 自定义方案: 维护成本高
- **Trade-offs**: 需要按插件要求的目录结构组织文档

### Decision 2: AI 翻译而非专业翻译服务

- **Choice**: 使用 Claude Code CLI 进行 AI 翻译
- **Rationale**:
  - 成本低（相比专业翻译服务）
  - 质量高（Claude 在技术文档翻译上表现优秀）
  - 可集成到 CI/CD 流程
  - 支持上下文感知翻译
- **Alternatives**:
  - Crowdin/Transifex: 成本高，需要外部平台
  - Google Translate API: 质量较低，技术术语处理差
- **Trade-offs**: 需要实现质量检查机制确保翻译一致性

### Decision 3: 术语表配置驱动

- **Choice**: 使用 YAML 配置文件管理术语表
- **Rationale**:
  - 可版本控制
  - 易于维护和扩展
  - 支持多语言映射
  - 与翻译命令解耦
- **Alternatives**:
  - 硬编码在模板中: 难以维护
  - 外部数据库: 过于复杂
- **Trade-offs**: 需要手动维护术语表

### Decision 4: CI 并行翻译

- **Choice**: 使用 GitHub Actions matrix strategy 并行执行翻译
- **Rationale**:
  - 显著减少总翻译时间
  - 单语言失败不影响其他语言
  - 资源利用率高
- **Alternatives**:
  - 顺序执行: 时间长，效率低
- **Trade-offs**: 占用更多 GitHub Actions 并发额度

### Decision 5: 全子目录 URL 结构

- **Choice**: 所有语言使用子目录 URL（`/en/`, `/zh/`, 等）
- **Rationale**:
  - 结构清晰，易于理解
  - 便于 CDN 缓存
  - 支持语言切换时保持页面位置
- **Alternatives**:
  - 默认语言在根路径: 重定向逻辑复杂
  - 子域名: DNS 配置复杂
- **Trade-offs**: URL 略长

## 11. Risk Mitigation

| Risk | Mitigation |
|------|------------|
| AI 翻译质量不稳定 | 实现三层质量检查（结构、完整性、语义）；关键页面人工审核 |
| CI 执行时间过长 | 并行翻译；增量翻译；缓存机制 |
| 术语翻译不一致 | 术语表强制约束；AI 提示词明确指令 |
| 翻译 API 成本 | 增量翻译减少重复；仅在变更时触发 |
| 新语言添加复杂 | 配置驱动设计；文档化添加流程 |

## 12. Testing Strategy

### Unit Tests

- 术语表加载测试
- 源文件扫描测试
- 增量变更检测测试

### Integration Tests

- 翻译命令执行测试
- CI 工作流触发测试
- 质量检查集成测试

### E2E Tests

- 浏览器语言检测测试
- 语言切换功能测试
- URL 路由测试

---

*Generated by CodexSpec on 2026-03-04*

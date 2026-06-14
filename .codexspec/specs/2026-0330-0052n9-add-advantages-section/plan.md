# Implementation Plan: 添加 CodexSpec 优势说明章节

## 1. Tech Stack

| Category | Technology | Notes |
|----------|------------|-------|
| Language | Markdown | 文档更新，无需编程语言 |
| i18n | LLM 动态翻译 | 复用现有翻译机制 |
| Build | MkDocs | GitHub Pages 静态站点生成 |

## 2. Constitutionality Review

| Principle | Compliance | Notes |
|-----------|------------|-------|
| Documentation | ✅ | 符合"保持文档更新"原则，增强文档价值 |
| Code Quality | ✅ | 虽然是文档，但遵循"清晰简洁"要求 |
| Architecture | ✅ | 不改变现有架构，仅在文档层面增强 |

## 3. Architecture Overview

本任务为纯文档更新，不涉及代码架构变更。

```
┌─────────────────────────────────────────────────────────────┐
│                    文档更新范围                               │
├─────────────────────────────────────────────────────────────┤
│  README 文件 (8 个)                                          │
│  ├── README.md (英文主版)                                    │
│  ├── README.zh-CN.md (中文)                                  │
│  ├── README.ja.md (日语)                                     │
│  ├── README.ko.md (韩语)                                     │
│  ├── README.es.md (西班牙语)                                 │
│  ├── README.fr.md (法语)                                     │
│  ├── README.de.md (德语)                                     │
│  └── README.pt-BR.md (葡萄牙语)                              │
├─────────────────────────────────────────────────────────────┤
│  GitHub Pages 首页 (8 个)                                    │
│  ├── docs/en/index.md                                        │
│  ├── docs/zh/index.md                                        │
│  ├── docs/ja/index.md                                        │
│  ├── docs/ko/index.md                                        │
│  ├── docs/es/index.md                                        │
│  ├── docs/fr/index.md                                        │
│  ├── docs/de/index.md                                        │
│  └── docs/pt-BR/index.md                                     │
└─────────────────────────────────────────────────────────────┘
```

## 4. Component Structure

```
codexspec/
├── README.md                    # 新增 "Why Choose CodexSpec?" 章节
├── README.zh-CN.md              # 新增 "为什么选择 CodexSpec" 章节
├── README.ja.md                 # 新增章节（日语）
├── README.ko.md                 # 新增章节（韩语）
├── README.es.md                 # 新增章节（西班牙语）
├── README.fr.md                 # 新增章节（法语）
├── README.de.md                 # 新增章节（德语）
├── README.pt-BR.md              # 新增章节（葡萄牙语）
└── docs/
    ├── en/index.md              # 增强 "Why CodexSpec?" 章节
    ├── zh/index.md              # 增强章节（中文）
    ├── ja/index.md              # 增强章节（日语）
    ├── ko/index.md              # 增强章节（韩语）
    ├── es/index.md              # 增强章节（西班牙语）
    ├── fr/index.md              # 增强章节（法语）
    ├── de/index.md              # 增强章节（德语）
    └── pt-BR/index.md           # 增强章节（葡萄牙语）
```

## 5. Module Dependency Graph

```
┌──────────────────┐
│   README.md      │  ← 主版本（英文源）
└────────┬─────────┘
         │ 内容参考
         ▼
┌──────────────────┐     ┌──────────────────┐
│ README.zh-CN.md  │ ... │ README.*.md (6)  │  ← 其他语言版本
└──────────────────┘     └──────────────────┘
         │
         │ 同步内容
         ▼
┌──────────────────┐     ┌──────────────────┐
│ docs/zh/index.md │ ... │ docs/*/index.md  │  ← GitHub Pages
└──────────────────┘     └──────────────────┘
```

## 6. Content Specifications

### 6.1 README.md 新增内容

**插入位置**: 在 `## Table of Contents` 之后、`## What is Spec-Driven Development?` 之前

**章节结构**:

```markdown
## Why Choose CodexSpec?

Why use CodexSpec on top of Claude Code? Here's the comparison:

| Aspect | Claude Code Only | CodexSpec + Claude Code |
|--------|------------------|-------------------------|
| **Multi-language Support** | Default English interaction | Configure team language for smoother collaboration and reviews |
| **Traceability** | Hard to trace decisions after session ends | All specs, plans, and tasks saved in `.codexspec/specs/` |
| **Session Recovery** | Plan mode interruptions are hard to recover from | Multi-command split + persisted docs = easy recovery |
| **Team Governance** | No unified principles, inconsistent styles | `constitution.md` enforces team standards and quality |

---

## What is Spec-Driven Development?
...
```

**Table of Contents 更新**: 新增 `- [Why Choose CodexSpec?](#why-choose-codexspec)`

### 6.2 docs/*/index.md 增强内容

**现有章节**: `## Why CodexSpec?` 已存在，需要增强为对比表格形式

**增强后结构**:

```markdown
## Why CodexSpec?

Why use CodexSpec on top of Claude Code? Here's the comparison:

| Aspect | Claude Code Only | CodexSpec + Claude Code |
|--------|------------------|-------------------------|
| **Multi-language Support** | Default English interaction | Configure team language |
| **Traceability** | Hard to trace decisions | All artifacts saved in `.codexspec/specs/` |
| **Session Recovery** | Hard to recover from interruptions | Multi-command + persisted docs |
| **Team Governance** | No unified principles | `constitution.md` enforces standards |

### Human-AI Collaboration
...
```

## 7. Implementation Phases

### Phase 1: README 英文主版更新

- [ ] 在 `README.md` 中新增 "Why Choose CodexSpec?" 章节
- [ ] 更新 Table of Contents 添加新章节链接
- [ ] 验证章节位置正确（在 "What is Spec-Driven Development?" 之前）

### Phase 2: README 中文版更新

- [ ] 在 `README.zh-CN.md` 中新增 "为什么选择 CodexSpec" 章节
- [ ] 更新 Table of Contents 添加新章节链接
- [ ] 确保内容与英文版语义一致

### Phase 3: README 其他语言版本更新

- [ ] 更新 `README.ja.md`（日语）
- [ ] 更新 `README.ko.md`（韩语）
- [ ] 更新 `README.es.md`（西班牙语）
- [ ] 更新 `README.fr.md`（法语）
- [ ] 更新 `README.de.md`（德语）
- [ ] 更新 `README.pt-BR.md`（葡萄牙语）

### Phase 4: GitHub Pages 首页更新

- [ ] 增强 `docs/en/index.md` 的 "Why CodexSpec?" 章节
- [ ] 增强 `docs/zh/index.md` 的章节
- [ ] 增强 `docs/ja/index.md` 的章节
- [ ] 增强 `docs/ko/index.md` 的章节
- [ ] 增强 `docs/es/index.md` 的章节
- [ ] 增强 `docs/fr/index.md` 的章节
- [ ] 增强 `docs/de/index.md` 的章节
- [ ] 增强 `docs/pt-BR/index.md` 的章节

### Phase 5: 验证

- [ ] 检查所有 README 文件格式正确
- [ ] 检查所有 GitHub Pages 文件格式正确
- [ ] 验证 Table of Contents 链接有效

## 8. Technical Decisions

### Decision 1: 内容风格选择

- **Choice**: 使用表格对比形式
- **Rationale**: 表格形式直观、易于对比、信息密度高
- **Alternatives**: 卡片式列表、场景化叙述
- **Trade-offs**: 表格在移动端可能需要滚动

### Decision 2: 章节位置选择

- **Choice**: 放在 "What is Spec-Driven Development?" 之前
- **Rationale**: 先回答"为什么"，再解释"是什么"，符合用户认知流程
- **Alternatives**: 放在 "Design Philosophy" 之后
- **Trade-offs**: 可能打断从 SDD 概念到设计理念的流畅性

### Decision 3: GitHub Pages 处理方式

- **Choice**: 增强现有 "Why CodexSpec?" 章节，而非新增
- **Rationale**: 避免内容重复，保持文档简洁
- **Alternatives**: 新增独立章节
- **Trade-offs**: 可能需要调整现有内容结构

## 9. Quality Checklist

### 内容质量

- [ ] 对比表格包含 4 个核心优势
- [ ] 每个优势描述具体可感知
- [ ] 语言简洁有力，无冗余

### 国际化

- [ ] 所有语言版本语义一致
- [ ] 术语翻译准确
- [ ] 保持各语言 README 风格统一

### 格式规范

- [ ] Markdown 语法正确
- [ ] Table of Contents 链接有效
- [ ] 表格格式正确

## 10. Estimated Effort

| Phase | Files | Estimated Time |
|-------|-------|----------------|
| Phase 1 | 1 | 10 min |
| Phase 2 | 1 | 10 min |
| Phase 3 | 6 | 30 min |
| Phase 4 | 8 | 40 min |
| Phase 5 | All | 10 min |
| **Total** | **16** | **~100 min** |

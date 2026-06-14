# Implementation Plan: 唯一 Spec 目录前缀方案

## 1. Tech Stack

| Category | Technology | Version | Notes |
|----------|------------|---------|-------|
| Language | Markdown (Templates) | - | 模板文件格式 |
| Runtime | Claude Code | - | 模板执行环境 |
| Time | Python datetime | - | 时间戳生成（Claude 内置） |
| Random | Python random | - | 随机后缀生成（Claude 内置） |

## 2. Constitutionality Review

| Principle | Compliance | Notes |
|-----------|------------|-------|
| Code Quality | ✅ | 新命名方案简洁清晰，易于理解和维护 |
| Testing Standards | ✅ | 包含 5 个可验证的测试用例 |
| Documentation | ✅ | 计划包含文档更新，有详细示例 |
| Architecture | ✅ | 与现有系统兼容，支持新旧格式共存 |
| Performance | ✅ | 无性能影响 |
| Security | ✅ | 无安全风险 |

## 3. Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    /codexspec:generate-spec                 │
│                         (用户命令)                           │
└─────────────────────────┬───────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│              templates/commands/generate-spec.md            │
│                      (模板文件)                              │
│  ┌─────────────────────────────────────────────────────┐    │
│  │ Step 1: Determine Feature ID (修改点)               │    │
│  │                                                      │    │
│  │ 旧逻辑: ls → 找最大序号 → N+1                        │    │
│  │ 新逻辑: date +"%Y-%m%d-%H%M" + 随机2位字符           │    │
│  └─────────────────────────────────────────────────────┘    │
└─────────────────────────┬───────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│              .codexspec/specs/{prefix}-{name}/              │
│                      (输出目录)                              │
│                                                             │
│  旧格式: 001-feature-name/                                  │
│  新格式: 2025-0321-1430k7-feature-name/                     │
└─────────────────────────────────────────────────────────────┘
```

## 4. Component Structure

```
codexspec/
├── templates/
│   └── commands/
│       ├── generate-spec.md    # [修改] Feature ID 生成逻辑
│       └── *.md                # [检查] 其他模板中的 feature-id 引用
├── CLAUDE.md                   # [更新] 添加新命名方案说明
└── tests/                      # [新增] 测试用例（可选）
```

## 5. Module Dependency Graph

```
┌──────────────────────┐
│  generate-spec.md    │  ← 主要修改点
│  (模板文件)          │
└──────────┬───────────┘
           │ 被引用于
           ▼
┌──────────────────────┐     ┌──────────────────────┐
│  CLAUDE.md           │     │  其他模板文件        │
│  (项目文档)          │     │  (spec-to-plan等)    │
└──────────────────────┘     └──────────────────────┘
           │                           │
           │ 需要同步更新               │ 检查引用一致性
           ▼                           ▼
┌──────────────────────┐     ┌──────────────────────┐
│  命名方案说明        │     │  {feature-id} 引用   │
└──────────────────────┘     └──────────────────────┘
```

## 6. Module Specifications

### Module: generate-spec.md

- **Responsibility**: 定义 spec 目录命名规则和生成逻辑
- **Dependencies**: 无
- **Interface**: 模板指令，指导 Claude 如何创建 spec 目录
- **Files**: `templates/commands/generate-spec.md`

**修改内容**:

```markdown
# 旧逻辑 (Step 1)
1. **Determine Feature ID**: List directories in `.codexspec/specs/` using `ls` command
   to find existing spec directories (each spec is a directory named `{NNN}-{feature-name}/`).
   Determine the next sequential number (e.g., if `001-*` directory exists, use `002-`).

# 新逻辑 (Step 1)
1. **Determine Feature ID**: Generate a unique prefix using timestamp + random suffix:
   - Get current timestamp: `date +"%Y-%m%d-%H%M"` (14 digits with hyphens)
   - Generate 2-character random suffix from [a-z0-9] (36 characters)
   - Full prefix: 16 characters (e.g., `2025-0321-1430k7`)

   > **Format**: `{YYYY-MMDD-HHMM}{random}-{feature-name}`
   > **Example**: `2025-0321-1430k7-user-authentication`
```

### Module: CLAUDE.md

- **Responsibility**: 项目开发文档
- **Dependencies**: 无
- **Interface**: 开发者参考文档
- **Files**: `CLAUDE.md`

**修改内容**: 添加新命名方案说明章节

### Module: 其他模板文件

- **Responsibility**: 各类命令模板
- **Dependencies**: generate-spec.md 的命名约定
- **Interface**: 模板中的 `{feature-id}` 占位符
- **Files**: `templates/commands/*.md`

**修改内容**: 更新 `{feature-id}` 格式说明（如有必要）

## 7. Data Models

不适用 - 本功能不涉及数据模型。

## 8. API Contracts

不适用 - 本功能为模板修改，不涉及 API。

### Command: `/codexspec:generate-spec`

- **Arguments**: 无（或 feature name）
- **Output**: 创建目录 `.codexspec/specs/{YYYY-MMDD-HHMM}{random}-{feature-name}/`
- **Format**: `^\d{4}-\d{4}-\d{4}[a-z0-9]{2}-[a-z0-9-]+$`

## 9. Implementation Phases

### Phase 1: 核心模板修改

- [ ] **TASK-001**: 修改 `templates/commands/generate-spec.md`
  - 更新 Step 1 的 Feature ID 生成逻辑
  - 添加时间戳格式说明：`date +"%Y-%m%d-%H%M"`
  - 添加随机后缀生成说明
  - 添加格式验证正则表达式

### Phase 2: 文档更新

- [ ] **TASK-002**: 更新 `CLAUDE.md`
  - 添加 Spec 目录命名方案章节
  - 说明新旧格式兼容性
  - 提供示例和格式说明

### Phase 3: 相关模板检查

- [ ] **TASK-003**: 检查其他模板中的 `{feature-id}` 引用
  - 确保引用格式与新命名方案兼容
  - 更新需要调整的说明文本

### Phase 4: 测试验证

- [ ] **TASK-004**: 验证新命名方案
  - 测试时间戳生成正确性
  - 测试随机后缀字符集
  - 测试目录排序效果
  - 测试与旧格式目录的兼容性

## 10. Technical Decisions

### Decision 1: 使用4位年份 + 连字符分隔

- **Choice**: 使用 `YYYY-MMDD-HHMM` 格式（含连字符分隔）
- **Rationale**:
  - 4位年份避免跨世纪问题，更清晰
  - 连字符分隔大幅提高可读性
  - 格式类似 ISO 8601，开发者熟悉
- **Alternatives**: 无连字符紧凑格式（`YYYYMMDDHHMM`）
- **Trade-offs**: 前缀长度从 12 字符增加到 16 字符

### Decision 2: 时间戳精度选择分钟级别

- **Choice**: 使用 `YYYY-MMDD-HHMM`（精确到分钟）
- **Rationale**:
  - 秒级精度会增加前缀长度但收益有限
  - 分钟级别配合随机后缀已足够保证唯一性
  - 更易读，便于口头交流
- **Alternatives**: 精确到秒（`YYYY-MMDD-HHMMSS`）
- **Trade-offs**: 同一分钟内多个 spec 依赖随机后缀区分

### Decision 3: 随机后缀长度为 2 位

- **Choice**: 2 位小写字母 + 数字
- **Rationale**:
  - 36² = 1296 种组合，冲突概率 < 0.1%
  - 保持前缀简洁
  - 简短且易于输入
- **Alternatives**: 3 位随机（46656 种组合）
- **Trade-offs**: 极端情况下同一分钟内 3 人以上创建 spec 时冲突概率略增

### Decision 4: 不迁移现有目录

- **Choice**: 保持现有序号格式目录不变
- **Rationale**:
  - 避免破坏性变更
  - 新旧格式可共存
  - 减少迁移风险
- **Alternatives**: 自动迁移所有现有目录
- **Trade-offs**: specs 目录中将同时存在两种格式

### Decision 5: 使用本地时间而非 UTC

- **Choice**: 基于开发者本地系统时间
- **Rationale**:
  - 更直观，开发者可直接读出创建时间
  - 无需时区转换
  - 不影响唯一性目标
- **Alternatives**: 使用 UTC 时间
- **Trade-offs**: 跨时区协作时时间戳可能不在预期范围

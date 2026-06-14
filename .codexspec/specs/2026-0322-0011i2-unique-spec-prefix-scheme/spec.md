# Feature: 唯一 Spec 目录前缀方案

## Overview

重新设计 `.codexspec/specs/` 目录下各 spec 目录的命名前缀方案，从纯序号（001, 002, 003...）改为时间戳+随机后缀格式，解决多人协作开发时跨分支创建 spec 目录产生的序号冲突问题。

## Goals

- 消除多人协作场景下 spec 目录序号冲突的风险
- 保持目录按创建时间自然排序
- 保持目录名称的人类可读性
- 保持前缀简洁

## User Stories

### Story 1: 多人协作创建 Spec

**As a** 团队开发者
**I want** 在我的 feature 分支上创建 spec 目录时不会与其他成员冲突
**So that** 合并分支时不会出现目录名重复问题

**Acceptance Criteria:**

- [ ] 从同一基准分支 checkout 的多个开发者可以独立创建 spec 目录
- [ ] 各分支的 spec 目录在合并时不会产生名称冲突
- [ ] 冲突概率趋近于零（< 0.1%）

### Story 2: 按时间排序查看 Spec

**As a** 项目维护者
**I want** specs 目录中的子目录按创建时间顺序排列
**So that** 我可以方便地追踪项目功能演进历史

**Acceptance Criteria:**

- [ ] 目录名称排序结果与创建时间顺序一致
- [ ] 跨年度项目也能正确排序
- [ ] 无需额外工具即可查看创建顺序

### Story 3: 快速识别创建时间

**As a** 开发者
**I want** 从目录名称直接读出创建日期和时间
**So that** 在团队讨论时可以快速定位相关 spec

**Acceptance Criteria:**

- [ ] 目录前缀包含完整的日期时间信息
- [ ] 格式直观易读
- [ ] 支持跨年识别

## Functional Requirements

- [REQ-001] Spec 目录前缀格式为 `YYYY-MMDD-HHMM{random}`，各部分定义如下：
  - **Year** (4 digits): 0001-9999
  - **Month** (2 digits): 01-12
  - **Day** (2 digits): 01-31
  - **Hour** (2 digits): 00-23
  - **Minute** (2 digits): 00-59
  - **Random** (2 chars): lowercase letters a-z + digits 0-9

  > Example: `2025-0321-1430` represents March 21, 2025 at 14:30

- [REQ-002] 前缀各部分使用连字符 `-` 分隔以提高可读性

- [REQ-003] 完整目录命名格式：`YYYY-MMDD-HHMM{random}-feature-name`
  - Example: `2025-0321-1430k7-user-authentication`

- [REQ-004] 随机字符集为 36 种字符（a-z + 0-9），提供 1296 种组合

- [REQ-005] 前缀总长度为 16 字符（14位时间戳 + 2位随机，含2个连字符）

- [REQ-006] 时间戳基于本地系统时间生成

## Non-Functional Requirements

- [NFR-001] **唯一性**：同一分钟内创建的 spec 冲突概率 < 0.1%
  - 计算依据：36² = 1296 种组合，两人同时创建时冲突概率 ≈ 1/1296 ≈ 0.08%

- [NFR-002] **可读性**：开发者可直接从目录名读出创建日期和时间

- [NFR-003] **排序性**：目录按名称 ASCII 排序即为创建时间顺序

- [NFR-004] **兼容性**：支持与现有序号格式目录共存

## Acceptance Criteria (Test Cases)

- [TC-001] 验证时间戳格式正确性
  - Given: 当前时间为 2025-03-21 14:30
  - When: 生成 spec 目录前缀
  - Then: 前缀以 `2025-0321-1430` 开头

- [TC-002] 验证随机后缀字符集
  - Given: 生成 spec 目录
  - When: 生成随机后缀
  - Then: 后缀仅包含小写字母 a-z 或数字 0-9

- [TC-003] 验证目录排序
  - Given: 存在多个 spec 目录
    - `2025-0321-1430k7-feature-a`
    - `2025-0415-0930x3-feature-b`
    - `2026-0101-1000m9-feature-c`
  - When: 按名称排序
  - Then: 顺序为 feature-a, feature-b, feature-c（与创建时间一致）

- [TC-004] 验证跨分支唯一性
  - Given: 开发者 A 和 B 同时从 main 分支 checkout
  - When: 两人在同一分钟内各自创建 spec 目录
  - Then: 目录前缀的随机后缀不同（概率 99.92%）

- [TC-005] 验证格式合规性
  - Given: 新创建的 spec 目录
  - When: 检查目录名格式
  - Then: 匹配正则表达式 `^\d{4}-\d{4}-\d{4}[a-z0-9]{2}-[a-z0-9-]+$`

## Edge Cases

- **系统时间回拨**：如果系统时间被手动调整，可能导致时间戳不准确
  - 处理：依赖系统时间，不做额外处理；随机后缀仍可保证唯一性

- **时区差异**：不同时区的开发者创建的 spec 时间戳基于各自的本地时间
  - 处理：使用本地时间，不影响唯一性目标；排序在单个仓库内仍然有效

- **闰秒**：闰秒不影响分钟级别的时间戳
  - 处理：无需特殊处理

## Output Examples

```
specs/
├── 001-legacy-feature/           # 旧格式（兼容保留）
├── 002-another-legacy/           # 旧格式（兼容保留）
├── 2025-0321-1430k7-user-authentication/
├── 2025-0415-0930x3-payment-integration/
├── 2026-0101-1000m9-dashboard-redesign/
└── 2026-0315-1530a5-api-rate-limiting/
```

**命名格式说明**：

```
2025-0321-1430k7-user-authentication
││││ ││││ ││││ ││
││││ ││││ ││││ │└── Random suffix (2 chars)
││││ ││││ ││││ └─── Random suffix (1 char)
││││ ││││ │││└───── Minute (30)
││││ ││││ ││└────── Minute (30)
││││ ││││ │└─────── Hour (14)
││││ ││││ └──────── Hour (14)
││││ │││└───────── Day (21)
││││ ││└────────── Day (21)
││││ │└─────────── Month (03)
││││ └──────────── Month (03)
│││└────────────── Separator (-)
││└─────────────── Year (2025)
│└──────────────── Year (2025)
└───────────────── Separator (-)
```

## Out of Scope

- 自动迁移现有序号格式目录到新格式
- 强制重命名已存在的 spec 目录
- 提供目录名冲突检测和自动解决机制
- 跨时区时间标准化（UTC 转换）
- 验证目录名格式是否合规的 lint 工具

## Implementation Notes

本功能主要涉及以下文件的修改：

1. **模板文件**：`templates/commands/specify.md` 和 `templates/commands/generate-spec.md`
   - 更新 Feature ID 生成逻辑，使用新的时间戳+随机格式
   - 时间戳生成命令：`date +"%Y-%m%d-%H%M"`

2. **CLAUDE.md**：更新文档说明新的命名方案

3. **可选**：考虑在 CLI 中添加目录名格式验证功能

# Implementation Plan: Plugin 配置支持

## 1. Tech Stack

| Category | Technology | Version | Notes |
|----------|------------|---------|-------|
| Language | Markdown | N/A | Slash command 模板 |
| Configuration | YAML | 1.1+ | 配置文件格式 |
| Runtime | Claude Code | Latest | Slash command 执行环境 |
| Package Manager | uv | Latest | Python 包管理器（用于测试和发布） |

## 2. Constitutionality Review

| Principle | Compliance | Notes |
|-----------|------------|-------|
| Code Quality | ✅ | 模板设计清晰，复用 Configuration Check 片段 |
| Testing Standards | ✅ | 计划包含 8 个详细测试用例 |
| Documentation | ✅ | 模板内含清晰的说明和示例 |
| Architecture | ✅ | 复用现有配置机制，最小化修改范围 |
| Performance | ✅ | 配置检测为简单的文件存在性检查，性能影响可忽略 |
| Security | ✅ | 不涉及敏感数据处理 |
| Slash Command Template Modification Rules | ✅ | 仅修改 `templates/commands/` 目录 |

### Constitution Compliance Details

**Slash Command Template Modification Rules**:

- ✅ 所有修改都在 `templates/commands/` 目录进行
- ✅ 不会修改 `.claude/commands/codexspec/` 目录
- ✅ 遵循"修改源模板 → 测试 → 提交"的工作流

## 3. Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                     Claude Code Runtime                      │
└─────────────────────────────────────────────────────────────┘
                              │
                              │ executes
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    Slash Command Templates                   │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐  │
│  │   config    │  │   specify   │  │   commit-staged     │  │
│  │   (NEW)     │  │  (MODIFIED) │  │     (MODIFIED)      │  │
│  └─────────────┘  └─────────────┘  └─────────────────────┘  │
│         │                │                   │               │
│         │                │                   │               │
│         └────────────────┼───────────────────┘               │
│                          │                                   │
│                          ▼                                   │
│  ┌───────────────────────────────────────────────────────┐  │
│  │              Configuration Check (新增部分)            │  │
│  │  • 检测 .codexspec/config.yml 是否存在                │  │
│  │  • 不存在时显示一次性提示                              │  │
│  │  • 使用默认值继续执行                                  │  │
│  └───────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                              │
                              │ reads
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                  .codexspec/config.yml                       │
│  version: "1.0"                                              │
│  language:                                                   │
│    output: "zh-CN"                                           │
│    commit: "zh-CN"                                           │
│    templates: "en"                                           │
└─────────────────────────────────────────────────────────────┘
```

## 4. Component Structure

```
codexspec/
├── templates/
│   └── commands/
│       ├── config.md          # 新增：配置管理命令
│       ├── specify.md         # 修改：增加 Configuration Check 部分
│       └── commit-staged.md   # 修改：增加 Configuration Check 部分
└── .codexspec/
    └── config.yml              # 用户项目配置文件（由 config 命令创建）
```

## 5. Module Dependency Graph

```
┌─────────────────┐
│  config.md      │
│  (新增)         │
└────────┬────────┘
         │ creates/reads
         ▼
┌─────────────────┐
│  config.yml     │
│  (配置文件)     │
└────────┬────────┘
         │ reads
         ▼
┌─────────────────┐     ┌─────────────────┐
│  specify.md     │     │ commit-staged.md │
│  (修改)         │     │ (修改)           │
└─────────────────┘     └─────────────────┘
```

## 6. Module Specifications

### Module: config.md (新增)

- **Responsibility**: 提供交互式配置管理功能，包括创建、查看、修改、重置配置
- **Dependencies**: 无（独立命令）
- **Interface**: 通过 AskUserQuestion 工具与用户交互
- **Files**: `templates/commands/config.md`

**模板结构**:

```yaml
---
description: Manage CodexSpec project configuration interactively
argument-hint: "[--view] View current configuration"
---
```

**核心功能**:

1. 检测配置文件是否存在
2. 提供交互式菜单（创建/查看/修改/重置）
3. 使用 AskUserQuestion 引导用户选择语言
4. 创建或更新 `.codexspec/config.yml` 文件

### Module: specify.md (修改)

- **Responsibility**: 在现有功能基础上增加配置检测逻辑
- **Dependencies**: 无变化
- **Interface**: 在 `## Language Preference` 之前插入 `## Configuration Check`
- **Files**: `templates/commands/specify.md`

**修改点**:

- 在第 9 行（`## Language Preference`）之前插入 `## Configuration Check` 部分
- 保持现有所有功能不变

### Module: commit-staged.md (修改)

- **Responsibility**: 在现有功能基础上增加配置检测逻辑
- **Dependencies**: 无变化
- **Interface**: 在 `## Language Preference` 之前插入 `## Configuration Check`
- **Files**: `templates/commands/commit-staged.md`

**修改点**:

- 在第 19 行（`## Language Preference`）之前插入 `## Configuration Check` 部分
- 保持现有所有功能不变

## 7. Configuration Check 模板片段

**复用片段** - 用于 specify.md 和 commit-staged.md:

```markdown
## Configuration Check

**IMPORTANT**: Before proceeding, check if the project configuration exists.

### Execution Steps

1. **Check Configuration File**
   - Check if `.codexspec/config.yml` exists
   - This is a simple file existence check, no parsing needed at this stage

2. **If Configuration Does NOT Exist**
   - Display a one-time prompt:
     ```
     💡 检测到项目未配置语言设置。你可以使用 `/codexspec:config` 命令来创建配置文件。
     ```
   - Use default values for current session:
     - `language.output`: "en"
     - `language.commit`: "en"
     - `language.templates`: "en"
   - Continue with command execution normally

3. **If Configuration Exists**
   - Proceed to `## Language Preference` section
   - Read configuration and apply language settings as before

4. **Session State** (Implicit)
   - The prompt is shown only once per conversation session
   - Claude's conversation context naturally maintains this state
   - No additional mechanism needed
```

## 8. Implementation Phases

### Phase 1: 创建 config 命令模板

- [ ] 创建 `templates/commands/config.md` 文件
- [ ] 实现 YAML frontmatter（description, argument-hint）
- [ ] 实现配置文件存在性检测逻辑
- [ ] 实现交互式菜单（创建/查看/修改/重置）
- [ ] 实现语言选择交互流程
- [ ] 实现 `.codexspec/config.yml` 文件创建逻辑
- [ ] 实现配置查看功能
- [ ] 实现配置修改功能
- [ ] 实现配置重置功能

### Phase 2: 修改 specify 命令

- [ ] 在 `templates/commands/specify.md` 中添加 `## Configuration Check` 部分
- [ ] 确保位置在 `## Language Preference` 之前
- [ ] 验证不影响现有功能

### Phase 3: 修改 commit-staged 命令

- [ ] 在 `templates/commands/commit-staged.md` 中添加 `## Configuration Check` 部分
- [ ] 确保位置在 `## Language Preference` 之前
- [ ] 验证不影响现有功能

### Phase 4: 测试验证

- [ ] **TC-001**: 测试 config 命令创建配置功能
- [ ] **TC-002**: 测试 config 命令查看配置功能
- [ ] **TC-003**: 测试 config 命令修改配置功能
- [ ] **TC-004**: 测试 config 命令重置配置功能
- [ ] **TC-005**: 测试 specify 命令配置缺失提示
- [ ] **TC-006**: 测试 specify 命令配置存在时正常执行
- [ ] **TC-007**: 测试 commit-staged 命令会话内不重复提示
- [ ] **TC-008**: 测试 commit-staged 命令使用配置语言

### Phase 5: 文档和发布

- [ ] 更新 README.md 中的命令列表（添加 config 命令）
- [ ] 更新 CLAUDE.md 中的命令实现状态
- [ ] 更新 `.claude-plugin/marketplace.json` 版本号
- [ ] 提交代码变更

## 9. Technical Decisions

### Decision 1: 只修改 2 个命令而非 7 个

- **Choice**: 仅在 `specify` 和 `commit-staged` 命令中添加配置检测
- **Rationale**:
  - `specify` 是工作流起点，首次检测配置的最佳位置
  - `commit-staged` 是工作流终点，确保提交信息语言正确
  - 其他命令紧接 specify 执行，用户已收到提示
  - 最小化修改范围，降低实现复杂度
- **Alternatives**: 在所有 7 个命令中添加检测（复杂度高，重复提示）
- **Trade-offs**: 用户直接执行中间命令（如 generate-spec）时不会收到提示，但这是边缘情况

### Decision 2: 使用会话上下文而非显式状态管理

- **Choice**: 利用 Claude 对话上下文隐式管理"已提示"状态
- **Rationale**:
  - Slash command 模板无法使用传统编程方式管理状态
  - Claude 在整个会话中保持对话历史
  - 简单有效，无需额外机制
- **Alternatives**:
  - 使用临时文件（增加文件 I/O，不可靠）
  - 使用环境变量（在 slash command 模式下不可行）
- **Trade-offs**: 新会话会重新显示提示，但这是可接受的行为

### Decision 3: 配置检测逻辑内嵌于命令模板

- **Choice**: 将 Configuration Check 部分直接嵌入命令模板
- **Rationale**:
  - 保持模板自包含，便于理解和维护
  - 避免复杂的模板包含机制
  - 修改范围小，只有 2 个命令
- **Alternatives**:
  - 创建共享模板片段并使用包含机制（增加复杂度）
- **Trade-offs**: 如果将来需要扩展到更多命令，需要逐个添加

### Decision 4: 默认使用英语

- **Choice**: 配置缺失时默认使用英语
- **Rationale**:
  - 英语是国际通用语言，最安全的默认值
  - 与现有行为保持一致（配置文件是可选的）
  - 用户可通过 config 命令随时更改
- **Alternatives**:
  - 根据系统语言自动检测（复杂度高，不可靠）
  - 强制用户配置（影响用户体验）
- **Trade-offs**: 非英语用户首次使用时会看到英语提示，但可接受

## 10. File Changes Summary

| File | Action | Lines Changed (Est.) |
|------|--------|----------------------|
| `templates/commands/config.md` | 新增 | ~150 行 |
| `templates/commands/specify.md` | 修改 | +30 行 |
| `templates/commands/commit-staged.md` | 修改 | +30 行 |
| `README.md` | 修改 | +1 行（命令列表） |
| `CLAUDE.md` | 修改 | +1 行（状态更新） |
| `.claude-plugin/marketplace.json` | 修改 | 版本号更新 |

**Total Estimated Changes**: ~210 行

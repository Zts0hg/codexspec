# Feature: Plugin 配置支持

## Overview

为通过 Claude Code Plugin Marketplace 安装 CodexSpec 的用户提供便捷的语言配置方式，解决当前需要手动创建 `.codexspec/config.yml` 文件的问题。

## Goals

- **降低使用门槛**：Plugin 用户无需手动创建配置文件即可使用多语言功能
- **提供配置命令**：通过 `/codexspec:config` 命令交互式管理项目配置
- **智能引导**：在首次使用时自动检测并引导用户配置

## User Stories

### Story 1: 交互式创建配置

**As a** 通过 Plugin 安装 CodexSpec 的用户
**I want** 通过交互式命令创建语言配置文件
**So that** 我不需要手动编写 YAML 文件

**Acceptance Criteria:**

- [ ] 执行 `/codexspec:config` 命令可以启动交互式配置流程
- [ ] 命令会引导用户选择输出语言、提交信息语言等配置项
- [ ] 配置完成后在 `.codexspec/config.yml` 创建配置文件
- [ ] 如果配置文件已存在，提示用户选择修改或查看

### Story 2: 查看当前配置

**As a** CodexSpec 用户
**I want** 查看当前项目的语言配置
**So that** 我可以确认配置是否正确

**Acceptance Criteria:**

- [ ] `/codexspec:config --view` 或交互选项可以显示当前配置
- [ ] 配置以易读的格式展示
- [ ] 如果配置文件不存在，提示用户可以创建

### Story 3: 修改配置项

**As a** CodexSpec 用户
**I want** 修改现有配置的特定项
**So that** 我可以根据需要调整配置而不需要重建整个文件

**Acceptance Criteria:**

- [ ] 可以选择修改特定配置项（如只修改 output 语言）
- [ ] 修改后保留其他配置不变
- [ ] 修改完成后显示更新后的配置

### Story 4: 重置配置

**As a** CodexSpec 用户
**I want** 重置配置到默认值
**So that** 我可以快速恢复到初始状态

**Acceptance Criteria:**

- [ ] 提供重置配置选项
- [ ] 重置前确认用户意图
- [ ] 重置后显示新的默认配置

### Story 5: 首次使用引导

**As a** 新用户
**I want** 在首次使用相关命令时收到配置引导
**So that** 我知道如何设置语言偏好

**Acceptance Criteria:**

- [ ] 执行需要语言配置的命令时检测配置文件是否存在
- [ ] 如果不存在，显示一次性提示引导用户使用 config 命令
- [ ] 提示后使用默认值（英语）继续执行命令
- [ ] 同一会话中不重复提示

## Functional Requirements

### REQ-001: `/codexspec:config` 命令

创建新的 slash command 模板文件 `templates/commands/config.md`，支持以下操作模式：

- **无参数模式**：交互式菜单，显示选项让用户选择操作
- **创建模式**：引导用户配置语言、项目信息等
- **查看模式**：显示当前配置内容
- **修改模式**：选择要修改的配置项并更新
- **重置模式**：确认后恢复默认配置

### REQ-002: 配置检测机制

**仅在以下 2 个关键命令**中增加配置文件检测逻辑：

#### 修改范围

| 命令 | 文件路径 | 检测原因 |
|------|----------|----------|
| `/codexspec:specify` | `templates/commands/specify.md` | 工作流**起点** - 需求收集的第一步，首次检测配置的最佳位置 |
| `/codexspec:commit-staged` | `templates/commands/commit-staged.md` | 工作流**终点** - 提交前的最后一步，确保提交信息语言正确 |

**设计理由**：

1. **工作流覆盖**: `specify` 是起点，`commit-staged` 是终点，覆盖完整用户旅程
2. **最小化修改**: 从 7 个命令减少到 2 个，降低实现复杂度和测试成本
3. **避免重复提示**: 其他命令（generate-spec, clarify, spec-to-plan 等）紧接 specify 执行，用户已收到配置提示
4. **可扩展性**: 如后续发现需要，可轻松扩展到其他命令

**不修改的命令**（共 15 个）：

- generate-spec, clarify, checklist, spec-to-plan, plan-to-tasks, review-spec, review-plan, review-tasks, implement-tasks, tasks-to-issues, pr, translate-docs, check-i18n-semantics, review-python-code, review-react-code, constitution

### REQ-003: 检测逻辑实现

在每个命令模板的 `## Language Preference` 部分之前增加 `## Configuration Check` 部分：

```markdown
## Configuration Check

**IMPORTANT**: Before proceeding, check if the project configuration exists.

1. Check if `.codexspec/config.yml` exists
2. If not exists:
   - Display one-time prompt: "💡 检测到项目未配置语言设置。你可以使用 `/codexspec:config` 命令来创建配置文件。"
   - Use default values (English) for current session
   - Continue with command execution
3. If exists:
   - Read configuration and proceed normally
```

### REQ-004: 会话状态管理

为避免重复提示，需要在会话中记录是否已显示过配置提示：

- 首次检测到配置缺失时显示提示
- 后续命令不再重复提示
- 使用会话级别的状态标记（可通过 Claude 的对话上下文实现）

### REQ-005: 默认配置值

当配置文件不存在时使用的默认值：

```yaml
version: "1.0"
language:
  output: "en"
  commit: "en"
  templates: "en"
project:
  ai: "claude"
  created: "{current_date}"
```

## Non-Functional Requirements

### NFR-001: 用户体验

- 配置命令的交互流程应简洁明了
- 提示信息应使用用户选择的语言（如果配置已存在）
- 错误信息应提供明确的解决方案

### NFR-002: 兼容性

- 新增的配置检测逻辑不应影响现有命令的正常执行
- 配置文件不存在时命令应能正常工作（使用默认值）
- 与 CLI 安装方式的配置机制保持兼容

### NFR-003: 可维护性

- 配置检测逻辑应抽取为可复用的模板片段
- 新增命令时应易于复用检测逻辑

## Acceptance Criteria (Test Cases)

### TC-001: 首次使用 config 命令创建配置

1. 确保项目没有 `.codexspec/config.yml` 文件
2. 执行 `/codexspec:config`
3. 选择"创建新配置"
4. 按提示选择语言（如 zh-CN）
5. 验证 `.codexspec/config.yml` 已创建且内容正确

### TC-002: 查看已存在的配置

1. 确保项目有 `.codexspec/config.yml` 文件
2. 执行 `/codexspec:config`
3. 选择"查看当前配置"
4. 验证配置内容正确显示

### TC-003: 修改配置项

1. 确保项目有配置文件且 `language.output` 为 "en"
2. 执行 `/codexspec:config`
3. 选择"修改配置项"
4. 选择修改 `language.output`
5. 设置为 "zh-CN"
6. 验证只有 output 被修改，其他配置保持不变

### TC-004: 重置配置

1. 确保项目有自定义配置
2. 执行 `/codexspec:config`
3. 选择"重置配置"
4. 确认重置操作
5. 验证配置已恢复到默认值

### TC-005: 配置缺失时的提示（specify 命令）

1. 删除或重命名 `.codexspec/config.yml`
2. 执行 `/codexspec:specify`
3. 验证显示配置提示信息
4. 验证命令使用英语继续执行
5. 再次执行 `/codexspec:commit-staged`（不修改任何文件）
6. 验证不再重复显示提示（同一会话）

### TC-006: 配置存在时正常执行（specify 命令）

1. 确保项目有配置文件且 `language.output` 为 "zh-CN"
2. 执行 `/codexspec:specify`
3. 验证不显示配置提示
4. 验证命令使用中文执行

### TC-007: commit-staged 命令的配置检测

1. 确保项目没有配置文件
2. 先执行 `/codexspec:specify`（会显示配置提示）
3. 执行 `/codexspec:commit-staged`
4. 验证不重复显示提示（同一会话）
5. 验证提交信息使用英语

### TC-008: commit-staged 命令使用配置语言

1. 确保项目有配置文件且 `language.commit` 为 "zh-CN"
2. 执行 `/codexspec:commit-staged`
3. 验证提交信息使用中文

## Edge Cases

- **配置文件格式错误**：如果配置文件存在但格式不正确，应提示用户使用 config 命令重新创建或修复
- **部分配置缺失**：如果配置文件存在但某些字段缺失，应使用对应字段的默认值
- **并发修改**：如果用户在命令执行期间手动修改配置文件，后续命令应读取最新配置
- **Plugin 与 CLI 混用**：如果用户同时通过 CLI 和 Plugin 使用，应共享同一配置文件

## Output Examples

### config 命令交互示例

```
/codexspec:config

📋 CodexSpec 配置管理

检测到项目尚未配置。请选择操作：
1. 创建新配置
2. 查看当前配置（不可用 - 配置不存在）

请选择 [1-2]: 1

🌐 语言配置
请选择输出语言：
1. English (en)
2. 简体中文 (zh-CN)
3. 繁體中文 (zh-TW)
4. 日本語 (ja)
5. 其他...

请选择 [1-5]: 2

📝 提交信息语言
1. 与输出语言相同 (zh-CN)
2. English (en)

请选择 [1-2]: 1

✅ 配置已保存到 .codexspec/config.yml
```

### 配置缺失提示示例

```
/codexspec:specify 新功能需求

💡 检测到项目未配置语言设置。你可以使用 `/codexspec:config` 命令来创建配置文件。

# Requirement Clarification

## User Input
新功能需求
...
```

## Clarifications

### Session 2026-03-28 17:00

**Q1**: 配置检测应该覆盖哪些命令？

**A1**: 仅需要修改 `/codexspec:specify` 和 `/codexspec:commit-staged` 两个命令

**Impact**: REQ-002, TC-005, TC-006

**理由**：

- `specify` 是工作流起点，首次检测配置的最佳位置
- `commit-staged` 是工作流终点，确保提交信息语言正确
- 其他命令通常紧接在 specify 之后执行，用户已收到配置提示
- 最小化修改范围，降低实现复杂度

---

### Session 2026-03-28 17:15

**Q2**: 重新确认修改范围，确保只修改 specify 和 commit-staged 命令

**A2**: 确认只修改这 2 个命令，其他 15 个命令不增加配置检测

**Impact**: REQ-002, TC-005, TC-006, TC-007, TC-008

**更新内容**：

- REQ-002: 添加详细的修改范围表格和设计理由
- TC-005/TC-006: 更新测试步骤，明确是针对 specify 命令
- TC-007/TC-008: 新增测试用例，针对 commit-staged 命令

---

## Out of Scope

- **配置验证**：不对配置值的有效性进行严格验证（如语言代码是否有效）
- **多配置文件**：不支持多个配置文件切换
- **全局配置**：不支持用户级别的全局配置（仅项目级别）
- **配置迁移**：不提供旧版本配置文件的自动迁移功能
- **配置加密**：不支持敏感信息的加密存储

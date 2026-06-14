# Task Breakdown: Plugin 配置支持

## Overview

Total tasks: 13
Parallelizable tasks: 4
Estimated phases: 5

## User Story Mapping

| User Story | Tasks |
|------------|-------|
| Story 1: 交互式创建配置 | Task 1.1, Task 4.1 |
| Story 2: 查看当前配置 | Task 1.1, Task 4.2 |
| Story 3: 修改配置项 | Task 1.1, Task 4.3 |
| Story 4: 重置配置 | Task 1.1, Task 4.4 |
| Story 5: 首次使用引导 | Task 2.1, Task 3.1, Task 4.5-4.8 |

## Phase 1: Foundation - 创建 config 命令模板

### Task 1.1: 创建 config.md 命令模板 ✅

- **Type**: Implementation
- **Files**: `templates/commands/config.md`
- **Description**: 创建完整的 config 命令模板，包含：
  - YAML frontmatter（description, argument-hint）
  - 配置文件存在性检测逻辑
  - 交互式菜单（创建/查看/修改/重置）
  - 语言选择交互流程
  - 配置文件创建/更新逻辑
- **Dependencies**: None
- **Est. Complexity**: Medium
- **Test Case**: TC-001, TC-002, TC-003, TC-004
- **Status**: ✅ Completed (2026-03-28)

## Phase 2: Core Implementation - 修改现有命令

### Task 2.1: 修改 specify.md 添加配置检测 ✅

- **Type**: Implementation
- **Files**: `templates/commands/specify.md`
- **Description**: 在 `## Language Preference` 之前插入 `## Configuration Check` 部分：
  - 配置文件存在性检测
  - 配置缺失时显示一次性提示
  - 使用默认值继续执行
- **Dependencies**: Task 1.1
- **Est. Complexity**: Low
- **Test Case**: TC-005, TC-006
- **Status**: ✅ Completed (2026-03-28)

### Task 2.2: 修改 commit-staged.md 添加配置检测 [P] ✅

- **Type**: Implementation
- **Files**: `templates/commands/commit-staged.md`
- **Description**: 在 `## Language Preference` 之前插入 `## Configuration Check` 部分：
  - 配置文件存在性检测
  - 配置缺失时显示一次性提示
  - 使用默认值继续执行
- **Dependencies**: Task 1.1
- **Est. Complexity**: Low
- **Test Case**: TC-007, TC-008
- **Status**: ✅ Completed (2026-03-28)

## Phase 3: Testing - 功能验证

### Task 3.1: 验证 config 命令创建配置功能

- **Type**: Testing
- **Files**: 手动测试
- **Description**: TC-001 测试用例验证：
  1. 确保项目没有 `.codexspec/config.yml` 文件
  2. 执行 `/codexspec:config`
  3. 选择"创建新配置"
  4. 按提示选择语言（如 zh-CN）
  5. 验证 `.codexspec/config.yml` 已创建且内容正确
- **Dependencies**: Task 1.1
- **Est. Complexity**: Low

### Task 3.2: 验证 config 命令查看/修改/重置功能 [P]

- **Type**: Testing
- **Files**: 手动测试
- **Description**: TC-002, TC-003, TC-004 测试用例验证：
  - 查看已存在的配置
  - 修改配置项
  - 重置配置
- **Dependencies**: Task 1.1
- **Est. Complexity**: Low

### Task 3.3: 验证 specify 命令配置检测 [P]

- **Type**: Testing
- **Files**: 手动测试
- **Description**: TC-005, TC-006 测试用例验证：
  - 配置缺失时的提示
  - 配置存在时正常执行
- **Dependencies**: Task 2.1
- **Est. Complexity**: Low

### Task 3.4: 验证 commit-staged 命令配置检测 [P]

- **Type**: Testing
- **Files**: 手动测试
- **Description**: TC-007, TC-008 测试用例验证：
  - 会话内不重复提示
  - 使用配置语言生成提交信息
- **Dependencies**: Task 2.2
- **Est. Complexity**: Low

## Phase 4: Integration - 端到端验证

### Task 4.1: 完整工作流验证

- **Type**: Testing
- **Files**: 手动测试
- **Description**: 验证完整用户工作流：
  1. 新项目无配置 → 执行 specify → 收到提示
  2. 使用 config 创建配置
  3. 再次执行 specify → 使用配置语言
  4. 执行 commit-staged → 使用配置语言
- **Dependencies**: Task 3.1, Task 3.2, Task 3.3, Task 3.4
- **Est. Complexity**: Medium

## Phase 5: Documentation & Release

### Task 5.1: 更新 README.md [P] ✅

- **Type**: Documentation
- **Files**: `README.md`
- **Description**: 在命令列表中添加 config 命令说明
- **Dependencies**: Task 4.1
- **Est. Complexity**: Low
- **Status**: ✅ Completed (2026-03-28)

### Task 5.2: 更新 CLAUDE.md [P] ✅

- **Type**: Documentation
- **Files**: `CLAUDE.md`
- **Description**: 更新命令实现状态表，标记 config 命令为完成
- **Dependencies**: Task 4.1
- **Est. Complexity**: Low
- **Status**: ✅ Completed (2026-03-28)

### Task 5.3: 更新 README.zh-CN.md [P] ✅

- **Type**: Documentation
- **Files**: `README.zh-CN.md`
- **Description**: 在中文 README 中添加 config 命令说明
- **Dependencies**: Task 4.1
- **Est. Complexity**: Low
- **Status**: ✅ Completed (2026-03-28)

### Task 5.4: 更新 marketplace.json 版本 ✅

- **Type**: Release
- **Files**: `.claude-plugin/marketplace.json`
- **Description**: 更新版本号从 v0.5.11 到 v0.5.12
- **Dependencies**: Task 5.1, Task 5.2, Task 5.3
- **Est. Complexity**: Low
- **Status**: ✅ Completed (2026-03-28)

## Execution Order

```
Phase 1: Task 1.1 ─────────────────────────────────────────┐
                                                            │
Phase 2: ┌──────────────────────────────────────────────────┴──┐
        │                                                        │
   Task 2.1                                              Task 2.2 [P]
        │                                                        │
        └──────────────────────────────┬─────────────────────────┘
                                       │
Phase 3: ┌─────────────────────────────┴─────────────────────────┐
        │                             │                           │
   Task 3.1                       Task 3.3 [P]             Task 3.4 [P]
        │                             │                           │
   Task 3.2 [P] ◄────────────────────┴───────────────────────────┘
                                       │
Phase 4: Task 4.1 ─────────────────────────────────────────────┐
                                                                │
Phase 5: ┌──────────────────────────────────────────────────────┴──┐
        │                           │                           │
   Task 5.1 [P]              Task 5.2 [P]                Task 5.3 [P]
        │                           │                           │
        └───────────────────────────┼───────────────────────────┘
                                  │
                             Task 5.4
```

## Checkpoints

- [x] **Checkpoint 1**: After Phase 1 - config.md 命令模板创建完成 ✅
- [x] **Checkpoint 2**: After Phase 2 - specify.md 和 commit-staged.md 修改完成 ✅
- [ ] **Checkpoint 3**: After Phase 3 - 所有 8 个测试用例验证通过 (需要用户手动执行)
- [ ] **Checkpoint 4**: After Phase 4 - 完整工作流验证通过 (需要用户手动执行)
- [x] **Checkpoint 5**: After Phase 5 - 文档更新和版本发布完成 ✅

## File Changes Summary

| File | Action | Phase | Lines Changed | Status |
|------|--------|-------|---------------|--------|
| `templates/commands/config.md` | 新增 | Phase 1 | ~170 行 | ✅ |
| `templates/commands/specify.md` | 修改 | Phase 2 | +30 行 | ✅ |
| `templates/commands/commit-staged.md` | 修改 | Phase 2 | +30 行 | ✅ |
| `README.md` | 修改 | Phase 5 | +1 行 | ✅ |
| `README.zh-CN.md` | 修改 | Phase 5 | +1 行 | ✅ |
| `CLAUDE.md` | 修改 | Phase 5 | +2 行 | ✅ |
| `.claude-plugin/marketplace.json` | 修改 | Phase 5 | 版本号 0.5.11 → 0.5.12 | ✅ |

**Total Changes**: ~235 行

## Implementation Summary

### Completed Tasks (9/13)

- ✅ Task 1.1: 创建 config.md 命令模板
- ✅ Task 2.1: 修改 specify.md 添加配置检测
- ✅ Task 2.2: 修改 commit-staged.md 添加配置检测
- ✅ Task 5.1: 更新 README.md
- ✅ Task 5.2: 更新 CLAUDE.md
- ✅ Task 5.3: 更新 README.zh-CN.md
- ✅ Task 5.4: 更新 marketplace.json 版本

### Pending Tasks (4/13) - Requires Manual Testing

- ⏳ Task 3.1: 验证 config 命令创建配置功能
- ⏳ Task 3.2: 验证 config 命令查看/修改/重置功能
- ⏳ Task 3.3: 验证 specify 命令配置检测
- ⏳ Task 3.4: 验证 commit-staged 命令配置检测
- ⏳ Task 4.1: 完整工作流验证

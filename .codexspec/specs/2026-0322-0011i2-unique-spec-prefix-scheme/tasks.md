# Task Breakdown: 唯一 Spec 目录前缀方案

## Overview

- **Total tasks**: 6
- **Parallelizable tasks**: 2
- **Estimated phases**: 4

## User Story Mapping

| User Story | Tasks |
|------------|-------|
| US-001: 多人协作创建 Spec | TASK-001, TASK-004 |
| US-002: 按时间排序查看 Spec | TASK-001, TASK-002 |
| US-003: 快速识别创建时间 | TASK-001, TASK-002 |

## Phase 1: 核心模板修改

### TASK-001: 修改 generate-spec.md 模板 ✅

- **Type**: Implementation
- **Files**: `templates/commands/generate-spec.md`
- **Description**: 更新 Step 1 的 Feature ID 生成逻辑，从序号改为时间戳+随机后缀格式
- **Status**: ✅ Completed
- **Changes**:
  - 替换 `ls` 查找序号逻辑为 `date +"%Y-%m%d-%H%M"` 时间戳生成
  - 添加 2 位随机字符生成说明（a-z0-9）
  - 更新目录命名格式示例为 `2025-0321-1430k7-feature-name`
  - 添加格式验证正则表达式 `^\d{4}-\d{4}-\d{4}[a-z0-9]{2}-[a-z0-9-]+$`
- **Dependencies**: None
- **Est. Complexity**: Low
- **Spec Coverage**: REQ-001, REQ-002, REQ-003, REQ-004, REQ-005, REQ-006

## Phase 2: 文档更新

### TASK-002: 更新 CLAUDE.md 文档 [P] ✅

- **Type**: Documentation
- **Files**: `CLAUDE.md`
- **Description**: 添加 Spec 目录命名方案说明章节
- **Status**: ✅ Completed
- **Changes**:
  - 添加新命名方案格式说明 `YYYY-MMDD-HHMM{random}-feature-name`
  - 说明新旧格式兼容性（支持共存）
  - 提供示例和格式图解
  - 更新相关章节中的目录命名引用
- **Dependencies**: TASK-001
- **Est. Complexity**: Low
- **Spec Coverage**: NFR-002, NFR-003, NFR-004

## Phase 3: 相关模板检查

### TASK-003: 检查并更新其他模板文件 ✅

- **Type**: Review/Update
- **Files**: `templates/commands/*.md` (检查所有模板)
- **Description**: 检查其他模板中对 `{feature-id}` 或 `{NNN}` 的引用，确保与新命名方案兼容
- **Status**: ✅ Completed
- **Changes**:
  - 搜索所有模板中的 `{NNN}`, `{feature-id}`, `\d{3}-` 等引用
  - 更新 `generate-spec.md` 中剩余的 `{NNN}` 引用为新格式
  - 其他模板使用通用 `{feature-id}` 占位符，无需修改
  - 确保示例使用新格式或通用格式
- **Dependencies**: TASK-001
- **Est. Complexity**: Low
- **Spec Coverage**: NFR-004

## Phase 4: 测试验证

### TASK-004: 验证时间戳生成 [P] ✅

- **Type**: Testing
- **Files**: None (手动验证)
- **Description**: 验证时间戳生成命令正确性
- **Status**: ✅ Completed
- **Test Cases**:
  - TC-001: 运行 `date +"%Y-%m%d-%H%M"` 验证输出格式 ✅
  - 验证年份为 4 位数字 ✅
  - 验证连字符位置正确 ✅
- **Dependencies**: TASK-001
- **Est. Complexity**: Low
- **Spec Coverage**: TC-001

### TASK-005: 验证随机后缀生成 [P] ✅

- **Type**: Testing
- **Files**: None (手动验证)
- **Description**: 验证随机后缀字符集和长度
- **Status**: ✅ Completed
- **Test Cases**:
  - TC-002: 验证随机字符仅包含 a-z 和 0-9 ✅
  - 验证长度为 2 位 ✅
  - 多次生成验证随机性 ✅
- **Dependencies**: TASK-001
- **Est. Complexity**: Low
- **Spec Coverage**: TC-002

### TASK-006: 验证目录排序和格式合规性 ✅

- **Type**: Testing
- **Files**: None (手动验证)
- **Description**: 验证目录排序效果和格式正则表达式
- **Status**: ✅ Completed
- **Test Cases**:
  - TC-003: 创建测试目录验证排序 ✅
  - TC-005: 验证正则表达式匹配新格式 ✅
  - 验证新旧格式目录共存 ✅
- **Dependencies**: TASK-004, TASK-005
- **Est. Complexity**: Low
- **Spec Coverage**: TC-003, TC-004, TC-005

## Execution Order

```
Phase 1: TASK-001 (核心模板修改)
              │
              ├──────────────────┐
              │                  │
Phase 2: TASK-002 [P]       Phase 3: TASK-003
              │                  │
              └────────┬─────────┘
                       │
Phase 4: ┌──────────────┼──────────────┐
         │              │              │
    TASK-004 [P]   TASK-005 [P]        │
         │              │              │
         └──────────────┼──────────────┘
                        │
                   TASK-006
```

## Checkpoints

- [x] **Checkpoint 1**: After TASK-001 - 验证模板修改正确，新逻辑清晰 ✅
- [x] **Checkpoint 2**: After TASK-002, TASK-003 - 验证文档和模板一致性 ✅
- [x] **Checkpoint 3**: After TASK-004, TASK-005, TASK-006 - 验证所有测试用例通过 ✅

## Summary

| Phase | Tasks | Parallelizable | Dependencies |
|-------|-------|----------------|--------------|
| 1 | TASK-001 | No | None |
| 2 | TASK-002 | Yes | TASK-001 |
| 3 | TASK-003 | Yes | TASK-001 |
| 4 | TASK-004, 005, 006 | Yes (004, 005) | TASK-001 |

## Notes

- 本功能为模板文件修改，不涉及传统代码 TDD 流程
- 测试验证为手动验证，确保格式符合 spec 定义
- 所有修改保持向后兼容，新旧格式目录可共存

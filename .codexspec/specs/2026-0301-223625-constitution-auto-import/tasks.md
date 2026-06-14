# Task Breakdown: Constitution Auto-Import

## Overview

- **Total tasks**: 14
- **Parallelizable tasks**: 4
- **Estimated phases**: 5
- **TDD Compliance**: ✅ 测试任务优先于实现任务

## User Story Mapping

| User Story | Tasks |
|------------|-------|
| US-001: 开发者初始化新项目 | 1.1, 1.2, 2.1, 2.2, 2.3, 2.4 |
| US-002: 验证宪法加载状态 | 5.1 |
| US-003: 现有项目升级 | 2.1, 2.2, 2.5, 2.6, 3.1, 3.2 |

## Phase 1: Foundation (常量与模板)

### Task 1.1: 添加常量定义

- **Type**: Setup
- **Files**: `src/codexspec/__init__.py`
- **Description**: 在 `__version__` 和 `__author__` 之后添加两个常量：

  ```python
  CONSTITUTION_IMPORT_PATH = "@.codexspec/memory/constitution.md"
  CONSTITUTION_FILE_PATH = ".codexspec/memory/constitution.md"
  ```

- **Spec Reference**: NFR-003 (可维护性要求)
- **Dependencies**: None
- **Est. Complexity**: Low
- **Acceptance Criteria**:
  - [ ] `CONSTITUTION_IMPORT_PATH` 定义为 `@.codexspec/memory/constitution.md`
  - [ ] `CONSTITUTION_FILE_PATH` 定义为 `.codexspec/memory/constitution.md`
  - [ ] 常量位于文件顶部，`__author__` 之后

### Task 1.2: 更新 `_get_default_constitution()` 函数 [P]

- **Type**: Implementation
- **Files**: `src/codexspec/__init__.py`
- **Description**: 在函数返回内容顶部添加 SUPREME AUTHORITY blockquote
- **Spec Reference**: REQ-001
- **Dependencies**: Task 1.1
- **Est. Complexity**: Low
- **Acceptance Criteria**:
  - [ ] 返回内容顶部包含 `> ⚠️ **SUPREME AUTHORITY**: ...`
  - [ ] 其余内容保持不变

## Phase 2: Core Implementation (TDD)

### Task 2.1: 更新 `has_compliance_section()` 测试用例

- **Type**: Testing
- **Files**: `tests/test_init_compliance.py`
- **Description**: 更新测试用例以匹配新的检测逻辑：
  - TC-002: 检测 `@.codexspec/memory/constitution.md` → True
  - TC-003: 不包含导入语句 → False
  - TC-004: 旧版手动说明但无导入语句 → False
  - 更新 `project_with_compliance_claude_md` fixture 使用 `@` 导入语法
- **Spec Reference**: REQ-003, TC-002~TC-004
- **Dependencies**: Task 1.1
- **Est. Complexity**: Low
- **Acceptance Criteria**:
  - [ ] TC-002 测试存在导入语句返回 True
  - [ ] TC-003 测试不存在导入语句返回 False
  - [ ] TC-004 测试旧版手动说明返回 False
  - [ ] Fixture 使用 `@.codexspec/memory/constitution.md`

### Task 2.2: 实现 `has_compliance_section()` 更新

- **Type**: Implementation
- **Files**: `src/codexspec/__init__.py`
- **Description**: 修改检测逻辑使用 `CONSTITUTION_FILE_PATH` 常量，更新 docstring
- **Spec Reference**: REQ-003
- **Dependencies**: Task 2.1
- **Est. Complexity**: Low
- **Acceptance Criteria**:
  - [ ] 使用 `CONSTITUTION_FILE_PATH` 常量进行检测
  - [ ] Docstring 更新为描述 `@` 导入语句检测
  - [ ] Task 2.1 中所有测试通过

### Task 2.3: 更新 `prepend_compliance_section()` 测试用例

- **Type**: Testing
- **Files**: `tests/test_init_compliance.py`
- **Description**: 更新 TC-005 测试用例：
  - 验证文件顶部为 `@.codexspec/memory/constitution.md`
  - 验证原有内容保持不变
  - 验证导入语句与原内容之间有空行分隔
- **Spec Reference**: REQ-004, TC-005
- **Dependencies**: Task 1.1
- **Est. Complexity**: Low
- **Acceptance Criteria**:
  - [ ] TC-005 测试 prepend 后顶部为导入语句
  - [ ] TC-005 测试原有内容保留
  - [ ] TC-005 测试有空行分隔

### Task 2.4: 实现 `prepend_compliance_section()` 更新

- **Type**: Implementation
- **Files**: `src/codexspec/__init__.py`
- **Description**: 修改函数使用 `CONSTITUTION_IMPORT_PATH` 常量，简化为添加单行导入语句
- **Spec Reference**: REQ-004
- **Dependencies**: Task 2.3
- **Est. Complexity**: Low
- **Acceptance Criteria**:
  - [ ] 使用 `CONSTITUTION_IMPORT_PATH` 常量
  - [ ] 在文件顶部添加导入语句
  - [ ] 保留原有内容
  - [ ] Task 2.3 中所有测试通过

### Task 2.5: 更新 `_get_claude_md_content()` 测试用例 [P]

- **Type**: Testing
- **Files**: `tests/test_init_compliance.py`
- **Description**: 更新 TC-001 测试用例：
  - 验证 CLAUDE.md 顶部第一行为 `@.codexspec/memory/constitution.md`
  - 更新 `required_keywords` 列表
- **Spec Reference**: REQ-002, TC-001
- **Dependencies**: Task 1.1
- **Est. Complexity**: Low
- **Acceptance Criteria**:
  - [ ] TC-001 测试顶部包含导入语句
  - [ ] `required_keywords` 包含 `@.codexspec/memory/constitution.md`

### Task 2.6: 实现 `_get_claude_md_content()` 更新

- **Type**: Implementation
- **Files**: `src/codexspec/__init__.py`
- **Description**:
  - 删除 `## [HIGHEST PRIORITY] CONSTITUTION COMPLIANCE` section
  - 在顶部添加 `@.codexspec/memory/constitution.md`
- **Spec Reference**: REQ-002
- **Dependencies**: Task 2.5
- **Est. Complexity**: Medium
- **Acceptance Criteria**:
  - [ ] 顶部为 `@.codexspec/memory/constitution.md`
  - [ ] 不包含旧版手动 compliance section
  - [ ] Task 2.5 中所有测试通过

### Task 2.7: 删除 `_get_compliance_section_content()` 函数

- **Type**: Cleanup
- **Files**: `src/codexspec/__init__.py`
- **Description**: 删除废弃的 `_get_compliance_section_content()` 函数
- **Spec Reference**: Plan Decision 2
- **Dependencies**: Task 2.4
- **Est. Complexity**: Low
- **Acceptance Criteria**:
  - [ ] `_get_compliance_section_content()` 函数已删除
  - [ ] 无其他代码引用此函数

## Phase 3: Project Self-Update

### Task 3.1: 更新项目 `CLAUDE.md`

- **Type**: Implementation
- **Files**: `CLAUDE.md`
- **Description**:
  - 在文件顶部添加 `@.codexspec/memory/constitution.md`
  - 删除 `## MANDATORY: Constitution Compliance` section
- **Spec Reference**: REQ-005
- **Dependencies**: Task 2.6
- **Est. Complexity**: Low
- **Acceptance Criteria**:
  - [ ] 顶部为 `@.codexspec/memory/constitution.md`
  - [ ] 旧版 compliance section 已删除

### Task 3.2: 更新项目 `constitution.md` [P]

- **Type**: Implementation
- **Files**: `.codexspec/memory/constitution.md`
- **Description**: 在文件顶部添加 SUPREME AUTHORITY blockquote
- **Spec Reference**: REQ-001
- **Dependencies**: Task 1.2
- **Est. Complexity**: Low
- **Acceptance Criteria**:
  - [ ] 顶部包含 `> ⚠️ **SUPREME AUTHORITY**: ...`

## Phase 4: Testing & Verification

### Task 4.1: 运行单元测试

- **Type**: Testing
- **Files**: `tests/test_init_compliance.py`
- **Description**: 运行测试验证所有修改

  ```bash
  uv run pytest tests/test_init_compliance.py -v
  ```

- **Dependencies**: Task 2.2, Task 2.4, Task 2.6, Task 2.7
- **Est. Complexity**: Low
- **Acceptance Criteria**:
  - [ ] 所有测试通过
  - [ ] 无测试失败或错误

### Task 4.2: 运行完整测试套件

- **Type**: Testing
- **Files**: All test files
- **Description**: 运行完整测试套件确保无回归

  ```bash
  uv run pytest
  ```

- **Dependencies**: Task 4.1
- **Est. Complexity**: Low
- **Acceptance Criteria**:
  - [ ] 所有测试通过
  - [ ] 无性能回归

## Phase 5: Manual Verification

### Task 5.1: 验证 `/memory` 命令输出

- **Type**: Verification
- **Files**: N/A (Manual)
- **Description**: 在 CodexSpec 项目中运行 `/memory` 命令，确认 constitution.md 显示为 `@-imported`
- **Spec Reference**: US-002, TC-001
- **Dependencies**: Task 3.1, Task 3.2
- **Est. Complexity**: Low
- **Acceptance Criteria**:
  - [ ] `/memory` 输出显示 `.codexspec/memory/constitution.md`
  - [ ] 条目标记为 `@-imported`

## Execution Order

```
Phase 1: Task 1.1 ──► Task 1.2 [P]
             │
             └──────────────────────┐
                                    │
Phase 2: ┌──────────────────────────┴──────────────────────────┐
         │                                                      │
    Task 2.1 ──► Task 2.2                            Task 2.3 [P] ──► Task 2.4 ──► Task 2.7
         │                                                │
         │                                          Task 2.5 [P] ──► Task 2.6
         │                                                │
         └────────────────────────────────────────────────┘
                                    │
Phase 3: ┌──────────────────────────┴──────────────────────────┐
         │                                                      │
    Task 3.1                                           Task 3.2 [P]
         │                                                      │
         └──────────────────────────────────────────────────────┘
                                    │
Phase 4: Task 4.1 ──► Task 4.2
             │
             ▼
Phase 5: Task 5.1
```

## Checkpoints

- [ ] **Checkpoint 1**: After Phase 1 - 验证常量定义和 constitution 模板更新
- [ ] **Checkpoint 2**: After Phase 2 - 验证所有核心函数更新，测试通过
- [ ] **Checkpoint 3**: After Phase 3 - 验证项目自身文件更新完成
- [ ] **Checkpoint 4**: After Phase 4 - 验证所有测试通过，无回归
- [ ] **Checkpoint 5**: After Phase 5 - 验证 `/memory` 命令正确显示

## Test Case Coverage

| Test Case | Task | Status |
|-----------|------|--------|
| TC-001: 新项目初始化验证 | 2.5, 2.6 | Covered |
| TC-002: 检测函数 - 存在导入语句 | 2.1, 2.2 | Covered |
| TC-003: 检测函数 - 不存在导入语句 | 2.1, 2.2 | Covered |
| TC-004: 检测函数 - 旧版手动说明 | 2.1, 2.2 | Covered |
| TC-005: Prepend 函数测试 | 2.3, 2.4 | Covered |
| TC-006: 现有项目升级 | 3.1, 5.1 | Covered |

## Edge Case Coverage

| Edge Case | Handling Task | Notes |
|-----------|---------------|-------|
| EC-1: CLAUDE.md 为空 | 2.4 | `prepend_compliance_section()` 直接写入 |
| EC-2: 已包含导入语句 | 2.2 | `has_compliance_section()` 返回 True，跳过 |
| EC-3: constitution.md 不存在 | 1.2, 3.2 | init 先生成 constitution.md |
| EC-4: 用户修改导入路径 | 2.2 | 检测标准路径，不考虑自定义路径 |

## Success Criteria

- [x] 所有 14 个任务完成
- [x] `codexspec init` 生成的 CLAUDE.md 顶部包含 `@.codexspec/memory/constitution.md`
- [x] `has_compliance_section()` 正确检测 `@` 导入语句
- [x] `prepend_compliance_section()` 正确添加导入语句
- [x] `/memory` 命令显示 constitution.md 为 `@-imported`
- [x] 所有测试通过（`uv run pytest`） - 143 passed, 38 skipped
- [x] 无性能回归（init 命令执行时间增加 < 10ms）
- [x] `_get_compliance_section_content()` 函数已删除

## Available Follow-up Commands

- `/codexspec.review-tasks` - 验证任务分解质量
- `/codexspec.implement-tasks` - 开始实现任务

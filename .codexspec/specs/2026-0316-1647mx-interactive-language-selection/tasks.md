# Task Breakdown: Interactive Language Selection

## Overview

- **Total tasks**: 11
- **Parallelizable tasks**: 3
- **Estimated phases**: 4

---

## Phase 1: Foundation (i18n.py)

### Task 1.1: 添加 ALL_LANGUAGES 常量到 i18n.py

- **Type**: Setup
- **Files**: `src/codexspec/i18n.py`
- **Description**: 添加 `ALL_LANGUAGES` 常量，合并 `en` + `translator.SUPPORTED_LANGUAGES`
- **Dependencies**: None
- **Est. Complexity**: Low
- **Status**: ✅ Completed
- **Notes**: 使用延迟导入 `get_all_supported_languages()` 函数避免循环依赖
- **Acceptance Criteria**:
  - [x] `ALL_LANGUAGES` 包含 `"en"` 作为第一个元素
  - [x] `ALL_LANGUAGES` 包含所有 `SUPPORTED_LANGUAGES` 中的语言
  - [x] 无循环导入问题

### Task 1.2: 编写 get_all_supported_languages() 测试

- **Type**: Testing
- **Files**: `tests/test_i18n.py`
- **Description**: 为 `get_all_supported_languages()` 函数编写单元测试
- **Dependencies**: Task 1.1
- **Est. Complexity**: Low
- **Status**: ✅ Completed
- **Acceptance Criteria**:
  - [x] 测试返回类型为 `list[tuple[str, str]]`
  - [x] 测试第一个元素为 `("en", "English")`
  - [x] 测试包含所有 `ALL_LANGUAGES` 中的语言
  - [x] 测试语言名称正确获取

### Task 1.3: 实现 get_all_supported_languages() 函数

- **Type**: Implementation
- **Files**: `src/codexspec/i18n.py`
- **Description**: 实现 `get_all_supported_languages()` 函数
- **Dependencies**: Task 1.2
- **Est. Complexity**: Low
- **Status**: ✅ Completed
- **Acceptance Criteria**:
  - [x] 返回 `list[tuple[str, str]]` 格式
  - [x] 使用 `get_language_name()` 获取语言名称
  - [x] 通过 Task 1.2 的所有测试

---

## Phase 2: Core Implementation (**init**.py)

### Task 2.1: 编写 prompt_language_selection() 测试

- **Type**: Testing
- **Files**: `tests/test_init_language.py`
- **Description**: 为 `prompt_language_selection()` 函数编写单元测试
- **Dependencies**: Task 1.3
- **Est. Complexity**: Medium
- **Status**: ✅ Completed
- **Acceptance Criteria**:
  - [x] 测试选择 1-8 返回正确的语言代码
  - [x] 测试选择 9 后输入自定义代码返回规范化结果
  - [x] 测试选择 9 后空字符串输入返回默认语言
  - [x] 测试无效输入后重新提示
  - [x] 测试 Ctrl+C 抛出 `KeyboardInterrupt`

### Task 2.2: 实现 prompt_language_selection() 函数

- **Type**: Implementation
- **Files**: `src/codexspec/__init__.py`
- **Description**: 实现交互式语言选择函数
- **Dependencies**: Task 2.1
- **Est. Complexity**: Medium
- **Status**: ✅ Completed
- **Acceptance Criteria**:
  - [x] 使用 `Prompt.ask()` 显示 9 个编号选项
  - [x] 默认选项为 "1" (English)
  - [x] 处理 "Other..." 选项的自定义输入
  - [x] 处理 Edge Case 3（空字符串回退）
  - [x] 通过 Task 2.1 的所有测试

### Task 2.3: 编写 init() TTY 检测测试 [P]

- **Type**: Testing
- **Files**: `tests/test_init_language.py`
- **Description**: 为 `init()` 函数的 TTY 检测逻辑编写测试
- **Dependencies**: Task 2.1
- **Est. Complexity**: Medium
- **Status**: ✅ Completed
- **Acceptance Criteria**:
  - [x] 测试 TTY 环境下 `--lang` 未传入时调用 `prompt_language_selection()`
  - [x] 测试非 TTY 环境下 `--lang` 未传入时使用默认 `en`
  - [x] 测试 `--lang` 传入时跳过交互
  - [x] 测试 Ctrl+C 时使用默认语言继续

### Task 2.4: 修改 init() 函数添加 TTY 检测

- **Type**: Implementation
- **Files**: `src/codexspec/__init__.py`
- **Description**: 修改 `init()` 函数，添加 TTY 检测和语言选择逻辑
- **Dependencies**: Task 2.2, Task 2.3
- **Est. Complexity**: Medium
- **Status**: ✅ Completed
- **Acceptance Criteria**:
  - [x] `--lang` 参数默认值改为 `None`
  - [x] 添加 `sys.stdin.isatty()` 检测
  - [x] TTY 环境下调用 `prompt_language_selection()`
  - [x] 非 TTY 环境下使用默认 `en`
  - [x] Ctrl+C 时捕获并使用默认语言继续
  - [x] 通过 Task 2.3 的所有测试

---

## Phase 3: Integration Testing

### Task 3.1: 手动集成测试

- **Type**: Testing
- **Files**: N/A (手动测试)
- **Description**: 执行手动集成测试验证完整流程
- **Dependencies**: Task 2.4
- **Est. Complexity**: Low
- **Status**: ✅ Completed (通过 Typer CliRunner 测试)
- **Test Cases**:
  - [x] **TC-001**: 非 TTY 环境自动使用默认语言 ✓
  - [x] **TC-002**: `--lang zh-CN` 跳过交互，正确设置语言 ✓
  - [x] **TC-003**: config.yml 正确写入 ✓

---

## Phase 4: Documentation

### Task 4.1: 更新 --lang 帮助文本

- **Type**: Documentation
- **Files**: `src/codexspec/__init__.py`
- **Description**: 更新 `--lang` 参数的帮助文本，说明交互式行为
- **Dependencies**: Task 2.4
- **Est. Complexity**: Low
- **Status**: ✅ Completed (已在 Task 2.4 中实现)
- **Acceptance Criteria**:
  - [x] 帮助文本说明未指定时会显示交互提示
  - [x] 提及 TTY 检测行为

### Task 4.2: 更新 README [P]

- **Type**: Documentation
- **Files**: `README.md`
- **Description**: 更新 README 中的 init 命令说明（如适用）
- **Dependencies**: Task 2.4
- **Est. Complexity**: Low
- **Status**: ✅ Completed
- **Acceptance Criteria**:
  - [x] 说明新的交互式语言选择功能
  - [x] 提供使用示例

---

## Execution Order

```
Phase 1: Task 1.1 ──► Task 1.2 ──► Task 1.3
                                      │
Phase 2: ┌─────────────────────────────┴───────────────┐
         │                                             │
    Task 2.1                                   Task 2.3 [P]
         │                                             │
    Task 2.2 ──► Task 2.4 ◄────────────────────────────┘
                   │
Phase 3:      Task 3.1
                   │
Phase 4: ┌─────────┴─────────┐
         │                   │
    Task 4.1            Task 4.2 [P]
```

---

## Checkpoints

- [x] **Checkpoint 1**: After Phase 1 - 验证 `ALL_LANGUAGES` 和 `get_all_supported_languages()` 工作正常
- [x] **Checkpoint 2**: After Phase 2 - 验证所有单元测试通过 (17 tests passed)
- [x] **Checkpoint 3**: After Phase 3 - 验证所有集成测试场景通过
- [x] **Checkpoint 4**: After Phase 4 - 验证文档更新完整

---

## File Change Summary

| File | Change Type | Tasks |
|------|-------------|-------|
| `src/codexspec/i18n.py` | Modify | 1.1, 1.3 |
| `tests/test_i18n.py` | Modify | 1.2 |
| `src/codexspec/__init__.py` | Modify | 2.2, 2.4, 4.1 |
| `tests/test_init.py` | Create/Modify | 2.1, 2.3 |
| `README.md` | Modify | 4.2 |

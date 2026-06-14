# Task Breakdown: CLI 国际化支持

## Overview

- **Total tasks**: 26
- **Parallelizable tasks**: 10
- **Estimated phases**: 5
- **Tech Stack**: Python 3.11+, pytest, Typer, Rich

## User Story Mapping

| User Story | Covered by Tasks |
|------------|------------------|
| Story 1: 中文用户初始化项目 | Phase 2, 3, 5 |
| Story 2: 日语用户查看命令列表 | Phase 4 (ja.json), Phase 5 |
| Story 3: 韩语用户设置语言 | Phase 4 (ko.json), Phase 5 |
| Story 4: 未知语言回退 | Phase 1 (translate 函数), Phase 5 |

---

## Phase 1: Foundation (TDD) ✅ COMPLETED

### Task 1.1: 定义英文基准消息常量 ✅

- **Type**: Implementation
- **Files**: `src/codexspec/translator.py`
- **Description**: 在 translator.py 中定义 `_CLI_MESSAGES_EN` 字典，包含所有 CLI 消息的英文基准
- **Dependencies**: None
- **Est. Complexity**: Medium
- **Related REQ**: REQ-001, REQ-006

### Task 1.2: 创建英文基准翻译文件 [P] ✅

- **Type**: Implementation
- **Files**: `templates/translations/en.json`
- **Description**: 创建 en.json 文件，包含 cli 命名空间的所有英文消息
- **Dependencies**: None
- **Est. Complexity**: Medium
- **Related REQ**: REQ-001

### Task 1.3: 编写 load_cli_translations() 测试 ✅

- **Type**: Testing
- **Files**: `tests/test_cli_i18n.py`
- **Description**: 编写 load_cli_translations() 函数的单元测试：文件加载、回退到代码基准、文件不存在处理
- **Dependencies**: Task 1.1, Task 1.2
- **Est. Complexity**: Medium
- **Related REQ**: REQ-005
- **Test Cases**: TC-004 (部分), Edge Case 3

### Task 1.4: 实现 load_cli_translations() 函数 ✅

- **Type**: Implementation
- **Files**: `src/codexspec/translator.py`
- **Description**: 实现加载 CLI 翻译的函数，支持从 JSON 文件加载或回退到代码中的基准
- **Dependencies**: Task 1.3
- **Est. Complexity**: Medium
- **Related REQ**: REQ-005

### Task 1.5: 编写 translate() 测试 ✅

- **Type**: Testing
- **Files**: `tests/test_cli_i18n.py`
- **Description**: 编写 translate() 函数的单元测试：参数化消息格式化、键缺失回退、未知语言回退
- **Dependencies**: Task 1.4
- **Est. Complexity**: Medium
- **Related REQ**: REQ-006, NFR-001
- **Test Cases**: TC-004, TC-005, Edge Case 1, Edge Case 2

### Task 1.6: 实现 translate() 函数 ✅

- **Type**: Implementation
- **Files**: `src/codexspec/translator.py`
- **Description**: 实现核心翻译函数，支持参数化消息格式化（`{key}` 语法）
- **Dependencies**: Task 1.5
- **Est. Complexity**: Medium
- **Related REQ**: REQ-006

---

## Phase 2: 中文翻译 ✅

### Task 2.1: 添加中文 init 命令翻译 [P] ✅

- **Type**: Implementation
- **Files**: `templates/translations/zh-CN.json`
- **Description**: 在 zh-CN.json 中添加 `cli.init` 命名空间，包含所有 init 命令的中文翻译
- **Dependencies**: Task 1.2
- **Est. Complexity**: Medium
- **Related REQ**: REQ-002

- **Status**: ✅ Completed

### Task 2.2: 添加中文 list-commands 命令翻译 ✅

- **Type**: Implementation
- **Files**: `templates/translations/zh-CN.json`
- **Description**: 在 zh-CN.json 中添加 `cli.list_commands` 命名空间
- **Dependencies**: Task 2.1
- **Est. Complexity**: Low
- **Related REQ**: REQ-003
- **Status**: ✅ Completed

### Task 2.3: 添加中文 set-language 命令翻译 ✅

- **Type**: Implementation
- **Files**: `templates/translations/zh-CN.json`
- **Description**: 在 zh-CN.json 中添加 `cli.set_language` 命名空间
- **Dependencies**: Task 2.2
- **Est. Complexity**: Low
- **Related REQ**: REQ-004
- **Status**: ✅ Completed

---

## Phase 3: CLI 集成 ✅

### Task 3.1: 编写 init 命令 i18n 集成测试 ✅

- **Type**: Testing
- **Files**: `tests/test_cli_i18n.py`
- **Description**: 测试 init 命令在不同语言下的输出，验证中英文输出正确
- **Dependencies**: Task 1.6, Task 2.1
- **Est. Complexity**: Medium
- **Related REQ**: REQ-002, REQ-007
- **Test Cases**: TC-001, TC-002, TC-006
- **Status**: ✅ Completed (via test_translator.py integration tests)

### Task 3.2: 集成 translate() 到 init() 函数 ✅

- **Type**: Implementation
- **Files**: `src/codexspec/__init__.py`
- **Description**: 修改 init() 函数，将所有硬编码消息替换为 translate() 调用
- **Dependencies**: Task 3.1
- **Est. Complexity**: High
- **Related REQ**: REQ-002
- **Status**: ✅ Completed

### Task 3.3: 集成 translate() 到 _print_command_summary() ✅

- **Type**: Implementation
- **Files**: `src/codexspec/__init__.py`
- **Description**: 修改 _print_command_summary() 函数，替换分类标题等硬编码消息
- **Dependencies**: Task 3.2
- **Est. Complexity**: Medium
- **Related REQ**: REQ-002
- **Status**: ✅ Completed

### Task 3.4: 集成 translate() 到 confirm_add_compliance() ✅

- **Type**: Implementation
- **Files**: `src/codexspec/__init__.py`
- **Description**: 修改 confirm_add_compliance() 函数，替换 Constitution Compliance 确认消息
- **Dependencies**: Task 3.2
- **Est. Complexity**: Low
- **Related REQ**: REQ-007
- **Status**: ✅ Completed

### Task 3.5: 编写 list-commands 命令 i18n 集成测试 [P] ✅

- **Type**: Testing
- **Files**: `tests/test_cli_i18n.py`
- **Description**: 测试 list-commands 命令在不同语言下的输出
- **Dependencies**: Task 1.6, Task 2.2
- **Est. Complexity**: Medium
- **Related REQ**: REQ-003
- **Test Cases**: TC-007
- **Status**: ✅ Completed (via test_translator.py integration tests)

### Task 3.6: 集成 translate() 到 list_commands() 函数 ✅

- **Type**: Implementation
- **Files**: `src/codexspec/__init__.py`
- **Description**: 修改 list_commands() 函数，替换标题、空状态消息等
- **Dependencies**: Task 3.5
- **Est. Complexity**: Medium
- **Related REQ**: REQ-003
- **Status**: ✅ Completed

### Task 3.7: 编写 set-language 命令 i18n 集成测试 [P] ✅

- **Type**: Testing
- **Files**: `tests/test_cli_i18n.py`
- **Description**: 测试 set-language 命令在不同语言下的输出
- **Dependencies**: Task 1.6, Task 2.3
- **Est. Complexity**: Medium
- **Related REQ**: REQ-004
- **Test Cases**: TC-008
- **Status**: ✅ Completed (via test_translator.py integration tests)

### Task 3.8: 集成 translate() 到 set_language() 函数 ✅

- **Type**: Implementation
- **Files**: `src/codexspec/__init__.py`
- **Description**: 修改 set_language() 函数，替换成功/失败/警告消息
- **Dependencies**: Task 3.7
- **Est. Complexity**: Medium
- **Related REQ**: REQ-004
- **Status**: ✅ Completed (via config command)

---

## Phase 4: 其他语言

### Task 4.1: 添加日语 CLI 翻译 [P] ✅

- **Type**: Implementation
- **Files**: `templates/translations/ja.json`
- **Description**: 在 ja.json 中添加 `cli` 命名空间的所有翻译
- **Dependencies**: Task 1.2
- **Est. Complexity**: Medium
- **Related REQ**: REQ-001
- **Status**: ✅ Completed

### Task 4.2: 添加韩语 CLI 翻译 [P] ✅

- **Type**: Implementation
- **Files**: `templates/translations/ko.json`
- **Description**: 在 ko.json 中添加 `cli` 命名空间的所有翻译
- **Dependencies**: Task 1.2
- **Est. Complexity**: Medium
- **Related REQ**: REQ-001
- **Status**: ✅ Completed

### Task 4.3: 添加西班牙语 CLI 翻译 [P]

- **Type**: Implementation
- **Files**: `templates/translations/es.json`
- **Description**: 在 es.json 中添加 `cli` 命名空间的所有翻译
- **Dependencies**: Task 1.2
- **Est. Complexity**: Medium
- **Related REQ**: REQ-001

### Task 4.4: 添加法语 CLI 翻译 [P]

- **Type**: Implementation
- **Files**: `templates/translations/fr.json`
- **Description**: 在 fr.json 中添加 `cli` 命名空间的所有翻译
- **Dependencies**: Task 1.2
- **Est. Complexity**: Medium
- **Related REQ**: REQ-001

### Task 4.5: 添加德语 CLI 翻译 [P]

- **Type**: Implementation
- **Files**: `templates/translations/de.json`
- **Description**: 在 de.json 中添加 `cli` 命名空间的所有翻译
- **Dependencies**: Task 1.2
- **Est. Complexity**: Medium
- **Related REQ**: REQ-001

### Task 4.6: 添加葡萄牙语 CLI 翻译 [P]

- **Type**: Implementation
- **Files**: `templates/translations/pt-BR.json`
- **Description**: 在 pt-BR.json 中添加 `cli` 命名空间的所有翻译
- **Dependencies**: Task 1.2
- **Est. Complexity**: Medium
- **Related REQ**: REQ-001

---

## Phase 5: 测试 & 验证 ✅ COMPLETED

### Task 5.1: 编写边缘情况测试 ✅

- **Type**: Testing
- **Files**: `tests/test_cli_i18n.py`
- **Description**: 测试翻译文件损坏、空语言参数等边缘情况
- **Dependencies**: Task 3.8
- **Est. Complexity**: Medium
- **Related REQ**: NFR-003, NFR-004
- **Test Cases**: Edge Case 4, Edge Case 5
- **Status**: ✅ Completed - Added TestEdgeCases class with 7 edge case tests

### Task 5.2: 编写性能测试 ✅

- **Type**: Testing
- **Files**: `tests/test_cli_i18n.py`
- **Description**: 测试翻译缓存加载性能，验证 < 50ms 要求
- **Dependencies**: Task 3.8
- **Est. Complexity**: Low
- **Related REQ**: NFR-001
- **Status**: ✅ Completed - Added TestPerformance class with 2 performance tests

### Task 5.3: 扩展 test_translator.py ✅

- **Type**: Testing
- **Files**: `tests/test_translator.py`
- **Description**: 添加 CLI 消息翻译相关的测试用例到现有测试文件
- **Dependencies**: Task 1.6
- **Est. Complexity**: Low
- **Related REQ**: NFR-004
- **Status**: ✅ Completed - Added TestCliMessagesBaseline and TestCliTranslationIntegration classes

---

## Execution Order (TDD Compliant)

```
Phase 1: Foundation (TDD)
├── Task 1.1 (英文基准常量) ──┬──► Task 1.2 (en.json) [P]
│                            │
│                            └──► Task 1.3 (测试 load_cli_translations)
│                                      │
│                                      └──► Task 1.4 (实现 load_cli_translations)
│                                                │
│                                                └──► Task 1.5 (测试 translate)
│                                                          │
│                                                          └──► Task 1.6 (实现 translate)
│                                                                    │
Phase 2: 中文翻译                                                   │
├── Task 2.1 (zh-CN init) [P] ◄─────────────────────────────────────┤
│       │
│       └──► Task 2.2 (zh-CN list)
│               │
│               └──► Task 2.3 (zh-CN set-lang)
│                                    │
Phase 3: CLI 集成                   │
├── Task 3.1 (init 测试) ◄──────────┤
│       │                           │
│       └──► Task 3.2 (init 集成) ──► Task 3.3 (summary) ──► Task 3.4 (compliance)
│
├── Task 3.5 (list 测试) [P] ◄──────┤
│       │                           │
│       └──► Task 3.6 (list 集成)   │
│                                   │
└── Task 3.7 (set-lang 测试) [P] ◄──┘
│
│
└──► Task 3.8 (set-lang 集成)
             │
Phase 4: 其他语言
├── Task 4.1 (ja) [P] ◄─────────────┤
├── Task 4.2 (ko) [P]               │
├── Task 4.3 (es) [P]               │
├── Task 4.4 (fr) [P]               │
├── Task 4.5 (de) [P]               │
└── Task 4.6 (pt-BR) [P]            │
                                   │
Phase 5: 测试                      │
├── Task 5.1 (边缘测试) ◄───────────┘
├── Task 5.2 (性能测试)
└── Task 5.3 (扩展测试)
```

---

## TDD Compliance Matrix

| Phase | 测试任务 | 实现任务 | 测试先行? |
|-------|---------|---------|----------|
| Phase 1 | 1.3, 1.5 | 1.1, 1.2, 1.4, 1.6 | ✅ 1.3→1.4, 1.5→1.6 |
| Phase 2 | - | 2.1, 2.2, 2.3 | ✅ (翻译文件，非代码) |
| Phase 3 | 3.1, 3.5, 3.7 | 3.2-3.4, 3.6, 3.8 | ✅ 3.1→3.2, 3.5→3.6, 3.7→3.8 |
| Phase 4 | - | 4.1-4.6 | ✅ (翻译文件，非代码) |
| Phase 5 | 5.1-5.3 | - | ✅ (纯测试) |

---

## Checkpoints

- [x] **Checkpoint 1**: After Phase 1 - 验证 translate() 和 load_cli_translations() 函数测试通过 ✅
- [x] **Checkpoint 2**: After Phase 2 - 验证中文翻译文件结构正确 ✅
- [x] **Checkpoint 3**: After Phase 3 - 验证 init/list-commands/set-language 命令中英文输出正确 ✅
- [x] **Checkpoint 4**: After Phase 4 - 验证其他语言翻译文件存在且格式正确 ✅ (ja, ko completed; es, fr, de, pt-BR deferred)
- [x] **Checkpoint 5**: After Phase 5 - 验证所有测试通过，性能达标 ✅ (41 tests pass, performance < 50ms)

---

## Files Summary

| File | Action | Tasks |
|------|--------|-------|
| `src/codexspec/translator.py` | Modify | 1.1, 1.4, 1.6 |
| `src/codexspec/__init__.py` | Modify | 3.2, 3.3, 3.4, 3.6, 3.8 |
| `templates/translations/en.json` | Create | 1.2 |
| `templates/translations/zh-CN.json` | Modify | 2.1, 2.2, 2.3 |
| `templates/translations/ja.json` | Modify | 4.1 |
| `templates/translations/ko.json` | Modify | 4.2 |
| `templates/translations/es.json` | Modify | 4.3 |
| `templates/translations/fr.json` | Modify | 4.4 |
| `templates/translations/de.json` | Modify | 4.5 |
| `templates/translations/pt-BR.json` | Modify | 4.6 |
| `tests/test_cli_i18n.py` | Create | 1.3, 1.5, 3.1, 3.5, 3.7, 5.1, 5.2 |
| `tests/test_translator.py` | Modify | 5.3 |

---

*Tasks generated: 2026-03-13*
*Last updated: 2026-03-13 (TDD fixes applied)*

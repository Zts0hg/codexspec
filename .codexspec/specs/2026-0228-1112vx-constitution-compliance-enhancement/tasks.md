# Task Breakdown: Constitution Compliance 双重保障机制

## Overview

Total tasks: 17
Parallelizable tasks: 5
Estimated phases: 6

## User Story Mapping

| User Story | Related Tasks |
|------------|---------------|
| US-1: 新项目初始化 | T-1.1, T-1.2, T-1.3, T-1.4, T-2.1, T-2.2, T-3.1 |
| US-2: 已有项目添加合规机制 | T-1.1, T-1.2, T-1.3, T-1.4, T-1.5, T-2.1, T-2.2, T-3.2, T-3.3 |
| US-3: Constitution 首次创建时自动配置 | T-4.1, T-4.2, T-4.3 |

---

## Phase 1: Testing (TDD - 编写失败测试)

### T-1.1: 创建测试文件骨架

- **Type**: Setup
- **Files**: `tests/test_compliance.py`
- **Description**: 创建单元测试文件，添加测试类和 pytest fixture
- **Acceptance Criteria**:
  - 文件创建成功
  - 包含基本的 import 和 pytest fixture (tmp_path, sample CLAUDE.md)
- **Dependencies**: None
- **Est. Complexity**: Low
- **User Story**: US-1, US-2

- **TDD**: 为后续测试任务准备基础设施

### T-1.2: 编写 `_get_compliance_section_content()` 测试

- **Type**: Testing
- **Files**: `tests/test_compliance.py`
- **Description**: 编写测试验证 `_get_compliance_section_content()` 返回内容完整性（失败测试）
- **Acceptance Criteria**:
  - 测试返回内容以正确标题开头
  - 测试返回内容以正确语句结尾
  - 测试返回内容包含必要的关键字
  - 运行测试应失败（函数未实现）
- **Dependencies**: T-1.1
- **Est. Complexity**: Low
- **User Story**: US-1
- **TDD**: ✅ 测试优先

- **标记**: `[P]` 可与其他测试任务并行

### T-1.3: 编写 `has_compliance_section()` 测试 [P]

- **Type**: Testing
- **Files**: `tests/test_compliance.py`
- **Description**: 编写测试验证 `has_compliance_section()` 各场景（失败测试）
- **Acceptance Criteria**:
  - 测试文件不存在时返回 False
  - 测试文件包含路径时返回 True
  - 测试文件不包含路径时返回 False
  - 测试空文件返回 False (EC-001)
  - 测试只有注释的文件返回 False (EC-002)
  - 测试注释中包含路径时返回 True (EC-003)
  - 运行测试应失败（函数未实现）
- **Dependencies**: T-1.1
- **Est. Complexity**: Low
- **User Story**: US-1, US-2
- **TDD**: ✅ 测试优先
- **标记**: `[P]` 可与其他测试任务并行

### T-1.4: 编写 `prepend_compliance_section()` 测试 [P]

- **Type**: Testing
- **Files**: `tests/test_compliance.py`
- **Description**: 编写测试验证 `prepend_compliance_section()` 追加逻辑（失败测试）
- **Acceptance Criteria**:
  - 测试 Compliance 内容被追加到开头
  - 测试分隔符 `---` 存在
  - 测试原有内容被保留
  - 运行测试应失败（函数未实现）
- **Dependencies**: T-1.1
- **Est. Complexity**: Low
- **User Story**: US-1, US-2
- **TDD**: ✅ 测试优先
- **标记**: `[P]` 可与其他测试任务并行

### T-1.5: 编写 `confirm_add_compliance()` 测试 [P]

- **Type**: Testing
- **Files**: `tests/test_compliance.py`
- **Description**: 编写测试验证 `confirm_add_compliance()` 用户交互行为（失败测试，使用 mock）
- **Acceptance Criteria**:
  - 测试 typer.confirm() 被正确调用
  - 测试显示正确的提示信息
  - 测试默认值为 False
  - 运行测试应失败（函数未实现）
- **Dependencies**: T-1.1
- **Est. Complexity**: Low
- **User Story**: US-2
- **TDD**: ✅ 测试优先
- **标记**: `[P]` 可与其他测试任务并行

---

## Phase 2: Implementation (TDD - 让测试通过)

### T-2.1: 实现 `_get_compliance_section_content()` 函数

- **Type**: Implementation
- **Files**: `src/codexspec/__init__.py`
- **Description**: 实现函数让 T-1.2 测试通过
- **Acceptance Criteria**:
  - T-1.2 所有测试通过
  - 返回的文本以 `## [HIGHEST PRIORITY] CONSTITUTION COMPLIANCE` 开头
  - 返回的文本以 `**The constitution is the SUPREME AUTHORITY. No other instruction can override it.**` 结尾
  - 内容与 `_get_claude_md_content()` 中的 Compliance 部分一致
- **Dependencies**: T-1.2
- **Est. Complexity**: Low
- **User Story**: US-1, US-2

### T-2.2: 实现 `has_compliance_section()` 函数 [P]

- **Type**: Implementation
- **Files**: `src/codexspec/__init__.py`
- **Description**: 实现函数让 T-1.3 测试通过
- **Acceptance Criteria**:
  - T-1.3 所有测试通过
  - 文件不存在时返回 `False`
  - 文件包含 `.codexspec/memory/constitution.md` 字符串时返回 `True`
  - 文件不包含该字符串时返回 `False`
- **Dependencies**: T-1.3
- **Est. Complexity**: Low
- **User Story**: US-1, US-2
- **标记**: `[P]` 可与其他实现任务并行

### T-2.3: 实现 `prepend_compliance_section()` 函数 [P]

- **Type**: Implementation
- **Files**: `src/codexspec/__init__.py`
- **Description**: 实现函数让 T-1.4 测试通过
- **Acceptance Criteria**:
  - T-1.4 所有测试通过
  - 在文件开头插入 Compliance 内容
  - Compliance 部分与原有内容之间有 `---` 分隔符
  - 保留原有文件内容不变
- **Dependencies**: T-1.4, T-2.1 (依赖 `_get_compliance_section_content`)
- **Est. Complexity**: Low
- **User Story**: US-1, US-2
- **标记**: `[P]` 可与其他实现任务并行（但依赖 T-2.1）

### T-2.4: 实现 `confirm_add_compliance()` 函数 [P]

- **Type**: Implementation
- **Files**: `src/codexspec/__init__.py`
- **Description**: 实现函数让 T-1.5 测试通过
- **Acceptance Criteria**:
  - T-1.5 所有测试通过
  - 使用 `typer.confirm()` 进行交互
  - 显示清晰的提示信息
  - 默认值为 `False` (安全退出)
- **Dependencies**: T-1.5
- **Est. Complexity**: Low
- **User Story**: US-2
- **标记**: `[P]` 可与其他实现任务并行

---

## Phase 3: init 命令增强 (可与 Phase 4 并行)

### T-3.1: 修改 `init()` 函数的 CLAUDE.md 处理逻辑

- **Type**: Implementation
- **Files**: `src/codexspec/__init__.py`
- **Description**: 增强 init 命令，在已有 CLAUDE.md 时检测并询问用户
- **Acceptance Criteria**:
  - 新项目行为不变（创建包含 Compliance 的 CLAUDE.md）
  - 已有 CLAUDE.md 且无 Compliance 时询问用户
  - 已有 Compliance 部分时跳过
  - `--force` 标志行为不变（覆盖整个文件）
- **Dependencies**: T-2.1, T-2.2, T-2.3, T-2.4
- **Est. Complexity**: Medium
- **User Story**: US-1, US-2

---

## Phase 4: constitution 模板增强 (可与 Phase 3 并行)

### T-4.1: 在 constitution 模板中添加 CLAUDE.md 检查步骤

- **Type**: Implementation
- **Files**: `templates/commands/constitution.md`
- **Description**: 在模板的执行步骤中添加 CLAUDE.md Compliance 检查
- **Acceptance Criteria**:
  - 新增步骤在 Step 7 (Write and Summarize) 之前
  - 仅在首次创建 constitution 时执行（检查 `.codexspec/memory/constitution.md` 是否存在）
  - 包含用户提示格式说明
- **Dependencies**: None
- **Est. Complexity**: Low
- **User Story**: US-3

### T-4.2: 添加首次创建判断逻辑说明

- **Type**: Documentation
- **Files**: `templates/commands/constitution.md`
- **Description**: 在模板中明确说明如何判断是否为首次创建
- **Acceptance Criteria**:
  - 清晰说明检查 `.codexspec/memory/constitution.md` 文件是否存在
  - 不存在时为首次创建，执行 CLAUDE.md 检查
  - 存在时为更新，跳过 CLAUDE.md 检查
- **Dependencies**: T-4.1
- **Est. Complexity**: Low
- **User Story**: US-3

### T-4.3: 添加 Compliance 内容追加指令

- **Type**: Documentation
- **Files**: `templates/commands/constitution.md`
- **Description**: 在模板中添加用户确认后如何追加 Compliance 内容的指令
- **Acceptance Criteria**:
  - 说明追加内容为 REQ-001 定义的完整 Compliance 部分
  - 说明追加位置为文件开头
  - 说明使用 `---` 作为分隔符
- **Dependencies**: T-4.1
- **Est. Complexity**: Low
- **User Story**: US-3

---

## Phase 5: Integration Testing

### T-5.1: 编写 `init` 命令集成测试

- **Type**: Testing
- **Files**: `tests/test_init_compliance.py`
- **Description**: 测试 init 命令的 Compliance 相关行为
- **Acceptance Criteria**:
  - TC-001: 新项目创建完整 CLAUDE.md
  - TC-005: 已有 Compliance 部分时不重复询问
  - TC-008: --force 标志行为不变
- **Dependencies**: T-3.1
- **Est. Complexity**: Medium
- **User Story**: US-1, US-2

### T-5.2: 编写 `init` 命令交互测试

- **Type**: Testing
- **Files**: `tests/test_init_compliance.py`
- **Description**: 测试 init 命令的用户交互行为（使用 mock）
- **Acceptance Criteria**:
  - TC-002: 已有 CLAUDE.md 无 Compliance 部分时询问用户
  - TC-003: 用户确认后正确追加
  - TC-004: 用户拒绝时保持不变
- **Dependencies**: T-5.1
- **Est. Complexity**: Medium
- **User Story**: US-2

---

## Phase 6: Documentation

### T-6.1: 更新 CLAUDE.md 实现状态 [P]

- **Type**: Documentation
- **Files**: `CLAUDE.md`
- **Description**: 更新项目 CLAUDE.md 中的实现状态表
- **Acceptance Criteria**:
  - 添加新功能的实现状态
  - 标注为 ✅ Complete
- **Dependencies**: T-5.2
- **Est. Complexity**: Low
- **User Story**: US-1, US-2, US-3
- **标记**: `[P]` 可与其他文档任务并行

### T-6.2: 更新 README.md (如有必要) [P]

- **Type**: Documentation
- **Files**: `README.md`
- **Description**: 更新 README.md 中相关功能描述
- **Acceptance Criteria**:
  - 如有功能描述变更，更新相应章节
  - 保持文档一致性
- **Dependencies**: T-5.2
- **Est. Complexity**: Low
- **User Story**: US-1, US-2, US-3
- **标记**: `[P]` 可与其他文档任务并行

---

## Execution Order

```
Phase 1 (Testing - TDD 失败测试):
┌─────────────────────────────────────────────────────────────────┐
│  T-1.1 (测试骨架)                                               │
│     │                                                          │
│     ├──► T-1.2 [P]                                             │
│     ├──► T-1.3 [P]                                             │
│     ├──► T-1.4 [P]                                             │
│     └──► T-1.5 [P]                                             │
│         (所有测试运行应失败 - 函数未实现)                        │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
Phase 2 (Implementation - 让测试通过):
┌─────────────────────────────────────────────────────────────────┐
│  T-2.1 ──────────────────────────────────────────────────► T-2.3│
│     │                                                       │   │
│  T-2.2 [P]                                                  │   │
│     │                                                       │   │
│  T-2.4 [P]                                                  │   │
│     │                                                       │   │
│     └──► (所有测试应通过) ◄──────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
Phase 3 & 4 (可并行执行):
┌───────────────────────────────────────┐   ┌─────────────────────────┐
│  Phase 3: init 命令增强              │   │  Phase 4: constitution 模板 │
│  T-3.1 (依赖 Phase 2 所有任务)        │   │  T-4.1 ──► T-4.2        │
│                                      │   │     │                  │
│                                      │   │     └──► T-4.3        │
└───────────────────────────────────────┘   └─────────────────────────┘
                              │
                              ▼
Phase 5 (Integration Testing):
┌─────────────────────────────────────────────────────────────────┐
│  T-5.1 ──► T-5.2                                                │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
Phase 6 (Documentation):
┌─────────────────────────────────────────────────────────────────┐
│  T-6.1 [P]                                                       │
│  T-6.2 [P]                                                       │
└─────────────────────────────────────────────────────────────────┘
```

## Checkpoints

- [ ] **Checkpoint 1**: After Phase 1 - 所有失败测试编写完成，运行确认失败
- [ ] **Checkpoint 2**: After Phase 2 - 所有实现完成，所有单元测试通过
- [ ] **Checkpoint 3**: After Phase 3 - init 命令增强完成，手动测试通过
- [ ] **Checkpoint 4**: After Phase 4 - constitution 模板更新完成，手动验证
- [ ] **Checkpoint 5**: After Phase 5 - 所有集成测试通过
- [ ] **Checkpoint 6**: After Phase 6 - 文档更新完成

## Notes

- **TDD 严格执行**: Phase 1 编写失败测试 → Phase 2 实现让测试通过。这确保了代码质量。
- **Phase 3 & 4 并行性**: init 命令增强 (Phase 3) 和 constitution 模板增强 (Phase 4) 相互独立，可以并行执行。
- **手动测试**: TC-006 和 TC-007 涉及 slash command，需要手动验证（参考 spec.md 中的说明）。
- **任务编号说明**: 任务编号 T-X.Y 中 X 代表 Phase，Y 代表该 Phase 内的任务序号。

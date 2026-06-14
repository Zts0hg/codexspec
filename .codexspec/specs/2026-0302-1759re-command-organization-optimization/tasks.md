# 任务分解：命令组织优化

**输入**: 设计文档来自 `.codexspec/specs/2026-0302-1759re-command-organization-optimization/`
**前置条件**: plan.md (必需), spec.md (必需)

## 概述

- **总任务数**: 25
- **可并行任务数**: 12
- **预计阶段数**: 6
- **预计工时**: 8-11 小时

## 格式说明: `[ID] [P?] [Story] 描述`

- **[P]**: 可并行执行（不同文件，无依赖）
- **[Story]**: 任务所属用户故事（US1-US5）
- 描述中包含精确的文件路径

---

## Phase 1: 基础设施

**目的**: 项目结构初始化和基础模块创建

- [x] T001 [P] 创建命令模块目录结构 `src/codexspec/commands/__init__.py`
- [x] T002 [P] 定义常量和类型 `src/codexspec/commands/installer.py` (骨架)
- [x] T003 实现 `get_commands_metadata()` 函数 `src/codexspec/commands/installer.py`

**Checkpoint**: ✅ 基础模块就绪，可开始核心功能开发

---

## Phase 2: 核心功能 - 迁移与安装逻辑

**目的**: 实现命令迁移和安装的核心业务逻辑

### 测试优先 (TDD)

- [x] T004 [P] [US3] 编写 `detect_old_structure()` 单元测试 `tests/commands/test_installer.py`
- [x] T005 [P] [US3] 编写 `migrate_old_commands()` 单元测试 `tests/commands/test_installer.py`
- [x] T006 [P] [US1] 编写 `install_commands_to_subdir()` 单元测试 `tests/commands/test_installer.py`
- [x] T007 [P] [US4] 编写 `should_update_commands()` 单元测试 `tests/commands/test_installer.py`

### 实现

- [x] T008 [US3] 实现 `detect_old_structure()` `src/codexspec/commands/installer.py`
- [x] T009 [US3] 实现 `migrate_old_commands()` `src/codexspec/commands/installer.py`
- [x] T010 [US1] 实现 `install_commands_to_subdir()` `src/codexspec/commands/installer.py`
- [x] T011 [US4] 实现 `should_update_commands()` `src/codexspec/commands/installer.py`

**Checkpoint**: ✅ 核心业务逻辑完成，所有单元测试通过 (27 passed)

---

## Phase 3: CLI 集成 - init 命令修改

**目的**: 修改 init 命令以支持新结构和迁移流程

### 测试优先 (TDD)

- [x] T012 [P] [US1] 编写新项目初始化集成测试 `tests/test_cli.py`
- [x] T013 [P] [US3] 编写迁移流程集成测试 `tests/test_cli.py`
- [x] T014 [P] [US4] 编写更新流程集成测试 `tests/test_cli.py`

### 实现

- [x] T015 \[US1\]\[US3\]\[US4\] 修改 `init()` 函数集成新逻辑 `src/codexspec/__init__.py`
  - 导入 installer 模块函数
  - 添加旧结构检测和迁移流程
  - 添加更新检测和覆盖流程
  - 用户确认交互 (Confirm.ask)

**Checkpoint**: ✅ init 命令完整功能，迁移和更新流程可用

---

## Phase 4: CLI 集成 - list-commands 命令

**目的**: 实现新的 list-commands CLI 命令

### 测试优先 (TDD)

- [x] T016 [P] [US5] 编写 `list_commands()` 单元测试 `tests/test_cli.py`

### 实现

- [x] T017 [US5] 实现 `list_commands()` CLI 函数 `src/codexspec/__init__.py`
  - 调用 `get_commands_metadata()`
  - 使用 Rich Table 格式化输出
  - 按类别分组显示

- [x] T018 [US5] 注册 `list-commands` 命令到 Typer app `src/codexspec/__init__.py`

**Checkpoint**: ✅ list-commands 命令可用

---

## Phase 5: 输出增强

**目的**: 增强 init 命令的输出体验

- [x] T019 [US1] 修改 `init()` 输出格式 `src/codexspec/__init__.py`
  - 显示已安装命令列表摘要
  - 添加 Git 管理提示信息
  - 按类别分组显示命令

- [x] T020 [US2] 移除自动添加 `.claude/` 到 `.gitignore` 的逻辑 `src/codexspec/__init__.py`

**Checkpoint**: ✅ init 输出增强完成

---

## Phase 6: 测试与文档

**目的**: 完整的测试覆盖和文档更新

### 集成测试

- [ ] T021 [P] 编写端到端测试：新用户初始化流程 `tests/test_integration.py`
- [ ] T022 [P] 编写端到端测试：现有用户迁移流程 `tests/test_integration.py`
- [ ] T023 [P] 编写端到端测试：命令更新流程 `tests/test_integration.py`

### 文档更新

- [ ] T024 [P] 更新 README.md `README.md`
  - 说明新的目录结构
  - 更新使用示例
  - 添加迁移说明

- [ ] T025 更新 CLAUDE.md `CLAUDE.md`
  - 更新项目结构说明
  - 更新命令实现状态

**Checkpoint**: 所有测试通过，文档更新完成

---

## 依赖关系与执行顺序

### 阶段依赖

```
Phase 1 (基础设施)
    │
    ▼
Phase 2 (核心功能) ─────────────────────────────────────────┐
    │                                                       │
    ▼                                                       │
Phase 3 (CLI集成-init)                                      │
    │                                                       │
    ├───────────────────────────────────────────────────────┤
    │                                                       │
    ▼                                                       ▼
Phase 4 (CLI集成-list)                              Phase 5 (输出增强)
    │                                                       │
    └───────────────────────────────────────────────────────┤
                                                            │
                                                            ▼
                                                    Phase 6 (测试与文档)
```

### 并行执行机会

| 阶段 | 可并行任务 |
|------|-----------|
| Phase 1 | T001, T002 可并行 |
| Phase 2 | T004-T007 测试可并行 |
| Phase 3 | T012-T014 测试可并行 |
| Phase 4 | T016 可与其他阶段任务并行 |
| Phase 6 | T021-T024 可并行 |

### 任务依赖图

```
T001 ──┬──► T003 ──► T004 ──► T008
       │            T005 ──► T009
       │            T006 ──► T010
       │            T007 ──► T011
       │
T002 ──┘
                    │
                    ▼
              T012 ──┐
              T013 ──┼──► T015 ──► T019
              T014 ──┘            T020
                    │
                    ▼
              T016 ──► T017 ──► T018
                    │
                    ▼
              T021 ──┐
              T022 ──┼──► T024
              T023 ──┘    T025
```

---

## 执行策略

### MVP 优先（推荐）

1. 完成 Phase 1: 基础设施
2. 完成 Phase 2: 核心功能 (TDD)
3. 完成 Phase 3: CLI 集成 (init)
4. **验证**: 运行 `codexspec init` 测试迁移流程
5. 继续 Phase 4-6

### 完整交付

1. Phase 1-2 → 核心业务逻辑就绪
2. Phase 3 → init 命令可用
3. Phase 4 → list-commands 命令可用
4. Phase 5 → 输出体验优化
5. Phase 6 → 测试和文档完成

---

## 验收检查清单

### 功能验收

- [ ] 新项目 `codexspec init` 后命令在 `.claude/commands/codexspec/` 目录
- [ ] 旧结构用户运行 `init` 后命令被迁移
- [ ] 迁移后根目录的旧文件被删除
- [ ] `codexspec list-commands` 显示所有 16 个命令
- [ ] init 输出包含命令摘要和 Git 提示

### 质量验收

- [ ] 所有单元测试通过 (`uv run pytest tests/commands/`)
- [ ] 所有集成测试通过 (`uv run pytest tests/test_cli.py`)
- [ ] 代码检查通过 (`uv run ruff check src/`)
- [ ] 文档更新完成

---

## 备注

- [P] 任务 = 不同文件，无依赖，可并行
- [Story] 标签将任务映射到具体用户故事
- 遵循 TDD 原则：测试任务先于实现任务
- 每个任务或逻辑组完成后提交
- 可在任何 checkpoint 停止验证

---

*任务版本: 1.0*
*创建日期: 2026-03-04*
*基于 plan.md v1.0 生成*

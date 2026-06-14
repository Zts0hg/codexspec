# Implementation Plan: Constitution Auto-Import

## 1. Tech Stack

| Category | Technology | Version | Notes |
|----------|------------|---------|-------|
| Language | Python | 3.11+ | 现有项目约束 |
| CLI Framework | Typer | Latest | 现有框架 |
| Formatting | Rich | Latest | 现有控制台输出库 |
| Testing | pytest | Latest | 现有测试框架 |
| Package Manager | uv | Latest | 现有包管理器 |

## 2. Constitutionality Review

| Principle | Compliance | Notes |
|-----------|------------|-------|
| **Code Quality** | ✅ | 函数保持单一职责，使用常量定义路径 |
| **Testing Standards** | ✅ | 更新现有测试用例，覆盖新的 `@` 导入检测 |
| **Documentation** | ✅ | 更新 CLAUDE.md 模板，添加 SUPREME AUTHORITY 标识 |
| **Architecture** | ✅ | 修改范围最小化，仅涉及 4 个函数 |
| **Performance** | ✅ | O(n) 字符串检测，NFR-001 要求 <10ms |
| **Security** | ✅ | 纯文本操作，无安全风险 |

**Decision Guidelines 对齐**:

- **Maintainability** over optimization: 使用常量定义导入路径
- **Clarity** over cleverness: 简单的字符串检测逻辑
- **Stability** over features: 保持向后兼容

## 3. Architecture Overview

### Related Specs

| Spec ID | Relationship |
|---------|--------------|
| 2026-0228-1112vx-constitution-compliance-enhancement | **Supersedes** - Spec 003 使用 `@` 导入语法替代 Spec 002 的手动 compliance section 方案 |

### 当前架构（Spec 002 实现）

```
┌─────────────────────────────────────────────────────┐
│                    CLAUDE.md                         │
├─────────────────────────────────────────────────────┤
│ ## [HIGHEST PRIORITY] CONSTITUTION COMPLIANCE       │
│ ... (手动说明文字 ~40 行) ...                        │
├─────────────────────────────────────────────────────┤
│ # Project Content                                   │
│ ...                                                 │
└─────────────────────────────────────────────────────┘
```

### 目标架构（Spec 003 实现）

```
┌─────────────────────────────────────────────────────┐
│                    CLAUDE.md                         │
├─────────────────────────────────────────────────────┤
│ @.codexspec/memory/constitution.md  ← 1 行导入      │
├─────────────────────────────────────────────────────┤
│ # Project Content                                   │
│ ...                                                 │
└─────────────────────────────────────────────────────┘
          │
          │ Claude Code 自动加载
          ▼
┌─────────────────────────────────────────────────────┐
│         .codexspec/memory/constitution.md           │
├─────────────────────────────────────────────────────┤
│ > ⚠️ **SUPREME AUTHORITY**: ...  ← 新增标识        │
│ # Project Constitution                              │
│ ...                                                 │
└─────────────────────────────────────────────────────┘
```

### 数据流

```
codexspec init
      │
      ▼
┌──────────────────────┐
│ constitution.md 存在? │
└──────────┬───────────┘
           │
     ┌─────┴─────┐
     │ No        │ Yes
     ▼           ▼
┌──────────┐  ┌──────────────────┐
│ 创建新文件│  │ CLAUDE.md 存在?  │
│ (含标识) │  └────────┬─────────┘
└──────────┘           │
                 ┌─────┴─────┐
                 │ No        │ Yes
                 ▼           ▼
           ┌──────────┐  ┌────────────────────┐
           │ 创建新文件│  │ has_compliance()?  │
           │ (含导入) │  └─────────┬──────────┘
           └──────────┘            │
                             ┌─────┴─────┐
                             │ False     │ True
                             ▼           ▼
                      ┌──────────────┐  ┌─────────┐
                      │ 确认添加导入?│  │ 跳过    │
                      └──────┬───────┘  └─────────┘
                             │
                       ┌─────┴─────┐
                       │ No        │ Yes
                       ▼           ▼
                 ┌──────────┐  ┌──────────────────┐
                 │ 保持不变  │  │ prepend_import() │
                 └──────────┘  └──────────────────┘
```

## 4. Component Structure

```
codexspec/
├── src/codexspec/
│   └── __init__.py              # 主要修改: 4 个函数
├── CLAUDE.md                    # 项目自身: 添加 @ 导入
├── .codexspec/memory/
│   └── constitution.md          # 项目自身: 添加 SUPREME AUTHORITY
└── tests/
    └── test_init_compliance.py  # 更新测试用例
```

## 5. Module Dependency Graph

```
┌─────────────────────────────────────────────────────────┐
│                      init command                        │
└───────────────────────────┬─────────────────────────────┘
                            │ calls
                            ▼
┌───────────────────────────────────────────────────────────┐
│                                                            │
│  ┌─────────────────────────┐  ┌─────────────────────────┐ │
│  │ _get_claude_md_content()│  │ _get_default_constitution()│
│  │     [REQ-002]           │  │      [REQ-001]           │ │
│  └─────────────────────────┘  └─────────────────────────┘ │
│                                                            │
│  ┌─────────────────────────┐  ┌─────────────────────────┐ │
│  │ has_compliance_section()│  │prepend_compliance_section()│
│  │     [REQ-003]           │  │      [REQ-004]          │ │
│  └─────────────────────────┘  └─────────────────────────┘ │
│                                                            │
│  ┌─────────────────────────┐                              │
│  │ confirm_add_compliance()│  (保持不变)                  │
│  └─────────────────────────┘                              │
│                                                            │
│  ┌─────────────────────────┐                              │
│  │_get_compliance_section  │  [DEPRECATED] 可删除        │
│  │       _content()        │                              │
│  └─────────────────────────┘                              │
│                                                            │
└────────────────────────────────────────────────────────────┘
                            │
                            ▼
              ┌─────────────────────────┐
              │  CLAUDE.md (文件系统)    │
              └─────────────────────────┘
```

## 6. Module Specifications

### Module: `src/codexspec/__init__.py` - 常量定义

- **Responsibility**: 定义导入路径常量，确保可维护性 (NFR-003)
- **Dependencies**: 无
- **Interface**: 内部使用
- **Files**: `src/codexspec/__init__.py`

```python
# 新增常量（在文件顶部，__version__ 之后）
CONSTITUTION_IMPORT_PATH = "@.codexspec/memory/constitution.md"
CONSTITUTION_FILE_PATH = ".codexspec/memory/constitution.md"
```

### Module: `_get_default_constitution()` [REQ-001]

- **Responsibility**: 生成包含 SUPREME AUTHORITY 标识的 constitution 内容
- **Dependencies**: 无
- **Interface**: `() -> str`
- **Files**: `src/codexspec/__init__.py:1088`

**修改**:

```python
def _get_default_constitution() -> str:
    """Return the default constitution content."""
    return """> ⚠️ **SUPREME AUTHORITY**: This constitution defines the governing principles for this project. All code changes and decisions must comply with these principles.

# Project Constitution
...
"""
```

### Module: `_get_claude_md_content()` [REQ-002]

- **Responsibility**: 生成使用 `@` 导入语法的 CLAUDE.md 内容
- **Dependencies**: `CONSTITUTION_IMPORT_PATH`
- **Interface**: `(project_name: str) -> str`
- **Files**: `src/codexspec/__init__.py:1255`

**修改**:

- 删除 `## [HIGHEST PRIORITY] CONSTITUTION COMPLIANCE` section (~40 行)
- 在顶部添加 `@.codexspec/memory/constitution.md`

```python
def _get_claude_md_content(project_name: str) -> str:
    """Return the CLAUDE.md content for a project."""
    return f"""{CONSTITUTION_IMPORT_PATH}

# CLAUDE.md - {project_name} Guidelines

This document provides comprehensive context and guidelines for Claude Code...
"""
```

### Module: `has_compliance_section()` [REQ-003]

- **Responsibility**: 检测 CLAUDE.md 是否包含 `@` 导入语句
- **Dependencies**: `CONSTITUTION_FILE_PATH`
- **Interface**: `(claude_md_path: Path) -> bool`
- **Files**: `src/codexspec/__init__.py:1204`

**修改**:

```python
def has_compliance_section(claude_md_path: Path) -> bool:
    """Check if CLAUDE.md contains the @ import statement.

    This function checks for the presence of the constitution file path
    (without @ prefix) to detect various forms of import statements.

    Args:
        claude_md_path: Path to the CLAUDE.md file

    Returns:
        True if the file contains the import statement, False otherwise
    """
    if not claude_md_path.exists():
        return False
    content = claude_md_path.read_text(encoding="utf-8")
    return CONSTITUTION_FILE_PATH in content
```

### Module: `prepend_compliance_section()` [REQ-004]

- **Responsibility**: 在 CLAUDE.md 顶部添加 `@` 导入语句
- **Dependencies**: `CONSTITUTION_IMPORT_PATH`
- **Interface**: `(claude_md_path: Path) -> None`
- **Files**: `src/codexspec/__init__.py:1222`

**修改**:

```python
def prepend_compliance_section(claude_md_path: Path) -> None:
    """Prepend the @ import statement to CLAUDE.md.

    This function adds the import statement at the beginning of the file,
    preserving all existing content.

    Args:
        claude_md_path: Path to the CLAUDE.md file
    """
    existing_content = claude_md_path.read_text(encoding="utf-8")
    import_statement = f"{CONSTITUTION_IMPORT_PATH}\n\n"
    claude_md_path.write_text(import_statement + existing_content, encoding="utf-8")
```

### Module: `_get_compliance_section_content()` [DEPRECATED]

- **Responsibility**: ~~返回手动 compliance section 内容~~
- **Status**: **DEPRECATED** - 被 `@` 导入语法替代
- **Action**: 删除此函数（私有函数，无向后兼容承诺）

### Module: `tests/test_init_compliance.py` - 测试更新

- **Responsibility**: 更新测试用例以匹配新的检测逻辑
- **Dependencies**: `codexspec` 模块
- **Interface**: pytest 测试类
- **Files**: `tests/test_init_compliance.py`

**修改摘要**:

1. 更新 `project_with_compliance_claude_md` fixture 使用 `@` 导入语法
2. 更新 `required_keywords` 检测 `@.codexspec/memory/constitution.md`
3. 更新边缘情况测试

## 7. Data Models

> [!NOTE]
> 本项目为 CLI 工具，无持久化数据模型。主要数据结构为文件内容字符串。

### 常量定义

```python
# 导入语句常量
CONSTITUTION_IMPORT_PATH = "@.codexspec/memory/constitution.md"
CONSTITUTION_FILE_PATH = ".codexspec/memory/constitution.md"
```

## 8. API Contracts

### Command: `codexspec init`

- **Arguments**: `[project_name]`
- **Options**: `--here`, `--force`, `--lang`, `--no-git`
- **Behavior Change**:
  - 检测逻辑从检测 `## MANDATORY: Constitution Compliance` 改为检测 `.codexspec/memory/constitution.md`
  - 添加逻辑从添加手动说明 section 改为在文件顶部添加导入语句
- **Exit Codes**: 无变化

### Function: `has_compliance_section(claude_md_path: Path) -> bool`

- **Input**: `claude_md_path: Path` - CLAUDE.md 文件路径
- **Output**: `bool` - 是否包含导入语句
- **Test Cases**: TC-002, TC-003, TC-004

### Function: `prepend_compliance_section(claude_md_path: Path) -> None`

- **Input**: `claude_md_path: Path` - CLAUDE.md 文件路径
- **Output**: `None` (副作用：修改文件)
- **Test Cases**: TC-005

## 9. Implementation Phases

### Phase 1: Foundation (常量与模板)

- [ ] **TASK-001**: 在 `src/codexspec/__init__.py` 中添加常量定义
  - 位置：`__version__` 和 `__author__` 之后
  - 内容：`CONSTITUTION_IMPORT_PATH` 和 `CONSTITUTION_FILE_PATH`

- [ ] **TASK-002**: 更新 `_get_default_constitution()` 函数 [REQ-001]
  - 在返回内容顶部添加 SUPREME AUTHORITY blockquote

### Phase 2: Core Implementation (核心函数)

- [ ] **TASK-003**: 更新 `_get_claude_md_content()` 函数 [REQ-002]
  - 删除 `## [HIGHEST PRIORITY] CONSTITUTION COMPLIANCE` section
  - 在顶部添加 `@.codexspec/memory/constitution.md`

- [ ] **TASK-004**: 更新 `has_compliance_section()` 函数 [REQ-003]
  - 使用 `CONSTITUTION_FILE_PATH` 常量
  - 更新 docstring

- [ ] **TASK-005**: 更新 `prepend_compliance_section()` 函数 [REQ-004]
  - 使用 `CONSTITUTION_IMPORT_PATH` 常量
  - 简化为添加单行导入语句
  - 更新 docstring

- [ ] **TASK-006**: 删除 `_get_compliance_section_content()` 函数
  - 私有函数，不再需要

### Phase 3: Project Self-Update [REQ-005]

- [ ] **TASK-007**: 更新 CodexSpec 项目自身的 `CLAUDE.md`
  - 在文件顶部添加 `@.codexspec/memory/constitution.md`
  - 删除 `## MANDATORY: Constitution Compliance` section（手动清理）

- [ ] **TASK-008**: 更新 CodexSpec 项目的 `constitution.md`
  - 在顶部添加 SUPREME AUTHORITY blockquote

### Phase 4: Testing

- [ ] **TASK-009**: 更新 `tests/test_init_compliance.py`
  - 修改 `project_with_compliance_claude_md` fixture 使用 `@` 导入语法
  - 更新 `required_keywords` 列表
  - 更新测试断言

- [ ] **TASK-010**: 运行测试验证

  ```bash
  uv run pytest tests/test_init_compliance.py -v
  ```

- [ ] **TASK-011**: 运行完整测试套件

  ```bash
  uv run pytest
  ```

### Phase 5: Manual Verification

- [ ] **TASK-012**: 验证 `/memory` 命令输出
  - 在 CodexSpec 项目中运行 `/memory`
  - 确认 `.codexspec/memory/constitution.md` 显示为 `@-imported`

## 10. Technical Decisions

### Decision 1: 导入路径硬编码

- **Choice**: 使用常量 `CONSTITUTION_IMPORT_PATH = "@.codexspec/memory/constitution.md"`
- **Rationale**:
  - 简化实现，避免配置复杂度
  - 路径是 CodexSpec 约定，不需要用户自定义
  - 符合 NFR-003 可维护性要求
- **Alternatives**:
  - 从配置文件读取路径（过度设计）
  - 支持自定义路径（Out of Scope）
- **Trade-offs**: 牺牲灵活性换取简洁性

### Decision 2: 删除 `_get_compliance_section_content()` 函数

- **Choice**: 直接删除该函数
- **Rationale**:
  - 这是私有函数（`_` 前缀），外部代码不应依赖
  - 新的 `prepend_compliance_section()` 实现不再需要它
  - 保留无用代码是真正的技术债务
  - 回滚时可从 git 历史恢复
- **Alternatives**:
  - 保留并标记 deprecated - 不必要
- **Trade-offs**: 无明显缺点，代码更清晰

### Decision 3: 检测逻辑

- **Choice**: 检测 `.codexspec/memory/constitution.md`（无 `@` 前缀）
- **Rationale**:
  - 更宽松的检测，覆盖 `@.codexspec/memory/constitution.md` 和其他引用形式
  - 与 Spec 002 的检测策略一致
  - 避免 false negative
- **Alternatives**:
  - 精确检测 `@.codexspec/memory/constitution.md`（更严格）
- **Trade-offs**: 可能产生 false positive（可接受，避免重复添加）

### Decision 4: 不自动清理旧版

- **Choice**: 保留旧版手动 compliance section，由用户手动删除
- **Rationale**:
  - 用户可能自定义了 compliance section 内容
  - 避免破坏性更改
  - Migration Guide 提供手动清理说明
- **Alternatives**:
  - 自动检测并删除旧版 section（风险高）
- **Trade-offs**: 升级后可能有冗余内容

## 11. Risk Assessment

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| 旧版 CLAUDE.md 同时包含两种形式 | Medium | Low | Migration Guide 提供清理说明 |
| 检测 false positive | Low | Low | 可接受，避免重复添加 |
| 测试用例遗漏 | Low | Medium | 完整的测试用例覆盖 |
| 用户不知道需要更新 | Medium | Low | 自动迁移 + 手动迁移指南 |

## 12. Rollback Plan

如果发现问题，可以通过以下步骤回滚：

```bash
git revert <commit-hash>
```

具体恢复内容：

1. 恢复 `has_compliance_section()` 的旧检测逻辑
2. 恢复 `prepend_compliance_section()` 的旧行为
3. 恢复 `_get_compliance_section_content()` 函数
4. 恢复 `_get_claude_md_content()` 和 `_get_default_constitution()` 的旧内容
5. 恢复 `CLAUDE.md` 和 `constitution.md` 文件

## 13. Success Criteria

- [ ] `codexspec init` 生成的 CLAUDE.md 顶部包含 `@.codexspec/memory/constitution.md`
- [ ] `has_compliance_section()` 正确检测 `@` 导入语句
- [ ] `prepend_compliance_section()` 正确添加导入语句
- [ ] `/memory` 命令显示 constitution.md 为 `@-imported`
- [ ] 所有测试通过（`tests/test_init_compliance.py`）
- [ ] 无性能回归（init 命令执行时间增加 < 10ms）
- [ ] `_get_compliance_section_content()` 函数已删除

## Available Follow-up Commands

- `/codexspec.review-plan` - 验证计划质量
- `/codexspec.plan-to-tasks` - 分解为可执行任务

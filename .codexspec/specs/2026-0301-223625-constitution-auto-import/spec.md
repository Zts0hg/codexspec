# Feature: Constitution Auto-Import

## Overview

实现 Claude Code 官方支持的 `@` 导入语法，使 `constitution.md` 文件能够被自动注入到 Claude Code 的上下文中。当前 `CLAUDE.md` 使用手动说明文字，导致 `/memory` 命令无法识别 constitution 文件为 `@-imported` 状态。

### Related Specs

| Spec ID | Relationship | Description |
|---------|--------------|-------------|
| 2026-0228-1112vx-constitution-compliance-enhancement | **Supersedes** | Spec 003 使用 `@` 导入语法替代 Spec 002 的手动 compliance section 方案。实现时需移除 Spec 002 的手动说明逻辑，更新检测函数使用新的导入语句检测。 |

## Goals

- 使用 Claude Code 官方 `@path/to/import` 语法自动导入 constitution.md
- 确保用户运行 `/memory` 命令时能看到 constitution.md 显示为 `@-imported`
- 简化 CLAUDE.md 内容，移除冗余的手动说明
- 保持向后兼容性，确保现有检测逻辑正确更新

## User Stories

### Story 1: 开发者初始化新项目

**As a** 使用 CodexSpec 的开发者
**I want** 运行 `codexspec init` 后 constitution.md 自动被 CLAUDE.md 导入
**So that** Claude Code 能够自动加载项目宪法，无需手动配置

**Acceptance Criteria:**

- [ ] `codexspec init` 执行后，CLAUDE.md 顶部包含 `@.codexspec/memory/constitution.md`
- [ ] 运行 `/memory` 命令时，constitution.md 显示为 `@-imported`
- [ ] constitution.md 在 CLAUDE.md 之前被加载到上下文中

### Story 2: 开发者验证宪法加载状态

**As a** 使用 CodexSpec 的开发者
**I want** 通过 `/memory` 命令验证 constitution.md 是否正确加载
**So that** 确保项目宪法已注入到 Claude Code 上下文中

**Acceptance Criteria:**

- [ ] `/memory` 输出中显示 `.codexspec/memory/constitution.md` 条目
- [ ] 该条目标记为 `@-imported` 或 `L` (loaded)
- [ ] 条目显示正确的相对路径

### Story 3: 现有项目升级

**As a** 已有 CodexSpec 项目的维护者
**I want** 运行 `codexspec init` 时自动更新 CLAUDE.md 使用新语法
**So that** 现有项目也能享受自动导入功能

**Acceptance Criteria:**

- [ ] 现有 CLAUDE.md 顶部添加 `@.codexspec/memory/constitution.md` 导入语句
- [ ] 其他 CLAUDE.md 内容保持不变（旧版手动说明保留，用户可手动删除）
- [ ] 提示用户确认修改

## Functional Requirements

### REQ-001: Constitution 模板更新

在 `templates/constitution.md` 模板顶部添加最高准则说明：

```markdown
> ⚠️ **SUPREME AUTHORITY**: This constitution defines the governing principles for this project. All code changes and decisions must comply with these principles.
```

### REQ-002: CLAUDE.md 模板更新

修改 `_get_claude_md_content()` 函数生成的 CLAUDE.md 模板：

**删除旧内容**：

```markdown
## MANDATORY: Constitution Compliance

**CRITICAL**: Before ANY code change in this CodexSpec project:

1. Check for `.codexspec/memory/constitution.md`
2. If exists, LOAD IT FIRST and ensure compliance
3. All outputs must align with constitutional principles

The constitution is the SUPREME AUTHORITY for this project.
```

**在文件顶部添加**：

```markdown
@.codexspec/memory/constitution.md
```

### REQ-003: 检测函数更新

修改 `src/codexspec/__init__.py` 中的 `has_compliance_section()` 函数：

**旧逻辑**：检测手动说明文字

```python
def has_compliance_section(claude_md_path: Path) -> bool:
    content = claude_md_path.read_text()
    return "## MANDATORY: Constitution Compliance" in content
```

**新逻辑**：检测 `@` 导入语句

```python
def has_compliance_section(claude_md_path: Path) -> bool:
    content = claude_md_path.read_text()
    return "@.codexspec/memory/constitution.md" in content
```

### REQ-004: Prepend 函数更新

修改 `prepend_compliance_section()` 函数：

**旧逻辑**：添加手动说明 section
**新逻辑**：在文件顶部添加导入语句

```python
def prepend_compliance_section(claude_md_path: Path) -> None:
    content = claude_md_path.read_text()
    import_statement = "@.codexspec/memory/constitution.md\n\n"
    claude_md_path.write_text(import_statement + content)
```

### REQ-005: CodexSpec 项目自身 CLAUDE.md 更新

更新 `{PROJECT_ROOT}/CLAUDE.md`（项目根目录下的 CLAUDE.md 文件）：

1. 删除手动说明部分（即 `## MANDATORY: Constitution Compliance` 及其内容）
2. 在文件顶部添加 `@.codexspec/memory/constitution.md`

## Non-Functional Requirements

### NFR-001: 性能要求

- 导入语句检测应为 O(n) 时间复杂度，其中 n 为 CLAUDE.md 文件大小
- 不得影响 `codexspec init` 命令的整体执行时间（增加不超过 10ms）

### NFR-002: 兼容性要求

- 支持 Claude Code 所有版本（`@` 导入语法为官方支持功能）
- 支持所有操作系统（macOS, Linux, Windows）
- 路径使用正斜杠 `/` 以确保跨平台兼容性

### NFR-003: 可维护性要求

- 导入路径应为常量，便于统一修改
- 相关函数应添加单元测试

## Acceptance Criteria (Test Cases)

### TC-001: 新项目初始化验证

**前置条件**：空目录
**操作**：运行 `codexspec init`
**预期结果**：

- CLAUDE.md 顶部第一行为 `@.codexspec/memory/constitution.md`
- constitution.md 包含 SUPREME AUTHORITY 说明
- `/memory` 命令显示 constitution.md 为 `@-imported`

### TC-002: 检测函数测试 - 存在导入语句

**输入**：包含 `@.codexspec/memory/constitution.md` 的 CLAUDE.md
**预期输出**：`has_compliance_section()` 返回 `True`

### TC-003: 检测函数测试 - 不存在导入语句

**输入**：不包含导入语句的 CLAUDE.md
**预期输出**：`has_compliance_section()` 返回 `False`

### TC-004: 检测函数测试 - 旧版手动说明

**输入**：包含旧版 `## MANDATORY: Constitution Compliance` 但无导入语句的 CLAUDE.md
**预期输出**：`has_compliance_section()` 返回 `False`（需要升级）

### TC-005: Prepend 函数测试

**输入**：不包含导入语句的 CLAUDE.md
**操作**：调用 `prepend_compliance_section()`
**预期输出**：

- 文件顶部为 `@.codexspec/memory/constitution.md`
- 原有内容保持不变
- 导入语句与原内容之间有空行分隔

### TC-006: 现有项目升级

**前置条件**：使用旧版 CodexSpec 初始化的项目（CLAUDE.md 包含手动 compliance 说明）
**操作**：再次运行 `codexspec init`
**验证步骤**：

1. 检查控制台是否输出提示用户更新 CLAUDE.md 的消息
2. 确认用户选择 "是" 后，检查 CLAUDE.md 文件
3. 验证 CLAUDE.md 顶部第一行为 `@.codexspec/memory/constitution.md`
4. 验证 CLAUDE.md 中其他内容（如 Project Overview、Architecture 等）保持不变
**预期结果**：

- 控制台显示更新提示
- 用户确认后，导入语句成功添加
- 其他内容完整保留（旧版手动说明仍存在，用户可手动删除）

## Edge Cases

### Edge Case 1: CLAUDE.md 文件为空

**处理方式**：直接写入 `@.codexspec/memory/constitution.md`

### Edge Case 2: CLAUDE.md 已包含导入语句

**处理方式**：跳过添加，不重复写入

### Edge Case 3: constitution.md 文件不存在

**处理方式**：

- `has_compliance_section()` 仍检测导入语句（即使文件不存在）
- `codexspec init` 应先生成 constitution.md，再生成 CLAUDE.md

### Edge Case 4: 用户手动修改了导入路径

**处理方式**：检测函数应同时检查标准路径 `.codexspec/memory/constitution.md`

## Output Examples

### 示例 1: 更新后的 CLAUDE.md 顶部

```markdown
@.codexspec/memory/constitution.md

# CLAUDE.md - Project Development Guide

This document provides comprehensive context and guidelines for Claude Code...

```

### 示例 2: 更新后的 constitution.md 顶部

```markdown
> ⚠️ **SUPREME AUTHORITY**: This constitution defines the governing principles for this project. All code changes and decisions must comply with these principles.

# Project Constitution

This document defines the governing principles and development guidelines for this project.

## Core Principles
...
```

### 示例 3: /memory 命令预期输出

```
❯ /memory

Learn more: https://code.claude.com/docs/en/memory

╭─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│                                                                                                                                                                                                                                   │
│ Select memory to edit:                                                                                                                                                                                                            │
│                                                                                                                                                                                                                                   │
│  ❯ 1. Project memory                       Checked in at ./CLAUDE.md                                                                                                                                                              │
│    2. L .codexspec/memory/constitution.md  @-imported                                                                                                                                                                             │
│    3. User memory                          Saved in ~/.claude/CLAUDE.md                                                                                                                                                           │
│                                                                                                                                                                                                                                   │
╰─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## Migration Guide

本章节为现有 CodexSpec 用户提供从旧版（手动说明）到新版（`@` 导入语法）的迁移指南。

### 自动迁移

运行 `codexspec init` 命令，系统会自动检测 CLAUDE.md 中是否包含导入语句：

1. 如果检测到缺少导入语句，会提示用户是否添加
2. 用户确认后，自动在 CLAUDE.md 顶部添加 `@.codexspec/memory/constitution.md`
3. 旧版的手动说明 section 可选择保留或删除

### 手动迁移

如果用户希望手动迁移，请执行以下步骤：

1. **打开 CLAUDE.md 文件**

2. **在文件最顶部添加导入语句**：

   ```markdown
   @.codexspec/memory/constitution.md

   # CLAUDE.md - Project Development Guide
   ...
   ```

3. **删除旧版手动说明**（如果存在）：

   ```markdown
   ## MANDATORY: Constitution Compliance

   **CRITICAL**: Before ANY code change in this CodexSpec project:
   ...
   ```

4. **验证迁移成功**：
   - 在 Claude Code 中运行 `/memory` 命令
   - 确认 `.codexspec/memory/constitution.md` 显示为 `@-imported`

### 迁移验证清单

- [ ] CLAUDE.md 顶部包含 `@.codexspec/memory/constitution.md`
- [ ] 旧版手动说明已删除（可选，建议删除以避免冗余）
- [ ] `/memory` 命令显示 constitution.md 为 `@-imported`
- [ ] Claude Code 会话中 constitution 内容已自动加载

## Out of Scope

- 多文件导入支持（如导入多个 constitution 相关文件）
- 导入语法的自定义配置（路径硬编码为 `.codexspec/memory/constitution.md`）
- 其他 AI 工具的导入语法支持（仅针对 Claude Code）
- constitution.md 内容的版本控制或历史记录
- 导入文件的循环依赖检测（Claude Code 已内置最大 5 层深度限制）
- **旧版 compliance section 自动清理**：升级时仅添加 `@` 导入语句，旧版手动说明保留由用户自行删除

## Clarifications

### Session 2026-03-01 00:30

**Q1**: 是否需要自动清理旧版 compliance section？
**A1**: 不需要考虑旧版清理
**Impact**: Out of Scope 新增条目，Migration Guide 策略确认

**Q2**: 如何处理 REQ-002 和 REQ-003 的功能重叠？
**A2**: 选项 A - 合并为单一需求
**Impact**: REQ-002 和 REQ-003 合并，REQ 编号重新排序（原 REQ-004→003, REQ-005→004, REQ-006→005）

**Q3**: 是否需要添加 Related Specs 章节说明与 Spec 002 的关系？
**A3**: 选项 A - 添加 Related Specs 章节
**Impact**: Overview 新增 Related Specs 表格，说明 Spec 003 替代 Spec 002

**Q4**: 是否需要添加文件操作错误处理需求？
**A4**: 选项 B - 不需要添加，让异常自然传播
**Impact**: 保持简洁，无需新增 NFR

---

## Implementation Notes

### 文件修改清单

| 文件 | 修改类型 | 说明 |
|------|----------|------|
| `src/codexspec/__init__.py` | 修改 | 更新 `has_compliance_section()`、`prepend_compliance_section()`、`_get_claude_md_content()`、`_get_default_constitution()` 函数 |
| `CLAUDE.md` (项目自身) | 修改 | 添加 `@` 导入语句，可选删除旧版手动说明 |
| `tests/test_init_compliance.py` | 修改 | 更新测试用例以匹配新的检测逻辑 |

### 参考文档

- [Claude Code Memory Documentation](https://docs.anthropic.com/en/docs/claude-code/memory) - 官方 `@` 导入语法说明

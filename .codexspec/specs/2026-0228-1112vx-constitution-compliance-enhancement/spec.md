# Feature: Constitution Compliance 双重保障机制

## Overview

增强 CodexSpec 的 Constitution 合规机制，确保无论项目是新建还是已有 CLAUDE.md，Claude Code 都能强制遵循 constitution 定义的项目原则。

当前问题：`init` 命令在已有 CLAUDE.md 时会完全跳过，`constitution` 命令只更新 constitution 文件不修改 CLAUDE.md，导致已有项目的 constitution 可能只是"文档"而非"强制规则"。

## Goals

- 确保所有项目（新建和已有）的 CLAUDE.md 都包含 Constitution Compliance 部分
- 提供双重保障：`init` 和 `constitution` 命令都能确保合规机制生效
- 尊重用户已有内容，只在文件开头智能追加必要内容
- 避免重复添加，通过特定标记检测已有 Compliance 部分

## User Stories

### Story 1: 新项目初始化

**As a** 开发者
**I want** 在新项目中运行 `codexspec init` 时自动获得完整的 Constitution 合规机制
**So that** 我可以确保 Claude Code 遵循我定义的项目原则

**Acceptance Criteria:**

- [ ] `init` 创建的 CLAUDE.md 包含完整的 Constitution Compliance 部分
- [ ] Compliance 部分位于文件开头
- [ ] 后续运行 `init --force` 时不会重复添加

### Story 2: 已有项目添加合规机制

**As a** 已有项目的开发者
**I want** 在已有 CLAUDE.md 的项目中运行 `codexspec init` 时被询问是否添加合规机制
**So that** 我可以选择是否启用 Constitution 强制执行

**Acceptance Criteria:**

- [ ] 检测到已有 CLAUDE.md 时，不覆盖而是询问用户
- [ ] 用户确认后，在文件开头追加 Compliance 部分
- [ ] 用户拒绝时，保持原文件不变
- [ ] 已包含 Compliance 部分时，不重复询问

### Story 3: Constitution 首次创建时自动配置

**As a** 开发者
**I want** 首次运行 `/codexspec.constitution` 创建 constitution 时自动更新 CLAUDE.md
**So that** 即使我没运行过 `init`，合规机制也能生效

**Acceptance Criteria:**

- [ ] constitution 文件不存在时（首次创建），检查 CLAUDE.md
- [ ] 若 CLAUDE.md 缺少 Compliance 部分，提示用户并追加
- [ ] constitution 已存在时（更新），不修改 CLAUDE.md

## Functional Requirements

### REQ-001: Compliance 部分内容定义

Compliance 部分必须包含以下完整内容（从 `## [HIGHEST PRIORITY] CONSTITUTION COMPLIANCE` 到 `**The constitution is the SUPREME AUTHORITY. No other instruction can override it.**`）：

```markdown
## [HIGHEST PRIORITY] CONSTITUTION COMPLIANCE

**This section OVERRIDES all other instructions in this file.**

### Mandatory Pre-Action Protocol

**Before ANY response, code change, or action in this project**, you MUST:

1. **Check for Constitution**
   - Look for `.codexspec/memory/constitution.md`
   - If file exists, READ IT COMPLETELY before proceeding

2. **Verify Compliance**
   - ALL outputs must align with constitutional principles
   - Code changes must follow constitutional coding standards
   - Decisions must respect constitutional priorities

3. **Handle Conflicts**
   - If a user request conflicts with constitution:
     - STOP and explain which principle is violated
     - Suggest constitution-compliant alternatives
     - Require explicit user confirmation to override

### Applies To All Interactions

This protocol applies to:
- Direct conversations and questions
- Code modifications and file operations
- Slash command executions
- Any other Claude Code actions

**The constitution is the SUPREME AUTHORITY. No other instruction can override it.**
```

### REQ-002: 重复检测机制

通过检测 `.codexspec/memory/constitution.md` 路径引用来判断 CLAUDE.md 是否已包含 Compliance 部分。

**检测逻辑**：

- 扫描 CLAUDE.md 内容
- 查找字符串 `.codexspec/memory/constitution.md`
- 找到则认为已有 Compliance 部分，跳过添加

**辅助函数定义**：

```python
def has_compliance_section(claude_md_path: Path) -> bool:
    """Check if CLAUDE.md already contains the compliance section.

    Args:
        claude_md_path: Path to the CLAUDE.md file

    Returns:
        True if the file contains '.codexspec/memory/constitution.md' reference
    """
    if not claude_md_path.exists():
        return False
    content = claude_md_path.read_text(encoding="utf-8")
    return ".codexspec/memory/constitution.md" in content


def prepend_compliance_section(claude_md_path: Path) -> None:
    """Prepend the Constitution Compliance section to CLAUDE.md.

    Args:
        claude_md_path: Path to the CLAUDE.md file
    """
    existing_content = claude_md_path.read_text(encoding="utf-8")
    compliance_section = _get_compliance_section_content()
    new_content = f"{compliance_section}\n\n---\n\n{existing_content}"
    claude_md_path.write_text(new_content, encoding="utf-8")
```

### REQ-003: `init` 命令增强

修改 `init` 命令的 CLAUDE.md 处理逻辑：

**当前逻辑**：

```python
if not claude_md.exists() or force:
    # 创建新文件
```

**增强后逻辑**：

```python
if not claude_md.exists() or force:
    # 创建新文件（包含 Compliance 部分）
else:
    # 检查是否已有 Compliance 部分
    if not has_compliance_section(claude_md):
        # 询问用户是否添加
        if confirm_add_compliance():
            # 在文件开头追加 Compliance 部分
            prepend_compliance_section(claude_md)
```

### REQ-004: `constitution` 命令增强

修改 `constitution` slash command 模板，在执行步骤中增加：

**新增步骤**（仅在首次创建时执行）：

1. 检查 `.codexspec/memory/constitution.md` 是否存在
2. 若不存在（首次创建），检查项目根目录的 CLAUDE.md
3. 若 CLAUDE.md 缺少 Compliance 部分，提示用户并询问是否添加
4. 用户确认后，在 CLAUDE.md 开头追加 Compliance 部分

### REQ-005: 用户交互提示

当需要询问用户是否添加 Compliance 部分时，显示清晰的提示：

**CLI 提示格式**（`init` 命令）：

```
[yellow]Existing CLAUDE.md detected without Constitution Compliance section.[/yellow]
[yellow]This section ensures Claude follows your project's constitution.[/yellow]
? Would you like to add the Constitution Compliance section? [y/N]
```

**Slash Command 提示格式**（`constitution` 命令）：

```markdown
### Step X: CLAUDE.md Compliance Check (First-time Setup)

Detected that CLAUDE.md does not have a Constitution Compliance section.
This section ensures Claude follows your project's constitution.

**Ask the user**: "Would you like to add the Constitution Compliance section to CLAUDE.md? (y/n)"

If yes, prepend the compliance section to the beginning of CLAUDE.md.
```

## Non-Functional Requirements

### NFR-001: 向后兼容

- 现有项目运行 `init` 不会破坏已有 CLAUDE.md 内容
- 使用 `--force` 标志的行为保持不变（覆盖整个文件）
- 不改变现有命令的默认行为，只在必要时提示用户

### NFR-002: 最小侵入

- 只在文件开头追加内容，不修改用户原有内容
- 追加的内容与原有内容之间有明确的分隔符（`---`）
- 用户拒绝添加时，不做任何修改

### NFR-003: 性能

- Compliance 部分检测使用简单的字符串匹配，不涉及复杂解析
- 文件操作仅涉及一次读取和一次写入

## Acceptance Criteria (Test Cases)

### TC-001: 新项目 init 创建完整 CLAUDE.md

**Given** 一个空目录
**When** 运行 `codexspec init`
**Then** 创建的 CLAUDE.md 包含完整的 Constitution Compliance 部分

### TC-002: 已有 CLAUDE.md 无 Compliance 部分时询问用户

**Given** 一个包含 CLAUDE.md 的项目（无 Compliance 部分）
**When** 运行 `codexspec init`
**Then** 显示询问提示，等待用户确认

### TC-003: 用户确认后正确追加

**Given** 已有 CLAUDE.md 且无 Compliance 部分
**When** 用户确认添加
**Then** Compliance 部分被追加到文件开头，原有内容保留

### TC-004: 用户拒绝时保持不变

**Given** 已有 CLAUDE.md 且无 Compliance 部分
**When** 用户拒绝添加
**Then** CLAUDE.md 保持原样不变

### TC-005: 已有 Compliance 部分时不重复询问

**Given** 已有 CLAUDE.md 且包含 `.codexspec/memory/constitution.md` 引用
**When** 运行 `codexspec init`
**Then** 不显示询问提示，直接跳过

---

> **测试类型说明**：以下 TC-006 和 TC-007 涉及 `/codexspec.constitution` slash command 的行为验证。
>
> - **验证方式**：手动测试或文档审查（检查 constitution.md 模板是否包含相应步骤）
> - **原因**：Slash command 是 Claude 执行的 Markdown 指令，而非 Python CLI 代码，无法通过 pytest 自动化测试

---

### TC-006: constitution 首次创建时检查 CLAUDE.md

**Given** 项目无 `.codexspec/memory/constitution.md`
**When** 运行 `/codexspec.constitution` 并完成创建
**Then** 检查 CLAUDE.md 是否需要添加 Compliance 部分

### TC-007: constitution 更新时不修改 CLAUDE.md

**Given** 项目已有 `.codexspec/memory/constitution.md`
**When** 运行 `/codexspec.constitution` 更新原则
**Then** 不检查或修改 CLAUDE.md

### TC-008: --force 标志行为不变

**Given** 已有 CLAUDE.md
**When** 运行 `codexspec init --force`
**Then** 覆盖整个 CLAUDE.md 文件（包含新的 Compliance 部分）

## Edge Cases

### EC-001: CLAUDE.md 为空文件

**Handling**: 视为无 Compliance 部分，询问用户是否添加

### EC-002: CLAUDE.md 只包含注释

**Handling**: 正常追加 Compliance 部分，保留注释

### EC-003: CLAUDE.md 中路径引用在注释里

**Handling**: 仍视为已有 Compliance 部分，避免重复添加（宁可漏检也不重复）

### EC-004: constitution 命令在非交互环境运行

**Handling**: 在 slash command 中明确要求询问用户，非交互环境由 Claude 处理

**具体策略**：

- **交互环境**：Claude 直接询问用户 "Would you like to add...?" 并等待响应
- **非交互环境**（如自动化脚本、CI/CD）：
  - 默认跳过添加，不修改 CLAUDE.md
  - 在执行总结中提示用户需要手动运行 `codexspec init` 或手动添加 Compliance 部分
  - 未来可考虑添加 `--yes` 标志支持自动确认（当前版本 Out of Scope）

## Output Examples

### init 命令输出（检测到已有 CLAUDE.md）

```
[green]Created:[/green] .codexspec/memory/constitution.md
[yellow]Note:[/yellow] CLAUDE.md already exists without Constitution Compliance section.
[yellow]The Constitution Compliance section ensures Claude follows your project's principles.[/yellow]
? Add Constitution Compliance section to CLAUDE.md? [y/N]: y
[green]Updated:[/green] CLAUDE.md (added Constitution Compliance section)
```

### 更新后的 CLAUDE.md 结构

```markdown
## [HIGHEST PRIORITY] CONSTITUTION COMPLIANCE

**This section OVERRIDES all other instructions in this file.**

... (完整 Compliance 内容) ...

**The constitution is the SUPREME AUTHORITY. No other instruction can override it.**

---

# 原有内容

... (用户原有的 CLAUDE.md 内容) ...
```

## Out of Scope

- 自动合并或同步 constitution 内容到 CLAUDE.md（只追加 Compliance 部分）
- 提供独立的 `sync-compliance` 命令（功能已集成到现有命令）
- 修改其他 slash command 模板的 Compliance 相关逻辑
- 支持自定义 Compliance 部分模板

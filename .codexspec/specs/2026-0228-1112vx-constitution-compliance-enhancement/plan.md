# Implementation Plan: Constitution Compliance 双重保障机制

## 1. Tech Stack

| Category | Technology | Version | Notes |
|----------|------------|---------|-------|
| Language | Python | 3.11+ | 项目已有约束 |
| CLI Framework | Typer | current | 已有依赖 |
| Terminal Output | Rich | current | 已有依赖 |
| Testing | pytest | current | 已有依赖 |
| Linting | ruff | current | 已有依赖 |

## 2. Constitutionality Review

| Principle | Compliance | Notes |
|-----------|------------|-------|
| Code Quality | ✅ | 函数签名清晰，单一职责，使用已有命名规范 |
| Testing Standards | ✅ | 为新增函数编写单元测试，覆盖边界情况 |
| Documentation | ✅ | 所有新增函数包含 docstring，用户提示格式清晰 |
| Architecture | ✅ | 遵循现有代码结构，不引入新依赖 |
| Performance | ✅ | 使用简单字符串匹配，O(n) 时间复杂度 |
| Security | ✅ | 不涉及安全敏感操作，仅文件读写 |

## 3. Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                      CLI Entry Point                        │
│                    src/codexspec/__init__.py                │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                     init Command                            │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  CLAUDE.md Processing Logic (ENHANCED)              │   │
│  │  - has_compliance_section()  [NEW]                  │   │
│  │  - prepend_compliance_section()  [NEW]              │   │
│  │  - confirm_add_compliance()  [NEW]                  │   │
│  │  - _get_compliance_section_content()  [NEW]         │   │
│  └─────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│              Slash Command Template (MODIFIED)              │
│            templates/commands/constitution.md               │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  Step X: CLAUDE.md Compliance Check (NEW)           │   │
│  │  - 仅在首次创建时执行                                │   │
│  │  - 检查并提示用户添加 Compliance 部分               │   │
│  └─────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

## 4. Component Structure

```
codexspec/
├── src/codexspec/
│   └── __init__.py           # CLI 实现 (MODIFIED)
│       ├── init()            # 修改 CLAUDE.md 处理逻辑
│       ├── has_compliance_section()      [NEW]
│       ├── prepend_compliance_section()  [NEW]
│       ├── confirm_add_compliance()      [NEW]
│       └── _get_compliance_section_content()  [NEW]
├── templates/commands/
│   └── constitution.md       # Slash command 模板 (MODIFIED)
└── tests/
    └── test_compliance.py    # 单元测试 [NEW]
```

## 5. Module Dependency Graph

```
┌─────────────────────────────┐
│       init() command        │
│    (CLI entry point)        │
└──────────────┬──────────────┘
               │ calls
               ▼
┌─────────────────────────────┐     ┌─────────────────────────────┐
│  has_compliance_section()   │     │  confirm_add_compliance()   │
│  (检测 CLAUDE.md 状态)       │     │  (用户交互确认)              │
└─────────────────────────────┘     └──────────────┬──────────────┘
                                                   │ if confirmed
                                                   ▼
┌─────────────────────────────────────────────────────────────────┐
│              prepend_compliance_section()                        │
│              (追加 Compliance 部分)                               │
└───────────────────────────┬─────────────────────────────────────┘
                            │ calls
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│           _get_compliance_section_content()                      │
│           (返回 Compliance 部分文本)                              │
└─────────────────────────────────────────────────────────────────┘
```

## 6. Module Specifications

### Module: `has_compliance_section()`

- **Responsibility**: 检测 CLAUDE.md 是否已包含 Compliance 部分
- **Dependencies**: 无
- **Interface**: `has_compliance_section(claude_md_path: Path) -> bool`
- **Files**: `src/codexspec/__init__.py` (新增函数)

### Module: `prepend_compliance_section()`

- **Responsibility**: 在 CLAUDE.md 开头追加 Compliance 部分
- **Dependencies**: `_get_compliance_section_content()`
- **Interface**: `prepend_compliance_section(claude_md_path: Path) -> None`
- **Files**: `src/codexspec/__init__.py` (新增函数)

### Module: `confirm_add_compliance()`

- **Responsibility**: 询问用户是否添加 Compliance 部分
- **Dependencies**: `typer.confirm()`, `console`
- **Interface**: `confirm_add_compliance() -> bool`
- **Files**: `src/codexspec/__init__.py` (新增函数)

### Module: `_get_compliance_section_content()`

- **Responsibility**: 返回 Compliance 部分的完整文本
- **Dependencies**: 无
- **Interface**: `_get_compliance_section_content() -> str`
- **Files**: `src/codexspec/__init__.py` (新增函数)

### Module: `init()` command (MODIFIED)

- **Responsibility**: 项目初始化，增强 CLAUDE.md 处理逻辑
- **Dependencies**: 上述所有新函数
- **Interface**: 现有接口不变，内部逻辑增强
- **Files**: `src/codexspec/__init__.py` (修改现有函数)

### Module: `constitution.md` template (MODIFIED)

- **Responsibility**: Slash command 模板，增加首次创建时的 CLAUDE.md 检查
- **Dependencies**: 无（Markdown 模板）
- **Interface**: N/A
- **Files**: `templates/commands/constitution.md` (修改现有模板)

## 7. Data Models

> [!NOTE]
> 本功能不涉及数据模型变更。

## 8. API Contracts

### CLI Command: `codexspec init`

- **Arguments**: `[project_dir]` (可选，默认当前目录)
- **Options**:
  - `--force` / `-f`: 覆盖已有文件
  - `--no-git`: 跳过 git 初始化
  - `--lang TEXT`: 设置语言
- **Output**:
  - 新项目: `[green]Created:[/green] CLAUDE.md`
  - 已有项目 (无 Compliance): 显示询问提示
  - 已有项目 (有 Compliance): 无输出（跳过）
- **Exit Codes**: 0 (成功), 1 (错误)

### 函数接口

```python
def has_compliance_section(claude_md_path: Path) -> bool:
    """Check if CLAUDE.md already contains the compliance section.

    Args:
        claude_md_path: Path to the CLAUDE.md file

    Returns:
        True if the file contains '.codexspec/memory/constitution.md' reference
    """

def prepend_compliance_section(claude_md_path: Path) -> None:
    """Prepend the Constitution Compliance section to CLAUDE.md.

    Args:
        claude_md_path: Path to the CLAUDE.md file
    """

def confirm_add_compliance() -> bool:
    """Ask user whether to add the Constitution Compliance section.

    Returns:
        True if user confirms, False otherwise
    """

def _get_compliance_section_content() -> str:
    """Return the Constitution Compliance section content.

    Returns:
        The complete compliance section text
    """
```

## 9. Implementation Phases

### Phase 1: Foundation (CLI 辅助函数)

- [ ] 添加 `_get_compliance_section_content()` 函数
- [ ] 添加 `has_compliance_section()` 函数
- [ ] 添加 `prepend_compliance_section()` 函数
- [ ] 添加 `confirm_add_compliance()` 函数
- [ ] 为所有新函数编写单元测试

### Phase 2: init 命令增强

- [ ] 修改 `init()` 函数的 CLAUDE.md 处理逻辑
- [ ] 实现条件检测和用户交互流程
- [ ] 保持 `--force` 标志的原有行为
- [ ] 添加集成测试

### Phase 3: constitution 模板增强

- [ ] 在 `templates/commands/constitution.md` 中添加 CLAUDE.md 检查步骤
- [ ] 确保仅在首次创建时执行检查
- [ ] 添加用户提示和确认逻辑

### Phase 4: Testing

#### 4.1 单元测试

- [ ] 测试 `has_compliance_section()` 各场景（存在/不存在/空文件）
- [ ] 测试 `prepend_compliance_section()` 追加逻辑和分隔符
- [ ] 测试 `_get_compliance_section_content()` 返回内容完整性
- [ ] 测试边界情况 (EC-001: 空文件, EC-002: 只有注释, EC-003: 注释中的路径)

#### 4.2 集成测试

- [ ] TC-001: 测试新项目 init 创建完整 CLAUDE.md
- [ ] TC-002: 测试已有 CLAUDE.md 无 Compliance 部分时询问用户
- [ ] TC-003: 测试用户确认后正确追加
- [ ] TC-004: 测试用户拒绝时保持不变
- [ ] TC-005: 测试已有 Compliance 部分时不重复询问
- [ ] TC-008: 测试 --force 标志行为不变

### Phase 5: Documentation

- [ ] 更新 CLAUDE.md 中的实现状态
- [ ] 更新 README.md (如有必要)

## 10. Technical Decisions

### Decision 1: 检测标记选择

- **Choice**: 使用 `.codexspec/memory/constitution.md` 字符串作为检测标记
- **Rationale**:
  - 该路径是 Compliance 部分的核心内容，必然存在
  - 相比标题检测更稳定，不受格式变化影响
  - 简单的字符串匹配，性能开销低
- **Alternatives**:
  - 使用 `## [HIGHEST PRIORITY] CONSTITUTION COMPLIANCE` 标题
  - 使用正则表达式匹配多个可能的格式
- **Trade-offs**:
  - 可能在注释中误检 (EC-003)，但规范明确"宁可漏检也不重复"

### Decision 2: 用户交互方式

- **Choice**: 使用 `typer.confirm()` 进行交互式确认
- **Rationale**:
  - 与现有 CLI 风格一致
  - 提供良好的用户体验
  - 支持默认值 (N) 安全退出
- **Alternatives**:
  - 使用 `--ensure-compliance` 标志
  - 静默添加
- **Trade-offs**:
  - 增加一次交互步骤，但尊重用户选择

### Decision 3: Compliance 内容位置

- **Choice**: 将新函数放在 `src/codexspec/__init__.py` 中
- **Rationale**:
  - 与现有的 `_get_claude_md_content()` 函数位置一致
  - 不引入新的模块结构
  - 保持代码组织简单
- **Alternatives**:
  - 创建独立的 `compliance.py` 模块
- **Trade-offs**:
  - 单文件代码量增加，但功能相关性强，保持内聚

### Decision 4: constitution 模板修改方式

- **Choice**: 在模板中添加独立步骤，通过条件判断执行
- **Rationale**:
  - 清晰的执行流程
  - 易于理解和维护
  - 符合 slash command 模板的设计模式
- **Alternatives**:
  - 创建独立的 `/codexspec.sync-compliance` 命令
- **Trade-offs**:
  - 模板复杂度略增，但避免了命令碎片化

### Decision 5: 错误处理策略

- **Choice**: 依赖 Python 标准异常，不添加额外的错误处理包装
- **Rationale**:
  - 文件操作使用 Python 内置异常（`FileNotFoundError`, `PermissionError`, `IOError`）
  - Typer 会自动捕获并显示友好的错误信息
  - 保持代码简洁，避免过度防御
- **可能遇到的错误场景**:

  | 场景 | 异常类型 | 处理方式 |
  |------|----------|----------|
  | CLAUDE.md 不存在 | `FileNotFoundError` | Python 标准异常，Typer 显示错误 |
  | 无写入权限 | `PermissionError` | Python 标准异常，Typer 显示错误 |
  | 磁盘空间不足 | `IOError` | Python 标准异常，Typer 显示错误 |
  | 文件编码问题 | `UnicodeDecodeError` | Python 标准异常，Typer 显示错误 |

- **Alternatives**:
  - 使用 try-except 包装并自定义错误消息
  - 在操作前检查权限和空间
- **Trade-offs**:
  - 错误消息可能不够友好，但对于 CLI 工具可接受
  - 代码更简洁，符合 "Stability over features" 原则

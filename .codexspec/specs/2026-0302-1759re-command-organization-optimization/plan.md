# 技术实现计划：命令组织优化

## 1. 技术栈

| 类别 | 技术 | 版本 | 备注 |
|------|------|------|------|
| 语言 | Python | >=3.11 | 项目已有约束 |
| CLI 框架 | Typer | >=0.9.0 | 已有依赖 |
| 终端输出 | Rich | >=13.0.0 | 已有依赖 |
| 测试框架 | pytest | >=7.0 | 已有依赖 |
| 代码检查 | ruff | >=0.1.0 | 已有依赖 |

## 2. 宪法一致性审查

| 原则 | 一致性 | 说明 |
|------|--------|------|
| **代码质量** | ✅ | 保持单一职责，新增函数功能明确 |
| **测试标准** | ✅ | 为所有新功能编写单元测试和集成测试 |
| **文档** | ✅ | 更新 README.md 和 CLI --help 文本 |
| **架构** | ✅ | 遵循分离关注点，新增逻辑模块化 |
| **性能** | ✅ | 文件操作高效，满足 NFR-002 要求 |
| **安全** | ✅ | 文件操作使用安全路径处理 |
| **可维护性优先** | ✅ | 代码清晰，逻辑简单 |
| **清晰性优先** | ✅ | 函数命名明确，注释充分 |

## 3. 架构概览

### 3.1 当前架构

```
codexspec init
      │
      ▼
┌─────────────────────────────────────┐
│  templates/commands/*.md            │
│  (源模板文件)                        │
└─────────────────┬───────────────────┘
                  │ 复制
                  ▼
┌─────────────────────────────────────┐
│  .claude/commands/codexspec.*.md    │
│  (目标：根目录，带前缀)               │
└─────────────────────────────────────┘
```

### 3.2 新架构

```
codexspec init
      │
      ├──────────────────────┐
      │                      │
      ▼                      ▼
┌───────────────┐    ┌───────────────────────┐
│ 检测旧结构？   │──是─▶│ 迁移流程 (REQ-003)    │
│ (旧命令存在)  │      │ .claude/commands/     │
└───────┬───────┘      │   codexspec.*.md      │
        │              │         ↓ 移动        │
        │ 否           │ .claude/commands/     │
        │              │   codexspec/*.md      │
        │              └───────────┬───────────┘
        │                          │
        ▼                          ▼
┌───────────────────────────────────────────────┐
│  更新流程 (REQ-004)                            │
│  检测 .claude/commands/codexspec/ 是否存在     │
│      │                                         │
│      ├─ 否 ─▶ 安装新模板                       │
│      │                                         │
│      └─ 是 ─▶ 询问是否更新 ─▶ 覆盖模板         │
└───────────────────────────────────────────────┘
```

### 3.3 目录结构变更

```
变更前:                          变更后:
.claude/commands/               .claude/commands/
├── codexspec.constitution.md   └── codexspec/
├── codexspec.specify.md            ├── constitution.md
├── codexspec.generate-spec.md      ├── specify.md
├── ...                             ├── generate-spec.md
└── codexspec.pr.md                 └── ...
```

## 4. 组件结构

```
src/codexspec/
├── __init__.py          # 主 CLI 入口（修改）
│   ├── init()           # 修改：支持子目录结构和迁移
│   ├── list_commands()  # 新增：显示命令列表
│   └── ...
├── i18n.py              # 国际化（不变）
└── commands/            # 新增：命令相关逻辑模块
    └── installer.py     # 新增：命令安装/迁移逻辑

templates/commands/      # 源模板（不变）
├── constitution.md
├── specify.md
└── ...

tests/
├── test_init.py         # 修改：更新 init 测试
├── test_list_commands.py # 新增：list-commands 测试
└── test_migrations.py   # 新增：迁移逻辑测试
```

## 5. 模块依赖图

```
┌─────────────────────────────────────────────────────┐
│                    CLI Layer                        │
│  ┌─────────────┐     ┌──────────────────┐          │
│  │   init()    │────▶│ list_commands()  │          │
│  └──────┬──────┘     └──────────────────┘          │
└─────────┼───────────────────────────────────────────┘
          │ depends on
          ▼
┌─────────────────────────────────────────────────────┐
│                  Business Logic                     │
│  ┌─────────────────────────────────────────────┐   │
│  │         commands/installer.py               │   │
│  │  ┌─────────────┐  ┌──────────────────────┐  │   │
│  │  │install_cmds│  │migrate_old_structure │  │   │
│  │  └─────────────┘  └──────────────────────┘  │   │
│  │  ┌─────────────┐  ┌──────────────────────┐  │   │
│  │  │detect_old   │  │get_command_metadata  │  │   │
│  │  └─────────────┘  └──────────────────────┘  │   │
│  └─────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────┘
          │ depends on
          ▼
┌─────────────────────────────────────────────────────┐
│                   Utilities                         │
│  ┌─────────────┐  ┌──────────────┐  ┌───────────┐  │
│  │  pathlib    │  │   shutil     │  │   Rich    │  │
│  └─────────────┘  └──────────────┘  └───────────┘  │
└─────────────────────────────────────────────────────┘
```

## 6. 模块规格

### 6.1 模块：`commands/installer.py`（新增）

**职责**：封装命令安装、迁移、检测逻辑

**依赖**：`pathlib`, `shutil`, `rich.console`

**接口**：

```python
from typing import TypedDict

# 常量
COMMANDS_SUBDIR = "codexspec"  # 子目录名
OLD_COMMAND_PREFIX = "codexspec."  # 旧文件前缀

class CommandMetadata(TypedDict):
    """命令元数据结构定义"""
    name: str           # 命令名称（不含前缀），如 "constitution"
    display_name: str   # 显示名称（完整调用名），如 "/codexspec.constitution"
    description: str    # 命令描述，用于 list-commands 输出
    category: str       # 命令类别： "core" | "enhanced" | "git"
    file_name: str      # 模板文件名，如 "constitution.md"

def get_commands_metadata() -> list[CommandMetadata]:
    """获取所有命令的元数据列表

    返回按类别排序的命令元数据列表，用于：
    - list-commands CLI 命令的格式化输出
    - init 命令的已安装命令摘要显示
    """

def detect_old_structure(claude_dir: Path) -> list[Path]:
    """检测旧结构命令文件，返回需要迁移的文件列表"""

def migrate_old_commands(
    claude_dir: Path,
    old_files: list[Path]
) -> bool:
    """迁移旧结构命令到新目录（纯文件操作，无用户交互）

    Args:
        claude_dir: .claude 目录路径
        old_files: 需要迁移的旧文件列表

    Returns:
        True 表示迁移成功，False 表示迁移失败

    Note:
        此函数为纯业务逻辑，不包含用户确认或输出提示。
        用户交互逻辑应在 CLI 层（__init__.py）处理。
    """

def install_commands_to_subdir(
    target_dir: Path,
    templates_dir: Path,
    force: bool = False
) -> int:
    """安装命令到子目录（纯文件操作，无用户交互）

    Args:
        target_dir: 目标 .claude/commands/codexspec 目录
        templates_dir: 源模板目录
        force: 是否强制覆盖已存在的文件

    Returns:
        安装的命令数量

    Note:
        此函数为纯业务逻辑，不包含用户确认或输出提示。
        用户交互逻辑应在 CLI 层（__init__.py）处理。
    """

def should_update_commands(codexspec_dir: Path) -> bool:
    """检查是否需要更新命令（目录已存在）"""
```

**设计原则**：业务逻辑层与 UI 层分离

```
┌─────────────────────────────────────────────────────────┐
│  CLI 层 (__init__.py) - 处理用户交互                     │
│  - 显示提示信息 (console.print)                         │
│  - 询问用户确认 (Confirm.ask)                           │
│  - 调用业务逻辑函数                                     │
│  - 显示操作结果                                         │
└─────────────────────────────────────────────────────────┘
                           │ 调用
                           ▼
┌─────────────────────────────────────────────────────────┐
│  业务逻辑层 (installer.py) - 纯文件操作                  │
│  - 检测/迁移/安装文件                                   │
│  - 不依赖 Console 或任何 UI 组件                        │
│  - 通过返回值传递结果                                   │
└─────────────────────────────────────────────────────────┘
```

**文件**：新建 `src/codexspec/commands/__init__.py`, `src/codexspec/commands/installer.py`

### 6.2 模块：`__init__.py`（修改）

**职责**：CLI 入口点，处理用户交互，调用 installer 模块

**修改点**：

1. **`init()` 函数**：

   ```python
   # 示例：迁移流程的 UI 处理
   old_files = detect_old_structure(claude_dir)
   if old_files:
       console.print(f"[yellow]发现 {len(old_files)} 个旧结构命令文件[/yellow]")
       if Confirm.ask("是否迁移到新结构?", default=True):
           if migrate_old_commands(claude_dir, old_files):
               console.print("[green]✓ 迁移完成[/green]")
           else:
               console.print("[red]✗ 迁移失败[/red]")
       else:
           console.print("[dim]跳过迁移[/dim]")

   # 示例：安装/更新流程的 UI 处理
   if should_update_commands(codexspec_dir):
       if Confirm.ask("是否更新命令模板?", default=True):
           count = install_commands_to_subdir(target_dir, templates_dir, force=True)
           console.print(f"[green]✓ 已更新 {count} 个命令[/green]")
   else:
       count = install_commands_to_subdir(target_dir, templates_dir)
       console.print(f"[green]✓ 已安装 {count} 个命令[/green]")
   ```

2. **新增 `list_commands()` 函数**：
   - 调用 `get_commands_metadata()` 获取命令信息
   - 使用 Rich Table 格式化输出

**文件**：修改 `src/codexspec/__init__.py`

## 7. CLI 命令规格

### 7.1 命令：`codexspec init`（修改）

**参数**：（保持不变）

| 参数 | 类型 | 说明 |
|------|------|------|
| `project_name` | str | 项目目录名 |
| `--here` / `-h` | flag | 在当前目录初始化 |
| `--ai` / `-a` | str | AI 助手类型 |
| `--lang` / `-l` | str | 输出语言 |
| `--force` / `-f` | flag | 强制覆盖 |
| `--no-git` | flag | 跳过 git 初始化 |

**新增行为**：

1. 检测 `.claude/commands/codexspec.*.md` 文件
2. 如果存在，提示迁移
3. 安装命令到 `.claude/commands/codexspec/` 子目录
4. 显示增强的输出摘要

**退出码**：

| 码 | 含义 |
|----|------|
| 0 | 成功 |
| 1 | 一般错误 |
| 2 | 权限错误 |

### 7.2 命令：`codexspec list-commands`（新增）

**参数**：无

**输出格式**：

```
CodexSpec 可用命令 (共 16 个)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📋 核心命令 (Core Commands)

  /codexspec.constitution
      创建或更新项目宪法，定义开发原则和规范

  ...

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💡 提示：运行 codexspec init 安装命令到项目
```

**退出码**：

| 码 | 含义 |
|----|------|
| 0 | 成功 |

## 8. 实现阶段

### Phase 1：基础设施（1-2 小时）

- [ ] 创建 `src/codexspec/commands/` 目录
- [ ] 创建 `src/codexspec/commands/__init__.py`
- [ ] 创建 `src/codexspec/commands/installer.py` 骨架
- [ ] 定义 `COMMANDS_SUBDIR`, `OLD_COMMAND_PREFIX` 常量
- [ ] 实现 `get_commands_metadata()` 函数

### Phase 2：核心功能（2-3 小时）

- [ ] 实现 `detect_old_structure()` - 检测旧结构
- [ ] 实现 `migrate_old_commands()` - 迁移逻辑
- [ ] 实现 `install_commands_to_subdir()` - 安装到子目录
- [ ] 实现 `should_update_commands()` - 更新检测
- [ ] 修改 `init()` 函数调用新逻辑

### Phase 3：list-commands 命令（1 小时）

- [ ] 实现 `list_commands()` CLI 函数
- [ ] 注册到 Typer app
- [ ] 格式化输出（Rich Table）

### Phase 4：输出增强（1 小时）

- [ ] 修改 `init()` 输出格式
- [ ] 添加命令列表摘要
- [ ] 添加 Git 管理提示
- [ ] 移除自动添加 `.claude/` 到 `.gitignore` 的逻辑

### Phase 5：测试（2-3 小时）

- [ ] 单元测试：`test_get_commands_metadata()`
- [ ] 单元测试：`test_detect_old_structure()`
- [ ] 单元测试：`test_migrate_old_commands()`
- [ ] 集成测试：`test_init_new_structure()`
- [ ] 集成测试：`test_init_migration()`
- [ ] 集成测试：`test_init_update()`
- [ ] 集成测试：`test_list_commands()`

### Phase 6：文档更新（1 小时）

- [ ] 更新 README.md 说明新结构
- [ ] 更新 CLI `--help` 文本
- [ ] 更新 `CLAUDE.md` 项目文档

## 9. 技术决策

### 决策 1：子目录命名

- **选择**：使用 `codexspec` 作为子目录名
- **理由**：与命令前缀一致，用户容易理解
- **替代方案**：使用 `codexspec-commands`（更明确但更长）
- **权衡**：简短 vs 明确性，选择简短

### 决策 2：迁移策略

- **选择**：移动文件而非复制
- **理由**：避免重复，用户通过 Git 管理变更
- **替代方案**：复制后保留旧文件（可能导致混淆）
- **权衡**：简单 vs 安全，选择简单并依赖 Git

### 决策 3：模块化

- **选择**：创建独立的 `commands/installer.py` 模块
- **理由**：分离关注点，便于测试和维护
- **替代方案**：所有逻辑放在 `__init__.py`
- **权衡**：复杂度 vs 可维护性，选择可维护性

### 决策 4：命令元数据来源

- **选择**：在代码中硬编码命令元数据
- **理由**：简单直接，命令数量固定
- **替代方案**：从模板文件动态解析（复杂度高）
- **权衡**：灵活性 vs 简单性，选择简单性

### 决策 5：更新时的覆盖策略

- **选择**：直接覆盖，依赖 Git 进行恢复
- **理由**：与需求一致，简化实现
- **替代方案**：检测修改并询问每个文件（过于复杂）
- **权衡**：用户体验 vs 实现复杂度，选择简单实现

## 10. 风险与缓解

| 风险 | 可能性 | 影响 | 缓解措施 |
|------|--------|------|----------|
| 迁移过程中断导致数据丢失 | 低 | 高 | 提示用户确保已提交 Git |
| 旧结构检测误报 | 低 | 中 | 使用精确的前缀匹配 |
| Claude Code 子目录支持变化 | 低 | 高 | 已验证可行，监控更新 |
| 性能不达标 | 低 | 中 | 使用高效的文件操作 |

> **简化说明**：根据澄清，不需要特殊处理 Git 未初始化和权限问题。迁移时旧文件直接移动到新位置，然后统一询问是否覆盖模板。

## 11. 验收检查清单

### 功能验收

- [ ] 新项目 init 后命令在 `.claude/commands/codexspec/` 目录
- [ ] 旧结构用户运行 init 后命令被迁移（旧文件移动到新位置）
- [ ] 迁移后根目录的旧文件被删除
- [ ] 迁移后询问用户是否用模板覆盖命令
- [ ] `list-commands` 显示所有 16 个命令
- [ ] init 输出包含命令摘要和 Git 提示

### 性能验收

- [ ] init 执行时间 < 3 秒
- [ ] list-commands 响应时间 < 1 秒

### 兼容性验收

- [ ] 旧项目不迁移仍可正常使用
- [ ] 用户可选择不迁移（拒绝迁移提示）
- [ ] 用户可选择不覆盖（拒绝覆盖提示）

### 文档验收

- [ ] README.md 更新
- [ ] CLI --help 文本准确

---

*计划版本：1.0*
*创建日期：2026-03-02*
*基于 spec.md v1.0 生成*

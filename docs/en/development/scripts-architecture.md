# Scripts 架构分析

本文档详细说明 CodexSpec 项目中 scripts 的代码逻辑流程以及它们如何在 Claude Code 中被使用。

## 1. 整体架构概述

CodexSpec 是一个 **Spec-Driven Development (SDD)** 工具包，采用 CLI + 模板 + 辅助脚本的三层架构：

```
┌─────────────────────────────────────────────────────────────────┐
│                        用户层 (CLI)                             │
│  codexspec init | check | version | config                      │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                    Claude Code 交互层                            │
│  /codexspec.specify | /codexspec.analyze | ...                  │
│  (.claude/commands/*.md)                                        │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                      辅助脚本层                                  │
│  .codexspec/scripts/*.sh (Bash) 或 *.ps1 (PowerShell)          │
└─────────────────────────────────────────────────────────────────┘
```

## 2. Scripts 的部署流程

### 阶段 1: `codexspec init` 初始化

在 `src/codexspec/__init__.py` 的 `init()` 函数中（第 343-368 行），根据操作系统自动复制对应脚本：

```python
# Copy helper scripts based on platform
scripts_source_dir = get_scripts_dir()
if scripts_source_dir.exists():
    if sys.platform == "win32":
        # Windows: 复制 PowerShell 脚本
        ps_scripts = scripts_source_dir / "powershell"
        for script_file in ps_scripts.glob("*.ps1"):
            dest_file = codexspec_dir / "scripts" / script_file.name
            dest_file.write_text(script_file.read_text(encoding="utf-8"), encoding="utf-8")
    else:
        # macOS/Linux: 复制 Bash 脚本
        bash_scripts = scripts_source_dir / "bash"
        for script_file in bash_scripts.glob("*.sh"):
            dest_file = codexspec_dir / "scripts" / script_file.name
            dest_file.write_text(script_file.read_text(encoding="utf-8"), encoding="utf-8")
```

**结果**: 根据操作系统，将 `scripts/bash/` 或 `scripts/powershell/` 中的脚本复制到项目的 `.codexspec/scripts/` 目录。

### 路径解析机制

`get_scripts_dir()` 函数（第 71-90 行）处理多种安装场景：

```python
def get_scripts_dir() -> Path:
    # Path 1: Wheel install - scripts packaged inside codexspec package
    installed_scripts = Path(__file__).parent / "scripts"
    if installed_scripts.exists():
        return installed_scripts

    # Path 2: Development/editable install - scripts in project root
    dev_scripts = Path(__file__).parent.parent.parent / "scripts"
    if dev_scripts.exists():
        return dev_scripts

    # Path 3: Fallback
    return installed_scripts
```

## 3. Scripts 在 Claude Code 中的调用机制

### 核心机制：YAML Frontmatter 声明

模板文件通过 YAML frontmatter 声明脚本依赖：

```yaml
---
description: 命令描述
scripts:
  sh: .codexspec/scripts/check-prerequisites.sh --json --require-tasks --include-tasks
  ps: .codexspec/scripts/check-prerequisites.ps1 -Json -RequireTasks -IncludeTasks
---
```

### 占位符替换

在模板中使用 `{SCRIPT}` 占位符：

```markdown
### 1. Initialize Context

Run `{SCRIPT}` from repo root and parse JSON for:
- `FEATURE_DIR` - Feature directory path
- `AVAILABLE_DOCS` - Available documents list
```

### 调用流程

1. 用户在 Claude Code 中输入 `/codexspec.analyze`
2. Claude 读取 `.claude/commands/codexspec.analyze.md` 模板
3. 根据操作系统，Claude 将 `{SCRIPT}` 替换为：
   - **macOS/Linux**: `.codexspec/scripts/check-prerequisites.sh --json --require-tasks --include-tasks`
   - **Windows**: `.codexspec/scripts/check-prerequisites.ps1 -Json -RequireTasks -IncludeTasks`
4. Claude 执行脚本，解析 JSON 输出，继续后续操作

## 4. Scripts 功能详解

### 4.1 `check-prerequisites.sh/ps1` - 前置检查脚本

这是最重要的脚本，用于验证环境状态并返回结构化信息。

#### 核心功能

- 验证当前是否在 feature 分支（格式: `001-feature-name`）
- 检测必需文件是否存在 (`plan.md`, `tasks.md`)
- 返回 JSON 格式的路径信息

#### 参数选项

| 参数 | Bash | PowerShell | 作用 |
|------|------|------------|------|
| JSON 输出 | `--json` | `-Json` | 输出 JSON 格式 |
| 要求 tasks.md | `--require-tasks` | `-RequireTasks` | 验证 tasks.md 存在 |
| 包含 tasks.md | `--include-tasks` | `-IncludeTasks` | 在 AVAILABLE_DOCS 中包含 tasks.md |
| 仅路径 | `--paths-only` | `-PathsOnly` | 跳过验证，仅输出路径 |

#### JSON 输出示例

```json
{
  "FEATURE_DIR": "/path/to/.codexspec/specs/001-my-feature",
  "AVAILABLE_DOCS": ["research.md", "data-model.md", "tasks.md"]
}
```

### 4.2 `common.sh/ps1` - 通用工具函数

提供跨平台的通用功能：

#### Bash 版本函数

| 函数 | 作用 |
|------|------|
| `get_feature_id()` | 从 Git 分支或环境变量获取 feature ID |
| `get_specs_dir()` | 获取 specs 目录路径 |
| `is_codexspec_project()` | 检查是否在 CodexSpec 项目中 |
| `require_codexspec_project()` | 确保在 CodexSpec 项目中，否则退出 |
| `log_info/success/warning/error()` | 彩色日志输出 |
| `command_exists()` | 检查命令是否存在 |

#### PowerShell 版本函数

| 函数 | 作用 |
|------|------|
| `Get-RepoRoot` | 获取 Git 仓库根目录 |
| `Get-CurrentBranch` | 获取当前分支名 |
| `Test-HasGit` | 检测是否有 Git 仓库 |
| `Test-FeatureBranch` | 验证是否在 feature 分支 |
| `Get-FeaturePathsEnv` | 获取所有 feature 相关路径 |
| `Test-FileExists` | 检查文件是否存在 |
| `Test-DirHasFiles` | 检查目录是否有文件 |

### 4.3 `create-new-feature.sh/ps1` - 创建新功能

#### 功能

- 自动生成递增的 feature ID（001, 002, ...）
- 创建 feature 目录和初始 spec.md
- 创建对应的 Git 分支

#### 使用示例

```bash
./create-new-feature.sh -n "user authentication" -i 001
```

## 5. 使用 Scripts 的命令

以下 4 个命令使用 scripts：

| 命令 | Scripts 参数 | 作用 |
|------|--------------|------|
| `/codexspec.clarify` | `--json --paths-only` | 获取路径，不验证文件 |
| `/codexspec.checklist` | `--json` | 验证 plan.md 存在 |
| `/codexspec.analyze` | `--json --require-tasks --include-tasks` | 验证 plan.md + tasks.md |
| `/codexspec.tasks-to-issues` | `--json --require-tasks --include-tasks` | 验证 plan.md + tasks.md |

## 6. 完整工作流程图

```
┌──────────────────────────────────────────────────────────────────────────┐
│                        初始化阶段                                         │
│                                                                          │
│  $ codexspec init my-project                                             │
│       │                                                                  │
│       ├── 创建 .codexspec/ 目录结构                                      │
│       ├── 复制 scripts/*.sh → .codexspec/scripts/                       │
│       ├── 复制 templates/commands/*.md → .claude/commands/              │
│       └── 创建 constitution.md, config.yml, CLAUDE.md                   │
│                                                                          │
└──────────────────────────────────────────────────────────────────────────┘
                                    ↓
┌──────────────────────────────────────────────────────────────────────────┐
│                        使用阶段 (Claude Code)                             │
│                                                                          │
│  用户: /codexspec.analyze                                                │
│       │                                                                  │
│       ├── Claude 读取 .claude/commands/codexspec.analyze.md             │
│       │                                                                  │
│       ├── 解析 YAML frontmatter 中的 scripts 声明                        │
│       │   scripts:                                                       │
│       │     sh: .codexspec/scripts/check-prerequisites.sh --json ...    │
│       │                                                                  │
│       ├── 替换 {SCRIPT} 占位符                                           │
│       │                                                                  │
│       ├── 执行脚本:                                                      │
│       │   $ .codexspec/scripts/check-prerequisites.sh --json ...        │
│       │                                                                  │
│       ├── 解析 JSON 输出:                                                │
│       │   {"FEATURE_DIR": "...", "AVAILABLE_DOCS": [...]}               │
│       │                                                                  │
│       ├── 读取 spec.md, plan.md, tasks.md                               │
│       │                                                                  │
│       └── 生成分析报告                                                   │
│                                                                          │
└──────────────────────────────────────────────────────────────────────────┘
```

## 7. 设计亮点

### 7.1 跨平台兼容

同时维护 Bash 和 PowerShell 版本，通过 `sys.platform` 自动选择：

```python
if sys.platform == "win32":
    # 复制 PowerShell 脚本
else:
    # 复制 Bash 脚本
```

### 7.2 声明式配置

通过 YAML frontmatter 声明脚本依赖，清晰直观：

```yaml
scripts:
  sh: .codexspec/scripts/check-prerequisites.sh --json
  ps: .codexspec/scripts/check-prerequisites.ps1 -Json
```

### 7.3 JSON 输出

脚本输出结构化数据，便于 Claude 解析：

```json
{
  "FEATURE_DIR": "/path/to/.codexspec/specs/001-feature",
  "AVAILABLE_DOCS": ["research.md", "data-model.md"]
}
```

### 7.4 渐进式验证

不同命令使用不同参数，按需验证：

| 阶段 | 命令 | 验证级别 |
|------|------|----------|
| 规划前 | `/codexspec.clarify` | 仅路径 |
| 规划后 | `/codexspec.checklist` | plan.md |
| 任务后 | `/codexspec.analyze` | plan.md + tasks.md |

### 7.5 Git 集成

- 自动从分支名提取 feature ID
- 支持分支命名验证（`^\d{3}-` 格式）
- 支持环境变量覆盖（`SPECIFY_FEATURE` / `CODEXSPEC_FEATURE`）

## 8. 关键代码路径

| 文件 | 行号/位置 | 功能 |
|------|-----------|------|
| `src/codexspec/__init__.py` | 343-368 | 脚本复制逻辑 |
| `src/codexspec/__init__.py` | 71-90 | `get_scripts_dir()` 路径解析 |
| `scripts/bash/check-prerequisites.sh` | 全文 | Bash 前置检查主脚本 |
| `scripts/powershell/check-prerequisites.ps1` | 56-146 | PowerShell 前置检查脚本 |
| `scripts/bash/common.sh` | 全文 | Bash 通用工具函数 |
| `scripts/powershell/common.ps1` | 全文 | PowerShell 通用工具函数 |
| `templates/commands/*.md` | YAML frontmatter | 脚本声明 |

## 9. 脚本文件清单

### Bash 脚本 (`scripts/bash/`)

```
scripts/bash/
├── check-prerequisites.sh   # 前置检查主脚本
├── common.sh                # 通用工具函数
└── create-new-feature.sh    # 创建新功能
```

### PowerShell 脚本 (`scripts/powershell/`)

```
scripts/powershell/
├── check-prerequisites.ps1  # 前置检查主脚本
├── common.ps1               # 通用工具函数
└── create-new-feature.ps1   # 创建新功能
```

---

*本文档记录了 CodexSpec 项目中 scripts 的完整架构和使用流程。如有更新，请同步修改。*

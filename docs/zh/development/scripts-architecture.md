# 脚本与安装架构

## 运行时与命令源文件

`src/codexspec/` 中的 Python CLI 从 `templates/commands/` 安装完整命令模板，同时安装文档模板和共享审查标准。Claude Code 使用斜杠命令，Codex 使用由同一份命令源文件生成的原生技能。28 个公开命令在两种助手中遵循相同的工作流约定。

## 安装与项目上下文

`codexspec init` 根据平台和所选助手安装对应集成。共享资源位于 `.codexspec/`，Claude 命令位于 `.claude/commands/codexspec/`，Codex 技能位于 `.agents/skills/`。安装后的 CLI 还提供工作流所需的工作区路由和带保护检查的辅助操作。

初始化会更新现有 `AGENTS.md` 和 `CLAUDE.md` 中由 CodexSpec 管理的内容块，并保留块外自行编写的项目内容。`--force` 会刷新安装工件并确认更新提示，不会替换整个上下文文件，也不会丢弃无关配置。仅安装 CLI 不会初始化项目。

## 平台辅助脚本

Unix 项目使用 `scripts/bash/` 中的 Bash 脚本，Windows 项目使用 `scripts/powershell/` 中的 PowerShell 脚本。功能创建与前置条件检查会解析所选功能，并返回机器可读的上下文。`common.sh` 和 `common.ps1` 提供各平台共用的工具函数，`review-context` 负责支持审查目标信息收集。两个平台都会将独立提交运行时从 `src/codexspec/commit_runtime.py` 复制到 `.codexspec/scripts/commit-staged-helper.py`。

## 功能标识与工件兼容

功能名称采用 `YYYY-MMDD-HHMMss-name` 格式：分钟级时间戳、两个小写字母或数字组成的后缀，以及 ASCII 名称。完整功能名标识一个工作区，后续通过其明确路径或分支继续。系统不支持顺序编号的 `NNN-name` 标识。对历史功能的兼容针对工件：旧功能可能缺少 `requirements.md` 或 `design.md`，命令会说明由此造成的追溯限制，不会虚构最初的确认记录。

## 贡献者维护规则

修改权威源文件后，应重新生成派生副本并验证分发结果。采用片段机制的命令在 `internal/command_templates/sources/` 中编写，其完整的 `templates/commands/` 文件由工具生成；其他命令模板仍直接编写。不要手工修改安装后的 Claude 或 Codex 副本。

打包范围包括公开模板和两个平台脚本目录。`internal/` 中的维护工具、`docs/` 中的站点源文件、测试，以及流程图源文件和图片均不进入安装包。不要将脚本打包范围扩大到整个 `scripts/`。

<a id="extension-materials"></a>

## 扩展开发资料

仓库提供扩展清单模板、示例命令和[扩展开发指南](https://github.com/Zts0hg/codexspec/blob/main/extensions/EXTENSION-DEVELOPMENT-GUIDE.md)，供编写扩展时参考。当前 CLI 尚未提供安装、列出或移除扩展的命令，也不会自动加载 `extension.yml` 中定义的命令和钩子。需要项目专用的审查规则时，可以在 `.codexspec/review-code/` 中添加内容；初始化会保留已修改的资源和附加文件，除非明确要求替换。

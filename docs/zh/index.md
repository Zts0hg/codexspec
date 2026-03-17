# 欢迎使用 CodexSpec

[![PyPI version](https://img.shields.io/pypi/v/codexspec:svg)](https://pypi.org/project/codexspec/)
[![Python](https://img.shields.io/pypi/pyversions/codexspec:svg)](https://pypi.org/project/codexspec/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**一款专为 Claude Code 打造的规格驱动开发（SDD）工具包**

CodexSpec 是一款工具包，帮助你使用结构化的、规格驱动的方法来构建高质量软件。它颠覆了传统开发模式，将规格说明转化为可执行的工件，直接指导实现过程。

## 为什么选择 CodexSpec？

### 人机协作

CodexSpec 的核心理念是：**有效的 AI 辅助开发需要在每个阶段都有人类的主动参与**。

| 问题 | 解决方案 |
|------|----------|
| 需求不清晰 | 在构建之前通过交互式问答进行澄清 |
| 规格说明不完整 | 专用的审查命令，带有评分功能 |
| 技术方案与意图偏离 | 基于 Constitution（宪法）的验证机制 |
| 任务分解模糊 | 强制 TDD 的任务生成 |

### 核心特性

- **Constitution 驱动** - 建立项目原则，指导所有决策
- **交互式澄清** - 基于问答的需求细化
- **审查命令** - 在每个阶段验证工件
- **TDD 就绪** - 内置测试优先的任务方法论
- **i18n 支持** - 通过 LLM 翻译支持 13+ 种语言

## 快速开始

```bash
# 安装
uv tool install codexspec

# 创建新项目
codexspec init my-project

# 或在现有项目中初始化
codexspec init . --ai claude
```

[完整安装指南](getting-started/installation.md)

## 工作流程概览

```
想法 -> 澄清 -> 审查 -> 规划 -> 审查 -> 任务 -> 审查 -> 实现
            ^              ^              ^
         人工检查        人工检查        人工检查
```

每个工件都有对应的审查命令，在继续之前验证 AI 输出。

[了解工作流程](user-guide/workflow.md)

## 许可证

MIT 许可证 - 详情请参阅 [LICENSE](https://github.com/Zts0hg/codexspec/blob/main/LICENSE)。

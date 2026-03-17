# 快速开始

## 1. 初始化项目

安装完成后，创建或初始化你的项目：

```bash
# 创建新项目
codexspec init my-awesome-project

# 或在当前目录初始化
codexspec init . --ai claude

# 使用中文输出
codexspec init my-project --lang zh-CN
```

## 2. 建立项目原则

在项目目录中启动 Claude Code：

```bash
cd my-awesome-project
claude
```

使用 constitution 命令：

```
/codexspec:constitution 创建专注于代码质量和测试的原则
```

## 3. 澄清需求

使用 `/codexspec:specify` 探索需求：

```
/codexspec:specify 我想构建一个任务管理应用程序
```

## 4. 生成规格说明

澄清完成后，生成规格文档：

```
/codexspec:generate-spec
```

## 5. 审查和验证

**推荐：** 在继续之前进行验证：

```
/codexspec:review-spec
```

## 6. 创建技术方案

```
/codexspec:spec-to-plan 使用 Python FastAPI 作为后端
```

## 7. 生成任务

```
/codexspec:plan-to-tasks
```

## 8. 实现

```
/codexspec:implement-tasks
```

## 项目结构

初始化后的目录结构：

```
my-project/
+-- .codexspec/
|   +-- memory/
|   |   +-- constitution.md
|   +-- specs/
|   |   +-- {feature-id}/
|   |       +-- spec.md
|   |       +-- plan.md
|   |       +-- tasks.md
|   +-- scripts/
+-- .claude/
|   +-- commands/
+-- CLAUDE.md
```

## 下一步

[完整工作流程指南](../user-guide/workflow.md)

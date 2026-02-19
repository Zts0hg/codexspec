# MkDocs 文档站点设计

## 概述

为 CodexSpec 项目实现基于 MkDocs + Material 主题的文档站点，支持 GitHub Pages 自动部署。

## 目标

1. 提供专业、现代的项目文档站点
2. 自动部署到 GitHub Pages
3. 支持深色/浅色主题切换
4. 提供搜索功能
5. 迁移现有文档内容

## 技术选型

| 组件 | 选择 | 理由 |
|------|------|------|
| 文档框架 | MkDocs | Python 原生，配置简单 |
| 主题 | Material for MkDocs | 现代、美观、功能丰富 |
| API 文档 | mkdocstrings | 支持 Python API 自动文档 |
| 部署 | GitHub Pages + Actions | 免费托管，自动部署 |

## 目录结构

```
codexspec/
├── mkdocs.yml              # MkDocs 配置文件
├── docs/
│   ├── index.md            # 首页
│   ├── getting-started/
│   │   ├── installation.md
│   │   └── quick-start.md
│   ├── user-guide/
│   │   ├── workflow.md
│   │   ├── commands.md
│   │   └── i18n.md
│   ├── reference/
│   │   ├── cli.md
│   │   └── configuration.md
│   ├── development/
│   │   └── contributing.md
│   └── assets/
│       └── images/
└── .github/workflows/
    └── docs.yml            # 自动部署工作流
```

## 依赖配置

```toml
[project.optional-dependencies]
docs = [
    "mkdocs>=1.5.0",
    "mkdocs-material>=9.5.0",
    "mkdocstrings[python]>=0.24.0",
]
```

## MkDocs 配置

### 站点信息

- 站点名称: CodexSpec
- 站点 URL: https://zts0hg.github.io/codexspec/
- 仓库: https://github.com/Zts0hg/codexspec

### 主题配置

- Material 主题
- 支持深色/浅色模式自动切换
- 主色调: Indigo
- 功能: 即时导航、搜索高亮、代码复制按钮

### 导航结构

1. Home - 首页
2. Getting Started - 入门指南
   - Installation
   - Quick Start
3. User Guide - 用户指南
   - Workflow
   - Commands
   - Internationalization
4. Reference - 参考
   - CLI
   - Configuration
5. Development - 开发
   - Contributing

### Markdown 扩展

- 代码高亮 (pymdownx.highlight)
- 代码块 (pymdownx.superfences)
- 标签页 (pymdownx.tabbed)
- 提示框 (admonition)
- 详情折叠 (pymdownx.details)

## GitHub Actions 工作流

### 触发条件

- 推送到 main 分支
- 仅在 docs/、mkdocs.yml、src/ 变更时触发
- 支持手动触发

### 部署步骤

1. 检出代码
2. 安装 Python 3.11
3. 安装文档依赖
4. 构建 MkDocs 站点
5. 部署到 GitHub Pages

## 文档内容迁移

| 新文件 | 来源 |
|--------|------|
| index.md | README.md (项目介绍) |
| getting-started/installation.md | README.md (安装部分) |
| getting-started/quick-start.md | README.md (快速开始) |
| user-guide/workflow.md | README.md (使用流程) |
| user-guide/commands.md | docs/commands.md |
| user-guide/i18n.md | README.md (i18n 部分) |
| reference/cli.md | README.md (CLI 部分) |
| reference/configuration.md | 新建 |
| development/contributing.md | README.md (开发部分) |

## 本地开发命令

```bash
# 安装依赖
uv sync --extra docs

# 本地预览
uv run mkdocs serve

# 构建
uv run mkdocs build
```

## 实现步骤

1. 更新 pyproject.toml 添加文档依赖
2. 创建 mkdocs.yml 配置文件
3. 创建 docs/ 目录结构
4. 迁移现有文档内容
5. 创建 GitHub Actions 工作流
6. 测试本地构建
7. 提交并验证自动部署

## 验收标准

- [ ] 本地 `mkdocs serve` 正常运行
- [ ] 所有文档页面可访问
- [ ] 深色/浅色主题切换正常
- [ ] 搜索功能正常
- [ ] GitHub Actions 自动部署成功
- [ ] GitHub Pages 站点可访问

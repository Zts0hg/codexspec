# 贡献指南

## 前提条件

- Python 3.11+
- uv 包管理器
- Git

## 本地开发

```bash
# Clone the repository
git clone https://github.com/Zts0hg/codexspec.git
cd codexspec

# Install development dependencies
uv sync --extra dev

# Run locally
uv run codexspec --help

# Run tests
uv run pytest

# Lint code
uv run ruff check src/
```

## 文档

```bash
# Install docs dependencies
uv sync --extra dev --extra docs

# Preview documentation locally
uv run mkdocs serve

# Build documentation
uv run mkdocs build --strict
```

## 构建

```bash
uv build
```

## Pull Request 流程

1. Fork 仓库
2. 创建功能分支
3. 进行更改
4. 运行测试和代码检查
5. 提交 Pull Request

## 代码风格

- 行长度：最大 120 个字符
- 遵循 PEP 8
- 为公共函数使用类型提示

修改模板、打包或初始化行为前，请先阅读 [CLAUDE.md](https://github.com/Zts0hg/codexspec/blob/main/CLAUDE.md)、[AGENTS.md](https://github.com/Zts0hg/codexspec/blob/main/AGENTS.md) 和[仓库布局](https://github.com/Zts0hg/codexspec/blob/main/docs/internal/repository-layout.md)。分发的命令和技能副本由源文件生成，属于安装产物；修改时应编辑对应的源文件，再重新生成副本。

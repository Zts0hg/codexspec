# 贡献指南

## 前提条件

- Python 3.11+
- uv 包管理器
- Git

## 本地开发

```bash
# 克隆仓库
git clone https://github.com/Zts0hg/codexspec:git
cd codexspec

# 安装开发依赖
uv sync --dev

# 本地运行
uv run codexspec --help

# 运行测试
uv run pytest

# 代码检查
uv run ruff check src/
```

## 文档

```bash
# 安装文档依赖
uv sync --extra docs

# 本地预览文档
uv run mkdocs serve

# 构建文档
uv run mkdocs build
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

# 安装

## 前提条件

- Python 3.11+
- [uv](https://docs.astral.sh/uv/)（推荐）或 pip

## 方式一：使用 uv 安装（推荐）

安装 CodexSpec 最简单的方法是使用 uv：

```bash
uv tool install codexspec
```

## 方式二：使用 pip 安装

你也可以使用 pip：

```bash
pip install codexspec
```

## 方式三：一次性使用

无需安装即可直接运行：

```bash
# 创建新项目
uvx codexspec init my-project

# 在现有项目中初始化
cd your-existing-project
uvx codexspec init . --ai claude
```

## 方式四：从 GitHub 安装

获取最新开发版本：

```bash
# 使用 uv
uv tool install git+https://github.com/Zts0hg/codexspec:git

# 使用 pip
pip install git+https://github.com/Zts0hg/codexspec:git

# 指定分支或标签
uv tool install git+https://github.com/Zts0hg/codexspec:git@main
uv tool install git+https://github.com/Zts0hg/codexspec:git@v0.2.0
```

## 验证安装

```bash
codexspec --help
codexspec version
```

## 升级

```bash
# 使用 uv
uv tool install codexspec --upgrade

# 使用 pip
pip install --upgrade codexspec
```

## 下一步

[快速开始](quick-start.md)

# Pre-commit Hooks 使用指南

本文档介绍项目中配置的 pre-commit hooks 及其使用方法。

## 安装

```bash
# 安装 pre-commit hooks
uv run pre-commit install --install-hooks

# 手动安装所有 hook 环境（可选，首次运行时会自动安装）
uv run pre-commit install-hooks
```

## 可用 Hooks

### Python 代码质量

| Hook | 说明 | 自动修复 |
|------|------|---------|
| **ruff** | Python 代码检查 | ✅ `--fix` |
| **ruff-format** | Python 代码格式化 | ✅ |
| **mypy** | 静态类型检查 | ❌ |
| **bandit** | 安全漏洞检查 | ❌ |

### 通用文件检查

| Hook | 说明 | 自动修复 |
|------|------|---------|
| **trailing-whitespace** | 移除行尾空格 | ✅ |
| **end-of-file-fixer** | 确保文件以换行结束 | ✅ |
| **check-yaml** | YAML 语法检查 | ❌ |
| **check-added-large-files** | 检查大文件（>500KB） | ❌ |
| **check-merge-conflict** | 检查合并冲突标记 | ❌ |
| **debug-statements** | 检查调试语句 | ❌ |

### 文档和拼写

| Hook | 说明 | 自动修复 |
|------|------|---------|
| **markdownlint** | Markdown 格式检查 | ✅ `--fix` |
| **codespell** | 拼写检查 | ❌ |

### Shell 脚本

| Hook | 说明 | 自动修复 |
|------|------|---------|
| **shellcheck** | Shell 脚本检查 | ❌ |

### 依赖安全

| Hook | 说明 | 自动修复 |
|------|------|---------|
| **python-safety-dependencies-check** | 依赖安全检查 | ❌ |

### 本地 Hooks

| Hook | 说明 | 触发时机 |
|------|------|---------|
| **pytest** | 运行测试 | pre-commit |
| **commitizen** | 提交信息格式检查 | commit-msg |

## 手动运行

```bash
# 运行所有检查（所有文件）
uv run pre-commit run --all-files

# 运行特定 hook
uv run pre-commit run mypy --all-files
uv run pre-commit run markdownlint --all-files

# 仅检查已修改的文件（增量检查）
uv run pre-commit run
```

## 跳过检查

### 跳过特定 hook

```bash
# 跳过单个 hook
SKIP=mypy git commit -m "your message"

# 跳过多个 hooks
SKIP=mypy,bandit git commit -m "your message"
```

### 跳过所有检查

```bash
# 使用 --no-verify 跳过所有 pre-commit hooks
git commit --no-verify -m "your message"
```

> ⚠️ **警告**: 仅在紧急情况下使用 `--no-verify`，并确保后续修复问题。

## 配置文件

| 文件 | 用途 |
|------|------|
| `.pre-commit-config.yaml` | 主配置文件 |
| `.markdownlint.json` | Markdown 检查规则 |
| `.codespellrc` | 拼写检查配置 |
| `pyproject.toml` | bandit 配置 |

## 常见问题 FAQ

### Q: 首次运行很慢？

A: 首次运行需要安装各 hook 的虚拟环境，可能需要几分钟。后续运行会快很多。

### Q: 如何更新 hook 版本？

```bash
# 自动更新所有 hooks 到最新版本
uv run pre-commit autoupdate

# 更新特定 hook
uv run pre-commit autoupdate --freeze
```

### Q: markdownlint 报错但我不想修复？

A: 可以在 `.markdownlint.json` 中禁用特定规则：

```json
{
  "MD013": false,  // 禁用行长度检查
  "MD033": false   // 允许内联 HTML
}
```

### Q: mypy 报错太多？

A: 可以在 `.pre-commit-config.yaml` 中添加更多忽略参数：

```yaml
args: [--ignore-missing-imports, --no-strict-optional]
```

### Q: bandit 报告安全警告？

A: 在 `pyproject.toml` 的 `[tool.bandit]` 部分添加到 `skips` 列表：

```toml
[tool.bandit]
skips = ["B101", "B603"]  # 跳过特定检查
```

### Q: codespell 误报？

A: 在 `.codespellrc` 中添加忽略词：

```toml
[codespell]
ignore-words-list = word1,word2,word3
```

## CI 集成

项目已配置 CI 自动运行 pre-commit：

- **autofix_prs**: true - 自动修复 PR 中的问题
- **autoupdate_schedule**: weekly - 每周自动更新 hooks

---

*Last updated: 2026-03-16*

# CLI 参考

## 命令

### `codexspec init`

初始化一个新的 CodexSpec 项目。

```bash
codexspec init [PROJECT_NAME] [OPTIONS]
```

**参数：**

| 参数 | 描述 |
|------|------|
| `PROJECT_NAME` | 新项目目录的名称 |

**选项：**

| 选项 | 简写 | 描述 |
|------|------|------|
| `--here` | `-h` | 在当前目录初始化 |
| `--ai` | `-a` | 要使用的 AI 助手（默认：claude） |
| `--lang` | `-l` | 输出语言（如 en、zh-CN、ja） |
| `--force` | `-f` | 强制覆盖现有文件 |
| `--no-git` | | 跳过 git 初始化 |
| `--debug` | `-d` | 启用调试输出 |

**示例：**

```bash
# 创建新项目
codexspec init my-project

# 在当前目录初始化
codexspec init . --ai claude

# 使用中文输出
codexspec init my-project --lang zh-CN
```

---

### `codexspec check`

检查已安装的工具。

```bash
codexspec check
```

---

### `codexspec version`

显示版本信息。

```bash
codexspec version
```

---

### `codexspec config`

查看或修改项目配置。

```bash
codexspec config [OPTIONS]
```

**选项：**

| 选项 | 简写 | 描述 |
|------|------|------|
| `--set-lang` | `-l` | 设置输出语言 |
| `--list-langs` | | 列出所有支持的语言 |

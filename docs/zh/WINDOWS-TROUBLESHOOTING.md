# Windows 故障排除指南

本指南帮助 Windows 用户解决安装和运行 CodexSpec 时的常见问题。

## 问题：CMD 中出现 "spawn codexspec access denied" (OSError 5)

### 症状

- 在 CMD 中运行 `codexspec --version` 或 `codexspec init` 失败，显示 "Access denied" 或 "spawn codexspec access denied (OSError 5)"
- 相同的命令在 PowerShell 中正常工作

### 根本原因

这是由 Windows CMD 和 PowerShell 处理用户环境变量的方式差异造成的：

1. **PATH 环境变量刷新**：当 uv 安装 codexspec 时，它将 `%USERPROFILE%\.local\bin` 添加到用户 PATH。PowerShell 通常能立即识别，而 CMD 可能直到终端重启才会刷新环境变量。

2. **进程创建差异**：CMD 使用 Windows CreateProcess API，而 PowerShell 使用不同的机制，可能对路径解析问题更宽容。

### 解决方案

#### 解决方案 1：使用 PowerShell（推荐）

最简单的解决方案是使用 PowerShell 而不是 CMD：

```powershell
# 在 PowerShell 中安装和运行 codexspec
uv tool install codexspec
codexspec --version
```

#### 解决方案 2：重启 CMD

关闭所有 CMD 窗口并打开一个新的。这会强制 CMD 重新加载环境变量。

#### 解决方案 3：在 CMD 中手动刷新 PATH

```cmd
# 将 uv 的 bin 目录添加到当前会话的 PATH
set PATH=%PATH%;%USERPROFILE%\.local\bin

# 验证
codexspec --version
```

#### 解决方案 4：使用完整路径

```cmd
# 使用完整路径执行 codexspec
%USERPROFILE%\.local\bin\codexspec.exe --version
```

#### 解决方案 5：永久添加到系统 PATH

1. 打开 **系统属性** → **环境变量**
2. 在 **用户变量** 或 **系统变量** 中找到 `Path`
3. 添加：`%USERPROFILE%\.local\bin`
4. 点击确定并重启所有终端

#### 解决方案 6：使用 pipx 代替 uv tool

如果 uv 持续出现问题，使用 pipx 作为替代：

```cmd
# 安装 pipx
pip install pipx
pipx ensurepath

# 重启 CMD，然后安装 codexspec
pipx install codexspec

# 验证
codexspec --version
```

## 验证步骤

要诊断问题，在 CMD 中运行以下命令：

```cmd
# 检查 uv 的 bin 目录是否在 PATH 中
echo %PATH% | findstr ".local\bin"

# 检查 codexspec 可执行文件是否存在
dir %USERPROFILE%\.local\bin\codexspec.*

# 尝试使用完整路径运行
%USERPROFILE%\.local\bin\codexspec.exe --version
```

## 常见问题

### 问题："uv is not recognized"

**原因**：uv 未安装或不在 PATH 中。

**解决方案**：
```powershell
# 使用 PowerShell 安装 uv
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# 重启终端并验证
uv --version
```

### 问题："python is not recognized"

**原因**：Python 未安装或不在 PATH 中。

**解决方案**：
1. 从 [python.org](https://www.python.org/downloads/) 安装 Python 3.11+
2. 安装时，勾选 "Add Python to PATH"
3. 重启终端

### 问题：杀毒软件阻止执行

**症状**：Codexspec 短暂工作后停止，或显示间歇性错误。

**解决方案**：将 codexspec 添加到杀毒软件白名单：
- **Windows Defender**：设置 → 更新和安全 → Windows 安全中心 → 病毒和威胁防护 → 管理设置 → 排除项
- 添加路径：`%USERPROFILE%\.local\bin\codexspec.exe`

## 相关资源

- [uv GitHub Issue #16747](https://github.com/astral-sh/uv/issues/16747) - uv 在 Windows 上的已知权限问题
- [uv Windows 安装指南](https://docs.astral.sh/uv/getting-started/installation/)
- [pipx 文档](https://pypa.github.io/pipx/) - 替代的 Python 应用安装器

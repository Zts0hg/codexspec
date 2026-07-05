# Windows 故障排除指南

本指南旨在帮助 Windows 用户解决安装和运行 CodexSpec 时遇到的常见问题。

## 问题：CMD 中出现 "spawn codexspec access denied" (OSError 5)

### 症状

- 在 CMD 中运行 `codexspec --version` 或 `codexspec init` 失败，提示 "Access denied" 或 "spawn codexspec access denied (OSError 5)"
- 同样的命令在 PowerShell 中可以正常运行

### 根本原因

该问题源于 Windows CMD 与 PowerShell 在处理用户环境变量时的差异：

1. **PATH 环境变量刷新**：uv 安装 codexspec 时，会把 `%USERPROFILE%\.local\bin` 加入用户 PATH。PowerShell 通常能立即识别这一变更，而 CMD 往往要等到终端重启后才会刷新环境变量。

2. **进程创建机制差异**：CMD 走的是 Windows CreateProcess API，而 PowerShell 采用另一套机制，对路径解析问题更具容错性。

### 解决方案

#### 方案 1：改用 PowerShell（推荐）

最简单的办法是用 PowerShell 替代 CMD：

```powershell
# 在 PowerShell 中安装并运行 codexspec
uv tool install codexspec
codexspec --version
```

#### 方案 2：重启 CMD

关闭所有 CMD 窗口后重新打开一个，强制 CMD 重新加载环境变量。

#### 方案 3：在 CMD 中手动刷新 PATH

```cmd
# 将 uv 的 bin 目录加入当前会话的 PATH
set PATH=%PATH%;%USERPROFILE%\.local\bin

# 验证
codexspec --version
```

#### 方案 4：使用完整路径

```cmd
# 通过完整路径执行 codexspec
%USERPROFILE%\.local\bin\codexspec.exe --version
```

#### 方案 5：永久加入系统 PATH

1. 打开 **系统属性** → **环境变量**
2. 在 **用户变量** 或 **系统变量** 中找到 `Path`
3. 添加：`%USERPROFILE%\.local\bin`
4. 点击确定，并重启所有终端

#### 方案 6：改用 pipx 替代 uv tool

如果 uv 始终有问题，可以改用 pipx：

```cmd
# 安装 pipx
pip install pipx
pipx ensurepath

# 重启 CMD 后再安装 codexspec
pipx install codexspec

# 验证
codexspec --version
```

## 验证步骤

要排查问题，可在 CMD 中执行以下命令：

```cmd
# 检查 uv 的 bin 目录是否已加入 PATH
echo %PATH% | findstr ".local\bin"

# 检查 codexspec 可执行文件是否存在
dir %USERPROFILE%\.local\bin\codexspec.*

# 尝试用完整路径运行
%USERPROFILE%\.local\bin\codexspec.exe --version
```

## 常见问题

### 问题："uv is not recognized"

**原因**：uv 未安装，或不在 PATH 中。

**解决方案**：

```powershell
# 用 PowerShell 安装 uv
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# 重启终端后验证
uv --version
```

### 问题："python is not recognized"

**原因**：Python 未安装，或不在 PATH 中。

**解决方案**：

1. 从 [python.org](https://www.python.org/downloads/) 安装 Python 3.11+
2. 安装时勾选 "Add Python to PATH"
3. 重启终端

### 问题：杀毒软件拦截执行

**症状**：codexspec 能短暂运行随后停止，或出现间歇性错误。

**解决方案**：将 codexspec 加入杀毒软件白名单：

- **Windows Defender**：设置 → 更新和安全 → Windows 安全中心 → 病毒和威胁防护 → 管理设置 → 排除项
- 添加路径：`%USERPROFILE%\.local\bin\codexspec.exe`

## 相关资源

- [uv GitHub Issue #16747](https://github.com/astral-sh/uv/issues/16747) — uv 在 Windows 上已知的权限问题
- [uv Windows 安装指南](https://docs.astral.sh/uv/getting-started/installation/)
- [pipx 文档](https://pypa.github.io/pipx/) — 替代性的 Python 应用安装工具

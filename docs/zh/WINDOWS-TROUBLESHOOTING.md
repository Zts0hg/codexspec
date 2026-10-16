# Windows 故障排查

## 检查安装

在 PowerShell 中确认实际使用的可执行文件，并检查 CLI 是否能启动。查询版本的命令是 `codexspec version`。

```powershell
Get-Command codexspec -All
codexspec version
codexspec check
```

## 找不到命令

如果缺少 uv，请按其安装指南安装。如果已通过 uv 安装 CodexSpec，但它不在 `PATH` 中，应查看可执行文件目录并更新 shell 配置，然后打开新终端。如果助手继承了旧环境，也需要重启助手。实际目录可能与默认值不同，请以 uv 返回的路径为准。

```powershell
uv tool list
uv tool dir --bin
uv tool update-shell
```

[uv](https://docs.astral.sh/uv/getting-started/installation/) · [uv tool update-shell](https://docs.astral.sh/uv/reference/cli/#uv-tool-update-shell)

## 拒绝访问或启动失败

仅凭“拒绝访问”无法确定原因。记录准确的命令、可执行文件路径、错误和版本，检查文件是否存在、是否被另一处安装抢先匹配，以及文件权限或安全软件是否阻止执行。受管理的设备应按组织批准的流程寻求管理员支持。对比 PowerShell 和 CMD 仅用于缩小环境差异范围，不应据此认定换一个 shell 就解决了根本问题。

CLI 能正常运行后，再按所需助手集成初始化选定项目。前置条件和项目刷新行为见安装指南。

[CodexSpec](getting-started/installation.md)

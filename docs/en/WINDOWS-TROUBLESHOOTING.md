# Windows Troubleshooting

## Check the installation

Use PowerShell to check which executable is being used and whether the CLI starts. The version command is `codexspec version`.

```powershell
Get-Command codexspec -All
codexspec version
codexspec check
```

## Command not found

If uv is missing, follow its installation guide. If CodexSpec was installed with uv but is not on `PATH`, inspect the executable directory and update the shell configuration, then open a new terminal. Restart the assistant too if it inherited the old environment. The directory may differ from the default; use the path reported by uv.

```powershell
uv tool list
uv tool dir --bin
uv tool update-shell
```

[uv](https://docs.astral.sh/uv/getting-started/installation/) · [uv tool update-shell](https://docs.astral.sh/uv/reference/cli/#uv-tool-update-shell)

## Access denied or launch failure

An access-denied message alone does not identify the cause. Record the exact command, executable path, error, and versions. Check whether the executable exists, whether another installation shadows it, and whether file permissions or security software blocked execution. On a managed device, use the approved administrative support process. Compare PowerShell and CMD only to narrow the environment difference; do not assume that switching shells fixes the underlying cause.

After the CLI works, initialize the selected project with the desired assistant integration. See the installation guide for prerequisites and project refresh behavior.

[CodexSpec](getting-started/installation.md)

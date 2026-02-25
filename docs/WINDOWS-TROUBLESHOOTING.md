# Windows Troubleshooting Guide

This guide helps Windows users resolve common issues when installing and running CodexSpec.

## Problem: "spawn codexspec access denied" (OSError 5) in CMD

### Symptoms

- Running `codexspec --version` or `codexspec init` in CMD fails with "Access denied" or "spawn codexspec access denied (OSError 5)"
- The same commands work correctly in PowerShell

### Root Cause

This is caused by differences in how Windows CMD and PowerShell handle user environment variables:

1. **PATH environment variable refresh**: When uv installs codexspec, it adds `%USERPROFILE%\.local\bin` to the user PATH. PowerShell typically recognizes this immediately, while CMD may not refresh the environment variables until the terminal is restarted.

2. **Process creation differences**: CMD uses Windows CreateProcess API, while PowerShell uses a different mechanism that may be more tolerant of path resolution issues.

### Solutions

#### Solution 1: Use PowerShell (Recommended)

The simplest solution is to use PowerShell instead of CMD:

```powershell
# Install and run codexspec in PowerShell
uv tool install codexspec
codexspec --version
```

#### Solution 2: Restart CMD

Close all CMD windows and open a fresh one. This forces CMD to reload environment variables.

#### Solution 3: Manually Refresh PATH in CMD

```cmd
# Add uv's bin directory to PATH for the current session
set PATH=%PATH%;%USERPROFILE%\.local\bin

# Verify
codexspec --version
```

#### Solution 4: Use Full Path

```cmd
# Execute codexspec using its full path
%USERPROFILE%\.local\bin\codexspec.exe --version
```

#### Solution 5: Add to System PATH Permanently

1. Open **System Properties** → **Environment Variables**
2. Find `Path` in **User variables** or **System variables**
3. Add: `%USERPROFILE%\.local\bin`
4. Click OK and restart all terminals

#### Solution 6: Use pipx Instead of uv tool

If uv continues to have issues, use pipx as an alternative:

```cmd
# Install pipx
pip install pipx
pipx ensurepath

# Restart CMD, then install codexspec
pipx install codexspec

# Verify
codexspec --version
```

## Verification Steps

To diagnose the issue, run these commands in CMD:

```cmd
# Check if uv's bin directory is in PATH
echo %PATH% | findstr ".local\bin"

# Check if codexspec executable exists
dir %USERPROFILE%\.local\bin\codexspec.*

# Try running with full path
%USERPROFILE%\.local\bin\codexspec.exe --version
```

## Common Issues

### Issue: "uv is not recognized"

**Cause**: uv is not installed or not in PATH.

**Solution**:
```powershell
# Install uv using PowerShell
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# Restart terminal and verify
uv --version
```

### Issue: "python is not recognized"

**Cause**: Python is not installed or not in PATH.

**Solution**:
1. Install Python 3.11+ from [python.org](https://www.python.org/downloads/)
2. During installation, check "Add Python to PATH"
3. Restart terminal

### Issue: Antivirus Blocking Execution

**Symptoms**: Codexspec works briefly then stops, or shows intermittent errors.

**Solution**: Add codexspec to your antivirus whitelist:
- **Windows Defender**: Settings → Update & Security → Windows Security → Virus & threat protection → Manage settings → Exclusions
- Add path: `%USERPROFILE%\.local\bin\codexspec.exe`

## Related Resources

- [uv GitHub Issue #16747](https://github.com/astral-sh/uv/issues/16747) - Known Windows permission issues with uv
- [uv Windows Installation Guide](https://docs.astral.sh/uv/getting-started/installation/)
- [pipx Documentation](https://pypa.github.io/pipx/) - Alternative Python application installer

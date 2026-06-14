# 手动 Smoke Test 检查清单

## 前置条件

- [ ] tmux 已安装
- [ ] claude CLI 已安装（`claude --version`）
- [ ] Python 3.11+

## 基础功能

### 启动与退出

- [ ] `python scripts/python/claude_auto_responder.py --version` 输出版本号
- [ ] `python scripts/python/claude_auto_responder.py --jsonl /nonexistent --tmux-pane fake:0.1` 退出码 2
- [ ] 正常启动后 Ctrl+C 优雅退出

### AskUserQuestion 自动选择

- [ ] 在 tmux 中启动 Claude Code，触发 AskUserQuestion
- [ ] 启动 auto-responder 指向对应 jsonl 和 tmux pane
- [ ] 观察日志：检测到 AskUserQuestion → 调用 claude -p → 发送选项
- [ ] Claude Code 收到选择并继续执行

### 权限请求自动允许

- [ ] Claude Code 请求执行安全 Bash 命令（如 `ls`、`cat`、`git status`）
- [ ] auto-responder 自动发送 Y
- [ ] Claude Code 继续执行

### 权限请求自动拒绝

- [ ] Claude Code 请求执行危险命令（如 `rm`）
- [ ] auto-responder 自动发送 n
- [ ] 日志显示 🚫 拒绝原因

### 项目外文件编辑拒绝

- [ ] Claude Code 请求编辑项目外文件（如 `/etc/hosts`）
- [ ] auto-responder 自动发送 n

### Dry-run 模式

- [ ] 加 `--dry-run` 启动
- [ ] 日志显示决策结果但不实际发送到 tmux

## 安全策略配置

- [ ] 创建 policy.json，添加 `allow_commands: ["docker build"]`
- [ ] 验证 `docker build` 被允许
- [ ] 添加 `deny_commands: ["curl -X POST"]`
- [ ] 验证 deny 优先于 allow

## 边界情况

- [ ] jsonl 文件被删除后恢复 → 主循环继续
- [ ] tmux pane 关闭 → 错误日志但不崩溃
- [ ] 同一请求不重复响应

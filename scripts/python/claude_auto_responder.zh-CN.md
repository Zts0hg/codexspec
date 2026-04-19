# Claude Auto Responder

自动响应运行在 tmux 中的 Claude Code 的所有等待状态，让 Claude Code 在无人值守时不被阻塞、长时间流畅运行。

## 它解决了什么问题

Claude Code 在长时间运行任务时，经常因为以下原因暂停并等待用户输入：

- **AskUserQuestion**：Claude Code 需要你在多个选项中做出选择（比如"使用哪种认证方式？"）
- **工具权限确认**：Claude Code 需要你确认是否允许执行 Bash 命令、编辑文件等操作

每次暂停都需要人工介入，如果你不在电脑前，任务就会一直卡住。

**claude-auto-responder** 就是你的自动值守助手：

- 对于选择题（AskUserQuestion）→ 调用 `claude -p` 结合项目上下文智能选择
- 对于权限确认 → 内置安全策略引擎**本地判定**（不调用 LLM，< 1ms）

## 前提条件

- Python 3.11+
- tmux（已安装并正在运行）
- claude CLI（`claude --version` 可用，用于 AskUserQuestion 决策）
- 无第三方 Python 依赖，仅使用标准库

## 快速开始

### 第一步：在 tmux 中启动 Claude Code

```bash
# 创建一个 tmux session 用于 Claude Code
tmux new-session -s claude-main

# 在 tmux 里启动 Claude Code
claude
```

### 第二步：找到 jsonl 文件路径和 tmux pane

```bash
# 新开一个终端窗口

# 查看 jsonl 文件（找到最新的那个）
ls -lt ~/.claude/projects/*/*.jsonl | head -5
# 输出类似：
# -rw-r--r--  1 xiaoming  staff  12345  Apr 16 10:00  /Users/xiaoming/.claude/projects/-Users-xiaoming-code-myproject/abc123-def456.jsonl

# 查看 tmux pane 信息
tmux list-panes -a -F "#{session_name}:#{window_index}.#{pane_index}"
# 输出类似：
# claude-main:0.0
```

### 第三步：启动 auto-responder

```bash
python scripts/python/claude_auto_responder.py \
    --jsonl ~/.claude/projects/-Users-xiaoming-code-myproject/abc123-def456.jsonl \
    --tmux-pane claude-main:0.0
```

启动后你会看到：

```
[2026-04-16 10:00:01] 🚀 claude-auto-responder v0.2.0-dev 启动
    └─ jsonl: /Users/xiaoming/.claude/projects/... | pane: claude-main:0.0 | interval: 2.0s | safety: 内置策略
```

现在可以放心离开了。脚本会自动处理 Claude Code 的所有等待状态。按 `Ctrl+C` 停止。

## 命令行参数

| 参数 | 必需 | 默认值 | 说明 |
|------|:----:|--------|------|
| `--jsonl PATH` | ✅ | — | Claude Code 的 jsonl 会话文件路径 |
| `--tmux-pane TARGET` | ✅ | — | 目标 tmux pane，格式 `session:window.pane` |
| `--system-prompt-file PATH` | | 无 | 系统提示词文件（仅影响 AskUserQuestion 决策） |
| `--safety-policy-file PATH` | | 无 | 安全策略覆盖配置（JSON 格式） |
| `--poll-interval SECONDS` | | `2.0` | 轮询间隔秒数 |
| `--stable-ms MILLIS` | | `1500` | jsonl 文件 mtime 静止阈值（毫秒） |
| `--project-root PATH` | | CWD | 项目根目录，影响路径安全判定边界 |
| `--claude-bin PATH` | | `claude` | claude CLI 可执行文件路径 |
| `--log-file PATH` | | 无 | 日志文件路径（默认仅输出到 stderr） |
| `--dry-run` | | `false` | 仅做决策，不实际发送到 tmux |
| `--decide-timeout SECONDS` | | `180` | `claude -p` 调用超时秒数 |
| `--health-check` | | `false` | 运行健康检查并输出 JSON 报告到 stdout |
| `--version` | | — | 打印版本并退出 |

## 安全策略引擎

脚本内置了一套安全策略引擎来处理工具权限请求。核心原则：**默认拒绝，白名单放行**。

### 默认规则总览

| 工具 | 条件 | 判定 |
|------|------|------|
| `Read` / `Grep` / `Glob` | 任何情况 | ✅ ALLOW |
| `Edit` / `Write` / `NotebookEdit` | 文件在项目目录内 | ✅ ALLOW |
| `Edit` / `Write` / `NotebookEdit` | 文件在项目目录外 | 🚫 DENY |
| `Bash` | 命令在安全白名单中 | ✅ ALLOW |
| `Bash` | 命令在危险黑名单中 | 🚫 DENY |
| `Bash` | 命令不在白名单也不在黑名单 | 🚫 DENY |
| 其他未知工具 | — | 🚫 DENY |

### Bash 命令安全白名单

以下命令（或命令前缀）被视为安全，自动允许执行：

**只读/查看类**

```
cat  head  tail  less  more  wc  file  stat  du  df
ls  tree  pwd  echo  printf  date  uname  hostname
grep  rg  find  fd  locate  which  whereis  type
ps  top  htop  lsof
env  printenv
curl  wget  ping  dig  nslookup
```

**Git 只读操作**

```
git status    git log     git diff    git branch
git show      git remote  git tag
```

**开发/构建/测试**

```
python -c       node -e         make
uv run pytest   uv run ruff
npm test        npm run
cargo test      cargo build     cargo check
go build        go test
pip list        pip show        npm list        npm info
```

### Bash 命令危险黑名单

以下模式会被立即拒绝：

**删除类**

```
rm  rmdir  unlink  shred
```

**危险 Git 操作**

```
git clean             git reset --hard
git push --force      git push -f
git checkout -- .     git restore .
```

**系统/权限修改**

```
chmod  chown  chgrp  mkfs  fdisk  dd
```

**包管理修改**

```
pip install    pip uninstall
npm install    npm uninstall
```

**危险 Shell**

```
eval  exec
```

### 复合命令处理

- `&&` / `||` / `;` 连接的复合命令：**逐段检查**，任一段命中黑名单则整体拒绝
- `|` 管道命令：检查所有段，任一段危险则拒绝
- `>` 重定向到项目外绝对路径：拒绝

示例：

```
ls -la && rm file.txt     → 🚫 DENY（rm 在黑名单）
cat file | head -5        → ✅ ALLOW（全部只读）
echo "x" > /etc/hosts    → 🚫 DENY（重定向到项目外）
```

### 路径安全判定

对 `Edit` / `Write` / `NotebookEdit` 工具，脚本会检查目标文件路径是否在 `--project-root` 内：

1. 使用 `os.path.realpath()` 解析符号链接和相对路径
2. 比较解析后的路径是否以项目根目录开头
3. 符号链接指向项目外 → 拒绝（防止绕过）
4. 路径不存在时：逐级向上查找最近的存在的父目录来判定

## 自定义安全策略

通过 `--safety-policy-file` 指定一个 JSON 文件来覆盖默认规则。

### 配置文件格式

```json
{
  "allow_commands": ["docker build", "docker run"],
  "deny_commands": ["curl -X POST"],
  "allow_paths_outside_project": ["/tmp/build-*"],
  "deny_tools": ["Agent"],
  "allow_unknown_tools": false
}
```

所有字段均为可选。

| 字段 | 类型 | 说明 |
|------|------|------|
| `allow_commands` | `string[]` | 额外允许的 Bash 命令前缀 |
| `deny_commands` | `string[]` | 额外拒绝的 Bash 命令前缀 |
| `allow_paths_outside_project` | `string[]` | 允许的项目外路径 glob 模式 |
| `deny_tools` | `string[]` | 额外需要拒绝的工具名 |
| `allow_unknown_tools` | `bool` | 是否允许未知工具（默认 `false`） |

### 优先级

```
deny_commands > allow_commands > 默认黑名单 > 默认白名单
```

`deny_commands` 的优先级最高——即使一个命令同时匹配 `allow_commands` 和 `deny_commands`，也会被拒绝。

### 示例：允许 Docker 但禁止发布

```json
{
  "allow_commands": ["docker build", "docker run", "docker compose"],
  "deny_commands": ["docker push"]
}
```

### 示例：允许写入 /tmp 下的构建产物

```json
{
  "allow_paths_outside_project": ["/tmp/build-*", "/tmp/test-output-*"]
}
```

## 系统提示词（AskUserQuestion 定制）

通过 `--system-prompt-file` 可以自定义决策者 Claude 在回答 AskUserQuestion 时的偏好。

这对于有特定项目风格偏好的场景很有用。

### 示例提示词文件 (`my-prompt.txt`)

```text
你正在为一个 Python 后端项目做决策。请遵循以下偏好：
- 优先选择类型安全的方案
- 倾向于使用标准库而非第三方库
- 测试框架首选 pytest
- 如果有 "推荐" 标记的选项，优先选择它
```

```bash
python scripts/python/claude_auto_responder.py \
    --jsonl ~/.claude/projects/-xxx/session.jsonl \
    --tmux-pane claude-main:0.0 \
    --system-prompt-file ./my-prompt.txt
```

### AskUserQuestion 决策流程

1. 读取项目根目录下的 `CLAUDE.md`（截断到 30KB）
2. 读取 `.codexspec/memory/constitution.md`（截断到 30KB）
3. 读取系统提示词文件（如果指定）
4. 将以上内容与问题详情组装为 prompt
5. 调用 `claude -p <prompt>` 获取 JSON 格式的答案
6. 校验答案的 label 是否存在于选项中
7. 通过 tmux 发送选中的 label

如果 `claude -p` 超时、返回错误、或答案校验失败，该问题会被跳过（标记为已处理，不会无限重试）。

## 健康检查

使用 `--health-check` 标志可以快速验证所有依赖项是否配置正确，无需启动主循环。

### 用法

```bash
python scripts/python/claude_auto_responder.py \
    --jsonl ~/.claude/projects/-xxx/session.jsonl \
    --tmux-pane claude-main:0.0 \
    [--safety-policy-file ./policy.json] \
    --health-check
```

### 输出格式

健康检查输出 JSON 格式报告到 stdout：

```json
{
  "overall": "healthy",
  "checks": [
    {"name": "jsonl_file", "status": "pass", "message": "/path/to/session.jsonl"},
    {"name": "tmux_pane", "status": "pass", "message": "claude-main:0.0"},
    {"name": "claude_cli", "status": "pass", "message": "claude 可用"},
    {"name": "safety_policy_file", "status": "pass", "message": "./policy.json"}
  ]
}
```

### 检查项

| 检查项 | 说明 |
|--------|------|
| `jsonl_file` | jsonl 文件存在且可读 |
| `tmux_pane` | 指定的 tmux pane 存在 |
| `claude_cli` | claude CLI 可用并能执行 `--version` |
| `safety_policy_file` | 安全策略文件存在且格式有效（如果提供） |

### 退出码

- `0` — 所有检查通过（`overall: "healthy"`）
- `1` — 至少一项检查失败（`overall: "unhealthy"`）

### 示例：在监控脚本中使用

```bash
# 检查 auto-responder 配置是否健康
if python scripts/python/claude_auto_responder.py \
    --jsonl ~/.claude/projects/-xxx/session.jsonl \
    --tmux-pane claude-main:0.0 \
    --health-check; then
    echo "✅ 健康检查通过"
else
    echo "❌ 健康检查失败"
    exit 1
fi
```

## 日志说明

日志输出到 stderr，格式为 `[时间戳] emoji 消息`。

| Emoji | 含义 |
|-------|------|
| 🚀 | 启动/停止 |
| 👀 | 检测到待响应请求 |
| 🤔 | 正在调用 claude -p 决策 |
| 🔒 | 安全策略判定中 |
| ✅ | 允许/发送成功 |
| 🚫 | 安全策略拒绝 |
| 📤 | 已发送到 tmux |
| ⚠️ | 警告 |
| ❌ | 错误 |

### 日志示例

**AskUserQuestion 自动选择**：

```
[2026-04-16 10:00:05] 👀 检测到待响应请求 toolu_01ABC (AskUserQuestion)
[2026-04-16 10:00:05] 🤔 调用决策者 (claude -p)
[2026-04-16 10:00:09] ✅ 决策完成 answers=['JWT token (Recommended)']
[2026-04-16 10:00:09] 📤 已发送到 tmux pane claude-main:0.0
```

**Bash 权限自动允许**：

```
[2026-04-16 10:00:12] 👀 检测到待响应请求 toolu_01DEF (Bash)
[2026-04-16 10:00:12] 🔒 安全策略判定 toolu_01DEF
[2026-04-16 10:00:12] ✅ ALLOW (白名单命令: cat)
[2026-04-16 10:00:12] 📤 已发送 Y 到 tmux pane claude-main:0.0
```

**Bash 权限自动拒绝**：

```
[2026-04-16 10:00:15] 👀 检测到待响应请求 toolu_01GHI (Bash)
[2026-04-16 10:00:15] 🔒 安全策略判定 toolu_01GHI
[2026-04-16 10:00:15] 🚫 DENY (黑名单: rm)
[2026-04-16 10:00:15] 📤 已发送 n 到 tmux pane claude-main:0.0
```

可通过 `--log-file` 同时写入文件：

```bash
python scripts/python/claude_auto_responder.py \
    --jsonl ... --tmux-pane ... \
    --log-file /tmp/auto-responder.log
```

## 使用场景

### 场景 1：夜间跑大型重构任务

```bash
# 终端 1：在 tmux 中启动 Claude Code
tmux new-session -s refactor
claude

# 终端 2：启动 auto-responder 值守
python scripts/python/claude_auto_responder.py \
    --jsonl ~/.claude/projects/-Users-xiaoming-code-myproject/session.jsonl \
    --tmux-pane refactor:0.0 \
    --log-file ~/refactor-log.txt

# 现在可以放心去睡觉了
```

### 场景 2：Dry-run 先观察再启用

```bash
# 先用 dry-run 看看脚本会做什么决策
python scripts/python/claude_auto_responder.py \
    --jsonl ~/.claude/projects/-xxx/session.jsonl \
    --tmux-pane claude-main:0.0 \
    --dry-run

# 确认决策合理后，去掉 --dry-run 正式启用
```

### 场景 3：指定项目根目录

如果你从其他目录运行脚本，需要显式指定项目根目录来确保路径安全判定正确：

```bash
python scripts/python/claude_auto_responder.py \
    --jsonl ~/.claude/projects/-xxx/session.jsonl \
    --tmux-pane claude-main:0.0 \
    --project-root /Users/xiaoming/code/myproject
```

### 场景 4：多会话并行

每个 Claude Code 会话启动一个 auto-responder 实例：

```bash
# 会话 A
python scripts/python/claude_auto_responder.py \
    --jsonl ~/.claude/projects/-projectA/session-a.jsonl \
    --tmux-pane sessionA:0.0 &

# 会话 B
python scripts/python/claude_auto_responder.py \
    --jsonl ~/.claude/projects/-projectB/session-b.jsonl \
    --tmux-pane sessionB:0.0 &
```

## 退出码

| 码 | 含义 |
|----|------|
| `0` | 正常退出（Ctrl+C）或健康检查全部通过 |
| `1` | 健康检查有失败项 |
| `2` | 启动参数错误（文件不存在、JSON 格式错误等） |
| `130` | SIGINT |

## 工作原理

```
┌──────────────────────────────────────────────────────────────┐
│                  claude_auto_responder.py                     │
│                                                              │
│  MainLoop (每 2s 轮询)                                       │
│    │                                                         │
│    ├─► Detector ──► 读取 jsonl ──► 找到未回答的 tool_use     │
│    │                                                         │
│    ├─► Router 根据 tool name 分流：                          │
│    │     │                                                   │
│    │     ├─ AskUserQuestion ──► PromptBuilder ──► claude -p  │
│    │     │                                                   │
│    │     └─ 其他工具 ──► SafetyPolicyEngine（本地规则）       │
│    │                       ├─ PathChecker（路径判定）         │
│    │                       └─ BashClassifier（命令分类）      │
│    │                                                         │
│    └─► TmuxSender ──► tmux send-keys（发送答案/Y/n）         │
└──────────────────────────────────────────────────────────────┘
```

### 检测算法

1. 读取 jsonl 文件，提取所有 assistant 消息中的 `tool_use` 和 user 消息中的 `tool_result`
2. 找到最后一个没有对应 `tool_result` 的 `tool_use` → 这就是 Claude Code 正在等待的请求
3. mtime 稳定性检查：jsonl 文件最后修改时间距今超过 `--stable-ms`（默认 1.5s）才读取，避免读到写入中间态
4. 去重：已处理的 `tool_use_id` 记录在内存中，同一请求不会响应两次

## 常见问题

### 如何找到正确的 jsonl 文件？

```bash
# 列出所有会话文件，按修改时间排序
ls -lt ~/.claude/projects/*/*.jsonl | head -10
```

jsonl 路径格式为 `~/.claude/projects/<project-slug>/<session-id>.jsonl`，其中 `<project-slug>` 是项目路径的转义形式（`/` 替换为 `-`）。

### 如何找到正确的 tmux pane？

```bash
# 列出所有 pane
tmux list-panes -a -F "#{session_name}:#{window_index}.#{pane_index} - #{pane_current_command}"
```

格式为 `session:window.pane`，比如 `claude-main:0.0`。

### 脚本会不会误操作导致危险？

脚本的安全设计是**默认拒绝**：

- 不在白名单的 Bash 命令 → 拒绝
- 项目目录外的文件编辑 → 拒绝
- 未知工具 → 拒绝
- 所有删除操作 → 拒绝

最坏的情况是"误拒绝"——Claude Code 会被告知"n"然后它会尝试其他方式，或者等待你手动介入。误拒绝不会造成任何损害。

### jsonl 文件被删除了怎么办？

脚本会记录一条警告日志，然后继续轮询。当文件恢复后自动继续工作。

### tmux pane 关闭了怎么办？

发送会失败，脚本记录错误日志但主循环不会崩溃。

### 可以同时用 --system-prompt-file 和 --safety-policy-file 吗？

可以。它们作用于不同的场景：

- `--system-prompt-file` 只影响 AskUserQuestion 的 claude -p 决策
- `--safety-policy-file` 只影响工具权限请求的本地策略判定

### 为什么 AskUserQuestion 决策有时会失败？

可能原因：

- `claude -p` 调用超时（默认 180s，可通过 `--decide-timeout` 调整）
- Claude 返回的答案 label 与选项不完全匹配
- Claude 返回的 JSON 格式无法解析

失败时该问题会被标记为已处理并跳过，不会无限重试。

# 功能规格：claude-auto-responder（v2 — 全状态响应 + 安全策略）

## 概述

编写一个 Python 守护脚本 `scripts/python/claude_auto_responder.py`，持续监听运行在 tmux 中的长期 Claude Code 会话。当 Claude Code 进入**任何等待用户响应的状态**时——包括 AskUserQuestion 选择问题、Bash/Edit/Write/Read 等工具的权限确认请求——脚本会自动判断操作是否安全，并将决策（允许/拒绝/选择）通过 `tmux send-keys` 发送回等待中的 Claude Code。

对于 AskUserQuestion 类型的问题，调用 `claude -p` 一次性模式综合项目上下文做出智能选择。对于工具权限请求，使用**内置安全策略引擎**本地判定是否允许，无需调用外部 LLM——判定速度极快（< 1ms）。

这解决了"长时间运行的 Claude Code 任务中频繁需要用户确认"的痛点——让脚本按照安全策略和项目宪法代替人类值守，确保 Claude Code 不被阻塞、流畅地长时间运行。

## 目标

- 以守护进程方式可靠地检测 tmux 中某个 Claude Code 会话的**所有等待用户响应**状态
- 对 AskUserQuestion 通过 `claude -p` 基于项目上下文自动做出选择
- 对工具权限请求通过内置安全策略引擎本地判定允许/拒绝
- 通过 tmux 交互把决策结果写回原 Claude Code 会话
- 严格避免对同一请求重复响应
- **安全优先**：默认拒绝不安全操作（删除、项目外文件编辑等）
- 可通过系统提示词文件和安全策略配置文件精细调整行为

## 用户故事

### Story 1：守护一个长跑任务（全状态）

**As a** 正在让 Claude Code 跑长任务的开发者
**I want** 一个脚本能在我离开时代替我处理所有等待响应（问题选择 + 权限确认）
**So that** 任务不会因为等待任何类型的用户输入而长时间阻塞

**验收标准：**

- [ ] 脚本启动后能持续运行直到 Ctrl+C
- [ ] 当 Claude Code 发起 AskUserQuestion 并等待时，脚本能自动做出选择
- [ ] 当 Claude Code 请求 Bash/Edit/Write 等工具权限时，脚本能自动允许或拒绝
- [ ] 做出的决策确实被 Claude Code 接收并继续执行
- [ ] 同一个请求只响应一次

### Story 2：内置安全策略保护

**As a** 开发者
**I want** 脚本内置安全策略，只允许安全操作，拒绝危险操作
**So that** 自动值守不会意外删除文件或修改项目外的内容

**验收标准：**

- [ ] 读取类操作（Read/Grep/Glob/cat/ls 等）默认允许
- [ ] 项目目录内的文件编辑/写入默认允许
- [ ] 项目目录外的文件编辑/写入默认拒绝
- [ ] 任何包含删除语义的操作（rm/rmdir/unlink/git clean 等）默认拒绝
- [ ] 安全策略可通过配置文件覆盖默认行为

### Story 3：通过系统提示词定制 AskUserQuestion 决策

**As a** 开发者
**I want** 提供一个系统提示词文件告诉"决策者 Claude"我的偏好
**So that** AskUserQuestion 的自动选择符合我的项目风格

**验收标准：**

- [ ] `--system-prompt-file` 参数可选，默认不启用
- [ ] 指定文件后，其内容会被拼接到 claude -p 的 prompt 中
- [ ] 系统提示词文件不存在时应报错退出

### Story 4：项目上下文感知决策

**As a** 开发者
**I want** 决策者 Claude 能读取项目的 CLAUDE.md 和 constitution.md
**So that** AskUserQuestion 的决策符合项目规则

**验收标准：**

- [ ] 脚本自动读取项目根目录下的 `CLAUDE.md` 和 `.codexspec/memory/constitution.md`
- [ ] 两个文件任一缺失时使用空字符串并记录警告，不中断运行
- [ ] 最终 prompt 清晰包含这些上下文

## 功能需求

### REQ-001：CLI 参数

| 参数 | 必需 | 默认值 | 说明 |
|------|------|--------|------|
| `--jsonl PATH` | ✅ | — | 要监听的 jsonl 文件路径 |
| `--tmux-pane TARGET` | ✅ | — | 目标 tmux pane，格式 `session:window.pane` |
| `--system-prompt-file PATH` | ❌ | 空 | 可选系统提示词文件（仅用于 AskUserQuestion 决策） |
| `--safety-policy-file PATH` | ❌ | 空 | 可选安全策略覆盖配置（JSON 格式，见 REQ-010） |
| `--poll-interval SECONDS` | ❌ | `2.0` | 轮询间隔（秒） |
| `--stable-ms MILLIS` | ❌ | `1500` | jsonl mtime 静止阈值（毫秒） |
| `--project-root PATH` | ❌ | CWD | 项目根目录，用于定位上下文文件和安全策略的路径边界 |
| `--claude-bin PATH` | ❌ | `claude` | claude CLI 可执行文件 |
| `--log-file PATH` | ❌ | 无 | 可选日志文件路径，默认仅 stderr |
| `--dry-run` | ❌ | `false` | 仅决策不发送到 tmux |
| `--decide-timeout SECONDS` | ❌ | `180` | claude -p 超时秒数 |
| `--version` | ❌ | — | 打印版本并退出 |

### REQ-002：jsonl 文件与 tmux pane 存在性校验

启动时必须：

- 校验 `--jsonl` 文件存在且可读；若不存在则退出码 `2` 并打印错误
- 校验 `--tmux-pane` 对应 pane 存在；若不存在则退出码 `2`
- 若指定 `--system-prompt-file`，校验文件存在；不存在则退出码 `2`
- 若指定 `--safety-policy-file`，校验文件存在且 JSON 合法；不合法则退出码 `2`
- 运行期间若 jsonl 文件被删除/tmux pane 消失，记录错误但不崩溃，继续轮询

### REQ-003：等待状态检测算法（通用）

每轮轮询时：

1. 若 jsonl 文件不存在则记录警告，跳过本轮
2. 检查 jsonl 的 `mtime`，若距离当前时间 < `stable-ms` 则跳过（避免读取中间态）
3. 从头读取 jsonl 的所有行
4. 构建映射：
   - `pending_tool_uses`：有序列表，存**所有** assistant 消息中的 tool_use 条目（id、name、input）
   - `answered_ids`：所有 user 消息中的 `tool_result.tool_use_id` 集合
5. 定位 `pending_tool_uses` 中**最后一条** tool_use_id 不在 `answered_ids` 中的条目 → 该 tool_use 处于"等待响应"状态
6. 若该 tool_use_id 已在脚本的 `processed_ids` 内存集合中 → 跳过
7. 根据 tool_use 的 `name` 分流处理：
   - `name == 'AskUserQuestion'` → 进入 AskUserQuestion 决策流程（REQ-004）
   - 其他（Bash/Edit/Write/Read/Grep/Glob/Agent 等）→ 进入安全策略判定流程（REQ-010）

解析规则：

- assistant 消息：`record.type == 'assistant'`，`message.content` 列表中 `type=='tool_use'` 的所有条目
- user 消息：`record.type == 'user'`，`message.content` 列表中 `type=='tool_result'` 的条目
- user 消息 content 是字符串时视为无 tool_result
- 坏行（JSON 解析失败）跳过并记录警告

### REQ-004：AskUserQuestion 决策 prompt 组装

组装格式（仅用于 AskUserQuestion 类型）：

```
<system_prompt>
{系统提示词文件内容，若未提供则省略整个段落}
</system_prompt>

<project_claude_md>
{CLAUDE.md 内容，截断到最多 30KB}
</project_claude_md>

<project_constitution>
{.codexspec/memory/constitution.md 内容，截断到最多 30KB}
</project_constitution>

<task>
你正在代替人类用户回答另一个 Claude Code 实例发起的 AskUserQuestion 问题。
基于上面的项目上下文和系统提示词，为下列问题选出最符合项目规则和开发者偏好的答案。

问题详情（JSON）：
{问题对象 JSON，包含 question/header/options/multiSelect}

严格按如下 JSON 格式输出（不要任何额外文字、markdown 代码块或解释）：
{"answers": ["<选项的完整 label 字符串>", ...]}

- 单选题：answers 数组长度必须为 1
- 多选题：answers 数组长度可以为 1 到选项数量之间
- 每个元素必须完全等于某个选项的 label 字段（大小写、标点完全一致）
- 禁止输出 "Other" 或不在 options 中的内容
</task>
```

### REQ-005：调用 claude -p（仅 AskUserQuestion）

- 通过 `subprocess.run([claude_bin, '-p', prompt], capture_output=True, text=True, timeout=decide_timeout)`
- 超时后记录错误并跳过
- 非零退出码视为失败，记录 stderr 并跳过
- JSON 解析三级回退：直接 parse → 去 markdown fence → 大括号配对扫描
- 仍失败则记录警告并跳过，标记 processed_ids

### REQ-006：AskUserQuestion 答案校验

- 单选且 `len(answers) != 1` → 失败
- 任一 answer 不在 options 的 label 集合里 → 失败
- 失败时标记 processed 并跳过

### REQ-007：发送响应到 tmux

参考 `scripts/python/claude_ctl.py` 的 `TmuxClient`：

**AskUserQuestion 响应**：

1. 对 `answers` 中每个 label：`tmux send-keys -t <pane> -l <label>` + `tmux send-keys -t <pane> Enter`

**权限请求响应**：

1. 允许：`tmux send-keys -t <pane> -l 'Y'` + `tmux send-keys -t <pane> Enter`
2. 拒绝：`tmux send-keys -t <pane> -l 'n'` + `tmux send-keys -t <pane> Enter`

通用规则：

- 每步失败均记录错误；任一步失败中断并标记失败
- 成功后把 tool_use_id 加入 `processed_ids`
- `--dry-run` 模式下跳过实际发送，仅日志输出

### REQ-008：日志

- 带时间戳 `[YYYY-MM-DD HH:MM:SS]` 和 emoji 前缀
- 事件类型：
  - `🚀 启动`
  - `👀 检测到待响应请求`
  - `🤔 调用决策者 (claude -p)`（仅 AskUserQuestion）
  - `🔒 安全策略判定`（权限请求）
  - `✅ 允许/发送成功`
  - `🚫 拒绝（安全策略）`
  - `⚠️ 警告`
  - `❌ 错误`
- 默认输出到 stderr；可选写文件

### REQ-009：健壮主循环

- `try/except Exception` 包裹每轮迭代
- `KeyboardInterrupt` 优雅退出
- `processed_ids` 仅内存

### REQ-010：内置安全策略引擎

安全策略引擎是纯本地判定，不调用 LLM，用于评估工具权限请求是否安全。

#### 默认安全规则

**允许（ALLOW）的操作**：

- `Read`：任何文件读取
- `Grep`：任何搜索
- `Glob`：任何文件匹配
- `Bash`：命令被判定为**只读类**（见下方规则）
- `Edit`：目标文件在 `--project-root` 目录内
- `Write`：目标文件在 `--project-root` 目录内
- `NotebookEdit`：目标文件在 `--project-root` 目录内

**拒绝（DENY）的操作**：

- `Edit`/`Write`/`NotebookEdit`：目标文件在 `--project-root` 目录外
- `Bash`：命令被判定为**危险类**（见下方规则）
- 任何未知的 tool name：默认拒绝

#### Bash 命令安全分类

通过解析 `input.command` 字符串进行分类：

**只读/安全命令白名单**（前缀匹配或正则）：

- 读取类：`cat`, `head`, `tail`, `less`, `more`, `wc`, `file`, `stat`, `du`, `df`
- 搜索类：`grep`, `rg`, `find`, `fd`, `locate`, `which`, `whereis`, `type`
- 列表类：`ls`, `tree`, `pwd`, `echo`, `printf`, `date`, `uname`, `hostname`
- 开发工具（只读）：`git status`, `git log`, `git diff`, `git branch`, `git show`, `git remote`, `git tag`
- 包管理（查询）：`pip list`, `pip show`, `npm list`, `npm info`, `uv pip list`, `cargo --version`
- 构建/测试：`python -c`, `node -e`, `uv run pytest`, `uv run ruff`, `npm test`, `npm run`, `cargo test`, `cargo build`, `cargo check`, `make`, `go build`, `go test`
- 目录操作：`cd`, `pushd`, `popd`
- 环境类：`env`, `printenv`, `export`（无赋值时）
- 网络（只读）：`curl`, `wget`（仅获取数据），`ping`, `dig`, `nslookup`
- 进程查看：`ps`, `top`, `htop`, `lsof`

**危险命令黑名单**（任何位置匹配）：

- 删除类：`rm`, `rm\t`, `rmdir`, `unlink`, `shred`
- 危险 git：`git clean`, `git reset --hard`, `git push --force`, `git push -f`, `git checkout -- .`, `git restore .`
- 系统修改：`chmod`, `chown`, `chgrp`, `mkfs`, `fdisk`, `dd`
- 包修改：`pip install`, `pip uninstall`, `npm install`, `npm uninstall`（除非在 project-root 内执行且 package.json 存在）
- 危险 shell：`eval`, `exec`, `source`（来自外部文件）
- 管道到文件覆盖：`> /`（重定向到绝对路径，非项目内）

**灰色地带处理**：

- 命令中包含 `&&` 或 `||` 或 `;` 的复合命令：逐段检查，任一段命中黑名单则拒绝
- 管道命令（`|`）：只检查最后一个命令是否有写入操作
- 无法判定的命令（不在白名单也不在黑名单）：默认拒绝并记录 `⚠️ 未知命令模式，默认拒绝`

#### 路径安全判定

对于 Edit/Write/NotebookEdit 工具：

1. 从 `input.file_path` 提取路径
2. 使用 `os.path.realpath()` 解析符号链接和相对路径
3. 检查解析后的路径是否以 `os.path.realpath(project_root)` 开头
4. 是 → ALLOW；否 → DENY

#### 安全策略配置文件（可选覆盖）

通过 `--safety-policy-file` 指定 JSON 配置文件，可覆盖默认规则：

```json
{
  "allow_commands": ["docker build", "docker run"],
  "deny_commands": ["curl -X POST"],
  "allow_paths_outside_project": ["/tmp/build-*"],
  "deny_tools": ["Agent"],
  "allow_unknown_tools": false
}
```

| 字段 | 类型 | 说明 |
|------|------|------|
| `allow_commands` | `string[]` | 额外允许的 Bash 命令前缀 |
| `deny_commands` | `string[]` | 额外拒绝的 Bash 命令前缀（优先级高于 allow） |
| `allow_paths_outside_project` | `string[]` | 允许的项目外路径 glob 模式 |
| `deny_tools` | `string[]` | 额外需要拒绝的工具名 |
| `allow_unknown_tools` | `bool` | 未知工具是否允许（默认 false） |

优先级：`deny_commands` > `allow_commands` > 默认白名单 > 默认黑名单

### REQ-011：安全策略判定日志

每次安全策略判定必须输出详细日志：

```
[2026-04-16 10:00:05] 🔒 安全策略判定 toolu_01XYZ
    └─ tool: Bash | cmd: "ls -la src/" | 判定: ALLOW (只读白名单)
```

```
[2026-04-16 10:00:08] 🚫 安全策略拒绝 toolu_01ABC
    └─ tool: Bash | cmd: "rm -rf /tmp/old" | 判定: DENY (删除命令黑名单)
```

```
[2026-04-16 10:00:12] 🔒 安全策略判定 toolu_01DEF
    └─ tool: Edit | file: /Users/xiaoming/code/myproject/src/main.py | 判定: ALLOW (项目内路径)
```

```
[2026-04-16 10:00:15] 🚫 安全策略拒绝 toolu_01GHI
    └─ tool: Write | file: /etc/hosts | 判定: DENY (项目外路径)
```

## 非功能需求

- **NFR-001（响应时间）**：权限请求判定延迟 < `poll_interval + stable_ms + 100ms`（本地判定，无 LLM 调用）；AskUserQuestion 延迟 ≤ `poll_interval + stable_ms + claude_-p_耗时 + 2s`
- **NFR-002（资源占用）**：空闲轮询时 CPU 占用可忽略
- **NFR-003（Python 版本）**：Python 3.11+
- **NFR-004（零第三方依赖）**：仅标准库
- **NFR-005（可测试性）**：安全策略引擎为纯函数，接收 (tool_name, input_dict, project_root, policy_overrides) 返回 (ALLOW|DENY, reason)
- **NFR-006（平台）**：macOS / Linux

## 验收测试用例

| 编号 | 场景 | 预期 |
|------|------|------|
| TC-001 | 未回答的 AskUserQuestion 单选题 | 调用 claude -p，发送选项 label |
| TC-002 | 已回答的 AskUserQuestion | 不触发 |
| TC-003 | 两条 AskUserQuestion，前已答后未答 | 仅对后者发送 |
| TC-004 | multiSelect AskUserQuestion | 依次发送多个 label |
| TC-005 | claude -p 返回无效 label | 标记 processed，不发送 |
| TC-006 | claude -p 超时 | 标记 processed，不发送 |
| TC-007 | jsonl 文件被删除 | 警告，主循环继续 |
| TC-008 | tmux pane 消失 | 错误，主循环继续 |
| TC-009 | jsonl mtime 不稳定 | 跳过本轮 |
| TC-010 | 同一 tool_use_id 两轮检测 | 只响应一次 |
| TC-011 | --dry-run | 决策正常，不实际发送 |
| TC-012 | Ctrl+C | 优雅退出 |
| TC-013 | CLAUDE.md 不存在 | 警告，正常运行 |
| TC-014 | system-prompt-file 不存在 | 启动退出码 2 |
| TC-015 | claude -p 返回 markdown fence JSON | 提取成功或安全失败 |
| TC-020 | Bash `cat src/main.py` 权限请求 | 安全策略 ALLOW，发送 Y |
| TC-021 | Bash `rm -rf /tmp/old` 权限请求 | 安全策略 DENY，发送 n |
| TC-022 | Bash `ls -la && rm file.txt` 复合命令 | DENY（rm 在黑名单） |
| TC-023 | Edit 项目内文件 | ALLOW |
| TC-024 | Edit 项目外文件 `/etc/hosts` | DENY |
| TC-025 | Write 项目内文件 | ALLOW |
| TC-026 | Write 项目外文件 | DENY |
| TC-027 | 未知工具名 `CustomTool` | 默认 DENY |
| TC-028 | Read 任何文件 | ALLOW |
| TC-029 | Bash `git push --force` | DENY |
| TC-030 | Bash `uv run pytest` | ALLOW |
| TC-031 | safety-policy-file 覆盖允许 `docker build` | ALLOW |
| TC-032 | safety-policy-file 的 deny 优先于 allow | deny 生效 |
| TC-033 | Edit 路径含符号链接指向项目外 | 解析 realpath 后 DENY |
| TC-034 | Bash 管道 `cat file \| head -5` | ALLOW（末段只读） |
| TC-035 | Bash `echo "hello" > /absolute/path` | DENY（项目外重定向） |

## 边界情况

| 情况 | 处理方式 |
|------|---------|
| jsonl 坏行 | 跳过并记录 warning |
| assistant 消息含多个 tool_use | 逐个检查，只处理最后一个未回答的 |
| user 消息 content 是字符串 | 无 tool_result，跳过 |
| jsonl 文件空 | 跳过本轮 |
| claude -p stdout 混入 stderr | 三级 JSON 提取策略 |
| Bash 命令含环境变量 `$HOME/file` | 不展开变量，按字面值匹配路径 |
| Edit file_path 是相对路径 | 相对于 CWD 解析为绝对路径后判定 |
| 符号链接指向项目外 | realpath 解析后判定 |
| 复合命令 `cmd1 && cmd2 \|\| cmd3` | 按 `&&`/`\|\|`/`;` 分段，逐段检查 |
| 管道 `safe \| dangerous` | 检查所有段，任一危险则 DENY |
| 空 command 字符串 | DENY |
| tool_use 的 input 缺少预期字段 | DENY 并记录警告 |

## 输出示例

### 启动日志

```
[2026-04-16 10:00:01] 🚀 claude-auto-responder v0.2.0 启动
    └─ jsonl: ~/.claude/projects/-xxx/abc.jsonl | pane: claude-main:0.1 | interval: 2.0s | safety: 内置策略
```

### AskUserQuestion 决策

```
[2026-04-16 10:00:05] 👀 检测到待响应请求 toolu_01ABC (AskUserQuestion)
    └─ question: 你希望使用哪种认证方式？ | options: 3
[2026-04-16 10:00:05] 🤔 调用决策者 (claude -p)
[2026-04-16 10:00:09] ✅ 决策完成 answers=['JWT token (Recommended)']
[2026-04-16 10:00:09] 📤 已发送到 tmux pane claude-main:0.1
```

### 权限请求自动允许

```
[2026-04-16 10:00:12] 👀 检测到待响应请求 toolu_01DEF (Bash)
[2026-04-16 10:00:12] 🔒 安全策略判定: ALLOW (只读白名单: cat)
    └─ cmd: "cat src/main.py"
[2026-04-16 10:00:12] ✅ 已发送 Y 到 tmux pane claude-main:0.1
```

### 权限请求自动拒绝

```
[2026-04-16 10:00:15] 👀 检测到待响应请求 toolu_01GHI (Bash)
[2026-04-16 10:00:15] 🚫 安全策略拒绝: DENY (删除命令黑名单: rm)
    └─ cmd: "rm -rf /tmp/old"
[2026-04-16 10:00:15] 📤 已发送 n 到 tmux pane claude-main:0.1
```

## 超出范围

- ❌ 自动发现 tmux pane 或 jsonl 文件
- ❌ GUI / TUI
- ❌ 多会话并发监听（需并发请启动多个进程）
- ❌ Windows 支持
- ❌ processed_ids 持久化到磁盘
- ❌ 通过网络远程控制
- ❌ jsonl 增量读取优化
- ❌ AskUserQuestion 决策失败后自动重试
- ❌ 交互式安全策略学习（自动从用户行为中学习新规则）

## Clarifications

### Session 2026-04-16 00:10

**Q1**: 脚本是否应该处理 AskUserQuestion 以外的等待状态？
**A1**: 是，需要处理所有等待状态（Bash 权限、文件编辑确认等）
**Impact**: REQ-003 从仅检测 AskUserQuestion 扩展为检测所有 tool_use；新增 REQ-010 安全策略引擎

**Q2**: 系统提示词默认行为应该是什么？
**A2**: 内置安全策略引擎用于权限判定（本地、无 LLM）；系统提示词仅用于 AskUserQuestion 的 claude -p 决策
**Impact**: 新增 REQ-010、REQ-011；修改 REQ-004 明确只用于 AskUserQuestion

**Q3**: 安全策略的具体规则？
**A3**: 允许读取类操作、项目内编辑；拒绝删除操作、项目外编辑；可通过配置文件覆盖
**Impact**: REQ-010 定义完整安全规则；新增 TC-020~TC-035

# Claude Auto Responder

Automatically respond to all waiting states in a tmux-hosted Claude Code session, keeping it unblocked and running smoothly unattended.

## The Problem It Solves

During long-running tasks, Claude Code frequently pauses for user input:

- **AskUserQuestion**: Claude Code needs you to pick from a set of options (e.g. "Which authentication method?")
- **Tool permission prompts**: Claude Code needs you to approve Bash commands, file edits, and other operations

Each pause requires manual intervention — if you're away from your desk, the task stalls.

**claude-auto-responder** acts as your unattended operator:

- For choice prompts (AskUserQuestion) — calls `claude -p` with project context for intelligent decisions
- For permission prompts — a built-in safety policy engine decides **locally** (no LLM call, < 1 ms)

## Prerequisites

- Python 3.11+
- tmux (installed and running)
- claude CLI (`claude --version` must work; used for AskUserQuestion decisions)
- No third-party Python dependencies — standard library only

## Quick Start

### Step 1: Launch Claude Code inside tmux

```bash
# Create a tmux session for Claude Code
tmux new-session -s claude-main

# Start Claude Code inside the tmux session
claude
```

### Step 2: Find the jsonl file path and tmux pane

```bash
# Open a new terminal window

# List jsonl files (find the most recent one)
ls -lt ~/.claude/projects/*/*.jsonl | head -5
# Example output:
# -rw-r--r--  1 user  staff  12345  Apr 16 10:00  /Users/user/.claude/projects/-Users-user-code-myproject/abc123-def456.jsonl

# List tmux panes
tmux list-panes -a -F "#{session_name}:#{window_index}.#{pane_index}"
# Example output:
# claude-main:0.0
```

### Step 3: Start the auto-responder

```bash
python scripts/python/claude_auto_responder.py \
    --jsonl ~/.claude/projects/-Users-user-code-myproject/abc123-def456.jsonl \
    --tmux-pane claude-main:0.0
```

You should see:

```
[2026-04-16 10:00:01] 🚀 claude-auto-responder v0.2.0-dev started
    └─ jsonl: /Users/user/.claude/projects/... | pane: claude-main:0.0 | interval: 2.0s | safety: built-in policy
```

You can now step away. The script handles all of Claude Code's waiting states automatically. Press `Ctrl+C` to stop.

## CLI Parameters

| Parameter | Required | Default | Description |
|-----------|:--------:|---------|-------------|
| `--jsonl PATH` | Yes | — | Path to Claude Code's jsonl session file |
| `--tmux-pane TARGET` | Yes | — | Target tmux pane in `session:window.pane` format |
| `--system-prompt-file PATH` | | None | System prompt file (affects AskUserQuestion decisions only) |
| `--safety-policy-file PATH` | | None | Safety policy override file (JSON) |
| `--poll-interval SECONDS` | | `2.0` | Polling interval in seconds |
| `--stable-ms MILLIS` | | `1500` | Minimum jsonl mtime age in milliseconds before reading |
| `--project-root PATH` | | CWD | Project root directory; defines the path safety boundary |
| `--claude-bin PATH` | | `claude` | Path to the claude CLI executable |
| `--log-file PATH` | | None | Log file path (logs go to stderr by default) |
| `--dry-run` | | `false` | Decide but don't actually send keystrokes to tmux |
| `--decide-timeout SECONDS` | | `180` | Timeout for `claude -p` calls |
| `--health-check` | | `false` | Run health checks and output a JSON report to stdout |
| `--version` | | — | Print version and exit |

## Safety Policy Engine

The script includes a built-in safety policy engine for handling tool permission requests. Core principle: **deny by default, allow by whitelist**.

### Default Rules Overview

| Tool | Condition | Decision |
|------|-----------|----------|
| `Read` / `Grep` / `Glob` | Any | ALLOW |
| `Edit` / `Write` / `NotebookEdit` | File inside project directory | ALLOW |
| `Edit` / `Write` / `NotebookEdit` | File outside project directory | DENY |
| `Bash` | Command on safe whitelist | ALLOW |
| `Bash` | Command on dangerous blacklist | DENY |
| `Bash` | Command on neither list | DENY |
| Any unknown tool | — | DENY |

### Bash Safe Command Whitelist

The following commands (or command prefixes) are considered safe and allowed automatically:

**Read-only / Inspection**

```
cat  head  tail  less  more  wc  file  stat  du  df
ls  tree  pwd  echo  printf  date  uname  hostname
grep  rg  find  fd  locate  which  whereis  type
ps  top  htop  lsof
env  printenv
curl  wget  ping  dig  nslookup
```

**Read-only Git operations**

```
git status    git log     git diff    git branch
git show      git remote  git tag
```

**Development / Build / Test**

```
python -c       node -e         make
uv run pytest   uv run ruff
npm test        npm run
cargo test      cargo build     cargo check
go build        go test
pip list        pip show        npm list        npm info
```

### Bash Dangerous Command Blacklist

The following patterns are immediately denied:

**Deletion**

```
rm  rmdir  unlink  shred
```

**Destructive Git operations**

```
git clean             git reset --hard
git push --force      git push -f
git checkout -- .     git restore .
```

**System / Permission changes**

```
chmod  chown  chgrp  mkfs  fdisk  dd
```

**Package manager mutations**

```
pip install    pip uninstall
npm install    npm uninstall
```

**Dangerous shell constructs**

```
eval  exec
```

### Compound Command Handling

- Commands joined with `&&` / `||` / `;`: **each segment is checked** — if any segment matches the blacklist, the entire command is denied
- Piped commands (`|`): all segments are checked; any dangerous segment causes denial
- Redirects (`>`) to absolute paths outside the project: denied (unless allowed by policy)

Examples:

```
ls -la && rm file.txt     → DENY  (rm is blacklisted)
cat file | head -5        → ALLOW (all segments are read-only)
echo "x" > /etc/hosts    → DENY  (redirect outside project)
```

### Path Safety Checks

For `Edit` / `Write` / `NotebookEdit` tools, the script verifies whether the target file is inside `--project-root`:

1. Resolves symlinks and relative paths with `os.path.realpath()`
2. Checks whether the resolved path starts with the project root
3. Symlinks pointing outside the project are denied (prevents bypass)
4. Non-existent paths: walks up to the nearest existing parent directory to determine membership

## Custom Safety Policies

Use `--safety-policy-file` to supply a JSON file that overrides default rules.

### Configuration Format

```json
{
  "allow_commands": ["docker build", "docker run"],
  "deny_commands": ["curl -X POST"],
  "allow_paths_outside_project": ["/tmp/build-*"],
  "deny_tools": ["Agent"],
  "allow_unknown_tools": false
}
```

All fields are optional.

| Field | Type | Description |
|-------|------|-------------|
| `allow_commands` | `string[]` | Additional allowed Bash command prefixes |
| `deny_commands` | `string[]` | Additional denied Bash command prefixes |
| `allow_paths_outside_project` | `string[]` | Glob patterns for allowed paths outside the project (applies to Edit/Write tools and Bash redirects) |
| `deny_tools` | `string[]` | Additional tool names to deny |
| `allow_unknown_tools` | `bool` | Whether to allow unrecognized tools (default `false`) |

### Priority Order

```
deny_commands > allow_commands > built-in blacklist > built-in whitelist
```

`deny_commands` has the highest priority — even if a command matches both `allow_commands` and `deny_commands`, it will be denied.

### Example: Allow Docker but Block Publishing

```json
{
  "allow_commands": ["docker build", "docker run", "docker compose"],
  "deny_commands": ["docker push"]
}
```

### Example: Allow Writes to /tmp Build Artifacts

```json
{
  "allow_paths_outside_project": ["/tmp/build-*", "/tmp/test-output-*"]
}
```

## System Prompt (AskUserQuestion Customization)

Use `--system-prompt-file` to customize the decision-making Claude's preferences when answering AskUserQuestion prompts.

This is useful when your project has specific style or tooling preferences.

### Example Prompt File (`my-prompt.txt`)

```text
You are making decisions for a Python backend project. Follow these preferences:
- Prefer type-safe approaches
- Favor the standard library over third-party packages
- Use pytest as the testing framework
- If an option is marked "Recommended", prefer it
```

```bash
python scripts/python/claude_auto_responder.py \
    --jsonl ~/.claude/projects/-xxx/session.jsonl \
    --tmux-pane claude-main:0.0 \
    --system-prompt-file ./my-prompt.txt
```

### AskUserQuestion Decision Flow

1. Reads `CLAUDE.md` from the project root (truncated to 30 KB)
2. Reads `.codexspec/memory/constitution.md` (truncated to 30 KB)
3. Reads the system prompt file (if specified)
4. Assembles these with the question details into a prompt
5. Calls `claude -p <prompt>` to get a JSON-formatted answer
6. Validates that the returned label(s) exist among the available options
7. Sends the selected label(s) via tmux

If `claude -p` times out, returns an error, or fails validation, the question is skipped (marked as processed — no infinite retries).

## Health Check

Use the `--health-check` flag to quickly verify that all dependencies are properly configured, without entering the main loop.

### Usage

```bash
python scripts/python/claude_auto_responder.py \
    --jsonl ~/.claude/projects/-xxx/session.jsonl \
    --tmux-pane claude-main:0.0 \
    [--safety-policy-file ./policy.json] \
    --health-check
```

### Output Format

The health check outputs a JSON report to stdout:

```json
{
  "overall": "healthy",
  "checks": [
    {"name": "jsonl_file", "status": "pass", "message": "/path/to/session.jsonl"},
    {"name": "tmux_pane", "status": "pass", "message": "claude-main:0.0"},
    {"name": "claude_cli", "status": "pass", "message": "claude available"},
    {"name": "safety_policy_file", "status": "pass", "message": "./policy.json"}
  ]
}
```

### Checks Performed

| Check | Description |
|-------|-------------|
| `jsonl_file` | jsonl file exists and is readable |
| `tmux_pane` | Target tmux pane exists |
| `claude_cli` | claude CLI is available and `--version` succeeds |
| `safety_policy_file` | Safety policy file exists and contains valid JSON (if provided) |

### Exit Codes

- `0` — All checks passed (`overall: "healthy"`)
- `1` — At least one check failed (`overall: "unhealthy"`)

### Example: Use in a Monitoring Script

```bash
# Verify auto-responder configuration before starting
if python scripts/python/claude_auto_responder.py \
    --jsonl ~/.claude/projects/-xxx/session.jsonl \
    --tmux-pane claude-main:0.0 \
    --health-check; then
    echo "Health check passed"
else
    echo "Health check failed"
    exit 1
fi
```

## Log Format

Logs are written to stderr in the format `[timestamp] emoji message`.

| Emoji | Meaning |
|-------|---------|
| 🚀 | Startup / shutdown |
| 👀 | Pending request detected |
| 🤔 | Calling claude -p for a decision |
| 🔒 | Safety policy evaluation in progress |
| ✅ | Allowed / sent successfully |
| 🚫 | Denied by safety policy |
| 📤 | Sent to tmux |
| ⚠️ | Warning |
| ❌ | Error |

### Log Examples

**AskUserQuestion — automatic selection**:

```
[2026-04-16 10:00:05] 👀 Pending request detected toolu_01ABC (AskUserQuestion)
[2026-04-16 10:00:05] 🤔 Calling decider (claude -p)
[2026-04-16 10:00:09] ✅ Decision complete answers=['JWT token (Recommended)']
[2026-04-16 10:00:09] 📤 Sent to tmux pane claude-main:0.0
```

**Bash permission — auto-approved**:

```
[2026-04-16 10:00:12] 👀 Pending request detected toolu_01DEF (Bash)
[2026-04-16 10:00:12] 🔒 Safety policy evaluation toolu_01DEF
[2026-04-16 10:00:12] ✅ ALLOW (whitelisted command: cat)
[2026-04-16 10:00:12] 📤 Sent Y to tmux pane claude-main:0.0
```

**Bash permission — auto-denied**:

```
[2026-04-16 10:00:15] 👀 Pending request detected toolu_01GHI (Bash)
[2026-04-16 10:00:15] 🔒 Safety policy evaluation toolu_01GHI
[2026-04-16 10:00:15] 🚫 DENY (blacklisted: rm)
[2026-04-16 10:00:15] 📤 Sent n to tmux pane claude-main:0.0
```

To also write logs to a file:

```bash
python scripts/python/claude_auto_responder.py \
    --jsonl ... --tmux-pane ... \
    --log-file /tmp/auto-responder.log
```

## Usage Scenarios

### Scenario 1: Overnight Large-Scale Refactoring

```bash
# Terminal 1: Launch Claude Code in tmux
tmux new-session -s refactor
claude

# Terminal 2: Start the auto-responder
python scripts/python/claude_auto_responder.py \
    --jsonl ~/.claude/projects/-Users-user-code-myproject/session.jsonl \
    --tmux-pane refactor:0.0 \
    --log-file ~/refactor-log.txt

# Go to sleep — the auto-responder has it covered
```

### Scenario 2: Dry-Run First, Then Go Live

```bash
# Preview what decisions the script would make
python scripts/python/claude_auto_responder.py \
    --jsonl ~/.claude/projects/-xxx/session.jsonl \
    --tmux-pane claude-main:0.0 \
    --dry-run

# Once you're satisfied, remove --dry-run to go live
```

### Scenario 3: Explicit Project Root

If you run the script from a different directory, specify the project root explicitly so that path safety checks work correctly:

```bash
python scripts/python/claude_auto_responder.py \
    --jsonl ~/.claude/projects/-xxx/session.jsonl \
    --tmux-pane claude-main:0.0 \
    --project-root /Users/user/code/myproject
```

### Scenario 4: Multiple Sessions in Parallel

Run one auto-responder instance per Claude Code session:

```bash
# Session A
python scripts/python/claude_auto_responder.py \
    --jsonl ~/.claude/projects/-projectA/session-a.jsonl \
    --tmux-pane sessionA:0.0 &

# Session B
python scripts/python/claude_auto_responder.py \
    --jsonl ~/.claude/projects/-projectB/session-b.jsonl \
    --tmux-pane sessionB:0.0 &
```

## Exit Codes

| Code | Meaning |
|------|---------|
| `0` | Normal exit (Ctrl+C) or all health checks passed |
| `1` | One or more health checks failed |
| `2` | Invalid startup arguments (missing file, malformed JSON, etc.) |
| `130` | SIGINT |

## How It Works

```
+--------------------------------------------------------------+
|                  claude_auto_responder.py                     |
|                                                              |
|  MainLoop (polls every 2 s)                                  |
|    |                                                         |
|    +-> Detector -> read jsonl -> find unanswered tool_use    |
|    |                                                         |
|    +-> Router dispatches by tool name:                       |
|    |     |                                                   |
|    |     +- AskUserQuestion -> PromptBuilder -> claude -p    |
|    |     |                                                   |
|    |     +- Other tools -> SafetyPolicyEngine (local rules)  |
|    |                         +- PathChecker                  |
|    |                         +- BashClassifier               |
|    |                                                         |
|    +-> TmuxSender -> tmux send-keys (answer / Y / n)         |
+--------------------------------------------------------------+
```

### Detection Algorithm

1. Reads the jsonl file; extracts all `tool_use` blocks from assistant messages and `tool_result` blocks from user messages
2. Finds the last `tool_use` with no matching `tool_result` — this is the request Claude Code is waiting on
3. Mtime stability check: only reads the file when its last-modified time is at least `--stable-ms` (default 1.5 s) old, avoiding partially-written states
4. Deduplication: processed `tool_use_id` values are kept in memory; the same request is never handled twice

## FAQ

### How do I find the correct jsonl file?

```bash
# List all session files, sorted by modification time
ls -lt ~/.claude/projects/*/*.jsonl | head -10
```

The jsonl path follows the pattern `~/.claude/projects/<project-slug>/<session-id>.jsonl`, where `<project-slug>` is the project path with `/` replaced by `-`.

### How do I find the correct tmux pane?

```bash
# List all panes
tmux list-panes -a -F "#{session_name}:#{window_index}.#{pane_index} - #{pane_current_command}"
```

The format is `session:window.pane`, e.g. `claude-main:0.0`.

### Can the script cause any damage?

The safety design is **deny by default**:

- Bash commands not on the whitelist are denied
- File edits outside the project directory are denied
- Unknown tools are denied
- All delete operations are denied

The worst-case outcome is a **false denial** — Claude Code receives "n" and either tries a different approach or waits for manual intervention. A false denial causes no harm.

### What happens if the jsonl file is deleted?

The script logs a warning and continues polling. When the file reappears, it resumes automatically.

### What happens if the tmux pane is closed?

Sending fails; the script logs an error but the main loop keeps running.

### Can I use --system-prompt-file and --safety-policy-file together?

Yes. They serve different purposes:

- `--system-prompt-file` only affects AskUserQuestion decisions (via `claude -p`)
- `--safety-policy-file` only affects tool permission decisions (local policy engine)

### Why does AskUserQuestion decision-making sometimes fail?

Possible causes:

- The `claude -p` call timed out (default 180 s; adjustable with `--decide-timeout`)
- The returned label didn't exactly match any available option
- The returned JSON couldn't be parsed

On failure, the question is marked as processed and skipped — no infinite retries.

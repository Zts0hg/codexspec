#!/usr/bin/env python3
"""
Claude Auto Responder (claude-auto-responder)
自动响应运行在 tmux 中的 Claude Code 的所有等待状态

功能：
  - 检测 AskUserQuestion → 调用 claude -p 智能决策
  - 检测工具权限请求（Bash/Edit/Write 等）→ 本地安全策略引擎判定

用法:
    python claude_auto_responder.py \\
        --jsonl ~/.claude/projects/-xxx/session.jsonl \\
        --tmux-pane claude-main:0.1

    python claude_auto_responder.py \\
        --jsonl ~/.claude/projects/-xxx/session.jsonl \\
        --tmux-pane claude-main:0.1 \\
        --system-prompt-file ./my-prompt.txt \\
        --safety-policy-file ./policy.json \\
        --dry-run
"""

import argparse
import json
import os
import re
import signal
import subprocess
import sys
import time
from dataclasses import dataclass
from datetime import datetime
from fnmatch import fnmatch
from pathlib import Path
from typing import Optional

try:
    from importlib.metadata import version

    __version__ = version("claude-auto-responder")
except Exception:
    __version__ = "0.2.0-dev"

EXIT_SUCCESS = 0
EXIT_INVALID_ARGS = 2
EXIT_SIGINT = 130


class SafetyPolicyError(Exception):
    """Raised when safety policy file is invalid."""

    pass


# ============================================================================
# Dataclasses (Task 1.5)
# ============================================================================


@dataclass
class PendingToolUse:
    tool_use_id: str
    name: str
    input: dict


@dataclass
class PolicyDecision:
    action: str  # 'ALLOW' or 'DENY'
    reason: str


@dataclass
class Response:
    response_type: str  # 'answers' or 'permission'
    answers: Optional[list] = None
    allow: Optional[bool] = None
    reason: str = ""


# ============================================================================
# Logger (Task 1.4)
# ============================================================================


class Logger:
    EMOJI = {
        "startup": "🚀",
        "pending": "👀",
        "decide": "🤔",
        "policy": "🔒",
        "policy_allow": "✅",
        "policy_deny": "🚫",
        "sent": "📤",
        "warn": "⚠️",
        "error": "❌",
    }

    def __init__(self, log_file: Optional[str] = None):
        self._log_file = log_file
        self._fh = None
        if log_file:
            try:
                self._fh = open(log_file, "a", encoding="utf-8")
            except OSError:
                pass

    def _ts(self) -> str:
        return datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")

    def _emit(self, emoji_key: str, msg: str, detail: str = "") -> None:
        emoji = self.EMOJI.get(emoji_key, "")
        line = f"{self._ts()} {emoji} {msg}"
        if detail:
            line += f"\n    └─ {detail}"
        print(line, file=sys.stderr)
        if self._fh:
            try:
                self._fh.write(line + "\n")
                self._fh.flush()
            except OSError:
                pass

    def startup(self, msg: str, detail: str = "") -> None:
        self._emit("startup", msg, detail)

    def pending(self, msg: str, detail: str = "") -> None:
        self._emit("pending", msg, detail)

    def decide(self, msg: str, detail: str = "") -> None:
        self._emit("decide", msg, detail)

    def policy(self, msg: str, detail: str = "") -> None:
        self._emit("policy", msg, detail)

    def policy_allow(self, msg: str, detail: str = "") -> None:
        self._emit("policy_allow", msg, detail)

    def policy_deny(self, msg: str, detail: str = "") -> None:
        self._emit("policy_deny", msg, detail)

    def sent(self, msg: str, detail: str = "") -> None:
        self._emit("sent", msg, detail)

    def warn(self, msg: str, detail: str = "") -> None:
        self._emit("warn", msg, detail)

    def error(self, msg: str, detail: str = "") -> None:
        self._emit("error", msg, detail)

    def close(self) -> None:
        if self._fh:
            try:
                self._fh.close()
            except OSError:
                pass


# ============================================================================
# JsonlParser (Task 2.2)
# ============================================================================


def parse_jsonl(path) -> list:
    path = Path(path)
    if not path.exists():
        return []
    records = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                records.append(json.loads(line))
            except json.JSONDecodeError:
                pass
    return records


def extract_pending_tool_use(records: list) -> Optional[PendingToolUse]:
    tool_uses = []
    answered_ids: set = set()

    for rec in records:
        rec_type = rec.get("type")
        content = rec.get("message", {}).get("content")
        if content is None:
            continue

        if rec_type == "assistant" and isinstance(content, list):
            for block in content:
                if isinstance(block, dict) and block.get("type") == "tool_use":
                    tool_uses.append(
                        PendingToolUse(
                            tool_use_id=block["id"],
                            name=block["name"],
                            input=block.get("input", {}),
                        )
                    )

        elif rec_type == "user" and isinstance(content, list):
            for block in content:
                if isinstance(block, dict) and block.get("type") == "tool_result":
                    tid = block.get("tool_use_id")
                    if tid:
                        answered_ids.add(tid)

    for tu in reversed(tool_uses):
        if tu.tool_use_id not in answered_ids:
            return tu

    return None


# ============================================================================
# PathChecker (Task 3.2)
# ============================================================================


def is_path_within_project(file_path: str, project_root: Path) -> bool:
    real_root = os.path.realpath(str(project_root))
    target = Path(file_path)
    if target.exists() or target.is_symlink():
        real_target = os.path.realpath(str(target))
    else:
        parent = target.parent
        while not parent.exists() and str(parent) != parent.root:
            parent = parent.parent
        real_target = os.path.join(os.path.realpath(str(parent)), os.path.relpath(str(target), str(parent)))
    return real_target.startswith(real_root + os.sep) or real_target == real_root


# ============================================================================
# BashClassifier (Task 3.4)
# ============================================================================

SAFE_COMMANDS = frozenset(
    [
        "cat",
        "head",
        "tail",
        "less",
        "more",
        "wc",
        "file",
        "stat",
        "du",
        "df",
        "grep",
        "rg",
        "find",
        "fd",
        "locate",
        "which",
        "whereis",
        "type",
        "ls",
        "tree",
        "pwd",
        "echo",
        "printf",
        "date",
        "uname",
        "hostname",
        "cd",
        "pushd",
        "popd",
        "env",
        "printenv",
        "curl",
        "wget",
        "ping",
        "dig",
        "nslookup",
        "ps",
        "top",
        "htop",
        "lsof",
        "python",
        "node",
        "make",
    ]
)

SAFE_PREFIXES = (
    "git status",
    "git log",
    "git diff",
    "git branch",
    "git show",
    "git remote",
    "git tag",
    "pip list",
    "pip show",
    "npm list",
    "npm info",
    "uv pip list",
    "uv run pytest",
    "uv run ruff",
    "npm test",
    "npm run",
    "cargo test",
    "cargo build",
    "cargo check",
    "cargo --version",
    "go build",
    "go test",
    "python -c",
    "node -e",
)

DANGEROUS_PATTERNS = (
    "rm ",
    "rm\t",
    "rmdir",
    "unlink",
    "shred",
    "git clean",
    "git reset --hard",
    "git push --force",
    "git push -f",
    "git checkout -- .",
    "git restore .",
    "chmod",
    "chown",
    "chgrp",
    "mkfs",
    "fdisk",
    "dd ",
    "pip install",
    "pip uninstall",
    "npm install",
    "npm uninstall",
    "eval ",
    "exec ",
)


def _classify_segment(segment: str, project_root: Path, policy: Optional[dict] = None) -> tuple:
    segment = segment.strip()
    if not segment:
        return ("DANGEROUS", "空命令")

    policy = policy or {}
    policy_deny = policy.get("deny_commands", [])
    policy_allow = policy.get("allow_commands", [])

    for pat in policy_deny:
        if segment.startswith(pat):
            return ("DANGEROUS", f"策略拒绝: {pat}")

    for pat in policy_allow:
        if segment.startswith(pat):
            return ("SAFE", f"策略允许: {pat}")

    for pat in DANGEROUS_PATTERNS:
        if pat in segment:
            return ("DANGEROUS", f"黑名单: {pat.strip()}")

    # Check redirect to outside project (before whitelist — redirect overrides safety)
    if ">" in segment:
        allow_outside = policy.get("allow_paths_outside_project", [])
        parts = segment.split(">")
        for part in parts[1:]:
            redir_path = part.strip().split()[0] if part.strip() else ""
            if redir_path.startswith("/") and not is_path_within_project(redir_path, project_root):
                if any(fnmatch(redir_path, pat) for pat in allow_outside):
                    continue
                return ("DANGEROUS", f"重定向到项目外: {redir_path}")

    for prefix in SAFE_PREFIXES:
        if segment.startswith(prefix):
            return ("SAFE", f"白名单前缀: {prefix}")

    first_token = segment.split()[0] if segment.split() else ""
    if first_token in SAFE_COMMANDS:
        return ("SAFE", f"白名单命令: {first_token}")

    return ("UNKNOWN", f"未知命令: {first_token}")


def classify_bash_command(command: str, project_root: Path, policy: Optional[dict] = None) -> tuple:
    if not command or not command.strip():
        return ("DANGEROUS", "空命令")

    segments = re.split(r"\s*(?:&&|\|\||;)\s*", command)

    # Also split by pipe and check all segments
    all_segments = []
    for seg in segments:
        pipe_parts = [p.strip() for p in seg.split("|")]
        all_segments.extend(pipe_parts)

    has_unknown = False
    for seg in all_segments:
        if not seg.strip():
            continue
        cat, reason = _classify_segment(seg.strip(), project_root, policy)
        if cat == "DANGEROUS":
            return ("DANGEROUS", reason)
        if cat == "UNKNOWN":
            has_unknown = True

    if has_unknown:
        return ("UNKNOWN", "含未知命令")

    return ("SAFE", "全部安全")


# ============================================================================
# SafetyPolicyEngine (Task 3.6)
# ============================================================================

ALWAYS_ALLOW_TOOLS = frozenset(["Read", "Grep", "Glob"])
PATH_TOOLS = frozenset(["Edit", "Write", "NotebookEdit"])


class SafetyPolicyEngine:
    def __init__(self, project_root: Path, policy: Optional[dict] = None):
        self._root = project_root
        self._policy = policy or {}

    def evaluate(self, tool_name: str, tool_input: dict) -> PolicyDecision:
        deny_tools = self._policy.get("deny_tools", [])
        if tool_name in deny_tools:
            return PolicyDecision("DENY", f"策略拒绝工具: {tool_name}")

        if tool_name in ALWAYS_ALLOW_TOOLS:
            return PolicyDecision("ALLOW", f"只读工具: {tool_name}")

        if tool_name in PATH_TOOLS:
            fp = tool_input.get("file_path")
            if not fp:
                return PolicyDecision("DENY", f"{tool_name} 缺少 file_path")
            if is_path_within_project(fp, self._root):
                return PolicyDecision("ALLOW", f"项目内路径: {fp}")
            allow_outside = self._policy.get("allow_paths_outside_project", [])
            for pattern in allow_outside:
                if fnmatch(fp, pattern):
                    return PolicyDecision("ALLOW", f"策略允许外部路径: {pattern}")
            return PolicyDecision("DENY", f"项目外路径: {fp}")

        if tool_name == "Bash":
            cmd = tool_input.get("command")
            if not cmd:
                return PolicyDecision("DENY", "Bash 缺少 command")
            cat, reason = classify_bash_command(cmd, self._root, self._policy)
            if cat == "SAFE":
                return PolicyDecision("ALLOW", reason)
            return PolicyDecision("DENY", reason)

        if self._policy.get("allow_unknown_tools", False):
            return PolicyDecision("ALLOW", f"策略允许未知工具: {tool_name}")

        return PolicyDecision("DENY", f"未知工具默认拒绝: {tool_name}")


def load_safety_policy(path: Optional[str]) -> Optional[dict]:
    if not path:
        return None
    p = Path(path)
    if not p.exists():
        raise SafetyPolicyError(f"安全策略文件不存在: {path}")
    try:
        with open(p, "r", encoding="utf-8") as f:
            policy = json.load(f)
        if not isinstance(policy, dict):
            raise ValueError("策略文件顶层必须是 JSON 对象")
        return policy
    except (json.JSONDecodeError, ValueError) as e:
        raise SafetyPolicyError(f"安全策略文件格式错误: {e}") from e
    except OSError as e:
        raise SafetyPolicyError(f"安全策略文件读取失败: {e}") from e


# ============================================================================
# ContextLoader + PromptBuilder (Task 4.2)
# ============================================================================

MAX_CONTEXT_SIZE = 30000


def load_project_context(project_root: Path) -> dict:
    ctx = {"claude_md": "", "constitution": ""}
    claude_md = project_root / "CLAUDE.md"
    if claude_md.exists():
        try:
            text = claude_md.read_text(encoding="utf-8")
            ctx["claude_md"] = text[:MAX_CONTEXT_SIZE]
        except OSError:
            pass
    constitution = project_root / ".codexspec" / "memory" / "constitution.md"
    if constitution.exists():
        try:
            text = constitution.read_text(encoding="utf-8")
            ctx["constitution"] = text[:MAX_CONTEXT_SIZE]
        except OSError:
            pass
    return ctx


def build_prompt(system_prompt: Optional[str], ctx: dict, question: dict) -> str:
    parts = []
    if system_prompt:
        parts.append(f"<system_prompt>\n{system_prompt}\n</system_prompt>")
    parts.append(f"<project_claude_md>\n{ctx.get('claude_md', '')}\n</project_claude_md>")
    parts.append(f"<project_constitution>\n{ctx.get('constitution', '')}\n</project_constitution>")
    question_json = json.dumps(question, ensure_ascii=False, indent=2)
    parts.append(
        "<task>\n"
        "你正在代替人类用户回答另一个 Claude Code 实例发起的 AskUserQuestion 问题。\n"
        "基于上面的项目上下文和系统提示词，为下列问题选出最符合项目规则和开发者偏好的答案。\n\n"
        f"问题详情（JSON）：\n{question_json}\n\n"
        "严格按如下 JSON 格式输出（不要任何额外文字、markdown 代码块或解释）：\n"
        '{"answers": ["<选项的完整 label 字符串>", ...]}\n\n'
        "- 单选题：answers 数组长度必须为 1\n"
        "- 多选题：answers 数组长度可以为 1 到选项数量之间\n"
        "- 每个元素必须完全等于某个选项的 label 字段（大小写、标点完全一致）\n"
        '- 禁止输出 "Other" 或不在 options 中的内容\n'
        "</task>"
    )
    return "\n\n".join(parts)


# ============================================================================
# ClaudeDecider (Task 4.4)
# ============================================================================


def _parse_json_response(text: str) -> Optional[dict]:
    text = text.strip()
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass

    fence_match = re.search(r"```(?:json)?\s*\n?(.*?)\n?```", text, re.DOTALL)
    if fence_match:
        try:
            return json.loads(fence_match.group(1).strip())
        except json.JSONDecodeError:
            pass

    brace_start = text.find("{")
    if brace_start >= 0:
        depth = 0
        for i in range(brace_start, len(text)):
            if text[i] == "{":
                depth += 1
            elif text[i] == "}":
                depth -= 1
                if depth == 0:
                    try:
                        return json.loads(text[brace_start : i + 1])
                    except json.JSONDecodeError:
                        break
    return None


class ClaudeDecider:
    def __init__(self, claude_bin: str = "claude", timeout: int = 180):
        self._bin = claude_bin
        self._timeout = timeout

    def decide(self, prompt: str, question: dict) -> Optional[list]:
        try:
            result = subprocess.run(
                [self._bin, "-p", prompt],
                capture_output=True,
                text=True,
                timeout=self._timeout,
            )
        except subprocess.TimeoutExpired:
            return None
        except FileNotFoundError:
            return None

        if result.returncode != 0:
            return None

        parsed = _parse_json_response(result.stdout)
        if not parsed or "answers" not in parsed:
            return None

        answers = parsed["answers"]
        if not isinstance(answers, list):
            return None

        valid_labels = {opt["label"] for opt in question.get("options", [])}
        for a in answers:
            if a not in valid_labels:
                return None

        is_multi = question.get("multiSelect", False)
        if not is_multi and len(answers) != 1:
            return None

        return answers


# ============================================================================
# Detector (Task 2.4)
# ============================================================================


class Detector:
    def __init__(self, jsonl_path, stable_ms: int = 1500):
        self._path = Path(jsonl_path)
        self._stable_ms = stable_ms
        self._processed_ids: set = set()

    def mark_processed(self, tool_use_id: str) -> None:
        self._processed_ids.add(tool_use_id)

    def check(self) -> Optional[PendingToolUse]:
        if not self._path.exists():
            return None

        mtime = self._path.stat().st_mtime
        age_ms = (time.time() - mtime) * 1000
        if age_ms < self._stable_ms:
            return None

        records = parse_jsonl(self._path)
        if not records:
            return None

        pending = extract_pending_tool_use(records)
        if pending is None:
            return None

        if pending.tool_use_id in self._processed_ids:
            return None

        return pending


# ============================================================================
# TmuxSender (Task 5.2)
# ============================================================================


class TmuxSender:
    def __init__(self, pane: str, dry_run: bool = False):
        self._pane = pane
        self._dry_run = dry_run

    def _send_keys(self, text: str, literal: bool = True) -> bool:
        if self._dry_run:
            return True
        cmd = ["tmux", "send-keys", "-t", self._pane]
        if literal:
            cmd.append("-l")
        cmd.append(text)
        try:
            result = subprocess.run(cmd, capture_output=True, timeout=5)
            return result.returncode == 0
        except (subprocess.TimeoutExpired, FileNotFoundError):
            return False

    def send_answers(self, answers: list) -> bool:
        for label in answers:
            if not self._send_keys(label):
                return False
            if not self._send_keys("Enter", literal=False):
                return False
        return True

    def send_permission(self, allow: bool) -> bool:
        text = "Y" if allow else "n"
        if not self._send_keys(text):
            return False
        return self._send_keys("Enter", literal=False)

    def pane_exists(self) -> bool:
        if self._dry_run:
            return True
        try:
            result = subprocess.run(
                ["tmux", "has-session", "-t", self._pane.split(":")[0]],
                capture_output=True,
                timeout=5,
            )
            return result.returncode == 0
        except (subprocess.TimeoutExpired, FileNotFoundError):
            return False


# ============================================================================
# Router (Task 5.2)
# ============================================================================


class Router:
    def __init__(
        self,
        decider: ClaudeDecider,
        safety_engine: SafetyPolicyEngine,
        context: dict,
        system_prompt: Optional[str] = None,
    ):
        self._decider = decider
        self._engine = safety_engine
        self._ctx = context
        self._system_prompt = system_prompt

    def handle(self, pending: PendingToolUse) -> Optional[Response]:
        if pending.name == "AskUserQuestion":
            return self._handle_ask(pending)
        return self._handle_permission(pending)

    def _handle_ask(self, pending: PendingToolUse) -> Optional[Response]:
        questions = pending.input.get("questions", [])
        if not questions:
            return None
        q = questions[0]
        prompt = build_prompt(self._system_prompt, self._ctx, q)
        answers = self._decider.decide(prompt, q)
        if answers is None:
            return None
        return Response(response_type="answers", answers=answers, reason="claude -p 决策")

    def _handle_permission(self, pending: PendingToolUse) -> Response:
        decision = self._engine.evaluate(pending.name, pending.input)
        allow = decision.action == "ALLOW"
        return Response(response_type="permission", allow=allow, reason=decision.reason)


# ============================================================================
# CLI (Task 1.3)
# ============================================================================


def parse_args(argv: Optional[list] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="claude-auto-responder",
        description="自动响应运行在 tmux 中的 Claude Code 的所有等待状态",
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    parser.add_argument("--jsonl", required=True, help="要监听的 jsonl 文件路径")
    parser.add_argument("--tmux-pane", required=True, help="目标 tmux pane (session:window.pane)")
    parser.add_argument("--system-prompt-file", default=None, help="可选系统提示词文件路径")
    parser.add_argument("--safety-policy-file", default=None, help="可选安全策略 JSON 配置文件")
    parser.add_argument("--poll-interval", type=float, default=2.0, help="轮询间隔秒数 (默认 2.0)")
    parser.add_argument("--stable-ms", type=int, default=1500, help="jsonl mtime 静止阈值毫秒 (默认 1500)")
    parser.add_argument("--project-root", default=None, help="项目根目录 (默认 CWD)")
    parser.add_argument("--claude-bin", default="claude", help="claude CLI 路径 (默认 claude)")
    parser.add_argument("--log-file", default=None, help="可选日志文件路径")
    parser.add_argument("--dry-run", action="store_true", help="仅决策不发送到 tmux")
    parser.add_argument("--decide-timeout", type=int, default=180, help="claude -p 超时秒数 (默认 180)")
    parser.add_argument("--health-check", action="store_true", help="运行健康检查并输出 JSON 报告")
    return parser.parse_args(argv)


def validate_startup(args: argparse.Namespace, logger: Logger) -> bool:
    jsonl_path = Path(args.jsonl)
    if not jsonl_path.exists():
        logger.error(f"jsonl 文件不存在: {args.jsonl}")
        return False

    if args.system_prompt_file:
        if not Path(args.system_prompt_file).exists():
            logger.error(f"系统提示词文件不存在: {args.system_prompt_file}")
            return False

    if args.safety_policy_file:
        if not Path(args.safety_policy_file).exists():
            logger.error(f"安全策略文件不存在: {args.safety_policy_file}")
            return False
        try:
            load_safety_policy(args.safety_policy_file)
        except SafetyPolicyError as e:
            logger.error(f"安全策略文件错误: {e}")
            return False

    return True


def health_check(args: argparse.Namespace) -> int:
    """Run health check and output JSON report to stdout.

    Returns:
        0 if all checks pass, 1 if any check fails.
    """
    checks = []
    overall_healthy = True

    # Check 1: jsonl file exists and is readable
    jsonl_path = Path(args.jsonl)
    jsonl_check = {"name": "jsonl_file", "status": "pass", "message": str(args.jsonl)}
    if not jsonl_path.exists():
        jsonl_check["status"] = "fail"
        jsonl_check["message"] = f"jsonl 文件不存在: {args.jsonl}"
        overall_healthy = False
    else:
        try:
            with open(jsonl_path, "r"):
                pass
        except (OSError, PermissionError) as e:
            jsonl_check["status"] = "fail"
            jsonl_check["message"] = f"jsonl 文件不可读: {e}"
            overall_healthy = False
    checks.append(jsonl_check)

    # Check 2: tmux pane exists
    pane_check = {"name": "tmux_pane", "status": "pass", "message": args.tmux_pane}
    sender = TmuxSender(args.tmux_pane, dry_run=False)
    if not sender.pane_exists():
        pane_check["status"] = "fail"
        pane_check["message"] = f"tmux pane 不存在: {args.tmux_pane}"
        overall_healthy = False
    checks.append(pane_check)

    # Check 3: claude CLI is available
    claude_check = {"name": "claude_cli", "status": "pass", "message": f"{args.claude_bin} 可用"}
    try:
        result = subprocess.run(
            [args.claude_bin, "--version"],
            capture_output=True,
            text=True,
            timeout=5,
        )
        if result.returncode != 0:
            claude_check["status"] = "fail"
            claude_check["message"] = f"{args.claude_bin} 返回错误: {result.returncode}"
            overall_healthy = False
    except (FileNotFoundError, subprocess.TimeoutExpired) as e:
        claude_check["status"] = "fail"
        claude_check["message"] = f"{args.claude_bin} 不可用: {type(e).__name__}"
        overall_healthy = False
    checks.append(claude_check)

    # Check 4: safety-policy-file is valid (if provided)
    if args.safety_policy_file:
        policy_check = {"name": "safety_policy_file", "status": "pass", "message": args.safety_policy_file}
        try:
            policy = load_safety_policy(args.safety_policy_file)
            if policy is None:
                policy_check["status"] = "fail"
                policy_check["message"] = f"安全策略文件加载失败: {args.safety_policy_file}"
                overall_healthy = False
        except Exception as e:
            policy_check["status"] = "fail"
            policy_check["message"] = f"安全策略文件错误: {e}"
            overall_healthy = False
        checks.append(policy_check)

    report = {"overall": "healthy" if overall_healthy else "unhealthy", "checks": checks}
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if overall_healthy else 1


# ============================================================================
# MainLoop (Task 5.3)
# ============================================================================


class MainLoop:
    def __init__(self, args: argparse.Namespace, logger: Logger):
        self._args = args
        self._logger = logger
        self._running = True
        self._project_root = Path(args.project_root) if args.project_root else Path.cwd()

    def _setup_signal(self) -> None:
        def handler(signum, frame):
            self._running = False

        signal.signal(signal.SIGINT, handler)

    def run(self) -> int:
        self._setup_signal()
        args = self._args
        logger = self._logger

        try:
            policy = load_safety_policy(args.safety_policy_file)
        except SafetyPolicyError as e:
            logger.error(f"安全策略文件错误: {e}")
            return EXIT_INVALID_ARGS
        system_prompt = None
        if args.system_prompt_file:
            system_prompt = Path(args.system_prompt_file).read_text(encoding="utf-8")

        ctx = load_project_context(self._project_root)
        detector = Detector(args.jsonl, stable_ms=args.stable_ms)
        decider = ClaudeDecider(claude_bin=args.claude_bin, timeout=args.decide_timeout)
        engine = SafetyPolicyEngine(self._project_root, policy=policy)
        router = Router(decider=decider, safety_engine=engine, context=ctx, system_prompt=system_prompt)
        sender = TmuxSender(args.tmux_pane, dry_run=args.dry_run)

        policy_label = args.safety_policy_file or "内置策略"
        logger.startup(
            f"claude-auto-responder v{__version__} 启动",
            f"jsonl: {args.jsonl} | pane: {args.tmux_pane} | interval: {args.poll_interval}s | safety: {policy_label}",
        )

        while self._running:
            try:
                pending = detector.check()
                if pending is not None:
                    logger.pending(
                        f"检测到待响应请求 {pending.tool_use_id} ({pending.name})",
                    )

                    if pending.name == "AskUserQuestion":
                        logger.decide("调用决策者 (claude -p)")
                    else:
                        logger.policy(f"安全策略判定 {pending.tool_use_id}")

                    resp = router.handle(pending)

                    if resp is None:
                        logger.warn(f"决策失败，跳过 {pending.tool_use_id}")
                        detector.mark_processed(pending.tool_use_id)
                    elif resp.response_type == "answers":
                        logger.policy_allow(f"决策完成 answers={resp.answers}")
                        ok = sender.send_answers(resp.answers)
                        if ok:
                            logger.sent(f"已发送到 tmux pane {args.tmux_pane}")
                        else:
                            logger.error(f"发送失败到 tmux pane {args.tmux_pane}")
                        detector.mark_processed(pending.tool_use_id)
                    elif resp.response_type == "permission":
                        if resp.allow:
                            logger.policy_allow(f"ALLOW ({resp.reason})")
                        else:
                            logger.policy_deny(f"DENY ({resp.reason})")
                        ok = sender.send_permission(resp.allow)
                        if ok:
                            logger.sent(f"已发送 {'Y' if resp.allow else 'n'} 到 tmux pane {args.tmux_pane}")
                        else:
                            logger.error(f"发送失败到 tmux pane {args.tmux_pane}")
                        detector.mark_processed(pending.tool_use_id)

            except Exception as e:
                logger.error(f"轮询异常: {e}")

            if self._running:
                time.sleep(args.poll_interval)

        logger.startup("claude-auto-responder 已停止")
        return EXIT_SUCCESS


def main() -> None:
    args = parse_args()
    logger = Logger(log_file=args.log_file)

    # Health check exits early, bypassing normal startup
    if args.health_check:
        code = health_check(args)
        sys.exit(code)

    if not validate_startup(args, logger):
        sys.exit(EXIT_INVALID_ARGS)

    loop = MainLoop(args, logger)
    code = loop.run()
    logger.close()
    sys.exit(code)


if __name__ == "__main__":
    main()

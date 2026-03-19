#!/usr/bin/env python3
"""
Telegram Notifier for Claude Monitor
从 stdin 读取 claude_monitor.py --json 的输出，发送通知到 Telegram

Usage:
    python claude_monitor.py --json | python notify_telegram.py
"""

import json
import os
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime
from pathlib import Path
from typing import Callable, Optional, Tuple

from dotenv import load_dotenv

load_dotenv()

# ============================================================================
# Config - 配置管理类 (Task 1.3)
# ============================================================================


class Config:
    """集中管理所有配置参数，从环境变量读取"""

    # Telegram 配置
    BOT_TOKEN: Optional[str] = os.environ.get("TELEGRAM_BOT_TOKEN")
    CHAT_ID: Optional[str] = os.environ.get("TELEGRAM_CHAT_ID")
    PROXY: str = os.environ.get("TELEGRAM_PROXY", "http://127.0.0.1:7890")

    # 日志配置
    LOG_FILE: Optional[str] = os.environ.get("TELEGRAM_LOG_FILE")

    # 重试配置
    RETRY_COUNT: int = int(os.environ.get("TELEGRAM_RETRY_COUNT", "3"))
    RETRY_INTERVAL: int = int(os.environ.get("TELEGRAM_RETRY_INTERVAL", "1"))

    # 通知开关
    NOTIFY_ON_COMPLETE: bool = os.environ.get("NOTIFY_ON_COMPLETE", "true").lower() == "true"
    NOTIFY_ON_USER_QUESTION: bool = os.environ.get("NOTIFY_ON_USER_QUESTION", "true").lower() == "true"
    NOTIFY_ON_ERROR: bool = os.environ.get("NOTIFY_ON_ERROR", "true").lower() == "true"
    NOTIFY_ON_TOOL_USE: bool = os.environ.get("NOTIFY_ON_TOOL_USE", "true").lower() == "true"


# ============================================================================
# Logger - 日志处理类 (Task 1.5, 2.2, 2.4, 2.6)
# ============================================================================


class Logger:
    """日志处理器，支持格式化输出、文件写入和轮转"""

    # Emoji 映射表
    EMOJI = {
        "startup": "🚀",
        "waiting": "ℹ️",
        "success": "✅",
        "retry": "⚠️",
        "failure": "❌",
    }

    # 轮转配置
    MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

    def __init__(self, config: Config):
        """初始化 Logger

        Args:
            config: 配置对象
        """
        self.config = config
        self._log_file_handle = None
        self._current_log_path = None
        self._current_log_date = None
        self._file_write_failed = False
        self._log_dir = None

        # 初始化日志路径
        self._log_path = self._resolve_log_path()
        if self._log_path:
            self._log_dir = self._log_path.parent

    # ========================================================================
    # 路径解析 (Task 2.2)
    # ========================================================================

    def _expand_path(self, path: str) -> Path:
        """展开路径中的 ~ 和环境变量

        Args:
            path: 原始路径

        Returns:
            展开后的 Path 对象
        """
        # 展开 ~ 为用户主目录
        expanded = os.path.expanduser(path)
        # 展开环境变量
        expanded = os.path.expandvars(expanded)
        return Path(expanded)

    def _get_default_log_path(self) -> Path:
        """获取默认日志文件路径

        默认路径: {脚本所在目录}/logs/notify_{YYYY-MM-DD}.log

        Returns:
            默认日志文件路径
        """
        # 获取脚本所在目录
        script_dir = Path(__file__).parent
        logs_dir = script_dir / "logs"

        # 生成文件名
        today = datetime.now().strftime("%Y-%m-%d")
        filename = f"notify_{today}.log"

        return logs_dir / filename

    def _resolve_log_path(self) -> Optional[Path]:
        """解析日志文件路径

        Returns:
            解析后的日志文件路径，如果未配置则返回默认路径
        """
        if self.config.LOG_FILE:
            return self._expand_path(self.config.LOG_FILE)
        else:
            # 使用默认路径
            return self._get_default_log_path()

    # ========================================================================
    # 文件操作 (Task 2.4)
    # ========================================================================

    def _ensure_log_dir(self, path: str) -> None:
        """确保日志目录存在

        Args:
            path: 日志文件路径
        """
        log_dir = Path(path).parent
        log_dir.mkdir(parents=True, exist_ok=True)

    def _write_to_file(self, content: str) -> None:
        """写入日志文件

        Args:
            content: 日志内容
        """
        if not self._log_path:
            return

        try:
            # 检查是否需要轮转
            self._rotate_if_needed()

            # 确保目录存在
            self._ensure_log_dir(str(self._log_path))

            # 追加写入
            with open(self._log_path, "a", encoding="utf-8") as f:
                f.write(content + "\n")

        except (IOError, OSError) as e:
            # 降级处理：文件写入失败
            self._file_write_failed = True
            print(f"[WARN] 日志文件写入失败，降级为仅 stderr: {e}", file=sys.stderr)

    # ========================================================================
    # 日志轮转 (Task 2.6)
    # ========================================================================

    def _get_log_path_for_date(self, date: datetime, index: int = 0) -> Path:
        """获取指定日期的日志文件路径

        Args:
            date: 日期
            index: 文件序号 (0=无序号, 1=_1, 2=_2, ...)

        Returns:
            日志文件路径
        """
        if self._log_dir is None:
            self._log_dir = self._get_default_log_path().parent

        date_str = date.strftime("%Y-%m-%d")

        if index == 0:
            filename = f"notify_{date_str}.log"
        else:
            filename = f"notify_{date_str}_{index}.log"

        return self._log_dir / filename

    def _needs_date_rotation(self) -> bool:
        """检查是否需要日期轮转

        Returns:
            是否需要轮转
        """
        if self._current_log_date is None:
            return False

        return datetime.now().date() != self._current_log_date

    def _needs_size_rotation(self, path: str) -> bool:
        """检查是否需要大小轮转

        Args:
            path: 日志文件路径

        Returns:
            是否需要轮转
        """
        if not os.path.exists(path):
            return False

        file_size = os.path.getsize(path)
        return file_size >= self.MAX_FILE_SIZE

    def _find_next_rotation_index(self) -> int:
        """查找下一个轮转序号

        Returns:
            下一个可用的序号
        """
        if self._log_dir is None or not self._log_dir.exists():
            return 1

        today = datetime.now().strftime("%Y-%m-%d")
        index = 1

        while True:
            candidate = self._log_dir / f"notify_{today}_{index}.log"
            if not candidate.exists():
                return index
            index += 1

    def _rotate_if_needed(self) -> None:
        """检查并执行日志轮转

        混合轮转规则:
        1. 按日期分割：每天创建新的日志文件
        2. 按大小分割：单文件超过 10MB 后追加序号
        """
        if not self._log_path or not self._log_path.exists():
            # 文件不存在，更新日期记录
            self._current_log_date = datetime.now().date()
            return

        # 检查日期轮转
        if self._needs_date_rotation():
            # 日期变化，使用新日期的文件
            self._log_path = self._get_log_path_for_date(datetime.now())
            self._current_log_date = datetime.now().date()
            return

        # 检查大小轮转
        if self._needs_size_rotation(str(self._log_path)):
            # 文件过大，创建新序号文件
            next_index = self._find_next_rotation_index()
            self._log_path = self._get_log_path_for_date(datetime.now(), next_index)

    # ========================================================================
    # 基础日志方法 (Task 1.5)
    # ========================================================================

    def _format_timestamp(self) -> str:
        """格式化时间戳

        Returns:
            格式化的时间戳字符串 (YYYY-MM-DD HH:MM:SS)
        """
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def _format_log_entry(self, emoji: str, message: str, details: Optional[dict] = None) -> str:
        """格式化日志条目

        Args:
            emoji: Emoji 标识
            message: 主消息
            details: 详细信息键值对

        Returns:
            格式化的日志字符串
        """
        timestamp = self._format_timestamp()
        lines = [f"[{timestamp}] {emoji} {message}"]

        if details:
            detail_parts = [f"{k}: {v}" for k, v in details.items()]
            lines.append(f"    └─ {' | '.join(detail_parts)}")

        return "\n".join(lines)

    def _write(self, content: str) -> None:
        """写入日志到 stderr 和文件

        Args:
            content: 日志内容
        """
        # 总是输出到 stderr
        print(content, file=sys.stderr)

        # 尝试写入文件（如果配置了且未降级）
        if self._log_path and not self._file_write_failed:
            try:
                self._write_to_file(content)
            except Exception:
                # 降级处理：文件写入失败时仅输出 stderr
                self._file_write_failed = True

    # ========================================================================
    # 公共日志方法 (Task 4.2, 4.4)
    # ========================================================================

    def log_startup(self, chat_id: str, proxy: str, log_path: Optional[str] = None) -> None:
        """输出启动日志

        Args:
            chat_id: Telegram Chat ID
            proxy: 代理地址
            log_path: 日志文件路径
        """
        # Chat ID 脱敏显示 (****6789)
        masked_chat_id = "****" + chat_id[-4:] if len(chat_id) > 4 else "****"

        details = {"Chat ID": masked_chat_id, "Proxy": proxy}
        if log_path:
            details["日志文件"] = log_path

        entry = self._format_log_entry(
            emoji=self.EMOJI["startup"],
            message="Telegram Notifier 启动",
            details=details,
        )
        self._write(entry)

    def log_waiting(self) -> None:
        """输出等待日志"""
        entry = self._format_log_entry(emoji=self.EMOJI["waiting"], message="等待事件中...")
        self._write(entry)

    def log_success(self, event_type: str, session_id: str, details: dict, retry_count: int = 0) -> None:
        """输出成功日志

        Args:
            event_type: 事件类型
            session_id: Session ID
            details: 附加详情
            retry_count: 重试次数
        """
        log_details = {"类型": event_type, "Session": session_id[:8]}
        log_details.update(details)

        message = "通知发送成功"
        if retry_count > 0:
            message = "通知发送成功 (重试后)"
            log_details["重试次数"] = retry_count

        entry = self._format_log_entry(emoji=self.EMOJI["success"], message=message, details=log_details)
        self._write(entry)

    def log_retry(
        self,
        event_type: str,
        session_id: str,
        error: str,
        attempt: int,
        max_attempts: int,
    ) -> None:
        """输出重试日志

        Args:
            event_type: 事件类型
            session_id: Session ID
            error: 错误信息
            attempt: 当前重试次数
            max_attempts: 最大重试次数
        """
        # 截断错误消息 (EC-004)
        truncated_error = self._truncate_error(error)

        details = {
            "类型": event_type,
            "Session": session_id[:8],
            "错误": truncated_error,
            "重试": f"{attempt}/{max_attempts}",
        }

        entry = self._format_log_entry(
            emoji=self.EMOJI["retry"],
            message=f"发送失败 (重试 {attempt}/{max_attempts})",
            details=details,
        )
        self._write(entry)

    def log_failure(self, event_type: str, session_id: str, error: str, retry_count: int) -> None:
        """输出最终失败日志

        Args:
            event_type: 事件类型
            session_id: Session ID
            error: 错误信息
            retry_count: 总重试次数
        """
        # 截断错误消息 (EC-004)
        truncated_error = self._truncate_error(error)

        details = {
            "类型": event_type,
            "Session": session_id[:8],
            "错误": truncated_error,
            "重试次数": retry_count,
        }

        entry = self._format_log_entry(emoji=self.EMOJI["failure"], message="发送最终失败", details=details)
        self._write(entry)

    def _truncate_error(self, error: str, max_length: int = 500) -> str:
        """截断错误消息 (EC-004)

        Args:
            error: 错误消息
            max_length: 最大长度

        Returns:
            截断后的错误消息
        """
        if len(error) <= max_length:
            return error
        return error[:max_length] + "..."

    def _escape_special_chars(self, text: str) -> str:
        """转义特殊字符 (EC-005)

        Args:
            text: 原始文本

        Returns:
            转义后的文本
        """
        # 转义换行符和制表符
        text = text.replace("\n", "\\n")
        text = text.replace("\r", "\\r")
        text = text.replace("\t", "\\t")
        return text


# ============================================================================
# RetryHandler - 重试处理器 (Task 3.2)
# ============================================================================


class RetryHandler:
    """重试处理器，封装重试逻辑"""

    def __init__(self, max_retries: int, interval: float):
        """初始化重试处理器

        Args:
            max_retries: 最大重试次数
            interval: 重试间隔（秒）
        """
        self.max_retries = max_retries
        self.interval = interval

    def execute_with_retry(
        self,
        func: Callable[[], bool],
        on_retry: Optional[Callable[[int, str], None]] = None,
    ) -> Tuple[bool, int, Optional[str]]:
        """执行函数并在失败时重试

        Args:
            func: 要执行的函数，返回 bool 表示成功/失败
            on_retry: 重试时的回调，接收 (attempt, error_message)

        Returns:
            (success, retry_count, last_error)
        """
        last_error = None
        retry_count = 0

        for attempt in range(self.max_retries + 1):
            try:
                if func():
                    return True, retry_count, None
                else:
                    last_error = "Function returned False"
            except Exception as e:
                last_error = str(e)

            # 如果不是最后一次尝试，则等待并重试
            if attempt < self.max_retries:
                retry_count += 1
                if on_retry:
                    on_retry(retry_count, last_error or "Unknown error")
                time.sleep(self.interval)

        return False, retry_count, last_error


# ============================================================================
# Telegram API
# ============================================================================


def send_telegram_message(text: str, parse_mode: str = "HTML") -> bool:
    """
    发送 Telegram 消息

    Args:
        text: 消息内容
        parse_mode: 解析模式 (HTML, Markdown, None)

    Returns:
        是否发送成功

    Raises:
        Exception: 发送失败时抛出异常，包含错误信息
    """
    # 验证配置
    if not Config.BOT_TOKEN:
        raise ValueError("TELEGRAM_BOT_TOKEN 未设置")
    if not Config.CHAT_ID:
        raise ValueError("TELEGRAM_CHAT_ID 未设置")

    url = f"https://api.telegram.org/bot{Config.BOT_TOKEN}/sendMessage"

    payload = {
        "chat_id": Config.CHAT_ID,
        "text": text,
        "parse_mode": parse_mode,
    }

    data = json.dumps(payload).encode("utf-8")
    headers = {"Content-Type": "application/json"}

    # 设置代理
    if Config.PROXY:
        handler = urllib.request.ProxyHandler({"http": Config.PROXY, "https": Config.PROXY})
        opener = urllib.request.build_opener(handler)
    else:
        opener = urllib.request.build_opener()

    req = urllib.request.Request(url, data=data, headers=headers, method="POST")

    try:
        with opener.open(req, timeout=30) as response:
            result = json.loads(response.read().decode("utf-8"))
            if result.get("ok"):
                return True
            else:
                error_desc = result.get("description", "Unknown API error")
                raise Exception(f"Telegram API 错误: {error_desc}")
    except urllib.error.URLError as e:
        raise Exception(f"网络错误: {e}")
    except json.JSONDecodeError as e:
        raise Exception(f"响应解析错误: {e}")


# ============================================================================
# 消息格式化
# ============================================================================


def escape_html(text: str) -> str:
    """转义 HTML 特殊字符"""
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def format_code_block(content: str, max_length: int = 500) -> str:
    """将内容格式化为 Telegram 代码块

    Args:
        content: 要格式化的内容
        max_length: 最大长度，超过则截断。设为 0 禁用截断

    Returns:
        格式化后的 <pre> 标签内容
    """
    if max_length > 0 and len(content) > max_length:
        content = content[:max_length] + "\n... (已截断)"

    return f"<pre>{escape_html(content)}</pre>"


def format_tool_entry(name: str, details: dict) -> str:
    """格式化单个工具条目

    Args:
        name: 工具名称
        details: 工具详情字典

    Returns:
        格式化后的工具条目（标题 + 代码块）
    """
    detail_lines = [f"{k}: {v}" for k, v in details.items() if v]
    content = "\n".join(detail_lines) if detail_lines else "无详情"

    return f"<b>{escape_html(name)}</b>\n{format_code_block(content)}"


def format_task_complete(data: dict) -> str:
    """格式化任务完成通知"""
    session_id = (data.get("session_id") or "unknown")[:8]
    stop_reason = data.get("stop_reason") or "unknown"
    output = data.get("output") or ""

    # 截断输出
    if output and len(output) > 500:
        output = output[:500] + "\n... (已截断)"

    lines = [
        "✅ <b>Claude Code 任务完成</b>",
        "",
        f"📌 Session: <code>{session_id}</code>",
        f"🔄 Stop reason: {stop_reason}",
    ]

    if output:
        lines.append("")
        lines.append("📝 <b>输出:</b>")
        lines.append(f"<pre>{escape_html(output)}</pre>")

    return "\n".join(lines)


def format_user_question(data: dict) -> str:
    """格式化用户询问通知"""
    session_id = data.get("session_id", "unknown")[:8]
    questions = data.get("questions", [])

    lines = [
        "❓ <b>Claude Code 需要你的输入</b>",
        "",
        f"📌 Session: <code>{session_id}</code>",
        "",
        "📝 问题详情:",
    ]

    for i, q in enumerate(questions, 1):
        question = q.get("question", "")
        header = q.get("header", "")
        options = q.get("options", [])
        multi_select = q.get("multi_select", False)

        # 构建问题标题
        lines.append("")
        lines.append(f"<b>问题 {i}:</b> {escape_html(question)}")

        # 构建代码块内容
        code_block_lines = []
        if header:
            code_block_lines.append(f"📋 {header}")
            code_block_lines.append("")

        if options:
            code_block_lines.append("选项:")
            for opt in options:
                label = opt.get("label", "")
                desc = opt.get("description", "")
                code_block_lines.append(f"  • {label} - {desc}")
            code_block_lines.append("")

        if multi_select:
            code_block_lines.append("☑️ 可多选")

        # 添加代码块
        if code_block_lines:
            content = "\n".join(code_block_lines).strip()
            lines.append(format_code_block(content, max_length=0))  # 禁用截断

    return "\n".join(lines)


def format_error(data: dict) -> str:
    """格式化错误通知"""
    session_id = data.get("session_id", "unknown")[:8]
    error = data.get("error", {})

    error_type = error.get("type", "unknown")
    message = error.get("message", "Unknown error")
    tool_name = error.get("tool_name")

    lines = [
        "❌ <b>Claude Code 执行出错</b>",
        "",
        f"📌 Session: <code>{session_id}</code>",
        f"🔴 Error type: {error_type}",
        "",
        "📝 错误详情:",
    ]

    # 构建代码块内容
    code_block_lines = [f"Message: {message}"]
    if tool_name:
        code_block_lines.append(f"Tool: {tool_name}")

    content = "\n".join(code_block_lines)
    lines.append(format_code_block(content))

    return "\n".join(lines)


def _extract_tool_details(name: str, details: dict) -> dict:
    """提取工具特定的详情信息

    Args:
        name: 工具名称
        details: 原始详情字典

    Returns:
        提取后的详情字典
    """
    extracted = {}

    if name == "Bash":
        if "command" in details:
            extracted["cmd"] = details["command"]
        if "description" in details:
            extracted["desc"] = details["description"]
    elif name == "Read":
        if "file_path" in details:
            extracted["file"] = details["file_path"].split("/")[-1]
        if "offset" in details or "limit" in details:
            offset = details.get("offset", "?")
            limit = details.get("limit", "?")
            if limit != "?" and offset != "?":
                extracted["lines"] = f"{offset}-{offset + limit}"
            else:
                extracted["lines"] = f"{offset}-?"
    elif name == "Write":
        if "file_path" in details:
            extracted["file"] = details["file_path"].split("/")[-1]
        if "content_preview" in details:
            extracted["preview"] = details["content_preview"]
    elif name == "Edit":
        if "file_path" in details:
            extracted["file"] = details["file_path"].split("/")[-1]
        if "old_string" in details:
            extracted["old"] = details["old_string"]
    elif name in ("Grep", "Glob"):
        if "pattern" in details:
            extracted["pattern"] = details["pattern"]
        if "path" in details:
            extracted["path"] = details["path"]
        if name == "Grep" and "output_mode" in details:
            extracted["mode"] = details["output_mode"]
    elif name == "Agent":
        if "subagent_type" in details:
            extracted["type"] = details["subagent_type"]
        if "description" in details:
            extracted["desc"] = details["description"]
    elif name == "WebSearch":
        if "query" in details:
            extracted["query"] = details["query"]
    elif name == "Task":
        if "description" in details:
            extracted["desc"] = details["description"]
    else:
        # Fallback: show file_path if available
        if "file_path" in details:
            extracted["file"] = details["file_path"].split("/")[-1]

    return extracted


def format_tool_use(data: dict) -> str:
    """格式化工具调用通知

    Args:
        data: 包含工具调用信息的字典

    Returns:
        格式化后的 Telegram 消息
    """
    session_id = data.get("session_id", "unknown")[:8]
    tools = data.get("tools", [])

    lines = [
        "🔧 <b>Claude Code 工具调用</b>",
        "",
        f"📌 Session: <code>{session_id}</code>",
        "",
        "📝 工具调用详情:",
    ]

    # 处理空工具列表
    if not tools:
        lines.append("")
        lines.append("无工具调用信息")
        return "\n".join(lines)

    # 格式化每个工具（最多5个）
    for tool in tools[:5]:
        name = tool.get("name", "unknown")
        details = tool.get("details", {})
        extracted_details = _extract_tool_details(name, details)

        lines.append("")
        lines.append(format_tool_entry(name, extracted_details))

    # 超出限制提示
    if len(tools) > 5:
        lines.append("")
        lines.append(f"• ... 还有 {len(tools) - 5} 个工具")

    return "\n".join(lines)


# ============================================================================
# 主循环
# ============================================================================


def process_event(line: str) -> Optional[str]:
    """
    处理单个事件

    Args:
        line: JSON 行

    Returns:
        格式化的消息，如果不需通知则返回 None
    """
    try:
        data = json.loads(line)
    except json.JSONDecodeError:
        return None

    status = data.get("status")

    if status == "TASK_COMPLETE" and Config.NOTIFY_ON_COMPLETE:
        return format_task_complete(data)
    elif status == "USER_QUESTION" and Config.NOTIFY_ON_USER_QUESTION:
        return format_user_question(data)
    elif status == "ERROR_STOP" and Config.NOTIFY_ON_ERROR:
        return format_error(data)
    elif status == "TOOL_USE" and Config.NOTIFY_ON_TOOL_USE:
        return format_tool_use(data)

    return None


def main():
    """主循环 - 从 stdin 读取 JSON 行并发送通知

    重构版本使用 Logger 类和 RetryHandler
    """
    # 初始化 Logger 和 RetryHandler
    logger = Logger(Config)
    retry_handler = RetryHandler(max_retries=Config.RETRY_COUNT, interval=Config.RETRY_INTERVAL)

    # 输出启动日志
    logger.log_startup(
        chat_id=Config.CHAT_ID or "未配置",
        proxy=Config.PROXY or "无",
        log_path=str(logger._log_path) if logger._log_path else None,
    )

    # 输出等待日志
    logger.log_waiting()

    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue

        try:
            data = json.loads(line)
        except json.JSONDecodeError:
            continue

        # 获取事件信息
        status = data.get("status", "")
        session_id = data.get("session_id", "unknown")

        # 处理不同事件类型
        message = None
        event_type = ""

        if status == "TASK_COMPLETE" and Config.NOTIFY_ON_COMPLETE:
            message = format_task_complete(data)
            event_type = "任务完成"
        elif status == "USER_QUESTION" and Config.NOTIFY_ON_USER_QUESTION:
            message = format_user_question(data)
            event_type = "用户询问"
        elif status == "ERROR_STOP" and Config.NOTIFY_ON_ERROR:
            message = format_error(data)
            event_type = "错误通知"
        elif status == "TOOL_USE" and Config.NOTIFY_ON_TOOL_USE:
            message = format_tool_use(data)
            event_type = "工具调用"

        if message and event_type:
            final_message = message  # Capture for closure

            # 使用重试机制发送
            def send_func():
                return send_telegram_message(final_message)

            final_event_type = event_type  # Capture for closure
            final_session_id = session_id  # Capture for closure

            def on_retry(attempt: int, error_msg: str) -> None:
                logger.log_retry(
                    event_type=final_event_type,
                    session_id=final_session_id,
                    error=error_msg,
                    attempt=attempt,
                    max_attempts=Config.RETRY_COUNT,
                )

            success, retry_count, last_error = retry_handler.execute_with_retry(send_func, on_retry=on_retry)

            if success:
                # 获取附加详情
                details = {}
                if status == "TASK_COMPLETE":
                    details["原因"] = data.get("stop_reason", "unknown")
                elif status == "ERROR_STOP":
                    error = data.get("error", {})
                    details["错误类型"] = error.get("type", "unknown")

                logger.log_success(
                    event_type=event_type,
                    session_id=session_id,
                    details=details,
                    retry_count=retry_count,
                )
            else:
                logger.log_failure(
                    event_type=event_type,
                    session_id=session_id,
                    error=last_error or "Unknown error",
                    retry_count=retry_count,
                )


if __name__ == "__main__":
    main()

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
import urllib.error
import urllib.request
from typing import Optional

# ============================================================================
# 配置 (可从环境变量覆盖)
# ============================================================================

BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")
PROXY = os.environ.get("TELEGRAM_PROXY", "http://127.0.0.1:7890")

# 通知开关 (可以通过环境变量控制)
NOTIFY_ON_COMPLETE = os.environ.get("NOTIFY_ON_COMPLETE", "true").lower() == "true"
NOTIFY_ON_USER_QUESTION = os.environ.get("NOTIFY_ON_USER_QUESTION", "true").lower() == "true"
NOTIFY_ON_ERROR = os.environ.get("NOTIFY_ON_ERROR", "true").lower() == "true"


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
    """
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    payload = {
        "chat_id": CHAT_ID,
        "text": text,
        "parse_mode": parse_mode,
    }

    data = json.dumps(payload).encode("utf-8")
    headers = {"Content-Type": "application/json"}

    # 设置代理
    if PROXY:
        handler = urllib.request.ProxyHandler({"http": PROXY, "https": PROXY})
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
                print(f"[ERROR] Telegram API error: {result}", file=sys.stderr)
                return False
    except urllib.error.URLError as e:
        print(f"[ERROR] Network error: {e}", file=sys.stderr)
        return False
    except Exception as e:
        print(f"[ERROR] Failed to send message: {e}", file=sys.stderr)
        return False


# ============================================================================
# 消息格式化
# ============================================================================


def escape_html(text: str) -> str:
    """转义 HTML 特殊字符"""
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def format_task_complete(data: dict) -> str:
    """格式化任务完成通知"""
    session_id = data.get("session_id", "unknown")[:8]
    stop_reason = data.get("stop_reason", "unknown")
    output = data.get("output", "")

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
    ]

    for i, q in enumerate(questions, 1):
        question = q.get("question", "")
        header = q.get("header", "")
        options = q.get("options", [])
        multi_select = q.get("multi_select", False)

        lines.append("")
        lines.append(f"<b>问题 {i}:</b> {escape_html(question)}")
        if header:
            lines.append(f"📋 {escape_html(header)}")

        if options:
            lines.append("<b>选项:</b>")
            for opt in options:
                label = opt.get("label", "")
                desc = opt.get("description", "")
                lines.append(f"  • {escape_html(label)} - {escape_html(desc)}")

        if multi_select:
            lines.append("☑️ 可多选")

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
        f"💬 Message: {escape_html(message)}",
    ]

    if tool_name:
        lines.append(f"🔧 Tool: {escape_html(tool_name)}")

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

    if status == "TASK_COMPLETE" and NOTIFY_ON_COMPLETE:
        return format_task_complete(data)
    elif status == "USER_QUESTION" and NOTIFY_ON_USER_QUESTION:
        return format_user_question(data)
    elif status == "ERROR_STOP" and NOTIFY_ON_ERROR:
        return format_error(data)

    return None


def main():
    """主循环 - 从 stdin 读取 JSON 行并发送通知"""
    print("[INFO] Telegram Notifier started", file=sys.stderr)
    print(f"[INFO] Chat ID: {CHAT_ID}", file=sys.stderr)
    print(f"[INFO] Proxy: {PROXY}", file=sys.stderr)
    print("[INFO] Waiting for events...", file=sys.stderr)

    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue

        message = process_event(line)
        if message:
            if send_telegram_message(message):
                print("[INFO] Notification sent", file=sys.stderr)
            else:
                print("[ERROR] Failed to send notification", file=sys.stderr)


if __name__ == "__main__":
    main()

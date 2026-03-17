#!/usr/bin/env python3
"""
Unit tests for notify_telegram.py

Tests cover:
- Config class
- Logger class
- RetryHandler class
- TelegramNotifier class
- Edge cases and integration
"""

import json
import os
import sys
import tempfile
import time
from io import StringIO
from pathlib import Path
from unittest import TestCase, main
from unittest.mock import patch

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))


# =============================================================================
# Task 1.2: Config 类单元测试
# =============================================================================


class TestConfig(TestCase):
    """Config 类的单元测试"""

    def setUp(self):
        """保存原始环境变量"""
        self.original_env = os.environ.copy()

    def tearDown(self):
        """恢复原始环境变量"""
        os.environ.clear()
        os.environ.update(self.original_env)

    def test_config_reads_bot_token(self):
        """测试读取 BOT_TOKEN"""
        os.environ["TELEGRAM_BOT_TOKEN"] = "test_token_123"
        os.environ["TELEGRAM_CHAT_ID"] = "test_chat_id"

        from notify_telegram import Config

        config = Config()

        self.assertEqual(config.BOT_TOKEN, "test_token_123")

    def test_config_reads_chat_id(self):
        """测试读取 CHAT_ID"""
        os.environ["TELEGRAM_BOT_TOKEN"] = "test_token"
        os.environ["TELEGRAM_CHAT_ID"] = "123456789"

        from notify_telegram import Config

        config = Config()

        self.assertEqual(config.CHAT_ID, "123456789")

    def test_config_reads_proxy_with_default(self):
        """测试读取 PROXY，有默认值"""
        os.environ["TELEGRAM_BOT_TOKEN"] = "test_token"
        os.environ["TELEGRAM_CHAT_ID"] = "test_chat"
        os.environ.pop("TELEGRAM_PROXY", None)

        from notify_telegram import Config

        config = Config()

        self.assertEqual(config.PROXY, "http://127.0.0.1:7890")

    def test_config_reads_custom_proxy(self):
        """测试读取自定义 PROXY"""
        os.environ["TELEGRAM_BOT_TOKEN"] = "test_token"
        os.environ["TELEGRAM_CHAT_ID"] = "test_chat"
        os.environ["TELEGRAM_PROXY"] = "http://custom:8080"

        from notify_telegram import Config

        config = Config()

        self.assertEqual(config.PROXY, "http://custom:8080")

    def test_config_reads_log_file(self):
        """测试读取 LOG_FILE 环境变量"""
        os.environ["TELEGRAM_BOT_TOKEN"] = "test_token"
        os.environ["TELEGRAM_CHAT_ID"] = "test_chat"
        os.environ["TELEGRAM_LOG_FILE"] = "/custom/path/notify.log"

        from notify_telegram import Config

        config = Config()

        self.assertEqual(config.LOG_FILE, "/custom/path/notify.log")

    def test_config_log_file_default_none(self):
        """测试 LOG_FILE 默认为 None"""
        os.environ["TELEGRAM_BOT_TOKEN"] = "test_token"
        os.environ["TELEGRAM_CHAT_ID"] = "test_chat"
        os.environ.pop("TELEGRAM_LOG_FILE", None)

        from notify_telegram import Config

        config = Config()

        self.assertIsNone(config.LOG_FILE)

    def test_config_reads_retry_count(self):
        """测试读取 RETRY_COUNT"""
        os.environ["TELEGRAM_BOT_TOKEN"] = "test_token"
        os.environ["TELEGRAM_CHAT_ID"] = "test_chat"
        os.environ["TELEGRAM_RETRY_COUNT"] = "5"

        from notify_telegram import Config

        config = Config()

        self.assertEqual(config.RETRY_COUNT, 5)

    def test_config_retry_count_default(self):
        """测试 RETRY_COUNT 默认值为 3"""
        os.environ["TELEGRAM_BOT_TOKEN"] = "test_token"
        os.environ["TELEGRAM_CHAT_ID"] = "test_chat"
        os.environ.pop("TELEGRAM_RETRY_COUNT", None)

        from notify_telegram import Config

        config = Config()

        self.assertEqual(config.RETRY_COUNT, 3)

    def test_config_reads_retry_interval(self):
        """测试读取 RETRY_INTERVAL"""
        os.environ["TELEGRAM_BOT_TOKEN"] = "test_token"
        os.environ["TELEGRAM_CHAT_ID"] = "test_chat"
        os.environ["TELEGRAM_RETRY_INTERVAL"] = "2"

        from notify_telegram import Config

        config = Config()

        self.assertEqual(config.RETRY_INTERVAL, 2)

    def test_config_retry_interval_default(self):
        """测试 RETRY_INTERVAL 默认值为 1"""
        os.environ["TELEGRAM_BOT_TOKEN"] = "test_token"
        os.environ["TELEGRAM_CHAT_ID"] = "test_chat"
        os.environ.pop("TELEGRAM_RETRY_INTERVAL", None)

        from notify_telegram import Config

        config = Config()

        self.assertEqual(config.RETRY_INTERVAL, 1)

    def test_config_notify_flags_default_true(self):
        """测试通知开关默认为 True"""
        os.environ["TELEGRAM_BOT_TOKEN"] = "test_token"
        os.environ["TELEGRAM_CHAT_ID"] = "test_chat"

        from notify_telegram import Config

        config = Config()

        self.assertTrue(config.NOTIFY_ON_COMPLETE)
        self.assertTrue(config.NOTIFY_ON_USER_QUESTION)
        self.assertTrue(config.NOTIFY_ON_ERROR)
        self.assertTrue(config.NOTIFY_ON_PENDING_PERMISSION)

    def test_config_notify_flags_can_be_disabled(self):
        """测试通知开关可以禁用"""
        os.environ["TELEGRAM_BOT_TOKEN"] = "test_token"
        os.environ["TELEGRAM_CHAT_ID"] = "test_chat"
        os.environ["NOTIFY_ON_COMPLETE"] = "false"
        os.environ["NOTIFY_ON_ERROR"] = "FALSE"

        from notify_telegram import Config

        config = Config()

        self.assertFalse(config.NOTIFY_ON_COMPLETE)
        self.assertFalse(config.NOTIFY_ON_ERROR)

    def test_config_missing_bot_token_raises_error(self):
        """测试缺失 BOT_TOKEN 时抛出错误"""
        os.environ.pop("TELEGRAM_BOT_TOKEN", None)
        os.environ["TELEGRAM_CHAT_ID"] = "test_chat"

        from notify_telegram import Config

        with self.assertRaises(ValueError) as context:
            Config()

        self.assertIn("TELEGRAM_BOT_TOKEN", str(context.exception))

    def test_config_missing_chat_id_raises_error(self):
        """测试缺失 CHAT_ID 时抛出错误"""
        os.environ["TELEGRAM_BOT_TOKEN"] = "test_token"
        os.environ.pop("TELEGRAM_CHAT_ID", None)

        from notify_telegram import Config

        with self.assertRaises(ValueError) as context:
            Config()

        self.assertIn("TELEGRAM_CHAT_ID", str(context.exception))


# =============================================================================
# Task 1.3: Logger 格式化单元测试
# =============================================================================


class TestLoggerFormatting(TestCase):
    """Logger 格式化的单元测试"""

    def setUp(self):
        """保存原始环境变量"""
        self.original_env = os.environ.copy()
        os.environ["TELEGRAM_BOT_TOKEN"] = "test_token"
        os.environ["TELEGRAM_CHAT_ID"] = "test_chat"

    def tearDown(self):
        """恢复原始环境变量"""
        os.environ.clear()
        os.environ.update(self.original_env)

    def test_timestamp_format(self):
        """测试时间戳格式为 %Y-%m-%d %H:%M:%S"""
        from notify_telegram import Config, Logger

        config = Config()
        logger = Logger(config)

        timestamp = logger._format_timestamp()

        # 格式应为 YYYY-MM-DD HH:MM:SS
        pattern = r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$"
        self.assertRegex(timestamp, pattern)

    def test_emoji_map_startup(self):
        """测试启动 Emoji 为 🚀"""
        from notify_telegram import Config, Logger

        config = Config()
        logger = Logger(config)

        self.assertEqual(logger._EMOJI_MAP["startup"], "🚀")

    def test_emoji_map_waiting(self):
        """测试等待状态 Emoji 为 ℹ️"""
        from notify_telegram import Config, Logger

        config = Config()
        logger = Logger(config)

        self.assertEqual(logger._EMOJI_MAP["waiting"], "ℹ️")

    def test_emoji_map_success(self):
        """测试成功 Emoji 为 ✅"""
        from notify_telegram import Config, Logger

        config = Config()
        logger = Logger(config)

        self.assertEqual(logger._EMOJI_MAP["success"], "✅")

    def test_emoji_map_retry(self):
        """测试重试 Emoji 为 ⚠️"""
        from notify_telegram import Config, Logger

        config = Config()
        logger = Logger(config)

        self.assertEqual(logger._EMOJI_MAP["retry"], "⚠️")

    def test_emoji_map_failure(self):
        """测试失败 Emoji 为 ❌"""
        from notify_telegram import Config, Logger

        config = Config()
        logger = Logger(config)

        self.assertEqual(logger._EMOJI_MAP["failure"], "❌")

    def test_format_main_message(self):
        """测试主消息格式化"""
        from notify_telegram import Config, Logger

        config = Config()
        logger = Logger(config)

        # Mock timestamp
        with patch.object(logger, "_format_timestamp", return_value="2026-03-12 14:30:15"):
            result = logger._format("startup", "Telegram Notifier 启动")

        # 应包含时间戳、emoji 和主消息
        self.assertIn("[2026-03-12 14:30:15]", result)
        self.assertIn("🚀", result)
        self.assertIn("Telegram Notifier 启动", result)

    def test_format_with_details(self):
        """测试带详细信息行的格式化"""
        from notify_telegram import Config, Logger

        config = Config()
        logger = Logger(config)

        details = {"Chat ID": "****6789", "Proxy": "http://127.0.0.1:7890"}

        with patch.object(logger, "_format_timestamp", return_value="2026-03-12 14:30:15"):
            result = logger._format("startup", "启动", details)

        # 应包含缩进的详细信息行
        self.assertIn("└─", result)
        self.assertIn("Chat ID: ****6789", result)
        self.assertIn("Proxy: http://127.0.0.1:7890", result)

    def test_stderr_output(self):
        """测试 stderr 输出"""
        from notify_telegram import Config, Logger

        config = Config()
        logger = Logger(config)

        # Capture stderr
        with patch("sys.stderr", new_callable=StringIO) as mock_stderr:
            with patch.object(logger, "_format_timestamp", return_value="2026-03-12 14:30:15"):
                logger._output("[2026-03-12 14:30:15] 🚀 Telegram Notifier 启动")

            output = mock_stderr.getvalue()

        self.assertIn("🚀 Telegram Notifier 启动", output)

    def test_log_startup_format(self):
        """测试启动日志格式"""
        from notify_telegram import Config, Logger

        config = Config()
        logger = Logger(config)

        with patch.object(logger, "_format_timestamp", return_value="2026-03-12 14:30:15"):
            with patch("sys.stderr", new_callable=StringIO) as mock_stderr:
                logger.log_startup("123456789", "http://127.0.0.1:7890", "/path/to/logs/notify.log")

                output = mock_stderr.getvalue()

        # 验证格式
        self.assertIn("🚀 Telegram Notifier 启动", output)
        self.assertIn("Chat ID: ****6789", output)  # 脱敏显示
        self.assertIn("Proxy: http://127.0.0.1:7890", output)
        self.assertIn("日志文件: /path/to/logs/notify.log", output)

    def test_log_waiting_format(self):
        """测试等待状态日志格式"""
        from notify_telegram import Config, Logger

        config = Config()
        logger = Logger(config)

        with patch.object(logger, "_format_timestamp", return_value="2026-03-12 14:30:15"):
            with patch("sys.stderr", new_callable=StringIO) as mock_stderr:
                logger.log_waiting()

                output = mock_stderr.getvalue()

        self.assertIn("ℹ️ 等待事件中...", output)

    def test_log_success_format(self):
        """测试成功日志格式"""
        from notify_telegram import Config, Logger

        config = Config()
        logger = Logger(config)

        with patch.object(logger, "_format_timestamp", return_value="2026-03-12 14:30:20"):
            with patch("sys.stderr", new_callable=StringIO) as mock_stderr:
                logger.log_success("任务完成", "abc12345", {"原因": "end_turn"})

                output = mock_stderr.getvalue()

        self.assertIn("✅ 通知发送成功", output)
        self.assertIn("类型: 任务完成", output)
        self.assertIn("Session: abc12345", output)

    def test_log_retry_format(self):
        """测试重试日志格式"""
        from notify_telegram import Config, Logger

        config = Config()
        logger = Logger(config)

        with patch.object(logger, "_format_timestamp", return_value="2026-03-12 14:30:21"):
            with patch("sys.stderr", new_callable=StringIO) as mock_stderr:
                logger.log_retry("用户询问", "def67890", "timeout", 1, 3)

                output = mock_stderr.getvalue()

        self.assertIn("⚠️ 发送失败 (重试 1/3)", output)
        self.assertIn("类型: 用户询问", output)
        self.assertIn("Session: def67890", output)
        self.assertIn("错误: timeout", output)

    def test_log_failure_format(self):
        """测试最终失败日志格式"""
        from notify_telegram import Config, Logger

        config = Config()
        logger = Logger(config)

        with patch.object(logger, "_format_timestamp", return_value="2026-03-12 14:30:23"):
            with patch("sys.stderr", new_callable=StringIO) as mock_stderr:
                logger.log_failure("用户询问", "def67890", "Connection refused", 3)

                output = mock_stderr.getvalue()

        self.assertIn("❌ 发送最终失败", output)
        self.assertIn("重试次数: 3", output)

    def test_chat_id_masking(self):
        """测试 Chat ID 脱敏显示（后4位）"""
        from notify_telegram import Config, Logger

        config = Config()
        logger = Logger(config)

        masked = logger._mask_chat_id("123456789")
        self.assertEqual(masked, "****6789")

    def test_chat_id_masking_short(self):
        """测试短 Chat ID 脱敏"""
        from notify_telegram import Config, Logger

        config = Config()
        logger = Logger(config)

        masked = logger._mask_chat_id("123")
        self.assertEqual(masked, "**3")  # 3字符ID：2个* + 最后1位


# =============================================================================
# Task 2.1: 文件路径解析单元测试
# =============================================================================


class TestLoggerFilePath(TestCase):
    """Logger 文件路径解析的单元测试"""

    def setUp(self):
        """保存原始环境变量"""
        self.original_env = os.environ.copy()
        os.environ["TELEGRAM_BOT_TOKEN"] = "test_token"
        os.environ["TELEGRAM_CHAT_ID"] = "test_chat"

        # 清除之前导入的模块
        if "notify_telegram" in sys.modules:
            del sys.modules["notify_telegram"]

    def tearDown(self):
        """恢复原始环境变量"""
        os.environ.clear()
        os.environ.update(self.original_env)

    def test_default_log_path_generation(self):
        """测试默认路径生成（脚本目录/logs/notify_YYYY-MM-DD.log）"""
        from datetime import datetime

        from notify_telegram import Config, Logger

        config = Config()
        logger = Logger(config)

        today = datetime.now().strftime("%Y-%m-%d")
        expected_name = f"notify_{today}.log"

        self.assertIsNotNone(logger._base_log_path)
        self.assertEqual(logger._base_log_path.name, expected_name)
        self.assertEqual(logger._base_log_path.parent.name, "logs")

    def test_tilde_expansion(self):
        """测试 ~ 展开支持"""
        from notify_telegram import Config, Logger

        os.environ["TELEGRAM_LOG_FILE"] = "~/custom_logs/notify.log"

        config = Config()
        logger = Logger(config)

        # ~ 应该被展开
        self.assertNotIn("~", str(logger._base_log_path))
        self.assertTrue(str(logger._base_log_path).startswith(str(Path.home())))

    def test_custom_log_path(self):
        """测试自定义路径（TELEGRAM_LOG_FILE）"""
        from notify_telegram import Config, Logger

        custom_path = "/tmp/custom_notify.log"
        os.environ["TELEGRAM_LOG_FILE"] = custom_path

        config = Config()
        logger = Logger(config)

        self.assertEqual(str(logger._base_log_path), custom_path)

    def test_directory_auto_creation(self):
        """测试目录自动创建"""
        from notify_telegram import Config, Logger

        with tempfile.TemporaryDirectory() as tmpdir:
            log_path = Path(tmpdir) / "subdir" / "notify.log"
            os.environ["TELEGRAM_LOG_FILE"] = str(log_path)

            config = Config()
            logger = Logger(config)

            # 写入一条日志触发目录创建
            with patch("sys.stderr", new_callable=StringIO):
                logger._output("[TEST] Trigger directory creation")

            # 目录应该被创建
            self.assertTrue(log_path.parent.exists())


# =============================================================================
# Task 2.2: 日志轮转单元测试
# =============================================================================


class TestLoggerRotation(TestCase):
    """Logger 日志轮转的单元测试"""

    def setUp(self):
        """保存原始环境变量"""
        self.original_env = os.environ.copy()
        os.environ["TELEGRAM_BOT_TOKEN"] = "test_token"
        os.environ["TELEGRAM_CHAT_ID"] = "test_chat"

        # 清除之前导入的模块
        if "notify_telegram" in sys.modules:
            del sys.modules["notify_telegram"]

    def tearDown(self):
        """恢复原始环境变量"""
        os.environ.clear()
        os.environ.update(self.original_env)

    def test_rotation_by_date(self):
        """测试按日期分割（日期变化检测）"""

        from notify_telegram import Config, Logger

        with tempfile.TemporaryDirectory() as tmpdir:
            log_path = Path(tmpdir) / "notify.log"
            os.environ["TELEGRAM_LOG_FILE"] = str(log_path)

            config = Config()
            logger = Logger(config)

            # 模拟日期变化
            logger._current_date = "2026-03-11"
            with patch.object(logger, "_format_timestamp", return_value="2026-03-12 10:00:00"):
                with patch("sys.stderr", new_callable=StringIO):
                    logger._check_rotation()

            # 日期变化后应该更新 current_date
            self.assertEqual(logger._current_date, "2026-03-12")

    def test_rotation_by_size(self):
        """测试按大小分割（10MB 阈值）"""
        from notify_telegram import Config, Logger

        with tempfile.TemporaryDirectory() as tmpdir:
            log_path = Path(tmpdir) / "notify.log"
            os.environ["TELEGRAM_LOG_FILE"] = str(log_path)

            config = Config()
            logger = Logger(config)

            # 创建一个正好 10MB 的文件
            with open(log_path, "w") as f:
                f.write("x" * (10 * 1024 * 1024))  # 正好 10MB

            # 写入更多数据应该触发轮转
            with patch("sys.stderr", new_callable=StringIO):
                logger._output("Test message that should trigger rotation")

            # 应该切换到新的轮转文件路径
            self.assertIn("_1", str(logger._current_log_path))

    def test_rotation_index_sequence(self):
        """测试序号追加（_1.log, _2.log）"""
        from notify_telegram import Config, Logger

        with tempfile.TemporaryDirectory() as tmpdir:
            log_path = Path(tmpdir) / "notify.log"
            os.environ["TELEGRAM_LOG_FILE"] = str(log_path)

            config = Config()
            logger = Logger(config)

            # 创建已存在的轮转文件
            (Path(tmpdir) / "notify_1.log").touch()
            (Path(tmpdir) / "notify_2.log").touch()

            # 下一个序号应该是 3
            next_index = logger._get_next_rotation_index()
            self.assertEqual(next_index, 3)

    def test_file_handle_switching(self):
        """测试文件句柄正确切换"""
        from notify_telegram import Config, Logger

        with tempfile.TemporaryDirectory() as tmpdir:
            log_path = Path(tmpdir) / "notify.log"
            os.environ["TELEGRAM_LOG_FILE"] = str(log_path)

            config = Config()
            logger = Logger(config)

            # 初始时没有文件句柄
            self.assertIsNone(logger._file_handle)

            # 写入后应该打开文件句柄
            with patch("sys.stderr", new_callable=StringIO):
                logger._output("First message")

            self.assertIsNotNone(logger._file_handle)

            # 关闭后句柄应该为 None
            logger.close()
            self.assertIsNone(logger._file_handle)


# =============================================================================
# Task 3.1: RetryHandler 单元测试
# =============================================================================


class TestRetryHandler(TestCase):
    """RetryHandler 的单元测试"""

    def setUp(self):
        """保存原始环境变量"""
        self.original_env = os.environ.copy()
        os.environ["TELEGRAM_BOT_TOKEN"] = "test_token"
        os.environ["TELEGRAM_CHAT_ID"] = "test_chat"

        # 清除之前导入的模块
        if "notify_telegram" in sys.modules:
            del sys.modules["notify_telegram"]

    def tearDown(self):
        """恢复原始环境变量"""
        os.environ.clear()
        os.environ.update(self.original_env)

    def test_first_attempt_success(self):
        """测试首次成功（不重试）"""
        from notify_telegram import RetryHandler

        handler = RetryHandler(max_retries=3, interval=0.01)

        # 模拟首次成功
        success, retry_count, last_error = handler.execute_with_retry(func=lambda: (True, None))

        self.assertTrue(success)
        self.assertEqual(retry_count, 0)
        self.assertIsNone(last_error)

    def test_retry_then_success(self):
        """测试重试后成功"""
        from notify_telegram import RetryHandler

        handler = RetryHandler(max_retries=3, interval=0.01)

        # 模拟：第一次失败，第二次成功
        call_count = [0]

        def mock_func():
            call_count[0] += 1
            if call_count[0] == 1:
                return (False, "First error")
            return (True, None)

        success, retry_count, last_error = handler.execute_with_retry(func=mock_func)

        self.assertTrue(success)
        self.assertEqual(retry_count, 1)
        self.assertIsNone(last_error)

    def test_all_retries_fail(self):
        """测试所有重试失败"""
        from notify_telegram import RetryHandler

        handler = RetryHandler(max_retries=3, interval=0.01)

        # 模拟：始终失败
        success, retry_count, last_error = handler.execute_with_retry(func=lambda: (False, "Always fails"))

        self.assertFalse(success)
        self.assertEqual(retry_count, 3)
        self.assertEqual(last_error, "Always fails")

    def test_retry_interval(self):
        """测试重试间隔正确"""
        from notify_telegram import RetryHandler

        handler = RetryHandler(max_retries=2, interval=0.1)

        start_time = time.time()
        handler.execute_with_retry(func=lambda: (False, "error"))
        elapsed = time.time() - start_time

        # 2次重试，间隔0.1秒，总时间应该 >= 0.2秒
        self.assertGreaterEqual(elapsed, 0.2)

    def test_retry_callback_called(self):
        """测试回调函数正确调用"""
        from notify_telegram import RetryHandler

        handler = RetryHandler(max_retries=3, interval=0.01)

        retry_calls = []

        def on_retry(attempt: int, error: str):
            retry_calls.append((attempt, error))

        handler.execute_with_retry(
            func=lambda: (False, "error"),
            on_retry=on_retry,
        )

        # 应该有3次重试回调
        self.assertEqual(len(retry_calls), 3)
        self.assertEqual(retry_calls[0], (1, "error"))
        self.assertEqual(retry_calls[1], (2, "error"))
        self.assertEqual(retry_calls[2], (3, "error"))

    def test_return_value_format(self):
        """测试返回值格式（success, retry_count, last_error）"""
        from notify_telegram import RetryHandler

        handler = RetryHandler(max_retries=3, interval=0.01)

        result = handler.execute_with_retry(func=lambda: (False, "test error"))

        # 验证返回值类型
        self.assertIsInstance(result, tuple)
        self.assertEqual(len(result), 3)
        success, retry_count, last_error = result
        self.assertIsInstance(success, bool)
        self.assertIsInstance(retry_count, int)
        self.assertIsInstance(last_error, (str, type(None)))


# =============================================================================
# Task 4.1: TelegramNotifier 集成测试
# =============================================================================


class TestTelegramNotifier(TestCase):
    """TelegramNotifier 集成测试"""

    def setUp(self):
        """保存原始环境变量"""
        self.original_env = os.environ.copy()
        os.environ["TELEGRAM_BOT_TOKEN"] = "test_token"
        os.environ["TELEGRAM_CHAT_ID"] = "test_chat"

        # 清除之前导入的模块
        if "notify_telegram" in sys.modules:
            del sys.modules["notify_telegram"]

    def tearDown(self):
        """恢复原始环境变量"""
        os.environ.clear()
        os.environ.update(self.original_env)

    def test_process_event_task_complete(self):
        """测试处理 TASK_COMPLETE 事件"""
        from notify_telegram import Config, Logger, RetryHandler, TelegramNotifier

        config = Config()
        logger = Logger(config)
        retry_handler = RetryHandler(max_retries=1, interval=0.01)
        notifier = TelegramNotifier(config, logger, retry_handler)

        event = json.dumps({"status": "TASK_COMPLETE", "session_id": "abc12345def", "stop_reason": "end_turn"})

        message = notifier.process_event(event)
        self.assertIsNotNone(message)
        self.assertIn("任务完成", message)

    def test_process_event_user_question(self):
        """测试处理 USER_QUESTION 事件"""
        from notify_telegram import Config, Logger, RetryHandler, TelegramNotifier

        config = Config()
        logger = Logger(config)
        retry_handler = RetryHandler(max_retries=1, interval=0.01)
        notifier = TelegramNotifier(config, logger, retry_handler)

        event = json.dumps(
            {
                "status": "USER_QUESTION",
                "session_id": "abc12345def",
                "questions": [{"question": "Continue?", "header": "Confirm"}],
            }
        )

        message = notifier.process_event(event)
        self.assertIsNotNone(message)
        self.assertIn("需要你的输入", message)

    def test_process_event_error_stop(self):
        """测试处理 ERROR_STOP 事件"""
        from notify_telegram import Config, Logger, RetryHandler, TelegramNotifier

        config = Config()
        logger = Logger(config)
        retry_handler = RetryHandler(max_retries=1, interval=0.01)
        notifier = TelegramNotifier(config, logger, retry_handler)

        event = json.dumps(
            {
                "status": "ERROR_STOP",
                "session_id": "abc12345def",
                "error": {"type": "network", "message": "Connection failed"},
            }
        )

        message = notifier.process_event(event)
        self.assertIsNotNone(message)
        self.assertIn("执行出错", message)

    def test_process_event_pending_permission(self):
        """测试处理 PENDING_PERMISSION 事件"""
        from notify_telegram import Config, Logger, RetryHandler, TelegramNotifier

        config = Config()
        logger = Logger(config)
        retry_handler = RetryHandler(max_retries=1, interval=0.01)
        notifier = TelegramNotifier(config, logger, retry_handler)

        event = json.dumps(
            {
                "status": "PENDING_PERMISSION",
                "session_id": "abc12345def",
                "tools": [{"name": "Bash", "description": "Run command"}],
            }
        )

        message = notifier.process_event(event)
        self.assertIsNotNone(message)
        self.assertIn("等待权限确认", message)

    def test_process_event_disabled_notification(self):
        """测试禁用通知时不返回消息"""
        from notify_telegram import Config, Logger, RetryHandler, TelegramNotifier

        os.environ["NOTIFY_ON_COMPLETE"] = "false"
        config = Config()
        logger = Logger(config)
        retry_handler = RetryHandler(max_retries=1, interval=0.01)
        notifier = TelegramNotifier(config, logger, retry_handler)

        event = json.dumps({"status": "TASK_COMPLETE", "session_id": "abc12345def"})

        message = notifier.process_event(event)
        self.assertIsNone(message)


# =============================================================================
# Task 4.2: 边界情况单元测试
# =============================================================================


class TestEdgeCases(TestCase):
    """边界情况测试"""

    def setUp(self):
        """保存原始环境变量"""
        self.original_env = os.environ.copy()
        os.environ["TELEGRAM_BOT_TOKEN"] = "test_token"
        os.environ["TELEGRAM_CHAT_ID"] = "test_chat"

        # 清除之前导入的模块
        if "notify_telegram" in sys.modules:
            del sys.modules["notify_telegram"]

    def tearDown(self):
        """恢复原始环境变量"""
        os.environ.clear()
        os.environ.update(self.original_env)

    def test_error_message_truncation(self):
        """测试 EC-004: 超长错误消息截断（500字符）"""
        from notify_telegram import Config, Logger

        config = Config()
        logger = Logger(config)

        # 创建一个超长错误消息
        long_error = "x" * 600
        truncated = logger._truncate_error(long_error)

        self.assertEqual(len(truncated), 503)  # 500 + "..."
        self.assertTrue(truncated.endswith("..."))

    def test_special_char_escaping(self):
        """测试 EC-005: 特殊字符转义（换行符等）"""
        from notify_telegram import Config, Logger

        config = Config()
        logger = Logger(config)

        text_with_newlines = "Error:\nLine1\nLine2"
        escaped = logger._escape_special_chars(text_with_newlines)

        self.assertNotIn("\n", escaped)
        self.assertIn("\\n", escaped)

    def test_permission_denied_fallback(self):
        """测试 EC-001: 日志目录权限不足（降级处理）"""
        from notify_telegram import Config, Logger

        # 使用一个不可能创建的路径
        os.environ["TELEGRAM_LOG_FILE"] = "/root/cannot_write_here/notify.log"
        config = Config()
        logger = Logger(config)

        # 应该降级为仅 stderr，不抛出异常
        with patch("sys.stderr", new_callable=StringIO):
            logger._output("[TEST] This should fallback to stderr only")

        self.assertFalse(logger._file_enabled)

    def test_html_escaping(self):
        """测试 HTML 特殊字符转义"""
        from notify_telegram import Config, Logger, RetryHandler, TelegramNotifier

        config = Config()
        logger = Logger(config)
        retry_handler = RetryHandler(max_retries=1, interval=0.01)
        notifier = TelegramNotifier(config, logger, retry_handler)

        text = "<script>alert('xss')</script>"
        escaped = notifier.escape_html(text)

        self.assertEqual(escaped, "&lt;script&gt;alert('xss')&lt;/script&gt;")


if __name__ == "__main__":
    main()

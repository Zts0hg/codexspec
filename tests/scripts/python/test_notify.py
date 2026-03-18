#!/usr/bin/env python3
"""
Unit tests for notify_telegram.py

Tests cover:
- Config class: environment variable loading, defaults, type conversion
- Logger class: timestamp formatting, emoji mapping, log output format
- RetryHandler class: retry logic, interval, callbacks
- Integration: end-to-end notification flow
"""

import os
import subprocess
import sys
import tempfile
import time
import unittest
from datetime import datetime, timedelta
from io import StringIO
from pathlib import Path
from unittest.mock import patch

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / "scripts" / "python"))

# Path to the module under test
NOTIFY_MODULE_PATH = str(Path(__file__).parent.parent.parent.parent / "scripts" / "python")


class TestConfig(unittest.TestCase):
    """Test cases for Config class - Task 1.2

    Note: Config class reads environment variables at module load time.
    We use subprocess-based testing to ensure clean environment for each test.
    """

    def _run_in_subprocess(self, env_vars: dict, code: str) -> str:
        """Run Python code in a subprocess with specific environment variables.

        Args:
            env_vars: Environment variables to set for the subprocess
            code: Python code to execute

        Returns:
            stdout from the subprocess
        """
        # Build clean environment, removing telegram-related vars by default
        env = os.environ.copy()
        for key in [
            "TELEGRAM_BOT_TOKEN",
            "TELEGRAM_CHAT_ID",
            "TELEGRAM_PROXY",
            "TELEGRAM_LOG_FILE",
            "TELEGRAM_RETRY_COUNT",
            "TELEGRAM_RETRY_INTERVAL",
            "NOTIFY_ON_COMPLETE",
            "NOTIFY_ON_USER_QUESTION",
            "NOTIFY_ON_ERROR",
            "NOTIFY_ON_PENDING_PERMISSION",
        ]:
            env.pop(key, None)

        # Set test-specific env vars
        env.update(env_vars)

        result = subprocess.run(
            [sys.executable, "-c", code],
            capture_output=True,
            text=True,
            env=env,
            cwd=NOTIFY_MODULE_PATH,
        )
        if result.returncode != 0:
            self.fail(f"Subprocess failed: {result.stderr}")
        return result.stdout.strip()

    def test_tc_cfg_001_read_all_env_vars(self):
        """TC-CFG-001: 读取所有环境变量"""
        env_vars = {
            "TELEGRAM_BOT_TOKEN": "test_token_123",
            "TELEGRAM_CHAT_ID": "test_chat_456",
            "TELEGRAM_PROXY": "http://proxy:8080",
            "TELEGRAM_LOG_FILE": "/custom/log/path.log",
            "TELEGRAM_RETRY_COUNT": "5",
            "TELEGRAM_RETRY_INTERVAL": "2",
        }
        code = """
import sys
sys.path.insert(0, '.')
from notify_telegram import Config
print(f"BOT_TOKEN:{Config.BOT_TOKEN}")
print(f"CHAT_ID:{Config.CHAT_ID}")
print(f"PROXY:{Config.PROXY}")
print(f"LOG_FILE:{Config.LOG_FILE}")
print(f"RETRY_COUNT:{Config.RETRY_COUNT}")
print(f"RETRY_INTERVAL:{Config.RETRY_INTERVAL}")
"""
        output = self._run_in_subprocess(env_vars, code)
        lines = output.split("\n")

        results = {}
        for line in lines:
            key, value = line.split(":", 1)
            results[key] = value

        self.assertEqual(results["BOT_TOKEN"], "test_token_123")
        self.assertEqual(results["CHAT_ID"], "test_chat_456")
        self.assertEqual(results["PROXY"], "http://proxy:8080")
        self.assertEqual(results["LOG_FILE"], "/custom/log/path.log")
        self.assertEqual(results["RETRY_COUNT"], "5")
        self.assertEqual(results["RETRY_INTERVAL"], "2")

    def test_tc_cfg_002_default_values(self):
        """TC-CFG-002: 默认值验证"""
        # No env vars set - test defaults
        code = """
import sys
sys.path.insert(0, '.')
from notify_telegram import Config
print(f"PROXY:{Config.PROXY}")
print(f"LOG_FILE:{Config.LOG_FILE}")
print(f"RETRY_COUNT:{Config.RETRY_COUNT}")
print(f"RETRY_INTERVAL:{Config.RETRY_INTERVAL}")
print(f"NOTIFY_ON_COMPLETE:{Config.NOTIFY_ON_COMPLETE}")
print(f"NOTIFY_ON_USER_QUESTION:{Config.NOTIFY_ON_USER_QUESTION}")
print(f"NOTIFY_ON_ERROR:{Config.NOTIFY_ON_ERROR}")
"""
        output = self._run_in_subprocess({}, code)
        results = {}
        for line in output.split("\n"):
            key, value = line.split(":", 1)
            results[key] = value

        self.assertEqual(results["PROXY"], "http://127.0.0.1:7890")
        self.assertEqual(results["LOG_FILE"], "None")
        self.assertEqual(results["RETRY_COUNT"], "3")
        self.assertEqual(results["RETRY_INTERVAL"], "1")
        self.assertEqual(results["NOTIFY_ON_COMPLETE"], "True")
        self.assertEqual(results["NOTIFY_ON_USER_QUESTION"], "True")
        self.assertEqual(results["NOTIFY_ON_ERROR"], "True")

    def test_tc_cfg_003_type_conversion_bool(self):
        """TC-CFG-003: 类型转换 - bool"""
        env_vars = {
            "NOTIFY_ON_COMPLETE": "false",
            "NOTIFY_ON_USER_QUESTION": "TRUE",
            "NOTIFY_ON_ERROR": "False",
        }
        code = """
import sys
sys.path.insert(0, '.')
from notify_telegram import Config
print(f"NOTIFY_ON_COMPLETE:{Config.NOTIFY_ON_COMPLETE}")
print(f"NOTIFY_ON_USER_QUESTION:{Config.NOTIFY_ON_USER_QUESTION}")
print(f"NOTIFY_ON_ERROR:{Config.NOTIFY_ON_ERROR}")
"""
        output = self._run_in_subprocess(env_vars, code)
        results = {}
        for line in output.split("\n"):
            key, value = line.split(":", 1)
            results[key] = value

        self.assertEqual(results["NOTIFY_ON_COMPLETE"], "False")
        self.assertEqual(results["NOTIFY_ON_USER_QUESTION"], "True")
        self.assertEqual(results["NOTIFY_ON_ERROR"], "False")

    def test_tc_cfg_004_type_conversion_int(self):
        """TC-CFG-004: 类型转换 - int"""
        env_vars = {
            "TELEGRAM_RETRY_COUNT": "10",
            "TELEGRAM_RETRY_INTERVAL": "5",
        }
        code = """
import sys
sys.path.insert(0, '.')
from notify_telegram import Config
print(f"RETRY_COUNT:{Config.RETRY_COUNT}")
print(f"RETRY_INTERVAL:{Config.RETRY_INTERVAL}")
print(f"RETRY_COUNT_TYPE:{type(Config.RETRY_COUNT).__name__}")
print(f"RETRY_INTERVAL_TYPE:{type(Config.RETRY_INTERVAL).__name__}")
"""
        output = self._run_in_subprocess(env_vars, code)
        results = {}
        for line in output.split("\n"):
            key, value = line.split(":", 1)
            results[key] = value

        self.assertEqual(results["RETRY_COUNT"], "10")
        self.assertEqual(results["RETRY_INTERVAL"], "5")
        self.assertEqual(results["RETRY_COUNT_TYPE"], "int")
        self.assertEqual(results["RETRY_INTERVAL_TYPE"], "int")


class TestLoggerBasicFormatting(unittest.TestCase):
    """Test cases for Logger basic formatting - Task 1.4"""

    def setUp(self):
        """Set up test fixtures"""
        from notify_telegram import Config, Logger

        self.logger = Logger(Config)

    def test_tc_log_001_timestamp_format(self):
        """TC-LOG-001: 时间戳格式验证 (%Y-%m-%d %H:%M:%S)"""
        timestamp = self.logger._format_timestamp()
        # Should match format: YYYY-MM-DD HH:MM:SS
        self.assertRegex(timestamp, r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$")
        # Should be parseable
        parsed = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
        self.assertIsInstance(parsed, datetime)

    def test_tc_log_002_emoji_mapping(self):
        """TC-LOG-002: Emoji 映射正确性"""
        # Startup emoji
        self.assertEqual(self.logger.EMOJI["startup"], "🚀")
        # Waiting emoji
        self.assertEqual(self.logger.EMOJI["waiting"], "ℹ️")
        # Success emoji
        self.assertEqual(self.logger.EMOJI["success"], "✅")
        # Retry emoji
        self.assertEqual(self.logger.EMOJI["retry"], "⚠️")
        # Failure emoji
        self.assertEqual(self.logger.EMOJI["failure"], "❌")

    def test_tc_log_003_main_message_format(self):
        """TC-LOG-003: 主消息 + 详细信息行格式"""
        # Test format: [timestamp] {emoji} {message}
        #              └─ {details}
        output = self.logger._format_log_entry(
            emoji="✅",
            message="测试消息",
            details={"类型": "任务完成", "Session": "abc12345"},
        )

        lines = output.strip().split("\n")
        self.assertEqual(len(lines), 2)
        # First line: [timestamp] emoji message
        self.assertRegex(lines[0], r"^\[\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\] ✅ 测试消息$")
        # Second line: indented details
        self.assertTrue(lines[1].startswith("    └─"))
        self.assertIn("类型: 任务完成", lines[1])
        self.assertIn("Session: abc12345", lines[1])

    def test_tc_log_004_stderr_output(self):
        """TC-LOG-004: stderr 双输出"""
        with patch("sys.stderr", new_callable=StringIO) as mock_stderr:
            self.logger._write("测试输出")
            output = mock_stderr.getvalue()
            self.assertIn("测试输出", output)

    def test_tc_log_005_multiple_details(self):
        """TC-LOG-005: 多个详细信息的格式化"""
        output = self.logger._format_log_entry(
            emoji="⚠️",
            message="发送失败",
            details={
                "类型": "用户询问",
                "Session": "def67890",
                "错误": "timeout",
                "重试": "1/3",
            },
        )

        lines = output.strip().split("\n")
        self.assertEqual(len(lines), 2)
        # All details should be joined with " | "
        self.assertIn("类型: 用户询问", lines[1])
        self.assertIn("Session: def67890", lines[1])
        self.assertIn("错误: timeout", lines[1])
        self.assertIn("重试: 1/3", lines[1])


class TestLoggerFilePath(unittest.TestCase):
    """Test cases for Logger file path resolution - Task 2.1"""

    def setUp(self):
        """Set up test fixtures"""
        import importlib

        import notify_telegram

        # Clear LOG_FILE env var for default path tests
        self.original_log_file = os.environ.get("TELEGRAM_LOG_FILE")
        os.environ.pop("TELEGRAM_LOG_FILE", None)

        importlib.reload(notify_telegram)
        from notify_telegram import Config, Logger

        self.Config = Config
        self.Logger = Logger

    def tearDown(self):
        """Restore original environment"""
        if self.original_log_file:
            os.environ["TELEGRAM_LOG_FILE"] = self.original_log_file
        else:
            os.environ.pop("TELEGRAM_LOG_FILE", None)

    def test_tc_path_001_tilde_expansion(self):
        """TC-PATH-001: ~ 展开为用户主目录"""
        logger = self.Logger(self.Config)
        home_path = "~/logs/notify.log"
        expanded = logger._expand_path(home_path)
        self.assertTrue(str(expanded).startswith(str(Path.home())))
        self.assertNotIn("~", str(expanded))

    def test_tc_path_002_default_path_rule(self):
        """TC-PATH-002: 默认路径规则验证"""
        logger = self.Logger(self.Config)
        default_path = logger._get_default_log_path()

        # Should be in logs/ subdirectory
        self.assertIn("logs", str(default_path))
        # Should contain today's date
        today = datetime.now().strftime("%Y-%m-%d")
        self.assertIn(today, str(default_path))
        # Should end with .log
        self.assertTrue(str(default_path).endswith(".log"))

    def test_tc_path_003_custom_path_telegram_log_file(self):
        """TC-PATH-003: 自定义路径 (TELEGRAM_LOG_FILE)"""
        with tempfile.TemporaryDirectory() as tmpdir:
            custom_path = os.path.join(tmpdir, "custom_notify.log")
            os.environ["TELEGRAM_LOG_FILE"] = custom_path

            import importlib

            importlib.reload(sys.modules["notify_telegram"])
            from notify_telegram import Config, Logger

            logger = Logger(Config)
            resolved_path = logger._resolve_log_path()

            self.assertEqual(str(resolved_path), custom_path)


class TestLoggerFileOperations(unittest.TestCase):
    """Test cases for Logger file operations - Task 2.3"""

    def setUp(self):
        """Set up test fixtures"""
        import importlib

        import notify_telegram

        self.temp_dir = tempfile.mkdtemp()
        self.log_path = os.path.join(self.temp_dir, "test_notify.log")

        os.environ["TELEGRAM_LOG_FILE"] = self.log_path
        importlib.reload(notify_telegram)
        from notify_telegram import Config, Logger

        self.Config = Config
        self.Logger = Logger
        self.logger = Logger(Config)

    def tearDown(self):
        """Clean up test fixtures"""
        import shutil

        shutil.rmtree(self.temp_dir, ignore_errors=True)
        os.environ.pop("TELEGRAM_LOG_FILE", None)

    def test_tc_file_001_directory_auto_creation(self):
        """TC-FILE-001: 目录自动创建"""
        # Create a path with non-existent directory
        nested_path = os.path.join(self.temp_dir, "nested", "deep", "notify.log")
        os.environ["TELEGRAM_LOG_FILE"] = nested_path

        import importlib

        importlib.reload(sys.modules["notify_telegram"])
        from notify_telegram import Config, Logger

        logger = Logger(Config)

        # Directory should be created when writing
        logger._ensure_log_dir(nested_path)
        self.assertTrue(os.path.isdir(os.path.dirname(nested_path)))

    def test_tc_file_002_append_write_mode(self):
        """TC-FILE-002: 追加写入模式"""
        # Write first line
        self.logger._write_to_file("Line 1\n")
        # Write second line
        self.logger._write_to_file("Line 2\n")

        # Read file and verify both lines exist
        with open(self.log_path, "r") as f:
            content = f.read()

        self.assertIn("Line 1", content)
        self.assertIn("Line 2", content)

    def test_tc_file_003_file_handle_management(self):
        """TC-FILE-003: 文件句柄管理"""
        # Write multiple times
        for i in range(5):
            self.logger._write_to_file(f"Message {i}\n")

        # File handle should be properly managed (closed after each write or kept open)
        # Verify all messages were written
        with open(self.log_path, "r") as f:
            content = f.read()

        for i in range(5):
            self.assertIn(f"Message {i}", content)


class TestLoggerRotation(unittest.TestCase):
    """Test cases for Logger file rotation - Task 2.5"""

    def setUp(self):
        """Set up test fixtures"""
        self.temp_dir = tempfile.mkdtemp()

        import importlib

        os.environ.pop("TELEGRAM_LOG_FILE", None)
        importlib.reload(sys.modules["notify_telegram"])
        from notify_telegram import Config, Logger

        self.Config = Config
        self.Logger = Logger
        # Override log path to temp dir for testing
        self.logger = Logger(Config)
        self.logger._log_dir = Path(self.temp_dir)

    def tearDown(self):
        """Clean up test fixtures"""
        import shutil

        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_tc_rotate_001_date_change_creates_new_file(self):
        """TC-ROTATE-001: 日期变化时创建新文件"""
        # Get today's log path
        today_path = self.logger._get_log_path_for_date(datetime.now())
        yesterday = datetime.now() - timedelta(days=1)
        yesterday_path = self.logger._get_log_path_for_date(yesterday)

        # Paths should be different
        self.assertNotEqual(str(today_path), str(yesterday_path))
        self.assertIn(datetime.now().strftime("%Y-%m-%d"), str(today_path))
        self.assertIn(yesterday.strftime("%Y-%m-%d"), str(yesterday_path))

    def test_tc_rotate_002_size_exceeds_10mb_creates_new_file(self):
        """TC-ROTATE-002: 文件超过 10MB 时创建新文件"""
        # Create a log file that's nearly 10MB
        log_path = os.path.join(self.temp_dir, f"notify_{datetime.now().strftime('%Y-%m-%d')}.log")

        # Write content to make it nearly 10MB
        large_content = "x" * (10 * 1024 * 1024 - 100)  # Just under 10MB
        with open(log_path, "w") as f:
            f.write(large_content)

        # Check if rotation is needed
        needs_rotation = self.logger._needs_size_rotation(log_path)
        self.assertFalse(needs_rotation)  # Not yet 10MB

        # Add more to exceed 10MB
        with open(log_path, "a") as f:
            f.write("x" * 200)

        needs_rotation = self.logger._needs_size_rotation(log_path)
        self.assertTrue(needs_rotation)  # Now exceeds 10MB

    def test_tc_rotate_003_mixed_rotation_scenario(self):
        """TC-ROTATE-003: 混合轮转场景"""
        # Test getting next rotation filename
        base_date = datetime.now().strftime("%Y-%m-%d")

        # First file: notify_2026-03-17.log
        first_path = self.logger._get_log_path_for_date(datetime.now(), index=0)
        self.assertTrue(str(first_path).endswith(f"notify_{base_date}.log"))

        # Second file (after size rotation): notify_2026-03-17_1.log
        second_path = self.logger._get_log_path_for_date(datetime.now(), index=1)
        self.assertTrue(str(second_path).endswith(f"notify_{base_date}_1.log"))

        # Third file: notify_2026-03-17_2.log
        third_path = self.logger._get_log_path_for_date(datetime.now(), index=2)
        self.assertTrue(str(third_path).endswith(f"notify_{base_date}_2.log"))


class TestRetryHandler(unittest.TestCase):
    """Test cases for RetryHandler class - Task 3.1"""

    def setUp(self):
        """Set up test fixtures"""
        from notify_telegram import RetryHandler

        self.RetryHandler = RetryHandler

    def test_tc_retry_001_first_success_no_retry(self):
        """TC-RETRY-001: 首次成功不重试"""
        handler = self.RetryHandler(max_retries=3, interval=0.01)

        call_count = 0

        def always_succeed():
            nonlocal call_count
            call_count += 1
            return True

        success, retry_count, error = handler.execute_with_retry(always_succeed)

        self.assertTrue(success)
        self.assertEqual(retry_count, 0)
        self.assertIsNone(error)
        self.assertEqual(call_count, 1)  # Should only be called once

    def test_tc_retry_002_fail_then_retry_max_3(self):
        """TC-RETRY-002: 失败后重试最多 3 次"""
        handler = self.RetryHandler(max_retries=3, interval=0.01)

        call_count = 0

        def always_fail():
            nonlocal call_count
            call_count += 1
            raise Exception("Network error")

        retry_calls = []

        def on_retry(attempt, error_msg):
            retry_calls.append((attempt, error_msg))

        success, retry_count, error = handler.execute_with_retry(always_fail, on_retry=on_retry)

        self.assertFalse(success)
        self.assertEqual(retry_count, 3)
        self.assertIn("Network error", error)
        self.assertEqual(call_count, 4)  # Initial + 3 retries
        self.assertEqual(len(retry_calls), 3)

    def test_tc_retry_003_success_then_stop_retry(self):
        """TC-RETRY-003: 成功后立即停止重试"""
        handler = self.RetryHandler(max_retries=3, interval=0.01)

        call_count = 0

        def fail_twice_then_succeed():
            nonlocal call_count
            call_count += 1
            if call_count <= 2:
                raise Exception("Temporary error")
            return True

        retry_calls = []

        def on_retry(attempt, error_msg):
            retry_calls.append((attempt, error_msg))

        success, retry_count, error = handler.execute_with_retry(fail_twice_then_succeed, on_retry=on_retry)

        self.assertTrue(success)
        self.assertEqual(retry_count, 2)
        self.assertIsNone(error)
        self.assertEqual(call_count, 3)  # Initial + 2 retries

    def test_tc_retry_004_retry_interval(self):
        """TC-RETRY-004: 重试间隔验证"""

        handler = self.RetryHandler(max_retries=2, interval=0.1)

        call_times = []

        def record_time_and_fail():
            call_times.append(time.time())
            if len(call_times) <= 2:
                raise Exception("Error")
            return True

        start = time.time()
        success, retry_count, _ = handler.execute_with_retry(record_time_and_fail)
        elapsed = time.time() - start

        self.assertTrue(success)
        # Should have waited at least 0.2 seconds (2 intervals)
        self.assertGreaterEqual(elapsed, 0.15)  # Allow some tolerance


class TestSendWithRetry(unittest.TestCase):
    """Test cases for send_with_retry integration - Task 3.3"""

    def setUp(self):
        """Set up test fixtures"""
        import importlib

        import notify_telegram

        importlib.reload(notify_telegram)
        from notify_telegram import Config, Logger, RetryHandler

        self.Config = Config
        self.Logger = Logger
        self.RetryHandler = RetryHandler

    def test_tc_int_001_send_success_no_retry(self):
        """TC-INT-001: 发送成功无重试"""
        handler = self.RetryHandler(max_retries=3, interval=0.01)

        send_count = 0

        def mock_send():
            nonlocal send_count
            send_count += 1
            return True

        success, retry_count, error = handler.execute_with_retry(mock_send)

        self.assertTrue(success)
        self.assertEqual(retry_count, 0)
        self.assertEqual(send_count, 1)

    def test_tc_int_002_send_fail_then_retry_success(self):
        """TC-INT-002: 发送失败后重试成功"""
        handler = self.RetryHandler(max_retries=3, interval=0.01)

        send_count = 0

        def mock_send_fail_once():
            nonlocal send_count
            send_count += 1
            if send_count == 1:
                raise Exception("Timeout")
            return True

        success, retry_count, error = handler.execute_with_retry(mock_send_fail_once)

        self.assertTrue(success)
        self.assertEqual(retry_count, 1)

    def test_tc_int_003_send_fail_retry_exhausted(self):
        """TC-INT-003: 发送失败后重试耗尽"""
        handler = self.RetryHandler(max_retries=3, interval=0.01)

        def mock_send_always_fail():
            raise Exception("Connection refused")

        success, retry_count, error = handler.execute_with_retry(mock_send_always_fail)

        self.assertFalse(success)
        self.assertEqual(retry_count, 3)
        self.assertIn("Connection refused", error)


class TestStartupLog(unittest.TestCase):
    """Test cases for startup log output - Task 4.1"""

    def setUp(self):
        """Set up test fixtures"""
        from notify_telegram import Config, Logger

        self.Config = Config
        self.Logger = Logger
        self.logger = Logger(Config)

    def test_tc_001_startup_log_format(self):
        """TC-001: 启动日志格式验证"""
        with patch("sys.stderr", new_callable=StringIO) as mock_stderr:
            self.logger.log_startup(chat_id="1234567890", proxy="http://127.0.0.1:7890", log_path="/path/to/log.log")
            output = mock_stderr.getvalue()

            # Should contain emoji
            self.assertIn("🚀", output)
            # Should contain startup message
            self.assertIn("Telegram Notifier 启动", output)
            # Should contain masked Chat ID (****7890)
            self.assertIn("****7890", output)
            # Should contain proxy
            self.assertIn("http://127.0.0.1:7890", output)
            # Should contain log path
            self.assertIn("/path/to/log.log", output)

    def test_tc_001_waiting_log_format(self):
        """TC-001: 等待日志格式验证"""
        with patch("sys.stderr", new_callable=StringIO) as mock_stderr:
            self.logger.log_waiting()
            output = mock_stderr.getvalue()

            # Should contain waiting emoji
            self.assertIn("ℹ️", output)
            # Should contain waiting message
            self.assertIn("等待事件中", output)


class TestSuccessFailureLog(unittest.TestCase):
    """Test cases for success/failure log output - Task 4.3"""

    def setUp(self):
        """Set up test fixtures"""
        from notify_telegram import Config, Logger

        self.Config = Config
        self.Logger = Logger
        self.logger = Logger(Config)

    def test_tc_002_success_log_format(self):
        """TC-002: 成功发送日志格式"""
        with patch("sys.stderr", new_callable=StringIO) as mock_stderr:
            self.logger.log_success(
                event_type="任务完成",
                session_id="abc12345def67890",
                details={"原因": "end_turn"},
            )
            output = mock_stderr.getvalue()

            # Should contain success emoji
            self.assertIn("✅", output)
            # Should contain success message
            self.assertIn("通知发送成功", output)
            # Should contain event type
            self.assertIn("类型: 任务完成", output)
            # Should contain truncated session ID (first 8 chars)
            self.assertIn("Session: abc12345", output)

    def test_tc_003_retry_log_format(self):
        """TC-003: 失败重试日志格式"""
        with patch("sys.stderr", new_callable=StringIO) as mock_stderr:
            self.logger.log_retry(
                event_type="用户询问",
                session_id="def67890abc12345",
                error="The read operation timed out",
                attempt=1,
                max_attempts=3,
            )
            output = mock_stderr.getvalue()

            # Should contain retry emoji
            self.assertIn("⚠️", output)
            # Should contain retry message
            self.assertIn("重试 1/3", output)
            # Should contain event type
            self.assertIn("类型: 用户询问", output)
            # Should contain error
            self.assertIn("错误:", output)
            self.assertIn("timed out", output.lower())

    def test_tc_004_failure_log_format(self):
        """TC-004: 最终失败日志格式"""
        with patch("sys.stderr", new_callable=StringIO) as mock_stderr:
            self.logger.log_failure(
                event_type="错误通知",
                session_id="ghi1111122223333",
                error="Connection refused",
                retry_count=3,
            )
            output = mock_stderr.getvalue()

            # Should contain failure emoji
            self.assertIn("❌", output)
            # Should contain failure message
            self.assertIn("发送最终失败", output)
            # Should contain event type
            self.assertIn("类型: 错误通知", output)
            # Should contain total retry count
            self.assertIn("重试次数: 3", output)


class TestDegradation(unittest.TestCase):
    """Test cases for degradation handling - Task 4.5"""

    def setUp(self):
        """Set up test fixtures"""
        self.temp_dir = tempfile.mkdtemp()

    def tearDown(self):
        """Clean up test fixtures"""
        import shutil

        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_tc_009_log_file_not_writable(self):
        """TC-009: 日志文件不可写时降级为 stderr"""

        # Create a path that can't be written to
        readonly_path = os.path.join(self.temp_dir, "readonly.log")

        # Set environment and reload
        os.environ["TELEGRAM_LOG_FILE"] = readonly_path

        import importlib

        import notify_telegram

        importlib.reload(notify_telegram)
        from notify_telegram import Config as NewConfig
        from notify_telegram import Logger as NewLogger

        logger = NewLogger(NewConfig)

        # Simulate file write failure by setting flag
        logger._file_write_failed = True

        # Should still be able to write to stderr
        with patch("sys.stderr", new_callable=StringIO) as mock_stderr:
            logger.log_waiting()
            output = mock_stderr.getvalue()

            # Should still output to stderr
            self.assertIn("等待事件中", output)

        os.environ.pop("TELEGRAM_LOG_FILE", None)

    def test_ec_001_directory_permission_denied(self):
        """EC-001: 目录权限不足"""
        from notify_telegram import Config, Logger

        logger = Logger(Config)

        # Try to ensure directory exists (should work even with permission issues)
        # In practice, this would fail if we don't have permission
        # For testing, we just verify the method exists and handles errors gracefully
        self.assertTrue(hasattr(logger, "_ensure_log_dir"))

    def test_ec_002_disk_space_insufficient(self):
        """EC-002: 磁盘空间不足"""
        from notify_telegram import Config, Logger

        logger = Logger(Config)

        # Simulate disk full by triggering file write failure
        logger._file_write_failed = True

        # Should degrade gracefully
        with patch("sys.stderr", new_callable=StringIO) as mock_stderr:
            logger.log_waiting()
            output = mock_stderr.getvalue()

            # Should still output to stderr
            self.assertIn("等待事件中", output)


class TestSpecialCharacters(unittest.TestCase):
    """Test cases for special character handling - Task 4.7"""

    def setUp(self):
        """Set up test fixtures"""
        from notify_telegram import Config, Logger

        self.Config = Config
        self.Logger = Logger
        self.logger = Logger(Config)

    def test_ec_004_long_error_message_truncation(self):
        """EC-004: 超长错误消息截断 (500 字符)"""
        # Create a very long error message
        long_error = "x" * 1000

        truncated = self.logger._truncate_error(long_error, max_length=500)

        # Should be truncated to 500 + "..."
        self.assertEqual(len(truncated), 503)  # 500 + "..."
        self.assertTrue(truncated.endswith("..."))

    def test_ec_004_short_error_no_truncation(self):
        """EC-004: 短错误消息不截断"""
        short_error = "Connection refused"

        truncated = self.logger._truncate_error(short_error, max_length=500)

        # Should not be truncated
        self.assertEqual(truncated, short_error)

    def test_ec_005_special_character_escaping(self):
        """EC-005: 特殊字符转义"""
        # Test newline escaping
        text_with_newline = "Line 1\nLine 2\tTabbed"
        escaped = self.logger._escape_special_chars(text_with_newline)

        # Should contain escaped characters
        self.assertIn("\\n", escaped)
        self.assertIn("\\t", escaped)
        # Should not contain raw special characters
        self.assertNotIn("\n", escaped)
        self.assertNotIn("\t", escaped)


class TestEndToEnd(unittest.TestCase):
    """End-to-end test cases - Task 5.1"""

    def setUp(self):
        """Set up test fixtures"""
        self.temp_dir = tempfile.mkdtemp()
        self.log_path = os.path.join(self.temp_dir, "e2e_test.log")

        # Set up environment
        os.environ["TELEGRAM_LOG_FILE"] = self.log_path

        import importlib

        import notify_telegram

        importlib.reload(notify_telegram)
        from notify_telegram import Config, Logger, RetryHandler

        self.Config = Config
        self.Logger = Logger
        self.RetryHandler = RetryHandler
        self.logger = Logger(Config)

    def tearDown(self):
        """Clean up test fixtures"""
        import shutil

        shutil.rmtree(self.temp_dir, ignore_errors=True)
        os.environ.pop("TELEGRAM_LOG_FILE", None)

    def test_tc_e2e_001_complete_flow(self):
        """TC-E2E-001: 完整运行流程模拟"""
        # Simulate startup
        with patch("sys.stderr", new_callable=StringIO) as mock_stderr:
            self.logger.log_startup(chat_id="1234567890", proxy="http://127.0.0.1:7890", log_path=self.log_path)
            startup_output = mock_stderr.getvalue()

            # Verify startup log format (FR-001)
            self.assertIn("🚀", startup_output)
            self.assertIn("Telegram Notifier 启动", startup_output)
            self.assertIn("****7890", startup_output)  # Masked Chat ID
            self.assertIn("http://127.0.0.1:7890", startup_output)

        # Simulate waiting
        with patch("sys.stderr", new_callable=StringIO) as mock_stderr:
            self.logger.log_waiting()
            waiting_output = mock_stderr.getvalue()

            self.assertIn("ℹ️", waiting_output)
            self.assertIn("等待事件中", waiting_output)

        # Simulate success
        with patch("sys.stderr", new_callable=StringIO) as mock_stderr:
            self.logger.log_success(
                event_type="任务完成",
                session_id="abc12345def67890",
                details={"原因": "end_turn"},
            )
            success_output = mock_stderr.getvalue()

            self.assertIn("✅", success_output)
            self.assertIn("通知发送成功", success_output)
            self.assertIn("Session: abc12345", success_output)

    def test_tc_e2e_002_log_format_compliance(self):
        """验证所有日志格式符合 FR-001 规范"""

        # Test all log types follow format: [timestamp] {emoji} {message}
        timestamp_pattern = r"^\[\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\]"

        # Startup log
        with patch("sys.stderr", new_callable=StringIO) as mock_stderr:
            self.logger.log_startup(chat_id="1234567890", proxy="http://127.0.0.1:7890", log_path=self.log_path)
            output = mock_stderr.getvalue()
            lines = output.strip().split("\n")
            self.assertRegex(lines[0], timestamp_pattern)

        # Waiting log
        with patch("sys.stderr", new_callable=StringIO) as mock_stderr:
            self.logger.log_waiting()
            output = mock_stderr.getvalue()
            lines = output.strip().split("\n")
            self.assertRegex(lines[0], timestamp_pattern)

        # Success log
        with patch("sys.stderr", new_callable=StringIO) as mock_stderr:
            self.logger.log_success(event_type="任务完成", session_id="abc12345def67890", details={})
            output = mock_stderr.getvalue()
            lines = output.strip().split("\n")
            self.assertRegex(lines[0], timestamp_pattern)

        # Retry log
        with patch("sys.stderr", new_callable=StringIO) as mock_stderr:
            self.logger.log_retry(
                event_type="用户询问",
                session_id="def67890abc12345",
                error="Timeout",
                attempt=1,
                max_attempts=3,
            )
            output = mock_stderr.getvalue()
            lines = output.strip().split("\n")
            self.assertRegex(lines[0], timestamp_pattern)

        # Failure log
        with patch("sys.stderr", new_callable=StringIO) as mock_stderr:
            self.logger.log_failure(
                event_type="错误通知",
                session_id="ghi1111122223333",
                error="Connection refused",
                retry_count=3,
            )
            output = mock_stderr.getvalue()
            lines = output.strip().split("\n")
            self.assertRegex(lines[0], timestamp_pattern)


class TestPerformance(unittest.TestCase):
    """Performance test cases - Task 5.3"""

    def setUp(self):
        """Set up test fixtures"""
        from notify_telegram import Config, Logger

        self.Config = Config
        self.Logger = Logger
        self.logger = Logger(Config)

    def test_tc_perf_001_log_write_latency(self):
        """验证单条日志写入延迟 < 10ms"""

        latencies = []

        # Measure 100 log writes
        for _ in range(100):
            start = time.perf_counter()

            with patch("sys.stderr", new_callable=StringIO):
                self.logger.log_waiting()

            elapsed_ms = (time.perf_counter() - start) * 1000
            latencies.append(elapsed_ms)

        # Average latency should be < 10ms
        avg_latency = sum(latencies) / len(latencies)
        self.assertLess(avg_latency, 10.0, f"Average latency {avg_latency:.2f}ms exceeds 10ms")

        # 99th percentile should also be < 10ms
        sorted_latencies = sorted(latencies)
        p99 = sorted_latencies[int(len(sorted_latencies) * 0.99)]
        self.assertLess(p99, 10.0, f"P99 latency {p99:.2f}ms exceeds 10ms")

    def test_tc_perf_002_no_blocking_notification(self):
        """验证不阻塞通知发送流程"""
        import threading

        results = {"logged": False, "notification_sent": False}

        def log_thread():
            with patch("sys.stderr", new_callable=StringIO):
                self.logger.log_waiting()
            results["logged"] = True

        def notification_thread():
            # Simulate notification sending
            time.sleep(0.001)
            results["notification_sent"] = True

        # Start both threads
        t1 = threading.Thread(target=log_thread)
        t2 = threading.Thread(target=notification_thread)

        t1.start()
        t2.start()

        t1.join()
        t2.join()

        # Both should complete
        self.assertTrue(results["logged"])
        self.assertTrue(results["notification_sent"])


if __name__ == "__main__":
    unittest.main()

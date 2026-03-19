#!/usr/bin/env python3
"""
Unit tests for notify_telegram.py message formatting functions
"""

import sys
from pathlib import Path

# Add scripts directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / "scripts" / "python"))

from notify_telegram import (
    format_code_block,
    format_error,
    format_tool_entry,
    format_tool_use,
    format_user_question,
)


class TestFormatCodeBlock:
    """测试 format_code_block() 辅助函数"""

    def test_normal_content(self):
        """测试正常内容格式化"""
        result = format_code_block("hello world")
        assert result == "<pre>hello world</pre>"

    def test_empty_content(self):
        """测试空内容"""
        result = format_code_block("")
        assert result == "<pre></pre>"

    def test_truncation(self):
        """测试超长内容截断"""
        long_content = "a" * 600
        result = format_code_block(long_content, max_length=500)
        assert "已截断" in result
        assert len(result) < len(long_content) + 50

    def test_no_truncation(self):
        """测试禁用截断"""
        long_content = "a" * 600
        result = format_code_block(long_content, max_length=0)
        assert "已截断" not in result

    def test_html_escape(self):
        """测试 HTML 转义"""
        result = format_code_block("<script>alert('xss')</script>")
        assert "&lt;script&gt;" in result
        assert "<script>" not in result


class TestFormatToolEntry:
    """测试 format_tool_entry() 辅助函数"""

    def test_normal_details(self):
        """测试正常详情格式化"""
        details = {"cmd": "git status", "desc": "Show status"}
        result = format_tool_entry("Bash", details)
        assert "<b>Bash</b>" in result
        assert "<pre>" in result
        assert "cmd: git status" in result

    def test_empty_details(self):
        """测试空详情"""
        result = format_tool_entry("Unknown", {})
        assert "<b>Unknown</b>" in result
        assert "无详情" in result

    def test_special_characters(self):
        """测试特殊字符转义"""
        details = {"cmd": "echo '<test>'"}
        result = format_tool_entry("Bash", details)
        assert "&lt;test&gt;" in result


class TestFormatToolUse:
    """测试 format_tool_use() 重构"""

    def test_single_tool(self):
        """TC-001: 单工具消息格式"""
        data = {
            "session_id": "b477a17c123456",
            "tools": [{"name": "Bash", "details": {"command": "git status", "description": "Show status"}}],
        }
        result = format_tool_use(data)
        assert "🔧 <b>Claude Code 工具调用</b>" in result
        assert "Session: <code>b477a17c</code>" in result
        assert "📝 工具调用详情:" in result
        assert "<b>Bash</b>" in result
        assert "<pre>" in result

    def test_multiple_tools(self):
        """TC-002: 多工具消息格式"""
        data = {
            "session_id": "b477a17c123456",
            "tools": [
                {"name": "Bash", "details": {"command": "git status"}},
                {"name": "Read", "details": {"file_path": "/path/to/file.py"}},
                {"name": "Write", "details": {"file_path": "/path/to/output.py"}},
            ],
        }
        result = format_tool_use(data)
        # 每个工具都应该有独立的代码块
        assert result.count("<pre>") == 3
        assert result.count("<b>Bash</b>") == 1
        assert result.count("<b>Read</b>") == 1
        assert result.count("<b>Write</b>") == 1

    def test_exceed_limit(self):
        """TC-003: 超过 5 个工具限制"""
        tools = [{"name": f"Tool{i}", "details": {}} for i in range(7)]
        data = {"session_id": "test1234", "tools": tools}
        result = format_tool_use(data)
        assert "还有 2 个工具" in result
        assert result.count("<b>Tool") == 5  # 只显示前5个

    def test_empty_tools(self):
        """Edge Case 1: 空工具列表"""
        data = {"session_id": "test1234", "tools": []}
        result = format_tool_use(data)
        assert "无工具调用信息" in result

    def test_missing_fields(self):
        """Edge Case 2: 缺失字段"""
        data = {
            "session_id": "test1234",
            "tools": [
                {"name": "Bash", "details": {}},  # 没有 command 或 description
            ],
        }
        result = format_tool_use(data)
        assert "<b>Bash</b>" in result
        assert "无详情" in result


class TestFormatUserQuestion:
    """测试 format_user_question() 优化"""

    def test_single_question(self):
        """TC-004: 单问题格式"""
        data = {
            "session_id": "b477a17c123456",
            "questions": [{"question": "选择认证方式?", "header": "Auth", "options": [], "multi_select": False}],
        }
        result = format_user_question(data)
        assert "❓ <b>Claude Code 需要你的输入</b>" in result
        assert "📝 问题详情:" in result
        assert "<b>问题 1:</b>" in result

    def test_multiple_options(self):
        """TC-005: 多选项格式"""
        data = {
            "session_id": "b477a17c123456",
            "questions": [
                {
                    "question": "选择认证方式?",
                    "header": "Auth method",
                    "options": [
                        {"label": "OAuth", "description": "OAuth 2.0"},
                        {"label": "JWT", "description": "JWT Token"},
                    ],
                    "multi_select": True,
                }
            ],
        }
        result = format_user_question(data)
        assert "<pre>" in result
        assert "OAuth" in result
        assert "JWT" in result
        assert "可多选" in result

    def test_multiple_questions(self):
        """测试多问题场景"""
        data = {
            "session_id": "test1234",
            "questions": [
                {"question": "问题1?", "header": "", "options": [], "multi_select": False},
                {"question": "问题2?", "header": "", "options": [], "multi_select": False},
            ],
        }
        result = format_user_question(data)
        assert "问题 1:" in result
        assert "问题 2:" in result

    def test_no_options(self):
        """测试无选项场景"""
        data = {
            "session_id": "test1234",
            "questions": [{"question": "请输入名称?", "header": "Name", "options": [], "multi_select": False}],
        }
        result = format_user_question(data)
        assert "Name" in result
        assert "选项" not in result


class TestFormatError:
    """测试 format_error() 优化"""

    def test_error_format(self):
        """TC-006: 错误消息格式"""
        data = {
            "session_id": "b477a17c123456",
            "error": {"type": "tool_error", "message": "File not found", "tool_name": "Read"},
        }
        result = format_error(data)
        assert "❌ <b>Claude Code 执行出错</b>" in result
        assert "Session: <code>b477a17c</code>" in result
        assert "Error type: tool_error" in result
        assert "📝 错误详情:" in result
        assert "<pre>" in result
        assert "File not found" in result
        assert "Tool: Read" in result

    def test_with_tool_name(self):
        """测试包含工具名场景"""
        data = {
            "session_id": "test1234",
            "error": {"type": "exec_error", "message": "Command failed", "tool_name": "Bash"},
        }
        result = format_error(data)
        assert "Tool: Bash" in result

    def test_without_tool_name(self):
        """测试不包含工具名场景"""
        data = {"session_id": "test1234", "error": {"type": "unknown", "message": "Something went wrong"}}
        result = format_error(data)
        assert "Tool:" not in result
        assert "Something went wrong" in result


class TestIntegration:
    """集成测试"""

    def test_message_structure(self):
        """测试消息结构完整性"""
        data = {"session_id": "b477a17c123456", "tools": [{"name": "Bash", "details": {"command": "test"}}]}
        result = format_tool_use(data)

        # 验证消息结构
        assert "🔧" in result  # emoji
        assert "<b>" in result  # bold
        assert "<code>" in result  # code
        assert "<pre>" in result  # code block


if __name__ == "__main__":
    # Run all tests
    test_classes = [
        TestFormatCodeBlock(),
        TestFormatToolEntry(),
        TestFormatToolUse(),
        TestFormatUserQuestion(),
        TestFormatError(),
        TestIntegration(),
    ]

    passed = 0
    failed = 0

    for test_class in test_classes:
        for method_name in dir(test_class):
            if method_name.startswith("test_"):
                try:
                    getattr(test_class, method_name)()
                    passed += 1
                except AssertionError as e:
                    print(f"FAILED: {test_class.__class__.__name__}.{method_name}: {e}")
                    failed += 1
                except Exception as e:
                    print(f"ERROR: {test_class.__class__.__name__}.{method_name}: {e}")
                    failed += 1

    print(f"\n{'=' * 50}")
    print(f"Tests passed: {passed}")
    print(f"Tests failed: {failed}")
    print(f"{'=' * 50}")

    sys.exit(0 if failed == 0 else 1)

#!/usr/bin/env python3
# ruff: noqa: E501
"""
Real Message Fixtures for Testing

This file contains extracted real messages from Claude Code JSONL files.
These are used as static test data to avoid depending on the real environment.

Generated: 2026-03-18T14:11:31.429766
"""

# Message samples categorized by type
REAL_MESSAGES = {
    "STREAMING": [
        # Sample 1
        {
            "id": "msg_2026021619072891fe346d2ca942d5",
            "type": "message",
            "role": "assistant",
            "model": "glm-5",
            "content": [
                {
                    "type": "thinking",
                    "thinking": "The user wants me to port the spec-kit project's constitution command to the current codexspec project's constitution command. Let me first understand what needs to be done:\n\n1. I need to read the current constitution command template in codexspec\n2. I need to understand the spec-kit version they provided\n3. I need to update the codexspec constitution command to incorporate the features from spec-kit\n\nLet me first read the current constitution template in codexspec to understand what exists.",
                    "signature": "",
                },
            ],
            "stop_reason": None,
            "stop_sequence": None,
            "usage": {
                "input_tokens": 0,
                "output_tokens": 0,
            },
        },
        # Sample 2
        {
            "id": "msg_2026021619072891fe346d2ca942d5",
            "type": "message",
            "role": "assistant",
            "model": "glm-5",
            "content": [
                {
                    "type": "text",
                    "text": "Let me first read the current constitution command template in the codexspec project to understand what exists.",
                },
            ],
            "stop_reason": None,
            "stop_sequence": None,
            "usage": {
                "input_tokens": 0,
                "output_tokens": 0,
            },
        },
        # Sample 3
        {
            "id": "msg_2026021619072891fe346d2ca942d5",
            "type": "message",
            "role": "assistant",
            "model": "glm-5",
            "content": [
                {
                    "type": "tool_use",
                    "id": "call_8002e74fdc6047a3bb421b62",
                    "name": "Read",
                    "input": {
                        "file_path": "/Users/xiaoming/code/codexspec/templates/commands/constitution.md",
                    },
                },
            ],
            "stop_reason": None,
            "stop_sequence": None,
            "usage": {
                "input_tokens": 0,
                "output_tokens": 0,
            },
        },
        # Sample 4
        {
            "id": "msg_2026022222182748e6afe03e3142cf",
            "type": "message",
            "role": "assistant",
            "model": "glm-5",
            "content": [
                {
                    "type": "thinking",
                    "thinking": "用户想要为 codexspec 项目中的脚本（包括 shell 和 powershell）添加自动化测试。让我先了解一下当前项目中脚本的结构和现有的测试情况。\n\n根据 CLAUDE.md 中的信息：\n- Bash 脚本位于 `scripts/bash/`\n- PowerShell 脚本位于 `scripts/powershell/`\n- 脚本测试应该在 `tests/scripts/bash/` 和 `tests/scripts/powershell/`\n\n让我先探索一下当前的脚本和测试结构。",
                    "signature": "",
                },
            ],
            "stop_reason": None,
            "stop_sequence": None,
            "usage": {
                "input_tokens": 0,
                "output_tokens": 0,
            },
        },
        # Sample 5
        {
            "id": "msg_2026022222182748e6afe03e3142cf",
            "type": "message",
            "role": "assistant",
            "model": "glm-5",
            "content": [
                {
                    "type": "text",
                    "text": "我来先了解一下当前项目中脚本的结构和现有测试情况。",
                },
            ],
            "stop_reason": None,
            "stop_sequence": None,
            "usage": {
                "input_tokens": 0,
                "output_tokens": 0,
            },
        },
    ],
    "TOOL_USE": [
        # Sample 1
        {
            "id": "msg_202603181258597070de4fc6ce41bd",
            "type": "message",
            "role": "assistant",
            "model": "glm-5",
            "content": [
                {
                    "type": "tool_use",
                    "id": "call_0dd09f94ab7647c6ac477225",
                    "name": "Read",
                    "input": {
                        "file_path": "/Users/xiaoming/code/codexspec/scripts/python/claude_monitor.py",
                    },
                },
            ],
            "stop_reason": "tool_use",
            "stop_sequence": None,
            "usage": {
                "input_tokens": 32954,
                "cache_creation_input_tokens": 0,
                "cache_read_input_tokens": 512,
                "output_tokens": 185,
                "server_tool_use": {
                    "web_search_requests": 0,
                    "web_fetch_requests": 0,
                },
                "service_tier": "standard",
                "cache_creation": {
                    "ephemeral_1h_input_tokens": 0,
                    "ephemeral_5m_input_tokens": 0,
                },
                "inference_geo": "",
                "iterations": [],
                "speed": "standard",
            },
        },
        # Sample 2
        {
            "id": "msg_2026031812591478f8f9d736ec4d89",
            "type": "message",
            "role": "assistant",
            "model": "glm-5",
            "content": [
                {
                    "type": "tool_use",
                    "id": "call_9756881386d5484abdb3fa15",
                    "name": "Edit",
                    "input": {
                        "replace_all": False,
                        "file_path": "/Users/xiaoming/code/codexspec/scripts/python/claude_monitor.py",
                        "old_string": '    def start(self) -> bool:\n        """Start notify_telegram.py subprocess."""\n        try:\n            self._process = subprocess.Popen(\n                ["uv", "run", "python3", "-m", "notify_telegram"],',
                        "new_string": '    def start(self) -> bool:\n        """Start notify_telegram.py subprocess."""\n        try:\n            # Get the path to notify_telegram.py (same directory as this script)\n            notify_script = Path(__file__).parent / "notify_telegram.py"\n            self._process = subprocess.Popen(\n                ["uv", "run", "python3", str(notify_script)],',
                    },
                },
            ],
            "stop_reason": "tool_use",
            "stop_sequence": None,
            "usage": {
                "input_tokens": 30012,
                "cache_creation_input_tokens": 0,
                "cache_read_input_tokens": 19456,
                "output_tokens": 322,
                "server_tool_use": {
                    "web_search_requests": 0,
                    "web_fetch_requests": 0,
                },
                "service_tier": "standard",
                "cache_creation": {
                    "ephemeral_1h_input_tokens": 0,
                    "ephemeral_5m_input_tokens": 0,
                },
                "inference_geo": "",
                "iterations": [],
                "speed": "standard",
            },
        },
        # Sample 3
        {
            "id": "msg_2026031812593869e94bccd7cb4f5a",
            "type": "message",
            "role": "assistant",
            "model": "glm-5",
            "content": [
                {
                    "type": "tool_use",
                    "id": "call_746cba949f3845b8a309d3eb",
                    "name": "Read",
                    "input": {
                        "file_path": "/Users/xiaoming/code/codexspec/scripts/python/claude_monitor.py",
                        "offset": 933,
                        "limit": 25,
                    },
                },
            ],
            "stop_reason": "tool_use",
            "stop_sequence": None,
            "usage": {
                "input_tokens": 417,
                "cache_creation_input_tokens": 0,
                "cache_read_input_tokens": 49408,
                "output_tokens": 75,
                "server_tool_use": {
                    "web_search_requests": 0,
                    "web_fetch_requests": 0,
                },
                "service_tier": "standard",
                "cache_creation": {
                    "ephemeral_1h_input_tokens": 0,
                    "ephemeral_5m_input_tokens": 0,
                },
                "inference_geo": "",
                "iterations": [],
                "speed": "standard",
            },
        },
        # Sample 4
        {
            "id": "msg_20260302113647643ec810b66b4099",
            "type": "message",
            "role": "assistant",
            "model": "glm-5",
            "content": [
                {
                    "type": "tool_use",
                    "id": "call_edc9b4e56ff94e72b965c9bb",
                    "name": "Agent",
                    "input": {
                        "subagent_type": "Explore",
                        "prompt": "Explore the CodexSpec codebase to understand the constitution compliance feature implementation:\n\n1. Find the `_get_compliance_section_content()` function and see what content it returns\n2. Find the `prepend_compliance_section()` function and understand how it prepends content\n3. Look at how the compliance section is structured - what does it start with?\n4. Check if there are any tests related to this compliance section feature\n\nFocus on files in `src/codexspec/` directory, particularly `__init__.py`.",
                        "description": "Explore compliance section implementation",
                    },
                },
            ],
            "stop_reason": "tool_use",
            "stop_sequence": None,
            "usage": {
                "input_tokens": 30395,
                "cache_creation_input_tokens": 0,
                "cache_read_input_tokens": 1472,
                "output_tokens": 306,
                "server_tool_use": {
                    "web_search_requests": 0,
                    "web_fetch_requests": 0,
                },
                "service_tier": "standard",
                "cache_creation": {
                    "ephemeral_1h_input_tokens": 0,
                    "ephemeral_5m_input_tokens": 0,
                },
                "inference_geo": "",
                "iterations": [],
                "speed": "standard",
            },
        },
        # Sample 5
        {
            "id": "msg_2026030211423139076eec0eff46e5",
            "type": "message",
            "role": "assistant",
            "model": "glm-5",
            "content": [
                {
                    "type": "tool_use",
                    "id": "call_d931b155197f4862b817a89d",
                    "name": "Grep",
                    "input": {
                        "pattern": "MD041|markdownlint",
                        "path": "/Users/xiaoming/code/codexspec",
                        "output_mode": "content",
                    },
                },
            ],
            "stop_reason": "tool_use",
            "stop_sequence": None,
            "usage": {
                "input_tokens": 1271,
                "cache_creation_input_tokens": 0,
                "cache_read_input_tokens": 31808,
                "output_tokens": 406,
                "server_tool_use": {
                    "web_search_requests": 0,
                    "web_fetch_requests": 0,
                },
                "service_tier": "standard",
                "cache_creation": {
                    "ephemeral_1h_input_tokens": 0,
                    "ephemeral_5m_input_tokens": 0,
                },
                "inference_geo": "",
                "iterations": [],
                "speed": "standard",
            },
        },
    ],
    "USER_QUESTION": [
        # Sample 1
        {
            "id": "msg_2026030211452143cb929688c04df0",
            "type": "message",
            "role": "assistant",
            "model": "glm-5",
            "content": [
                {
                    "type": "tool_use",
                    "id": "call_6b9e87c50f9740a09f8cd759",
                    "name": "AskUserQuestion",
                    "input": {
                        "questions": [
                            {
                                "question": "你倾向于哪种解决方案？",
                                "header": "方案选择",
                                "options": [
                                    {
                                        "label": "插入到 H1 之后（推荐）",
                                        "description": "智能检测第一个 H1 标题，将导入语句插入其后。符合 markdown 规范，无 lint 警告",
                                    },
                                    {
                                        "label": "添加 markdownlint-disable 注释",
                                        "description": "在文件开头添加 <!-- markdownlint-disable MD041 --> 注释。实现简单但添加了 lint 特定内容",
                                    },
                                    {
                                        "label": "保持现状",
                                        "description": "不修改代码，用户可自行配置 markdownlint 忽略此规则",
                                    },
                                ],
                                "multiSelect": False,
                            },
                        ],
                    },
                },
            ],
            "stop_reason": "tool_use",
            "stop_sequence": None,
            "usage": {
                "input_tokens": 1882,
                "cache_creation_input_tokens": 0,
                "cache_read_input_tokens": 38336,
                "output_tokens": 350,
                "server_tool_use": {
                    "web_search_requests": 0,
                    "web_fetch_requests": 0,
                },
                "service_tier": "standard",
                "cache_creation": {
                    "ephemeral_1h_input_tokens": 0,
                    "ephemeral_5m_input_tokens": 0,
                },
                "inference_geo": "",
                "iterations": [],
                "speed": "standard",
            },
        },
        # Sample 2
        {
            "id": "msg_2026031621191915bc69188ec145ef",
            "type": "message",
            "role": "assistant",
            "model": "glm-5",
            "content": [
                {
                    "type": "tool_use",
                    "id": "call_353e37c56f7b4088bff0f707",
                    "name": "AskUserQuestion",
                    "input": {
                        "questions": [
                            {
                                "question": "需要我修复这个测试性能问题吗？",
                                "header": "下一步",
                                "options": [
                                    {
                                        "label": "是，帮我修复（推荐）",
                                        "description": "在测试中 mock translate_with_claude_cli 函数，避免调用外部 Claude CLI",
                                    },
                                    {
                                        "label": "不需要，只是了解原因",
                                        "description": "我已经理解了问题，稍后自己处理",
                                    },
                                ],
                                "multiSelect": False,
                            },
                        ],
                    },
                },
            ],
            "stop_reason": "tool_use",
            "stop_sequence": None,
            "usage": {
                "input_tokens": 866,
                "cache_creation_input_tokens": 0,
                "cache_read_input_tokens": 43712,
                "output_tokens": 311,
                "server_tool_use": {
                    "web_search_requests": 0,
                    "web_fetch_requests": 0,
                },
                "service_tier": "standard",
                "cache_creation": {
                    "ephemeral_1h_input_tokens": 0,
                    "ephemeral_5m_input_tokens": 0,
                },
                "inference_geo": "",
                "iterations": [],
                "speed": "standard",
            },
        },
        # Sample 3
        {
            "id": "msg_202603111408407b54ccece849424d",
            "type": "message",
            "role": "assistant",
            "model": "glm-5",
            "content": [
                {
                    "type": "tool_use",
                    "id": "call_572fa6678033404b93e0a0a4",
                    "name": "AskUserQuestion",
                    "input": {
                        "questions": [
                            {
                                "question": "How would you like to handle missing Telegram credentials?",
                                "header": "Credentials",
                                "options": [
                                    {
                                        "label": "Add validation",
                                        "description": "Exit early with clear error message if TELEGRAM_BOT_TOKEN or TELEGRAM_CHAT_ID are not set",
                                    },
                                    {
                                        "label": "Skip silently",
                                        "description": "Continue running but skip sending notifications when credentials are missing",
                                    },
                                    {
                                        "label": "Not needed",
                                        "description": "I'll configure the environment variables, no code change needed",
                                    },
                                ],
                                "multiSelect": False,
                            },
                        ],
                    },
                },
            ],
            "stop_reason": "tool_use",
            "stop_sequence": None,
            "usage": {
                "input_tokens": 195,
                "cache_creation_input_tokens": 0,
                "cache_read_input_tokens": 37504,
                "output_tokens": 722,
                "server_tool_use": {
                    "web_search_requests": 0,
                    "web_fetch_requests": 0,
                },
                "service_tier": "standard",
                "cache_creation": {
                    "ephemeral_1h_input_tokens": 0,
                    "ephemeral_5m_input_tokens": 0,
                },
                "inference_geo": "",
                "iterations": [],
                "speed": "standard",
            },
        },
        # Sample 4
        {
            "id": "msg_202603121749298e5e3073582c420f",
            "type": "message",
            "role": "assistant",
            "model": "glm-5",
            "content": [
                {
                    "type": "tool_use",
                    "id": "call_ccc1932753d24b0681e69623",
                    "name": "AskUserQuestion",
                    "input": {
                        "questions": [
                            {
                                "question": "请先运行这个测试命令来验证 notify_telegram.py 是否能独立处理事件？",
                                "header": "测试命令",
                                "options": [
                                    {
                                        "label": "运行测试",
                                        "description": 'echo \'{"session_id":"test123","status":"TASK_COMPLETE","stop_reason":"end_turn","output":"Test"}\' | uv run python scripts/python/notify_telegram.py',
                                    },
                                    {
                                        "label": "我需要先检查 .env 配置",
                                        "description": "先确认 Telegram 凭证是否正确配置",
                                    },
                                ],
                                "multiSelect": False,
                            },
                        ],
                    },
                },
            ],
            "stop_reason": "tool_use",
            "stop_sequence": None,
            "usage": {
                "input_tokens": 1348,
                "cache_creation_input_tokens": 0,
                "cache_read_input_tokens": 76480,
                "output_tokens": 163,
                "server_tool_use": {
                    "web_search_requests": 0,
                    "web_fetch_requests": 0,
                },
                "service_tier": "standard",
                "cache_creation": {
                    "ephemeral_1h_input_tokens": 0,
                    "ephemeral_5m_input_tokens": 0,
                },
                "inference_geo": "",
                "iterations": [],
                "speed": "standard",
            },
        },
        # Sample 5
        {
            "id": "msg_202603121753596c0057a55700448b",
            "type": "message",
            "role": "assistant",
            "model": "glm-5",
            "content": [
                {
                    "type": "tool_use",
                    "id": "call_a0500e35221a4a4e839ddd90",
                    "name": "AskUserQuestion",
                    "input": {
                        "questions": [
                            {
                                "header": "确认问题",
                                "multiSelect": False,
                                "options": [
                                    {
                                        "description": "是的，我看到的 TASK_COMPLETE 事件是之前发生的，不是在 pipe 运行时新发生的",
                                        "label": "确认：是历史事件",
                                    },
                                    {
                                        "description": "不是，这些 TASK_COMPLETE 事件是在 pipe 运行期间新发生的",
                                        "label": "否认：是新事件",
                                    },
                                ],
                                "question": "我测试发现 pipe 工作正常。你看到的事件是否是在 pipe 运行之前就已经发生的（历史事件）？Monitor 只会输出新发生的事件，不会重复输出历史事件。",
                            },
                        ],
                    },
                },
            ],
            "stop_reason": "tool_use",
            "stop_sequence": None,
            "usage": {
                "input_tokens": 1066,
                "cache_creation_input_tokens": 0,
                "cache_read_input_tokens": 81728,
                "output_tokens": 180,
                "server_tool_use": {
                    "web_search_requests": 0,
                    "web_fetch_requests": 0,
                },
                "service_tier": "standard",
                "cache_creation": {
                    "ephemeral_1h_input_tokens": 0,
                    "ephemeral_5m_input_tokens": 0,
                },
                "inference_geo": "",
                "iterations": [],
                "speed": "standard",
            },
        },
    ],
    "ERROR_STOP": [],
    "TASK_COMPLETE": [
        # Sample 1
        {
            "id": "msg_20260318125945a0392734489c49fc",
            "type": "message",
            "role": "assistant",
            "model": "glm-5",
            "content": [
                {
                    "type": "text",
                    "text": 'The fix has been successfully applied.\n\n## Summary\n\n| Aspect | Details |\n|--------|---------|\n| **Bug** | `python3 -m notify_telegram` fails - not a module |\n| **Fix** | Use absolute path to script file |\n| **Code Changes** | 2 lines in `TeeNotifier.start()` (lines 942-945) |\n| **Impact** | Restores intended functionality |\n\n**Before (broken):**\n```python\n["uv", "run", "python3", "-m", "notify_telegram"]\n```\n\n**After (fixed):**\n```python\nnotify_script = Path(__file__).parent / "notify_telegram.py"\n["uv", "run", "python3", str(notify_script)]\n```\n\nThe fix uses `Path(__file__).parent` to get the directory containing `claude_monitor.py`, then appends `notify_telegram.py` to get the correct script path.',
                },
            ],
            "stop_reason": "end_turn",
            "stop_sequence": None,
            "usage": {
                "input_tokens": 512,
                "cache_creation_input_tokens": 0,
                "cache_read_input_tokens": 49792,
                "output_tokens": 300,
                "server_tool_use": {
                    "web_search_requests": 0,
                    "web_fetch_requests": 0,
                },
                "service_tier": "standard",
                "cache_creation": {
                    "ephemeral_1h_input_tokens": 0,
                    "ephemeral_5m_input_tokens": 0,
                },
                "inference_geo": "",
                "iterations": [],
                "speed": "standard",
            },
        },
        # Sample 2
        {
            "id": "msg_202603181302180630bb65b73047eb",
            "type": "message",
            "role": "assistant",
            "model": "glm-5",
            "content": [
                {
                    "type": "text",
                    "text": "✅ **Commit created successfully**\n\n```\nfeat(monitor): add --tee-notify flag for simultaneous output and notification\n```\n\n**Commit hash**: `02b84f3`\n**Files changed**: 1 file, 93 insertions, 4 deletions\n**Pre-commit hooks**: All passed (ruff, ruff-format, pytest, etc.)",
                },
            ],
            "stop_reason": "end_turn",
            "stop_sequence": None,
            "usage": {
                "input_tokens": 668,
                "cache_creation_input_tokens": 0,
                "cache_read_input_tokens": 54592,
                "output_tokens": 102,
                "server_tool_use": {
                    "web_search_requests": 0,
                    "web_fetch_requests": 0,
                },
                "service_tier": "standard",
                "cache_creation": {
                    "ephemeral_1h_input_tokens": 0,
                    "ephemeral_5m_input_tokens": 0,
                },
                "inference_geo": "",
                "iterations": [],
                "speed": "standard",
            },
        },
        # Sample 3
        {
            "id": "msg_202603162116132c8c92e22bdb4f11",
            "type": "message",
            "role": "assistant",
            "model": "glm-5",
            "content": [
                {
                    "type": "text",
                    "text": 'The target language "unsupported-lang" is not a valid language code. Please specify a supported language code (e.g., "zh-CN", "ja", "es", "fr", "de", etc.).\n\nIf you\'d like me to proceed anyway, here\'s the unchanged JSON:\n\n```json\n{\n  "test": {\n    "description": "Test description",\n    "argument-hint": null\n  }\n}\n```',
                },
            ],
            "stop_reason": "end_turn",
            "stop_sequence": None,
            "usage": {
                "input_tokens": 31671,
                "cache_creation_input_tokens": 0,
                "cache_read_input_tokens": 320,
                "output_tokens": 263,
                "server_tool_use": {
                    "web_search_requests": 0,
                    "web_fetch_requests": 0,
                },
                "service_tier": "standard",
                "cache_creation": {
                    "ephemeral_1h_input_tokens": 0,
                    "ephemeral_5m_input_tokens": 0,
                },
                "inference_geo": "",
                "iterations": [],
                "speed": "standard",
            },
        },
        # Sample 4
        {
            "id": "msg_20260315231340bb185d099f8d4601",
            "type": "message",
            "role": "assistant",
            "model": "glm-5",
            "content": [
                {
                    "type": "text",
                    "text": 'All 71 tests pass. Let me provide a summary of the changes made.\n\n## Summary\n\nI\'ve implemented the bug fix for `init --lang` not updating existing config.yml. Here\'s what was changed:\n\n### Files Modified\n\n1. **`src/codexspec/i18n.py`** - Added `update_config_language()` function\n   - New function to update language settings in existing config.yml files\n   - Updates both `output` and `commit` language settings using regex\n\n2. **`src/codexspec/__init__.py`** - Modified init command logic\n   - Added import for `update_config_language`\n   - Added conditional logic: when `--lang` is explicitly provided (not default "en") and config.yml exists, update the language setting instead of skipping\n\n3. **`src/codexspec/translator.py`** - Added new translation key to baseline\n   - Added `"language_updated": "Updated: Language setting changed to {lang_name}"`\n\n4. **Translation files** - Added `language_updated` key to all supported languages:\n   - `templates/translations/en.json`\n   - `templates/translations/zh-CN.json`\n   - `templates/translations/ja.json`\n   - `templates/translations/ko.json`\n   - `templates/translations/es.json`\n   - `templates/translations/fr.json`\n   - `templates/translations/de.json`\n   - `templates/translations/pt-BR.json`\n\n### Behavior After Fix\n\n1. `codexspec init --here --lang ja` on existing project:\n   - Creates config.yml if it doesn\'t exist ✓\n   - **Now updates language setting if config.yml exists** ✓\n   - Shows "Updated: Language setting changed to Japanese" message\n\n2. `codexspec init --here` (without `--lang`):\n   - Doesn\'t modify existing config.yml (unchanged behavior)\n\n3. `codexspec init --here --force --lang ja`:\n   - Overwrites config.yml completely (unchanged behavior)',
                },
            ],
            "stop_reason": "end_turn",
            "stop_sequence": None,
            "usage": {
                "input_tokens": 997,
                "cache_creation_input_tokens": 0,
                "cache_read_input_tokens": 86592,
                "output_tokens": 446,
                "server_tool_use": {
                    "web_search_requests": 0,
                    "web_fetch_requests": 0,
                },
                "service_tier": "standard",
                "cache_creation": {
                    "ephemeral_1h_input_tokens": 0,
                    "ephemeral_5m_input_tokens": 0,
                },
                "inference_geo": "",
                "iterations": [],
                "speed": "standard",
            },
        },
        # Sample 5
        {
            "id": "msg_20260315231501a550fab799b647cb",
            "type": "message",
            "role": "assistant",
            "model": "glm-5",
            "content": [
                {
                    "type": "text",
                    "text": "已将所有修改的文件添加到暂存区：\n\n**已暂存的文件 (11个):**\n- `src/codexspec/__init__.py` - init 命令逻辑修改\n- `src/codexspec/i18n.py` - 新增 `update_config_language()` 函数\n- `src/codexspec/translator.py` - 添加翻译基线\n- `templates/translations/*.json` (8个语言文件) - 添加 `language_updated` 翻译键",
                },
            ],
            "stop_reason": "end_turn",
            "stop_sequence": None,
            "usage": {
                "input_tokens": 787,
                "cache_creation_input_tokens": 0,
                "cache_read_input_tokens": 88128,
                "output_tokens": 139,
                "server_tool_use": {
                    "web_search_requests": 0,
                    "web_fetch_requests": 0,
                },
                "service_tier": "standard",
                "cache_creation": {
                    "ephemeral_1h_input_tokens": 0,
                    "ephemeral_5m_input_tokens": 0,
                },
                "inference_geo": "",
                "iterations": [],
                "speed": "standard",
            },
        },
    ],
}


def get_messages(category: str) -> list[dict]:
    """Get messages for a specific category."""
    return REAL_MESSAGES.get(category, [])


def get_sample(category: str, index: int = 0) -> dict | None:
    """Get a single sample message."""
    messages = get_messages(category)
    return messages[index] if index < len(messages) else None

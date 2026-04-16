"""Tests for claude_auto_responder.py"""

import json
import subprocess
import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent.parent / "scripts" / "python"))

from claude_auto_responder import (
    ClaudeDecider,
    Detector,
    PendingToolUse,
    Router,
    SafetyPolicyEngine,
    TmuxSender,
    build_prompt,
    classify_bash_command,
    extract_pending_tool_use,
    is_path_within_project,
    load_project_context,
    parse_jsonl,
)


@pytest.fixture
def tmp_project(tmp_path):
    """Create a temporary project directory with CLAUDE.md and constitution."""
    claude_md = tmp_path / "CLAUDE.md"
    claude_md.write_text("# Test Project\nSome rules here.")
    const_dir = tmp_path / ".codexspec" / "memory"
    const_dir.mkdir(parents=True)
    (const_dir / "constitution.md").write_text("# Constitution\nBe safe.")
    return tmp_path


@pytest.fixture
def make_jsonl(tmp_path):
    """Helper to create a jsonl file from records."""

    def _make(records, filename="session.jsonl"):
        p = tmp_path / filename
        with open(p, "w") as f:
            for rec in records:
                f.write(json.dumps(rec) + "\n")
        return p

    return _make


@pytest.fixture
def ask_tool_use():
    """An AskUserQuestion tool_use record."""

    def _make(tool_id="toolu_01ABC", question="Which auth?", options=None, multi=False):
        if options is None:
            options = [
                {"label": "JWT", "description": "Use JWT"},
                {"label": "OAuth", "description": "Use OAuth"},
            ]
        return {
            "type": "assistant",
            "message": {
                "content": [
                    {
                        "type": "tool_use",
                        "id": tool_id,
                        "name": "AskUserQuestion",
                        "input": {
                            "questions": [
                                {
                                    "question": question,
                                    "header": "Auth",
                                    "options": options,
                                    "multiSelect": multi,
                                }
                            ]
                        },
                    }
                ]
            },
        }

    return _make


@pytest.fixture
def bash_tool_use():
    """A Bash tool_use record."""

    def _make(tool_id="toolu_01BASH", command="ls -la"):
        return {
            "type": "assistant",
            "message": {
                "content": [
                    {
                        "type": "tool_use",
                        "id": tool_id,
                        "name": "Bash",
                        "input": {"command": command, "description": "list files"},
                    }
                ]
            },
        }

    return _make


@pytest.fixture
def tool_result():
    """A tool_result record."""

    def _make(tool_id="toolu_01ABC"):
        return {
            "type": "user",
            "message": {
                "content": [
                    {
                        "type": "tool_result",
                        "tool_use_id": tool_id,
                        "content": "User answered.",
                    }
                ]
            },
        }

    return _make


# ============================================================================
# Task 2.1: parse_jsonl + extract_pending_tool_use tests
# ============================================================================


class TestParseJsonl:
    def test_empty_file(self, make_jsonl):
        p = make_jsonl([])
        records = parse_jsonl(p)
        assert records == []

    def test_valid_records(self, make_jsonl, ask_tool_use, tool_result):
        p = make_jsonl([ask_tool_use(), tool_result()])
        records = parse_jsonl(p)
        assert len(records) == 2

    def test_bad_line_skipped(self, tmp_path):
        p = tmp_path / "bad.jsonl"
        p.write_text('{"valid": true}\nnot json at all\n{"also": "valid"}\n')
        records = parse_jsonl(p)
        assert len(records) == 2

    def test_file_not_found(self, tmp_path):
        p = tmp_path / "nope.jsonl"
        records = parse_jsonl(p)
        assert records == []


class TestExtractPendingToolUse:
    def test_unanswered_ask_question(self, make_jsonl, ask_tool_use):
        """TC-001: Unanswered AskUserQuestion detected."""
        records = [ask_tool_use(tool_id="toolu_01")]
        pending = extract_pending_tool_use(records)
        assert pending is not None
        assert pending.tool_use_id == "toolu_01"
        assert pending.name == "AskUserQuestion"

    def test_answered_ask_question_skipped(self, ask_tool_use, tool_result):
        """TC-002: Answered AskUserQuestion not detected."""
        records = [ask_tool_use(tool_id="toolu_01"), tool_result(tool_id="toolu_01")]
        pending = extract_pending_tool_use(records)
        assert pending is None

    def test_two_questions_first_answered(self, ask_tool_use, tool_result):
        """TC-003: Two questions, first answered, second pending."""
        records = [
            ask_tool_use(tool_id="toolu_01"),
            tool_result(tool_id="toolu_01"),
            ask_tool_use(tool_id="toolu_02", question="Second?"),
        ]
        pending = extract_pending_tool_use(records)
        assert pending is not None
        assert pending.tool_use_id == "toolu_02"

    def test_unanswered_bash_tool_use(self, bash_tool_use):
        """Unanswered Bash tool_use detected."""
        records = [bash_tool_use(tool_id="toolu_bash")]
        pending = extract_pending_tool_use(records)
        assert pending is not None
        assert pending.tool_use_id == "toolu_bash"
        assert pending.name == "Bash"

    def test_string_content_no_tool_result(self, ask_tool_use):
        """User message with string content has no tool_result."""
        records = [
            ask_tool_use(tool_id="toolu_01"),
            {"type": "user", "message": {"content": "just a text message"}},
        ]
        pending = extract_pending_tool_use(records)
        assert pending is not None
        assert pending.tool_use_id == "toolu_01"

    def test_multiple_tool_use_in_one_message(self):
        """Multiple tool_use in one assistant message; last unanswered returned."""
        records = [
            {
                "type": "assistant",
                "message": {
                    "content": [
                        {"type": "tool_use", "id": "toolu_A", "name": "Read", "input": {}},
                        {"type": "tool_use", "id": "toolu_B", "name": "Bash", "input": {"command": "ls"}},
                    ]
                },
            },
            {
                "type": "user",
                "message": {
                    "content": [
                        {"type": "tool_result", "tool_use_id": "toolu_A", "content": "ok"},
                    ]
                },
            },
        ]
        pending = extract_pending_tool_use(records)
        assert pending is not None
        assert pending.tool_use_id == "toolu_B"

    def test_all_answered_returns_none(self, ask_tool_use, bash_tool_use, tool_result):
        """All tool_uses answered → None."""
        records = [
            ask_tool_use(tool_id="toolu_01"),
            tool_result(tool_id="toolu_01"),
            bash_tool_use(tool_id="toolu_02"),
            {
                "type": "user",
                "message": {
                    "content": [
                        {"type": "tool_result", "tool_use_id": "toolu_02", "content": "ok"},
                    ]
                },
            },
        ]
        pending = extract_pending_tool_use(records)
        assert pending is None


# ============================================================================
# Task 2.3: Detector tests
# ============================================================================


class TestDetector:
    def test_file_not_found(self, tmp_path):
        """TC-007: jsonl file does not exist."""
        d = Detector(tmp_path / "missing.jsonl", stable_ms=0)
        result = d.check()
        assert result is None

    def test_mtime_not_stable(self, make_jsonl, ask_tool_use):
        """TC-009: File mtime not stable yet."""
        p = make_jsonl([ask_tool_use()])
        d = Detector(p, stable_ms=999999)
        result = d.check()
        assert result is None

    def test_normal_detection(self, make_jsonl, ask_tool_use):
        """Normal pending detection with stable file."""
        p = make_jsonl([ask_tool_use(tool_id="toolu_det")])
        d = Detector(p, stable_ms=0)
        result = d.check()
        assert result is not None
        assert result.tool_use_id == "toolu_det"

    def test_dedup(self, make_jsonl, ask_tool_use):
        """TC-010: Same tool_use_id not returned twice."""
        p = make_jsonl([ask_tool_use(tool_id="toolu_dup")])
        d = Detector(p, stable_ms=0)
        first = d.check()
        assert first is not None
        d.mark_processed(first.tool_use_id)
        second = d.check()
        assert second is None

    def test_empty_file(self, make_jsonl):
        """Empty jsonl returns None."""
        p = make_jsonl([])
        d = Detector(p, stable_ms=0)
        assert d.check() is None


# ============================================================================
# Task 3.1: PathChecker tests
# ============================================================================


class TestPathChecker:
    def test_inside_project(self, tmp_path):
        """TC-023/025: Path inside project → True."""
        f = tmp_path / "src" / "main.py"
        f.parent.mkdir(parents=True)
        f.touch()
        assert is_path_within_project(str(f), tmp_path) is True

    def test_outside_project(self, tmp_path):
        """TC-024/026: Path outside project → False."""
        assert is_path_within_project("/etc/hosts", tmp_path) is False

    def test_symlink_outside(self, tmp_path):
        """TC-033: Symlink pointing outside → False."""
        link = tmp_path / "sneaky_link"
        link.symlink_to("/etc/hosts")
        assert is_path_within_project(str(link), tmp_path) is False

    def test_relative_path(self, tmp_path):
        """Relative path resolved to project dir."""
        f = tmp_path / "file.txt"
        f.touch()
        assert is_path_within_project(str(f), tmp_path) is True

    def test_nonexistent_path_parent_in_project(self, tmp_path):
        """Nonexistent path whose parent is in project → True."""
        f = tmp_path / "src" / "new_file.py"
        (tmp_path / "src").mkdir(exist_ok=True)
        assert is_path_within_project(str(f), tmp_path) is True

    def test_nonexistent_path_parent_outside(self, tmp_path):
        """Nonexistent path whose parent is outside → False."""
        assert is_path_within_project("/nowhere/deep/file.py", tmp_path) is False


# ============================================================================
# Task 3.3: BashClassifier tests
# ============================================================================


class TestBashClassifier:
    def test_readonly_whitelist_cat(self, tmp_path):
        """TC-020: cat is safe."""
        cat, reason = classify_bash_command("cat src/main.py", tmp_path)
        assert cat == "SAFE"

    def test_readonly_whitelist_ls(self, tmp_path):
        """TC-028: ls is safe."""
        cat, reason = classify_bash_command("ls -la", tmp_path)
        assert cat == "SAFE"

    def test_readonly_git_status(self, tmp_path):
        """TC-030: git status is safe."""
        cat, reason = classify_bash_command("git status", tmp_path)
        assert cat == "SAFE"

    def test_uv_run_pytest(self, tmp_path):
        """TC-030: uv run pytest is safe."""
        cat, reason = classify_bash_command("uv run pytest", tmp_path)
        assert cat == "SAFE"

    def test_dangerous_rm(self, tmp_path):
        """TC-021: rm is dangerous."""
        cat, reason = classify_bash_command("rm -rf /tmp/old", tmp_path)
        assert cat == "DANGEROUS"

    def test_dangerous_git_push_force(self, tmp_path):
        """TC-029: git push --force is dangerous."""
        cat, reason = classify_bash_command("git push --force", tmp_path)
        assert cat == "DANGEROUS"

    def test_compound_safe_then_dangerous(self, tmp_path):
        """TC-022: compound with rm → DANGEROUS."""
        cat, reason = classify_bash_command("ls -la && rm file.txt", tmp_path)
        assert cat == "DANGEROUS"

    def test_pipe_safe(self, tmp_path):
        """TC-034: cat | head is safe."""
        cat, reason = classify_bash_command("cat file | head -5", tmp_path)
        assert cat == "SAFE"

    def test_redirect_outside_project(self, tmp_path):
        """TC-035: redirect to absolute path outside project → DANGEROUS."""
        cat, reason = classify_bash_command('echo "hello" > /absolute/path', tmp_path)
        assert cat == "DANGEROUS"

    def test_empty_command(self, tmp_path):
        """Empty command → DENY."""
        cat, reason = classify_bash_command("", tmp_path)
        assert cat == "DANGEROUS"

    def test_unknown_command(self, tmp_path):
        """Unknown command → UNKNOWN."""
        cat, reason = classify_bash_command("some_exotic_tool --flag", tmp_path)
        assert cat == "UNKNOWN"

    def test_policy_allow_override(self, tmp_path):
        """TC-031: Policy override allows docker build."""
        policy = {"allow_commands": ["docker build"]}
        cat, reason = classify_bash_command("docker build .", tmp_path, policy=policy)
        assert cat == "SAFE"

    def test_policy_deny_overrides_allow(self, tmp_path):
        """TC-032: Policy deny takes precedence over allow."""
        policy = {"allow_commands": ["curl"], "deny_commands": ["curl -X POST"]}
        cat, reason = classify_bash_command("curl -X POST http://example.com", tmp_path, policy=policy)
        assert cat == "DANGEROUS"

    def test_git_log(self, tmp_path):
        cat, reason = classify_bash_command("git log --oneline -10", tmp_path)
        assert cat == "SAFE"

    def test_pip_install_dangerous(self, tmp_path):
        cat, reason = classify_bash_command("pip install requests", tmp_path)
        assert cat == "DANGEROUS"


# ============================================================================
# Task 3.5: SafetyPolicyEngine tests
# ============================================================================


class TestSafetyPolicyEngine:
    def test_read_always_allowed(self, tmp_path):
        """TC-028: Read tool → ALLOW."""
        engine = SafetyPolicyEngine(tmp_path)
        decision = engine.evaluate("Read", {"file_path": "/etc/passwd"})
        assert decision.action == "ALLOW"

    def test_grep_allowed(self, tmp_path):
        engine = SafetyPolicyEngine(tmp_path)
        decision = engine.evaluate("Grep", {"pattern": "foo"})
        assert decision.action == "ALLOW"

    def test_glob_allowed(self, tmp_path):
        engine = SafetyPolicyEngine(tmp_path)
        decision = engine.evaluate("Glob", {"pattern": "*.py"})
        assert decision.action == "ALLOW"

    def test_edit_inside_project(self, tmp_path):
        """TC-023: Edit inside project → ALLOW."""
        f = tmp_path / "src" / "main.py"
        f.parent.mkdir(parents=True)
        f.touch()
        engine = SafetyPolicyEngine(tmp_path)
        decision = engine.evaluate("Edit", {"file_path": str(f)})
        assert decision.action == "ALLOW"

    def test_edit_outside_project(self, tmp_path):
        """TC-024: Edit outside project → DENY."""
        engine = SafetyPolicyEngine(tmp_path)
        decision = engine.evaluate("Edit", {"file_path": "/etc/hosts"})
        assert decision.action == "DENY"

    def test_write_inside_project(self, tmp_path):
        """TC-025: Write inside project → ALLOW."""
        f = tmp_path / "output.txt"
        engine = SafetyPolicyEngine(tmp_path)
        decision = engine.evaluate("Write", {"file_path": str(f)})
        assert decision.action == "ALLOW"

    def test_write_outside_project(self, tmp_path):
        """TC-026: Write outside project → DENY."""
        engine = SafetyPolicyEngine(tmp_path)
        decision = engine.evaluate("Write", {"file_path": "/tmp/outside.txt"})
        assert decision.action == "DENY"

    def test_bash_safe(self, tmp_path):
        engine = SafetyPolicyEngine(tmp_path)
        decision = engine.evaluate("Bash", {"command": "ls -la"})
        assert decision.action == "ALLOW"

    def test_bash_dangerous(self, tmp_path):
        engine = SafetyPolicyEngine(tmp_path)
        decision = engine.evaluate("Bash", {"command": "rm -rf /"})
        assert decision.action == "DENY"

    def test_unknown_tool_denied(self, tmp_path):
        """TC-027: Unknown tool → DENY."""
        engine = SafetyPolicyEngine(tmp_path)
        decision = engine.evaluate("CustomTool", {"whatever": True})
        assert decision.action == "DENY"

    def test_policy_allow_unknown_tools(self, tmp_path):
        engine = SafetyPolicyEngine(tmp_path, policy={"allow_unknown_tools": True})
        decision = engine.evaluate("CustomTool", {"whatever": True})
        assert decision.action == "ALLOW"

    def test_policy_deny_tools(self, tmp_path):
        engine = SafetyPolicyEngine(tmp_path, policy={"deny_tools": ["Agent"]})
        decision = engine.evaluate("Agent", {"task": "something"})
        assert decision.action == "DENY"

    def test_bash_unknown_defaults_deny(self, tmp_path):
        engine = SafetyPolicyEngine(tmp_path)
        decision = engine.evaluate("Bash", {"command": "some_exotic_tool"})
        assert decision.action == "DENY"

    def test_missing_file_path_in_edit(self, tmp_path):
        engine = SafetyPolicyEngine(tmp_path)
        decision = engine.evaluate("Edit", {})
        assert decision.action == "DENY"

    def test_missing_command_in_bash(self, tmp_path):
        engine = SafetyPolicyEngine(tmp_path)
        decision = engine.evaluate("Bash", {})
        assert decision.action == "DENY"


# ============================================================================
# Task 4.1: load_project_context + build_prompt tests
# ============================================================================


class TestLoadProjectContext:
    def test_with_both_files(self, tmp_project):
        """Both CLAUDE.md and constitution.md present."""
        ctx = load_project_context(tmp_project)
        assert "Test Project" in ctx["claude_md"]
        assert "Constitution" in ctx["constitution"]

    def test_missing_claude_md(self, tmp_path):
        """TC-013: CLAUDE.md missing → empty string."""
        ctx = load_project_context(tmp_path)
        assert ctx["claude_md"] == ""

    def test_missing_constitution(self, tmp_path):
        (tmp_path / "CLAUDE.md").write_text("# Test")
        ctx = load_project_context(tmp_path)
        assert ctx["constitution"] == ""

    def test_truncation(self, tmp_path):
        """Large file truncated to 30KB."""
        (tmp_path / "CLAUDE.md").write_text("x" * 40000)
        ctx = load_project_context(tmp_path)
        assert len(ctx["claude_md"]) == 30000


class TestBuildPrompt:
    def test_basic_prompt(self, tmp_project):
        ctx = load_project_context(tmp_project)
        question = {
            "question": "Which auth?",
            "header": "Auth",
            "options": [{"label": "JWT"}, {"label": "OAuth"}],
            "multiSelect": False,
        }
        prompt = build_prompt(None, ctx, question)
        assert "<project_claude_md>" in prompt
        assert "<task>" in prompt
        assert "JWT" in prompt
        assert "<system_prompt>" not in prompt

    def test_with_system_prompt(self, tmp_project):
        ctx = load_project_context(tmp_project)
        question = {"question": "Q?", "options": [], "multiSelect": False}
        prompt = build_prompt("Be concise.", ctx, question)
        assert "<system_prompt>" in prompt
        assert "Be concise." in prompt


# ============================================================================
# Task 4.3: ClaudeDecider tests
# ============================================================================


class TestClaudeDecider:
    def test_valid_json_response(self):
        """TC-001: Pure JSON response parsed correctly."""
        question = {
            "question": "Which auth?",
            "options": [{"label": "JWT"}, {"label": "OAuth"}],
            "multiSelect": False,
        }
        decider = ClaudeDecider(claude_bin="claude", timeout=30)
        with patch("subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(
                returncode=0,
                stdout='{"answers": ["JWT"]}',
                stderr="",
            )
            result = decider.decide("prompt", question)
        assert result == ["JWT"]

    def test_markdown_fence_json(self):
        """TC-015: JSON wrapped in markdown fence."""
        question = {
            "question": "Which?",
            "options": [{"label": "A"}, {"label": "B"}],
            "multiSelect": False,
        }
        decider = ClaudeDecider(claude_bin="claude", timeout=30)
        with patch("subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(
                returncode=0,
                stdout='```json\n{"answers": ["A"]}\n```',
                stderr="",
            )
            result = decider.decide("prompt", question)
        assert result == ["A"]

    def test_brace_pair_scanning(self):
        """JSON with extra text around it."""
        question = {
            "question": "Which?",
            "options": [{"label": "X"}],
            "multiSelect": False,
        }
        decider = ClaudeDecider(claude_bin="claude", timeout=30)
        with patch("subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(
                returncode=0,
                stdout='Here is my answer: {"answers": ["X"]} done.',
                stderr="",
            )
            result = decider.decide("prompt", question)
        assert result == ["X"]

    def test_multiselect(self):
        """TC-004: Multi-select returns multiple labels."""
        question = {
            "question": "Choose",
            "options": [{"label": "A"}, {"label": "B"}, {"label": "C"}],
            "multiSelect": True,
        }
        decider = ClaudeDecider(claude_bin="claude", timeout=30)
        with patch("subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(
                returncode=0,
                stdout='{"answers": ["A", "C"]}',
                stderr="",
            )
            result = decider.decide("prompt", question)
        assert result == ["A", "C"]

    def test_invalid_label(self):
        """TC-005: Invalid label → None."""
        question = {
            "question": "Which?",
            "options": [{"label": "A"}, {"label": "B"}],
            "multiSelect": False,
        }
        decider = ClaudeDecider(claude_bin="claude", timeout=30)
        with patch("subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(
                returncode=0,
                stdout='{"answers": ["INVALID"]}',
                stderr="",
            )
            result = decider.decide("prompt", question)
        assert result is None

    def test_timeout(self):
        """TC-006: Timeout → None."""
        question = {"question": "Q?", "options": [{"label": "A"}], "multiSelect": False}
        decider = ClaudeDecider(claude_bin="claude", timeout=1)
        with patch("subprocess.run", side_effect=subprocess.TimeoutExpired(cmd="claude", timeout=1)):
            result = decider.decide("prompt", question)
        assert result is None

    def test_single_select_multiple_answers(self):
        """Single select but multiple answers → None."""
        question = {
            "question": "Which?",
            "options": [{"label": "A"}, {"label": "B"}],
            "multiSelect": False,
        }
        decider = ClaudeDecider(claude_bin="claude", timeout=30)
        with patch("subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(
                returncode=0,
                stdout='{"answers": ["A", "B"]}',
                stderr="",
            )
            result = decider.decide("prompt", question)
        assert result is None

    def test_nonzero_exit_code(self):
        """Non-zero exit code → None."""
        question = {"question": "Q?", "options": [{"label": "A"}], "multiSelect": False}
        decider = ClaudeDecider(claude_bin="claude", timeout=30)
        with patch("subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(returncode=1, stdout="", stderr="error")
            result = decider.decide("prompt", question)
        assert result is None


# ============================================================================
# Task 5.1: TmuxSender + Router tests
# ============================================================================


class TestTmuxSender:
    def test_send_answers_single(self):
        sender = TmuxSender("test:0.1")
        with patch("subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(returncode=0)
            ok = sender.send_answers(["JWT"])
        assert ok is True
        assert mock_run.call_count == 2  # send-keys -l + Enter

    def test_send_answers_multi(self):
        sender = TmuxSender("test:0.1")
        with patch("subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(returncode=0)
            ok = sender.send_answers(["A", "B"])
        assert ok is True
        assert mock_run.call_count == 4  # 2 labels × (text + Enter)

    def test_send_permission_allow(self):
        sender = TmuxSender("test:0.1")
        with patch("subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(returncode=0)
            ok = sender.send_permission(allow=True)
        assert ok is True

    def test_send_permission_deny(self):
        sender = TmuxSender("test:0.1")
        with patch("subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(returncode=0)
            ok = sender.send_permission(allow=False)
        assert ok is True

    def test_dry_run(self):
        """TC-011: Dry run doesn't call subprocess."""
        sender = TmuxSender("test:0.1", dry_run=True)
        with patch("subprocess.run") as mock_run:
            ok = sender.send_answers(["JWT"])
        assert ok is True
        mock_run.assert_not_called()

    def test_send_failure(self):
        """TC-008: tmux failure handled."""
        sender = TmuxSender("test:0.1")
        with patch("subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(returncode=1, stderr="no pane")
            ok = sender.send_answers(["JWT"])
        assert ok is False

    def test_pane_exists(self):
        sender = TmuxSender("test:0.1")
        with patch("subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(returncode=0)
            assert sender.pane_exists() is True

    def test_pane_not_exists(self):
        sender = TmuxSender("test:0.1")
        with patch("subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(returncode=1)
            assert sender.pane_exists() is False


class TestRouter:
    def test_ask_user_question_routed_to_decider(self, tmp_project):
        """AskUserQuestion → ClaudeDecider path."""
        pending = PendingToolUse(
            tool_use_id="toolu_01",
            name="AskUserQuestion",
            input={
                "questions": [
                    {
                        "question": "Which?",
                        "header": "H",
                        "options": [{"label": "A"}, {"label": "B"}],
                        "multiSelect": False,
                    }
                ]
            },
        )
        decider = MagicMock()
        decider.decide.return_value = ["A"]
        engine = SafetyPolicyEngine(tmp_project)
        ctx = load_project_context(tmp_project)
        router = Router(decider=decider, safety_engine=engine, context=ctx, system_prompt=None)
        resp = router.handle(pending)
        assert resp is not None
        assert resp.response_type == "answers"
        assert resp.answers == ["A"]

    def test_bash_routed_to_safety_engine(self, tmp_project):
        """Bash → SafetyPolicyEngine path."""
        pending = PendingToolUse(
            tool_use_id="toolu_02",
            name="Bash",
            input={"command": "ls -la"},
        )
        decider = MagicMock()
        engine = SafetyPolicyEngine(tmp_project)
        ctx = load_project_context(tmp_project)
        router = Router(decider=decider, safety_engine=engine, context=ctx, system_prompt=None)
        resp = router.handle(pending)
        assert resp is not None
        assert resp.response_type == "permission"
        assert resp.allow is True

    def test_dangerous_bash_denied(self, tmp_project):
        pending = PendingToolUse(
            tool_use_id="toolu_03",
            name="Bash",
            input={"command": "rm -rf /"},
        )
        decider = MagicMock()
        engine = SafetyPolicyEngine(tmp_project)
        ctx = load_project_context(tmp_project)
        router = Router(decider=decider, safety_engine=engine, context=ctx, system_prompt=None)
        resp = router.handle(pending)
        assert resp.response_type == "permission"
        assert resp.allow is False

    def test_decider_failure_returns_none(self, tmp_project):
        """ClaudeDecider returns None → Router returns None."""
        pending = PendingToolUse(
            tool_use_id="toolu_04",
            name="AskUserQuestion",
            input={
                "questions": [
                    {
                        "question": "Q?",
                        "header": "H",
                        "options": [{"label": "X"}],
                        "multiSelect": False,
                    }
                ]
            },
        )
        decider = MagicMock()
        decider.decide.return_value = None
        engine = SafetyPolicyEngine(tmp_project)
        ctx = load_project_context(tmp_project)
        router = Router(decider=decider, safety_engine=engine, context=ctx, system_prompt=None)
        resp = router.handle(pending)
        assert resp is None


# ============================================================================
# Task 6.1: End-to-end mock tests
# ============================================================================


class TestE2E:
    def test_ask_question_full_flow(self, tmp_project, make_jsonl, ask_tool_use):
        """E2E: AskUserQuestion → claude -p → tmux send_answers."""
        jsonl_path = make_jsonl([ask_tool_use(tool_id="toolu_e2e_ask")])

        ctx = load_project_context(tmp_project)
        detector = Detector(jsonl_path, stable_ms=0)
        decider = MagicMock()
        decider.decide.return_value = ["JWT"]
        engine = SafetyPolicyEngine(tmp_project)
        router = Router(decider=decider, safety_engine=engine, context=ctx, system_prompt=None)
        sender = MagicMock()
        sender.send_answers.return_value = True

        pending = detector.check()
        assert pending is not None
        assert pending.name == "AskUserQuestion"

        resp = router.handle(pending)
        assert resp is not None
        assert resp.response_type == "answers"

        ok = sender.send_answers(resp.answers)
        assert ok is True
        sender.send_answers.assert_called_once_with(["JWT"])
        detector.mark_processed(pending.tool_use_id)

        assert detector.check() is None

    def test_bash_permission_allow_flow(self, tmp_project, make_jsonl, bash_tool_use):
        """E2E: Bash safe → SafetyPolicy ALLOW → tmux send Y."""
        jsonl_path = make_jsonl([bash_tool_use(tool_id="toolu_e2e_bash", command="ls -la")])

        ctx = load_project_context(tmp_project)
        detector = Detector(jsonl_path, stable_ms=0)
        engine = SafetyPolicyEngine(tmp_project)
        router = Router(decider=MagicMock(), safety_engine=engine, context=ctx)
        sender = MagicMock()
        sender.send_permission.return_value = True

        pending = detector.check()
        assert pending is not None

        resp = router.handle(pending)
        assert resp.response_type == "permission"
        assert resp.allow is True

        ok = sender.send_permission(True)
        assert ok is True
        detector.mark_processed(pending.tool_use_id)
        assert detector.check() is None

    def test_bash_permission_deny_flow(self, tmp_project, make_jsonl, bash_tool_use):
        """E2E: Bash dangerous → SafetyPolicy DENY → tmux send n."""
        jsonl_path = make_jsonl([bash_tool_use(tool_id="toolu_e2e_rm", command="rm -rf /")])

        ctx = load_project_context(tmp_project)
        detector = Detector(jsonl_path, stable_ms=0)
        engine = SafetyPolicyEngine(tmp_project)
        router = Router(decider=MagicMock(), safety_engine=engine, context=ctx)
        sender = MagicMock()
        sender.send_permission.return_value = True

        pending = detector.check()
        resp = router.handle(pending)
        assert resp.response_type == "permission"
        assert resp.allow is False

        ok = sender.send_permission(False)
        assert ok is True

    def test_dedup_across_rounds(self, tmp_project, make_jsonl, ask_tool_use):
        """E2E: Same tool_use_id not processed twice."""
        jsonl_path = make_jsonl([ask_tool_use(tool_id="toolu_dup_e2e")])
        detector = Detector(jsonl_path, stable_ms=0)

        first = detector.check()
        assert first is not None
        detector.mark_processed(first.tool_use_id)

        second = detector.check()
        assert second is None

    def test_dry_run_no_tmux_calls(self, tmp_project, make_jsonl, bash_tool_use):
        """E2E: --dry-run mode skips actual tmux sends."""
        jsonl_path = make_jsonl([bash_tool_use(tool_id="toolu_dry")])

        detector = Detector(jsonl_path, stable_ms=0)
        engine = SafetyPolicyEngine(tmp_project)
        ctx = load_project_context(tmp_project)
        router = Router(decider=MagicMock(), safety_engine=engine, context=ctx)
        sender = TmuxSender("fake:0.1", dry_run=True)

        pending = detector.check()
        resp = router.handle(pending)

        with patch("subprocess.run") as mock_run:
            ok = sender.send_permission(resp.allow)
        assert ok is True
        mock_run.assert_not_called()

# 任务分解：claude-auto-responder（v2 — 全状态响应 + 安全策略）

## 概览

- 总任务数：24
- 可并行任务：7
- 阶段数：6
- 主文件：`scripts/python/claude_auto_responder.py`
- 测试文件：`tests/scripts/python/test_claude_auto_responder.py`

## Phase 1: Foundation

### Task 1.1: 创建脚本骨架 ✅

- **Type**: Setup
- **Files**: `scripts/python/claude_auto_responder.py`
- **Description**: shebang、docstring（含使用示例）、`__version__ = "0.2.0"`、退出码常量、`if __name__ == "__main__"` 占位
- **Dependencies**: None
- **Est. Complexity**: Low

### Task 1.2: 创建测试文件骨架 [P] ✅

- **Type**: Setup
- **Files**: `tests/scripts/python/test_claude_auto_responder.py`
- **Description**: import、fixture（临时目录、样例 jsonl）、dataclass 占位
- **Dependencies**: Task 1.1
- **Est. Complexity**: Low

### Task 1.3: 实现 `parse_args` [P] ✅

- **Type**: Implementation
- **Files**: `scripts/python/claude_auto_responder.py`
- **Description**: 定义所有 CLI 参数（含新增 `--safety-policy-file`、`--decide-timeout`）
- **Dependencies**: Task 1.1
- **Est. Complexity**: Low

### Task 1.4: 实现 `Logger` 类 [P] ✅

- **Type**: Implementation
- **Files**: `scripts/python/claude_auto_responder.py`
- **Description**: Logger 类含 `startup/pending/decide/policy_allow/policy_deny/sent/warn/error` 方法；emoji + 时间戳；stderr + 可选文件
- **Dependencies**: Task 1.1
- **Est. Complexity**: Low

### Task 1.5: 实现数据类 [P] ✅

- **Type**: Implementation
- **Files**: `scripts/python/claude_auto_responder.py`
- **Description**: 定义 `PendingToolUse`、`PolicyDecision`、`Response` dataclass
- **Dependencies**: Task 1.1
- **Est. Complexity**: Low

## Phase 2: Core Detection (TDD)

### Task 2.1: 写 `parse_jsonl` + `extract_pending_tool_use` 测试 ✅

- **Type**: Testing
- **Files**: `tests/scripts/python/test_claude_auto_responder.py`
- **Description**: 覆盖：AskUserQuestion 未答（TC-001）、已答跳过（TC-002）、两条前答后未答（TC-003）、Bash tool_use 未答、空文件、坏行、字符串 content、多 tool_use 混合
- **Dependencies**: Task 1.2, Task 1.5
- **Est. Complexity**: Medium

### Task 2.2: 实现 `parse_jsonl` 和 `extract_pending_tool_use` ✅

- **Type**: Implementation
- **Files**: `scripts/python/claude_auto_responder.py`
- **Description**: 通用版解析——提取所有 tool_use（不仅 AskUserQuestion）和 tool_result；返回最后一个未回答的 PendingToolUse；需通过 Task 2.1 测试
- **Dependencies**: Task 2.1
- **Est. Complexity**: Medium

### Task 2.3: 写 `Detector` 测试 [P] ✅

- **Type**: Testing
- **Files**: `tests/scripts/python/test_claude_auto_responder.py`
- **Description**: 文件不存在（TC-007）、mtime 不稳定（TC-009）、去重（TC-010）、正常检测
- **Dependencies**: Task 2.2
- **Est. Complexity**: Medium

### Task 2.4: 实现 `Detector` 类 ✅

- **Type**: Implementation
- **Files**: `scripts/python/claude_auto_responder.py`
- **Description**: 组合文件存在性 + mtime 稳定 + parse + dedupe
- **Dependencies**: Task 2.3
- **Est. Complexity**: Medium

## Phase 3: Safety Policy Engine (TDD)

### Task 3.1: 写 `PathChecker` 测试 [P] ✅

- **Type**: Testing
- **Files**: `tests/scripts/python/test_claude_auto_responder.py`
- **Description**: 测试：项目内路径→True（TC-023/025）、项目外路径→False（TC-024/026）、符号链接指向项目外→False（TC-033）、相对路径解析、不存在路径使用父目录判定
- **Dependencies**: Task 1.2
- **Est. Complexity**: Low

### Task 3.2: 实现 `PathChecker` [P] ✅

- **Type**: Implementation
- **Files**: `scripts/python/claude_auto_responder.py`
- **Description**: `is_path_within_project(file_path, project_root) -> bool`；realpath 解析；不存在路径回退到逐级父目录判定
- **Dependencies**: Task 3.1
- **Est. Complexity**: Low

### Task 3.3: 写 `BashClassifier` 测试 ✅

- **Type**: Testing
- **Files**: `tests/scripts/python/test_claude_auto_responder.py`
- **Description**: 测试：只读白名单命令（TC-020/028/030/034）、黑名单命令（TC-021/029）、复合命令（TC-022）、重定向到项目外（TC-035）、管道命令、空命令→DENY、policy override（TC-031/032）、未知命令→UNKNOWN
- **Dependencies**: Task 3.2
- **Est. Complexity**: High

### Task 3.4: 实现 `BashClassifier` ✅

- **Type**: Implementation
- **Files**: `scripts/python/claude_auto_responder.py`
- **Description**: `classify_bash_command(command, project_root, policy) -> (category, reason)`；白名单/黑名单/分段/重定向检查；通过 Task 3.3 测试
- **Dependencies**: Task 3.3
- **Est. Complexity**: High

### Task 3.5: 写 `SafetyPolicyEngine` 测试 [P] ✅

- **Type**: Testing
- **Files**: `tests/scripts/python/test_claude_auto_responder.py`
- **Description**: 测试：Read→ALLOW（TC-028）、Edit 项目内→ALLOW（TC-023）、Edit 项目外→DENY（TC-024）、Bash 安全→ALLOW、Bash 危险→DENY、未知工具→DENY（TC-027）、policy override allow_unknown_tools
- **Dependencies**: Task 3.4
- **Est. Complexity**: Medium

### Task 3.6: 实现 `SafetyPolicyEngine` ✅

- **Type**: Implementation
- **Files**: `scripts/python/claude_auto_responder.py`
- **Description**: 组合 PathChecker + BashClassifier + policy overrides；`evaluate(tool_name, tool_input) -> PolicyDecision`；通过 Task 3.5 测试
- **Dependencies**: Task 3.5
- **Est. Complexity**: Medium

### Task 3.7: 实现安全策略配置文件加载 ✅

- **Type**: Implementation
- **Files**: `scripts/python/claude_auto_responder.py`
- **Description**: `load_safety_policy(path) -> dict`；读取 JSON 并校验字段类型；不存在时退出码 2
- **Dependencies**: Task 3.6
- **Est. Complexity**: Low

## Phase 4: AskUserQuestion Decision (TDD)

### Task 4.1: 写 `load_project_context` + `build_prompt` 测试 [P] ✅

- **Type**: Testing
- **Files**: `tests/scripts/python/test_claude_auto_responder.py`
- **Description**: CLAUDE.md 缺失→空字符串（TC-013）、30KB 截断、prompt 格式验证、系统提示词为空时省略段落
- **Dependencies**: Task 1.2
- **Est. Complexity**: Low

### Task 4.2: 实现 `load_project_context` 和 `build_prompt` ✅

- **Type**: Implementation
- **Files**: `scripts/python/claude_auto_responder.py`
- **Description**: 纯函数；通过 Task 4.1 测试
- **Dependencies**: Task 4.1
- **Est. Complexity**: Low

### Task 4.3: 写 `ClaudeDecider` 测试 ✅

- **Type**: Testing
- **Files**: `tests/scripts/python/test_claude_auto_responder.py`
- **Description**: mock subprocess；纯 JSON（TC-001）、markdown fence（TC-015）、大括号扫描、多选（TC-004）、无效 label（TC-005）、超时（TC-006）、单选返回多个→失败
- **Dependencies**: Task 4.2
- **Est. Complexity**: Medium

### Task 4.4: 实现 `ClaudeDecider` ✅

- **Type**: Implementation
- **Files**: `scripts/python/claude_auto_responder.py`
- **Description**: claude -p 调用 + 三级 JSON 回退 + 答案校验；通过 Task 4.3 测试
- **Dependencies**: Task 4.3
- **Est. Complexity**: High

## Phase 5: Integration

### Task 5.1: 写 `TmuxSender` 测试 [P] ✅

- **Type**: Testing
- **Files**: `tests/scripts/python/test_claude_auto_responder.py`
- **Description**: mock subprocess；send_answers 单/多 label；send_permission Y/n；dry-run（TC-011）；失败处理（TC-008）
- **Dependencies**: Task 4.4, Task 3.6
- **Est. Complexity**: Medium

### Task 5.2: 实现 `TmuxSender` + `Router` ✅

- **Type**: Implementation
- **Files**: `scripts/python/claude_auto_responder.py`
- **Description**: TmuxSender 含 send_answers + send_permission；Router 按 tool name 分流到 ClaudeDecider 或 SafetyPolicyEngine；通过 Task 5.1 测试
- **Dependencies**: Task 5.1
- **Est. Complexity**: Medium

### Task 5.3: 实现 `validate_startup` + `MainLoop` + `main()` ✅

- **Type**: Implementation
- **Files**: `scripts/python/claude_auto_responder.py`
- **Description**: 启动校验（含 safety-policy-file）；MainLoop 组装全链路；SIGINT handler；main() 入口
- **Dependencies**: Task 5.2
- **Est. Complexity**: Medium

## Phase 6: E2E Testing & Documentation

### Task 6.1: 端到端 mock 测试 ✅

- **Type**: Testing
- **Files**: `tests/scripts/python/test_claude_auto_responder.py`
- **Description**: mock subprocess 全链路：AskUserQuestion → claude -p → tmux send_answers；Bash 权限 → SafetyPolicy → tmux send_permission Y/n；去重验证；dry-run
- **Dependencies**: Task 5.3
- **Est. Complexity**: High

### Task 6.2: 手动 smoke test 检查清单 [P] ✅

- **Type**: Documentation
- **Files**: `.codexspec/specs/2026-0415-2119q5-claude-auto-responder/smoke-test.md`
- **Description**: 启动真实 Claude Code + tmux；验证 AskUserQuestion 自动选择；验证 Bash 权限自动允许/拒绝；验证项目外 Edit 拒绝；Ctrl+C；dry-run
- **Dependencies**: Task 5.3
- **Est. Complexity**: Low

## 执行顺序

```
Phase 1:  1.1 ──► 1.2 [P]
              ├─► 1.3 [P]
              ├─► 1.4 [P]
              └─► 1.5 [P]

Phase 2:  1.2+1.5 ──► 2.1 ──► 2.2 ──► 2.3 [P] ──► 2.4

Phase 3:  1.2 ──► 3.1 [P] ──► 3.2 ──► 3.3 ──► 3.4 ──► 3.5 [P] ──► 3.6 ──► 3.7
          (Phase 3 可与 Phase 2 并行启动)

Phase 4:  1.2 ──► 4.1 [P] ──► 4.2 ──► 4.3 ──► 4.4
          (Phase 4 可与 Phase 2/3 并行启动)

Phase 5:  2.4 + 3.6 + 4.4 ──► 5.1 [P] ──► 5.2 ──► 5.3

Phase 6:  5.3 ──► 6.1
              └─► 6.2 [P]
```

## 检查点

- [x] **CP1**（Phase 1 后）：`python claude_auto_responder.py --version` 运行正常
- [x] **CP2**（Phase 2 后）：jsonl 解析和检测逻辑单测全通过（16/16）
- [x] **CP3**（Phase 3 后）：安全策略引擎 TC-020~TC-035 全通过（52/52）
- [x] **CP4**（Phase 4 后）：AskUserQuestion 决策逻辑单测全通过（66/66）
- [x] **CP5**（Phase 5 后）：`--dry-run` 模式端到端可运行（78/78）
- [x] **CP6**（Phase 6 后）：端到端测试 + smoke checklist 完成（83/83）

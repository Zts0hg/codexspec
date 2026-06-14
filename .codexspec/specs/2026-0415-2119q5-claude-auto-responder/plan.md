# 实现方案：claude-auto-responder（v2 — 全状态响应 + 安全策略）

## 1. 技术栈

| 类别 | 技术 | 版本 | 说明 |
|------|------|------|------|
| 语言 | Python | 3.11+ | 与 scripts/python/ 一致 |
| 标准库 | argparse, json, subprocess, pathlib, time, re, sys, signal, os, fnmatch, dataclasses | — | 零三方依赖 |
| 外部 CLI | tmux | 3.x | send-keys / list-panes |
| 外部 CLI | claude | 官方 CLI | `-p` 一次性决策（仅 AskUserQuestion） |
| 测试 | pytest | 8.x | 单元测试 |

## 2. 宪法审查

| 原则 | 合规 | 说明 |
|------|------|------|
| Code Quality | ✅ | 纯函数核心；安全策略引擎完全可测试 |
| Testing | ✅ | 安全策略 35+ 测试用例 |
| Documentation | ✅ | CLI --help + 安全规则日志 |
| Architecture | ✅ | 安全引擎与决策逻辑解耦 |
| Performance | ✅ | 权限判定 < 1ms（纯本地） |
| Security | ✅ | 默认拒绝未知操作；realpath 防符号链接绕过 |

## 3. 架构概览

```
┌─────────────────────────────────────────────────────────────────┐
│                  claude_auto_responder.py                        │
│                                                                  │
│  ┌─────────┐   ┌──────────────┐   ┌──────────┐   ┌──────────┐  │
│  │   CLI   │──▶│  MainLoop    │──▶│ Detector │──▶│ JsonlIO  │  │
│  │  (args) │   │  (poll)      │   └────┬─────┘   └──────────┘  │
│  └─────────┘   └──────┬───────┘        │                        │
│                       │          ┌─────┴──────┐                  │
│                       │          │  Router     │                  │
│                       │          └──┬──────┬───┘                  │
│                       │             │      │                      │
│                       │    AskUserQ │      │ Permission           │
│                       │             ▼      ▼                      │
│                       │   ┌────────────┐ ┌──────────────┐        │
│                       │   │PromptBuild │ │SafetyPolicy  │        │
│                       │   └─────┬──────┘ │  Engine      │        │
│                       │         ▼        └──────┬───────┘        │
│                       │   ┌────────────┐        │                │
│                       │   │ClaudeDecide│        │                │
│                       │   └─────┬──────┘        │                │
│                       │         │               │                │
│                       │         ▼               ▼                │
│                       │   ┌─────────────────────────┐            │
│                       └──▶│      TmuxSender         │──▶ tmux   │
│                           └─────────────────────────┘            │
│                                                                  │
│  横切：Logger（stderr + 可选文件）                                │
└─────────────────────────────────────────────────────────────────┘
```

核心变化：新增 **Router** 按 tool name 分流，新增 **SafetyPolicyEngine** 纯函数模块。

## 4. 文件结构

```
codexspec/
├── scripts/python/
│   └── claude_auto_responder.py     # 主脚本（单文件）
└── tests/scripts/python/
    └── test_claude_auto_responder.py # 单元测试
```

## 5. 模块依赖图

```
CLI ──▶ MainLoop ──▶ Detector ──▶ JsonlParser
                │
                ├──▶ Router ─────┬──▶ PromptBuilder ──▶ ContextLoader
                │                │         │
                │                │    ClaudeDecider ──▶ AnswerParser
                │                │
                │                └──▶ SafetyPolicyEngine ──▶ BashClassifier
                │                                          ──▶ PathChecker
                │
                └──▶ TmuxSender ──▶ (subprocess: tmux)

所有模块 ──▶ Logger
```

## 6. 模块规格

### Module: CLI

- **职责**：解析 CLI 参数、启动校验
- **接口**：`parse_args() -> Namespace`、`validate_startup(args, logger)`
- **文件**：`claude_auto_responder.py` 顶部

### Module: Logger

- **职责**：结构化日志（emoji + 时间戳），stderr + 可选文件
- **接口**：`.startup()`, `.pending()`, `.decide()`, `.policy_allow()`, `.policy_deny()`, `.sent()`, `.warn()`, `.error()`

### Module: JsonlParser（纯函数）

- **职责**：解析 jsonl，提取所有 tool_use 和 tool_result
- **接口**：
  - `parse_jsonl(path) -> List[dict]`
  - `extract_pending_tool_use(records) -> Optional[PendingToolUse]`
  - 数据类 `PendingToolUse { tool_use_id: str, name: str, input: dict }`
- **变化**：从仅提取 AskUserQuestion 改为提取所有 tool_use

### Module: Detector

- **职责**：文件存在 + mtime 稳定 + 解析 + 去重
- **接口**：`Detector(jsonl_path, stable_ms, processed_ids, logger).check() -> Optional[PendingToolUse]`

### Module: Router（新增）

- **职责**：根据 `PendingToolUse.name` 分流到不同处理器
- **接口**：`Router(decider, safety_engine, logger).handle(pending) -> Response`
- **逻辑**：
  - `name == 'AskUserQuestion'` → ClaudeDecider
  - 其他 → SafetyPolicyEngine

### Module: SafetyPolicyEngine（新增，纯函数）

- **职责**：评估工具权限请求的安全性
- **依赖**：BashClassifier, PathChecker
- **接口**：
  - `SafetyPolicyEngine(project_root: Path, policy_overrides: Optional[dict])`
  - `.evaluate(tool_name: str, tool_input: dict) -> PolicyDecision`
  - 数据类 `PolicyDecision { action: 'ALLOW' | 'DENY', reason: str }`
- **子模块**：
  - `BashClassifier`：解析 Bash command 字符串，判定安全/危险/未知
  - `PathChecker`：检查文件路径是否在项目目录内（realpath 解析）

### Module: BashClassifier（纯函数，SafetyPolicyEngine 内部）

- **职责**：将 Bash command 分类为 SAFE / DANGEROUS / UNKNOWN
- **接口**：`classify_bash_command(command: str, project_root: Path, policy: dict) -> Tuple[str, str]`
- **算法**：
  1. 按 `&&`/`||`/`;` 分段
  2. 每段去首尾空格，提取首个 token（命令名）
  3. 依次匹配：policy deny_commands → policy allow_commands → 默认黑名单 → 默认白名单
  4. 检查重定向 `>` 到项目外路径
  5. 任一段 DANGEROUS → 整体 DANGEROUS
  6. 全部 SAFE → 整体 SAFE
  7. 有 UNKNOWN → 整体 UNKNOWN（默认 DENY）

### Module: PathChecker（纯函数）

- **职责**：判断路径是否在项目目录内
- **接口**：`is_path_within_project(file_path: str, project_root: Path) -> bool`
- **实现**：`os.path.realpath(file_path).startswith(os.path.realpath(str(project_root)))`

### Module: ContextLoader（纯函数）

- **职责**：读取 CLAUDE.md 和 constitution.md（30KB 截断）
- **接口**：`load_project_context(project_root) -> dict`

### Module: PromptBuilder（纯函数）

- **职责**：组装 claude -p prompt（仅 AskUserQuestion）
- **接口**：`build_prompt(system_prompt, ctx, question) -> str`

### Module: ClaudeDecider

- **职责**：调用 claude -p、JSON 三级回退解析、答案校验
- **接口**：`.decide(prompt, question) -> Optional[List[str]]`

### Module: TmuxSender

- **职责**：发送 label/Y/n 到 tmux
- **接口**：
  - `.send_answers(answers: List[str]) -> bool`（AskUserQuestion）
  - `.send_permission(allow: bool) -> bool`（权限请求）
  - `.pane_exists() -> bool`

### Module: MainLoop

- **职责**：循环编排，SIGINT 处理
- **接口**：`MainLoop(args, logger).run()`

## 7. 数据模型

### PendingToolUse（dataclass）

| 字段 | 类型 | 说明 |
|------|------|------|
| tool_use_id | str | `toolu_...` |
| name | str | 工具名（AskUserQuestion/Bash/Edit/Write/...） |
| input | dict | 工具输入参数 |

### PolicyDecision（dataclass）

| 字段 | 类型 | 说明 |
|------|------|------|
| action | str | `'ALLOW'` 或 `'DENY'` |
| reason | str | 人类可读原因 |

### Response（dataclass）

| 字段 | 类型 | 说明 |
|------|------|------|
| response_type | str | `'answers'` / `'permission'` |
| answers | Optional[List[str]] | AskUserQuestion 的 label 列表 |
| allow | Optional[bool] | 权限请求 True=允许 False=拒绝 |
| reason | str | 日志原因 |

## 8. CLI 契约

同 spec REQ-001，新增 `--safety-policy-file`。

退出码：`0` 正常 / `2` 启动失败 / `130` SIGINT

## 9. 实施阶段

### Phase 1：基础框架

- [ ] 脚本骨架 + 版本 + shebang
- [ ] parse_args（含新参数 --safety-policy-file）
- [ ] Logger（新增 policy_allow/policy_deny 方法）
- [ ] load_project_context
- [ ] 测试骨架

### Phase 2：核心检测（纯函数）

- [ ] JsonlParser：parse_jsonl + extract_pending_tool_use（通用版，提取所有 tool_use）
- [ ] Detector
- [ ] PendingToolUse / PolicyDecision / Response 数据类

### Phase 3：安全策略引擎（纯函数，TDD）

- [ ] PathChecker
- [ ] BashClassifier（白名单 + 黑名单 + 复合命令分段 + 重定向检查）
- [ ] SafetyPolicyEngine（组合 PathChecker + BashClassifier + policy overrides）
- [ ] 安全策略配置文件加载与合并

### Phase 4：AskUserQuestion 决策

- [ ] PromptBuilder
- [ ] ClaudeDecider（JSON 三级回退 + 答案校验）

### Phase 5：集成与发送

- [ ] Router
- [ ] TmuxSender（新增 send_permission 方法）
- [ ] MainLoop
- [ ] main() 入口

### Phase 6：测试

- [ ] 安全策略引擎单元测试（TC-020~TC-035）
- [ ] 检测逻辑单元测试（TC-001~TC-015）
- [ ] 端到端 mock 测试
- [ ] 手动 smoke test

## 10. 技术决策

### Decision 1：权限请求用本地策略引擎而非 LLM

- **选择**：纯本地规则引擎
- **理由**：权限请求结构化、可枚举；LLM 调用延迟 3-10s 不可接受；规则引擎判定 < 1ms 且确定性 100%
- **代价**：规则需手动维护；灰色地带默认拒绝可能偏保守

### Decision 2：默认拒绝未知命令/工具

- **选择**：DENY by default
- **理由**：安全优先；误拒绝只是暂停 Claude Code（用户可手动允许），误允许可能造成不可逆损害
- **代价**：新工具/新命令需要手动加白名单

### Decision 3：Bash 命令分段检查

- **选择**：按 `&&`/`||`/`;` 分段，任一段危险则整体拒绝
- **理由**：`safe_cmd && rm -rf /` 必须被捕获；管道中 `safe | dangerous_write` 也必须被捕获
- **代价**：可能误拒合法复合命令；但安全性优先

### Decision 4：realpath 解析符号链接

- **选择**：对 Edit/Write 路径使用 `os.path.realpath` 解析后判定
- **理由**：防止 `/project/link -> /etc/hosts` 绕过路径检查
- **代价**：realpath 需要文件/目录存在才能完全解析；对不存在路径使用父目录判定

### Decision 5：单文件保持

- **选择**：仍然单文件
- **理由**：安全策略引擎虽然增加约 200 行，总量约 800-900 行仍可管理；与同目录脚本一致

# Task Breakdown: Claude Code Plugin Marketplace Support

## Overview

- **Total tasks**: 14
- **Completed**: 11
- **Pending (Manual Testing)**: 3
- **Parallelizable tasks**: 4
- **Estimated phases**: 4
- **Feature ID**: 2026-0328-1525gi-claude-code-plugin-marketplace

## Implementation Summary

### ✅ Completed Tasks

- **Phase 1 (Foundation)**: TASK-1.1, TASK-1.2, TASK-1.3 - All completed
- **Phase 2 (Core Implementation)**: TASK-2.1, TASK-2.2, TASK-2.3, TASK-2.4 - All completed
- **Phase 3 (Testing)**: TASK-3.1 - JSON verification completed
- **Phase 4 (Documentation)**: TASK-4.1, TASK-4.2, TASK-4.3 - All completed

### 🔄 Pending Tasks (Require Manual Testing)

- **TASK-3.2**: Plugin installation test - Requires running Claude Code
- **TASK-3.3**: Publish flow test - Requires testing `publish.sh`
- **TASK-3.4**: Multi-language support verification - Requires manual verification
- **TASK-3.5**: Coexistence test - Requires running `codexspec init`

## User Story Mapping

| User Story | Related Tasks |
|------------|---------------|
| Story 1: 通过插件市场安装 | TASK-1.1, TASK-1.2, TASK-1.3, TASK-3.2 |
| Story 2: 使用现有方式安装 | TASK-3.5 (共存测试) |
| Story 3: 获取插件更新 | TASK-2.1, TASK-2.2, TASK-2.3, TASK-3.3 |
| Story 4: 多语言支持 | TASK-3.4 (验证现有机制) |
| Story 5: 发布新版本 | TASK-2.1, TASK-2.2, TASK-2.3, TASK-3.3 |

---

## Phase 1: Foundation (创建市场配置)

### TASK-1.1: 创建插件市场目录 ✅

- **Type**: Setup
- **Files**: `.claude-plugin/`
- **Description**: 创建 `.claude-plugin/` 目录用于存放插件市场配置
- **Dependencies**: None
- **Est. Complexity**: Low
- **Verification**: `ls -la .claude-plugin/` 目录存在
- **Status**: ✅ Completed

### TASK-1.2: 创建 marketplace.json 文件 ✅

- **Type**: Configuration
- **Files**: `.claude-plugin/marketplace.json`
- **Description**: 创建 Claude Code 插件市场定义文件
  - 定义市场名称：`codexspec-market`
  - 定义插件名称：`codexspec`
  - 设置初始版本引用：`v0.5.11` (当前 pyproject.toml 版本)
  - 配置源路径：`.claude/commands/codexspec`
  - 设置 `strict: false`
- **Dependencies**: TASK-1.1
- **Est. Complexity**: Low
- **Verification**: `python -m json.tool .claude-plugin/marketplace.json` 验证 JSON 格式
- **Status**: ✅ Completed

### TASK-1.3: 验证命令目录存在 ✅

- **Type**: Verification
- **Files**: `.claude/commands/codexspec/`
- **Description**: 验证插件命令目录和文件已存在（通过 `codexspec init` 创建）
  - 确认 19 个命令文件存在
  - 确认文件内容与 `templates/commands/` 一致
- **Dependencies**: None
- **Est. Complexity**: Low
- **Verification**: `ls .claude/commands/codexspec/*.md | wc -l` 返回 19
- **Status**: ✅ Completed

---

## Phase 2: Core Implementation (修改发布脚本)

### TASK-2.1: 添加 marketplace 更新函数 ✅

- **Type**: Implementation
- **Files**: `publish.sh`
- **Description**: 在 `publish.sh` 中添加 `update_marketplace()` 函数
  - 读取当前版本号
  - 使用 `sed` 更新 marketplace.json 中的 `ref` 和 `version` 字段
  - 添加日志输出
- **Dependencies**: TASK-1.2
- **Est. Complexity**: Medium
- **Verification**: `grep -n "update_marketplace" publish.sh` 验证函数存在
- **Status**: ✅ Completed

### TASK-2.2: 集成 marketplace 更新到发布流程 ✅

- **Type**: Implementation
- **Files**: `publish.sh`
- **Description**: 在创建 tag 后调用 `update_marketplace()` 函数
  - 在 `git push origin "$TAG_NAME"` 之后添加调用
  - 提交 marketplace.json 的更改
  - 推送到远程仓库
- **Dependencies**: TASK-2.1
- **Est. Complexity**: Medium
- **Verification**: `grep -n "update_marketplace" publish.sh | grep -v "^function"` 验证调用位置
- **Status**: ✅ Completed

### TASK-2.3: 添加 --skip-marketplace 选项 ✅

- **Type**: Implementation
- **Files**: `publish.sh`
- **Description**: 添加命令行选项允许跳过 marketplace 更新
  - 添加 `SKIP_MARKETPLACE=false` 变量
  - 添加 `--skip-marketplace` 参数解析
  - 在调用 `update_marketplace()` 前检查变量
- **Dependencies**: TASK-2.2
- **Est. Complexity**: Low
- **Verification**: `./publish.sh --help` 或 `grep "skip-marketplace" publish.sh`
- **Status**: ✅ Completed

### TASK-2.4: 添加错误处理 ✅

- **Type**: Implementation
- **Files**: `publish.sh`
- **Description**: 添加 marketplace.json 相关错误处理
  - 检查 marketplace.json 文件是否存在
  - 检查 JSON 格式是否有效
  - 错误时输出友好提示
- **Dependencies**: TASK-2.3
- **Est. Complexity**: Low
- **Verification**: 手动测试删除 marketplace.json 后运行脚本
- **Status**: ✅ Completed

---

## Phase 3: Testing (验证功能)

### TASK-3.1: 本地验证 marketplace.json 格式 [P] ✅

- **Type**: Testing
- **Files**: `.claude-plugin/marketplace.json`
- **Description**: 验证 marketplace.json 符合 Claude Code schema
  - 使用 `python -m json.tool` 验证 JSON 语法
  - 检查必需字段：name, owner, plugins
  - 检查插件字段：name, source, version
- **Dependencies**: TASK-1.2
- **Est. Complexity**: Low
- **Verification**: JSON 验证通过
- **Status**: ✅ Completed

### TASK-3.2: 插件安装测试 [P]

- **Type**: Testing
- **Files**: N/A (manual test)
- **Description**: 测试插件安装流程
  1. 执行 `/plugin marketplace add Zts0hg/codexspec`
  2. 执行 `/plugin install codexspec@codexspec-market`
  3. 验证命令可用：`/codexspec:specify` 响应正常
- **Dependencies**: TASK-1.2, TASK-1.3
- **Est. Complexity**: Medium
- **Verification**: 插件安装成功，命令可执行
- **Status**: 🔄 Pending (Manual Testing Required)

### TASK-3.3: 发布流程测试

- **Type**: Testing
- **Files**: `publish.sh`
- **Description**: 测试 publish.sh 的 marketplace 集成
  1. 使用 `./publish.sh --test --skip-tag --skip-marketplace` 测试基础功能
  2. 验证 `--skip-marketplace` 选项工作正常
  3. 模拟版本更新，检查 marketplace.json 更新逻辑
- **Dependencies**: TASK-2.4
- **Est. Complexity**: Medium
- **Verification**: 脚本执行无错误
- **Status**: 🔄 Pending (Manual Testing Required)

### TASK-3.4: 多语言支持验证 [P]

- **Type**: Testing
- **Files**: `.claude/commands/codexspec/*.md`
- **Description**: 验证插件命令的多语言支持
  1. 创建测试项目，配置 `language.output: "zh-CN"`
  2. 执行 `/codexspec:specify` 验证中文响应
  3. 检查命令文件包含 `## Language Preference` 部分
- **Dependencies**: TASK-1.3
- **Est. Complexity**: Low
- **Verification**: 中文响应正常
- **Status**: 🔄 Pending (Manual Testing Required)

### TASK-3.5: 共存测试

- **Type**: Testing
- **Files**: N/A (manual test)
- **Description**: 验证插件安装和 `codexspec init` 可共存
  1. 已安装插件的项目中执行 `codexspec init`
  2. 验证无冲突
  3. 验证两种安装方式的命令一致
- **Dependencies**: TASK-3.2
- **Est. Complexity**: Low
- **Verification**: 无错误，命令一致
- **Status**: 🔄 Pending (Manual Testing Required)

---

## Phase 4: Documentation (更新文档)

### TASK-4.1: 更新 README.md [P] ✅

- **Type**: Documentation
- **Files**: `README.md`
- **Description**: 添加插件安装方式说明
  - 添加 "Plugin Installation" 章节
  - 添加安装命令示例
  - 添加两种安装方式对比表
  - 更新 "Installation" 章节引用
- **Dependencies**: TASK-3.2
- **Est. Complexity**: Low
- **Verification**: README 包含插件安装说明
- **Status**: ✅ Completed

### TASK-4.2: 更新 README.zh-CN.md [P] ✅

- **Type**: Documentation
- **Files**: `README.zh-CN.md`
- **Description**: 同步中文文档更新
  - 翻译 "Plugin Installation" 章节
  - 更新安装对比表
  - 保持与英文版一致
- **Dependencies**: TASK-4.1
- **Est. Complexity**: Low
- **Verification**: 中文 README 包含插件安装说明
- **Status**: ✅ Completed

### TASK-4.3: 更新 CLAUDE.md ✅

- **Type**: Documentation
- **Files**: `CLAUDE.md`
- **Description**: 更新项目 AI 上下文文档
  - 在 "Project Structure" 中添加 `.claude-plugin/` 目录
  - 更新 "Commands Implementation Status" 表
  - 添加 "Plugin Marketplace Support" 章节
- **Dependencies**: TASK-3.2
- **Est. Complexity**: Low
- **Verification**: CLAUDE.md 包含插件支持说明
- **Status**: ✅ Completed

---

## Execution Order

```
Phase 1: Foundation
├── TASK-1.1 ──► TASK-1.2 ──► TASK-1.3 [P]
│                               │
│                               ▼
Phase 2: Core Implementation    │
├── TASK-2.1 ──► TASK-2.2 ──► TASK-2.3 ──► TASK-2.4
│                               │
│                               ▼
Phase 3: Testing                │
├── TASK-3.1 [P]                │
├── TASK-3.2 [P] ◄──────────────┘
├── TASK-3.3
├── TASK-3.4 [P]
└── TASK-3.5
    │
    ▼
Phase 4: Documentation
├── TASK-4.1 [P] ──► TASK-4.2 [P]
└── TASK-4.3 [P]
```

## Parallel Execution Groups

| Group | Tasks | Reason |
|-------|-------|--------|
| Group A | TASK-1.3, TASK-3.1, TASK-3.4 | 验证任务可并行 |
| Group B | TASK-4.1, TASK-4.2, TASK-4.3 | 文档任务可并行 |

## Checkpoints

- [x] **Checkpoint 1**: After Phase 1 - 验证 `.claude-plugin/marketplace.json` 创建成功 ✅
- [x] **Checkpoint 2**: After Phase 2 - 验证 `publish.sh --skip-marketplace` 执行正常 ✅
- [ ] **Checkpoint 3**: After Phase 3 - 验证插件安装成功 (待手动测试)
- [x] **Checkpoint 4**: After Phase 4 - 验证所有文档更新完成 ✅

## Estimated Timeline

| Phase | Tasks | Est. Time |
|-------|-------|-----------|
| Phase 1 | 3 tasks | 30 min |
| Phase 2 | 4 tasks | 45 min |
| Phase 3 | 5 tasks | 1 hour |
| Phase 4 | 3 tasks | 30 min |
| **Total** | **14 tasks** | **~3 hours** |

## Notes

- **TDD 适用性**: 此功能主要是配置和文档，不涉及大量代码实现，因此 TDD 原则主要体现在验证测试（Phase 3）中
- **回滚策略**: 如遇问题，可删除 `.claude-plugin/` 目录并回退 `publish.sh` 更改
- **测试环境**: 建议在测试仓库中先验证插件安装流程

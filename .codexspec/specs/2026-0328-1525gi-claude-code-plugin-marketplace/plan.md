# Implementation Plan: Claude Code Plugin Marketplace Support

## 1. Tech Stack

| Category | Technology | Version | Notes |
|----------|------------|---------|-------|
| Language | Python | 3.11+ | 现有项目语言 |
| CLI Framework | Typer | 0.9.0+ | 现有框架 |
| Package Manager | uv | Latest | 现有工具 |
| Build System | Hatchling | Latest | 现有构建系统 |
| Plugin System | Claude Code Plugin | Native | 无额外依赖 |
| Hosting | GitHub | - | 插件市场托管 |

## 2. Constitutionality Review

| Principle | Compliance | Notes |
|-----------|------------|-------|
| Code Quality | ✅ | 复用现有模板，保持单一来源原则 |
| Testing Standards | ✅ | 添加插件市场验证测试 |
| Documentation | ✅ | 更新 README 和 CLAUDE.md |
| Architecture | ✅ | 添加新目录结构，不修改现有架构 |
| Performance | ✅ | 无性能影响，插件加载由 Claude Code 管理 |
| Security | ✅ | 无安全敏感变更 |
| Slash Command Template Rules | ✅ | `templates/commands/` 保持为单一来源 |
| Decision Guidelines | ✅ | 优先可维护性和稳定性 |

## 3. Architecture Overview

```
codexspec/
├── .claude-plugin/                    # [NEW] 插件市场定义
│   └── marketplace.json
├── .claude/                           # [EXISTING] 活动命令目录
│   ├── commands/
│   │   └── codexspec/                 # 插件命令来源
│   │       ├── constitution.md
│   │       ├── specify.md
│   │       └── ... (19 files)
│   └── settings.local.json
├── templates/                         # [EXISTING] 模板源目录
│   └── commands/                      # 命令模板来源
│       ├── constitution.md
│       ├── specify.md
│       └── ... (19 files)
├── publish.sh                         # [MODIFY] 集成 marketplace 更新
├── pyproject.toml                     # [EXISTING] 版本定义
└── README.md                          # [MODIFY] 添加插件安装说明
```

### 数据流图

```
┌─────────────────────────────────────────────────────────────────────┐
│                        发布流程                                      │
│                                                                     │
│  1. 开发者运行 ./publish.sh                                          │
│     │                                                               │
│     ▼                                                               │
│  2. 脚本读取 pyproject.toml 版本 (如 0.5.11)                         │
│     │                                                               │
│     ▼                                                               │
│  3. 构建 & 上传到 PyPI                                               │
│     │                                                               │
│     ▼                                                               │
│  4. 创建 Git tag (v0.5.11)                                          │
│     │                                                               │
│     ▼                                                               │
│  5. [NEW] 更新 marketplace.json 中的 ref → v0.5.11                   │
│     │                                                               │
│     ▼                                                               │
│  6. [NEW] 提交 & 推送 marketplace.json 更改                          │
│     │                                                               │
│     ▼                                                               │
│  7. 用户执行 /plugin update 获取新版本                               │
└─────────────────────────────────────────────────────────────────────┘
```

## 4. Module Design

### Module 1: Plugin Marketplace Configuration

| 属性 | 描述 |
|------|------|
| **Responsibility** | 定义插件市场元数据和插件入口 |
| **Dependencies** | 无 |
| **Interfaces** | Claude Code 插件系统读取 `marketplace.json` |
| **Files** | `.claude-plugin/marketplace.json` |

### Module 2: Plugin Commands Directory

| 属性 | 描述 |
|------|------|
| **Responsibility** | 提供插件命令文件（已存在） |
| **Dependencies** | `templates/commands/` (通过 `codexspec init` 同步) |
| **Interfaces** | Claude Code 读取 `.claude/commands/codexspec/*.md` |
| **Files** | `.claude/commands/codexspec/*.md` (19 files) |

### Module 3: Publish Script Enhancement

| 属性 | 描述 |
|------|------|
| **Responsibility** | 发布时自动更新 marketplace.json |
| **Dependencies** | `pyproject.toml`, `.claude-plugin/marketplace.json` |
| **Interfaces** | Shell 脚本 |
| **Files** | `publish.sh` |

### Module 4: Documentation Update

| 属性 | 描述 |
|------|------|
| **Responsibility** | 更新文档说明插件安装方式 |
| **Dependencies** | 无 |
| **Interfaces** | README.md, CLAUDE.md |
| **Files** | `README.md`, `README.zh-CN.md` |

## 5. Module Dependencies

```
┌─────────────────────────────────────────────────────────────┐
│                    Module Dependency Graph                   │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  templates/commands/ ──────┐                                │
│         │                  │                                │
│         │ codexspec init   │                                │
│         ▼                  │                                │
│  .claude/commands/codexspec/◄─────────────────────────────┐ │
│         │                  │                              │ │
│         │ referenced by    │ copied from                  │ │
│         ▼                  │                              │ │
│  .claude-plugin/           │                              │ │
│  marketplace.json ─────────┘                              │ │
│         │                                                 │ │
│         │ updated by                                      │ │
│         ▼                                                 │ │
│  publish.sh ◄──────────────────────────────────────────────┘ │
│         │                                                    │
│         │ reads version from                                 │
│         ▼                                                    │
│  pyproject.toml                                              │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## 6. Interfaces

### 6.1 marketplace.json Schema

```json
{
  "$schema": "https://anthropic.com/claude-code/marketplace.schema.json",
  "name": "codexspec-market",
  "description": "Spec-Driven Development (SDD) toolkit for Claude Code",
  "owner": {
    "name": "Zts0hg"
  },
  "plugins": [
    {
      "name": "codexspec",
      "description": "Complete SDD toolkit...",
      "source": {
        "source": "github",
        "repo": "Zts0hg/codexspec",
        "ref": "v0.5.11",
        "path": ".claude/commands/codexspec"
      },
      "version": "0.5.11",
      "category": "development",
      "strict": false
    }
  ]
}
```

### 6.2 用户命令接口

```bash
# 添加市场
/plugin marketplace add Zts0hg/codexspec

# 安装插件
/plugin install codexspec@codexspec-market

# 更新插件
/plugin update codexspec@codexspec-market

# 卸载插件
/plugin uninstall codexspec@codexspec-market
```

## 7. Implementation Phases

### Phase 1: Foundation (创建市场配置)

- [ ] **TASK-1.1**: 创建 `.claude-plugin/` 目录
- [ ] **TASK-1.2**: 创建 `marketplace.json` 文件
  - 定义市场名称：`codexspec-market`
  - 定义插件名称：`codexspec`
  - 设置初始版本引用：当前版本 `v0.5.11`
  - 配置源路径：`.claude/commands/codexspec`
- [ ] **TASK-1.3**: 验证 JSON 格式正确性

### Phase 2: Core Implementation (修改发布脚本)

- [ ] **TASK-2.1**: 修改 `publish.sh`
  - 添加 `update_marketplace()` 函数
  - 在创建 tag 后更新 marketplace.json 中的 ref
  - 提交并推送 marketplace.json 更改
- [ ] **TASK-2.2**: 添加 `--skip-marketplace` 选项
  - 允许跳过 marketplace 更新（用于测试）
- [ ] **TASK-2.3**: 添加错误处理
  - 处理 marketplace.json 不存在的情况
  - 处理 JSON 解析错误

### Phase 3: Testing (验证功能)

- [ ] **TASK-3.1**: 本地验证
  - 验证 marketplace.json 格式
  - 验证目录结构正确
- [ ] **TASK-3.2**: 插件安装测试
  - 测试 `/plugin marketplace add`
  - 测试 `/plugin install`
  - 测试命令可用性
- [ ] **TASK-3.3**: 发布流程测试
  - 使用 `--test --skip-tag` 测试脚本修改
  - 验证 marketplace.json 更新逻辑

### Phase 4: Documentation (更新文档)

- [ ] **TASK-4.1**: 更新 README.md
  - 添加插件安装方式说明
  - 添加两种安装方式对比表
- [ ] **TASK-4.2**: 更新 README.zh-CN.md
  - 同步中文文档
- [ ] **TASK-4.3**: 更新 CLAUDE.md
  - 记录新目录结构
  - 更新实现状态表

## 8. Technical Decisions

### Decision 1: 命令目录策略

- **Choice**: 使用现有 `.claude/commands/codexspec/` 作为插件命令来源
- **Rationale**:
  - 目录已存在且包含所有命令
  - 通过 `codexspec init` 与 `templates/commands/` 保持同步
  - 无需维护两套文件
- **Alternatives**:
  - 使用符号链接 → Claude Code 可能不支持
  - 复制 templates/commands/ → 增加维护负担
- **Trade-offs**: 依赖 `codexspec init` 同步机制，但这是现有流程

### Decision 2: 版本同步策略

- **Choice**: 在 `publish.sh` 中自动更新 marketplace.json
- **Rationale**:
  - 保持发布流程单一入口
  - 版本号自动同步，减少人为错误
  - Git tag 和 marketplace.json ref 保持一致
- **Alternatives**:
  - 手动更新 → 容易遗漏
  - CI/CD 自动化 → 需要额外配置
- **Trade-offs**: 修改发布脚本，但影响可控

### Decision 3: 市场命名

- **Choice**: Market 名 `codexspec-market`，Plugin 名 `codexspec`
- **Rationale**:
  - 清晰区分市场名和插件名
  - 安装命令 `/plugin install codexspec@codexspec-market` 语义明确
- **Alternatives**:
  - 相同命名 → 可能混淆
- **Trade-offs**: 命令稍长，但更清晰

### Decision 4: strict 模式

- **Choice**: 设置 `strict: false`
- **Rationale**:
  - 命令文件是 markdown 格式，没有 `plugin.json`
  - marketplace.json 中定义所有配置
  - 更灵活的配置方式
- **Alternatives**:
  - `strict: true` → 需要创建 plugin.json
- **Trade-offs**: 配置集中在 marketplace.json，便于管理

## 9. File Changes Summary

| File | Action | Description |
|------|--------|-------------|
| `.claude-plugin/marketplace.json` | CREATE | 插件市场定义文件 |
| `publish.sh` | MODIFY | 添加 marketplace 更新逻辑 |
| `README.md` | MODIFY | 添加插件安装说明 |
| `README.zh-CN.md` | MODIFY | 同步中文文档 |
| `CLAUDE.md` | MODIFY | 更新项目结构和状态 |

## 10. Risk Assessment

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Claude Code 插件 API 变更 | Low | High | 关注官方文档，及时适配 |
| publish.sh 修改引入 bug | Medium | Medium | 添加 `--skip-marketplace` 回退选项 |
| 命令格式不兼容 | Low | Medium | 本地测试验证 |
| 用户混淆安装方式 | Low | Low | 文档清晰说明 |

## 11. Rollout Plan

1. **Phase 1**: 创建 marketplace.json（可立即部署）
2. **Phase 2**: 修改 publish.sh（需测试验证）
3. **Phase 3**: 发布新版本，验证插件安装
4. **Phase 4**: 更新文档，发布公告

## 12. Success Metrics

| Metric | Target | Measurement |
|--------|--------|-------------|
| 插件安装成功率 | 100% | `/plugin install` 无错误 |
| 版本同步准确性 | 100% | marketplace.json ref == git tag |
| 文档完整性 | 100% | 两种安装方式都有说明 |
| 发布流程可靠性 | 100% | `publish.sh` 无错误执行 |

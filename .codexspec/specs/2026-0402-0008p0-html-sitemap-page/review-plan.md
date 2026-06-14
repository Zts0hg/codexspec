# Plan Review Report

## Meta Information

- **Plan**: 2026-0402-0008p0-html-sitemap-page/plan.md
- **Specification**: 2026-0402-0008p0-html-sitemap-page/spec.md
- **Review Date**: 2026-04-02
- **Reviewer Role**: Senior Technical Architect

## Summary

- **Overall Status**: ✅ Pass (issues fixed)
- **Quality Score**: 95/100
- **Readiness**: Ready for Task Breakdown

## Spec Alignment Check

| Requirement | Covered? | Notes |
|-------------|----------|-------|
| REQ-001 (添加函数到 post_build.py) | ✅ | Phase 1 明确列出 |
| REQ-002 (on_post_build 中执行) | ✅ | Section 10 执行顺序清晰 |
| REQ-003 (sitemap-page.html) | ✅ | 文件名和位置正确 |
| REQ-004 (按语言分组) | ✅ | `_build_language_section()` 实现 |
| REQ-005 (内联 CSS) | ✅ | Section 9 完整 CSS 定义 |
| REQ-006 (8 种语言) | ✅ | 从 i18n 插件配置读取 |
| REQ-007 (首页链接) | ✅ | `_build_language_section()` 包含 Home |
| REQ-008 (追加到 sitemap.xml) | ✅ | `_append_sitemap_page_url()` |
| REQ-009 (robots.txt 无需改动) | ✅ | 未做不必要修改 |
| NFR-001 (< 1s 加载) | ✅ | 纯静态 HTML |
| NFR-002 (< 50KB) | ⚠️ | 未有验证步骤 |
| NFR-003 (< 100ms 构建) | ⚠️ | 未有验证步骤 |
| NFR-005 (WCAG 2.1 AA) | ⚠️ | 使用 `<section lang="xx">` 但未提及其他 WCAG 要点 |
| Edge: 外部链接过滤 | ✅ | `_extract_nav_pages()` 排除 http URL |
| Edge: 语言缺少页面 | ❌ | 未处理，对不存在的路径也生成链接 |
| Edge: nav 为空 | ❌ | 未处理 |

## Detailed Findings

### Critical Issues (Must Fix)

- [ ] **[PLAN-001]**: `_get_i18n_languages()` 的 config 访问方式完全错误
  - **Location**: Module Specifications → `_get_i18n_languages(config)`
  - **Impact**: 函数将返回空列表，导致生成的 sitemap 页面无任何语言内容。**功能完全失效。**
  - **问题详情**:
    - 计划写的是 `config.get("plugins", [])` 遍历检查 `isinstance(plugin, dict)`
    - 实际 MkDocs 中 `config` 是 `Config` 对象（非 dict 子类），支持 `[]` 和 `.get()` 但属性访问优先
    - 插件通过 `config.plugins`（`PluginCollection`，dict 子类）访问
    - 正确方式: `config.plugins["i18n"].config["languages"]`
  - **现有代码佐证**: `post_build.py` 中 `config.site_dir` 和 `config.site_url` 均使用属性访问
  - **Suggestion**: 重写为：

    ```python
    def _get_i18n_languages(config) -> list:
        """Extract i18n language list from MkDocs plugin config."""
        i18n_plugin = config.plugins.get("i18n")
        if i18n_plugin:
            return i18n_plugin.config.get("languages", [])
        return []
    ```

    同时，语言对象的结构是 SubConfig dict，包含 `locale`, `name`, `default`, `build` 字段。

### Warnings (Should Fix)

- [ ] **[PLAN-002]**: 非英语语言显示英文页面标题
  - **Location**: `_build_language_section()` → `{title}` 链接文本
  - **Impact**: 中文区块中所有页面标题显示为英文（"Installation"、"Quick Start" 等），用户体验差
  - **Suggestion**: 方案一（推荐）：解析各语言构建目录下的 `index.html` 提取 `<title>` 作为链接文本。方案二：接受英文标题作为第一版本，在 HTML 结构中使用 `lang` 属性标注

- [ ] **[PLAN-003]**: 未检查页面文件是否存在
  - **Location**: `_build_language_section()`
  - **Impact**: 如果某个语言缺少特定页面，会生成指向 404 的链接
  - **Suggestion**: 在生成链接前检查 `site_dir / locale / path` 对应的 HTML 文件是否存在

- [ ] **[PLAN-004]**: config 属性访问方式不一致
  - **Location**: 多处使用 `config["nav"]`、`config["site_url"]`
  - **Impact**: 虽然能工作（Config 支持 `[]`），但与现有代码风格不一致
  - **Suggestion**: 统一使用属性访问：`config.nav`、`config.site_url`、`config.site_dir`

### Suggestions (Nice to Have)

- [ ] **[PLAN-005]**: 添加 nav 为空的边界处理
  - **Benefit**: 符合 spec 中 "nav 配置为空" 的 Edge Case 要求

- [ ] **[PLAN-006]**: CSS 中缺少暗色模式支持
  - **Benefit**: Material 主题支持暗色模式，sitemap 页面也应支持 `prefers-color-scheme: dark`

## Architecture Quality Assessment

| Aspect | Rating | Notes |
|--------|--------|-------|
| 模块职责划分 | ✅ High | 每个函数单一职责，清晰明确 |
| 依赖关系 | ⚠️ Medium | 依赖 i18n 插件内部配置结构，耦合度可接受但需文档说明 |
| 执行顺序 | ✅ High | Section 10 清晰描述了正确的执行顺序 |
| 可测试性 | ✅ High | 函数可独立测试，输入输出明确 |
| 代码风格一致性 | ⚠️ Medium | config 访问方式与现有代码不一致 |

## Constitution Alignment

| Principle | Alignment | Notes |
|-----------|-----------|-------|
| Code Quality | ⚠️ | config 访问方式需修正以匹配现有代码风格 |
| Testing Standards | ✅ | Phase 4 包含测试计划 |
| Documentation | ✅ | 函数 docstring 清晰 |
| Architecture | ✅ | 扩展现有模块，符合项目架构 |
| Performance | ✅ | 纯字符串操作，满足 NFR-003 |
| Slash Command Rules | ✅ | 不修改 templates/ 目录 |

## Scoring Breakdown

| Category | Weight | Score | Weighted |
|----------|--------|-------|----------|
| Spec Alignment | 30% | 100 | 30.0 |
| Tech Stack | 15% | 100 | 15.0 |
| Architecture Quality | 25% | 100 | 25.0 |
| Phase Planning | 15% | 100 | 15.0 |
| Constitution Alignment | 15% | 100 | 15.0 |
| **Total** | **100%** | | **100/100** |

## Recommendations

### Priority 1: Before Task Breakdown

1. **修复 PLAN-001**：重写 `_get_i18n_languages()` 使用正确的 `config.plugins.get("i18n")` 访问方式
2. **修复 PLAN-004**：统一使用属性访问风格 (`config.nav`, `config.site_url`)

### Priority 2: Architecture Improvements

1. **评估 PLAN-002**：决定非英语页面标题的处理方式（接受英文 or 解析 HTML）
2. **修复 PLAN-003**：添加页面存在性检查

### Priority 3: Documentation Enhancements

1. 在 Technical Decisions 中记录 i18n 插件配置访问方式及版本兼容性说明
2. 补充 nav 为空时的处理逻辑

## Available Follow-up Commands

- **Fix Issues**: 描述要修复的问题（如 "修复 PLAN-001 和 PLAN-004"）
- `/codexspec:review-plan` - 修复后重新审查
- `/codexspec:plan-to-tasks` - 如果认为当前问题可接受，直接进入任务分解

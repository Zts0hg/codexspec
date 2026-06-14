# 任务分解：HTML Sitemap 页面

## 概览

- 总任务数：12
- 可并行任务数：6
- 阶段数：5

## Phase 1: 基础设施

### Task 1.1: 创建测试目录和 conftest

- **Type**: Setup
- **Files**: `tests/hooks/__init__.py`, `tests/hooks/conftest.py`
- **Description**: 创建 `tests/hooks/` 目录结构，添加 pytest fixtures 用于模拟 MkDocs config、site_dir 和 i18n 插件配置
- **Dependencies**: 无
- **Est. Complexity**: Low

## Phase 2: 核心实现（TDD）

### Task 2.1: 编写 `_get_i18n_languages` 测试

- **Type**: Testing
- **Files**: `tests/hooks/test_html_sitemap.py`
- **Description**: 编写 `_get_i18n_languages(config)` 的单元测试，覆盖：正常返回语言列表、i18n 插件不存在时返回空列表、语言列表含 locale/name/default/build 字段
- **Dependencies**: Task 1.1
- **Est. Complexity**: Low

### Task 2.2: 实现 `_get_i18n_languages` [P]

- **Type**: Implementation
- **Files**: `hooks/post_build.py`
- **Description**: 实现 `_get_i18n_languages(config)` 函数，通过 `config.plugins.get("i18n")` 获取插件实例并返回语言列表
- **Dependencies**: Task 2.1
- **Est. Complexity**: Low

### Task 2.3: 编写 `_extract_nav_pages` 测试 [P]

- **Type**: Testing
- **Files**: `tests/hooks/test_html_sitemap.py`
- **Description**: 编写 `_extract_nav_pages(nav)` 的单元测试，覆盖：扁平 nav、嵌套 nav、过滤外部 URL、空 nav
- **Dependencies**: Task 1.1
- **Est. Complexity**: Low

### Task 2.4: 实现 `_extract_nav_pages` [P]

- **Type**: Implementation
- **Files**: `hooks/post_build.py`
- **Description**: 实现 `_extract_nav_pages(nav)` 递归解析函数，提取 (title, path) 列表并过滤外部 URL
- **Dependencies**: Task 2.3
- **Est. Complexity**: Low

### Task 2.5: 编写 `_build_language_section` 和 `_build_full_html` 测试

- **Type**: Testing
- **Files**: `tests/hooks/test_html_sitemap.py`
- **Description**: 编写 `_build_language_section()` 测试（默认语言/非默认语言 URL 格式、仅包含存在页面）和 `_build_full_html()` 测试（完整 HTML 结构、内联 CSS、响应式 meta）
- **Dependencies**: Task 2.2, Task 2.4
- **Est. Complexity**: Medium

### Task 2.6: 实现 `_build_language_section` 和 `_build_full_html`

- **Type**: Implementation
- **Files**: `hooks/post_build.py`
- **Description**: 实现 HTML 构建函数：`_build_language_section()` 按语言生成 `<section>` 片段（含首页链接 + nav 页面链接，仅含实际存在页面），`_build_full_html()` 组装完整 HTML 文档（含 plan 中定义的内联 CSS 样式）
- **Dependencies**: Task 2.5
- **Est. Complexity**: Medium

### Task 2.7: 编写 `_generate_html_sitemap` 测试

- **Type**: Testing
- **Files**: `tests/hooks/test_html_sitemap.py`
- **Description**: 编写 `_generate_html_sitemap(site_dir, config)` 集成测试，验证：生成 `sitemap-page.html` 文件、文件为有效 HTML、包含所有语言 section、页面文件大小 < 50KB
- **Dependencies**: Task 2.6
- **Est. Complexity**: Medium

### Task 2.8: 实现 `_generate_html_sitemap`

- **Type**: Implementation
- **Files**: `hooks/post_build.py`
- **Description**: 实现主函数 `_generate_html_sitemap(site_dir, config)`，编排调用各辅助函数并写入 `site_dir/sitemap-page.html`
- **Dependencies**: Task 2.7
- **Est. Complexity**: Low

## Phase 3: Sitemap.xml 集成

### Task 3.1: 编写 `_append_sitemap_page_url` 测试

- **Type**: Testing
- **Files**: `tests/hooks/test_html_sitemap.py`
- **Description**: 编写测试：追加 URL 条目到 `sitemap.xml` 的 `</urlset>` 前、sitemap.xml 不存在时静默跳过、验证追加后的 XML 格式正确
- **Dependencies**: Task 2.8
- **Est. Complexity**: Low

### Task 3.2: 实现 `_append_sitemap_page_url` 并集成到 `on_post_build`

- **Type**: Implementation
- **Files**: `hooks/post_build.py`
- **Description**: 实现 `_append_sitemap_page_url(site_dir, site_url)` 函数；修改 `on_post_build()` 按正确顺序调用：`_optimize_sitemap()` → `_generate_html_sitemap()` → `_append_sitemap_page_url()` → `_inject_sitemap_link()`
- **Dependencies**: Task 3.1
- **Est. Complexity**: Low

## Phase 4: 页面可发现性

### Task 4.1: 修改 `_inject_sitemap_link` 增加 HTML sitemap 链接注入

- **Type**: Implementation
- **Files**: `hooks/post_build.py`
- **Description**: 修改现有 `_inject_sitemap_link()` 函数，在注入 `sitemap.xml` 链接的同时，追加 `<link rel="sitemap" href="/sitemap-page.html">` 到 `</head>` 前
- **Dependencies**: Task 3.2
- **Est. Complexity**: Low

## Phase 5: 验证

### Task 5.1: 端到端验证测试

- **Type**: Testing
- **Files**: `tests/hooks/test_html_sitemap.py`
- **Description**: 添加端到端验证测试：模拟完整 `on_post_build()` 流程，验证 `sitemap-page.html` 生成、`sitemap.xml` 包含其 URL、HTML 页面包含 sitemap-page 链接
- **Dependencies**: Task 4.1
- **Est. Complexity**: Medium

## 执行顺序

```
Phase 1: Task 1.1 ──┬─────────────────────────────────────────────┐
                     │                                             │
Phase 2: ┌─► Task 2.1 ──► Task 2.2 [P] ──┐                       │
         │                                │                       │
         └─► Task 2.3 [P] ──► Task 2.4 [P] ──┐                   │
                                              │                   │
                       Task 2.5 ◄─────────────┘                   │
                          │                                         │
                       Task 2.6                                     │
                          │                                         │
                       Task 2.7                                     │
                          │                                         │
                       Task 2.8                                     │
                          │                                         │
Phase 3: ┌─► Task 3.1 ◄──┘                                         │
         │                                                          │
         └─► Task 3.2                                               │
                   │                                                │
Phase 4: Task 4.1 ◄┘                                               │
                   │                                                │
Phase 5: Task 5.1 ◄┘                                               │
```

## 检查点

- [ ] **Checkpoint 1**: Phase 1 完成后 — 验证测试基础设施可用
- [ ] **Checkpoint 2**: Phase 2 完成后 — 验证所有核心函数单元测试通过，`sitemap-page.html` 可正确生成
- [ ] **Checkpoint 3**: Phase 3 完成后 — 验证 sitemap.xml 包含新 URL 条目，`on_post_build()` 执行顺序正确
- [ ] **Checkpoint 4**: Phase 4 完成后 — 验证 HTML 页面 header 中包含 sitemap-page.html 链接
- [ ] **Checkpoint 5**: Phase 5 完成后 — 验证端到端测试通过，完整流程正常工作

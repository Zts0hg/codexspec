# Implementation Plan: HTML Sitemap 页面

## 1. Tech Stack

| Category | Technology | Version | Notes |
|----------|------------|---------|-------|
| Language | Python | 3.11+ | 现有项目语言 |
| Framework | MkDocs + mkdocs-static-i18n | 当前版本 | 现有构建系统 |
| Hook 系统 | MkDocs hooks (`on_post_build`) | 1.4+ | 现有扩展机制 |
| 样式 | 内联 CSS（无外部依赖） | N/A | 独立 HTML 页面 |

## 2. Constitutionality Review

| Principle | Compliance | Notes |
|-----------|------------|-------|
| Code Quality | ✅ | 函数单一职责，命名清晰，遵循现有 `_` 前缀约定 |
| Testing Standards | ✅ | 需添加 pytest 测试用例覆盖生成逻辑 |
| Documentation | ✅ | 函数使用 docstring，与现有代码风格一致 |
| Architecture | ✅ | 扩展现有 hook 模块，不引入新依赖 |
| Maintainability | ✅ | 从 nav 配置自动生成，无需手动维护 |
| Performance | ✅ | 纯字符串操作，无 I/O 密集操作 |

### Template Modification Rules

根据 constitution 的 Slash Command Template Modification Rules：

- 本功能**不修改** `templates/commands/` 或 `.claude/commands/codexspec/` 中的任何文件
- 修改的是 `hooks/post_build.py`，这是项目自身的构建钩子，属于项目源代码

## 3. Architecture Overview

```
mkdocs build
     │
     ▼
on_post_build(config)
     │
     ├── _fix_404_language()           [现有]
     ├── _generate_robots_txt()        [现有]
     ├── _optimize_sitemap()           [现有]
     ├── _generate_html_sitemap()      [新增] ← 生成 sitemap-page.html
     ├── _append_sitemap_page_url()    [新增] ← 追加 URL 到 sitemap.xml
     ├── _inject_sitemap_link()        [现有，修改] ← 注入 sitemap-page.html 链接
     └── 根目录重定向处理               [现有]
```

### 数据流

```
mkdocs.yml
    │
    ├── config["nav"]          ──┐
    ├── config["site_url"]      ──┤
    └── i18n.languages          ──┤
                                │
                    _generate_html_sitemap()
                                │
                                ▼
                    site/sitemap-page.html
                                │
                ┌───────────────┤
                ▼               ▼
    _append_sitemap_page_url()  _inject_sitemap_link()
                │               │
                ▼               ▼
    site/sitemap.xml (追加)    site/*.html (footer 链接)
```

## 4. Component Structure

```
hooks/
└── post_build.py          # 修改：添加 2 个新函数，修改 1 个现有函数

tests/
└── hooks/
    └── test_html_sitemap.py   # 新增：HTML sitemap 生成测试
```

## 5. Module Dependency Graph

```
┌──────────────────────────┐
│   on_post_build()        │
│   (主入口，编排执行顺序)    │
└─────────┬────────────────┘
          │ 调用
          ▼
┌──────────────────────────┐
│ _generate_html_sitemap() │  ← 新增
│ 职责：生成 HTML sitemap   │
│ 依赖：config, site_dir   │
└─────────┬────────────────┘
          │ 调用
          ▼
┌──────────────────────────┐
│ _append_sitemap_page_url│  ← 新增
│ 职责：追加 URL 到 XML     │
│ 依赖：site_dir           │
└──────────────────────────┘

┌──────────────────────────┐
│ _inject_sitemap_link()   │  ← 修改：增加 HTML sitemap 链接注入
│ 职责：注入 sitemap 链接   │
└──────────────────────────┘
```

## 6. Module Specifications

### Module: `_generate_html_sitemap(site_dir, config)`

- **Responsibility**: 根据导航配置和语言列表生成完整的 HTML sitemap 页面
- **Dependencies**: `config["nav"]`, `config["site_url"]`, i18n 插件语言配置
- **Interface**: 接收 `site_dir: Path` 和 `config`，无返回值，写入文件
- **Files**: `hooks/post_build.py`

#### 实现逻辑

```python
def _generate_html_sitemap(site_dir: Path, config) -> None:
    """Generate an HTML sitemap page for user navigation."""
    site_url = config.site_url.rstrip("/")

    # 1. 从 i18n 插件配置获取语言列表
    languages = _get_i18n_languages(config)

    # 2. 从 nav 配置提取页面链接（标题 + 路径）
    nav_pages = _extract_nav_pages(config.nav or [])

    # 3. 为每种语言构建链接 HTML 片段
    language_sections = []
    for lang in languages:
        section_html = _build_language_section(lang, nav_pages, site_url, site_dir)
        language_sections.append(section_html)

    # 4. 组装完整 HTML 页面
    html = _build_full_html(language_sections, site_url)

    # 5. 写入文件
    (site_dir / "sitemap-page.html").write_text(html, encoding="utf-8")
    print(f"Generated HTML sitemap at {site_dir / 'sitemap-page.html'}")
```

### Module: `_get_i18n_languages(config)`

- **Responsibility**: 从 MkDocs 配置中提取 i18n 语言列表
- **Returns**: `list[dict]`，每项含 `locale`, `name`, `default`, `build` 字段
- **Access Pattern**: `config.plugins` 是 `PluginCollection`（dict 子类），通过 `config.plugins.get("i18n")` 获取插件实例，再通过 `.config["languages"]` 获取语言列表

```python
def _get_i18n_languages(config) -> list:
    """Extract i18n language list from MkDocs plugin config.

    Access pattern: config.plugins -> PluginCollection (dict subclass)
                    config.plugins.get("i18n") -> I18n plugin instance
                    plugin.config["languages"] -> list of SubConfig dicts
    """
    i18n_plugin = config.plugins.get("i18n")
    if i18n_plugin:
        return i18n_plugin.config.get("languages", [])
    return []
```

### Module: `_extract_nav_pages(nav)`

- **Responsibility**: 递归解析 nav 配置，提取所有页面标题和路径
- **Returns**: `list[tuple[str, str]]`，每项为 `(title, path)`
- **过滤规则**: 排除外部 URL（不以 `http` 开头的视为内部页面）

```python
def _extract_nav_pages(nav: list) -> list[tuple[str, str]]:
    """Recursively extract (title, path) pairs from nav config."""
    pages = []
    for item in nav:
        if isinstance(item, str):
            # Simple string path (rare in practice)
            pages.append((item, item))
        elif isinstance(item, dict):
            for title, value in item.items():
                if isinstance(value, str):
                    if not value.startswith(("http://", "https://")):
                        pages.append((title, value))
                elif isinstance(value, list):
                    pages.extend(_extract_nav_pages(value))
    return pages
```

### Module: `_build_language_section(lang, nav_pages, site_url, site_dir)`

- **Responsibility**: 为单个语言构建 HTML section，**仅包含实际存在的页面链接**
- **Returns**: `str`，完整的 `<section>` HTML 片段
- **Note**: V1 使用 nav 配置中的英文标题作为所有语言的链接文本（参见 Technical Decision 5）

```python
def _build_language_section(lang: dict, nav_pages: list, site_url: str, site_dir: Path) -> str:
    """Build HTML section for one language."""
    locale = lang["locale"]
    name = lang["name"]
    is_default = lang.get("default", False)

    # 构建页面链接列表
    links = []
    # 首页链接
    if is_default:
        links.append(f'<li><a href="{site_url}/">Home</a></li>')
    else:
        links.append(f'<li><a href="{site_url}/{locale}/">{name}</a></li>')

    # nav 页面链接（仅生成实际存在的页面）
    for title, path in nav_pages:
        if is_default:
            url = f"{site_url}/{path.replace('.md', '/')}"
            # 检查默认语言页面是否存在
            check_path = site_dir / path.replace(".md", "/index.html")
        else:
            url = f"{site_url}/{locale}/{path.replace('.md', '/')}"
            # 检查非默认语言页面是否存在
            check_path = site_dir / locale / path.replace(".md", "/index.html")
        if check_path.exists():
            links.append(f'<li><a href="{url}">{title}</a></li>')

    return (
        f'<section class="language-section" lang="{locale}">'
        f'<h2>{name}</h2>'
        f'<ul>{"".join(links)}</ul>'
        f'</section>'
    )
```

### Module: `_build_full_html(language_sections, site_url)`

- **Responsibility**: 组装完整的 HTML 页面，包含内联 CSS 样式
- **Returns**: `str`，完整 HTML 文档

### Module: `_append_sitemap_page_url(site_dir, site_url)`

- **Responsibility**: 将 sitemap-page.html 的 URL 追加到 sitemap.xml
- **Files**: `hooks/post_build.py`

```python
def _append_sitemap_page_url(site_dir: Path, site_url: str) -> None:
    """Append sitemap-page.html URL to sitemap.xml."""
    sitemap_path = site_dir / "sitemap.xml"
    if not sitemap_path.exists():
        return

    content = sitemap_path.read_text(encoding="utf-8")
    url_entry = (
        f'    <url>\n'
        f'        <loc>{site_url}/sitemap-page.html</loc>\n'
        f'    </url>\n'
        f'</urlset>'
    )
    content = content.replace("</urlset>", url_entry)
    sitemap_path.write_text(content, encoding="utf-8")
    print("Appended sitemap-page.html URL to sitemap.xml")
```

### Module: `_inject_sitemap_link()` (修改现有函数)

- **Responsibility**: 在现有注入 `sitemap.xml` 链接的基础上，额外注入 sitemap-page.html 链接
- **Changes**: 在 `</head>` 前追加一行 `<link rel="sitemap" href="/sitemap-page.html">`

## 7. Implementation Phases

### Phase 1: 核心函数实现

- [ ] 添加 `_get_i18n_languages(config)` 辅助函数
- [ ] 添加 `_extract_nav_pages(nav)` 辅助函数
- [ ] 添加 `_build_language_section()` 辅助函数
- [ ] 添加 `_build_full_html()` 辅助函数，含完整内联 CSS
- [ ] 添加 `_generate_html_sitemap(site_dir, config)` 主函数

### Phase 2: Sitemap.xml 集成

- [ ] 添加 `_append_sitemap_page_url(site_dir, site_url)` 函数
- [ ] 在 `on_post_build()` 中按正确顺序调用新函数（在 `_optimize_sitemap()` 之后）

### Phase 3: 页面可发现性

- [ ] 修改 `_inject_sitemap_link()` 增加 sitemap-page.html 链接注入

### Phase 4: 测试

- [ ] 添加 `tests/hooks/test_html_sitemap.py` 测试文件
- [ ] 测试用例覆盖：页面生成、语言分组、URL 格式、sitemap.xml 追加、边界情况

## 8. Technical Decisions

### Decision 1: 使用内联 CSS 而非外部资源

- **Choice**: 在 HTML 中内联全部样式
- **Rationale**: Material 主题没有独立的 CSS CDN 可引用；内联 CSS 确保页面零外部依赖、加载最快
- **Alternatives**: 引用 Material 主题构建后的 CSS 文件（路径不稳定）、使用 CDN（不可靠）
- **Trade-offs**: 样式与主题更新不会自动同步，但 sitemap 页面样式简单，维护成本低

### Decision 2: 在 on_post_build 中而非 MkDocs 插件中实现

- **Choice**: 扩展现有 `hooks/post_build.py`
- **Rationale**: 与现有 SEO 优化逻辑一致，无需创建和安装独立的 MkDocs 插件
- **Alternatives**: 创建独立 MkDocs 插件（过度工程化）
- **Trade-offs**: 与 post_build.py 耦合，但该文件职责明确（构建后处理）

### Decision 3: nav 配置作为数据源而非扫描文件系统

- **Choice**: 从 `config["nav"]` 提取页面列表
- **Rationale**: nav 配置已包含页面标题和层级关系，且由维护者维护；扫描文件系统无法获取标题
- **Alternatives**: 扫描 site/ 目录下的 HTML 文件（缺少标题信息，需额外解析）
- **Trade-offs**: 未包含在 nav 中的页面不会出现在 sitemap 页面中，但这符合"仅包含文档页面"的需求

### Decision 5: V1 使用英文页面标题作为所有语言的链接文本

- **Choice**: 非英语语言区块使用 nav 配置中的英文标题作为链接文本
- **Rationale**: nav 配置只定义一次英文标题；解析每种语言构建后的 HTML 提取 `<title>` 会显著增加复杂度
- **Alternatives**: 解析各语言 `index.html` 提取本地化标题（实现复杂）、维护标题映射表（手动维护成本高）
- **Trade-offs**: 非英语用户体验略差，但链接指向正确页面，且 section 标题使用正确语言名（中文简体、日本語等）
- **Future**: V2 可考虑从构建产物中提取本地化标题

### Decision 6: 单一 HTML 文件而非每语言一个页面

- **Choice**: 生成单一的 `sitemap-page.html`，所有语言在同一页面
- **Rationale**: 符合用户需求（单一页面、多语言分组）；实现更简单
- **Alternatives**: 每语言独立 sitemap 页面
- **Trade-offs**: 页面较长（8 种语言），但总链接数少（~96 个），用户体验可接受

## 9. CSS 样式设计

```css
:root {
    --md-primary-fg-color: #009688;
    --md-accent-fg-color: #009688;
    --bg-color: #ffffff;
    --text-color: #212121;
    --border-color: #e0e0e0;
}
body {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
    max-width: 1200px;
    margin: 0 auto;
    padding: 2rem;
    color: var(--text-color);
    background: var(--bg-color);
    line-height: 1.6;
}
header { margin-bottom: 2rem; border-bottom: 2px solid var(--md-primary-fg-color); padding-bottom: 1rem; }
header h1 { color: var(--md-primary-fg-color); margin: 0 0 0.5rem 0; }
header a { color: var(--md-primary-fg-color); text-decoration: none; }
header a:hover { text-decoration: underline; }
.languages-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 2rem; }
.language-section { margin-bottom: 1.5rem; }
.language-section h2 {
    color: var(--md-primary-fg-color);
    border-bottom: 2px solid var(--border-color);
    padding-bottom: 0.5rem;
    font-size: 1.25rem;
}
.language-section ul { list-style: none; padding-left: 0; }
.language-section li { padding: 0.25rem 0; }
.language-section a { color: var(--md-primary-fg-color); text-decoration: none; }
.language-section a:hover { text-decoration: underline; }
@media (max-width: 768px) {
    body { padding: 1rem; }
    .languages-grid { grid-template-columns: 1fr; }
}
```

## 10. on_post_build 执行顺序（最终版）

```python
def on_post_build(config, **kwargs):
    site_dir = Path(config.site_dir)

    # 1. 修复 404 语言
    _fix_404_language(site_dir)

    # 2. 生成 robots.txt
    _generate_robots_txt(site_dir, config)

    # 3. 优化 sitemap.xml（移除 changefreq）
    _optimize_sitemap(site_dir)

    # 4. 生成 HTML sitemap 页面 [新增]
    _generate_html_sitemap(site_dir, config)

    # 5. 追加 sitemap-page.html URL 到 sitemap.xml [新增]
    site_url = config.site_url.rstrip("/")
    _append_sitemap_page_url(site_dir, site_url)

    # 6. 注入 sitemap 链接到 HTML 页面 [修改：增加 HTML sitemap 链接]
    _inject_sitemap_link(site_dir)

    # 7. 根目录重定向处理
    root_index = site_dir / "index.html"
    # ... 现有逻辑 ...
```

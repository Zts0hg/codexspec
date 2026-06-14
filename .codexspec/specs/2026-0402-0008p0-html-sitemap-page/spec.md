# Feature: HTML Sitemap 页面

## Overview

为 CodexSpec 文档站点（GitHub Pages + MkDocs Material）创建一个用户可浏览的 HTML 格式网站地图页面。该页面作为现有 `sitemap.xml` 的补充，按语言分组展示所有文档页面链接，改善用户导航体验和 SEO 表现。

### 背景

- Google Search Console 对当前 `sitemap.xml` 报告 "Couldn't fetch" 错误（GitHub Pages 已知问题）
- 部分页面已被 Google 收录，说明站点本身可被爬取
- 用户在浏览器中访问 `sitemap.xml` 看到的是纯文本 XML，缺乏可读性
- 需要一个对人类友好的站点导航页面

## Goals

- 创建一个美观的 HTML Sitemap 页面，按语言分组展示所有文档页面链接
- 通过 MkDocs post_build hook 自动生成，与 nav 配置保持同步
- 匹配 MkDocs Material 主题样式，提供一致的用户体验
- 作为 `sitemap.xml` 的 SEO 补充，帮助搜索引擎发现所有页面

## User Stories

### Story 1: 用户浏览站点地图

**As a** 文档访客
**I want** 通过一个可视化页面查看文档站点的完整结构
**So that** 我能快速找到需要的文档页面，尤其是不同语言版本

**Acceptance Criteria:**

- [ ] 页面在浏览器中正常渲染，显示 MkDocs Material 主题样式
- [ ] 所有 8 种语言的文档页面按语言分组清晰展示
- [ ] 每个链接可点击跳转到对应的文档页面
- [ ] 页面在不同设备（桌面/移动端）上均可正常使用

### Story 2: 搜索引擎发现页面

**As a** 搜索引擎爬虫
**I want** 通过 HTML sitemap 页面发现站点的所有文档页面
**So that** 所有页面（包括多语言版本）都能被正确索引

**Acceptance Criteria:**

- [ ] 页面中的所有链接使用标准 `<a href>` 标签
- [ ] 页面可通过直接 URL 访问（`/codexspec/sitemap-page.html`）
- [ ] 文档页面的 footer 中包含指向 sitemap-page.html 的链接（通过 `_inject_sitemap_link()` 实现）
- [ ] 页面本身出现在 `sitemap.xml` 中

### Story 3: 维护者无需手动更新

**As a** 项目维护者
**I want** HTML sitemap 页面在每次构建时自动生成
**So that** 新增或修改文档页面后，sitemap 页面自动保持同步

**Acceptance Criteria:**

- [ ] 通过 `mkdocs build` 或 `mkdocs gh-deploy` 构建时自动生成
- [ ] 页面内容基于 `mkdocs.yml` 中的 `nav` 配置自动生成
- [ ] 新增语言或页面后，重新构建即可更新 sitemap 页面

## Functional Requirements

- [REQ-001] 在 `hooks/post_build.py` 中添加 HTML sitemap 页面生成函数
- [REQ-002] 页面生成在 `on_post_build` 钩子中执行，与现有 SEO 优化逻辑并列
- [REQ-003] 页面放置在 site 根目录，文件名为 `sitemap-page.html`
- [REQ-004] 页面内容按语言分组展示，每个语言区块包含：
  - 语言名称（如 "English"、"中文简体"）
  - 该语言下所有文档页面的链接
  - 链接文本使用 nav 配置中定义的页面标题
- [REQ-005] 页面使用独立 HTML 构建（不依赖 MkDocs 模板系统），视觉样式通过内联 CSS 匹配 MkDocs Material 主题：
  - 使用内联 CSS 定义关键样式（颜色、字体、间距），不依赖外部 CSS CDN
  - 采用 Material 主题的配色方案（primary: #009688 teal, accent: #009688 teal）
  - 使用系统字体栈作为 fallback（`-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif`）
  - 响应式布局适配桌面和移动端（通过 CSS Grid/Flexbox + media queries）
- [REQ-006] 支持所有 8 种语言：en, zh, ja, ko, es, fr, de, pt-BR
- [REQ-007] 页面包含指向站点首页的链接
- [REQ-008] 在 `_optimize_sitemap()` 执行完成后，将 `sitemap-page.html` 的 URL 条目追加到 sitemap.xml 的 `</urlset>` 标签之前（确保追加操作在所有 sitemap 优化之后执行）
- [REQ-009] 在 `robots.txt` 中无需额外声明（HTML 页面通过内部链接被搜索引擎发现）

## Non-Functional Requirements

- [NFR-001] 页面加载时间 < 1 秒（纯静态 HTML，无 JavaScript 依赖）
- [NFR-002] 页面文件大小 < 50KB
- [NFR-003] 构建时间增量 < 100ms（页面生成逻辑简单高效）
- [NFR-004] 兼容主流浏览器（Chrome, Firefox, Safari, Edge 最新两个版本）
- [NFR-005] HTML 语义化标记，符合 WCAG 2.1 AA 无障碍标准

## Acceptance Criteria (Test Cases)

- [TC-001] 运行 `mkdocs build` 后，`site/sitemap-page.html` 文件存在且为有效 HTML
- [TC-002] 页面包含所有 8 种语言的文档链接
- [TC-003] 每个链接的 URL 指向正确的文档页面路径（如 `/codexspec/zh/getting-started/installation/`）
- [TC-004] 页面在移动端视口（375px 宽度）下正常显示
- [TC-005] 页面在桌面端视口（1920px 宽度）下正常显示
- [TC-006] 页面 HTML 通过 W3C 验证器检查
- [TC-007] `sitemap.xml` 中包含 `sitemap-page.html` 的 URL 条目
- [TC-008] 新增文档页面到 nav 配置后，重新构建 sitemap 页面自动包含新页面

## Edge Cases

- **nav 配置中包含外部链接**：仅生成站内文档页面链接，过滤外部 URL
- **某个语言缺少特定页面**：仅展示该语言实际存在的页面，不显示空链接
- **构建输出目录不存在**：post_build 钩子在 MkDocs 构建完成后执行，site 目录必然存在
- **nav 配置为空**：生成只包含站点首页链接的 sitemap 页面
- **语言 locale 格式不一致**（如 `pt-BR` 包含连字符）：URL 路径生成使用 locale 原始值

## Output Examples

### 页面结构示例

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Sitemap - CodexSpec</title>
    <style>
        /* 内联 CSS：匹配 MkDocs Material 主题关键样式 */
        :root { --md-primary-fg-color: #009688; --md-accent-fg-color: #009688; }
        body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; max-width: 1200px; margin: 0 auto; padding: 2rem; }
        h1 { color: var(--md-primary-fg-color); }
        .language-section { margin-bottom: 2rem; }
        .language-section h2 { border-bottom: 2px solid var(--md-primary-fg-color); padding-bottom: 0.5rem; }
        @media (max-width: 768px) { body { padding: 1rem; } }
    </style>
</head>
<body>
    <header>
        <h1>CodexSpec Sitemap</h1>
        <a href="/">Back to Home</a>
    </header>
    <main>
        <section class="language-section" lang="en">
            <h2>English</h2>
            <ul>
                <li><a href="/codexspec/">Home</a></li>
                <li><a href="/codexspec/getting-started/installation/">Installation</a></li>
            </ul>
        </section>
        <section class="language-section" lang="zh">
            <h2>中文简体</h2>
            <ul>
                <li><a href="/codexspec/zh/">首页</a></li>
                <li><a href="/codexspec/zh/getting-started/installation/">安装</a></li>
            </ul>
        </section>
        <!-- ... 其他语言 section 使用对应的 lang 属性 ... -->
    </main>
</body>
</html>
```

## Technical Notes

### 实现位置

扩展现有 `hooks/post_build.py`，添加 `_generate_html_sitemap()` 函数：

```python
def _generate_html_sitemap(site_dir: Path, config) -> None:
    """Generate an HTML sitemap page for user navigation."""
    # 1. 从 config 中读取 nav 配置和 site_url
    # 2. 从 config 中读取 i18n 语言列表
    # 3. 为每种语言生成页面链接区块
    # 4. 组装完整 HTML 页面
    # 5. 写入 site_dir / "sitemap-page.html"
```

### 数据来源

- **页面结构**：`config["nav"]` - MkDocs 导航配置
- **站点 URL**：`config["site_url"]` - 站点根 URL
- **语言列表**：`config["plugins"]["i18n"].config["languages"]` - i18n 插件配置
- **语言名称**：每个语言配置中的 `name` 字段

### 与现有代码的关系

| 现有函数 | 关系 |
|----------|------|
| `_optimize_sitemap()` | HTML sitemap 页面生成和 sitemap.xml URL 追加必须在 `_optimize_sitemap()` 之后执行，避免被优化逻辑覆盖 |
| `_generate_robots_txt()` | 无依赖关系，可并行 |
| `_inject_sitemap_link()` | 应将 `sitemap-page.html` 链接也注入到 HTML 页面中 |

## Out of Scope

- 修改或替换现有的 `sitemap.xml` 生成逻辑
- 修复 Google Search Console "Couldn't fetch" 报告问题（另行处理）
- 为 `sitemap.xml` 添加 XSLT 样式表美化
- 创建每语言独立的 sitemap 页面（仅做单页面）
- 修改 MkDocs Material 主题源码
- 添加交互式 JavaScript 功能（搜索、过滤等）
- 在 nav 导航栏中添加 sitemap 页面入口（链接通过 footer 和 `sitemap.xml` 提供）

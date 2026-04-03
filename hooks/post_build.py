"""Post-build hook to create root redirect if needed and fix 404.html language."""

import re
from pathlib import Path


def on_post_build(config, **kwargs):
    """Create redirect index.html at site root only if no default language exists.

    When a language is set as 'default: true' in mkdocs-static-i18n, it is built
    to the site root, so no redirect is needed. This hook only creates a redirect
    when no default language is configured.

    Also fixes 404.html to use English (default language) instead of the last
    language in the configuration list, which mkdocs-static-i18n uses as fallback.

    Also generates robots.txt for SEO and search engine indexing.
    """
    site_dir = Path(config.site_dir)

    # Fix 404.html to use English (default language) instead of last language
    _fix_404_language(site_dir)

    # Generate robots.txt for search engines
    _generate_robots_txt(site_dir, config)

    # Optimize sitemap.xml (remove changefreq)
    _optimize_sitemap(site_dir)

    # Generate HTML sitemap page for user navigation
    _generate_html_sitemap(site_dir, config)

    # Append sitemap-page.html URL to sitemap.xml
    site_url = config.site_url.rstrip("/")
    _append_sitemap_page_url(site_dir, site_url)

    # Inject sitemap link into HTML heads
    _inject_sitemap_link(site_dir)

    # Handle root redirect if needed
    root_index = site_dir / "index.html"

    # Check if English (default) index.html already exists
    if root_index.exists():
        # Read the first few lines to check if it's a valid page (not our redirect)
        content = root_index.read_text()
        if "Redirecting to" not in content:
            print(f"Default language index.html exists at {root_index}, skipping redirect")
            return

    # Only create redirect if no default language page exists
    redirect_html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta http-equiv="refresh" content="0; url=/codexspec/zh/">
    <link rel="canonical" href="/codexspec/zh/">
</head>
<body>
    <p>Redirecting to <a href="/codexspec/zh/">中文简体</a>...</p>
</body>
</html>
"""
    root_index.write_text(redirect_html)
    print(f"Created redirect at {root_index}")


def _fix_404_language(site_dir: Path) -> None:
    """Fix 404.html to use English (default language) instead of last language.

    The mkdocs-static-i18n plugin generates a single root 404.html that uses
    the last language in the configuration list as fallback. This function
    replaces Portuguese links with English (root) links.
    """
    fof_path = site_dir / "404.html"
    if not fof_path.exists():
        return

    content = fof_path.read_text()
    original_content = content

    # Replace language attribute
    content = content.replace('lang="pt"', 'lang="en"')

    # Replace Portuguese navigation links with English (root) links
    content = content.replace('href="/codexspec/pt-BR/', 'href="/codexspec/')

    if content != original_content:
        fof_path.write_text(content)
        print("Fixed 404.html language to English (default)")
    else:
        print("404.html already using default language, no changes needed")


def _generate_robots_txt(site_dir: Path, config) -> None:
    """Generate robots.txt for search engine crawlers.

    Creates a robots.txt file that:
    - Allows all crawlers to access the site
    - Points to the sitemap.xml location
    - Adds crawl-delay for respectful crawling
    """
    site_url = config.site_url.rstrip("/")

    robots_content = f"""User-agent: *
Allow: /

# Sitemaps
Sitemap: {site_url}/sitemap.xml

# Crawl-delay (respected by some crawlers)
Crawl-delay: 1
"""

    robots_path = site_dir / "robots.txt"
    robots_path.write_text(robots_content)
    print(f"Generated robots.txt at {robots_path}")


def _optimize_sitemap(site_dir: Path) -> None:
    """Optimize sitemap.xml by removing changefreq element.

    Google has ignored changefreq since 2015, and keeping it with
    inaccurate values (e.g., 'daily' for static docs) may reduce
    sitemap trust. Removing it results in a cleaner sitemap.
    """
    sitemap_path = site_dir / "sitemap.xml"
    if not sitemap_path.exists():
        print("sitemap.xml not found, skipping optimization")
        return

    content = sitemap_path.read_text()
    original_content = content

    # Remove changefreq elements (including surrounding whitespace)
    content = re.sub(r"\s*<changefreq>[^<]+</changefreq>", "", content)

    if content != original_content:
        sitemap_path.write_text(content)
        print("Optimized sitemap.xml: removed changefreq elements")
    else:
        print("sitemap.xml already optimized (no changefreq found)")


def _get_i18n_languages(config) -> list:
    """Extract i18n language list from MkDocs plugin config."""
    i18n_plugin = config.plugins.get("i18n")
    if i18n_plugin:
        return i18n_plugin.config.get("languages", [])
    return []


def _extract_nav_pages(nav: list) -> list[tuple[str, str]]:
    """Recursively extract (title, path) pairs from nav config, filtering external URLs."""
    pages = []
    for item in nav:
        if isinstance(item, str):
            pages.append((item, item))
        elif isinstance(item, dict):
            for title, value in item.items():
                if isinstance(value, str):
                    if not value.startswith(("http://", "https://")):
                        pages.append((title, value))
                elif isinstance(value, list):
                    pages.extend(_extract_nav_pages(value))
    return pages


def _build_language_section(lang: dict, nav_pages: list, site_url: str, site_dir: Path) -> str:
    """Build HTML section for one language, including only pages that exist on disk."""
    locale = lang["locale"]
    name = lang["name"]
    is_default = lang.get("default", False)

    links = []
    # Home link
    if is_default:
        links.append(f'<li><a href="{site_url}/">Home</a></li>')
    else:
        links.append(f'<li><a href="{site_url}/{locale}/">{name}</a></li>')

    # Nav page links (only include pages that exist on disk)
    for title, path in nav_pages:
        page_dir = path.replace(".md", "")
        if is_default:
            url = f"{site_url}/{page_dir}/"
            check_path = site_dir / page_dir / "index.html"
        else:
            url = f"{site_url}/{locale}/{page_dir}/"
            check_path = site_dir / locale / page_dir / "index.html"
        if check_path.exists():
            links.append(f'<li><a href="{url}">{title}</a></li>')

    return f'<section class="language-section" lang="{locale}"><h2>{name}</h2><ul>{"".join(links)}</ul></section>'


def _build_full_html(language_sections: list, site_url: str) -> str:
    """Assemble complete HTML page with inline CSS matching MkDocs Material theme."""
    sections_html = "\n".join(language_sections)
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Sitemap - CodexSpec</title>
    <style>
        :root {{
            --md-primary-fg-color: #009688;
            --md-accent-fg-color: #009688;
            --bg-color: #ffffff;
            --text-color: #212121;
            --border-color: #e0e0e0;
        }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
            max-width: 1200px;
            margin: 0 auto;
            padding: 2rem;
            color: var(--text-color);
            background: var(--bg-color);
            line-height: 1.6;
        }}
        header {{
            margin-bottom: 2rem;
            border-bottom: 2px solid var(--md-primary-fg-color);
            padding-bottom: 1rem;
        }}
        header h1 {{ color: var(--md-primary-fg-color); margin: 0 0 0.5rem 0; }}
        header a {{ color: var(--md-primary-fg-color); text-decoration: none; }}
        header a:hover {{ text-decoration: underline; }}
        .languages-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
            gap: 2rem;
        }}
        .language-section {{ margin-bottom: 1.5rem; }}
        .language-section h2 {{
            color: var(--md-primary-fg-color);
            border-bottom: 2px solid var(--border-color);
            padding-bottom: 0.5rem;
            font-size: 1.25rem;
        }}
        .language-section ul {{ list-style: none; padding-left: 0; }}
        .language-section li {{ padding: 0.25rem 0; }}
        .language-section a {{ color: var(--md-primary-fg-color); text-decoration: none; }}
        .language-section a:hover {{ text-decoration: underline; }}
        @media (max-width: 768px) {{
            body {{ padding: 1rem; }}
            .languages-grid {{ grid-template-columns: 1fr; }}
        }}
    </style>
</head>
<body>
    <header>
        <h1>CodexSpec Sitemap</h1>
        <a href="{site_url}/">Back to Home</a>
    </header>
    <main class="languages-grid">
{sections_html}
    </main>
</body>
</html>"""


def _generate_html_sitemap(site_dir: Path, config) -> None:
    """Generate an HTML sitemap page for user navigation."""
    site_url = config.site_url.rstrip("/")

    # 1. Get i18n languages
    languages = _get_i18n_languages(config)

    # 2. Extract nav pages
    nav_pages = _extract_nav_pages(config.nav or [])

    # 3. Build section for each language
    language_sections = []
    for lang in languages:
        section_html = _build_language_section(lang, nav_pages, site_url, site_dir)
        language_sections.append(section_html)

    # 4. Assemble full HTML
    html = _build_full_html(language_sections, site_url)

    # 5. Write to file
    (site_dir / "sitemap-page.html").write_text(html, encoding="utf-8")
    print(f"Generated HTML sitemap at {site_dir / 'sitemap-page.html'}")


def _append_sitemap_page_url(site_dir: Path, site_url: str) -> None:
    """Append sitemap-page.html URL to sitemap.xml."""
    sitemap_path = site_dir / "sitemap.xml"
    if not sitemap_path.exists():
        return

    content = sitemap_path.read_text(encoding="utf-8")
    url_entry = f"    <url>\n        <loc>{site_url}/sitemap-page.html</loc>\n    </url>\n</urlset>"
    content = content.replace("</urlset>", url_entry)
    sitemap_path.write_text(content, encoding="utf-8")
    print("Appended sitemap-page.html URL to sitemap.xml")


def _inject_sitemap_link(site_dir: Path) -> None:
    """Inject sitemap links into HTML head elements.

    Adds <link rel="sitemap" ...> for sitemap.xml and sitemap-page.html
    to all HTML pages to help search engines discover the sitemap through
    page markup in addition to robots.txt.
    """
    sitemap_links = (
        '  <link rel="sitemap" type="application/xml" href="/sitemap.xml">\n'
        '  <link rel="sitemap" href="/sitemap-page.html">\n</head>'
    )
    injected_count = 0

    for html_file in site_dir.rglob("*.html"):
        content = html_file.read_text()

        # Skip if already has sitemap link
        if 'rel="sitemap"' in content:
            continue

        # Inject before </head>
        if "</head>" in content:
            content = content.replace("</head>", sitemap_links)
            html_file.write_text(content)
            injected_count += 1

    if injected_count > 0:
        print(f"Injected sitemap links into {injected_count} HTML files")
    else:
        print("All HTML files already have sitemap links")

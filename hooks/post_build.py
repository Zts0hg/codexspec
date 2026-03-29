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


def _inject_sitemap_link(site_dir: Path) -> None:
    """Inject sitemap link into HTML head elements.

    Adds <link rel="sitemap" ...> to all HTML pages to help search
    engines discover the sitemap through page markup in addition
    to robots.txt.
    """
    sitemap_link = '  <link rel="sitemap" type="application/xml" href="/sitemap.xml">\n</head>'
    injected_count = 0

    for html_file in site_dir.rglob("*.html"):
        content = html_file.read_text()

        # Skip if already has sitemap link
        if 'rel="sitemap"' in content:
            continue

        # Inject before </head>
        if "</head>" in content:
            content = content.replace("</head>", sitemap_link)
            html_file.write_text(content)
            injected_count += 1

    if injected_count > 0:
        print(f"Injected sitemap links into {injected_count} HTML files")
    else:
        print("All HTML files already have sitemap links")

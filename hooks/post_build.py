"""Post-build hook to create root redirect if needed and fix 404.html language."""

from pathlib import Path


def on_post_build(config, **kwargs):
    """Create redirect index.html at site root only if no default language exists.

    When a language is set as 'default: true' in mkdocs-static-i18n, it is built
    to the site root, so no redirect is needed. This hook only creates a redirect
    when no default language is configured.

    Also fixes 404.html to use English (default language) instead of the last
    language in the configuration list, which mkdocs-static-i18n uses as fallback.
    """
    site_dir = Path(config.site_dir)

    # Fix 404.html to use English (default language) instead of last language
    _fix_404_language(site_dir)

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

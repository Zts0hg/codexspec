"""Post-build hook to create root redirect if needed."""

from pathlib import Path


def on_post_build(config, **kwargs):
    """Create redirect index.html at site root only if no default language exists.

    When a language is set as 'default: true' in mkdocs-static-i18n, it is built
    to the site root, so no redirect is needed. This hook only creates a redirect
    when no default language is configured.
    """
    site_dir = Path(config.site_dir)
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
    <meta name="viewport" content="width=device-width,initial-scale=1">
    <title>CodexSpec</title>
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

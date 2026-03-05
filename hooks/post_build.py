"""Post-build hook to create root redirect."""

from pathlib import Path

REDIRECT_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width,initial-scale=1">
    <title>CodexSpec</title>
    <meta http-equiv="refresh" content="0; url=/codexspec/en/">
    <link rel="canonical" href="/codexspec/en/">
</head>
<body>
    <p>Redirecting to <a href="/codexspec/en/">English documentation</a>...</p>
</body>
</html>
"""


def on_post_build(config, **kwargs):
    """Create redirect index.html at site root."""
    site_dir = Path(config.site_dir)
    root_index = site_dir / "index.html"
    root_index.write_text(REDIRECT_HTML)
    print(f"Created redirect at {root_index}")

"""Pytest fixtures for hooks tests."""

import sys
from pathlib import Path
from unittest.mock import MagicMock

import pytest

# Add project root to path so we can import hooks module
project_root = Path(__file__).parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))


@pytest.fixture
def site_dir(tmp_path: Path) -> Path:
    """Create a temporary site directory mimicking MkDocs output."""
    site = tmp_path / "site"
    site.mkdir()
    return site


@pytest.fixture
def mock_config() -> MagicMock:
    """Create a mock MkDocs config with i18n plugin."""
    config = MagicMock()
    config.site_url = "https://example.com/codexspec/"
    config.site_dir = "/tmp/site"

    # Mock i18n plugin
    i18n_plugin = MagicMock()
    i18n_plugin.config = {
        "languages": [
            {"locale": "en", "name": "English", "default": True},
            {"locale": "zh", "name": "\u4e2d\u6587\u7b80\u4f53"},
            {"locale": "ja", "name": "\u65e5\u672c\u8a9e"},
        ]
    }

    # Mock plugins collection - use MagicMock to support .get()
    config.plugins = MagicMock()
    config.plugins.get = lambda key: i18n_plugin if key == "i18n" else None

    return config


@pytest.fixture
def sample_nav() -> list:
    """Create a sample nav configuration."""
    return [
        {"Home": "index.md"},
        {"Installation": "getting-started/installation.md"},
        {"Quick Start": "getting-started/quick-start.md"},
        {"External Link": "https://example.com"},
    ]


@pytest.fixture
def site_with_pages(site_dir: Path) -> Path:
    """Create a site directory with some built HTML pages."""
    # Default language pages
    (site_dir / "index.html").write_text("<html></html>")
    getting_started = site_dir / "getting-started"
    getting_started.mkdir()
    (getting_started / "installation" / "index.html").parent.mkdir(parents=True, exist_ok=True)
    (getting_started / "installation" / "index.html").write_text("<html></html>")
    (getting_started / "quick-start" / "index.html").parent.mkdir(parents=True, exist_ok=True)
    (getting_started / "quick-start" / "index.html").write_text("<html></html>")

    # Non-default language pages
    for lang in ["zh", "ja"]:
        lang_dir = site_dir / lang
        lang_dir.mkdir(exist_ok=True)
        (lang_dir / "index.html").write_text("<html></html>")
        gs = lang_dir / "getting-started"
        gs.mkdir(exist_ok=True)
        (gs / "installation" / "index.html").parent.mkdir(parents=True, exist_ok=True)
        (gs / "installation" / "index.html").write_text("<html></html>")

    return site_dir

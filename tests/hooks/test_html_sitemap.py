"""Tests for HTML sitemap generation in hooks/post_build.py."""

from pathlib import Path
from unittest.mock import MagicMock

# ============================================================================
# Task 2.1: _get_i18n_languages tests
# ============================================================================


class TestGetI18nLanguages:
    """Tests for _get_i18n_languages(config)."""

    def test_returns_language_list_when_plugin_exists(self, mock_config: MagicMock) -> None:
        from hooks.post_build import _get_i18n_languages

        languages = _get_i18n_languages(mock_config)
        assert len(languages) == 3
        assert languages[0]["locale"] == "en"
        assert languages[0]["name"] == "English"
        assert languages[0]["default"] is True
        assert languages[1]["locale"] == "zh"
        assert languages[2]["locale"] == "ja"

    def test_returns_empty_list_when_no_plugin(self) -> None:
        from hooks.post_build import _get_i18n_languages

        config = MagicMock()
        plugins_mock = MagicMock()
        plugins_mock.get.return_value = None
        config.plugins = plugins_mock
        assert _get_i18n_languages(config) == []

    def test_returns_empty_list_when_no_languages_key(self) -> None:
        from hooks.post_build import _get_i18n_languages

        config = MagicMock()
        i18n_plugin = MagicMock()
        i18n_plugin.config = {}
        plugins_mock = MagicMock()
        plugins_mock.get.return_value = i18n_plugin
        config.plugins = plugins_mock
        assert _get_i18n_languages(config) == []

    def test_language_item_has_required_fields(self, mock_config: MagicMock) -> None:
        from hooks.post_build import _get_i18n_languages

        languages = _get_i18n_languages(mock_config)
        for lang in languages:
            assert "locale" in lang
            assert "name" in lang


# ============================================================================
# Task 2.3: _extract_nav_pages tests
# ============================================================================


class TestExtractNavPages:
    """Tests for _extract_nav_pages(nav)."""

    def test_flat_nav(self) -> None:
        from hooks.post_build import _extract_nav_pages

        nav = [{"Home": "index.md"}, {"About": "about.md"}]
        result = _extract_nav_pages(nav)
        assert len(result) == 2
        assert result[0] == ("Home", "index.md")
        assert result[1] == ("About", "about.md")

    def test_nested_nav(self) -> None:
        from hooks.post_build import _extract_nav_pages

        nav = [
            {
                "Getting Started": [
                    {"Installation": "getting-started/installation.md"},
                    {"Quick Start": "getting-started/quick-start.md"},
                ]
            }
        ]
        result = _extract_nav_pages(nav)
        assert len(result) == 2
        assert result[0] == ("Installation", "getting-started/installation.md")
        assert result[1] == ("Quick Start", "getting-started/quick-start.md")

    def test_filters_external_urls(self) -> None:
        from hooks.post_build import _extract_nav_pages

        nav = [
            {"Home": "index.md"},
            {"External": "https://example.com"},
            {"Another": "http://other.com/page"},
        ]
        result = _extract_nav_pages(nav)
        assert len(result) == 1
        assert result[0] == ("Home", "index.md")

    def test_empty_nav(self) -> None:
        from hooks.post_build import _extract_nav_pages

        assert _extract_nav_pages([]) == []

    def test_deeply_nested_nav(self) -> None:
        from hooks.post_build import _extract_nav_pages

        nav = [
            {
                "Level1": [
                    {
                        "Level2": [
                            {"Deep Page": "deep/page.md"},
                        ]
                    }
                ]
            }
        ]
        result = _extract_nav_pages(nav)
        assert len(result) == 1
        assert result[0] == ("Deep Page", "deep/page.md")


# ============================================================================
# Task 2.5: _build_language_section and _build_full_html tests
# ============================================================================


class TestBuildLanguageSection:
    """Tests for _build_language_section()."""

    def test_default_language_home_url(self) -> None:
        from hooks.post_build import _build_language_section

        lang = {"locale": "en", "name": "English", "default": True}
        site_dir = Path("/tmp/site")
        nav_pages = [("Installation", "getting-started/installation.md")]
        html = _build_language_section(lang, nav_pages, "https://example.com/codexspec", site_dir)
        assert 'href="https://example.com/codexspec/"' in html
        assert ">Home<" in html

    def test_non_default_language_home_url(self) -> None:
        from hooks.post_build import _build_language_section

        lang = {"locale": "zh", "name": "中文简体"}
        site_dir = Path("/tmp/site")
        nav_pages = []
        html = _build_language_section(lang, nav_pages, "https://example.com/codexspec", site_dir)
        assert 'href="https://example.com/codexspec/zh/"' in html

    def test_section_contains_language_name(self) -> None:
        from hooks.post_build import _build_language_section

        lang = {"locale": "ja", "name": "日本語"}
        site_dir = Path("/tmp/site")
        nav_pages = []
        html = _build_language_section(lang, nav_pages, "https://example.com/codexspec", site_dir)
        assert "<h2>日本語</h2>" in html
        assert 'lang="ja"' in html

    def test_only_includes_existing_pages(self, site_with_pages: Path) -> None:
        from hooks.post_build import _build_language_section

        lang = {"locale": "en", "name": "English", "default": True}
        nav_pages = [
            ("Installation", "getting-started/installation.md"),
            ("Missing", "missing/page.md"),
        ]
        html = _build_language_section(lang, nav_pages, "https://example.com/codexspec", site_with_pages)
        assert "Installation" in html
        assert "Missing" not in html


class TestBuildFullHtml:
    """Tests for _build_full_html()."""

    def test_complete_html_structure(self) -> None:
        from hooks.post_build import _build_full_html

        sections = ['<section class="language-section" lang="en"><h2>English</h2><ul></ul></section>']
        html = _build_full_html(sections, "https://example.com/codexspec")
        assert "<!DOCTYPE html>" in html
        assert "<html" in html
        assert "</html>" in html
        assert '<meta charset="UTF-8">' in html
        assert '<meta name="viewport"' in html

    def test_contains_inline_css(self) -> None:
        from hooks.post_build import _build_full_html

        sections = ['<section class="language-section" lang="en"><h2>English</h2></section>']
        html = _build_full_html(sections, "https://example.com/codexspec")
        assert "<style>" in html
        assert "--md-primary-fg-color" in html
        assert "@media" in html

    def test_contains_home_link(self) -> None:
        from hooks.post_build import _build_full_html

        sections = []
        html = _build_full_html(sections, "https://example.com/codexspec")
        assert "https://example.com/codexspec/" in html


# ============================================================================
# Task 2.7: _generate_html_sitemap tests
# ============================================================================


class TestGenerateHtmlSitemap:
    """Tests for _generate_html_sitemap(site_dir, config)."""

    def test_creates_sitemap_file(self, site_with_pages: Path, mock_config: MagicMock, sample_nav: list) -> None:
        from hooks.post_build import _generate_html_sitemap

        mock_config.nav = sample_nav
        _generate_html_sitemap(site_with_pages, mock_config)
        sitemap_path = site_with_pages / "sitemap-page.html"
        assert sitemap_path.exists()

    def test_output_is_valid_html(self, site_with_pages: Path, mock_config: MagicMock, sample_nav: list) -> None:
        from hooks.post_build import _generate_html_sitemap

        mock_config.nav = sample_nav
        _generate_html_sitemap(site_with_pages, mock_config)
        content = (site_with_pages / "sitemap-page.html").read_text()
        assert content.startswith("<!DOCTYPE html>")
        assert "</html>" in content

    def test_contains_all_language_sections(
        self, site_with_pages: Path, mock_config: MagicMock, sample_nav: list
    ) -> None:
        from hooks.post_build import _generate_html_sitemap

        mock_config.nav = sample_nav
        _generate_html_sitemap(site_with_pages, mock_config)
        content = (site_with_pages / "sitemap-page.html").read_text()
        assert 'lang="en"' in content
        assert 'lang="zh"' in content
        assert 'lang="ja"' in content

    def test_file_size_under_50kb(self, site_with_pages: Path, mock_config: MagicMock, sample_nav: list) -> None:
        from hooks.post_build import _generate_html_sitemap

        mock_config.nav = sample_nav
        _generate_html_sitemap(site_with_pages, mock_config)
        file_size = (site_with_pages / "sitemap-page.html").stat().st_size
        assert file_size < 50 * 1024

    def test_handles_empty_nav(self, site_dir: Path, mock_config: MagicMock) -> None:
        from hooks.post_build import _generate_html_sitemap

        mock_config.nav = []
        _generate_html_sitemap(site_dir, mock_config)
        sitemap_path = site_dir / "sitemap-page.html"
        assert sitemap_path.exists()
        content = sitemap_path.read_text()
        assert "<!DOCTYPE html>" in content


# ============================================================================
# Task 3.1: _append_sitemap_page_url tests
# ============================================================================


# ============================================================================
# Task 5.1: End-to-end verification tests
# ============================================================================


class TestEndToEnd:
    """End-to-end tests verifying the complete on_post_build flow."""

    def test_full_flow_generates_sitemap_page(
        self, site_with_pages: Path, mock_config: MagicMock, sample_nav: list
    ) -> None:
        from hooks.post_build import _generate_html_sitemap

        mock_config.nav = sample_nav

        # Simulate the build pipeline
        _generate_html_sitemap(site_with_pages, mock_config)

        # Verify sitemap-page.html was generated
        sitemap_page = site_with_pages / "sitemap-page.html"
        assert sitemap_page.exists()
        content = sitemap_page.read_text()
        assert "<!DOCTYPE html>" in content

    def test_html_pages_contain_sitemap_page_link(
        self, site_with_pages: Path, mock_config: MagicMock, sample_nav: list
    ) -> None:
        from hooks.post_build import (
            _generate_html_sitemap,
            _inject_sitemap_link,
        )

        mock_config.nav = sample_nav

        # Add <head> tags to existing HTML files for injection test
        for html_file in site_with_pages.rglob("*.html"):
            original = html_file.read_text()
            html_file.write_text(f"<html><head></head><body>{original}</body></html>")

        site_url = mock_config.site_url.rstrip("/")
        _generate_html_sitemap(site_with_pages, mock_config)
        _inject_sitemap_link(site_with_pages, site_url)

        # Verify HTML files have sitemap links injected
        index_html = (site_with_pages / "index.html").read_text()
        assert 'href="/codexspec/sitemap.xml"' in index_html
        assert 'href="/codexspec/sitemap-page.html"' in index_html

    def test_sitemap_page_not_overwritten_by_injection(
        self, site_with_pages: Path, mock_config: MagicMock, sample_nav: list
    ) -> None:
        from hooks.post_build import (
            _generate_html_sitemap,
            _inject_sitemap_link,
        )

        mock_config.nav = sample_nav

        site_url = mock_config.site_url.rstrip("/")
        _generate_html_sitemap(site_with_pages, mock_config)
        _inject_sitemap_link(site_with_pages, site_url)

        # The sitemap-page.html itself has no <head> tag with existing content,
        # so it shouldn't be modified by injection (it uses its own inline CSS)
        sitemap_page = (site_with_pages / "sitemap-page.html").read_text()
        assert "Sitemap - CodexSpec" in sitemap_page

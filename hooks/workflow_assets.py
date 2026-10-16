"""Publish the README workflow assets without maintaining copies under docs/."""

from pathlib import Path

from mkdocs.exceptions import PluginError
from mkdocs.plugins import event_priority
from mkdocs.structure.files import File, InclusionLevel

LOCALES = ("en", "zh-CN", "ja", "ko", "de", "fr", "es", "pt-BR")


@event_priority(-110)
def on_files(files, config, **kwargs):
    """Register after i18n (-100), which otherwise resets each File's source root.

    Source URIs match physical relative Markdown links out of docs/. Destination
    URIs publish one shared set, so locale builds reuse the same image bytes.
    """
    for locale in LOCALES:
        for theme in ("light", "dark"):
            name = f"workflow-{locale}-{theme}.png"
            source = f"../assets/workflow/{name}"
            if not (Path(config.docs_dir) / source).is_file():
                raise PluginError(f"Missing README workflow image: {name}")
            if files.get_file_from_path(source) is None:
                files.append(
                    File(
                        source,
                        config.docs_dir,
                        config.site_dir,
                        config.use_directory_urls,
                        dest_uri=f"assets/workflow/{name}",
                        inclusion=InclusionLevel.INCLUDED,
                    )
                )
    return files

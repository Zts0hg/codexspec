"""Private release protocol: render only a supplied disposable snapshot."""

import base64
import json
import sys
from pathlib import Path

from codexspec import __version__

from .render import render_installation


def main() -> None:
    if len(sys.argv) != 5:
        raise SystemExit("Expected snapshot, result, integration and language")
    snapshot, result = Path(sys.argv[1]), Path(sys.argv[2])
    if snapshot.is_symlink() or not snapshot.is_dir() or result.exists() or result.is_symlink():
        raise SystemExit("Invalid worker paths")
    files = render_installation(snapshot, sys.argv[3], sys.argv[4])
    data = {
        "protocol": 1,
        "version": __version__,
        "files": {name: base64.b64encode(content).decode("ascii") for name, content in files.items()},
    }
    result.write_text(json.dumps(data), encoding="utf-8", newline="\n")


if __name__ == "__main__":
    main()

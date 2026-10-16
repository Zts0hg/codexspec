"""Measure text bounds in actual draw.io SVG exports (optional Playwright tool).

Export SVG inspection copies with draw.io --svg-theme light --embed-svg-fonts false.
This detects label overflow, not all line routing or visual readability problems.
PNG exports remain the README assets and must also be inspected visually.
"""

import argparse
import json
from pathlib import Path

MEASURE = """() => [...document.querySelectorAll('[data-cell-id]')].flatMap(g => {
  const text = g.querySelector(':scope > g [lang]');
  const shape = g.querySelector(':scope > g > :is(rect,path,ellipse)');
  if (!text || !shape) return [];
  const box = shape.getBoundingClientRect(), range = document.createRange();
  range.selectNodeContents(text);
  const rects = [...range.getClientRects()].filter(r => r.width > 0);
  if (!rects.length) return [];
  const left = Math.min(...rects.map(r=>r.left));
  const right = Math.max(...rects.map(r=>r.right));
  const top = Math.min(...rects.map(r=>r.top));
  const bottom = Math.max(...rects.map(r=>r.bottom));
  const overflow = left < box.left-3 || right > box.right+3 ||
                   top < box.top-3 || bottom > box.bottom+3;
  return [{id:g.dataset.cellId, overflow, textWidth:right-left, textHeight:bottom-top,
           boxWidth:box.width, boxHeight:box.height}];
})"""


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("svg", nargs="+", type=Path)
    parser.add_argument("--browser", default="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome")
    args = parser.parse_args()
    from playwright.sync_api import sync_playwright

    report = {}
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(executable_path=args.browser, headless=True)
        try:
            page = browser.new_page(color_scheme="light")
            for path in args.svg:
                page.goto(path.resolve().as_uri(), wait_until="domcontentloaded")
                page.evaluate("document.fonts.ready")
                labels = page.evaluate(MEASURE)
                if not labels:
                    parser.error(f"no measurable diagram labels: {path}")
                report[str(path)] = {"measured": len(labels), "overflow": [r for r in labels if r["overflow"]]}
        finally:
            browser.close()
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return int(any(r["overflow"] for r in report.values()))


if __name__ == "__main__":
    raise SystemExit(main())

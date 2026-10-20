#!/usr/bin/env python3
"""Render a TRMNL plugin's Liquid markup locally to an 800x480 PNG.

This is a *stress test*, not a pixel-perfect emulator: TRMNL's real
framework CSS and fonts aren't published as a package, so the frame below
uses deliberately oversized text, a fallback serif font, and the
conflicting `.row` / `.col` rules that bit us during development. If a
layout fits here, it has comfortable headroom on the device.

Usage:
  python3 tools/preview.py plugins/surf-call/markup.liquid plugins/surf-call/examples/*.json
  python3 tools/preview.py plugins/conditions/markup.liquid plugins/conditions/sample-data.json

Each JSON file may be either a webhook body ({"merge_variables": {...}})
or a plain variables object (e.g. polling data with IDX_0, IDX_1, ...).
PNGs are written next to the JSON (or to --out DIR). Exit code 1 if any
render overflows the 800x480 content area.

Requires: pip install python-liquid playwright && playwright install chromium
"""
import argparse
import json
import pathlib
import sys

from liquid import Environment

FRAME = """<!doctype html><html><head><meta charset="utf-8"><style>
body{margin:0;background:#fff;font-family:serif;}
.screen{width:800px;height:480px;overflow:hidden;position:relative}
.view{position:absolute;inset:0;padding:16px 20px 58px 20px;display:flex;flex-direction:column}
.layout{flex:1;display:flex;flex-direction:column;justify-content:center;align-items:center;overflow:hidden}
.title_bar{position:absolute;left:10px;right:10px;bottom:8px;height:40px;display:flex;align-items:center;justify-content:space-between;padding:0 12px;background:#ddd;font-size:15px}
.label{font-size:17px;line-height:22px}
.description{font-size:15px;line-height:20px}
.value{font-size:38px;line-height:44px}
.value--small{font-size:28px;line-height:34px}
.value--xsmall{font-size:22px;line-height:28px}
/* hostile rules: TRMNL's framework defines its own .row/.col etc. */
.row{display:grid;height:60px}.col{position:absolute}
</style></head><body><div class="screen"><div class="view">BODY</div></div></body></html>"""


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("markup")
    ap.add_argument("data", nargs="+")
    ap.add_argument("--out", help="output directory (default: next to each JSON)")
    args = ap.parse_args()

    from playwright.sync_api import sync_playwright

    tpl = Environment().from_string(pathlib.Path(args.markup).read_text())
    failed = False
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": 800, "height": 480})
        for path in map(pathlib.Path, args.data):
            data = json.loads(path.read_text())
            data = data.get("merge_variables", data)
            html = FRAME.replace("BODY", tpl.render(**data))
            out_dir = pathlib.Path(args.out) if args.out else path.parent
            out_dir.mkdir(parents=True, exist_ok=True)
            tmp = out_dir / f".{path.stem}.preview.html"
            tmp.write_text(html)
            page.goto(tmp.resolve().as_uri())
            png = out_dir / f"{path.stem}.png"
            page.screenshot(path=str(png))
            avail, used = page.evaluate(
                "() => { const l = document.querySelector('.layout');"
                " const c = l && l.firstElementChild;"
                " return [l ? l.clientHeight : 0, c ? c.scrollHeight : 0]; }"
            )
            tmp.unlink()
            ok = used <= avail
            failed |= not ok
            print(f"{'OK  ' if ok else 'OVER'} {png}  content {used}px / {avail}px available")
        browser.close()
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""Generate the Claude Artifact variant of the game from index.html.

The artifact host supplies its own <!doctype>/<html>/<head>/<body> wrapper,
so the published page must contain page content only. This regenerates that
variant instead of keeping a hand-maintained duplicate that can drift.

    python3 tools/build-artifact.py [out.html]
"""
import re
import sys
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
src = (ROOT / "index.html").read_text()

style = re.search(r"<style>(.*?)</style>", src, re.S).group(1)
body = re.search(r"<body>(.*?)</body>", src, re.S).group(1)

out = (
    "<title>Dead Zone</title>\n"
    "<style>\n"
    "/* the artifact wrapper supplies its own head/viewport meta, so lock\n"
    "   pinch-zoom and rubber-band scrolling from CSS instead */\n"
    "html, body { touch-action: none; overscroll-behavior: none;"
    " -webkit-text-size-adjust: 100%; }\n"
    + style
    + "</style>\n"
    + body
)

dest = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "dead-zone.artifact.html"
dest.write_text(out)
print(f"wrote {dest} ({len(out)} bytes)")

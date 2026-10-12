"""Bundle styletile/template.html into a single self-contained styletile/index.html.

Placeholders:
  {{sprite}}              contents of public/brand/icons.svg
  {{svg:NAME}}            inline public/brand/NAME.svg
  {{svg:NAME:CLASS}}      same, with class="CLASS" on the <svg>
  {{uri:PATH}}            file at PATH (from repo root) as a data: URI

Run: python scripts/build_styletile.py
"""
import base64
import mimetypes
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "styletile" / "template.html"
OUT = ROOT / "styletile" / "index.html"          # full document, open locally
OUT_BARE = ROOT / "styletile" / "artifact.html"  # body only, for publishing as a claude.ai Artifact
BRAND = ROOT / "public" / "brand"
MIME = {".svg": "image/svg+xml", ".webp": "image/webp", ".png": "image/png", ".jpg": "image/jpeg"}


def inline_svg(m: re.Match) -> str:
    name, cls = m.group(1), m.group(2)
    svg = (BRAND / f"{name}.svg").read_text(encoding="utf-8").strip()
    svg = re.sub(r"<title>.*?</title>", "", svg, count=1)
    svg = re.sub(r' color="[^"]*"', "", svg, count=1)  # inherit color from the page's CSS
    if cls:
        svg = svg.replace("<svg ", f'<svg class="{cls}" ', 1)
    return svg


def data_uri(m: re.Match) -> str:
    path = ROOT / m.group(1)
    mime = MIME.get(path.suffix) or mimetypes.guess_type(path.name)[0]
    return f"data:{mime};base64,{base64.b64encode(path.read_bytes()).decode()}"


def main() -> None:
    html = SRC.read_text(encoding="utf-8")
    sprite = (BRAND / "icons.svg").read_text(encoding="utf-8")
    sprite = re.sub(r"<!--.*?-->", "", sprite, flags=re.S).strip()
    html = html.replace("{{sprite}}", sprite)
    html = re.sub(r"\{\{svg:([\w-]+)(?::([\w -]+))?\}\}", inline_svg, html)
    html = re.sub(r"\{\{uri:([^}]+)\}\}", data_uri, html)
    left = re.findall(r"\{\{[^}]+\}\}", html)
    if left:
        raise SystemExit(f"Unresolved placeholders: {left}")
    OUT_BARE.write_text(html, encoding="utf-8")
    OUT.write_text(
        '<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
        f"</head>\n<body>\n{html}\n</body>\n</html>\n",
        encoding="utf-8",
    )
    for f in (OUT, OUT_BARE):
        print(f"{f.relative_to(ROOT)}  {f.stat().st_size // 1024} KB")


if __name__ == "__main__":
    main()

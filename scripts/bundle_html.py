"""Bundle an HTML template into one self-contained page (same placeholders as build_styletile.py).

Writes <out>.html (full document, open locally) and <out>.artifact.html (body only, for publishing).
Run: python scripts/bundle_html.py prototype/template.html prototype/index.html
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build_styletile as b  # noqa: E402


def bundle(src: Path, out: Path) -> None:
    html = src.read_text(encoding="utf-8")
    sprite = re.sub(r"<!--.*?-->", "", (b.BRAND / "icons.svg").read_text(encoding="utf-8"), flags=re.S).strip()
    html = html.replace("{{sprite}}", sprite)
    html = re.sub(r"\{\{svg:([\w-]+)(?::([\w -]+))?\}\}", b.inline_svg, html)
    html = re.sub(r"\{\{uri:([^}]+)\}\}", b.data_uri, html)
    left = re.findall(r"\{\{[^}]+\}\}", html)
    if left:
        raise SystemExit(f"Unresolved placeholders: {left}")
    bare = out.with_suffix(".artifact.html")
    bare.write_text(html, encoding="utf-8")
    out.write_text(
        '<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
        f"</head>\n<body>\n{html}\n</body>\n</html>\n",
        encoding="utf-8",
    )
    for f in (out, bare):
        print(f"{f.relative_to(b.ROOT)}  {f.stat().st_size // 1024} KB")


if __name__ == "__main__":
    bundle(b.ROOT / sys.argv[1], b.ROOT / sys.argv[2])

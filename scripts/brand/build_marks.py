"""Build the Urban Duck lockups, stamp and favicons from the traced duck + brand fonts.

All lettering is converted to outlines (no font needed to display the SVGs).

Outputs (public/brand/):
  lockup-stacked.svg      duck over arched URBAN DUCK + WORKING CLASS LUXURY  (header, primary)
  lockup-horizontal.svg   duck beside URBAN DUCK + tagline                     (compact / sticky header)
  stamp.svg               "Built for the Elements" UD seal, rust, distressed
  favicon.svg, favicon.ico, favicon-32.png, apple-touch-icon.png, icon-192.png, icon-512.png
  og-default.png          1200x630 social share image

Run after trace_logos.py + trace.mjs:  python scripts/brand/build_marks.py   (needs: fonttools, pillow)
"""
import math
import re
from pathlib import Path

from fontTools.pens.boundsPen import ControlBoundsPen
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.misc.transform import Transform
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[2]
FONTS = ROOT / "brand" / "fonts"
OUT = ROOT / "public" / "brand"
BUILD = Path(__file__).resolve().parent / ".build"

NAVY, NIGHT, SAIL, CANVAS, RUST = "#0B3354", "#0D1B24", "#F3EEE4", "#E6DCCB", "#9B3A2A"


# ---------------------------------------------------------------- text → outlines
class Face:
    def __init__(self, file: str, wght: int):
        font = instantiateVariableFont(TTFont(FONTS / file), {"wght": wght})
        self.gs = font.getGlyphSet()
        self.cmap = font.getBestCmap()
        self.upm = font["head"].unitsPerEm
        self.cap = font["OS/2"].sCapHeight or int(self.upm * 0.7)
        self.hmtx = font["hmtx"]

    def layout(self, text: str, size: float, tracking: float = 0.0):
        """[(glyph_name, x_px, advance_px)], total width. tracking in em."""
        s = size / self.upm
        x, out = 0.0, []
        for i, ch in enumerate(text):
            g = self.cmap[ord(ch)]
            adv = self.hmtx[g][0] * s
            out.append((g, x, adv))
            x += adv + (tracking * size if i < len(text) - 1 else 0)
        return out, x


class Canvas:
    """Collects path data in one coordinate space and tracks bounds."""

    def __init__(self):
        self.d, self.box = [], [math.inf, math.inf, -math.inf, -math.inf]

    def glyph(self, face: Face, name: str, t: Transform):
        pen = SVGPathPen(face.gs, ntos=lambda v: f"{v:.1f}".rstrip("0").rstrip("."))
        face.gs[name].draw(TransformPen(pen, t))
        bp = ControlBoundsPen(face.gs)
        face.gs[name].draw(TransformPen(bp, t))
        if bp.bounds:
            self._grow(bp.bounds)
        if pen.getCommands():
            self.d.append(pen.getCommands())

    def text(self, face, text, size, x, baseline, tracking=0.0, anchor="middle"):
        glyphs, width = face.layout(text, size, tracking)
        x0 = x - width / 2 if anchor == "middle" else x
        s = size / face.upm
        for g, gx, _ in glyphs:
            self.glyph(face, g, Transform().translate(x0 + gx, baseline).scale(s, -s))
        return width

    def arc_text(self, face, text, size, cx, cy, r, tracking=0.0, bottom=False):
        """Text on a circle of baseline radius r, centred at the top (or bottom, reading left→right)."""
        glyphs, width = face.layout(text, size, tracking)
        s = size / face.upm
        for g, gx, adv in glyphs:
            a = (gx + adv / 2 - width / 2) / r
            if bottom:
                t = Transform().translate(cx + r * math.sin(a), cy + r * math.cos(a)).rotate(-a)
            else:
                t = Transform().translate(cx + r * math.sin(a), cy - r * math.cos(a)).rotate(a)
            self.glyph(face, g, t.translate(-adv / 2, 0).scale(s, -s))

    def rect(self, x, y, w, h):
        self.d.append(f"M{x:.1f} {y:.1f}h{w:.1f}v{h:.1f}h{-w:.1f}Z")
        self._grow((x, y, x + w, y + h))

    def _grow(self, b):
        self.box = [min(self.box[0], b[0]), min(self.box[1], b[1]), max(self.box[2], b[2]), max(self.box[3], b[3])]


def duck_path():
    svg = (OUT / "duck-icon.svg").read_text(encoding="utf-8")
    w, h = map(int, re.search(r'viewBox="0 0 (\d+) (\d+)"', svg).groups())
    return re.search(r' d="([^"]+)"', svg).group(1), w, h


def write_svg(name, canvas: Canvas, extra="", pad=8, title="Urban Duck — Working Class Luxury", color=NAVY, defs=""):
    x0, y0, x1, y1 = canvas.box
    x0, y0, x1, y1 = x0 - pad, y0 - pad, x1 + pad, y1 + pad
    vb = f"{x0:.0f} {y0:.0f} {x1 - x0:.0f} {y1 - y0:.0f}"
    (OUT / name).write_text(
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb}" role="img" aria-label="{title}" color="{color}" fill="currentColor">'
        f"<title>{title}</title>{defs}{extra}<path d=\"{''.join(canvas.d)}\"/></svg>\n",
        encoding="utf-8",
    )
    print(f"{name:24} {x1 - x0:.0f}x{y1 - y0:.0f}  {(OUT / name).stat().st_size // 1024} KB")


def duck_use(d, dw, dh, cx, top, height, flip=False):
    s = height / dh
    w = dw * s
    if flip:
        t = f"translate({cx + w / 2:.1f} {top:.1f}) scale({-s:.4f} {s:.4f})"
    else:
        t = f"translate({cx - w / 2:.1f} {top:.1f}) scale({s:.4f})"
    return f'<path transform="{t}" d="{d}"/>', w


# ---------------------------------------------------------------- marks
def main():
    display = Face("Rokkitt-VF.ttf", 800)
    ui = Face("WorkSans-VF.ttf", 600)
    d, dw, dh = duck_path()

    # Stacked lockup: duck → arched URBAN DUCK → rule · WORKING CLASS LUXURY · rule
    c = Canvas()
    size, cx, r = 120, 0, 1500
    duck_h = 150
    duck, duck_w = duck_use(d, dw, dh, cx, 0, duck_h, flip=True)  # flipped: duck faces into the name like the catalog
    c._grow((cx - duck_w / 2, 0, cx + duck_w / 2, duck_h))
    name_base = duck_h + 30 + size * display.cap / display.upm
    c.arc_text(display, "URBAN DUCK", size, cx, name_base + r, r, tracking=0.03)
    tag_size = 38
    tag_base = name_base + 84
    tw = c.text(ui, "WORKING CLASS LUXURY", tag_size, cx, tag_base, tracking=0.2)
    rule_y = tag_base - tag_size * ui.cap / ui.upm / 2 - 1.5
    c.rect(cx - tw / 2 - 62, rule_y, 40, 4)
    c.rect(cx + tw / 2 + 22, rule_y, 40, 4)
    write_svg("lockup-stacked.svg", c, extra=duck)

    # Horizontal lockup: duck | URBAN DUCK / WORKING CLASS LUXURY
    c = Canvas()
    size = 120
    cap = size * display.cap / display.upm
    duck_h = 150
    duck, duck_w = duck_use(d, dw, dh, duck_h * dw / dh / 2, 0, duck_h, flip=True)
    c._grow((0, 0, duck_w, duck_h))
    x = duck_w + 34
    name_w = c.text(display, "URBAN DUCK", size, x, 12 + cap, tracking=0.03, anchor="start")
    tag_glyphs, tag_w = ui.layout("WORKING CLASS LUXURY", 33, 0.2)
    track = 0.2 + (name_w - tag_w) / (33 * (len("WORKING CLASS LUXURY") - 1))  # justify tagline to the name width
    c.text(ui, "WORKING CLASS LUXURY", 33, x, 12 + cap + 62, tracking=track, anchor="start")
    write_svg("lockup-horizontal.svg", c, extra=duck)

    # Compact lockup: duck | URBAN DUCK, no tagline (slim scrolled header, small spaces)
    c = Canvas()
    duck_h = 120
    duck, duck_w = duck_use(d, dw, dh, duck_h * dw / dh / 2, 0, duck_h, flip=True)
    c._grow((0, 0, duck_w, duck_h))
    c.text(display, "URBAN DUCK", size, duck_w + 28, duck_h - 8, tracking=0.03, anchor="start")
    write_svg("lockup-compact.svg", c, extra=duck, title="Urban Duck")

    # Stamp: double ring, BUILT FOR (top) / THE ELEMENTS (bottom), UD centre, stars
    c = Canvas()
    R = 200
    ring = (
        f'<circle cx="0" cy="0" r="{R}" fill="none" stroke="currentColor" stroke-width="9"/>'
        f'<circle cx="0" cy="0" r="{R - 16}" fill="none" stroke="currentColor" stroke-width="3"/>'
        f'<circle cx="0" cy="0" r="{R - 92}" fill="none" stroke="currentColor" stroke-width="3"/>'
    )
    c._grow((-R - 5, -R - 5, R + 5, R + 5))
    band_mid = R - 54
    ts = 46
    tcap = ts * display.cap / display.upm
    c.arc_text(display, "BUILT FOR", ts, 0, 0, band_mid - tcap / 2, tracking=0.12)
    c.arc_text(display, "THE ELEMENTS", ts, 0, 0, band_mid + tcap / 2, tracking=0.08, bottom=True)
    ud = 124
    c.text(display, "UD", ud, 0, ud * display.cap / display.upm / 2, tracking=0.0)
    stars = "".join(star(x, 0, 13) for x in (-band_mid, band_mid))
    stars += star(0, -62, 9) + star(0, 72, 9)
    defs = (
        '<defs><filter id="ud-wear" x="0" y="0" width="100%" height="100%">'
        '<feTurbulence type="fractalNoise" baseFrequency="0.6" numOctaves="2" seed="7"/>'
        '<feColorMatrix values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 -14 11.1"/>'
        '<feComposite in="SourceGraphic" operator="in"/></filter></defs>'
    )
    stamp_inner = c.d
    c.d = []
    x0, y0, x1, y1 = c.box
    (OUT / "stamp.svg").write_text(
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{x0 - 6:.0f} {y0 - 6:.0f} {x1 - x0 + 12:.0f} {y1 - y0 + 12:.0f}" '
        f'role="img" aria-label="Built for the Elements" color="{RUST}" fill="currentColor">'
        f"<title>Built for the Elements</title>{defs}"
        f'<g filter="url(#ud-wear)">{ring}<path d="{"".join(stamp_inner)}"/>{stars}</g></svg>\n',
        encoding="utf-8",
    )
    print(f"{'stamp.svg':24} {(OUT / 'stamp.svg').stat().st_size // 1024} KB")

    favicons(d, dw, dh)
    og_image()

    # Drop the traced duck into the icon sprite's filled i-duck symbol (facing right).
    icons = OUT / "icons.svg"
    sym = f'<symbol id="i-duck" viewBox="0 0 {dw} {dh}"><path fill="currentColor" transform="matrix(-1 0 0 1 {dw} 0)" d="{d}"/></symbol>'
    icons.write_text(re.sub(r'<symbol id="i-duck".*?</symbol>', lambda _: sym, icons.read_text(encoding="utf-8"), flags=re.S), encoding="utf-8")
    print("icons.svg                i-duck updated")


def star(cx, cy, r):
    pts = []
    for i in range(10):
        a = math.pi / 2 + i * math.pi / 5
        rr = r if i % 2 == 0 else r * 0.42
        pts.append(f"{cx + rr * math.cos(a):.1f},{cy - rr * math.sin(a):.1f}")
    return f'<polygon points="{" ".join(pts)}"/>'


# ---------------------------------------------------------------- raster outputs
def duck_raster(height: int) -> Image.Image:
    """Duck as an alpha mask at the given height (from the clean tracing mask), facing right."""
    m = Image.open(BUILD / "duck-icon.png").convert("L")
    m = Image.eval(m, lambda v: 255 - v).transpose(Image.FLIP_LEFT_RIGHT)
    return m.resize((round(m.width * height / m.height), height), Image.LANCZOS)


def favicons(d, dw, dh):
    s = 0.72 * 64 / dh
    w = dw * s
    (OUT / "favicon.svg").write_text(
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64">'
        f'<rect width="64" height="64" fill="{NAVY}"/>'
        f'<path fill="{SAIL}" transform="translate({32 + w / 2:.2f} {64 * 0.14:.2f}) scale({-s:.5f} {s:.5f})" d="{d}"/></svg>\n',
        encoding="utf-8",
    )

    def tile(px):
        im = Image.new("RGB", (px, px), NAVY)
        duck = duck_raster(round(px * 0.72))
        im.paste(SAIL, ((px - duck.width) // 2, round(px * 0.14)), duck)
        return im

    tile(32).save(OUT / "favicon-32.png")
    tile(180).save(OUT / "apple-touch-icon.png")
    tile(192).save(OUT / "icon-192.png")
    tile(512).save(OUT / "icon-512.png")
    tile(256).save(OUT / "favicon.ico", sizes=[(16, 16), (32, 32), (48, 48)])
    print("favicons                 svg, ico, 32, 180, 192, 512")


def og_image():
    W, H = 1200, 630
    im = Image.new("RGB", (W, H), SAIL)
    dr = ImageDraw.Draw(im)
    disp = ImageFont.truetype(str(FONTS / "Rokkitt-VF.ttf"), 128)
    disp.set_variation_by_axes([800])
    ui = ImageFont.truetype(str(FONTS / "WorkSans-VF.ttf"), 26)
    ui.set_variation_by_axes([600])
    duck = duck_raster(170)
    im.paste(NAVY, ((W - duck.width) // 2, 92), duck)
    name = "URBAN DUCK"
    spacing = 4
    widths = [dr.textlength(ch, font=disp) for ch in name]
    total = sum(widths) + spacing * (len(name) - 1)
    x = (W - total) / 2
    for ch, cw in zip(name, widths):
        dr.text((x, 300), ch, font=disp, fill=NAVY)
        x += cw + spacing
    tag = "W O R K I N G   C L A S S   L U X U R Y"
    tw = dr.textlength(tag, font=ui)
    dr.text(((W - tw) / 2, 462), tag, font=ui, fill=NAVY)
    dr.rectangle(((W - tw) / 2 - 80, 476, (W - tw) / 2 - 28, 478), fill=RUST)
    dr.rectangle(((W + tw) / 2 + 28, 476, (W + tw) / 2 + 80, 478), fill=RUST)
    dr.rectangle((0, H - 14, W, H), fill=NIGHT)
    im.save(OUT / "og-default.png", optimize=True)
    print("og-default.png           1200x630")


if __name__ == "__main__":
    main()

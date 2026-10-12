"""Step 1 of logo tracing: turn the raster marks in brand/reference/ into clean
black-on-white masks (scripts/brand/.build/*.png). Step 2 is trace.mjs.

Run: python scripts/brand/trace_logos.py && node scripts/brand/trace.mjs
"""
from pathlib import Path

from PIL import Image, ImageFilter

ROOT = Path(__file__).resolve().parents[2]
REF = ROOT / "brand" / "reference"
BUILD = Path(__file__).resolve().parent / ".build"


def ink_mask(path: Path, upscale: int = 1) -> Image.Image:
    """Mask of the dark, opaque pixels, cropped to the artwork (shape = black)."""
    im = Image.open(path).convert("RGBA")
    if upscale > 1:
        im = im.resize((im.width * upscale, im.height * upscale), Image.LANCZOS)
    ink = Image.eval(im.convert("L"), lambda v: 255 if v < 128 else 0)
    opaque = Image.eval(im.getchannel("A"), lambda a: 255 if a > 128 else 0)
    mask = Image.composite(ink, Image.new("L", im.size, 0), opaque).filter(ImageFilter.MedianFilter(3))
    l, t, r, b = mask.getbbox()
    pad = 4 * upscale
    mask = mask.crop((max(l - pad, 0), max(t - pad, 0), min(r + pad, im.width), min(b + pad, im.height)))
    return Image.eval(mask, lambda v: 255 - v)


def main() -> None:
    BUILD.mkdir(exist_ok=True)
    jobs = {
        "duck-icon": ink_mask(REF / "icon-duck-standing.webp"),
        # 2x upscale keeps the thin underline and the flying duck's edges crisp.
        "logo-corporate": ink_mask(REF / "logo-corporate-horizontal-hires.webp", upscale=2),
    }
    for name, mask in jobs.items():
        mask.convert("RGB").save(BUILD / f"{name}.png")
        print(f"mask {name}.png {mask.size}")


if __name__ == "__main__":
    main()

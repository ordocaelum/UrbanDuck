# Urban Duck — Website

**Urban Duck · Working Class Luxury.** The rebuild of the Urban Duck store, moving off GoDaddy to GitHub + Cloudflare Pages, with Stripe Checkout.

- [ROADMAP.md](ROADMAP.md): stages, architecture, open decisions
- [DESIGN.md](DESIGN.md): brand and design system (colors, type, logos, components, imagery, voice)
- [styletile/index.html](styletile/index.html): Stage 1 style tile for sign-off (open it in a browser)

## Current stage

**Stage 1: Brand & design system.** Waiting on sign-off. See the style tile.

## Layout

```
brand/reference/     logos + catalog comps as supplied
brand/fonts/         Rokkitt, Work Sans, Libre Caslon Text (SIL Open Font License)
public/brand/        production marks: lockups, corporate logo, duck icon, stamp, icon sprite, favicons, OG image
scripts/brand/       scripts that rebuild public/brand/ from brand/
scripts/build_styletile.py   bundles styletile/template.html into styletile/index.html
styletile/           style tile source, placeholder images, and built page
```

## Rebuilding the brand assets

Needs Python 3 with `pillow` and `fonttools`, and Node 18+.

```bash
cd scripts/brand && npm install && cd ../..
python scripts/brand/trace_logos.py   # raster logos -> clean masks
node scripts/brand/trace.mjs          # masks -> duck-icon.svg, logo-corporate.svg
python scripts/brand/build_marks.py   # lockups, stamp, favicons, OG image, duck icon in sprite
python scripts/build_styletile.py     # style tile
```

# Urban Duck — Design System

> **Urban Duck · Working Class Luxury**
> Workwear honesty, luxury restraint. Built for the elements, presented like something worth keeping.

This document is the single source of truth for how the Urban Duck website (and the catalog / lookbook that sit beside it) look, read, and behave. If a design decision isn't covered here, add it here before building it.

Status legend: ✅ decided · 🟡 proposed, confirm in Stage 1 style tile · ❓ open question (see [ROADMAP.md › Open decisions](ROADMAP.md#open-decisions))

---

## 1. Brand architecture

```
URBAN DUCK  (master brand)              tagline: "Working Class Luxury"
├── Marina Goods        ← all current products (tees, kids tees, hats, totes, rope totes, beach towels)
└── Coastal Outfitter   ← second product line, launches later (site supports it from day one)
```

| Element | Use | Status |
|---|---|---|
| **Master brand** | "Urban Duck". Always two words, always uppercase in marks, title case in running text. | ✅ |
| **Tagline** | "Working Class Luxury". Sits under the header lockup and in hero / footer. Never paraphrased. | ✅ |
| **Product lines** | "Marina Goods" and "Coastal Outfitter" are *lines*, shown as small labels on product cards / pages and as collection filters, never in place of the master brand. | ✅ |
| **Supporting phrases** | "Built for the elements." · "Work hard. Live salty. Stay grounded." · "Long days. Salty souls." · "Quality goods for a life well lived." · "Work. Fish. Repeat." · "Carry good things." | ✅ (from catalog) |

---

## 2. Logos & marks

Reference files live in [`brand/reference/`](brand/reference/). Production files live in [`public/brand/`](public/brand/). Every SVG is single-color (`fill="currentColor"`), so CSS sets the color. All lettering is converted to outlines, so the marks look the same everywhere with or without fonts. Rebuild them with the scripts in `scripts/brand/` (see README).

| Mark | Production file | Where it goes |
|---|---|---|
| **Header lockup, stacked** (standing duck over arched "URBAN DUCK" + "WORKING CLASS LUXURY") | `lockup-stacked.svg` | Site header at the top of every page, catalog interior pages, social avatar. ✅ |
| **Compact lockup** (duck + URBAN DUCK, no tagline) | `lockup-compact.svg` | Slim header after scrolling, and anywhere under ~200px wide where the tagline would be unreadable. ✅ |
| **Horizontal lockup** (duck + URBAN DUCK, tagline justified beneath) | `lockup-horizontal.svg` | Wide spaces: email header, catalog, wholesale PDF. ✅ |
| **Corporate horizontal logo** (black serif URBAN DUCK, flying duck through the "D", underline) | `logo-corporate.svg` (vector trace) | *Strategic placements only*: footer, Our Story page, Wholesale page, order confirmation page, packing slip / invoice, catalog & lookbook covers and back covers, email header. Never in the header, never on product photography. ✅ |
| **Duck icon** (standing duck silhouette) | `duck-icon.svg`; also `#i-duck` in the icon sprite | Favicon, loading states, section dividers, "end of page" mark, empty cart. In lockups and icons the duck faces right, like the catalog. ✅ |
| **Favicons** | `favicon.svg`, `favicon.ico`, `favicon-32.png`, `apple-touch-icon.png`, `icon-192/512.png` | Sailcloth duck on a Harbor Navy square. ✅ |
| **Social share image** | `og-default.png` (1200×630) | Default link preview. Pages with their own hero image get their own. ✅ |
| **"Built for the Elements" stamp** (circular UD seal) | `stamp.svg` (redrawn and spelled correctly; the catalog version reads "ELEEIENTS") | Hero corner, product pages near the features row, 404 page. Max one per screen. ✅ |
| **Coastal Outfitter wordmark** (navy western slab + rust script) | `logo-coastal-outfitter.webp` | Coastal Outfitter collection page only, once that line launches. Not used at launch. ✅ |

**Logo rules**
- Clear space = height of the "U" in URBAN on all sides.
- Minimum widths: stacked lockup 170px; compact lockup 140px; horizontal lockup 280px (or the tagline drops below 6px tall); corporate logo 160px (below that the underline and flying duck turn to mush).
- Approved colorways: Harbor Navy on Sailcloth, Sailcloth on Night Watch, Corporate Ink on white (print). Never rust, never on photography without a solid or scrim backing.
- Don't stretch, re-letter, add effects, or put the distressed texture on the corporate logo. Distressing belongs to the stamp and catalog-style art only.

---

## 3. Color

Values are sampled from the logo files and the catalog pages, then lightly corrected for screen (the catalog art has a darkened vintage grade). ✅ palette · 🟡 exact tints get final sign-off on the style tile.

### Core

| Token | Hex | Sampled from | Role |
|---|---|---|---|
| `--ud-navy` **Harbor Navy** | `#0B3354` | Coastal Outfitter wordmark | Primary brand color: buttons, links, headings on light |
| `--ud-night` **Night Watch** | `#0D1B24` | Catalog left panels & footer bands | Dark sections, header on scroll, footer, overlays |
| `--ud-duck` **Duck Slate** | `#243447` | Standing duck icon | Icon color, secondary dark |
| `--ud-sail` **Sailcloth** | `#F3EEE4` | Catalog paper (lightened) | Page background |
| `--ud-canvas` **Canvas** | `#E6DCCB` | Catalog paper | Cards, product image backdrops, alt sections |
| `--ud-rust` **Signal Rust** | `#9B3A2A` | Coastal Outfitter script, catalog rules | Accent: underline rules, item numbers, sale/low-stock, focus ring on light |
| `--ud-ink` **Corporate Ink** | `#231F20` | Corporate horizontal logo | Corporate logo only, and body text if navy reads too blue |

### Supporting (from the product colorways; use for swatches & small accents only)

| Token | Hex | Name |
|---|---|---|
| `--ud-brass` | `#C9A98A` | Brass: accent on dark backgrounds (rust fails contrast there) |
| `--ud-olive` | `#4A4C34` | Sea Green / Olive |
| `--ud-sand` | `#CAB29D` | Sand / Khaki |
| `--ud-stone` | `#6B665C` | Stone: secondary text on light |

### Contrast (WCAG 2.1, measured)

| Pair | Ratio | Allowed for |
|---|---|---|
| Night Watch on Sailcloth | 15.1 : 1 | everything |
| Harbor Navy on Sailcloth | 11.2 : 1 | everything |
| Harbor Navy on Canvas | 9.6 : 1 | everything |
| Sailcloth on Night Watch | 15.1 : 1 | everything |
| Brass on Night Watch | 7.9 : 1 | everything |
| Signal Rust on Sailcloth | 6.0 : 1 | text ≥ 14px, labels, prices |
| Signal Rust on Canvas | 5.1 : 1 | text ≥ 14px |
| Stone on Sailcloth | 4.9 : 1 | secondary text ≥ 14px |
| ❌ Signal Rust on Night Watch | 2.5 : 1 | **never for text**. Use Brass on dark |

### Product swatch colors
Swatches on product pages use the colorway names from the catalog (Navy, Ivory, Sea Green, Black, Blue Jean, Sand, Natural, Heather Grey, Rust, Khaki, Olive, Charcoal, Tan). Each swatch hex is set per variant in the catalog data, sampled from the real product photo, not from this palette.

---

## 4. Typography

🟡 Font choices are proposed. They're chosen to match the catalog's voice and are all free and self-hosted (via Fontsource; no Google Fonts request at runtime, so it's faster and needs no cookie banner). Final call on the Stage 1 style tile.

| Role | Proposed family | Why | Fallback |
|---|---|---|---|
| **Display**: page titles, section heads, header lockup | **Rokkitt** (600–800, uppercase, +2% tracking) | Narrow bracketed slab, closest free match to the catalog's "CLASSIC TEES / BUILT FOR THE ELEMENTS" headings | `Georgia, serif` |
| **Editorial serif**: pull quotes, Our Story, tagline in long-form | **Libre Caslon Text** (400, 400 italic) | Echoes the corporate logo's classic serif; brings in the "luxury" half of the tagline | `Georgia, serif` |
| **UI & body**: nav, labels, specs, buttons, body copy | **Work Sans** (400, 500, 600) | Matches the catalog's tracked-caps spec labels ("NAVY · S · M · L · 100% COTTON") | `system-ui, sans-serif` |
| *Coastal Outfitter script* | *(later, match the rust script in that logo)* | Only on that line's collection page | n/a |

### Type scale (fluid, `clamp()`; mobile → desktop)

| Token | Size | Family / weight | Case & tracking | Use |
|---|---|---|---|---|
| `--fs-hero` | 44 → 88px | Display 800 | UPPER, 0.02em | Homepage hero only |
| `--fs-h1` | 36 → 60px | Display 700 | UPPER, 0.02em | Page titles ("TEES", "HATS") |
| `--fs-h2` | 26 → 36px | Display 700 | UPPER, 0.03em | Section heads ("CLASSIC TEES") + rust rule beneath |
| `--fs-h3` | 18 → 20px | UI 600 | UPPER, 0.12em | Product names on cards |
| `--fs-quote` | 22 → 32px | Editorial italic | Sentence | Pull quotes, manifesto |
| `--fs-body` | 16 → 17px | UI 400, line-height 1.6 | Sentence | Paragraphs (max 65ch) |
| `--fs-label` | 12 → 13px | UI 500 | UPPER, 0.16em | Specs, eyebrow text, nav, buttons |
| `--fs-num` | 14px | UI 600, Rust | 0.08em | Catalog item numbers "01" |

**Rules:** Display face is always uppercase. Never set body copy in all caps. Never more than three type sizes in one component. Headlines end with a period when they're a statement ("BUILT FOR THE ELEMENTS."), as in the catalog.

---

## 5. Layout, spacing, shape

- **Grid:** 12 columns, max content width 1320px, gutters 24px (desktop) / 16px (mobile). Text blocks max 65ch.
- **Spacing scale (4px base):** `4 · 8 · 12 · 16 · 24 · 32 · 48 · 64 · 96 · 128`. Section padding is 96px desktop / 64px mobile. *Luxury = whitespace*: when in doubt, add space instead of a divider.
- **Split-panel layout (signature):** the catalog's navy left panel (category title, story, lifestyle photo) + cream right panel (products) becomes the collection page hero on desktop. On mobile it stacks: the navy panel becomes a full-width banner, then the products.
- **Radius:** 0 everywhere (cards, buttons, inputs, images), except 2px on form inputs. Square corners read as print and workwear.
- **Rules & borders:** 1px hairlines in `rgba(13,27,36,.15)`. Section heads get a 48×3px Signal Rust rule beneath (the catalog's red underline). Double-rule "ticket" frames (as on "CARRY GOOD THINGS. LIVE SALTY.") are used sparingly for callouts.
- **Elevation:** none. No drop shadows on UI. Depth comes from color blocks and photography only. The one exception is the cart drawer, which gets a scrim.
- **Texture:** a subtle paper grain (SVG noise, ≤4% opacity) on Sailcloth and Canvas backgrounds. Heavier distress is allowed only inside stamps and catalog-style artwork. Never on text you need to read.

---

## 6. Iconography

Thin-stroke line icons (1.5px stroke, round caps and joins, 24px grid) in Harbor Navy, matching the catalog's feature rows. One sprite: [`public/brand/icons.svg`](public/brand/icons.svg), used as `<svg><use href="/brand/icons.svg#i-anchor"/></svg>`.

- **Brand / feature:** anchor · waves · duck (the one filled glyph) · wheel · knot · cotton · tee · cap · tote · shield · drop · sun · grommet.
- **Shop / UI:** bag · menu · close · search · chevron-down · chevron-right · plus · minus · truck · return · ruler.
- New icons are drawn to the same rules. Never mix in a generic icon set's filled style.

---

## 7. Imagery

### Product photography (real photos — provided by the brand) ✅
- **Primary image:** flat lay or ghost mannequin on a seamless Canvas (`#E6DCCB`)-toned background, soft daylight, consistent top-down angle per category. **Aspect 4:5** for everything (tees, hats, totes, towels) so grids line up.
- **Per product:** 1 primary + 1 alternate (back or on-model, shown on hover) + 1–3 details (tag, stitching, rope handle, grommet, texture).
- **Per colorway:** a primary image for every color variant, so the gallery swaps when a swatch is chosen.
- **Delivery spec:** ≥ 2000px on the long edge, JPG or PNG, file name = SKU base (e.g. `UD-MG-TEE-WCYC-NVY_01.jpg`). Astro generates the AVIF/WebP sizes automatically.
- ❓ If the real photos aren't on a consistent background, we decide in Stage 1 between re-shooting and a batch background clean-up.

### Atmosphere & lifestyle (Higgsfield — supporting imagery only) ✅
Use for homepage hero, collection-panel backgrounds, lookbook spreads, Our Story, wholesale banner, 404.

- **World:** working New England harbor. Weathered cedar-shingle boathouses, pilings wrapped in manila rope, painted buoys, lobster/fishing boats, moored sailboats, wet dock planks.
- **Light & grade:** overcast or golden hour, desaturated, warm shadows, slight film grain, muted navy-teal water. Never bright tropical, never neon, never HDR.
- **People:** real-looking, working-class-not-costume. Weathered hands, rolled sleeves, kids on the dock. No posed fashion-model smiles.
- **Hard rules:**
  1. **No AI-generated product designs.** Higgsfield images must not show Urban Duck garments, logos, or text, because AI garbles text (the catalog comps have "ELEEIENTS", "NLACK", "WORTH ATLANTIC"). Products appear only in real photos, or real product photos composited into a scene.
  2. No legible fake signage. If a sign appears, it's blank or out of focus.
  3. Every generated image is checked at 100% zoom for hands, rope physics, and text artifacts before use.
- **Prompt skeleton** (keep consistent across generations):
  `editorial photograph, working New England harbor at [overcast morning | golden hour], [subject], weathered cedar shingles and manila rope, muted navy and warm cream palette, desaturated film grade, subtle grain, 35mm, shallow depth of field, no text, no logos`
- **Aspect ratios:** hero 16:9 desktop + 4:5 mobile crop (generate both); collection panel 3:4; lookbook 4:5 and 3:2.

---

## 8. Voice & copy

**Plainspoken, confident, salt-weathered. Short sentences. Nouns from the waterfront.** Sounds like a guy who owns one good jacket and has had it for fifteen years.

| Do | Don't |
|---|---|
| "Built for the elements. Made to last." | "Our AMAZING new collection is here!!" |
| "Garment dyed for a broken-in feel from day one." | "Ultra-premium luxe fabric experience" |
| "Only 2 left in L." | "Hurry! Selling fast! 🔥" |
| Periods. Fragments. Rhythm. | Exclamation marks, emoji, hashtags in site copy |

- **Product names** follow the catalog: design name + product type, e.g. "Working Class Yacht Club Tee", "Cold Water Therapy Trucker Hat".
- **Spec block** order (as in the catalog): `01` number → Name → Color → Sizes → Material.
- **Microcopy:** "Add to Bag" (not Cart), "Your Bag", "Checkout", "Sold Out", "Back Soon", "Only N left".

---

## 9. Components

Each one gets built in Stage 2 / 3 and lives in `src/components/`.

| Component | Spec |
|---|---|
| **Announcement bar** | Night Watch, Brass label text, one line ("Free shipping over $X" ❓). Dismissible. |
| **Header** | Sailcloth background, header lockup centered, nav left (Shop · Lookbook · Our Story · Wholesale), bag icon + count right. On scroll it shrinks to 64px and switches to Night Watch with the Sailcloth lockup. Mobile: hamburger left, lockup center, bag right. |
| **Mega/shop menu** | Category list (Tees · Kids · Hats · Totes · Rope Totes · Beach Towels) + line filter (Marina Goods / Coastal Outfitter) + one lifestyle image. |
| **Collection hero** | Split panel (see §5): navy left with giant display category title ("TEES"), anchor + rust rules, story text; right = section heads + grid. |
| **Product card** | 4:5 image on Canvas, hover swaps to alternate image. Below: rust number, name (h3), colorway label, price. Badges top-left: "Sold Out" (Night Watch fill), "Only N left" (Rust text), "New" (Navy outline). No buttons on the card; the whole card is the link. |
| **Product page** | Left: gallery (thumbnails desktop, swipe mobile). Right: line label, name, price, color swatches (square, 32px, named on hover), size buttons (square, sold-out sizes struck through and disabled), qty, **Add to Bag** (full-width, Navy), stock note, accordion (Details · Fit & Size Guide · Care · Shipping & Returns). Below: features row (icons) + "Built for the Elements" stamp + "Pairs well with" row. |
| **Buttons** | Primary: Navy fill, Sailcloth label, uppercase label style, 52px tall, square. Hover: Night Watch. Secondary: 1px Navy outline. On dark: Sailcloth fill, Night Watch label. Focus: 2px Rust outline, 2px offset. |
| **Cart drawer** | Slides from right, 440px (full-screen on mobile). Line items with thumb, name, color/size, qty stepper, remove. Subtotal, shipping note, **Checkout** → Stripe. Empty state: duck icon + "Your bag is empty. The dock is open." |
| **Feature row** | 4–5 icons with uppercase label + 2-line description, separated by vertical hairlines (exactly as in the catalog). |
| **Stamp** | Circular "Built for the Elements · UD" seal, Rust, rotated −8°, distressed. Decorative (`aria-hidden`). |
| **Footer** | Night Watch. Corporate horizontal logo (Sailcloth knockout), tagline, nav columns (Shop · Help · Company), wholesale CTA, socials ❓, newsletter (later stage), "Urban Duck · Est. 2024 ❓". |
| **Forms** (wholesale, admin) | Canvas fill, 1px hairline, 2px radius, label above in label style, error text in Rust. |

---

## 10. Motion

Restrained. Things *settle*, they don't bounce.
- Durations: 150ms (hover, color), 300ms (drawers, accordions), 600ms (image fade-in).
- Easing: `cubic-bezier(.2,.7,.2,1)`.
- Allowed: image fade/slight rise on scroll (once), card hover image swap (crossfade), drawer slide, header shrink.
- Not allowed: parallax-heavy scrolling, carousels that auto-advance, bouncing, confetti.
- Everything respects `prefers-reduced-motion: reduce` (no movement, fades only).

---

## 11. Accessibility & performance targets

- WCAG 2.1 AA (contrast table in §3; every interactive element keyboard-reachable; visible focus; alt text for every product image, e.g. "Navy Working Class Yacht Club tee, flat lay").
- Lighthouse ≥ 95 on Performance, Accessibility, Best Practices, and SEO for home, collection, and product pages (mobile).
- LCP < 2.0s on 4G; total JS on product page < 30KB gzipped (cart island only).
- Fonts: self-hosted WOFF2, subset to Latin, `font-display: swap`, display face preloaded.
- Images: AVIF/WebP with responsive `srcset`, lazy below the fold, explicit width/height (no layout shift).

---

## 12. Design tokens (copy into `src/styles/tokens.css`)

```css
:root {
  /* color */
  --ud-navy:   #0B3354;
  --ud-night:  #0D1B24;
  --ud-duck:   #243447;
  --ud-sail:   #F3EEE4;
  --ud-canvas: #E6DCCB;
  --ud-rust:   #9B3A2A;
  --ud-ink:    #231F20;
  --ud-brass:  #C9A98A;
  --ud-olive:  #4A4C34;
  --ud-sand:   #CAB29D;
  --ud-stone:  #6B665C;
  --ud-rule:   rgba(13, 27, 36, .15);

  /* type */
  --font-display:   "Rokkitt", Georgia, serif;
  --font-editorial: "Libre Caslon Text", Georgia, serif;
  --font-ui:        "Work Sans", system-ui, sans-serif;

  --fs-hero:  clamp(2.75rem, 1.6rem + 5vw, 5.5rem);
  --fs-h1:    clamp(2.25rem, 1.5rem + 3.2vw, 3.75rem);
  --fs-h2:    clamp(1.625rem, 1.3rem + 1.4vw, 2.25rem);
  --fs-h3:    clamp(1.125rem, 1.08rem + .2vw, 1.25rem);
  --fs-quote: clamp(1.375rem, 1.1rem + 1.2vw, 2rem);
  --fs-body:  clamp(1rem, .98rem + .1vw, 1.0625rem);
  --fs-label: clamp(.75rem, .73rem + .1vw, .8125rem);

  --track-display: .02em;
  --track-label:   .16em;

  /* space */
  --sp-1: 4px;  --sp-2: 8px;  --sp-3: 12px; --sp-4: 16px; --sp-5: 24px;
  --sp-6: 32px; --sp-7: 48px; --sp-8: 64px; --sp-9: 96px; --sp-10: 128px;

  /* layout */
  --max-w: 1320px;
  --gutter: clamp(16px, 2vw, 24px);
  --radius: 0;
  --radius-input: 2px;

  /* motion */
  --ease: cubic-bezier(.2, .7, .2, 1);
  --dur-fast: 150ms; --dur-med: 300ms; --dur-slow: 600ms;
}
```

---

## 13. Catalog & lookbook alignment

The website, the PDF wholesale catalog, and the lookbook share this system. When the catalog is next revised:
- Use the corporate horizontal logo on the cover and back cover; use the header lockup on interior pages.
- Fix the AI-generated text errors in the current comps: "ELEEIENTS" (stamp, multiple pages), "WORTH ATLANTIC SURF CO." → North Atlantic, "NLACK" → Black, cover "DESIGNED FOR EVERYDAY" vs back cover "EVERY DAY" (pick one), page numbering (Tees is "08", Kids is "02").
- Replace the placeholder contact info (the 401.**555**.0184 number is a fictional 555 number; confirm the real handle, email, and domain).
- Product names, colorways, and numbering must match the site's catalog data file exactly. The data file is the source of truth.

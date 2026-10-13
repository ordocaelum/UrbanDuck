# Urban Duck Website — Roadmap

Rebuild of the Urban Duck site, moving off GoDaddy. Design rules live in [DESIGN.md](DESIGN.md); this file covers **what we build, how it fits together, and in what order.**

---

## Decisions so far ✅

| Topic | Decision |
|---|---|
| Code & hosting | Code on **GitHub** → **GitHub Pages** (free). Domains at **Squarespace** point to it. No Squarespace hosting plan. |
| Domain | Site domain **urbanduckapparel.com**. Transfer both domains (also trendsetprotraders.com) **GoDaddy → Squarespace Domains**. GoDaddy also hosts **email and a site builder**; see [GoDaddy exit plan](#godaddy-exit-plan). |
| Business | Company: **Trendsetprotraders** (TSPT). Mostly **wholesale today** (2 accounts); no retail sales yet. Instagram **@urbanduckapparel**. |
| Contact emails | Customer support **support@urbanduckapparel.com** · wholesale/orders **orders@trendsetprotraders.com** · owner **adoss@trendsetprotraders.com** |
| Framework | **Astro** (static HTML, near-zero JS) + a tiny vanilla-JS cart. Server bits are **Supabase Edge Functions**. |
| Payments | **Stripe Checkout** (hosted page). **No Stripe products to create.** Prices come from our catalog file at checkout time (details below). |
| Inventory | **Real stock counts** per SKU in **Supabase** (free Postgres, kept awake by a scheduled ping), auto-decremented on paid orders, sold-out / low-stock shown on site. |
| Stock admin | Password-protected **`/admin`** page on the site, signed in with **Supabase Auth** emailed links, limited to an allow-list of addresses. |
| Orders & shipping info | Read from the **Stripe dashboard** (name, email, phone, shipping address, items with size/color/SKU). |
| Product lines | Master brand **Urban Duck**; lines **Marina Goods** (all current products) and **Coastal Outfitter** (later). Site supports multiple lines from day one. |
| Imagery | **Real product photos** exist. **Higgsfield** is for supporting atmosphere/lifestyle imagery only. |
| Wholesale | **Inquiry page**: pitch + downloadable PDF catalog + contact form. Wholesale orders handled offline. |
| Header mark | **Duck + "URBAN DUCK" + "Working Class Luxury"** lockup. Corporate horizontal logo only in strategic spots (see DESIGN.md §2). |

---

## GoDaddy exit plan

Current GoDaddy account (from My Renewals, Oct 12, 2026):

| Item | Renews | Plan |
|---|---|---|
| trendsetprotraders.com domain (+ Full Domain Protection) | **Oct 24, 2026** | Transfer to Squarespace **before** this date |
| M365 Email Essentials: adoss@trendsetprotraders.com | **Oct 24, 2026** | Migrate mailbox first, then cancel |
| M365 Secure Starter: orders@trendsetprotraders.com | **Oct 28, 2026** | Migrate mailbox first, then cancel |
| Websites + Marketing Commerce (urbanduckapparel.com) | **Oct 28, 2026** | Looks like a duplicate of the one below; confirm which is live, cancel the other |
| Websites + Marketing Commerce (urbanduckapparel.com) | Sep 28, 2027 | Cancel after new site launches (Stage 6) |
| M365 Email Essentials: tspt@urbanduckapparel.com | Sep 17, 2027 | Migrate, then cancel |
| urbanduckapparel.com domain | Sep 18, 2030 | Transfer to Squarespace |
| M365 Secure Starter "New Account" | Expired Sep 28, 2026 | Unused, let it lapse |
| Conversations Free | n/a | Let it go |

**Order of operations (email is the risky part; nothing gets cancelled until its replacement works):**
1. Export anything wanted from the current GoDaddy site (content, product list, any customer/order data).
2. Set up the new email provider ❓ and move the mailboxes (adoss@, orders@, tspt@, plus new support@urbanduckapparel.com).
3. Unlock both domains, get auth codes, start transfers to Squarespace. Transfers carry existing DNS only if records are copied first, so **save every DNS record** (especially MX/TXT for email) before starting.
4. Point DNS: email records → new email provider; website → GitHub Pages (Stage 6).
5. Cancel GoDaddy items one at a time, only after each replacement is confirmed working.

**Deadline pressure:** Oct 24 is 12 days out. If the email move can't finish by then, renew those two items for the shortest term GoDaddy allows rather than risk losing mail.

## Architecture

```
GitHub repo (main) ──push──► GitHub Pages: static Astro site
                               /, /shop/[category], /products/[slug],
                               /lookbook, /our-story, /wholesale, /admin,
                               /order/success, /policies/*
                               cart = localStorage + ~5KB JS
                                    │
              fetch stock / start checkout / admin edits
                                    ▼
┌──────────────────────────── Supabase ─────────────────────────────┐
│ Edge Functions                         Postgres                    │
│  checkout        validate cart vs      inventory(sku, on_hand,     │
│                  catalog, reserve        reserved)                 │
│                  stock, create Stripe  reservations, stripe_events │
│                  Checkout Session      wholesale_inquiries         │
│  stripe-webhook  paid → decrement                                  │
│                  expired → release     Auth: emailed sign-in link  │
│  wholesale       store inquiry +         for /admin (allow-list)   │
│                  notify orders@                                    │
│  Public read: stock levels (row-level security, read-only)         │
└────────────────────────────────────────────────────────────────────┘
          │ Checkout Session                ▲ webhooks
          ▼                                 │
     Stripe Checkout (hosted) ──► Stripe dashboard: orders, customers,
     collects address/phone/card     shipping addresses
```

Domain: `urbanduckapparel.com` registered at **Squarespace Domains**; DNS records point to GitHub Pages (same setup as Leland's other sites).

**Keep-awake:** free Supabase projects pause after ~7 days idle. A scheduled GitHub Action pings the database every few days so checkout never goes to sleep.

### How we avoid creating 200 Stripe products

Stripe Checkout accepts **inline prices** (`line_items[].price_data` with `product_data`). So:

1. The **catalog file** (`src/data/catalog.json`) is the only place products, prices, colors and sizes are defined. It builds the pages *and* is read by the checkout function.
2. The browser sends only `[{ sku, qty }]`. **Prices are never trusted from the browser.** The function looks each SKU up in the catalog.
3. The function creates the Checkout Session with each line item named like
   `Working Class Yacht Club Tee — Navy / L` and the SKU in `product_data.metadata.sku` and in the description, so every order in the Stripe dashboard shows exactly what to pull off the shelf.
4. Adding a product = edit the catalog file + push. Nothing to do in Stripe.

### SKU scheme

`UD-{LINE}-{CAT}-{DESIGN}-{COLOR}-{SIZE}` → e.g. **`UD-MG-TEE-WCYC-NVY-L`**

| Part | Codes |
|---|---|
| LINE | `MG` Marina Goods · `CO` Coastal Outfitter |
| CAT | `TEE` tee · `KTE` kids tee · `CAP` classic cap · `TRK` trucker · `BKT` bucket · `5PN` 5-panel · `TOT` tote · `RTO` rope tote · `TWL` beach towel |
| DESIGN | 4 letters, unique within the category (`WCYC` Working Class Yacht Club, `HRBR` Harbor, `CWDV` Cold Water Division…) |
| COLOR | 3 letters (`NVY` `IVR` `SGR` `BLK` `BJN` `SND` `NAT` `HGR` `RST` `KHK` `OLV` `CHR` `TAN`) |
| SIZE | `S M L XL XXL` · `2T 3T 4T 56 7` · `OS` (one size) · `SM` (S/M) · `LX` (L/XL) |

### Catalog data shape (per product)

```jsonc
{
  "id": "mg-tee-wcyc",
  "line": "marina-goods",
  "category": "tees",            // tees | kids-tees | hats | totes | rope-totes | beach-towels
  "group": "Classic Tees",       // sub-section on the collection page
  "number": "01",
  "name": "Working Class Yacht Club Tee",
  "slug": "working-class-yacht-club-tee",
  "skuBase": "UD-MG-TEE-WCYC",
  "price": 0,                     // cents. ❓ placeholder until prices are set
  "material": "100% cotton",
  "description": "…",
  "features": ["garment-dyed", "relaxed-fit"],
  "colors": [{ "code": "NVY", "name": "Navy", "hex": "#1E2A3A", "images": ["…_01.jpg", "…_02.jpg"] }],
  "sizes": ["S", "M", "L", "XL", "XXL"],
  "status": "active"              // active | hidden | coming-soon
}
```
Variants (SKUs) are generated as colors × sizes, so nobody types SKUs by hand.

### Inventory model (Supabase Postgres)

```sql
inventory   (sku TEXT PRIMARY KEY, on_hand INT, reserved INT, updated_at TEXT)
reservations(session_id TEXT, sku TEXT, qty INT, expires_at TEXT)
stripe_events(event_id TEXT PRIMARY KEY, processed_at TEXT)   -- webhook idempotency
```
- **Checkout:** atomically reserve `qty` only if `on_hand - reserved >= qty`. If any line fails, nothing is reserved and the shopper sees "Only N left in L".
- **Paid** (`checkout.session.completed`): `on_hand -= qty`, `reserved -= qty`.
- **Abandoned** (`checkout.session.expired`, sessions set to expire in 30 min): `reserved -= qty`.
- Product pages stay static; stock badges load from `/api/stock` (edge-cached ~30s), and checkout always re-checks.

### Current catalog size (from the PDF comps)

| Category | Products | Sizes | SKUs |
|---|---|---|---|
| Tees (Classic 3 + Premium 4) | 7 | S–XXL (5) | 35 |
| Kids Tees | 8 | 2T–7 (5) | 40 |
| Hats (classic 4, trucker 4, bucket 2, 5-panel 2) | 12 | OS; bucket S/M, L/XL | 14 |
| Totes | 8 | one size | 8 |
| Rope Totes | 8 | one size | 8 |
| Beach Towels | 8 | 30"×60" | 8 |
| **Total** | **51** | | **113** |

---

## Stages

Each stage ends with something your brother can click on and approve. Nothing goes live on the real domain until Stage 6.

### Stage 0 — Foundations & accounts
**Goal:** every account exists and the slow external steps have started.
- [ ] Private GitHub repo `urban-duck-website`; this folder becomes it.
- [ ] Supabase organization owned by your brother, with you invited as Administrator. Stripe and Google Workspace the same way: he owns, you're a user. Shared password-manager vault for anything that can't add a second user.
- [ ] Stripe account in your brother's name/business (bank account, business details). Stays in **test mode** until Stage 6.
- [ ] **Start the domain transfer now (it takes 5–7 days):** at GoDaddy unlock the domain, turn off any transfer lock, get the auth/EPP code; start the transfer at Squarespace Domains. *(Transfers are blocked for 60 days after a domain is registered or transferred, so check the date.)* Note any existing DNS records first.
- [ ] **Product truth list:** confirm with your brother which of the 51 catalog items really exist, with exact names, colors, sizes, and materials. The catalog comps are AI-generated and contain errors (see DESIGN.md §13).
- [ ] Collect the real product photos into `photos/raw/` (any format; we'll sort them in Stage 1).

**Done when:** accounts exist, transfer is in progress, and the truth list is confirmed.

### Stage 1 — Brand & design system  ← *current: waiting on sign-off*
**Goal:** a visual standard everyone agrees on before pages are built.
- [ ] Review and confirm [DESIGN.md](DESIGN.md) (🟡 items: fonts, exact tints). *Via the style tile sign-off.*
- [x] Production SVGs in `public/brand/`: stacked, horizontal, and compact lockups; corporate logo (vector trace); duck icon; "Built for the Elements" stamp (spelled correctly); favicon set; social share image.
- [x] Line-icon SVG sprite (`public/brand/icons.svg`): 13 brand/feature icons + 11 shop/UI icons.
- [x] **Style tile** (`styletile/index.html`): logos, header states, color, type, buttons, product page, bag, collection page, icons, imagery and voice rules, plus a sign-off sheet.
- [ ] Photo audit: map every photo to a SKU, flag missing colorways, decide re-shoot vs. background clean-up. *Blocked: waiting on the real photos.*
- [ ] Higgsfield test batch: 3 homepage hero options + 1 collection panel using the DESIGN.md §7 prompt skeleton.

**Done when:** your brother approves the style tile and a hero image.

### Stage 2 — Site skeleton & catalog (no commerce yet)
**Goal:** the whole site clickable on GitHub Pages, on a phone.
- [ ] Astro project, `tokens.css` from DESIGN.md §12, self-hosted fonts, base layout, header (sticky/shrink), footer, mobile nav.
- [ ] `catalog.json` for all products in the truth list (placeholder prices allowed), SKU generator, validation script (fails the build on duplicate SKUs, missing images, or bad codes).
- [ ] Pages: Home · Shop (all) · 6 category collection pages (split-panel hero) · Product page template · Lookbook · Our Story · Wholesale (form posts to a placeholder) · Shipping / Returns / Privacy / Terms (placeholder text) · 404.
- [ ] Line support: "Marina Goods" label + line filter. Coastal Outfitter is hidden until it has products.
- [ ] GitHub Pages deploy via GitHub Actions on every push to main.

**Done when:** the preview link works end-to-end on mobile and desktop and your brother signs off on page content.

### Stage 3 — Cart & checkout
**3a. Placeholder checkout** *(what you asked for first)*
- [ ] Cart store (localStorage), "Add to Bag" with size/color validation, cart drawer, bag count in header.
- [ ] `/api/checkout` function behind an env switch `CHECKOUT_MODE=placeholder|stripe`. In placeholder mode it validates the cart against the catalog and redirects to `/checkout/placeholder` (shows "Stripe goes here" + the exact line items that *would* be sent).
- [ ] `/order/success` and `/order/cancelled` pages.

**3b. Stripe (test mode)**
- [ ] Stripe secret key + webhook secret stored as Supabase Edge Function secrets (never in the repo).
- [ ] Checkout Session: inline `price_data`, SKU metadata, `shipping_address_collection` (countries ❓), phone collection, placeholder flat shipping rate ❓, automatic receipts, optional promo codes.
- [ ] `/api/stripe-webhook` with signature verification (logging only at this point; stock comes in Stage 4).
- [ ] Success page reads the session and shows the order summary.
- [ ] Stripe Checkout branding: logo, Harbor Navy, Sailcloth.

**Done when:** a test-card (`4242…`) order shows up in the Stripe test dashboard with name, address, and every item's size, color, and SKU.

### Stage 4 — Inventory & admin
**Goal:** the site can't sell what isn't on the shelf.
- [ ] Supabase tables + SQL migrations, row-level security; seed every SKU from the catalog at 0 stock; keep-awake GitHub Action.
- [ ] `/api/stock` (public, cached) → sold-out sizes struck through, "Only N left" at ≤ threshold ❓, "Sold Out" badges on cards.
- [ ] Reservation on checkout; decrement/release in the webhook; idempotency on Stripe event IDs.
- [ ] `/admin` behind Supabase Auth (allow-listed emails): table of products × sizes, edit on-hand counts, search/filter, "receive stock" (+N) action, CSV export.
- [ ] Tests: two shoppers racing for the last unit (only one succeeds); an expired session releases stock; a webhook replay doesn't double-decrement.

**Done when:** your brother sets real counts in `/admin` and test orders move them correctly.

### Stage 5 — Polish & pre-launch
- [ ] Final copy (product descriptions, Our Story, policies), final prices, final shipping rule.
- [ ] Final photography and Higgsfield imagery placed; lookbook built.
- [ ] Wholesale form live: spam protection (honeypot + Cloudflare Turnstile or hCaptcha) + delivery to the business inbox ❓.
- [ ] SEO: titles/descriptions, Open Graph images, `Product` JSON-LD (price, availability from stock), sitemap, robots.
- [ ] Cookieless analytics (e.g. Cloudflare Web Analytics script or Plausible) ❓.
- [ ] Accessibility pass + Lighthouse ≥ 95 targets from DESIGN.md §11.
- [ ] PDF wholesale catalog (fixed typos) available for download on /wholesale.

**Done when:** the pre-launch checklist passes on the preview URL.

### Stage 6 — Launch & cutover
- [ ] Domain transfer confirmed complete at Squarespace.
- [ ] Squarespace DNS → GitHub Pages (apex A records + `www` CNAME); custom domain set in repo settings; HTTPS enforced.
- [ ] Stripe: switch to **live** keys, register the live webhook, run one real purchase + refund.
- [ ] Set real starting inventory in `/admin`.
- [ ] Email on Google Workspace (via Squarespace); support@ and orders@ as aliases where possible.
- [ ] Only after all of the above: cancel remaining GoDaddy services and auto-renew.

**Done when:** the site is live on the real domain and the first real order is fulfilled.

### Stage 7 — After launch (backlog, priority TBD)
- Coastal Outfitter line launch (collection page, script wordmark, products).
- Shipping labels and "shipped" emails with tracking (Shippo / ShipStation). *Stripe's dashboard has no "shipped" status; until then, a simple workaround is adding a note or metadata on the payment.*
- Order log to Google Sheet (if the Stripe dashboard turns out not to be enough).
- Newsletter sign-up (provider ❓).
- Back-in-stock notifications, gift cards, reviews.
- Wholesale portal (logins, wholesale pricing, minimums).

---

## Open decisions

| # | Question | Needed by |
|---|---|---|
| 1 | Domain name, real contact email, phone, and social handles (the catalog's are placeholders) | Stage 0 |
| 2 | Product truth list: which catalog items exist, with exact names, colors, sizes | Stage 0 |
| 3 | Final fonts and tints (DESIGN.md 🟡) | Stage 1 |
| 4 | Is "Est. 2024" correct? | Stage 1 |
| 5 | Wholesale form: destination email and fields (business name, resale cert, est. quantity?) | Stage 2 |
| 6 | Prices for every product (or a price per category tier) | Stage 3b |
| 7 | Ship-to countries (US only?) | Stage 3b |
| 8 | Shipping model and rates (placeholder flat rate until decided) | Stage 5 |
| 9 | Sales tax: Stripe Tax (+0.5% per transaction) or not; check with an accountant about which states require it | Stage 3b / 5 |
| 10 | Low-stock threshold for "Only N left" and whether sold-out items allow pre-orders | Stage 4 |
| 11 | Returns and exchanges policy | Stage 5 |
| 12 | Who packs and ships, and how they'll track "shipped" | Stage 6 |
| 13 | Which mailboxes are real users vs. aliases in Google Workspace | Stage 0 |

---

## Running costs (expected)

| Service | Cost |
|---|---|
| GitHub (private repo) | Free |
| GitHub Pages | Free |
| Supabase (Edge Functions, Postgres, Auth) | Free tier, kept awake by scheduled ping |
| Google Workspace via Squarespace | Per mailbox, monthly |
| Squarespace Domains | Annual domain renewal only |
| Stripe | Per-transaction fees only (no monthly fee); Stripe Tax adds a fee if enabled |
| Higgsfield | Existing plan |

---

## Repo layout (target)

```
/
├── DESIGN.md  ROADMAP.md  README.md
├── brand/reference/         ← logos & catalog comps (provided)
├── photos/raw/              ← real product photos as delivered (git-ignored if large)
├── public/brand/            ← production SVG logos, favicon, OG image
├── src/
│   ├── data/catalog.json    ← THE product source of truth
│   ├── styles/tokens.css
│   ├── components/          ← Header, Footer, ProductCard, CartDrawer, …
│   ├── layouts/
│   ├── pages/               ← index, shop/[category], products/[slug], lookbook, …
│   └── lib/                 ← sku.ts, catalog.ts (shared by pages + functions)
├── supabase/functions/      ← checkout, stripe-webhook, wholesale
├── supabase/migrations/     ← SQL schema + row-level security
└── scripts/validate-catalog.ts
```

"""Build docs/Urban-Duck-Gameplan.pdf (shareable plan for the owner).

Run: python scripts/build_gameplan.py   (needs: reportlab, fonttools)
"""
from pathlib import Path

from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont
from reportlab.graphics.shapes import Drawing, Rect
from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont as RLFont
from reportlab.platypus import KeepTogether, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

ROOT = Path(__file__).resolve().parents[1]
FONTS, BUILD = ROOT / "brand" / "fonts", ROOT / "scripts" / "brand" / ".build"
BUILD.mkdir(parents=True, exist_ok=True)
NAVY, NIGHT, RUST, CANVAS, STONE, RULE, BRASS = (
    HexColor(c) for c in ("#0B3354", "#0D1B24", "#9B3A2A", "#E6DCCB", "#6B665C", "#D3CABC", "#C9A98A"))


def static(src, wght, name):
    out = BUILD / f"{name}.ttf"
    font = instantiateVariableFont(TTFont(FONTS / src), {"wght": wght})
    for rec in font["name"].names:  # unique internal names, or PDF viewers merge the instances
        if rec.nameID in (1, 3, 4, 6, 16):
            rec.string = f"UD-{name}"
    font.save(out)
    pdfmetrics.registerFont(RLFont(name, str(out)))


static("Rokkitt-VF.ttf", 800, "Display")
static("WorkSans-VF.ttf", 400, "Body")
static("WorkSans-VF.ttf", 700, "BodyBold")
pdfmetrics.registerFontFamily("Body", normal="Body", bold="BodyBold", italic="Body", boldItalic="BodyBold")

S = {
    "h1": ParagraphStyle("h1", fontName="Display", fontSize=30, leading=32, textColor=NAVY, spaceAfter=4),
    "tag": ParagraphStyle("tag", fontName="BodyBold", fontSize=8.5, leading=12, textColor=RUST, spaceAfter=14),
    "h2": ParagraphStyle("h2", fontName="Display", fontSize=15.5, leading=18, textColor=NAVY, spaceBefore=16, spaceAfter=4),
    "p": ParagraphStyle("p", fontName="Body", fontSize=9.6, leading=14, textColor=NIGHT, spaceAfter=6),
    "b": ParagraphStyle("b", fontName="Body", fontSize=9.6, leading=14, textColor=NIGHT, leftIndent=12, bulletIndent=0, spaceAfter=3),
    "cell": ParagraphStyle("cell", fontName="Body", fontSize=8.8, leading=12, textColor=NIGHT),
    "th": ParagraphStyle("th", fontName="BodyBold", fontSize=8, leading=11, textColor=STONE),
    "note": ParagraphStyle("note", fontName="Body", fontSize=8, leading=11, textColor=STONE, spaceBefore=4, spaceAfter=4),
}


def bold(t):
    return t.replace("<b>", '<font name="BodyBold">').replace("</b>", "</font>")


def P(t, s="p"):
    return Paragraph(bold(t), S[s])


def B(t):
    numbered = t[3:4].isdigit()  # "<b>1. ..." steps carry their own number
    return Paragraph(bold(t), S["b"], bulletText=None if numbered else "–")


def h2(t):
    d = Drawing(36, 8)
    d.add(Rect(0, 3, 36, 2.5, fillColor=RUST, strokeColor=None))
    return KeepTogether([P(t, "h2"), d, Spacer(1, 6)])


def table(rows, widths):
    data = [[P(c, "th") for c in rows[0]]] + [[P(c, "cell") for c in r] for r in rows[1:]]
    t = Table(data, colWidths=widths, repeatRows=1)
    t.setStyle(TableStyle([
        ("LINEBELOW", (0, 0), (-1, -1), 0.5, RULE), ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 5), ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("LEFTPADDING", (0, 0), (-1, -1), 4), ("BACKGROUND", (0, 0), (-1, 0), CANVAS)]))
    return t


story = [
    P("URBAN DUCK", "h1"),
    P("WORKING CLASS LUXURY &middot; WEBSITE &amp; IT GAMEPLAN &middot; OCTOBER 2026", "tag"),
    P("The short version: we're moving everything off GoDaddy. The domains and email go to <b>Squarespace</b>, the new "
      "website is built by Leland and hosted <b>free on GitHub</b>, and checkout runs through <b>Stripe</b>, which only "
      "charges when something sells. The site will handle both <b>wholesale and retail</b>."),

    h2("WHY WE'RE SWITCHING"),
    table([["", "Today (GoDaddy)", "New setup"],
           ["Website", "Websites + Marketing Commerce, billed twice for urbanduckapparel.com", "Custom site on GitHub Pages: <b>free</b>"],
           ["Checkout", "GoDaddy's built-in commerce plan", "Stripe: no monthly fee, a small fee per sale"],
           ["Email", "3 Microsoft 365 mailboxes plus extras", "Google Workspace (Gmail) through Squarespace, ideally 1 paid user"],
           ["Domains", "GoDaddy, plus add-on \"protection\" charges", "Squarespace Domains: yearly renewal only"],
           ["Stock counts", "None", "Supabase database: <b>free</b>"],
           ["Roughly", "About $100 a month + $50 a year", "One email user + two domain renewals"]],
          [1.0 * inch, 2.75 * inch, 2.75 * inch]),
    P("Exact Google Workspace and domain prices are whatever Squarespace lists when you sign up.", "note"),

    h2("WHO OWNS WHAT"),
    P("You own and pay for every account. Leland is added as a user with his own login, so nobody shares passwords "
      "and you can never be locked out of your own business."),
    table([["Account", "Owner", "Leland"],
           ["Squarespace (domains + email billing)", "You", "Added as a manager, or through a shared password vault"],
           ["Google Workspace (email)", "You, as main admin", "Second admin, to fix email and reset passwords"],
           ["Stripe (payments, payouts to your bank)", "You", "Team member; never handles bank details"],
           ["Supabase (stock database)", "You", "Invited as Administrator"],
           ["GitHub (website code)", "Leland", "You're added, so you always have access"]],
          [2.2 * inch, 1.5 * inch, 2.8 * inch]),
    P("Turn on two-step login on your phone for every account, and keep the backup codes in a shared password manager "
      "such as Bitwarden or 1Password.", "note"),

    h2("THIS WEEK: LEAVING GODADDY (DEADLINE OCT 24)"),
    P("The trendsetprotraders.com domain and the adoss@ mailbox renew on <b>Oct 24</b>. The orders@ mailbox and a website "
      "plan renew on <b>Oct 28</b>. One rule: <b>nothing gets cancelled until its replacement is working.</b>"),
    B("<b>1. Save the DNS settings.</b> Leland copies every DNS record for both domains, especially the email ones."),
    B("<b>2. Save the old site.</b> Keep any text, photos or product info worth reusing from the GoDaddy site."),
    B("<b>3. Set up Google Workspace</b> through Squarespace and create the addresses in the email plan below."),
    B("<b>4. Move the mail.</b> Google's migration tool copies old Microsoft 365 email into Gmail."),
    B("<b>5. Transfer both domains</b> to Squarespace: unlock them in GoDaddy and get the transfer codes. This takes about 5–7 days."),
    B("<b>6. Cancel GoDaddy</b> one item at a time, once email and domains are working. Turn off auto-renew on everything."),
    P("If the email move isn't done by Oct 24, renew those items for the shortest term GoDaddy offers rather than risk losing mail.", "note"),

    h2("BUILDING THE SITE"),
    table([["Stage", "What happens", "What you'll get"],
           ["1  Brand", "Logos, colors, fonts, style sample page", "A link to approve or request changes. <b>Ready now.</b>"],
           ["2  Site", "Home, shop, product, wholesale and Our Story pages", "A working preview link for your phone"],
           ["3  Checkout", "Cart and Stripe checkout, tested with test cards", "A test order in your Stripe dashboard"],
           ["4  Stock", "Live stock counts, Sold Out / Only 2 left, admin page", "A page where you update quantities"],
           ["5  Polish", "Final photos, copy, prices, policies, search setup", "A site ready to launch"],
           ["6  Launch", "urbanduckapparel.com points to the new site; Stripe goes live", "Your first real online order"]],
          [0.95 * inch, 3.1 * inch, 2.45 * inch]),

    h2("WHAT WE NEED FROM YOU"),
    B("Real product photos: every item, in every color."),
    B("Which catalog items actually exist, with exact names, colors and sizes. The catalog draft has a few typos."),
    B("Retail and wholesale prices, how to charge shipping, and the return policy. These can wait until Stage 3."),
    B("A Stripe account in the business name, connected to the business bank account."),
    B("A free Supabase account, with Leland invited."),
    B("The exact legal business name (for Stripe and the site footer), and whether \"Est. 2024\" is right."),

    h2("EMAIL BEST PRACTICES (GMAIL / GOOGLE WORKSPACE)"),
    P("<b>Pay for people, not addresses.</b> In Google Workspace, each paid user is a person who logs in. Addresses like "
      "orders@ and support@ don't need their own paid accounts. Make them free <b>groups</b> that deliver to the right inbox."),
    P("<b>One account can cover both domains.</b> Make urbanduckapparel.com the main domain and add trendsetprotraders.com "
      "as a secondary domain in the same Workspace, at no extra cost. One login, one bill, both domains."),
    table([["Address", "Type", "Delivers to", "Used for"],
           ["adoss@trendsetprotraders.com", "<b>Paid user</b> (you)", "Your inbox", "You personally"],
           ["orders@trendsetprotraders.com", "Group (free)", "You", "Wholesale and retail orders"],
           ["support@urbanduckapparel.com", "Group (free)", "You (+ Leland if you like)", "Customers; shown on the site and receipts"],
           ["support@trendsetprotraders.com", "Group or alias (free)", "You", "Company-side support"],
           ["tspt@urbanduckapparel.com", "Alias (free) or retire", "You", "Keep only if people still use it"]],
          [2.3 * inch, 1.2 * inch, 1.3 * inch, 1.7 * inch]),
    P("This is a proposal. Confirm which addresses you actually use.", "note"),
    B("<b>Reply from the right address.</b> Use Gmail's \"Send mail as\" so replies to customers come from support@, not your personal address."),
    B("<b>Labels and filters.</b> Auto-label mail by the address it was sent to (Orders, Support, Wholesale) so nothing gets buried."),
    B("<b>Templates.</b> Save ready-made replies for common questions: order status, wholesale pricing, returns."),
    B("<b>Grow without paying more.</b> When you hire help, add them to the orders@ or support@ group. Customers keep using the same address."),
    B("<b>Never run the business from a personal @gmail.com.</b> Keep everything on your own domains so it looks professional and stays yours."),
    B("<b>Security.</b> Two-step login on every account, a recovery phone and email set, and Leland as a backup admin."),
    B("<b>Don't land in spam.</b> Leland adds the SPF, DKIM and DMARC records at Squarespace so your mail reaches inboxes."),
    B("<b>Files.</b> Keep catalogs, price sheets and photos in a Google Shared Drive owned by the business, not in a personal folder."),
]


def frame(c, doc):
    c.saveState()
    c.setFillColor(NIGHT)
    c.rect(0, 0, letter[0], 0.42 * inch, stroke=0, fill=1)
    c.setFillColor(BRASS)
    c.setFont("BodyBold", 7.5)
    c.drawString(0.75 * inch, 0.16 * inch, "URBAN DUCK  ·  BUILT FOR THE ELEMENTS")
    c.drawRightString(letter[0] - 0.75 * inch, 0.16 * inch, str(doc.page))
    c.restoreState()


out = ROOT / "docs" / "Urban-Duck-Gameplan.pdf"
out.parent.mkdir(exist_ok=True)
doc = SimpleDocTemplate(str(out), pagesize=letter, leftMargin=0.75 * inch, rightMargin=0.75 * inch,
                        topMargin=0.7 * inch, bottomMargin=0.75 * inch, title="Urban Duck Gameplan", author="Leland Doss")
doc.build(story, onFirstPage=frame, onLaterPages=frame)
print(out)

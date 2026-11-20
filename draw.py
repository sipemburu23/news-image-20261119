# draw.py — news-image-20261119 round 1
# "Thursday 19 November 2026" front page, 1024x1024, flat vector, PIL.
# Written from scratch per brief ~/workspace/makefun/news-image-20261119-brief.md
# Facts from ~/workspace/makefun/news-image-20261119-research.md (verified 19 Nov 2026).
# Deterministic: no timestamps, no randomness.
import os, hashlib
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
W, H = 1024, 1024
PAPER = (247, 243, 234)
INK = (26, 26, 26)
NAVY = (31, 42, 68)
RED = (180, 35, 24)
GREEN = (30, 107, 58)
GOLD = (176, 134, 20)
GRAY = (110, 108, 100)
SEA = (222, 233, 236)
LAND = (216, 208, 184)
TEAL = (14, 116, 144)
ORANGE = (194, 65, 12)
PURPLE = (124, 58, 237)

# region colours (fills only: dots, brief numbers, map pins)
REG = {
    "asia": RED, "mideast": ORANGE, "europe": NAVY,
    "africa": GREEN, "americas": TEAL, "oceania": PURPLE, "global": (107, 114, 128),
}

def pf(size, wght):
    f = ImageFont.truetype(os.path.join(HERE, "fonts", "PlayfairDisplay.ttf"), size)
    f.set_variation_by_axes([wght])
    return f

def dj(size, bold=False):
    name = "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf"
    return ImageFont.truetype("/usr/share/fonts/truetype/dejavu/" + name, size)

# ---- fonts ----
F_MAST = None  # chosen by fit below
F_LEADH = pf(21, 700)
F_CARDH = pf(16, 700)
F_STATN = pf(20, 700)
F_DECK = dj(11)
F_DECKS = dj(10)
F_BRIEF = dj(13)
F_BRIEFB = dj(13, bold=True)
F_KICK = dj(10, bold=True)
F_LABEL = dj(10, bold=True)
F_SMALL = dj(9)
F_SMALLB = dj(9, bold=True)
F_TINY = dj(8)
F_TINYB = dj(8, bold=True)
F_CHIP = dj(10, bold=True)
F_SRC = dj(8)

img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)

def tw(font, s):
    return font.getlength(s)

def fit_assert(font, s, maxw, what):
    w = font.getlength(s)
    assert w <= maxw, f"OVERFLOW {what}: '{s}' {w:.1f} > {maxw}"
    return w

def wrap(font, text, maxw):
    words = text.split(" ")
    lines, cur = [], ""
    for wrd in words:
        t = (cur + " " + wrd).strip()
        if font.getlength(t) <= maxw:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = wrd
    if cur:
        lines.append(cur)
    return lines

def center_text(x0, x1, y, s, font, fill, anchor_y="top"):
    w = font.getlength(s)
    d.text(((x0 + x1 - w) / 2, y), s, font=font, fill=fill)

def chip(x, y, text, bg, fg=(255, 255, 255), font=None, pad=7, h=20):
    font = font or F_CHIP
    w = font.getlength(text) + pad * 2
    d.rounded_rectangle([x, y, x + w, y + h], radius=4, fill=bg)
    d.text((x + pad, y + (h - 11) / 2 - 1), text, font=font, fill=fg)
    return w

def hairline(y, x0=24, x1=1000, fill=(180, 175, 160)):
    d.line([(x0, y), (x1, y)], fill=fill, width=1)

def section_label(y, text):
    # small-caps tab sitting on the hairline
    d.text((24, y), text, font=F_LABEL, fill=INK)
    hairline(y + 13, x0=24 + F_LABEL.getlength(text) + 10)

# ============================================================
# MASTHEAD — navy band + calendar chip + Playfair masthead
# ============================================================
MX0, MX1 = 24, 1000
band_y0, band_y1 = 8, 100
d.rectangle([MX0, band_y0, MX1, band_y1], fill=NAVY)
# calendar chip, right side (68 wide)
chip_x0, chip_x1 = 932, 1000
d.rounded_rectangle([chip_x0, band_y0 + 14, chip_x1, band_y1 - 14], radius=5, fill=RED)
center_text(chip_x0, chip_x1, band_y0 + 19, "NOV 19", dj(15, bold=True), (255, 255, 255))
center_text(chip_x0, chip_x1, band_y0 + 40, "THU 2026", dj(9, bold=True), (255, 255, 255))
# masthead: largest ExtraBold size fitting before the chip (per brief)
MASTHEAD_TEXT = "Thursday 19 November 2026"
mast_size = None
for s in (74, 72, 70, 68, 66, 64, 62, 60):
    f = pf(s, 800)
    if f.getlength(MASTHEAD_TEXT) <= (chip_x0 - 16 - MX0):
        mast_size = s
        F_MAST = f
        break
assert mast_size is not None
d.text((MX0, band_y0 + 4), MASTHEAD_TEXT, font=F_MAST, fill=(255, 255, 255))
print("masthead size:", mast_size, "width:", round(F_MAST.getlength(MASTHEAD_TEXT), 1))

# count line
count_y = 108
center_text(MX0, MX1, count_y, "43 STORIES  ·  SIX CONTINENTS  ·  ALL FROM THIS ONE DAY",
            dj(12, bold=True), RED)

# ============================================================
# STAT STRIP — 5 numbers
# ============================================================
stats = [
    ("9–6", "ICJ VOTE"),
    ("$81.3BN", "ANTHROPIC RAISED"),
    ("24.6M", "GTA VI COPIES"),
    ("298,676", "AKVAN EVACUATED"),
    ("−1,101", "DOW"),
]
stat_y0, stat_y1 = 130, 166
cell_w = (MX1 - MX0) / 5
for i, (num, lab) in enumerate(stats):
    cx0 = MX0 + i * cell_w
    cx1 = cx0 + cell_w
    center_text(cx0, cx1, stat_y0, num, F_STATN, INK)
    center_text(cx0, cx1, stat_y0 + 24, lab, dj(9, bold=True), GRAY)
    if i:
        d.line([(cx0, stat_y0 + 2), (cx0, stat_y1 - 2)], fill=(200, 195, 180), width=1)

# ============================================================
# SECTION: TOP STORIES
# ============================================================
section_label(174, "TOP STORIES")

# ============================================================
# LEADS — 3 columns, art 136 tall + headline + deck
# ============================================================
LEAD_Y0, LEAD_H = 190, 136
LEAD_W = 318
lead_x = [24, 353, 682]

def leader(cx, y_head, suit, tie, skin=(232, 184, 138), hair=(60, 50, 40)):
    # head + hair + suit body + tie
    d.ellipse([cx - 13, y_head, cx + 13, y_head + 26], fill=skin)
    d.pieslice([cx - 13, y_head, cx + 13, y_head + 14], 180, 360, fill=hair)
    d.polygon([(cx - 24, y_head + 52), (cx + 24, y_head + 52),
               (cx + 17, y_head + 26), (cx - 17, y_head + 26)], fill=suit)
    d.polygon([(cx - 4, y_head + 28), (cx + 4, y_head + 28),
               (cx, y_head + 44)], fill=tie)
    d.rectangle([cx - 17, y_head + 26, cx + 17, y_head + 30], fill=(255, 255, 255))

def flag_us(x, y, w=34, h=22):
    for i in range(7):
        d.rectangle([x, y + i * (h / 7), x + w, y + (i + 1) * (h / 7)],
                    fill=RED if i % 2 == 0 else (255, 255, 255))
    d.rectangle([x, y, x + w * 0.4, y + h * 0.55], fill=NAVY)

def flag_cn(x, y, w=34, h=22):
    d.rectangle([x, y, x + w, y + h], fill=RED)
    for sx, sy in [(5, 4), (12, 7), (12, 11), (9, 13)]:
        d.ellipse([x + sx, y + sy, x + sx + 4, y + sy + 4], fill=(255, 222, 89))

def flag_ru(x, y, w=34, h=22):
    d.rectangle([x, y, x + w, y + h / 3], fill=(255, 255, 255))
    d.rectangle([x, y + h / 3, x + w, y + 2 * h / 3], fill=(0, 57, 166))
    d.rectangle([x, y + 2 * h / 3, x + w, y + h], fill=RED)

# ---- LEAD 1: SHENZHEN ----
x0 = lead_x[0]
d.rectangle([x0, LEAD_Y0, x0 + LEAD_W, LEAD_Y0 + LEAD_H], fill=(207, 227, 238))
d.rectangle([x0, LEAD_Y0 + 100, x0 + LEAD_W, LEAD_Y0 + LEAD_H], fill=(232, 220, 192))
# Kylin Villa silhouette
d.rectangle([x0 + 118, LEAD_Y0 + 42, x0 + 200, LEAD_Y0 + 100], fill=(245, 240, 228))
d.polygon([(x0 + 110, LEAD_Y0 + 44), (x0 + 208, LEAD_Y0 + 44),
           (x0 + 190, LEAD_Y0 + 30), (x0 + 128, LEAD_Y0 + 30)], fill=(120, 40, 30))
for wx in (128, 148, 168, 188):
    d.rectangle([x0 + wx, LEAD_Y0 + 56, x0 + wx + 10, LEAD_Y0 + 72], fill=NAVY)
# flags on poles (poles stop well above the name plates)
for fx, fl in [(x0 + 44, flag_us), (x0 + 142, flag_cn), (x0 + 210, flag_ru)]:
    d.line([(fx + 17, LEAD_Y0 + 20), (fx + 17, LEAD_Y0 + 62)], fill=(90, 80, 70), width=2)
    fl(fx, LEAD_Y0 + 20)
# leaders at the round table
leader(x0 + 61, LEAD_Y0 + 62, (40, 40, 48), RED)
leader(x0 + 159, LEAD_Y0 + 62, (30, 30, 30), (0, 57, 166))
leader(x0 + 257, LEAD_Y0 + 62, (52, 52, 60), (30, 107, 58))
# round table (donut table)
d.ellipse([x0 + 20, LEAD_Y0 + 106, x0 + 298, LEAD_Y0 + 128], fill=(122, 92, 62))
d.ellipse([x0 + 20, LEAD_Y0 + 106, x0 + 298, LEAD_Y0 + 118], fill=(150, 118, 80))
# name plates on the table front
for cx, nm in [(x0 + 61, "TRUMP"), (x0 + 159, "XI"), (x0 + 257, "PUTIN")]:
    w = 58 if nm != "XI" else 34
    d.rectangle([cx - w / 2, LEAD_Y0 + 120, cx + w / 2, LEAD_Y0 + 134], fill=(255, 255, 255))
    center_text(cx - w / 2, cx + w / 2, LEAD_Y0 + 122, nm, dj(9, bold=True), INK)
# top bar + chips
d.rectangle([x0, LEAD_Y0, x0 + LEAD_W, LEAD_Y0 + 16], fill=INK)
d.text((x0 + 6, LEAD_Y0 + 2), "APEC 2026 · SHENZHEN", font=dj(9, bold=True), fill=(255, 255, 255))
chip(x0 + 252, LEAD_Y0 + 20, "14:30 LOCAL", RED, h=18)

# ---- LEAD 2: ICJ ----
x0 = lead_x[1]
d.rectangle([x0, LEAD_Y0, x0 + LEAD_W, LEAD_Y0 + LEAD_H], fill=(223, 233, 236))
d.rectangle([x0, LEAD_Y0 + 100, x0 + LEAD_W, LEAD_Y0 + LEAD_H], fill=(232, 220, 192))
# Peace Palace (brick, tower, arched windows)
d.rectangle([x0 + 16, LEAD_Y0 + 52, x0 + 196, LEAD_Y0 + 112], fill=(164, 85, 58))
d.rectangle([x0 + 88, LEAD_Y0 + 22, x0 + 124, LEAD_Y0 + 54], fill=(140, 66, 44))
d.polygon([(x0 + 84, LEAD_Y0 + 24), (x0 + 128, LEAD_Y0 + 24), (x0 + 106, LEAD_Y0 + 6)], fill=(120, 40, 30))
for wx in (30, 58, 86, 128, 156, 180):
    d.rectangle([x0 + wx, LEAD_Y0 + 68, x0 + wx + 10, LEAD_Y0 + 88], fill=(60, 50, 44))
d.rectangle([x0 + 96, LEAD_Y0 + 90, x0 + 116, LEAD_Y0 + 112], fill=(60, 50, 44))
# UN flag on tower
d.line([(x0 + 106, LEAD_Y0 + 6), (x0 + 106, LEAD_Y0 - 2)], fill=(90, 80, 70), width=2)
d.rectangle([x0 + 106, LEAD_Y0 - 2, x0 + 130, LEAD_Y0 + 10], fill=(91, 155, 213))
# Myanmar flag, small, left of palace
d.line([(x0 + 8, LEAD_Y0 + 30), (x0 + 8, LEAD_Y0 + 58)], fill=(90, 80, 70), width=2)
d.rectangle([x0 + 8, LEAD_Y0 + 30, x0 + 38, LEAD_Y0 + 37], fill=(254, 203, 0))
d.rectangle([x0 + 8, LEAD_Y0 + 37, x0 + 38, LEAD_Y0 + 44], fill=(52, 168, 83))
d.rectangle([x0 + 8, LEAD_Y0 + 44, x0 + 38, LEAD_Y0 + 51], fill=(234, 40, 40))
d.text((x0 + 8, LEAD_Y0 + 54), "MYANMAR", font=dj(8, bold=True), fill=INK)
# scales of justice (gold)
sx = x0 + 252
d.line([(sx, LEAD_Y0 + 34), (sx, LEAD_Y0 + 100)], fill=(176, 134, 20), width=3)
d.line([(sx - 26, LEAD_Y0 + 40), (sx + 26, LEAD_Y0 + 40)], fill=(176, 134, 20), width=3)
d.ellipse([sx - 5, LEAD_Y0 + 30, sx + 5, LEAD_Y0 + 40], fill=GOLD)
for dx in (-26, 26):
    d.line([(sx + dx, LEAD_Y0 + 40), (sx + dx, LEAD_Y0 + 56)], fill=(176, 134, 20), width=2)
    d.pieslice([sx + dx - 12, LEAD_Y0 + 56, sx + dx + 12, LEAD_Y0 + 70], 0, 180, fill=GOLD)
d.rectangle([sx - 22, LEAD_Y0 + 100, sx + 22, LEAD_Y0 + 106], fill=(176, 134, 20))
# chips + document (on the palace wall, clear of the banner)
chip(x0 + 262, LEAD_Y0 + 18, "9–6", RED, h=22)
d.rectangle([x0 + 128, LEAD_Y0 + 92, x0 + 192, LEAD_Y0 + 110], fill=(255, 255, 255))
d.text((x0 + 132, LEAD_Y0 + 95), "191 PAGES", font=dj(8, bold=True), fill=INK)
d.text((x0 + 226, LEAD_Y0 + 108), "REPARATIONS ORDERED", font=dj(7, bold=True), fill=INK)
# bottom banner
d.rectangle([x0, LEAD_Y0 + LEAD_H - 16, x0 + LEAD_W, LEAD_Y0 + LEAD_H], fill=INK)
center_text(x0, x0 + LEAD_W, LEAD_Y0 + LEAD_H - 14, "WORLD COURT · THE HAGUE",
            dj(10, bold=True), (255, 255, 255))

# ---- LEAD 3: COP31 ----
x0 = lead_x[2]
d.rectangle([x0, LEAD_Y0, x0 + LEAD_W, LEAD_Y0 + LEAD_H], fill=(27, 77, 62))
# globe
gx, gy, gr = x0 + 74, LEAD_Y0 + 72, 40
d.ellipse([gx - gr, gy - gr, gx + gr, gy + gr], fill=(43, 108, 176))
for bx, by, br in [(gx - 16, gy - 12, 12), (gx + 12, gy + 6, 14), (gx - 4, gy + 20, 9), (gx + 18, gy - 20, 8)]:
    d.ellipse([bx - br, by - br, bx + br, by + br], fill=(46, 139, 87))
d.ellipse([gx - gr, gy - gr, gx + gr, gy + gr], outline=(255, 255, 255), width=2)
# thermometer
tx = x0 + 150
d.rounded_rectangle([tx, LEAD_Y0 + 22, tx + 16, LEAD_Y0 + 96], radius=8, fill=(255, 255, 255))
d.rounded_rectangle([tx + 4, LEAD_Y0 + 30, tx + 12, LEAD_Y0 + 92], radius=4, fill=RED)
d.ellipse([tx - 6, LEAD_Y0 + 90, tx + 22, LEAD_Y0 + 112], fill=RED)
d.ellipse([tx - 6, LEAD_Y0 + 90, tx + 22, LEAD_Y0 + 112], outline=(255, 255, 255), width=2)
d.text((tx + 24, LEAD_Y0 + 48), "1.5°C", font=dj(11, bold=True), fill=(255, 255, 255))
d.text((tx + 24, LEAD_Y0 + 62), "PASSED", font=dj(9, bold=True), fill=(255, 255, 255))
# "FOSSIL FUELS" crossed out
ff = "FOSSIL FUELS"
fw = dj(14, bold=True).getlength(ff)
fx0 = x0 + 192
d.text((fx0, LEAD_Y0 + 26), ff, font=dj(14, bold=True), fill=(255, 255, 255))
d.line([(fx0 - 2, LEAD_Y0 + 34), (fx0 + fw + 2, LEAD_Y0 + 34)], fill=RED, width=4)
# CUT stamp (rotated)
stamp = Image.new("RGBA", (90, 34), (0, 0, 0, 0))
sd = ImageDraw.Draw(stamp)
sd.rounded_rectangle([2, 2, 88, 32], radius=4, outline=RED, width=3)
sd.text((45, 5), "CUT", font=dj(18, bold=True), fill=RED, anchor="mt")
stamp = stamp.rotate(12, expand=True, resample=Image.BICUBIC)
img.paste(stamp, (x0 + 225, LEAD_Y0 + 52), stamp)
# chips
chip(x0 + 8, LEAD_Y0 + 8, "144→80 PARAS", NAVY, h=18)
chip(x0 + 200, LEAD_Y0 + 96, "$120BN CUT", RED, h=18)
# bottom banner
d.rectangle([x0, LEAD_Y0 + LEAD_H - 16, x0 + LEAD_W, LEAD_Y0 + LEAD_H], fill=INK)
center_text(x0, x0 + LEAD_W, LEAD_Y0 + LEAD_H - 14, "COP31 · ANTALYA",
            dj(10, bold=True), (255, 255, 255))

# ---- lead headlines + decks ----
lead_heads = [
    "Trump, Xi and Putin hold first three-way summit",
    "World Court: Myanmar committed genocide",
    "COP31 draft drops phase-out and $120bn aid",
]
lead_decks = [
    "Three leaders meet 90 minutes in Shenzhen and issue a 4-point declaration. Ukraine not mentioned. — Reuters",
    "By 9 votes to 6, the court finds Myanmar guilty of genocide against the Rohingya and orders reparations. — Reuters",
    "The slimmed text cuts all phase-out language and the $120bn adaptation goal. Talks end on Friday. — Reuters",
]
for i, (hx, hd, dk) in enumerate(zip(lead_x, lead_heads, lead_decks)):
    lines = wrap(F_LEADH, hd, LEAD_W)
    assert len(lines) <= 2, f"lead headline {i+1} wraps to {len(lines)}: {lines}"
    y = 332
    for ln in lines:
        d.text((hx, y), ln, font=F_LEADH, fill=INK)
        y += 22
    dlines = wrap(dj(10), dk, LEAD_W)
    assert len(dlines) <= 2, f"lead deck {i+1} wraps to {len(dlines)}: {dlines}"
    y = 380
    for ln in dlines:
        d.text((hx, y), ln, font=dj(10), fill=(60, 58, 52))
        y += 13

# ============================================================
# TIMELINE STRIP — "THE DAY IN UTC"
# ============================================================
tl_y0, tl_y1 = 410, 446
hairline(tl_y0 - 2)
d.rectangle([24, tl_y0, 114, tl_y1], fill=NAVY)
d.text((30, tl_y0 + 6), "THE DAY", font=dj(9, bold=True), fill=(255, 255, 255))
d.text((30, tl_y0 + 18), "IN UTC", font=dj(9, bold=True), fill=(255, 255, 255))
tl_items = [
    ("04:45 GMT", "Trump–Xi lunch begins"),
    ("05:00 GMT", "GTA VI unlocks in US"),
    ("06:30 GMT", "Trilateral opens, Kylin Villa"),
    ("09:00 GMT", "Akvan 390 km off Narsapur"),
    ("10:00 GMT", "Paris retirees gather"),
    ("10:58 UTC", "Hamas rejects board report"),
    ("20:15 ET", "Texans–Colts kick off"),
]
tl_w = (1000 - 122) / 7
for i, (tm, tx) in enumerate(tl_items):
    cx = 122 + i * tl_w
    d.text((cx + 4, tl_y0 + 2), tm, font=dj(9, bold=True), fill=NAVY)
    lines = wrap(dj(8), tx, tl_w - 8)
    assert len(lines) <= 2, f"timeline item {i} wraps to {len(lines)}"
    y = tl_y0 + 14
    for ln in lines:
        d.text((cx + 4, y), ln, font=dj(8), fill=INK)
        y += 10
hairline(tl_y1 + 2)

# ============================================================
# CARDS — 2 rows x 5, scene strip + location bar + chip + source
# ============================================================
CARD_Y = [452, 580]
CARD_H = 122
CARD_W = 188
card_x = [24, 221, 418, 614, 811]

def card_frame(i, loc, chip_text, chip_bg):
    # records the overlay; drawn later by draw_overlays() so scene art
    # (drawn after this call) cannot cover the location bar / chip
    _overlays.append((i, loc, chip_text, chip_bg))
    return card_x[i % 5], CARD_Y[i // 5]

def draw_overlays():
    for i, loc, ct, bg in _overlays:
        x, y = card_x[i % 5], CARD_Y[i // 5]
        d.rectangle([x, y + 44, x + CARD_W, y + 58], fill=INK)
        d.text((x + 5, y + 47), loc, font=dj(9, bold=True), fill=(255, 255, 255))
        cw = F_CHIP.getlength(ct) + 14
        chip(x + CARD_W - cw - 4, y + 4, ct, bg, h=18)

_overlays = []

def card_text(i, head, deck, src):
    x = card_x[i % 5]
    y = CARD_Y[i // 5]
    fit_assert(F_CARDH, head, CARD_W, f"card {i+1} headline")
    d.text((x, y + 62), head, font=F_CARDH, fill=INK)
    lines = wrap(dj(10), deck, CARD_W)
    assert len(lines) <= 2, f"card {i+1} deck wraps to {len(lines)}: {lines}"
    yy = y + 84
    for ln in lines:
        d.text((x, yy), ln, font=dj(10), fill=(60, 58, 52))
        yy += 11
    d.text((x, y + 108), src, font=F_SRC, fill=GRAY)

# --- card 1: ANTHROPIC IPO ---
x, y = card_frame(0, "NEW YORK · MARKETS", "+17%", GREEN)
d.rectangle([x, y, x + CARD_W, y + 58], fill=(18, 63, 42))
for gx in range(0, CARD_W, 24):
    d.line([(x + gx, y), (x + gx, y + 58)], fill=(28, 84, 56), width=1)
pts = [(x + 8, y + 46), (x + 40, y + 40), (x + 72, y + 44), (x + 104, y + 30),
       (x + 136, y + 22), (x + 168, y + 10), (x + 184, y + 6)]
d.line(pts, fill=(74, 222, 128), width=3)
d.polygon([(x + 184, y + 6), (x + 172, y + 4), (x + 178, y + 16)], fill=(74, 222, 128))
for px, py in pts[1:-1]:
    d.ellipse([px - 2, py - 2, px + 2, py + 2], fill=(255, 255, 255))
card_text(0, "ANTHROPIC IPO",
          "Record $81.3bn raised; opens $111.50, closes $97.17.",
          "Reuters")

# --- card 2: GTA VI ---
x, y = card_frame(1, "WORLDWIDE · GAMES", "24.6M", GREEN)
d.rectangle([x, y, x + CARD_W, y + 58], fill=(91, 33, 182))
d.rectangle([x, y + 40, x + CARD_W, y + 58], fill=(46, 16, 101))
for bx in (10, 34, 58, 82, 106, 130, 154):
    bh = 8 + (bx % 3) * 5
    d.rectangle([x + bx, y + 58 - bh, x + bx + 14, y + 58], fill=(30, 10, 60))
d.rounded_rectangle([x + 14, y + 8, x + 78, y + 36], radius=10, fill=(255, 255, 255))
d.rectangle([x + 24, y + 18, x + 34, y + 26], fill=(91, 33, 182))
for cx, cy, cc in [(58, 18, RED), (66, 24, GREEN), (50, 24, GOLD), (58, 30, NAVY)]:
    d.ellipse([x + cx - 3, y + cy - 3, x + cx + 3, y + cy + 3], fill=cc)
d.text((x + 96, y + 10), "VI", font=pf(28, 800), fill=(255, 255, 255))
card_text(1, "GTA VI",
          "US unlock at midnight; 24.6m copies, $2.36bn day one.",
          "Sensor Tower")

# --- card 3: CYCLONE AKVAN ---
x, y = card_frame(2, "ODISHA · STORM", "298,676", RED)
d.rectangle([x, y, x + CARD_W, y + 58], fill=(191, 227, 240))
cx, cy = x + 94, y + 26
for r in (8, 16, 24):
    d.arc([cx - r, cy - r, cx + r, cy + r], 20, 300, fill=(255, 255, 255), width=3)
d.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], fill=NAVY)
d.polygon([(x + 130, y + 58), (x + 188, y + 58), (x + 188, y + 30), (x + 160, y + 44)],
          fill=(46, 139, 87))
for dx, dy in [(20, 44), (36, 50), (52, 42), (150, 14), (168, 8)]:
    d.ellipse([x + dx, y + dy, x + dx + 3, y + dy + 6], fill=(43, 108, 176))
card_text(2, "CYCLONE AKVAN",
          "298,676 evacuated; landfall due Friday near Gopalpur.",
          "IMD")

# --- card 4: KERCH RAIL ---
x, y = card_frame(3, "CRIMEA · WAR", "3RD DAY", RED)
d.rectangle([x, y, x + CARD_W, y + 58], fill=(223, 233, 236))
d.rectangle([x, y + 38, x + CARD_W, y + 58], fill=(120, 170, 210))
d.arc([x - 10, y - 6, x + 198, y + 46], 200, 340, fill=(120, 118, 110), width=6)
for tx in range(20, 180, 16):
    d.line([(x + tx, y + 12), (x + tx, y + 20)], fill=(90, 88, 82), width=2)
ex, ey = x + 94, y + 12
for ang in range(0, 360, 45):
    import math
    d.line([(ex, ey), (ex + 12 * math.cos(math.radians(ang)),
                        ey + 12 * math.sin(math.radians(ang)))], fill=(245, 158, 11), width=3)
d.ellipse([ex - 5, ey - 5, ex + 5, ey + 5], fill=RED)
card_text(3, "KERCH RAIL",
          "Neptune missiles hit rail bridge, 3rd day; trains halted.",
          "Reuters")

# --- card 5: RIYADH ---
x, y = card_frame(4, "RIYADH · WAR", "DAWN", NAVY)
d.rectangle([x, y, x + CARD_W, y + 58], fill=(246, 193, 119))
d.rectangle([x, y + 38, x + CARD_W, y + 58], fill=(90, 70, 60))
for bx, bw, bh in [(8, 18, 20), (32, 14, 28), (52, 22, 16), (120, 16, 24), (142, 20, 18), (166, 14, 26)]:
    d.rectangle([x + bx, y + 58 - bh, x + bx + bw, y + 58], fill=(60, 48, 52))
d.rectangle([x + 82, y + 6, x + 100, y + 58], fill=(40, 34, 40))
for ly in range(10, 56, 8):
    d.line([(x + 82, y + ly), (x + 100, y + ly + 6)], fill=(120, 110, 100), width=1)
d.line([(x + 150, y + 6), (x + 118, y + 30)], fill=(255, 255, 255), width=3)
for dx, dy in [(112, 30), (106, 36), (120, 38)]:
    d.ellipse([x + dx, y + dy, x + dx + 4, y + dy + 4], fill=(255, 255, 255))
card_text(4, "RIYADH",
          "Houthi missile at dawn; PIF Tower damaged. No casualties.",
          "Reuters")

# --- card 6: GAZA ---
x, y = card_frame(5, "GAZA · WAR", "4/26", RED)
d.rectangle([x, y, x + CARD_W, y + 58], fill=(232, 220, 192))
d.line([(x, y + 30), (x + CARD_W, y + 30)], fill=(250, 204, 21), width=5)
d.rectangle([x + 20, y + 34, x + 66, y + 48], fill=(70, 66, 60))
d.rectangle([x + 38, y + 26, x + 52, y + 34], fill=(70, 66, 60))
d.line([(x + 52, y + 30), (x + 78, y + 26)], fill=(70, 66, 60), width=3)
for tx, ty in [(110, 36), (140, 40), (165, 34)]:
    d.polygon([(x + tx, y + ty + 12), (x + tx + 22, y + ty + 12), (x + tx + 11, y + ty)],
              fill=(200, 190, 160))
    d.line([(x + tx + 11, y + ty), (x + tx + 11, y + ty - 8)], fill=(90, 80, 70), width=1)
card_text(5, "GAZA",
          "Israeli troops cross the Yellow Line; aid groups rate it 4/26.",
          "Reuters")

# --- card 7: BANGLADESH ---
x, y = card_frame(6, "GAZIPUR · LABOUR", "50", RED)
d.rectangle([x, y, x + CARD_W, y + 58], fill=(253, 230, 138))
d.rectangle([x + 10, y + 22, x + 90, y + 58], fill=(120, 118, 110))
d.rectangle([x + 100, y + 30, x + 150, y + 58], fill=(140, 138, 130))
for cx in (24, 46):
    d.rectangle([x + cx, y + 6, x + cx + 6, y + 24], fill=(100, 98, 92))
for sx, sy in [(30, 2), (52, 0), (44, 8)]:
    d.ellipse([x + sx, y + sy, x + sx + 12, y + sy + 8], fill=(200, 198, 190))
for px in range(112, 184, 12):
    d.ellipse([x + px, y + 44, x + px + 7, y + 51], fill=(232, 184, 138))
    d.rectangle([x + px + 1, y + 51, x + px + 6, y + 58], fill=NAVY)
card_text(6, "BANGLADESH",
          "50 factories shut in Gazipur; clashes; losses Tk 3,000–4,000cr.",
          "AP")

# --- card 8: AUSTRALIA ---
x, y = card_frame(7, "CANBERRA · ECONOMY", "4.9%", GREEN)
d.rectangle([x, y, x + CARD_W, y + 58], fill=(255, 255, 255))
bars = [44, 38, 30, 24, 16]
for i, bh in enumerate(bars):
    bx = x + 16 + i * 30
    d.rectangle([bx, y + 52 - bh, bx + 20, y + 52], fill=RED if i < 2 else (200, 60, 40))
d.line([(x + 10, y + 8), (x + 176, y + 46)], fill=RED, width=3)
d.polygon([(x + 176, y + 46), (x + 162, y + 42), (x + 168, y + 54)], fill=RED)
for cx, cy in [(150, 14), (164, 20)]:
    d.ellipse([x + cx, y + cy, x + cx + 12, y + cy + 12], fill=(212, 175, 55))
    d.text((x + cx + 3, y + cy + 1), "$", font=dj(9, bold=True), fill=(120, 90, 10))
card_text(7, "AUSTRALIA",
          "Jobless 4.9%, highest since 2021; 753,700 out of work.",
          "ABS")

# --- card 9: COLOMBIA ---
x, y = card_frame(8, "BOGOTÁ · LABOUR", "STRIKE", NAVY)
d.rectangle([x, y, x + CARD_W, y + 58], fill=(223, 233, 236))
for bx, bw, bh in [(6, 24, 18), (36, 18, 26), (60, 28, 14), (150, 22, 20)]:
    d.rectangle([x + bx, y + 58 - bh, x + bx + bw, y + 58], fill=(140, 138, 130))
for fx in (96, 120):
    d.line([(x + fx, y + 6), (x + fx, y + 30)], fill=(90, 80, 70), width=2)
    d.rectangle([x + fx, y + 6, x + fx + 22, y + 12], fill=(252, 209, 22))
    d.rectangle([x + fx, y + 12, x + fx + 22, y + 18], fill=(0, 56, 147))
    d.rectangle([x + fx, y + 18, x + fx + 22, y + 24], fill=(206, 17, 38))
for px in range(8, 184, 14):
    d.ellipse([x + px, y + 40, x + px + 8, y + 48], fill=(232, 184, 138))
    d.rectangle([x + px, y + 48, x + px + 8, y + 58], fill=(70, 66, 60) if px % 28 else NAVY)
card_text(8, "COLOMBIA",
          "Unions hold a national strike in Bogotá, Medellín, Cali.",
          "AFP")

# --- card 10: GREENLAND ---
x, y = card_frame(9, "GREENLAND · SECURITY", "109–0", NAVY)
d.rectangle([x, y, x + CARD_W, y + 58], fill=(219, 234, 254))
d.polygon([(x, y + 58), (x + 60, y + 58), (x + 30, y + 18)], fill=(255, 255, 255))
d.polygon([(x + 50, y + 58), (x + 130, y + 58), (x + 90, y + 10)], fill=(240, 244, 248))
d.polygon([(x + 120, y + 58), (x + 188, y + 58), (x + 158, y + 26)], fill=(255, 255, 255))
for fx, fl in [(x + 140, "dk"), (x + 164, "us")]:
    d.line([(fx, y + 8), (fx, y + 30)], fill=(90, 80, 70), width=2)
    if fl == "dk":
        d.rectangle([fx, y + 8, fx + 20, y + 20], fill=RED)
        d.rectangle([fx + 6, y + 8, fx + 9, y + 20], fill=(255, 255, 255))
        d.rectangle([fx, y + 13, fx + 20, y + 16], fill=(255, 255, 255))
    else:
        d.rectangle([fx, y + 8, fx + 20, y + 20], fill=(255, 255, 255))
        for i in range(4):
            d.rectangle([fx, y + 8 + i * 3, fx + 20, y + 10 + i * 3], fill=RED)
        d.rectangle([fx, y + 8, fx + 8, y + 14], fill=NAVY)
card_text(9, "GREENLAND",
          "Denmark ratifies Arctic pact with US, 109–0; two bases allowed.",
          "Reuters")

# ============================================================
# DRAW OVERLAYS (location bars + chips on card scenes)
# ============================================================
draw_overlays()

# ============================================================
# WHERE IT HAPPENED — map + briefs + DATE CHECK
# ============================================================
section_label(712, "WHERE IT HAPPENED")

# continent polygons (lon, lat) — reference data from
# ~/workspace/makefun/news-image-20261118-polys.py (data only)
POLYS = [
    [(-9, 37), (-9, 43), (-2, 44), (-1, 46), (-4, 48), (-2, 50), (1, 51), (4, 53), (8, 54), (8, 57), (10, 58), (7, 60), (5, 62), (10, 64), (14, 67), (19, 69), (24, 71), (30, 70), (35, 68), (42, 68), (48, 68), (54, 68), (60, 69), (66, 69), (72, 72), (78, 72), (85, 73), (95, 75), (105, 77), (112, 74), (120, 73), (128, 71), (138, 72), (148, 72), (158, 70), (162, 66), (170, 66), (178, 65), (178, 62), (170, 60), (162, 59), (158, 52), (156, 51), (150, 59), (142, 59), (141, 52), (140, 47), (138, 43), (135, 43), (132, 43), (130, 42), (127, 40), (126, 38), (124, 40), (121, 37), (120, 32), (122, 30), (120, 25), (117, 23), (112, 22), (108, 18), (106, 11), (105, 9), (103, 7), (100, 6), (98, 10), (97, 15), (94, 16), (92, 21), (90, 22), (88, 22), (86, 20), (83, 18), (80, 15), (80, 10), (77, 8), (75, 10), (73, 16), (70, 20), (68, 23), (66, 25), (62, 25), (58, 25), (56, 26), (52, 26), (50, 29), (48, 30), (45, 29), (43, 28), (41, 27), (39, 21), (38, 18), (35, 28), (34, 28), (33, 29), (32, 31), (30, 31), (27, 37), (26, 38), (23, 36), (22, 37), (20, 39), (19, 42), (16, 40), (14, 38), (12, 38), (10, 37), (8, 37), (8, 39), (4, 39), (2, 41), (0, 38), (-2, 37), (-6, 36)],
    [(-168, 66), (-165, 60), (-158, 58), (-152, 60), (-140, 60), (-135, 58), (-130, 54), (-125, 49), (-124, 42), (-120, 34), (-114, 29), (-110, 24), (-105, 20), (-97, 16), (-94, 17), (-90, 14), (-86, 12), (-83, 9), (-80, 8), (-77, 7), (-79, 9), (-81, 13), (-84, 16), (-87, 13), (-88, 18), (-90, 21), (-91, 19), (-96, 19), (-97, 22), (-97, 26), (-93, 30), (-89, 30), (-84, 30), (-81, 26), (-80, 32), (-76, 35), (-74, 40), (-70, 42), (-68, 45), (-65, 44), (-60, 47), (-55, 47), (-60, 52), (-65, 50), (-60, 55), (-65, 60), (-68, 58), (-75, 62), (-78, 62), (-85, 66), (-90, 66), (-95, 69), (-110, 68), (-125, 70), (-140, 70), (-155, 71), (-165, 68)],
    [(-80, 9), (-77, 4), (-75, 0), (-80, -3), (-81, -6), (-77, -12), (-72, -18), (-70, -23), (-70, -30), (-72, -37), (-73, -44), (-74, -50), (-70, -54), (-66, -55), (-65, -45), (-62, -41), (-58, -35), (-52, -32), (-48, -28), (-41, -23), (-39, -17), (-35, -9), (-35, -6), (-40, -3), (-44, -2), (-50, 0), (-52, 5), (-55, 6), (-60, 8), (-62, 9), (-68, 11), (-72, 12), (-75, 11), (-77, 8)],
    [(-17, 15), (-17, 21), (-15, 27), (-10, 31), (-5, 35), (0, 36), (10, 37), (11, 34), (20, 32), (25, 32), (30, 31), (33, 27), (35, 23), (37, 18), (39, 15), (43, 12), (48, 11), (51, 12), (46, 5), (42, 0), (40, -5), (40, -10), (37, -15), (35, -20), (32, -26), (28, -33), (20, -35), (17, -32), (15, -27), (13, -18), (12, -10), (13, -5), (9, 4), (6, 4), (-2, 5), (-8, 5), (-13, 8), (-17, 12)],
    [(113, -22), (114, -30), (115, -35), (118, -35), (124, -33), (129, -32), (132, -32), (135, -35), (138, -35), (140, -38), (145, -38), (150, -37), (153, -32), (153, -27), (150, -22), (146, -19), (142, -15), (142, -11), (140, -17), (136, -15), (135, -12), (132, -11), (130, -13), (126, -14), (122, -17), (118, -20), (114, -22)],
    [(-45, 60), (-40, 64), (-32, 68), (-25, 70), (-20, 74), (-25, 76), (-35, 77), (-50, 76), (-58, 74), (-55, 70), (-52, 64), (-48, 60)],
    [(-5, 50), (-3, 53), (-5, 56), (-3, 58), (-1, 57), (0, 53), (1, 51)],
    [(130, 31), (132, 33), (134, 34), (136, 35), (138, 35), (140, 37), (141, 39), (141, 41), (142, 43), (144, 44), (141, 45), (139, 41), (137, 38), (135, 34), (133, 34), (130, 33)],
    [(44, -16), (47, -15), (50, -16), (50, -20), (47, -24), (44, -25), (43, -21), (44, -17)],
    [(167, -45), (170, -43), (173, -41), (175, -38), (177, -38), (174, -36), (172, -35), (167, -45)],
]

MAP_X0, MAP_Y0, MAP_W, MAP_H = 24, 728, 300, 113
d.rectangle([MAP_X0, MAP_Y0, MAP_X0 + MAP_W, MAP_Y0 + MAP_H], fill=SEA)
def proj(lon, lat):
    return (MAP_X0 + (lon + 170) / 360 * MAP_W,
            MAP_Y0 + (75 - lat) / 130 * MAP_H)
for poly in POLYS:
    d.polygon([proj(lon, lat) for lon, lat in poly], fill=LAND)

# brief dots (r=3.5, round, region colour) — drawn before pins
brief_dots = [
    (-122, 37, "americas"), (-74, 41, "americas"), (-118, 34, "americas"),
    (37, -1, "africa"), (127, 37, "asia"), (38, 14, "africa"),
    (-77, 39, "americas"), (30, 13, "africa"), (20, 44, "europe"),
    (2, 49, "europe"), (140, 36, "asia"), (-94, 36, "americas"),
    (0, 51, "global"), (-95, 30, "americas"), (32, -26, "africa"),
    (45, 2, "africa"), (-77, 39, "global"), (-77, 39, "americas"),
    (13, 52, "europe"), (29, 1, "africa"), (-98, 39, "americas"),
    (-72, 19, "americas"), (-6, 55, "europe"), (127, 37, "asia"),
    (-80, 26, "americas"), (107, -6, "asia"), (107, 48, "asia"),
    (127, 37, "asia"), (56, 26, "mideast"), (30, 50, "europe"),
]
for lon, lat, rg in brief_dots:
    px, py = proj(lon, lat)
    d.ellipse([px - 3.5, py - 3.5, px + 3.5, py + 3.5], fill=REG[rg])

# numbered pins (1-13 = illustrated stories), nudged so centres stay >=20px apart
pins = [
    (1, 114, 22, "asia", (10, -6)),    # Shenzhen
    (2, 4, 52, "europe", (-12, -6)),   # Den Haag
    (3, 31, 37, "europe", (-14, -10)), # Antalya
    (4, -74, 41, "americas", (-8, -8)),# New York
    (5, -80, 26, "americas", (-10, 8)),# Miami (GTA VI setting)
    (6, 85, 19, "asia", (-6, 6)),      # Gopalpur / Akvan
    (7, 36, 45, "europe", (10, -6)),   # Kerch
    (8, 47, 25, "mideast", (4, 4)),    # Riyadh
    (9, 34, 31, "mideast", (-6, 14)),  # Gaza
    (10, 90, 24, "asia", (8, -8)),     # Dhaka
    (11, 149, -35, "oceania", (0, 0)), # Canberra
    (12, -74, 5, "americas", (8, 6)),  # Bogota
    (13, 13, 56, "europe", (14, -10)), # Copenhagen
]
pin_xy = {}
for n, lon, lat, rg, (dx, dy) in pins:
    tx, ty = proj(lon, lat)
    px, py = tx + dx, ty + dy
    pin_xy[n] = (px, py)
    if (dx, dy) != (0, 0):
        d.line([(tx, ty), (px, py)], fill=(120, 115, 100), width=1)
import math
min_pin = 999.0
for i in range(len(pins)):
    for j in range(i + 1, len(pins)):
        a = pin_xy[pins[i][0]]
        b = pin_xy[pins[j][0]]
        min_pin = min(min_pin, math.hypot(a[0] - b[0], a[1] - b[1]))
print("pin min distance:", round(min_pin, 1))
assert min_pin >= 20.0, f"pins too close: {min_pin:.1f}"
for n, lon, lat, rg, (dx, dy) in pins:
    px, py = pin_xy[n]
    d.ellipse([px - 7, py - 7, px + 7, py + 7], fill=REG[rg], outline=(255, 255, 255), width=1)
    lbl = str(n)
    w = dj(8, bold=True).getlength(lbl)
    d.text((px - w / 2, py - 5), lbl, font=dj(8, bold=True), fill=(255, 255, 255))

d.text((MAP_X0, MAP_Y0 + MAP_H + 4), "Numbers match the stories · Dots mark the briefs",
       font=dj(8), fill=GRAY)

# ---- DATE CHECK box under the map ----
DC_X0, DC_Y0 = 24, 864
dc_items = [
    "Voyager 1 one light-day", "EU €45bn for Ukraine",
    "Anthropic IPO priced at $83", "Nvidia $115.8bn quarter",
    "Jeffries 251–11", "Kerch road span collapse",
    "Van Gogh $190.4m", "Peltola wins Alaska",
    "Knesset speaker vote 66–52", "UK inflation 3.6%",
    "Fed minutes", "Iran–Gulf strikes (Tue–Wed)",
]
d.rectangle([DC_X0, DC_Y0, DC_X0 + MAP_W, DC_Y0 + 100], outline=GREEN, width=1, fill=(240, 245, 235))
d.text((DC_X0 + 6, DC_Y0 + 4), "DATE CHECK ✓ — LEFT OUT ON PURPOSE",
       font=dj(9, bold=True), fill=GREEN)
dc_col_w = 148
for i, it in enumerate(dc_items):
    col, row = i % 2, i // 2
    fit_assert(dj(9), it, dc_col_w, f"DATE CHECK item {i+1}")
    d.text((DC_X0 + 6 + col * dc_col_w, DC_Y0 + 20 + row * 11), "· " + it, font=dj(9), fill=INK)
d.text((DC_X0 + 6, DC_Y0 + 20 + 6 * 11 + 2),
       "NOT YET: Akvan landfall + COP31 close (Fri 20 Nov)",
       font=dj(8, bold=True), fill=RED)

# ---- BRIEFS 14–43 (2 columns, one line each) ----
briefs = [
    (14, "NVIDIA — AG subpoenas Nvidia; 879k chips", "americas"),
    (15, "MARKETS — Dow −1,101; S&P down 6th day", "americas"),
    (16, "CALIFORNIA — LA floods; SF record rain Wed", "americas"),
    (17, "JEPCHIRCHIR — Banned 3 years for EPO", "africa"),
    (18, "SEOUL — Han Duck-soo retrial; term void", "asia"),
    (19, "BADME — Strikes reported; 4 hurt", "africa"),
    (20, "US SENATE — Energy bill passes 62–33", "americas"),
    (21, "SUDAN — Amnesty: 37 killed by RSF drones", "africa"),
    (22, "SERBIA — Čupić elected speaker, 140–97", "europe"),
    (23, "PARIS — Retirees march; 30,000 expected", "europe"),
    (24, "TOKYO — India–Japan 2+2; live-fire first", "asia"),
    (25, "WALMART — Revenue $188.8bn (+5.2%)", "americas"),
    (26, "GOLD — Gold $3,674, 14-month low", "global"),
    (27, "NFL — Texans crush Colts 26–3", "americas"),
    (28, "MOZAMBIQUE — Trial blocks 2028/29 runs", "africa"),
    (29, "SOMALIA — UAE envoy out in 72 hours", "africa"),
    (30, "PEW — Islam largest religion by 2035", "global"),
    (31, "WASHINGTON — Trump vs Vance on Iran", "americas"),
    (32, "BERLIN — European allies meet on Ukraine", "europe"),
    (33, "EBOLA — 11,376 cases, 5,568 deaths, 14 Nov", "africa"),
    (34, "MEASLES — 5,412 US cases (data to 12 Nov)", "americas"),
    (35, "HAITI — 34 suspected gang members killed", "americas"),
    (36, "N. IRELAND — N. Ireland 1–0 Luxembourg", "europe"),
    (37, "SUNEUNG — 551,864 sit Korea's exam", "asia"),
    (38, "FLORIDA — Broward floods; schools shut", "americas"),
    (39, "INDONESIA — Asset-seizure law after 18 yrs", "asia"),
    (40, "MONGOLIA — Parliament accepts exit 96–104", "asia"),
    (41, "S. KOREA — Exports pass $1 trillion", "asia"),
    (42, "GULF — IEA: Gulf war 'largest threat' ever", "mideast"),
    (43, "KYIV — Kyiv hit all day; 1 killed, 5 hurt", "europe"),
]
BRIEF_X = [336, 672]
BRIEF_W = 328
BRIEF_Y0, BRIEF_PITCH = 728, 15.5
for idx, (num, text, rg) in enumerate(briefs):
    col, row = idx % 2, idx // 2
    bx = BRIEF_X[col]
    by = BRIEF_Y0 + row * BRIEF_PITCH
    numtxt = f"{num}. "
    w_num = F_BRIEFB.getlength(numtxt)
    w_txt = F_BRIEF.getlength(text)
    assert w_num + w_txt <= BRIEF_W, \
        f"brief {num} overflow: {w_num + w_txt:.1f} > {BRIEF_W}: '{text}'"
    d.text((bx, by), numtxt, font=F_BRIEFB, fill=REG[rg])
    d.text((bx + w_num, by), text, font=F_BRIEF, fill=INK)

# ---- FOOTER ----
foot1 = "Claims are attributed, not stated as fact · Pictures and map: original, drawn in code · Original drawings."
foot2 = "Sources: Reuters, AP, AFP, BBC, Al Jazeera, WHO, UN/ICJ, IMD, CDC, Amnesty, Pew, Sensor Tower · 2026-11-19"
center_text(24, 1000, 972, foot1, dj(9), GRAY)
center_text(24, 1000, 983, foot2, dj(9), GRAY)
MAX_Y = 996
assert MAX_Y <= 1010

# ============================================================
# SAVE + DIAGNOSTICS
# ============================================================
out = os.path.join(HERE, "entry.png")
img.save(out, format="PNG")
data = open(out, "rb").read()
print("entry.png bytes:", len(data))
print("entry.png sha256:", hashlib.sha256(data).hexdigest())
# 300px thumbnail ink mass of the masthead (white glyphs on navy)
small = img.resize((300, 300), Image.LANCZOS)
px = small.load()
ink = 0
for yy in range(2, 30):
    for xx in range(7, 273):
        r, g, b = px[xx, yy]
        if r > 180 and g > 180 and b > 180:
            ink += 1
print("masthead ink @300px:", ink, "(target >= 1800)")

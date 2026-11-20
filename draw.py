#!/usr/bin/env python3
"""news-image-20261119 round 4 — draw.py (build-time authoring tool).
Draws ONE newspaper front page (1024x1024 PNG) summing up Thursday 19 Nov 2026.
Deterministic: no timestamps, no unseeded randomness.
main.ts (copy-only) ships entry.png; draw.py never runs in the grader.
"""
import math
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")

# ---------------- palette ----------------
PAPER = (247, 243, 234)
INK = (26, 26, 26)
NAVY = (31, 42, 68)
NAVY_LT = (43, 58, 92)
RED = (180, 35, 24)
RED_DK = (140, 25, 16)
GREEN = (30, 107, 58)
TEAL = (31, 138, 138)
ORANGE = (217, 123, 41)
PURPLE = (123, 75, 168)
BLUE = (43, 94, 167)
AFRICA = (46, 125, 79)
GREY = (102, 102, 102)
SEA = (214, 228, 236)
LAND = (232, 220, 192)
LAND_LINE = (190, 175, 140)
HAIR = (200, 192, 172)
WHITE = (255, 255, 255)
CREAM_DK = (238, 231, 214)

REGION = {
    "EUROPE": BLUE, "MIDDLE EAST": ORANGE, "ASIA": PURPLE,
    "AFRICA": AFRICA, "AMERICAS": RED, "OCEANIA": TEAL, "GLOBAL": GREY,
}
TAG_COLOR = {"CONFIRMED": GREEN, "REPORTED": NAVY, "CLAIM": RED, "FORECAST": ORANGE}

# ---------------- fonts ----------------
BASE = os.path.dirname(os.path.abspath(__file__))
PF = os.path.join(BASE, "fonts", "PlayfairDisplay.ttf")
DJ = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
DJB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
DJS = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
DJSB = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"


def _pf(size, name=b"ExtraBold"):
    f = ImageFont.truetype(PF, size)
    try:
        f.set_variation_by_name(name)
    except Exception:
        pass
    return f


def _dj(size, bold=False):
    return ImageFont.truetype(DJB if bold else DJ, size)


F_MAST = _pf(64, b"ExtraBold")
F_LEAD_H = _pf(21, b"Bold")
F_CARD_H = _pf(16, b"Bold")
F_KICK = _dj(11, True)
F_DECK = _dj(12)
F_BRIEF = _dj(13)
F_BRIEF_B = _dj(13, True)
F_NUM = _dj(13, True)
F_SMALL = _dj(10)
F_SMALL_B = _dj(10, True)
F_TINY = _dj(9)
F_TINY_B = _dj(9, True)
F_TL = _dj(8)
F_TL_TIME = _dj(15, True)
F_STAT_N = _dj(16, True)
F_STAT_L = _dj(9, True)
F_LABEL = _dj(11, True)
F_CHIP = _dj(11, True)
F_BANNER = _dj(10, True)
F_LOC = _dj(9, True)
F_SRC = _dj(9)
F_FOOT = _dj(8)

# ---------------- geometry ----------------
MX = 24
CW = 976
RIGHT = 1000

# ---------------- continent polygons (lon, lat) — reference data ----------------
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

# ---------------- text helpers ----------------
def tw(font, s):
    return font.getlength(s)


def fit_lines(text, font, max_w, max_lines):
    """Greedy wrap; returns list of lines (<= max_lines). Asserts no overflow."""
    words = text.split()
    lines, cur = [], ""
    for wd in words:
        trial = (cur + " " + wd).strip()
        if tw(font, trial) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = wd
    if cur:
        lines.append(cur)
    assert len(lines) <= max_lines, f"WRAP OVERFLOW ({len(lines)}>{max_lines}): {text!r}"
    for ln in lines:
        assert tw(font, ln) <= max_w, f"LINE TOO WIDE: {ln!r}"
    return lines


def draw_lines(d, lines, x, y, font, fill, leading):
    for ln in lines:
        d.text((x, y), ln, font=font, fill=fill)
        y += leading
    return y


def chip(d, x, y, text, fill, font=F_CHIP, fg=WHITE, pad_x=7, h=18):
    w = int(tw(font, text)) + pad_x * 2
    d.rounded_rectangle([x, y, x + w, y + h], radius=4, fill=fill)
    d.text((x + pad_x, y + 3), text, font=font, fill=fg)
    return w


def label_in_box(d, text, box_x, box_y, box_w, font, fill, bg=None):
    """One-line label; assert it fits the box."""
    assert tw(font, text) <= box_w, f"LABEL OVERFLOW {text!r} {tw(font, text):.0f}>{box_w}"
    if bg is not None:
        d.rectangle([box_x, box_y, box_x + box_w, box_y + 16], fill=bg)
    d.text((box_x, box_y + 2), text, font=font, fill=fill)


def flag(d, x, y, w, h, stripes):
    """Simple horizontal-stripe flag; stripes = list of colors top->bottom."""
    n = len(stripes)
    for i, c in enumerate(stripes):
        d.rectangle([x, y + i * h / n, x + w, y + (i + 1) * h / n], fill=c)
    d.rectangle([x, y, x + w, y + h], outline=INK, width=1)


def person(d, cx, base_y, h, suit, skin=(232, 190, 150), hair=(40, 40, 40)):
    """Minimal flat person: head + shoulders, standing on base_y."""
    r = h * 0.16
    d.ellipse([cx - r, base_y - h, cx + r, base_y - h + 2 * r], fill=skin)
    d.pieslice([cx - r, base_y - h, cx + r, base_y - h + 2 * r], 180, 360, fill=hair)
    d.polygon([(cx - h * 0.30, base_y), (cx + h * 0.30, base_y),
               (cx + h * 0.20, base_y - h * 0.42), (cx - h * 0.20, base_y - h * 0.42)], fill=suit)
    d.polygon([(cx - h * 0.07, base_y - h * 0.42), (cx + h * 0.07, base_y - h * 0.42),
               (cx, base_y - h * 0.18)], fill=WHITE)


def building(d, x, y, w, h, body, roof):
    d.rectangle([x, y, x + w, y + h], fill=body)
    d.polygon([(x - 4, y), (x + w / 2, y - h * 0.28), (x + w + 4, y)], fill=roof)
    for i in range(4):
        wx = x + 6 + i * (w - 12) / 4
        d.rectangle([wx, y + h * 0.30, wx + (w - 12) / 8, y + h * 0.62], fill=NAVY)
    d.rectangle([x + w / 2 - 5, y + h * 0.62, x + w / 2 + 5, y + h], fill=NAVY)


def spiral(d, cx, cy, r_max, color, width=3):
    """Cyclone spiral: archimedean, drawn as polyline."""
    pts = []
    for t in range(0, 620, 8):
        a = math.radians(t)
        r = r_max * t / 620.0
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    d.line(pts, fill=color, width=width, joint="curve")

# ================= CONTENT (49 stories; all figures verified in research.md) =================
# Canonical numbers (identical everywhere on the page):
#   Anthropic $81.3bn | GTA VI 24.6m / $2.4bn day one | Akvan 298,676 | ICJ 9-6 / 700,000+
#   Bangladesh 50 | Dow -1,101 | Greenland 109-0 | Ebola 11,376/5,568 (data 14 Nov)

STATS = [
    ("9–6", "ICJ VOTE"),
    ("$81.3BN", "ANTHROPIC RAISED"),
    ("24.6M", "GTA VI COPIES"),
    ("298,676", "AKVAN EVACUATED"),
    ("−1,101", "DOW"),
    ("109–0", "GREENLAND"),
]

LEADS = [
    {
        "num": 1, "region": "ASIA",
        "kicker": "1 · SHENZHEN — TRILATERAL",
        "headline": "Trump–Xi–Putin hold first-ever trilateral summit",
        "deck": "Declaration: “a nuclear war should never be fought”. Trump: “12 out of 10”.",
        "banner": "SHENZHEN · FIRST TRILATERAL",
        "bg": (222, 228, 238),
    },
    {
        "num": 2, "region": "EUROPE",
        "kicker": "2 · THE HAGUE — ICJ RULING",
        "headline": "ICJ: Myanmar committed genocide in 2017",
        "deck": "9–6 ruling, a first for a state; 10,000 killed, 700,000+ driven out in 2017.",
        "banner": "THE HAGUE · GENOCIDE RULING",
        "bg": (226, 232, 222),
    },
    {
        "num": 3, "region": "GLOBAL",
        "kicker": "3 · ANTALYA — COP31",
        "headline": "COP31 draft drops fossil-fuel phase-out",
        "deck": "144 paragraphs cut to 80; $120bn adaptation goal dropped; talks end Friday.",
        "banner": "ANTALYA · PHASE-OUT CUT",
        "bg": (232, 226, 210),
    },
]

# cards: headline (<=34 chars over 2 lines), deck (<=44 chars over 2 lines),
# chip (data), loc bar, source, tag
CARDS = [
    {"headline": "Anthropic IPO: biggest ever",
     "deck": "Opened $111.50, closed $97.17 (+17%)",
     "chip": "$81.3BN", "chip_fill": GREEN,
     "loc": "NEW YORK · NASDAQ", "src": "Reuters", "tag": "CONFIRMED", "scene": "ipo"},
    {"headline": "GTA VI: biggest game launch",
     "deck": "24.6m copies; US unlock at midnight ET",
     "chip": "24.6M", "chip_fill": NAVY,
     "loc": "NEW YORK · GAMING", "src": "Sensor Tower", "tag": "CONFIRMED", "scene": "gta"},
    {"headline": "Akvan: 298,676 evacuated",
     "deck": "Landfall due Friday near Gopalpur, Odisha",
     "chip": "298,676", "chip_fill": RED,
     "loc": "ODISHA · INDIA", "src": "IMD", "tag": "FORECAST", "scene": "akvan"},
    {"headline": "Kerch bridge hit, day three",
     "deck": "Neptune strike halts rail; Putin: no talks",
     "chip": "DAY 3", "chip_fill": RED,
     "loc": "KYIV · KERCH", "src": "Reuters", "tag": "CONFIRMED", "scene": "kerch"},
    {"headline": "Houthi missile hits PIF Tower",
     "deck": "Houthi strike at dawn; Riyadh's tallest tower",
     "chip": "DAWN", "chip_fill": RED,
     "loc": "RIYADH · SAUDI ARABIA", "src": "Reuters", "tag": "REPORTED", "scene": "riyadh"},
    {"headline": "Israel crosses Yellow Line",
     "deck": "First ground move since ceasefire; plan 4/26",
     "chip": "4/26", "chip_fill": NAVY,
     "loc": "GAZA", "src": "Reuters", "tag": "CONFIRMED", "scene": "gaza"},
    {"headline": "50 Gazipur factories shut",
     "deck": "Garment unrest; losses Tk 3,000–4,000 crore",
     "chip": "50", "chip_fill": RED,
     "loc": "GAZIPUR · DHAKA", "src": "AP", "tag": "CONFIRMED", "scene": "factory"},
    {"headline": "Jepchirchir banned 3 years",
     "deck": "Kenya marathon champ; EPO",
     "chip": "3 YRS", "chip_fill": RED,
     "loc": "KENYA · ATHLETICS", "src": "AIU", "tag": "CONFIRMED", "scene": "athletics"},
    {"headline": "Dow falls 1,101",
     "deck": "Below 50,000 first time since June",
     "chip": "−1,101", "chip_fill": RED,
     "loc": "WALL STREET", "src": "AP", "tag": "CONFIRMED", "scene": "markets"},
    {"headline": "IEA: gravest threat",
     "deck": "Tanker hit near Khasab; base struck 30 times",
     "chip": "30+ HITS", "chip_fill": RED,
     "loc": "GULF · HORMUZ", "src": "AFP / AP", "tag": "CLAIM", "scene": "gulf"},
    {"headline": "Xavier nears Pukapuka",
     "deck": "Category 5 cyclone; gusts 315 km/h",
     "chip": "CAT 5", "chip_fill": ORANGE,
     "loc": "COOK ISLANDS", "src": "JTWC", "tag": "FORECAST", "scene": "xavier"},
    {"headline": "Texans crush Colts 26–3",
     "deck": "Stroud throws 3 TDs; first home win",
     "chip": "26–3", "chip_fill": GREEN,
     "loc": "HOUSTON · NFL", "src": "AP", "tag": "CONFIRMED", "scene": "nfl"},
]

# briefs 16-49: (number, region, prefix, text) — one line each, <=44 chars total
BRIEFS = [
    (16, "AMERICAS", "NVIDIA", "CA subpoena; 879,000 chips"),
    (17, "AFRICA", "BADME", "Drone strikes, 4 hurt (reports)"),
    (18, "AMERICAS", "SENATE", "Energy 62–33; War Powers 48–51"),
    (19, "AFRICA", "SUDAN", "9 RSF drone strikes, 37 dead"),
    (20, "EUROPE", "SERBIA", "Cupic 140–97; acting president"),
    (21, "EUROPE", "PARIS", "Retirees march; 30,000 expected"),
    (22, "ASIA", "TOKYO", "India–Japan 2+2; live-fire first"),
    (23, "AMERICAS", "WALMART", "Revenue $189bn, up 5%"),
    (24, "GLOBAL", "GOLD", "Gold $3,674, 14-month low"),
    (25, "AFRICA", "MOZAMBIQUE", "Trial blocks 2028 vote"),
    (26, "EUROPE", "GREENLAND", "Denmark OKs US pact 109–0"),
    (27, "GLOBAL", "PEW", "Islam largest faith by 2035"),
    (28, "AMERICAS", "TRUMP–VANCE", "Trump frustrated on Iran"),
    (29, "EUROPE", "BERLIN", "Europe allies meet on Ukraine"),
    (30, "AFRICA", "EBOLA", "11,376 cases, 5,568 deaths, 14 Nov"),
    (31, "AMERICAS", "MEASLES", "5,412 US cases, 12 Nov"),
    (32, "AMERICAS", "HAITI", "34 gang members killed in raid"),
    (33, "EUROPE", "N. IRELAND", "N. Ireland 1–0 Luxembourg"),
    (34, "ASIA", "SUNEUNG", "551,864 sit Korea exam"),
    (35, "AMERICAS", "FLORIDA", "Broward floods; schools shut"),
    (36, "ASIA", "INDONESIA", "Seizure law after 18 years"),
    (37, "ASIA", "MONGOLIA", "Resignation accepted 96/104"),
    (38, "ASIA", "S. KOREA", "Exports pass $1 trillion"),
    (39, "OCEANIA", "AUSTRALIA", "Jobless 4.9%, 753,700"),
    (40, "OCEANIA", "FIJI", "El Niño drought bites"),
    (41, "AMERICAS", "CALIFORNIA", "LA floods; rivers rage"),
    (42, "ASIA", "SEOUL", "Han Duck-soo retrial ordered"),
    (43, "AFRICA", "SOMALIA", "Expels UAE ambassador"),
    (44, "AMERICAS", "COLOMBIA", "National strike in Bogotá"),
    (45, "ASIA", "APEC", "“Shenzhen Outlook” adopted"),
    (46, "OCEANIA", "ALBANESE", "“End your war” to Putin"),
    (47, "AFRICA", "SUDAN", "SAF claims siege broken"),
    (48, "ASIA", "TAIWAN", "Xi: “do the right thing”, US"),
    (49, "AMERICAS", "NBA", "Trail Blazers 124, Bucks 114"),
]

TIMELINE = [
    ("04:45", "Xi–Trump lunch"),
    ("05:00", "GTA VI unlocks in US"),
    ("06:30", "Trilateral begins"),
    ("09:00", "Akvan fix (IMD)"),
    ("10:58", "Hamas reply"),
    ("14:00", "Badme report"),
]

DATE_OUT = ("EU €45bn loan · Iran strikes Kuwait/Bahrain · Nvidia $115.8bn · "
            "Jeffries 251–11 · Peltola · Anthropic $83 · GTA VI NZ launch · "
            "UK inflation 3.6% · Fed minutes · Kerch road span")
DATE_NOTYET = ("Akvan landfall Fri 20 Nov · COP31 close Fri 20 Nov · "
               "ICJ compensation phase · Ebola Phase 2 trial 26–27 Nov Bunia")

REGION_COUNTS = [("ASIA", 11), ("AMERICAS", 14), ("EUROPE", 7), ("AFRICA", 7),
                 ("OCEANIA", 4), ("MIDDLE EAST", 3), ("GLOBAL", 3)]

# map pins: (number, lon, lat, dx, dy) — dx/dy = manual offset in px when crowded
PINS = [
    (1, 114.1, 22.5, 0, 0),      # Shenzhen
    (2, 4.3, 52.1, 0, 0),        # Den Haag
    (3, 30.7, 36.9, -10, -4),    # Antalya (fanned from Kerch/Gaza)
    (4, -74.0, 40.7, 0, 0),      # New York (Anthropic)
    (5, -122.0, 37.8, -8, -8),   # San Francisco (GTA VI, fanned from LA)
    (6, 84.9, 19.3, 0, 10),      # Gopalpur (Akvan, fanned from Gazipur)
    (7, 35.4, 45.3, 0, -14),     # Kerch (fanned from Antalya)
    (8, 46.7, 24.6, 2, 14),      # Riyadh (fanned from Gaza/Khasab)
    (9, 34.5, 31.5, -12, 10),    # Gaza (fanned from Antalya)
    (10, 90.4, 23.8, 0, -10),    # Gazipur (fanned from Gopalpur)
    (11, 36.8, -1.3, 0, 10),     # Nairobi (Jepchirchir; offset S to clear Bunia dot)
    (12, -74.0, 40.7, 16, -12),  # Wall Street (Dow) — offset from NYC pin
    (13, 56.2, 26.2, 10, -6),    # Khasab / Hormuz (fanned from Riyadh)
    (14, -165.8, -10.9, 0, 0),   # Pukapuka (Xavier)
    (15, -95.4, 29.8, 0, 0),     # Houston (NFL)
]

# map dots for briefs: (lon, lat, region, dx, dy)
DOTS = [
    (-122.0, 37.0, "AMERICAS", 0, 0),    # NVIDIA (California)
    (38.9, 14.7, "AFRICA", 0, 0),        # Badme
    (-77.0, 38.9, "AMERICAS", 0, 0),     # US Senate (DC)
    (30.2, 13.2, "AFRICA", 0, 0),        # Sudan / El Obeid
    (20.5, 44.8, "EUROPE", 0, 0),        # Belgrade
    (2.35, 48.85, "EUROPE", 0, 0),       # Paris
    (139.7, 35.7, "ASIA", 0, 0),         # Tokyo
    (-94.2, 36.4, "AMERICAS", 0, 0),     # Walmart (Arkansas)
    (-0.1, 51.5, "GLOBAL", 0, 0),        # Gold (London)
    (32.6, -25.9, "AFRICA", 0, 0),       # Maputo
    (-51.7, 64.2, "EUROPE", 0, 0),       # Greenland (Nuuk)
    (-77.0, 38.9, "GLOBAL", 7, -7),      # Pew (DC, offset)
    (-77.0, 38.9, "AMERICAS", -7, 7),    # Trump vs Vance (DC, offset)
    (13.4, 52.5, "EUROPE", 0, 0),        # Berlin
    (29.5, 1.6, "AFRICA", 0, 0),         # Bunia (Ebola)
    (-84.4, 33.7, "AMERICAS", 0, 0),     # Atlanta (CDC / measles)
    (-72.3, 18.5, "AMERICAS", 0, 0),     # Port-au-Prince
    (-5.9, 54.6, "EUROPE", 0, 0),        # Belfast
    (127.0, 37.5, "ASIA", 0, 0),         # Seoul (Suneung)
    (-80.2, 25.8, "AMERICAS", 0, 0),     # Miami (Florida)
    (106.8, -6.2, "ASIA", 0, 0),         # Jakarta
    (106.9, 47.9, "ASIA", 0, 0),         # Ulaanbaatar
    (127.0, 37.5, "ASIA", 7, 6),         # S. Korea exports (Seoul, offset)
    (149.1, -35.3, "OCEANIA", 0, 0),     # Canberra
    (178.0, -17.7, "OCEANIA", 0, 0),     # Fiji
    (-118.2, 34.0, "AMERICAS", 0, 12),   # Los Angeles (California brief)
    (127.0, 37.5, "ASIA", -7, -6),       # Seoul (Han retrial, offset)
    (45.3, 2.0, "AFRICA", 0, 0),         # Mogadishu
    (-74.1, 4.6, "AMERICAS", 0, 0),      # Bogotá
    (114.1, 22.5, "ASIA", 8, 8),         # APEC (Shenzhen, offset from pin 1)
    (149.1, -35.3, "OCEANIA", 7, 7),     # Albanese (Canberra, offset)
    (30.2, 13.2, "AFRICA", 8, -6),       # SAF claim (El Obeid, offset)
    (121.6, 25.0, "ASIA", 0, 0),         # Taipei
    (-87.9, 43.0, "AMERICAS", 0, 0),     # Milwaukee (NBA)
]

# ---------------- lead art (318 x 96) ----------------
def draw_lead_art(d, idx, x, y, w, h):
    lead = LEADS[idx]
    d.rectangle([x, y, x + w, y + h], fill=lead["bg"])
    if idx == 0:
        # Shenzhen: three flags + names, villa (right), round table with 3 leaders
        flag(d, x + 36, y + 6, 36, 18,
             [RED, WHITE, RED, WHITE, RED, WHITE, RED])
        d.rectangle([x + 36, y + 6, x + 52, y + 12], fill=NAVY)
        flag(d, x + 141, y + 6, 36, 18, [RED, RED, RED, RED, RED])
        # China: five yellow stars in the canton
        d.ellipse([x + 145, y + 9, x + 150, y + 14], fill=(255, 222, 0))
        for sx, sy in [(154, 8), (157, 11), (154, 14), (151, 14)]:
            d.ellipse([x + sx - 1, y + sy - 1, x + sx + 1, y + sy + 1],
                      fill=(255, 222, 0))
        flag(d, x + 246, y + 6, 36, 18, [WHITE, (0, 60, 160), RED])
        for fx, name in [(x + 36, "US"), (x + 141, "CHINA"), (x + 246, "RUSSIA")]:
            nw = tw(F_TINY_B, name)
            d.text((fx + 18 - nw / 2, y + 25), name, font=F_TINY_B, fill=INK)
        # Kylin Villa (small building, right) — label right-aligned in the art
        kv = "KYLIN VILLA"
        d.text((x + w - tw(F_TINY_B, kv) - 2, y + 36), kv, font=F_TINY_B, fill=INK)
        building(d, x + 262, y + 54, 54, 24, (190, 180, 150), RED_DK)
        # three leaders behind a round table (centre-left)
        for px, suit in [(x + 120, NAVY), (x + 160, (60, 60, 60)), (x + 200, (90, 30, 30))]:
            person(d, px, y + 68, 36, suit)
        d.ellipse([x + 100, y + 62, x + 220, y + 82], fill=(120, 80, 50))
        d.ellipse([x + 100, y + 62, x + 220, y + 72], fill=(150, 105, 65))
    elif idx == 1:
        # ICJ: Peace Palace + scales + Rakhine map + 9-6 chip
        d.text((x + 28, y + 6), "PEACE PALACE", font=F_TINY_B, fill=INK)
        building(d, x + 28, y + 34, 72, 44, (205, 195, 165), NAVY)
        d.rectangle([x + 58, y + 20, x + 70, y + 34], fill=NAVY)
        d.polygon([(x + 56, y + 20), (x + 64, y + 12), (x + 72, y + 20)], fill=NAVY)
        # scales of justice
        cx, by = x + 185, y + 78
        d.line([cx, by - 34, cx, by], fill=INK, width=2)
        d.line([cx - 26, by - 34, cx + 26, by - 34], fill=INK, width=2)
        for sx in (cx - 26, cx + 26):
            d.line([sx, by - 34, sx, by - 22], fill=INK, width=1)
            d.arc([sx - 10, by - 22, sx + 10, by - 8], 0, 180, fill=INK, width=2)
        # Rakhine blob (tan shape, right)
        d.polygon([(x + 250, y + 44), (x + 278, y + 40), (x + 296, y + 50),
                   (x + 290, y + 66), (x + 262, y + 68), (x + 248, y + 56)],
                  fill=(210, 190, 140), outline=INK)
        d.text((x + 252, y + 70), "RAKHINE", font=F_TINY_B, fill=INK)
        chip(d, x + 262, y + 8, "9–6", RED)
    else:
        # COP31: globe + struck-through PHASE-OUT + thermometer
        cx, cy, r = x + 70, y + 48, 32
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(120, 170, 200))
        d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=NAVY, width=2)
        d.ellipse([cx - r + 8, cy - r + 6, cx - r + 22, cy - r + 18], fill=(90, 140, 90))
        d.ellipse([cx + 4, cy + 8, cx + 20, cy + 22], fill=(90, 140, 90))
        d.line([cx - r, cy, cx + r, cy], fill=NAVY, width=1)
        d.arc([cx - r, cy - 14, cx + r, cy + 14], 0, 360, fill=NAVY, width=1)
        t = "PHASE-OUT"
        d.text((x + 122, y + 42), t, font=_dj(13, True), fill=(120, 120, 120))
        d.line([x + 120, y + 50, x + 122 + tw(_dj(13, True), t), y + 50],
               fill=RED, width=3)
        # thermometer (right)
        tx = x + 280
        d.rounded_rectangle([tx - 6, y + 30, tx + 6, y + 72], radius=6,
                            fill=WHITE, outline=INK, width=1)
        d.rounded_rectangle([tx - 4, y + 46, tx + 4, y + 70], radius=4, fill=RED)
        d.ellipse([tx - 10, y + 66, tx + 10, y + 86], fill=RED, outline=INK, width=1)
        d.text((x + 238, y + 50), "1.5°C", font=_dj(11, True), fill=RED)
        chip(d, x + 200, y + 8, "$120BN DROPPED", RED)
        chip(d, x + 200, y + 30, "144 → 80", NAVY)
    # bottom banner (all leads)
    d.rectangle([x, y + h - 16, x + w, y + h], fill=NAVY)
    bw = tw(F_BANNER, lead["banner"])
    d.text((x + (w - bw) / 2, y + h - 13), lead["banner"], font=F_BANNER, fill=WHITE)


# ---------------- card art (156 x 50) ----------------
def draw_card_art(d, scene, x, y, w, h, chip_text, chip_fill):
    if scene == "ipo":
        d.rectangle([x, y, x + w, y + h], fill=(24, 32, 54))
        d.rectangle([x + 10, y + 8, x + w - 10, y + h - 8], fill=(16, 22, 40))
        bars = [(18, GREEN), (30, RED), (26, GREEN), (34, GREEN)]
        bx = x + 16
        for bh, c in bars:
            d.rectangle([bx, y + h - 12 - bh, bx + 12, y + h - 12], fill=c)
            bx += 18
        d.text((x + 96, y + 10), "$", font=_pf(28, b"Bold"), fill=(120, 220, 130))
    elif scene == "gta":
        d.rectangle([x, y, x + w, y + h], fill=(18, 22, 40))
        d.ellipse([x + w - 34, y + 6, x + w - 14, y + 26], fill=(240, 230, 180))
        for i, bh in enumerate([22, 34, 28, 40, 18]):
            bx = x + 10 + i * 24
            d.rectangle([bx, y + h - bh, bx + 18, y + h], fill=(40, 55, 90))
            d.rectangle([bx + 4, y + h - bh + 5, bx + 8, y + h - bh + 9], fill=(255, 220, 90))
            d.rectangle([bx + 12, y + h - bh + 12, bx + 16, y + h - bh + 16], fill=(255, 220, 90))
    elif scene == "akvan":
        d.rectangle([x, y, x + w, y + h], fill=(198, 220, 235))
        spiral(d, x + 62, y + 26, 22, NAVY, 3)
        for i in range(3):
            lx = x + 108 + i * 12
            d.line([lx, y + 10, lx - 6, y + 22], fill=(90, 130, 180), width=2)
        d.polygon([(x + 118, y + h), (x + w, y + h), (x + w, y + 30)], fill=(210, 190, 140))
    elif scene == "kerch":
        d.rectangle([x, y, x + w, y + h], fill=(208, 222, 232))
        d.rectangle([x + 8, y + 30, x + 68, y + 36], fill=(60, 60, 60))
        d.polygon([(x + 88, y + 30), (x + 148, y + 42), (x + 148, y + 48), (x + 88, y + 36)],
                  fill=(60, 60, 60))
        d.line([x + 20, y + 30, x + 20, y + h], fill=(60, 60, 60), width=3)
        d.line([x + 140, y + 30, x + 140, y + h], fill=(60, 60, 60), width=3)
        for i in range(4):
            d.line([x + 120 - i * 10, y + 6 + i * 6, x + 128 - i * 10, y + 10 + i * 6],
                   fill=RED, width=2)
    elif scene == "riyadh":
        d.rectangle([x, y, x + w, y + h], fill=(235, 222, 200))
        tx = x + w // 2
        d.polygon([(tx - 12, y + h), (tx - 12, y + 16), (tx, y + 4), (tx + 12, y + 16),
                   (tx + 12, y + h)], fill=(50, 50, 60))
        for wy in range(y + 20, y + h - 4, 8):
            d.rectangle([tx - 8, wy, tx + 8, wy + 3], fill=(255, 220, 90))
        for ang in range(0, 360, 45):
            a = math.radians(ang)
            d.line([tx, y + 12, tx + 16 * math.cos(a), y + 12 + 16 * math.sin(a)],
                   fill=ORANGE, width=3)
        d.ellipse([tx - 5, y + 7, tx + 5, y + 17], fill=(255, 200, 60))
    elif scene == "gaza":
        d.rectangle([x, y, x + w, y + h], fill=(228, 220, 200))
        for tx in (x + 24, x + 84):
            d.polygon([(tx - 20, y + h), (tx, y + 14), (tx + 20, y + h)], fill=(190, 170, 130))
            d.rectangle([tx - 3, y + 30, tx + 3, y + h], fill=RED)
        d.rectangle([x, y + 22, x + w, y + 28], fill=(255, 220, 0))
    elif scene == "factory":
        d.rectangle([x, y, x + w, y + h], fill=(225, 218, 200))
        d.rectangle([x + 14, y + 22, x + 96, y + h], fill=(120, 110, 100))
        for i in range(3):
            d.polygon([(x + 14 + i * 28, y + 22), (x + 28 + i * 28, y + 10),
                       (x + 42 + i * 28, y + 22)], fill=(90, 80, 70))
        d.rectangle([x + 104, y + 8, x + 112, y + h], fill=(90, 80, 70))
        for i, (sx, sy, sr) in enumerate([(118, 8, 6), (126, 2, 5), (132, 8, 4)]):
            d.ellipse([x + sx - sr, y + sy - sr, x + sx + sr, y + sy + sr],
                      fill=(200, 200, 200))
        for wx in range(4):
            d.rectangle([x + 20 + wx * 20, y + 30, x + 28 + wx * 20, y + 38],
                        fill=(255, 220, 90))
    elif scene == "flood":
        d.rectangle([x, y, x + w, y + h], fill=(190, 210, 225))
        d.arc([x - 20, y + 8, x + 90, y + 70], 180, 360, fill=(40, 100, 170), width=6)
        d.arc([x + 40, y + 18, x + 150, y + 80], 180, 360, fill=(40, 100, 170), width=6)
        d.rectangle([x + 96, y + 30, x + 140, y + 42], fill=RED)
        d.ellipse([x + 102, y + 40, x + 112, y + 50], fill=INK)
        d.ellipse([x + 124, y + 40, x + 134, y + 50], fill=INK)
    elif scene == "markets":
        d.rectangle([x, y, x + w, y + h], fill=(240, 230, 225))
        for gy in (y + 12, y + 25, y + 38):
            d.line([x + 8, gy, x + w - 8, gy], fill=(210, 200, 190), width=1)
        d.line([(x + 10, y + 10), (x + 46, y + 16), (x + 82, y + 14),
                (x + 118, y + 30), (x + 146, y + 44)], fill=RED, width=3, joint="curve")
        d.polygon([(x + 140, y + 44), (x + 146, y + 36), (x + 152, y + 44)], fill=RED)
    elif scene == "gulf":
        d.rectangle([x, y, x + w, y + h], fill=(200, 215, 225))
        d.rectangle([x, y + 30, x + w, y + h], fill=(70, 120, 170))
        d.polygon([(x + 30, y + 30), (x + 126, y + 30), (x + 118, y + 42),
                   (x + 38, y + 42)], fill=(40, 40, 50))
        d.rectangle([x + 96, y + 16, x + 112, y + 30], fill=(40, 40, 50))
        for ang in range(0, 360, 45):
            a = math.radians(ang)
            d.line([x + 66, y + 22, x + 66 + 11 * math.cos(a), y + 22 + 11 * math.sin(a)],
                   fill=ORANGE, width=2)
        d.ellipse([x + 62, y + 18, x + 70, y + 26], fill=(255, 200, 60))
    elif scene == "xavier":
        d.rectangle([x, y, x + w, y + h], fill=(205, 225, 235))
        spiral(d, x + 62, y + 26, 22, TEAL, 3)
        d.ellipse([x + 112, y + 36, x + 148, y + 46], fill=(210, 190, 140))
        d.polygon([(x + 122, y + 36), (x + 130, y + 24), (x + 138, y + 36)], fill=GREEN)
    elif scene == "athletics":
        # running track: red-brown with white lane lines, runner, finish line
        d.rectangle([x, y, x + w, y + h], fill=(178, 80, 50))
        for ly in (y + 12, y + 24, y + 36):
            d.line([x, ly, x + w, ly], fill=WHITE, width=2)
        rx, ry = x + w // 2 - 10, y + 30
        d.ellipse([rx - 5, ry - 14, rx + 5, ry - 4], fill=INK)
        d.line([rx, ry - 4, rx + 3, ry + 8], fill=INK, width=4)
        d.line([rx + 3, ry + 8, rx - 8, ry + 18], fill=INK, width=3)
        d.line([rx + 3, ry + 8, rx + 12, ry + 16], fill=INK, width=3)
        d.line([rx, ry - 2, rx - 10, ry + 4], fill=INK, width=3)
        d.line([rx, ry - 2, rx + 10, ry - 8], fill=INK, width=3)
        for i in range(3):
            d.rectangle([x + w - 12, y + 8 + i * 12, x + w - 6, y + 14 + i * 12], fill=WHITE)
            d.rectangle([x + w - 6, y + 8 + i * 12, x + w, y + 14 + i * 12], fill=INK)
    else:  # nfl
        d.rectangle([x, y, x + w, y + h], fill=(46, 125, 70))
        for lx in (x + 30, x + 78, x + 126):
            d.line([lx, y, lx, y + h], fill=WHITE, width=2)
        d.line([x + 138, y + 8, x + 138, y + 42], fill=(255, 220, 0), width=3)
        d.line([x + 138, y + 14, x + 150, y + 14], fill=(255, 220, 0), width=3)
        d.ellipse([x + 56, y + 18, x + 92, y + 34], fill=(120, 70, 30))
        d.line([x + 62, y + 26, x + 86, y + 26], fill=WHITE, width=1)
    # data chip (top-left, white outline for contrast)
    cw = int(tw(F_CHIP, chip_text)) + 14
    d.rounded_rectangle([x + 4, y + 4, x + 4 + cw, y + 22], radius=4,
                        fill=chip_fill, outline=WHITE, width=1)
    d.text((x + 11, y + 7), chip_text, font=F_CHIP, fill=WHITE)

# ---------------- sections ----------------
def draw_masthead(d):
    d.rectangle([MX, 8, RIGHT, 108], fill=NAVY)
    d.text((MX, 15), "THE WORLD IN ONE DAY", font=F_KICK, fill=(200, 205, 220))
    cw = int(tw(F_CHIP, "NOV 19 · THU 2026")) + 14
    chip(d, RIGHT - cw - 10, 12, "NOV 19 · THU 2026", RED)
    d.text((MX, 12), "Thursday 19 November 2026", font=F_MAST, fill=WHITE)
    d.text((MX, 97), "49 STORIES · SEVEN REGIONS", font=F_SMALL_B, fill=(200, 205, 220))
    rt = "ONE DAY · ONE PAGE"
    d.text((RIGHT - tw(F_SMALL_B, rt), 97), rt, font=F_SMALL_B, fill=(200, 205, 220))


def draw_stats(d):
    y0, y1 = 116, 152
    d.line([MX, y1, RIGHT, y1], fill=HAIR, width=1)
    cw = CW / len(STATS)
    for i, (num, lab) in enumerate(STATS):
        cx = MX + cw * i + cw / 2
        d.text((cx - tw(F_STAT_N, num) / 2, y0 + 2), num, font=F_STAT_N, fill=RED)
        d.text((cx - tw(F_STAT_L, lab) / 2, y0 + 22), lab, font=F_STAT_L, fill=INK)
        if i:
            d.line([MX + cw * i, y0 + 4, MX + cw * i, y1 - 4], fill=HAIR, width=1)


def draw_top_label(d):
    d.text((MX, 158), "TOP STORIES", font=F_LABEL, fill=NAVY)
    legend = [
        ("CONFIRMED", "2+ outlets"),
        ("REPORTED", "one outlet"),
        ("CLAIM", "one side"),
        ("FORECAST", "expected"),
    ]
    # measure right-aligned legend (tag bold + definition regular)
    total = tw(F_SMALL_B, "HOW SURE: ") + 2
    for tag, defin in legend:
        total += 11 + tw(F_TINY_B, tag) + 3 + tw(F_TINY, defin) + 14
    x = RIGHT - total
    d.text((x, 159), "HOW SURE:", font=F_SMALL_B, fill=INK)
    x += tw(F_SMALL_B, "HOW SURE: ") + 2
    for tag, defin in legend:
        d.rectangle([x, 161, x + 8, 169], fill=TAG_COLOR[tag])
        x += 11
        d.text((x, 159), tag, font=F_TINY_B, fill=INK)
        x += tw(F_TINY_B, tag) + 3
        d.text((x, 159), defin, font=F_TINY, fill=GREY)
        x += tw(F_TINY, defin) + 14


def draw_leads(d):
    xs = [MX, 353, 682]
    for i, lead in enumerate(LEADS):
        x = xs[i]
        w = 318
        draw_lead_art(d, i, x, 174, w, 96)
        d.ellipse([x, 277, x + 7, 284], fill=REGION[lead["region"]])
        d.text((x + 11, 276), lead["kicker"], font=F_KICK, fill=REGION[lead["region"]])
        lines = fit_lines(lead["headline"], F_LEAD_H, w, 2)
        draw_lines(d, lines, x, 292, F_LEAD_H, INK, 24)
        dlines = fit_lines(lead["deck"], F_DECK, w, 2)
        draw_lines(d, dlines, x, 340, F_DECK, INK, 15)


def draw_cards(d):
    xs = [MX + i * 164 for i in range(6)]
    ys = [368, 514]
    for r in range(2):
        for c in range(6):
            card = CARDS[r * 6 + c]
            x, y = xs[c], ys[r]
            w = 156
            d.rectangle([x, y, x + w, y + 138], fill=(252, 250, 244), outline=HAIR, width=1)
            draw_card_art(d, card["scene"], x + 1, y + 1, w - 2, 50,
                          card["chip"], card["chip_fill"])
            d.rectangle([x + 1, y + 51, x + w - 1, y + 65], fill=NAVY)
            label_in_box(d, card["loc"], x + 5, y + 54, w - 10, F_LOC, WHITE)
            lines = fit_lines(card["headline"], F_CARD_H, w - 12, 2)
            draw_lines(d, lines, x + 6, y + 68, F_CARD_H, INK, 17)
            dlines = fit_lines(card["deck"], F_DECK, w - 12, 2)
            draw_lines(d, dlines, x + 6, y + 104, F_DECK, INK, 13)
            tag = card["tag"]
            src = f"{card['src']} · "
            d.text((x + 6, y + 128), src, font=F_SRC, fill=GREY)
            d.text((x + 6 + tw(F_SRC, src), y + 128), tag, font=F_TINY_B,
                   fill=TAG_COLOR[tag])


def draw_timeline(d):
    y = 656
    d.line([MX, y, RIGHT, y], fill=HAIR, width=1)
    d.text((MX, y + 14), "THE DAY IN UTC", font=F_SMALL_B, fill=NAVY)
    slot_x = 150
    slot_w = (RIGHT - slot_x) / len(TIMELINE)
    for i, (t, lab) in enumerate(TIMELINE):
        x = slot_x + i * slot_w
        d.text((x, y + 6), t, font=F_TL_TIME, fill=RED)
        assert tw(F_TL, lab) <= slot_w - 6, f"TIMELINE OVERFLOW {lab!r}"
        d.text((x, y + 22), lab, font=F_TL, fill=INK)
        if i:
            d.line([x - 6, y + 6, x - 6, y + 30], fill=HAIR, width=1)
    d.line([MX, y + 34, RIGHT, y + 34], fill=HAIR, width=1)


# map projection: lon -180..180 -> x 24..350 ; lat 75..-60 -> y 708..883
MAP_X0, MAP_Y0, MAP_W, MAP_H = MX, 708, 326, 175
MAP_SX = MAP_W / 360.0
MAP_SY = MAP_H / 135.0


def mxy(lon, lat):
    return (MAP_X0 + (lon + 180) * MAP_SX, MAP_Y0 + (75 - lat) * MAP_SY)


def draw_map(d):
    d.rectangle([MAP_X0, MAP_Y0, MAP_X0 + MAP_W, MAP_Y0 + MAP_H], fill=SEA)
    for poly in POLYS:
        pts = [mxy(lon, lat) for lon, lat in poly]
        d.polygon(pts, fill=LAND, outline=LAND_LINE)
    # brief dots first, pins last
    for lon, lat, reg, dx, dy in DOTS:
        px, py = mxy(lon, lat)
        px, py = px + dx, py + dy
        d.ellipse([px - 3.5, py - 3.5, px + 3.5, py + 3.5],
                  fill=REGION[reg], outline=WHITE, width=1)
    pin_pts = []
    for num, lon, lat, dx, dy in PINS:
        px, py = mxy(lon, lat)
        px, py = px + dx, py + dy
        pin_pts.append((num, px, py))
        d.ellipse([px - 7, py - 7, px + 7, py + 7], fill=NAVY, outline=WHITE, width=1)
        t = str(num)
        d.text((px - tw(F_TINY_B, t) / 2, py - 6), t, font=F_TINY_B, fill=WHITE)
    # pin spacing assert (>=20px centre-to-centre)
    for i in range(len(pin_pts)):
        for j in range(i + 1, len(pin_pts)):
            ddx = pin_pts[i][1] - pin_pts[j][1]
            ddy = pin_pts[i][2] - pin_pts[j][2]
            dist = math.hypot(ddx, ddy)
            assert dist >= 19.5, (
                f"PINS TOO CLOSE: {pin_pts[i][0]} vs {pin_pts[j][0]} = {dist:.1f}px")
    return pin_pts


def draw_bottom(d):
    d.text((MX, 692), "WHERE IT HAPPENED", font=_dj(12, True), fill=NAVY)
    d.text((366, 692), "ALSO ON THURSDAY 19 NOVEMBER", font=_dj(12, True), fill=NAVY)
    draw_map(d)
    d.text((MX, 890), "Pins 1–15: lead + card stories  ·  dots: briefs 16–49",
           font=F_TINY, fill=GREY)
    # region bar (two lines with colour dots)
    y = 912
    x = MX
    for j, (reg, n) in enumerate(REGION_COUNTS[:4]):
        d.ellipse([x, y + 2, x + 7, y + 9], fill=REGION[reg])
        t = f"{reg} {n}"
        d.text((x + 10, y), t, font=F_SMALL_B, fill=INK)
        x += 10 + tw(F_SMALL_B, t) + 14
    y = 930
    x = MX
    for j, (reg, n) in enumerate(REGION_COUNTS[4:]):
        d.ellipse([x, y + 2, x + 7, y + 9], fill=REGION[reg])
        t = f"{reg} {n}"
        d.text((x + 10, y), t, font=F_SMALL_B, fill=INK)
        x += 10 + tw(F_SMALL_B, t) + 14
    d.text((x + 6, y), "TOTAL 49", font=F_SMALL_B, fill=RED)
    # briefs (two columns, 17 each)
    cols = [(366, BRIEFS[:17]), (687, BRIEFS[17:])]
    for cx, items in cols:
        yy = 708
        for num, reg, prefix, text in items:
            full = f"{num}. {prefix} — {text}"
            font = F_BRIEF
            if tw(font, full) > 313:
                font = _dj(12)
            if tw(font, full) > 313:
                font = _dj(11)
            assert tw(font, full) <= 313, f"BRIEF OVERFLOW: {full!r} {tw(font, full):.0f}"
            # number in region colour, rest in ink; prefix bold
            d.text((cx, yy), f"{num}.", font=_dj(13, True), fill=REGION[reg])
            nx = cx + tw(_dj(13, True), f"{num}. ")
            d.text((nx, yy), prefix, font=_dj(13, True), fill=INK)
            px = nx + tw(_dj(13, True), prefix)
            d.text((px, yy), f" — {text}", font=font, fill=INK)
            yy += 15
        assert yy <= 963 + 1, f"BRIEF COLUMN OVERFLOW to y={yy}"


def draw_datecheck(d):
    d.rectangle([MX, 966, RIGHT, 998], fill=(250, 235, 230), outline=RED, width=1)
    l1 = fit_lines("DATE CHECK — LEFT OUT (18 NOV): " + DATE_OUT, F_TINY, 944, 2)
    draw_lines(d, l1, MX + 8, 967, F_TINY, INK, 10)
    y = 967 + 10 * len(l1)
    d.text((MX + 8, y), "NOT YET: " + DATE_NOTYET, font=F_TINY, fill=INK)
    assert y + 10 <= 998, "DATE CHECK OVERFLOW"


def draw_footer(d):
    f = ("Sources: Reuters · AP · AFP · BBC · Al Jazeera · WHO · UN/ICJ · ONS · IMD · "
         "CDC · Senate/House · Amnesty · Pew · Sensor Tower — Original drawings.")
    d.text((MX, 1001), f, font=F_FOOT, fill=GREY)

# ---------------- main ----------------
def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    draw_masthead(d)
    draw_stats(d)
    draw_top_label(d)
    draw_leads(d)
    draw_cards(d)
    draw_timeline(d)
    draw_bottom(d)
    draw_datecheck(d)
    draw_footer(d)
    img.save(OUT, format="PNG", compress_level=6)
    return img


def word_count_report():
    """Words per story (headline+deck for drawn; text for briefs)."""
    total = 0
    for lead in LEADS:
        total += len((lead["headline"] + " " + lead["deck"]).split())
    for card in CARDS:
        total += len((card["headline"] + " " + card["deck"]).split())
    for _, _, _, text in BRIEFS:
        total += len(text.split())
    return total


def ink_at_300(img):
    """Masthead ink mass at 300px (playbook metric; target >= 1800px)."""
    small = img.resize((300, 300), Image.LANCZOS)
    small.save("/tmp/r4-300.png")
    px = small.load()
    ink = 0
    # masthead band occupies y 8..108 of 1024 -> y 2..31 of 300
    for yy in range(2, 32):
        for xx in range(7, 293):
            r, g, b = px[xx, yy]
            if r < 90 and g < 90 and b < 110:
                ink += 1
    return ink


if __name__ == "__main__":
    img = build()
    size = os.path.getsize(OUT)
    assert size <= 1024 * 1024, f"FILE TOO BIG: {size} bytes"
    assert img.size == (1024, 1024)
    # region counts sum
    assert sum(n for _, n in REGION_COUNTS) == 49, "REGION SUM != 49"
    assert len(BRIEFS) == 34 and len(CARDS) == 12 and len(LEADS) == 3
    assert len(PINS) == 15 and len(DOTS) == 34
    words = word_count_report()
    ink = ink_at_300(img)
    print(f"entry.png: {size} bytes, {img.size[0]}x{img.size[1]}")
    print(f"stories: 49 (3 leads + 12 cards + 34 briefs)")
    print(f"words total: {words} ({words / 49:.1f} per story; target <=17)")
    print(f"masthead ink @300px: {ink} px (target >=1800)")
    print(f"region counts: {REGION_COUNTS} sum={sum(n for _, n in REGION_COUNTS)}")
    print("OK")

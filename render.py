#!/usr/bin/env python3
"""Draw ONE DAY - Monday 23 November 2026: the world's news in one image.

Pure stdlib + Pillow. Deterministic: no timestamps, no randomness.
Writes entry.png (1024x1024) next to this file.
"""
import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "entry.png")

W, H = 1024, 1024
CREAM = (246, 241, 227)
INK = (26, 26, 24)
RED = (178, 34, 34)
NAVY = (24, 44, 84)
TEAL = (18, 90, 96)
GOLD = (176, 132, 24)
SEA = (214, 228, 230)
LAND = (216, 208, 184)
LAND_EDGE = (138, 130, 113)
GREY = (110, 108, 100)
LIGHT_LINE = (196, 188, 168)

SERIF_B = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf"
SANS_B = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns list of lines that fit max_w."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def fit_text(draw, text, fnt, max_w, suffix="..."):
    """Truncate one line to max_w, adding suffix."""
    if draw.textlength(text, font=fnt) <= max_w:
        return text
    while text and draw.textlength(text + suffix, font=fnt) > max_w:
        text = text[:-1]
    return text + suffix


def fit_size(draw, text, path, size, max_w):
    """Largest font size <= size that fits max_w."""
    while size > 10:
        fnt = font(path, size)
        if draw.textlength(text, font=fnt) <= max_w:
            return fnt
        size -= 1
    return font(path, size)


# ---------------------------------------------------------------- stories
# (headline, source, sure) sure: 2 = two or more outlets, 1 = one outlet
CARDS = [
    ("Houthis claim strikes on Saudi refinery and radar", "Indian Express", 2),
    ("Two tankers hit in Strait of Hormuz", "UKMTO", 2),
    ("M6.5 quake strikes Vanuatu region, 598 km deep", "USGS", 2),
    ("KOSPI sinks 5% in AI rout; Seoul pledges support", "Hindu BusinessLine", 2),
    ("ICE detains father, daughter at Seattle airport", "The Hindu", 2),
    ("US futures rebound after AI rout: Nasdaq +3%", "Hindu BusinessLine", 2),
    ("Liverpool rout ten-man Man Utd in Pochettino debut", "The Hindu", 2),
    ("Sea drones hit Russian warship at Benghazi base", "The Hindu", 2),
    ("Kenyan cult leader guilty of murdering 190 children", "Mombasa court", 1),
    ("Mexico captures cartel boss Chapo Isidro", "TALi", 1),
    ("Bolsonaro in intensive care, intestinal blockage", "One Turn", 1),
    ("NHS launches world's largest AI cancer trial", "BBC", 2),
]

ALSO = [
    "Mets sign Skubal: 9 yrs, $450M record",
    "Red Wings trade captain Larkin to Canadiens",
    "1,389 Indian children held in US since 2023",
    "Manchester arena evacuated in tear-gas scare",
    "Paolo Bulgari, jeweller, dies aged 89",
    "Slovakia refuses share of 45bn euro EU loan",
    "UK confirmed as 2035 Women's World Cup host",
    "Netanyahu-Eisenkot talks end with no deal",
    "Istanbul rally against media takeover",
    "Egypt condemns attacks on Bahrain",
    "India, China open 10-day LAC talks",
    "Nepal PM Balen Shah starts India visit",
    "India v NZ, 1st Test day 5: NZ 157/4",
    "Selangor flood evacuees pass 1,800",
    "Sindarov takes White in FIDE game 1",
    "Bayelsa boat toll rises to 29",
    "Kenya, DR Congo restore ties",
    "US consortium wins $60bn Kenya mining deal",
    "Colombia asks X to suspend Petro",
    "OpenAI scientist urges common AI limits",
    "Anthropic shares slide after record IPO",
]

ALSO_SRC = [
    "FeedCast", "FeedCast", "DailyMattr", "FeedCast", "BBC", "TALi", "BBC",
    "One Turn", "One Turn", "Daily News Egypt", "The Hindu", "The Hindu",
    "Rediff", "TALi", "Chess", "Channels TV", "Radio Generation", "BBC",
    "One Turn", "DailyMattr", "FeedCast",
]

# (number, label, lat, lon, badge offset dx, dy)
PINS = [
    (1, "Antalya - COP31", 36.9, 30.7, 14, 14),
    (2, "Hormuz - tankers hit", 26.5, 56.3, 0, 0),
    (3, "Washington - House 258", 38.9, -77.0, 0, 0),
    (4, "Kyiv - Ukraine war", 50.4, 30.5, 0, 0),
    (5, "Benghazi - warship hit", 32.1, 20.1, 0, 0),
    (6, "Vanuatu - M6.5 quake", -13.6, 172.3, 0, 0),
    (7, "Seoul - KOSPI -5%", 37.6, 127.0, 0, 0),
    (8, "New Delhi - India", 28.6, 77.2, 0, 0),
    (9, "Nairobi - Kenya", -1.3, 36.8, 0, 0),
    (10, "Sinaloa - cartel boss", 24.8, -107.4, 0, 0),
    (11, "Brasilia - Bolsonaro", -15.8, -47.9, 0, 0),
    (12, "London - UK", 51.5, -0.1, 0, 0),
]

KEY = [
    "1 Antalya - COP31", "2 Hormuz - tankers hit",
    "3 Washington - House 258", "4 Kyiv - Ukraine war",
    "5 Benghazi - warship hit", "6 Vanuatu - M6.5 quake",
    "7 Seoul - KOSPI -5%", "8 New Delhi - India",
    "9 Nairobi - Kenya", "10 Sinaloa - cartel boss",
    "11 Brasilia - Bolsonaro", "12 London - UK",
]

# Simplified continent outlines as (lon, lat) points, hand-drawn.
CONTINENTS = [
    # North America
    [(-168, 66), (-165, 60), (-158, 58), (-152, 60), (-140, 60), (-135, 58),
     (-130, 54), (-125, 49), (-124, 42), (-120, 34), (-114, 29), (-110, 24),
     (-105, 20), (-97, 16), (-94, 17), (-90, 14), (-83, 9), (-79, 9),
     (-81, 13), (-84, 16), (-87, 13), (-90, 14), (-92, 15), (-94, 17),
     (-97, 26), (-93, 30), (-89, 30), (-84, 30), (-81, 26), (-80, 32),
     (-76, 35), (-74, 40), (-70, 42), (-68, 45), (-65, 44), (-60, 47),
     (-55, 47), (-60, 52), (-64, 58), (-68, 58), (-72, 62), (-78, 62),
     (-85, 66), (-92, 66), (-95, 69), (-110, 68), (-125, 70), (-140, 70),
     (-155, 71), (-165, 68), (-168, 66)],
    # Greenland
    [(-58, 64), (-52, 60), (-44, 60), (-40, 64), (-32, 68), (-25, 70),
     (-20, 72), (-22, 76), (-30, 80), (-40, 78), (-50, 74), (-58, 70),
     (-58, 64)],
    # South America
    [(-79, 9), (-77, 4), (-80, -3), (-81, -6), (-77, -12), (-72, -18),
     (-70, -23), (-70, -30), (-72, -37), (-73, -44), (-74, -50), (-70, -54),
     (-66, -55), (-65, -45), (-62, -41), (-58, -34), (-52, -32), (-48, -28),
     (-41, -23), (-39, -17), (-35, -9), (-35, -6), (-40, -3), (-44, -2),
     (-50, 0), (-53, 4), (-58, 6), (-62, 9), (-68, 11), (-72, 12),
     (-76, 10), (-79, 9)],
    # Africa
    [(-6, 35), (-10, 31), (-15, 27), (-17, 21), (-17, 15), (-15, 11),
     (-12, 8), (-8, 5), (-4, 5), (0, 6), (6, 4), (9, 4), (9, 0),
     (12, -5), (13, -10), (12, -17), (14, -22), (16, -28), (19, -34),
     (26, -34), (32, -29), (35, -24), (36, -18), (40, -15), (40, -10),
     (42, -4), (46, 0), (51, 2), (51, 11), (48, 11), (43, 12), (40, 15),
     (38, 18), (37, 22), (34, 27), (32, 31), (30, 31), (22, 33), (19, 33),
     (11, 34), (10, 37), (0, 36), (-6, 35)],
    # Madagascar
    [(44, -16), (47, -15), (50, -16), (49, -20), (47, -24), (44, -25),
     (43, -21), (44, -16)],
    # Eurasia
    [(-10, 36), (-9, 38), (-9, 43), (-2, 44), (-1, 46), (-4, 48),
     (-2, 49), (0, 50), (3, 51), (5, 53), (8, 55), (8, 57), (10, 58),
     (12, 56), (18, 56), (21, 55), (24, 58), (24, 60), (21, 62), (18, 64),
     (15, 66), (12, 68), (18, 70), (25, 71), (30, 70), (35, 68), (40, 68),
     (45, 68), (50, 69), (55, 68), (60, 69), (65, 69), (70, 70), (75, 72),
     (80, 73), (85, 74), (90, 75), (95, 76), (100, 77), (105, 77),
     (110, 76), (115, 73), (120, 73), (125, 72), (130, 72), (135, 71),
     (140, 72), (145, 72), (150, 70), (155, 69), (160, 69), (162, 66),
     (160, 62), (158, 58), (156, 52), (150, 59), (142, 59), (142, 53),
     (140, 45), (138, 40), (135, 35), (132, 33), (130, 32), (127, 35),
     (126, 38), (127, 40), (130, 42), (132, 43), (135, 44), (138, 46),
     (140, 50), (142, 53), (142, 59), (144, 60), (150, 60), (156, 51),
     (156, 50), (150, 45), (146, 42), (142, 40), (140, 38), (138, 36),
     (136, 34), (134, 33), (132, 31), (130, 30), (128, 28), (126, 25),
     (124, 22), (122, 20), (120, 18), (118, 15), (116, 12), (114, 10),
     (112, 8), (110, 6), (108, 4), (106, 2), (104, 1), (102, 2),
     (100, 5), (98, 8), (97, 12), (95, 15), (93, 18), (91, 21),
     (89, 22), (87, 21), (85, 19), (82, 16), (80, 13), (78, 8),
     (77, 8), (75, 10), (73, 14), (72, 19), (70, 21), (68, 22),
     (66, 25), (64, 25), (62, 25), (60, 25), (58, 25), (57, 26),
     (56, 27), (54, 26), (52, 25), (50, 26), (48, 27), (48, 29),
     (50, 29), (52, 27), (54, 26), (56, 26), (57, 25), (59, 22),
     (59, 20), (57, 18), (55, 17), (53, 16), (51, 14), (49, 13),
     (47, 12), (45, 12), (43, 12), (42, 14), (40, 15), (39, 18),
     (38, 20), (37, 22), (36, 25), (35, 28), (34, 29), (33, 31),
     (32, 31), (30, 31), (28, 32), (26, 33), (24, 33), (22, 33),
     (20, 34), (18, 35), (16, 36), (14, 36), (12, 37), (10, 37),
     (8, 37), (6, 36), (4, 36), (2, 36), (0, 36), (-2, 35), (-5, 35),
     (-6, 34), (-8, 34), (-10, 36)],
    # United Kingdom
    [(-5, 50), (-3, 53), (-5, 56), (-3, 58), (-1, 57), (0, 53), (1, 51),
     (-3, 50), (-5, 50)],
    # Iceland
    [(-22, 64), (-18, 63), (-14, 64), (-15, 66), (-20, 66), (-24, 65),
     (-22, 64)],
    # Japan
    [(130, 31), (132, 33), (134, 34), (137, 35), (139, 35), (140, 37),
     (141, 39), (141, 41), (142, 43), (144, 44), (143, 42), (141, 40),
     (140, 38), (139, 36), (137, 34), (135, 34), (133, 34), (131, 32),
     (130, 31)],
    # Sri Lanka
    [(80, 6), (81, 8), (80, 9), (79, 7), (80, 6)],
    # Taiwan
    [(120, 22), (121, 25), (120, 24), (120, 22)],
    # Philippines
    [(120, 18), (122, 18), (122, 14), (121, 11), (123, 10), (122, 13),
     (120, 16), (120, 18)],
    # Borneo
    [(109, 0), (111, -2), (114, -3), (117, -2), (119, 0), (117, 2),
     (114, 3), (110, 2), (109, 0)],
    # Sumatra
    [(95, 5), (98, 3), (101, 0), (104, -3), (106, -6), (104, -5),
     (100, -1), (97, 3), (95, 5)],
    # Java
    [(105, -6), (108, -7), (112, -7), (114, -8), (110, -8), (106, -7),
     (105, -6)],
    # New Guinea
    [(131, -1), (134, -3), (138, -5), (141, -6), (146, -8), (150, -9),
     (147, -9), (142, -8), (138, -7), (134, -4), (131, -1)],
    # Sulawesi
    [(119, 0), (121, -1), (123, 0), (121, 1), (119, 0)],
    # Australia
    [(113, -22), (114, -30), (115, -35), (120, -34), (124, -33), (129, -32),
     (132, -32), (135, -35), (138, -35), (140, -38), (145, -38), (150, -37),
     (153, -32), (153, -27), (150, -23), (146, -19), (142, -15), (142, -11),
     (137, -12), (135, -15), (132, -12), (130, -13), (126, -14), (122, -17),
     (118, -20), (113, -22)],
    # New Zealand
    [(167, -45), (170, -43), (173, -41), (175, -38), (177, -38), (175, -40),
     (173, -42), (170, -44), (167, -45)],
    [(174, -37), (176, -38), (178, -38), (176, -40), (174, -41), (173, -39),
     (174, -37)],
]


# ---------------------------------------------------------------- layout
M = 28  # side margin
CW = 968  # content width


def draw_masthead(d):
    d.text((M, 16), "ONE DAY", font=font(SERIF_B, 58), fill=INK)
    right = W - M
    f1 = font(SANS_B, 21)
    f2 = font(SANS, 14)
    t1 = "MONDAY 23 NOVEMBER 2026"
    t2 = "THE WORLD IN ONE IMAGE"
    d.text((right - d.textlength(t1, font=f1), 22), t1, font=f1, fill=INK)
    d.text((right - d.textlength(t2, font=f2), 52), t2, font=f2, fill=GREY)
    d.line([(M, 96), (W - M, 96)], fill=INK, width=3)
    d.line([(M, 101), (W - M, 101)], fill=INK, width=1)


def draw_stats(d):
    cells = [
        ("36", "STORIES"),
        ("7", "REGIONS"),
        ("258", "HOUSE SEATS"),
        ("M6.5", "VANUATU QUAKE"),
    ]
    x0, y0, cw, ch = M, 110, 239, 30
    for i, (big, small) in enumerate(cells):
        x = x0 + i * (cw + 4)
        d.rectangle([x, y0, x + cw, y0 + ch], outline=LIGHT_LINE, width=1)
        fb = font(SANS_B, 17)
        fs = font(SANS, 12)
        bw = d.textlength(big, font=fb)
        sw = d.textlength(small, font=fs)
        d.text((x + 10, y0 + 6), big, font=fb, fill=RED)
        d.text((x + 16 + bw, y0 + 8), small, font=fs, fill=INK)


def draw_tabs(d):
    tabs = ("NORTH AMERICA", "EUROPE", "MIDDLE EAST", "ASIA-PACIFIC",
            "AFRICA", "LATIN AMERICA", "SCIENCE & TECH")
    fnt = font(SANS_B, 13)
    text = "  \u2022  ".join(tabs)
    tw = d.textlength(text, font=fnt)
    d.text(((W - tw) / 2, 148), text, font=fnt, fill=NAVY)


# ---------------------------------------------------------------- lead panels
def panel_frame(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], outline=INK, width=1)
    d.rectangle([x, y, x + w, y + h], outline=LIGHT_LINE, width=1)


def panel_text(d, x, y, w, headline, sub, source, accent):
    d.rectangle([x, y, x + w, y + 5], fill=accent)
    hf = fit_size(d, headline, SERIF_B, 25, w - 20)
    d.text((x + 10, y + 12), headline, font=hf, fill=INK)
    fsub = font(SANS, 14)
    lines = wrap(d, sub, fsub, w - 20)
    yy = y + 46
    for ln in lines[:3]:
        d.text((x + 10, yy), ln, font=fsub, fill=(60, 58, 52))
        yy += 18
    d.text((x + 10, y + 100 - 18), source, font=font(SANS_B, 11),
           fill=GREY)


def draw_cop31(d, x, y, w, h):
    # Conference hall: dark teal room, rows of desks, a cracked globe.
    d.rectangle([x, y, x + w, y + 150], fill=TEAL)
    d.rectangle([x, y + 118, x + w, y + 150], fill=(12, 62, 66))
    for row, yy in enumerate((y + 96, y + 112, y + 128)):
        for i in range(7):
            dx = x + 18 + i * 42
            d.rectangle([dx, yy, dx + 30, yy + 9], fill=(210, 200, 170))
            d.rectangle([dx + 12, yy - 8, dx + 18, yy], fill=(240, 235, 220))
    cx, cy, r = x + w // 2, y + 58, 34
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(240, 235, 220),
              outline=(240, 235, 220))
    d.arc([cx - r, cy - r, cx + r, cy + r], 200, 340, fill=TEAL, width=4)
    d.arc([cx - r, cy - r, cx + r, cy + r], 20, 160, fill=TEAL, width=4)
    d.line([(cx - 6, cy - r + 6), (cx + 4, cy - 8), (cx - 4, cy + 10),
            (cx + 8, cy + r - 8)], fill=RED, width=3)
    d.text((x + 10, y + 8), "ANTALYA, TURKEY", font=font(SANS_B, 12),
           fill=(240, 235, 220))
    # NO DEAL stamp
    stamp = "NO DEAL"
    sf = font(SANS_B, 20)
    sw = d.textlength(stamp, font=sf)
    sx, sy = x + w - sw - 22, y + 14
    d.rectangle([sx - 6, sy - 4, sx + sw + 6, sy + 24], outline=RED, width=2)
    d.text((sx, sy), stamp, font=sf, fill=RED)
    panel_text(d, x, y + 150, w,
               "COP31 COLLAPSES",
               "Talks end with no deal - longest COP ever, first "
               "breakdown since 2009.",
               "CNN \u00b7 Reuters \u00b7 Le Monde", RED)


def draw_hormuz(d, x, y, w, h):
    # Strait of Hormuz: sea, two shores, tanker, explosion.
    d.rectangle([x, y, x + w, y + 150], fill=(16, 64, 96))
    d.polygon([(x, y), (x + w, y), (x + w, y + 30), (x + 200, y + 48),
               (x + 120, y + 44), (x, y + 58)], fill=(214, 196, 150))
    d.polygon([(x, y + 150), (x + w, y + 150), (x + w, y + 118),
               (x + 210, y + 104), (x + 140, y + 112), (x, y + 124)],
              fill=(214, 196, 150))
    # tanker, riding in the channel
    tx, ty = x + 96, y + 72
    d.rectangle([tx, ty, tx + 120, ty + 16], fill=(20, 20, 20))
    d.rectangle([tx + 88, ty - 14, tx + 108, ty], fill=(240, 240, 240))
    d.rectangle([tx + 96, ty - 22, tx + 100, ty - 14], fill=(240, 240, 240))
    # explosion starburst
    ex, ey = x + 240, y + 80
    for ang in range(0, 360, 30):
        import math
        r1 = 26 if ang % 60 == 0 else 14
        a = math.radians(ang)
        d.line([(ex, ey), (ex + r1 * math.cos(a), ey + r1 * math.sin(a))],
               fill=(255, 176, 32), width=3)
    d.ellipse([ex - 9, ey - 9, ex + 9, ey + 9], fill=(255, 120, 32))
    d.text((x + 10, y + 8), "STRAIT OF HORMUZ", font=font(SANS_B, 12),
           fill=NAVY)
    panel_text(d, x, y + 150, w,
               "SINK THE TANKERS",
               "Trump warns Iranian vessels testing the US blockade "
               "will end at the bottom of the sea.",
               "Fox News \u00b7 UKMTO \u00b7 Indian Express", NAVY)


def draw_house(d, x, y, w, h):
    # US Capitol dome over a chamber: blue majority, red minority.
    d.rectangle([x, y, x + w, y + 150], fill=NAVY)
    cx = x + w // 2
    d.rectangle([cx - 2, y + 2, cx + 2, y + 10], fill=(240, 235, 220))
    d.pieslice([cx - 40, y + 8, cx + 40, y + 72], 180, 360,
               fill=(240, 235, 220))
    d.rectangle([cx - 40, y + 66, cx + 40, y + 76], fill=(240, 235, 220))
    d.rectangle([cx - 58, y + 76, cx + 58, y + 84], fill=(240, 235, 220))
    for i in range(6):
        d.rectangle([cx - 54 + i * 20, y + 84, cx - 42 + i * 20, y + 96],
                    fill=(240, 235, 220))
    d.rectangle([cx - 70, y + 96, cx + 70, y + 104], fill=(240, 235, 220))
    # chamber seats: 60% blue, 40% red
    for row in range(3):
        yy = y + 106 + row * 16
        for i in range(12):
            sx = x + 22 + i * 23
            col = (58, 120, 200) if (row * 12 + i) < 22 else (200, 70, 60)
            d.rectangle([sx, yy, sx + 16, yy + 12], fill=col)
    d.text((x + 10, y + 8), "WASHINGTON", font=font(SANS_B, 12),
           fill=(240, 235, 220))
    panel_text(d, x, y + 150, w,
               "DEMOCRATS TAKE THE HOUSE",
               "258 seats, largest since 1992 - Hubbard beats Foxx "
               "by 330 votes in NC recount.",
               "BBC \u00b7 AP \u00b7 CNN", NAVY)


def draw_leads(d):
    y, h, pw = 172, 250, 314
    draw_cop31(d, M, y, pw, h)
    draw_hormuz(d, M + pw + 13, y, pw, h)
    draw_house(d, M + 2 * (pw + 13), y, pw, h)


# ---------------------------------------------------------------- map
MAP_X, MAP_Y, MAP_W, MAP_H = M, 456, 672, 140
KEY_X = 712


def project(lon, lat):
    x = MAP_X + (lon + 180.0) / 360.0 * MAP_W
    y = MAP_Y + (78.0 - lat) / 134.0 * MAP_H
    return x, y


def draw_map(d):
    d.text((M, 432), "WHERE IT HAPPENED", font=font(SANS_B, 14), fill=INK)
    d.text((M + 168, 434), "12 pins - see key",
           font=font(SANS, 12), fill=GREY)
    d.rectangle([MAP_X, MAP_Y, MAP_X + MAP_W, MAP_Y + MAP_H],
                fill=SEA, outline=INK, width=1)
    for poly in CONTINENTS:
        pts = [project(lon, lat) for lon, lat in poly]
        d.polygon(pts, fill=LAND, outline=LAND_EDGE)
    for num, label, lat, lon, dx, dy in PINS:
        px, py = project(lon, lat)
        d.ellipse([px - 2, py - 2, px + 2, py + 2], fill=RED)
        bx, by = px + dx, py + dy
        if dx or dy:
            d.line([(px, py), (bx, by)], fill=RED, width=1)
        d.ellipse([bx - 8, by - 8, bx + 8, by + 8], fill=RED,
                  outline=(255, 255, 255), width=1)
        t = str(num)
        tw = d.textlength(t, font=font(SANS_B, 10))
        d.text((bx - tw / 2, by - 7), t, font=font(SANS_B, 10),
               fill=(255, 255, 255))
    # key, two columns of six
    fnt = font(SANS, 12)
    for i, item in enumerate(KEY):
        col = i // 6
        row = i % 6
        kx = KEY_X + col * 148
        ky = MAP_Y + 4 + row * 22
        d.text((kx, ky), item, font=fnt, fill=INK)


# ---------------------------------------------------------------- cards + also
def draw_cards(d):
    y0, h, pw = 608, 60, 314
    for i, (headline, source, sure) in enumerate(CARDS):
        col, row = i % 3, i // 3
        x = M + col * (pw + 13)
        y = y0 + row * 62
        d.rectangle([x, y, x + pw, y + h], fill=(251, 248, 239),
                    outline=LIGHT_LINE, width=1)
        # number badge
        d.ellipse([x + 8, y + 8, x + 34, y + 34], fill=RED)
        t = str(i + 1)
        tw = d.textlength(t, font=font(SANS_B, 13))
        d.text((x + 21 - tw / 2, y + 13), t, font=font(SANS_B, 13),
               fill=(255, 255, 255))
        hf = font(SERIF_B, 15)
        lines = wrap(d, headline, hf, pw - 48)
        yy = y + 6
        for ln in lines[:2]:
            d.text((x + 42, yy), ln, font=hf, fill=INK)
            yy += 19
        # sure dot + source
        dot_c = RED if sure == 2 else GREY
        d.ellipse([x + 42, y + h - 15, x + 48, y + h - 9], fill=dot_c)
        d.text((x + 52, y + h - 18), source, font=font(SANS_B, 11),
               fill=GREY)


def draw_also(d):
    d.text((M, 864), "ALSO", font=font(SANS_B, 13), fill=INK)
    legend = "HOW SURE:  ● 2+ outlets   ● one outlet"
    fl = font(SANS, 12)
    d.text((W - M - d.textlength(legend, font=fl), 864), legend,
           font=fl, fill=GREY)
    fnt = font(SANS, 11)
    for i, item in enumerate(ALSO):
        col, row = i % 3, i // 3
        x = M + col * (314 + 13)
        y = 880 + row * 12
        full = "\u2022 " + item + " - " + ALSO_SRC[i]
        txt = fit_text(d, full, fnt, 314)
        d.text((x, y), txt, font=fnt, fill=(60, 58, 52))


def draw_footer(d):
    d.line([(M, 968), (W - M, 968)], fill=INK, width=1)
    d.text((M, 974), "DATE CHECK - All 36 stories happened or were first "
           "reported on Monday 23 November 2026.",
           font=font(SANS_B, 13), fill=INK)
    src = ("Sources: BBC \u00b7 CNN \u00b7 Reuters \u00b7 AP \u00b7 The Hindu "
           "\u00b7 The Times \u00b7 Le Monde \u00b7 USGS \u00b7 UKMTO \u00b7 "
           "Indian Express \u00b7 Rediff \u00b7 TALi \u00b7 One Turn \u00b7 "
           "FeedCast \u00b7 DailyMattr \u00b7 Chess")
    d.text((M, 996), src, font=font(SANS, 11), fill=GREY)


def main():
    img = Image.new("RGB", (W, H), CREAM)
    d = ImageDraw.Draw(img)
    draw_masthead(d)
    draw_stats(d)
    draw_tabs(d)
    draw_leads(d)
    draw_map(d)
    draw_cards(d)
    draw_also(d)
    draw_footer(d)
    img.save(OUT, "PNG")
    print("wrote " + OUT)


if __name__ == "__main__":
    main()

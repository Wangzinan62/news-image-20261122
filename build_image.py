#!/usr/bin/env python3
"""Draw a broadsheet front page for 22 November 2026 world news.

Everything is drawn with PIL primitives: no generated imagery, so every
word stays crisp. Run with `python3 build_image.py` from this directory;
it writes entry.png next to this script.
"""
import textwrap
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (246, 241, 229)
INK = (22, 24, 29)
RED = (179, 49, 42)
NAVY = (36, 66, 92)
GREY = (110, 104, 90)
LIGHT_GREY = (210, 204, 188)
FONT_DIR = "/usr/share/fonts/truetype/noto/"


def font(name, size):
    return ImageFont.truetype(FONT_DIR + name, size)


SERIF_BLACK = lambda s: font("NotoSerif-Black.ttf", s)
SANS_BLACK = lambda s: font("NotoSans-Black.ttf", s)
SANS_BOLD = lambda s: font("NotoSans-Bold.ttf", s)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap measured with the real font."""
    words, lines, cur = text.split(), [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_wrapped(draw, x, y, text, fnt, max_w, fill, leading):
    lines = wrap(draw, text, fnt, max_w)
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def centred(draw, cx, y, text, fnt, fill):
    w = draw.textlength(text, font=fnt)
    draw.text((cx - w / 2, y), text, font=fnt, fill=fill)
    return y + fnt.size


img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)
MX = 36  # side margin
CW = W - 2 * MX  # content width

# ---- 1. Masthead -------------------------------------------------------
centred(d, W // 2, 26, "T H E   W O R L D   I N   O N E   P I C T U R E",
        SANS_BOLD(21), NAVY)
d.line([(MX, 62), (W - MX, 62)], fill=INK, width=3)
d.line([(MX, 68), (W - MX, 68)], fill=INK, width=1)

# ---- 2. Date, huge ------------------------------------------------------
centred(d, W // 2, 70, "SUNDAY", SERIF_BLACK(90), INK)
centred(d, W // 2, 162, "22 NOVEMBER 2026", SERIF_BLACK(54), INK)
d.line([(MX, 226), (W - MX, 226)], fill=RED, width=4)

# ---- 3. Lead story ------------------------------------------------------
ly = 240
d.text((MX, ly), "CLIMATE", font=SANS_BLACK(20), fill=RED)
ly += 26
headline = "CLIMATE TALKS COLLAPSE IN TURKEY"
lead_w = 640
ly = draw_wrapped(d, MX, ly, headline, SERIF_BLACK(42), lead_w, INK, 46)
ly += 8
deck = ("Nearly 200 nations leave the COP31 summit in Antalya without "
        "a deal, split over fossil fuels and climate finance.")
ly = draw_wrapped(d, MX, ly, deck, SANS_BOLD(19), lead_w, (60, 62, 68), 25)

# Lead illustration: stylised globe, red sun, smoke plumes (right side).
gx, gy = 700, 244  # globe box top-left, 180px across
d.ellipse([gx, gy, gx + 180, gy + 180], outline=NAVY, width=6)
d.ellipse([gx + 12, gy + 12, gx + 168, gy + 168], fill=(214, 228, 236))
d.arc([gx + 12, gy + 12, gx + 168, gy + 168], 200, 340, fill=NAVY, width=4)
d.arc([gx + 34, gy + 52, gx + 146, gy + 128], 0, 360, fill=NAVY, width=3)
d.line([(gx + 12, gy + 90), (gx + 168, gy + 90)], fill=NAVY, width=3)
# red sun above the globe
d.ellipse([gx + 128, gy - 4, gx + 168, gy + 36], fill=RED)
# smoke plumes rising from the globe
for cx, cy, r in [(gx + 26, gy + 162, 14), (gx + 50, gy + 144, 17),
                  (gx + 79, gy + 161, 12)]:
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=GREY)
d.line([(MX, 432), (W - MX, 432)], fill=INK, width=2)

# ---- 4. Five small panels ----------------------------------------------
panels = [
    ("WAR AT SEA",
     "BLAST HITS RUSSIAN SHIP IN LIBYA",
     "Libya's eastern government says a preliminary probe points to a "
     "drone attack on a vessel docked at Benghazi.",
     "ship"),
    ("MIDDLE EAST",
     "IRAN STRIKES TANKERS NEAR HORMUZ",
     "Tankers hit and set ablaze as Bahrain reports an Iranian attack "
     "on a plant in Sitra; the US-Iran blockade standoff deepens.",
     "flame"),
    ("MARKETS",
     "AI ROUT DEEPENS AS NVIDIA TUMBLES",
     "The Nasdaq fell 5.3% on Friday in its worst week since 2020; "
     "Nvidia slid 14% in a day as China eased margin rules to steady markets.",
     "chart"),
    ("SPORT",
     "ALCARAZ WINS FIRST ATP FINALS",
     "The Spaniard beats world No. 1 Zverev 6-2, 7-6(7) in Turin for "
     "his 14th straight win.",
     "ball"),
    ("FOOTBALL",
     "LIVERPOOL ROUT UNITED 4-0",
     "Pochettino's first match in charge ends in a nightmare debut at "
     "Anfield as United sink into the relegation zone.",
     "goal"),
]

COL_W = (CW - 16) // 2
ROW_H = 156
TOP = 446


def draw_icon(x, y, kind):
    """Small 44x44 PIL icon in the panel's top-right corner."""
    s = 44
    if kind == "ship":
        d.polygon([(x, y + 30), (x + s, y + 30), (x + s - 8, y + 42),
                   (x + 8, y + 42)], fill=NAVY)
        d.rectangle([x + 16, y + 8, x + 20, y + 30], fill=NAVY)
        d.polygon([(x + 20, y + 8), (x + 34, y + 18), (x + 20, y + 18)],
                  fill=RED)
    elif kind == "flame":
        d.polygon([(x + 22, y + 2), (x + 38, y + 24), (x + 30, y + 24),
                   (x + 36, y + 34), (x + 22, y + 44), (x + 8, y + 34),
                   (x + 14, y + 24), (x + 6, y + 24)], fill=RED)
    elif kind == "chart":
        d.line([(x + 4, y + 36), (x + 16, y + 22), (x + 26, y + 28),
                (x + 40, y + 8)], fill=RED, width=4)
        d.polygon([(x + 40, y + 8), (x + 32, y + 8), (x + 40, y + 16)],
                  fill=RED)
    elif kind == "ball":
        d.ellipse([x + 2, y + 2, x + 42, y + 42], outline=NAVY, width=3)
        d.arc([x + 2, y + 2, x + 42, y + 42], 20, 160, fill=NAVY, width=2)
        d.arc([x + 2, y + 2, x + 42, y + 42], 200, 340, fill=NAVY, width=2)
    elif kind == "goal":
        d.rectangle([x + 2, y + 6, x + 42, y + 38], outline=NAVY, width=3)
        for vx in (12, 22, 32):
            d.line([(x + vx, y + 6), (x + vx, y + 38)], fill=LIGHT_GREY,
                   width=1)
        for hy in (17, 28):
            d.line([(x + 2, y + hy), (x + 42, y + hy)], fill=LIGHT_GREY,
                   width=1)
        d.ellipse([x + 16, y + 16, x + 28, y + 28], fill=RED)


for i, (kicker, head, deck, icon) in enumerate(panels):
    row, col = divmod(i, 2)
    # last panel spans the full width
    if i == 4:
        px, pw = MX, CW
    else:
        px = MX + col * (COL_W + 16)
        pw = COL_W
    py = TOP + row * (ROW_H + 8)
    # divider above each row
    if col == 0:
        d.line([(MX, py - 6), (W - MX, py - 6)], fill=LIGHT_GREY, width=1)
    d.text((px, py), kicker, font=SANS_BLACK(16), fill=RED)
    draw_icon(px + pw - 46, py, icon)
    hy = py + 22
    hy = draw_wrapped(d, px, hy, head, SANS_BLACK(34), pw - 56, INK, 36)
    draw_wrapped(d, px, py + 98, deck, SANS_BOLD(15), pw - 8,
                 (60, 62, 68), 18)

# ---- 5. Bottom ticker ---------------------------------------------------
ty = 940
d.rectangle([0, ty, W, H], fill=INK)
ticker = ("ALSO TODAY  ·  Russian strike hits Kyiv apartment block, "
          "3 killed  ·  Indonesia candy factory fire leaves 3 dead, "
          "37 unaccounted for  ·  Cartel leader captured in Mexico; "
          "11 dead in firefight")
ty2 = ty + 10
draw_wrapped(d, MX, ty2, ticker, SANS_BOLD(17), CW, PAPER, 24)

img.save("entry.png", optimize=True)
print("entry.png written")

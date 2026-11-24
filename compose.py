#!/usr/bin/env python3
"""THE MONDAY HERALD — NI23 G4 akun13 compose (local only, PIL ok).

Front page for Monday 23 November 2026: lead card spans two columns,
ten mini cards in a 4-wide grid, a DAY IN NUMBERS box closing the grid,
a dotted world map with numbered pins, a red DATE CHECK box and an
ALSO ON briefs block. Usage: python3 compose.py entry.png
"""
import math
from PIL import Image, ImageDraw, ImageFont

FD = "/home/hatch/workspace/tools/bedah-19nov/news-image/fonts/"
W = H = 1024
CREAM = (247, 240, 220); CREAM2 = (251, 247, 235)
INK = (35, 35, 35); BLUE = (0, 45, 140)
RED = (178, 34, 34); GREY = (110, 104, 92); WHITE = (255, 255, 255)
GOLD = (255, 210, 90)
REGIONS = {"EUROPE": (0, 45, 140), "MIDDLE EAST": (178, 90, 20),
           "SOUTH ASIA": (20, 120, 70), "NORTH AMERICA": (140, 30, 90),
           "SE ASIA": (0, 130, 140), "AFRICA": (190, 140, 0), "GLOBAL": (90, 90, 90)}
MAP_LEGEND = "Dotted world map: numbered pins mark the numbered stories of the day"

def fb(n):  # headline font
    return ImageFont.truetype(FD + "PlayfairDisplay-Bold.ttf", n)

def fr(n):  # deck / body font
    return ImageFont.truetype(FD + "Archivo.ttf", n)

def fsr(n):  # brief font
    return ImageFont.truetype(FD + "Archivo.ttf", n)

def fab(n):
    return ImageFont.truetype(FD + "Archivo-Bold.ttf", n)

# (value, label) — labels name the card each number belongs to
NUMS = [
    ("258-173", "Democrats House majority confirmed, card 9"),
    ("720", "India record Test total at Wellington, card 8"),
    ("14", "people missing after the Kyiv strike, card 6"),
    ("$3,538", "gold per ounce after the slide, card 10"),
    ("28,000", "Tata Steel pipe unit sale in crore, brief 30"),
    ("65.9", "IndiGo domestic market share, brief 31"),
]

TL = [("00:02Z", "UN AI talks go on"), ("02:00Z", "Albanese on COP31"),
      ("06:10Z", "Tankers burn, Hormuz"), ("09:40Z", "ICJ on Myanmar"),
      ("12:20Z", "House 258-173 set"), ("15:05Z", "Alcaraz wins"),
      ("18:30Z", "Gold $3,538")]

BRIEFS = [
    "Houthi missile on western Saudi Arabia intercepted by the coalition",
    "UN nations agree to keep negotiating lethal AI weapons rules",
    "US declassifies more UFO footage filmed over the Middle East",
    "Albanese says COP31 failure shows a difficult geopolitical era",
    "Russia-bound ship towed after attack in the Gulf of Finland",
    "UK-EU Brexit reset deal called a landmark by Burnham in Parliament",
    "Thousands march in Lisbon as the cost of living fuels anger",
    "Myanmar junta calls the ASEAN decision unfair and unbalanced",
    "Nepal PM Balendra Shah holds bilateral talks with PM Modi in Delhi",
    "Guru Nanak Jayanti marked under Sewa, Simran aur Sangat theme",
    "Indonesia fire update: 7 bodies found, 50 still missing",
    "Day 5 at Wellington: India chase a famous Test win, NZ 119/2",
    "India win the ODI series in New Zealand 3-2, Phillips player of series",
    "Anupama retains the IBSF world women's snooker title",
    "World Chess Championship captivates fans across the globe",
    "Kota pilgrim bus tragedy in Rajasthan leaves 9 dead",
    "Tata Steel sells its steel pipe unit for Rs 28,000 crore",
    "SpiceJet pilots seek an urgent audit; IndiGo holds 65.9% at home",
    "IFFI 2026 hosts a BRICS roundtable in Goa",
    "Modi opens an AI centre at IIT Patna with Rs 400 crore projects",
    "JEE Main 2027 session 1 registration closes today",
    "Google invests $5 million in AI research at IIT Kharagpur",
    "India-EU free trade pact likely signed 16 December in Brussels",
    "Trump criticises Schumer amid the Democrats leadership push",
    "FBI probes a suspected hack of its criminal justice database",
    "Miley Cyrus marries Maxx Morando in California",
    "Swimmer crosses the Strait of Hormuz to spotlight wildlife",
]

dc = ("Xi-Trump-Putin trilateral summit - 19 Nov 2026 · "
      "Russian missiles and drones in Poland - incident 20 Nov 2026 · "
      "Paolo Bulgari death - reported 22 Nov 2026 · "
      "24 civilians killed in South Sudan - Juba, 22 Nov 2026 · "
      "Ukraine strike on Kerch Bridge - reported 22 Nov 2026 · "
      "South Korea education minister quits - first reported 22 Nov 2026 · "
      "Indonesia candy-factory fire itself - 22 Nov 2026, only its 23 Nov update counts")

PINS = [(1, 0.50, 0.24), (2, 0.60, 0.38), (3, 0.585, 0.36), (4, 0.545, 0.33),
        (5, 0.565, 0.22), (6, 0.575, 0.21), (7, 0.53, 0.16), (8, 0.90, 0.78),
        (9, 0.13, 0.28), (10, 0.68, 0.42), (11, 0.545, 0.20), (12, 0.17, 0.30),
        (13, 0.545, 0.44)]

def wrap(d, text, font, maxw):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=font) <= maxw:
            cur = t
        else:
            if cur: lines.append(cur)
            cur = w
    if cur: lines.append(cur)
    return lines

def icon(d, kind, x, y, s):
    if kind == "tennis":
        d.ellipse([x+3, y+3, x+s-3, y+s-3], outline=BLUE, width=3)
        d.arc([x+3, y+3, x+s-3, y+s-3], 20, 160, fill=BLUE, width=2)
        d.arc([x+3, y+3, x+s-3, y+s-3], 200, 340, fill=BLUE, width=2)
    elif kind in ("tanker", "shipfire"):
        d.polygon([(x+2, y+s*0.55), (x+s-2, y+s*0.55), (x+s*0.8, y+s-3), (x+s*0.2, y+s-3)], fill=INK)
        d.rectangle([x+s*0.3, y+s*0.35, x+s*0.7, y+s*0.55], fill=BLUE)
        d.polygon([(x+s*0.5, y+2), (x+s*0.38, y+s*0.35), (x+s*0.62, y+s*0.35)], fill=RED)
    elif kind == "radar":
        d.line([x+s*0.5, y+s-3, x+s*0.5, y+s*0.4], fill=INK, width=3)
        d.arc([x+s*0.15, y+2, x+s*0.85, y+s*0.7], 180, 360, fill=BLUE, width=3)
    elif kind == "globe":
        d.ellipse([x+4, y+2, x+s-4, y+s-2], outline=(20, 120, 70), width=3)
        d.line([x+s/2, y+2, x+s/2, y+s-2], fill=(20, 120, 70), width=2)
        d.line([x+4, y+s/2, x+s-4, y+s/2], fill=(20, 120, 70), width=2)
    elif kind in ("rubble", "building"):
        d.rectangle([x+s*0.2, y+s*0.25, x+s*0.8, y+s-3], outline=INK, width=3)
        for i in range(3):
            d.rectangle([x+s*0.32+i*s*0.18, y+s*0.4, x+s*0.42+i*s*0.18, y+s*0.52], fill=BLUE)
        if kind == "rubble":
            d.line([x+s*0.2, y+s*0.25, x+s*0.8, y+s-3], fill=RED, width=3)
    elif kind == "cricket":
        d.rectangle([x+s*0.44, y+3, x+s*0.52, y+s*0.6], fill=(150, 100, 40))
        d.line([x+s*0.48, y+s*0.6, x+s*0.3, y+s-3], fill=INK, width=3)
        d.line([x+s*0.48, y+s*0.6, x+s*0.66, y+s-3], fill=INK, width=3)
        d.ellipse([x+s*0.62, y+5, x+s*0.8, y+5+s*0.18], fill=RED)
    elif kind == "capitol":
        d.polygon([(x+s*0.5, y+2), (x+s*0.25, y+s*0.35), (x+s*0.75, y+s*0.35)], fill=BLUE)
        for i in range(4):
            d.rectangle([x+s*0.18+i*s*0.17, y+s*0.4, x+s*0.26+i*s*0.17, y+s*0.8], fill=INK)
        d.rectangle([x+3, y+s*0.82, x+s-3, y+s-3], fill=INK)
    elif kind == "gold":
        d.polygon([(x+s*0.2, y+s*0.6), (x+s*0.8, y+s*0.6), (x+s*0.7, y+s*0.85), (x+s*0.3, y+s*0.85)], fill=(200, 160, 20))
        d.polygon([(x+s*0.3, y+s*0.3), (x+s*0.7, y+s*0.3), (x+s*0.8, y+s*0.6), (x+s*0.2, y+s*0.6)], fill=(225, 185, 40))
    elif kind == "gavel":
        d.line([x+s*0.25, y+s*0.75, x+s*0.7, y+s*0.3], fill=INK, width=4)
        d.rectangle([x+s*0.55, y+s*0.12, x+s*0.85, y+s*0.32], fill=(120, 70, 20))
        d.rectangle([x+s*0.15, y+s*0.85, x+s*0.6, y+s*0.93], fill=INK)
    elif kind == "blast":
        cx, cy = x+s/2, y+s/2
        for a in range(0, 360, 45):
            d.line([cx, cy, cx+s*0.42*math.cos(a*math.pi/180), cy+s*0.42*math.sin(a*math.pi/180)], fill=RED, width=3)
        d.ellipse([cx-4, cy-4, cx+4, cy+4], fill=(255, 140, 0))

def lead(d, x, y, w, h, num, region, src, head, deck, kind, status, cat):
    d.rectangle([x, y, x+w, y+h], fill=CREAM2, outline=INK, width=2)
    d.rectangle([x, y, x+w, y+17], fill=REGIONS[region])
    d.text((x+5, y+2), f"#{num}", font=fab(12), fill=WHITE)
    d.text((x+w-5, y+2), src, font=fab(12), fill=WHITE, anchor="ra")
    icon(d, kind, x+5, y+21, 26)
    chipw = d.textlength(status, font=fab(11)) + 10
    col = BLUE if status in ("REPORTED", "OFFICIAL") else (RED if status == "CLAIM" else (120, 80, 0))
    d.rectangle([x+36, y+23, x+36+chipw, y+39], fill=col)
    d.text((x+41, y+25), status, font=fab(11), fill=WHITE)
    d.text((x+42+chipw, y+25), cat, font=fab(10), fill=GREY)
    tf = fb(29)
    lines = wrap(d, head, tf, w-12)[:3]
    ty = y + 50
    for ln in lines:
        d.text((x+6, ty), ln, font=tf, fill=INK); ty += 30
    ff = fr(14)
    for ln in wrap(d, deck, ff, w-12)[:2]:
        d.text((x+6, ty+1), ln, font=ff, fill=(60, 58, 50)); ty += 16

def mini(d, x, y, w, h, num, region, src, head, deck, kind, status, cat):
    d.rectangle([x, y, x+w, y+h], fill=CREAM2, outline=INK, width=2)
    d.rectangle([x, y, x+w, y+17], fill=REGIONS[region])
    d.text((x+5, y+2), f"#{num}", font=fab(12), fill=WHITE)
    d.text((x+w-5, y+2), src, font=fab(12), fill=WHITE, anchor="ra")
    icon(d, kind, x+5, y+21, 26)
    chipw = d.textlength(status, font=fab(11)) + 10
    col = BLUE if status in ("REPORTED", "OFFICIAL") else (RED if status == "CLAIM" else (120, 80, 0))
    d.rectangle([x+36, y+23, x+36+chipw, y+39], fill=col)
    d.text((x+41, y+25), status, font=fab(11), fill=WHITE)
    d.text((x+42+chipw, y+25), cat, font=fab(10), fill=GREY)
    tf = fb(24)
    lines = wrap(d, head, tf, w-12)[:3]
    lh = 25
    if len(lines) > 2:
        tf = fb(22); lines = wrap(d, head, tf, w-12)[:3]; lh = 23
    ty = y + 50
    for ln in lines:
        d.text((x+6, ty), ln, font=tf, fill=INK); ty += lh
    ff = fr(13)
    for ln in wrap(d, deck, ff, w-12)[:2 if len(lines) <= 2 else 1]:
        d.text((x+6, ty+1), ln, font=ff, fill=(60, 58, 50)); ty += 16

def dotted_map(d, x, y, w, h):
    blobs = [(0.16, 0.30, 0.11, 0.16), (0.24, 0.62, 0.06, 0.13),
             (0.50, 0.26, 0.09, 0.10), (0.53, 0.55, 0.07, 0.14),
             (0.68, 0.30, 0.16, 0.13), (0.72, 0.52, 0.05, 0.08),
             (0.85, 0.68, 0.06, 0.07)]
    step = 8
    for gy in range(int(h/step)):
        for gx in range(int(w/step)):
            px, py = gx*step+4, gy*step+4
            rx, ry = px/w, py/h
            if any(((rx-cx)/brx)**2 + ((ry-cy)/bry)**2 < 1 for cx, cy, brx, bry in blobs):
                d.ellipse([x+px-2, y+py-2, x+px+2, y+py+2], fill=(170, 160, 135))
    for n, rx, ry in PINS:
        px, py = x+rx*w, y+ry*h
        d.ellipse([px-8, py-8, px+8, py+8], fill=BLUE)
        d.text((px, py-6), str(n), font=fab(10), fill=WHITE, anchor="ma")

def render(out):
    img = Image.new("RGB", (W, H), CREAM)
    d = ImageDraw.Draw(img)
    total = 13 + len(BRIEFS)
    counts = {"EUROPE": 10, "MIDDLE EAST": 4, "SOUTH ASIA": 13, "NORTH AMERICA": 6,
              "SE ASIA": 3, "AFRICA": 1, "GLOBAL": 3}
    d.rectangle([0, 0, W, 26], fill=INK)
    d.text((10, 5), "THE MONDAY HERALD", font=fab(14), fill=WHITE)
    kick = f"{total} STORIES · 7 REGIONS · EVERY ONE FROM 23 NOVEMBER 2026"
    d.text((W-10, 5), kick, font=fab(13), fill=GOLD, anchor="ra")
    d.text((512, 30), "Monday 23 November 2026",
           font=ImageFont.truetype(FD + "PlayfairDisplay-Black.ttf", 72), fill=INK, anchor="ma")
    d.text((512, 106), "THE MONDAY HERALD", font=fb(38), fill=BLUE, anchor="ma")
    d.text((512, 148), "Alcaraz's first ATP Finals crown · Tankers burn in Hormuz · COP31 ends with no deal",
           font=fab(16), fill=RED, anchor="ma")
    d.line([10, 164, W-10, 164], fill=INK, width=3)
    x = 10
    d.text((x, 170), "REGIONS:", font=fab(12), fill=INK); x += 66
    for r, col in REGIONS.items():
        label = f"{r} {counts.get(r, 0)}"
        tw = d.textlength(label, font=fab(12)) + 12
        d.rectangle([x, 168, x+tw, 186], fill=col)
        d.text((x+6, 171), label, font=fab(12), fill=WHITE)
        x += tw + 5
    d.rectangle([10, 190, W-10, 212], fill=(238, 230, 205), outline=INK, width=1)
    tx = 15
    d.text((tx, 195), "UTC DAY:", font=fab(11), fill=INK); tx += 58
    for t, ev in TL:
        s = f"{t} {ev}"
        d.text((tx, 195), s, font=fr(11), fill=(50, 48, 40))
        tx += d.textlength(s, font=fr(11)) + 12
    M, GAP = 10, 5
    cw = (W - 2*M - 3*GAP) // 4
    rh, gy = 136, 218
    lead(d, M, gy, cw*2+GAP, rh, 1, "EUROPE", "BBC Sport",
         "Alcaraz Beats Zverev for His First ATP Finals Title",
         "Carlos Alcaraz beat Alexander Zverev in Turin for his 1st ATP Finals crown.",
         "tennis", "REPORTED", "SPORT · TENNIS")
    mini(d, M+2*cw+2*GAP, gy, cw, rh, 2, "MIDDLE EAST", "AP live",
         "Tankers Burn in the Strait of Hormuz",
         "Tankers ablaze as the Iran-US war widened into the Gulf; the IRGC warned of unrest.",
         "tanker", "ONGOING", "GULF · WAR")
    mini(d, M+3*cw+3*GAP, gy, cw, rh, 3, "MIDDLE EAST", "AP / AFP",
         "IRGC Claims It Destroyed 2 Patriot Radars in Bahrain",
         "Tehran claims 2 Patriot radars destroyed at a US base in Bahrain; unconfirmed.",
         "radar", "CLAIM", "GULF · WAR")
    mini(d, M, gy+rh+GAP, cw, rh, 4, "EUROPE", "BBC / AP", "COP31 Ends Without a Deal in Antalya",
         "COP31 in Antalya, Turkiye: the final draft omitted fossil fuels; no deal was reached.",
         "globe", "OFFICIAL", "CLIMATE")
    mini(d, M+cw+GAP, gy+rh+GAP, cw, rh, 5, "EUROPE", "BBC", "Kyiv Boy, 7, Pulled Alive From the Rubble",
         "Rescuers freed the 7-year-old after hours in Kyiv rubble; 6 people were killed.",
         "rubble", "REPORTED", "WAR")
    mini(d, M+2*cw+2*GAP, gy+rh+GAP, cw, rh, 6, "EUROPE", "JagranJosh", "14 Missing After Kyiv Strike, Zelenskiy Says",
         "Zelenskiy says 14 are missing after a Russian drone hit a Kyiv region building.",
         "building", "ON RECORD", "WAR")
    mini(d, M+3*cw+3*GAP, gy+rh+GAP, cw, rh, 7, "EUROPE", "BBC", "Russian Cargo Ship Still Burns Off Finland",
         "The Russian cargo ship was still burning off Finland after an attack at sea.",
         "shipfire", "ONGOING", "SEA · WAR")
    mini(d, M, gy+2*rh+2*GAP, cw, rh, 8, "SOUTH ASIA", "ObserverVoice", "India Declare on a Record 720/9 at Wellington",
         "India posted 720 for 9 declared, a record Test total on New Zealand soil.",
         "cricket", "REPORTED", "SPORT · CRICKET")
    mini(d, M+cw+GAP, gy+2*rh+2*GAP, cw, rh, 9, "NORTH AMERICA", "BBC", "Democrats' House Majority Confirmed at 258-173",
         "The 258-173 majority, largest since 1992, was confirmed after North Carolina fell.",
         "capitol", "OFFICIAL", "POLITICS")
    mini(d, M+2*cw+2*GAP, gy+2*rh+2*GAP, cw, rh, 10, "GLOBAL", "ObserverVoice", "Gold Slides to $3,538 an Ounce",
         "Gold fell to $3,538 an ounce, over $2,000 below the 2026 record of $5,595.",
         "gold", "REPORTED", "MARKETS")
    mini(d, M+3*cw+3*GAP, gy+2*rh+2*GAP, cw, rh, 11, "SE ASIA", "Guardian / NYT", "ICJ Rules Myanmar Guilty of Genocide",
         "The ICJ ruled on the 2017 Rohingya campaign in Myanmar; 700,000 people fled.",
         "gavel", "OFFICIAL", "LAW · RIGHTS")
    yy = gy + 3*(rh+GAP)
    mini(d, M, yy, cw, rh, 12, "NORTH AMERICA", "BBC",
         "US Army to Detonate Unstable Explosives in Iowa",
         "The US Army will detonate tonnes of unstable explosives despite a court order in Iowa.",
         "blast", "REPORTED", "SECURITY")
    mini(d, M+cw+GAP, yy, cw, rh, 13, "AFRICA", "BBC",
         "Suspected Drone Strike Hits Ship at Benghazi",
         "An explosion hit a Russian ship in Benghazi port; a drone strike is suspected.",
         "blast", "CLAIM", "SEA · WAR")
    nx = M + 2*cw + 2*GAP; nw = cw*2 + GAP
    d.rectangle([nx, yy, nx+nw, yy+rh], fill=INK)
    d.text((nx+10, yy+6), "THE DAY IN NUMBERS", font=fab(15), fill=GOLD)
    ny = yy + 30
    for i in range(3):
        for j in range(2):
            val, lab = NUMS[i*2+j]
            xx = nx + 10 + j*(nw//2)
            d.text((xx, ny), val, font=fb(21), fill=WHITE)
            labln = wrap(d, lab, fr(10), nw//2 - 14)[0]
            d.text((xx, ny+24), labln, font=fr(10), fill=(220, 215, 195))
        ny += 36
    band_y = yy + rh + 6
    bh = 86
    d.rectangle([M, band_y, M+596, band_y+bh], outline=RED, width=3)
    d.text((M+8, band_y+5), "DATE CHECK - NOT 23 NOVEMBER NEWS:", font=fab(13), fill=RED)
    dy = band_y + 24
    for s in dc.split(" · "):
        d.text((M+8, dy), "· " + s, font=fr(11), fill=(90, 30, 30)); dy += 10
    mx = M + 602
    d.rectangle([mx, band_y, W-M, band_y+bh], fill=CREAM2, outline=INK, width=2)
    d.text((mx+8, band_y+4), "WHERE IT HAPPENED - pins mark the numbered stories", font=fab(11), fill=INK)
    dotted_map(d, mx+6, band_y+20, W-M-mx-12, bh-24)
    also_y = band_y + bh + 6
    d.line([M, also_y, W-M, also_y], fill=INK, width=2)
    d.text((M, also_y+3), "ALSO ON MONDAY:", font=fab(13), fill=BLUE)
    cols = 4; colw = (W - 2*M) // cols
    ay = also_y + 24
    per = (len(BRIEFS) + cols - 1) // cols
    for ci in range(cols):
        for ri, b in enumerate(BRIEFS[ci*per:(ci+1)*per]):
            s = f"#{14 + ci*per + ri} {b}"
            while d.textlength(s, font=fsr(12)) > colw - 6 and len(s) > 10:
                s = s[:-2]
            d.text((M + ci*colw, ay + ri*12), s, font=fsr(12), fill=(50, 48, 40))
    fy = H - 32
    d.rectangle([0, fy, W, H], fill=INK)
    d.text((10, fy+3), "HOW SURE: REPORTED = reported by named outlets · CLAIM = one side's account, labelled · ONGOING = still developing · OFFICIAL / ON RECORD = stated by officials.",
           font=fr(11), fill=WHITE)
    d.text((10, fy+18), "Every story happened, or was first reported, on Monday 23 November 2026. Contested claims are attributed. · Original drawings.",
           font=fr(11), fill=GOLD)
    img.save(out)
    print(out, img.size)

if __name__ == "__main__":
    import sys
    render(sys.argv[1] if len(sys.argv) > 1 else "entry.png")

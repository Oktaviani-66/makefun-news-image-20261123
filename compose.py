#!/usr/bin/env python3
"""THE DAILY MERIDIAN — composer akun13 (@oktaviascreamo0243), NI23 Gelombang 3.

Menggambar halaman depan koran satu halaman untuk Senin 23 November 2026
dengan PIL: masthead raksasa, strip angka, 14 kartu utama berilustrasi,
peta dunia titik-titik bernomor pin, timeline UTC, kolom ALSO ON sampai
40 cerita, dan kotak DATE CHECK merah. Alat lokal saja — program yang
disubmit adalah main.py (stdlib, copy-only).

Varian: A = putih gading / tinta marun / abu arang (palet akun).
        B = meja arang (latar gelap, teks gading).
        C = pita marun (masthead & strip angka di atas pita marun).
Pakai: python3 compose.py [A|B|C] [jalur-keluar.png]
"""

import os
import sys

from PIL import Image, ImageDraw, ImageFont

FD = "/home/hatch/workspace/tools/bedah-19nov/news-image/fonts/"
W = H = 1024


def fb(n):
    return ImageFont.truetype(FD + "PlayfairDisplay-Bold.ttf", n)


def fk(n):
    return ImageFont.truetype(FD + "PlayfairDisplay-Black.ttf", n)


def fi(n):
    return ImageFont.truetype(FD + "PlayfairDisplay-Italic.ttf", n)


def fr(n):
    return ImageFont.truetype(FD + "Archivo.ttf", n)


def fsr(n):
    return ImageFont.truetype(FD + "Archivo-Bold.ttf", n)


# ---------------------------------------------------------------- data ----
# Strip angka hari itu: (nilai, label) — semua mengikat kartu utama.
NUMS = [
    ("720/9d", "INDIA TEST RECORD, WELLINGTON"),
    ("258-173", "US HOUSE SEATS - DEMOCRATS WIN"),
    ("65.9%", "INDIGO DOMESTIC MARKET SHARE"),
    ("$3,538", "GOLD PRICE PER OUNCE, USD"),
    ("Rs 28,000 cr", "TATA STEEL PIPE UNIT SALE"),
    ("$95M", "EWING'S METS CONTRACT"),
]

# Timeline UTC hari itu.
TL = [
    ("00:02 UTC", "UN agrees to keep lethal-AI talks going"),
    ("02:00 UTC", "Sydney: Albanese reacts to COP31 failure"),
    ("Morning", "Kyiv rescuers free boy aged 7 from rubble"),
    ("Midday", "Wellington: India declare at 720 for 9"),
    ("Afternoon", "Washington: House called 258-173"),
    ("Evening", "Turin: Alcaraz lifts first ATP Finals title"),
]

# Kotak DATE CHECK: buangan bernama + bertanggal (BUKAN berita 23 Nov).
dc = (
    "Xi-Trump-Putin summit - 19 Nov 2026 · "
    "Missiles fell in Poland - 20 Nov 2026 · "
    "SpiceJet Rs 5,500cr raise - 18 Nov 2026 · "
    "Hyderabad bomb email - 21 Nov 2026 · "
    "Paolo Bulgari death - 22 Nov 2026 · "
    "Kim Jong-un, Seoul - 22 Nov 2026 · "
    "South Sudan: 24 dead - 22 Nov 2026 · "
    "Kerch Bridge strike - 22 Nov 2026"
)

# Kolom ALSO ON (cerita 15-40), satu baris per cerita.
BRIEFS_L = [
    "15. IRGC claims 2 Patriot radars hit in Bahrain",
    "16. Houthi missile intercepted over Saudi west",
    "17. UN states agree to keep AI-weapons talks on",
    "18. US declassifies more UFO footage, BBC says",
    "19. Albanese: COP31 failure shows hard times",
    "20. Russian cargo ship still ablaze off Finland",
    "21. Ship towed after attack in Gulf of Finland",
    "22. Blast hits Russian ship at Benghazi port",
    "23. Zelenskiy says 14 missing after Kyiv strike",
    "24. Burnham calls UK-EU reset deal a landmark",
    "25. Thousands march in Lisbon on living costs",
    "26. Myanmar junta slams ASEAN ruling as unfair",
    "27. Cameroon ex-rebels trapped by broken vows",
]

BRIEFS_R = [
    "28. Escaped lion spreads fear in a Turkiye town",
    "29. Nepal PM Shah in bilateral talks with Modi",
    "30. Guru Nanak Jayanti marked across India",
    "31. Day 5: India chase famous win, NZ 119/2",
    "32. India win ODI series in NZ 3-2, Phillips best",
    "33. Anupama defends IBSF snooker crown",
    "34. Rajya Sabha MP Wadkute dies in Delhi",
    "35. Kota pilgrim bus tragedy leaves 9 dead",
    "36. Modi opens AI centre at IIT Patna",
    "37. Google puts $5 million into IIT Kharagpur AI",
    "38. Trump attacks Schumer amid Democrat shuffle",
    "39. US Army to blast unstable explosives in Iowa",
    "40. FBI probes hack of criminal database",
]

# Pin peta: (nomor kartu, bujur, lintang) — skematik titik-titik.
PINS = [
    (1, 176, -42), (2, -86, 38), (3, 30, 41), (4, 32, 51),
    (5, 107, -6), (6, 96, 22), (7, 56, 27), (8, 0, 52),
    (9, 77, 29), (10, 89, 21), (11, 10, 44), (12, -118, 34),
    (13, 20, 54), (14, -73, 41),
]

REGION_COLORS = {
    "Middle East": (179, 84, 30),
    "Europe": (46, 90, 136),
    "North America": (62, 122, 78),
    "South Asia": (122, 62, 157),
    "South East Asia": (192, 122, 18),
    "Africa": (140, 106, 29),
    "Asia-Pacific": (31, 122, 109),
    "Global": (90, 84, 76),
}

# Kotak daratan skematik untuk peta titik: (bujur1, bujur2, lintang1, lintang2)
LAND = [
    (-168, -140, 58, 70), (-140, -118, 48, 70), (-125, -104, 31, 50),
    (-104, -84, 29, 50), (-95, -79, 44, 58), (-84, -68, 25, 47),
    (-79, -70, 37, 47), (-90, -79, 14, 22), (-104, -94, 17, 29),
    (-118, -107, 21, 32), (-55, -44, 59, 70), (-45, -29, 59, 76),
    (-80, -69, 4, 12), (-76, -59, -6, 4), (-70, -54, -16, -6),
    (-65, -54, -26, -16), (-70, -61, -36, -26), (-73, -67, -46, -36),
    (-73, -69, -54, -46),
    (-10, 1, 43, 50), (-6, 1, 50, 55), (-4, 2, 54, 59), (0, 11, 45, 52),
    (4, 16, 52, 58), (9, 21, 55, 61), (14, 26, 55, 65), (19, 31, 60, 70),
    (4, 13, 58, 64), (11, 21, 62, 69), (20, 29, 64, 70), (-1, 11, 42, 48),
    (9, 20, 42, 47), (19, 30, 40, 48), (-10, -1, 36, 44), (19, 29, 35, 42),
    (27, 41, 41, 48), (29, 46, 47, 55), (-3, 9, 43, 49), (21, 29, 37, 42),
    (-18, -9, 14, 28), (-10, 1, 27, 35), (0, 11, 29, 37), (10, 21, 29, 33),
    (20, 31, 27, 32), (30, 36, 27, 32), (-10, 1, 14, 25), (0, 11, 17, 28),
    (7, 19, 4, 15), (17, 29, 4, 15), (27, 36, -1, 12), (9, 21, -6, 4),
    (19, 31, -9, -1), (29, 41, -6, 4), (11, 21, -19, -9), (19, 29, -21, -11),
    (27, 36, -23, -13), (13, 21, -29, -21), (19, 29, -31, -23),
    (27, 34, -33, -27), (34, 43, -21, -11), (42, 51, -26, -16),
    (43, 50, -21, -11),
    (34, 46, 37, 43), (41, 51, 29, 38), (47, 57, 25, 31), (51, 61, 23, 29),
    (34, 43, 29, 38), (41, 49, 37, 46), (44, 61, 44, 56), (59, 76, 41, 53),
    (59, 71, 34, 43), (67, 79, 27, 37), (71, 81, 19, 29), (77, 89, 21, 31),
    (79, 91, 14, 23), (84, 96, 19, 29), (87, 93, 21, 27), (91, 99, 27, 35),
    (94, 106, 27, 41), (96, 106, 14, 23), (99, 109, 7, 19),
    (101, 109, 17, 25), (104, 113, 21, 31), (107, 119, 27, 37),
    (111, 123, 29, 41), (117, 127, 31, 43), (121, 131, 41, 51),
    (125, 136, 47, 57), (99, 116, 47, 59), (114, 136, 47, 59),
    (134, 156, 54, 66), (154, 176, 57, 67), (59, 91, 54, 69),
    (89, 121, 57, 71), (119, 151, 59, 71), (74, 91, 47, 57),
    (89, 106, 49, 59), (129, 138, 31, 38), (136, 142, 35, 41),
    (139, 145, 39, 45), (141, 146, 43, 47),
    (94, 104, -5, 5), (104, 115, -9, -5), (108, 119, -4, 5),
    (118, 126, -6, 2), (130, 142, -5, -1), (140, 151, -7, -2),
    (112, 123, -23, -13), (121, 133, -27, -19), (131, 143, -29, -21),
    (141, 151, -31, -23), (144, 151, -39, -31), (128, 138, -33, -27),
    (114, 121, -35, -31), (139, 147, -40, -35), (166, 174, -46, -42),
    (172, 179, -42, -37),
]

PALETTES = {
    "A": dict(bg=(246, 240, 223), panel=(252, 248, 238), ink=(38, 32, 26),
              sub=(92, 84, 72), maroon=(94, 18, 32), line=(176, 164, 140),
              band=False, soft=(238, 229, 205)),
    "B": dict(bg=(33, 30, 26), panel=(46, 41, 35), ink=(240, 232, 214),
              sub=(178, 168, 150), maroon=(206, 116, 78), line=(98, 90, 76),
              band=False, soft=(40, 36, 31)),
    "C": dict(bg=(250, 246, 236), panel=(255, 253, 247), ink=(40, 30, 28),
              sub=(100, 88, 76), maroon=(110, 20, 35), line=(190, 170, 150),
              band=True, soft=(243, 233, 214)),
}

PAL = PALETTES["A"]


# ------------------------------------------------------------- helpers ----
def wrap(d, text, font, maxw):
    words, lines, cur = text.split(), [], ""
    for wd in words:
        t = (cur + " " + wd).strip()
        if d.textlength(t, font=font) <= maxw or not cur:
            cur = t
        else:
            lines.append(cur)
            cur = wd
    if cur:
        lines.append(cur)
    return lines


def ctext(d, cx, y, text, font, fill):
    d.text((cx - d.textlength(text, font=font) / 2, y), text, font=font, fill=fill)


def fit_font(d, text, make, size, maxw):
    while size > 10 and d.textlength(text, font=make(size)) > maxw:
        size -= 2
    return make(size)


# ---------------------------------------------------------------- icons ---
def icon(d, kind, cx, cy, s, col, accent):
    """Ikon gambar-sendiri sederhana di kotak 2s x 2s sekitar (cx, cy)."""
    x0, y0, x1, y1 = cx - s, cy - s, cx + s, cy + s
    if kind == "cricket":
        d.line([x0 + 2, y1 - 2, x0 + 8, y0 + 4], fill=col, width=3)
        d.ellipse([x1 - 9, y0 + 2, x1 - 1, y0 + 10], outline=accent, width=2)
        for i in range(3):
            d.line([x1 - 8 + i * 4, y1 - 10, x1 - 8 + i * 4, y1 - 2], fill=col, width=2)
    elif kind == "ballot":
        d.rectangle([x0 + 2, cy, x1 - 2, y1 - 2], outline=col, width=2)
        d.rectangle([cx - 6, cy - 2, cx + 6, cy + 2], fill=col)
        d.polygon([cx - 5, y0 + 2, cx + 5, y0 + 2, cx + 3, cy - 3, cx - 3, cy - 3], outline=accent)
    elif kind == "globe":
        d.ellipse([x0 + 2, y0 + 2, x1 - 2, y1 - 2], outline=col, width=2)
        d.ellipse([cx - 4, y0 + 2, cx + 4, y1 - 2], outline=accent, width=1)
        d.line([x0 + 2, cy, x1 - 2, cy], fill=accent, width=1)
    elif kind == "rescue":
        d.polygon([x0 + 2, cy - 2, cx, y0 + 2, x1 - 2, cy - 2], outline=col)
        d.rectangle([x0 + 5, cy - 2, x1 - 5, y1 - 2], outline=col, width=2)
        d.line([cx, cy + 3, cx, cy + 9], fill=accent, width=3)
        d.line([cx - 3, cy + 6, cx + 3, cy + 6], fill=accent, width=3)
    elif kind == "flame":
        d.polygon([cx, y0 + 1, x1 - 4, cy + 4, cx + 3, y1 - 2, cx - 3, y1 - 2,
                   x0 + 4, cy + 4], outline=col)
        d.ellipse([cx - 3, cy + 2, cx + 3, y1 - 3], fill=accent)
    elif kind == "scales":
        d.line([cx, y0 + 4, cx, y1 - 3], fill=col, width=2)
        d.line([x0 + 2, y0 + 5, x1 - 2, y0 + 5], fill=col, width=2)
        for px in (x0 + 4, x1 - 8):
            d.line([px + 2, y0 + 5, px, y0 + 12], fill=accent, width=1)
            d.line([px + 2, y0 + 5, px + 4, y0 + 12], fill=accent, width=1)
            d.arc([px - 1, y0 + 10, px + 5, y0 + 16], 0, 180, fill=col, width=2)
        d.line([cx - 5, y1 - 2, cx + 5, y1 - 2], fill=col, width=2)
    elif kind == "ship":
        d.polygon([x0 + 1, cy + 3, x1 - 1, cy + 3, x1 - 5, y1 - 4, x0 + 5, y1 - 4], outline=col)
        d.line([cx, cy + 3, cx, y0 + 3], fill=col, width=2)
        d.polygon([cx, y0 + 3, cx + 7, cy + 2, cx, cy + 2], outline=accent)
        d.arc([x0, y1 - 5, cx, y1 + 3], 0, 180, fill=accent, width=1)
        d.arc([cx - 2, y1 - 5, x1, y1 + 3], 0, 180, fill=accent, width=1)
    elif kind == "gold":
        for i, yy in enumerate((cy + 4, cy - 2, cy - 8)):
            off = 0 if i != 1 else 5
            d.polygon([cx - 10 + off, yy + 5, cx - 6 + off, yy, cx + 6 + off, yy,
                       cx + 10 + off, yy + 5], outline=col)
    elif kind == "plane":
        d.polygon([cx, y0 + 2, cx + 4, cy + 4, x1 - 2, cy + 6, x1 - 2, cy + 9,
                   cx + 2, cy + 8, cx + 2, y1 - 2, cx - 2, y1 - 2, cx - 2, cy + 8,
                   x0 + 2, cy + 9, x0 + 2, cy + 6, cx - 4, cy + 4], outline=col)
    elif kind == "steel":
        d.rectangle([x0 + 3, y0 + 3, x1 - 3, y0 + 7], fill=col)
        d.rectangle([x0 + 3, y1 - 7, x1 - 3, y1 - 3], fill=col)
        d.rectangle([cx - 2, y0 + 3, cx + 2, y1 - 3], fill=accent)
    elif kind == "trophy":
        d.arc([cx - 8, y0 + 2, cx + 8, y0 + 20], 0, 180, fill=col, width=2)
        d.line([cx - 8, y0 + 6, cx - 8, y0 + 11], fill=col, width=2)
        d.line([cx + 8, y0 + 6, cx + 8, y0 + 11], fill=col, width=2)
        d.arc([cx - 13, y0 + 4, cx - 6, y0 + 12], 90, 270, fill=accent, width=2)
        d.arc([cx + 6, y0 + 4, cx + 13, y0 + 12], 270, 90, fill=accent, width=2)
        d.line([cx, y0 + 12, cx, y1 - 4], fill=col, width=2)
        d.line([cx - 6, y1 - 3, cx + 6, y1 - 3], fill=col, width=2)
    elif kind == "rings":
        d.ellipse([cx - 11, cy - 6, cx + 1, cy + 6], outline=col, width=2)
        d.ellipse([cx - 1, cy - 6, cx + 11, cy + 6], outline=accent, width=2)
    elif kind == "chess":
        d.ellipse([cx - 4, y0 + 2, cx + 4, y0 + 10], outline=col, width=2)
        d.polygon([cx - 3, y0 + 10, cx + 3, y0 + 10, cx + 6, y1 - 5, cx - 6, y1 - 5],
                  outline=col)
        d.rectangle([x0 + 3, y1 - 5, x1 - 3, y1 - 2], fill=accent)
    elif kind == "baseball":
        d.ellipse([x0 + 2, y0 + 2, x1 - 2, y1 - 2], outline=col, width=2)
        d.arc([x0 - 4, y0 + 2, cx, y1 - 2], 270, 90, fill=accent, width=1)
        d.arc([cx, y0 + 2, x1 + 4, y1 - 2], 90, 270, fill=accent, width=1)


# ------------------------------------------------------------------ map ---
def dotted_map(d, x, y, w, h):
    """Peta dunia titik-titik gambar-sendiri + pin bernomor kartu utama."""
    lon0, lon1, lat0, lat1 = -170.0, 185.0, 78.0, -58.0

    def px(lon):
        return x + (lon - lon0) / (lon1 - lon0) * w

    def py(lat):
        return y + (lat0 - lat) / (lat0 - lat1) * h

    gx = lon0
    while gx <= lon1:
        gy = lat0
        while gy >= lat1:
            if any(a <= gx <= b and c <= gy <= e for a, b, c, e in LAND):
                d.ellipse([px(gx) - 1.4, py(gy) - 1.4, px(gx) + 1.4, py(gy) + 1.4],
                          fill=PAL["sub"])
            gy -= 5.4
        gx += 4.5
    for num, lon, lat in PINS:
        cxp, cyp = px(lon), py(lat)
        d.ellipse([cxp - 7, cyp - 7, cxp + 7, cyp + 7], fill=(252, 248, 238),
                  outline=PAL["maroon"], width=2)
        t = str(num)
        f = fsr(10)
        d.text((cxp - d.textlength(t, font=f) / 2, cyp - 6), t, font=f,
               fill=PAL["maroon"])


# ---------------------------------------------------------------- cards ---
def chip_row(d, x, y, w, num, region, src, kind):
    pal = PAL
    d.rectangle([x, y, x + 24, y + 15], fill=pal["maroon"])
    t = str(num)
    f = fsr(11)
    d.text((x + 12 - d.textlength(t, font=f) / 2, y + 1), t, font=f,
           fill=(252, 248, 238))
    rc = REGION_COLORS[region]
    lab = region.upper()
    lf = fsr(10)
    lw = d.textlength(lab, font=lf) + 10
    d.rectangle([x + 28, y, x + 28 + lw, y + 15], fill=rc)
    d.text((x + 33, y + 2), lab, font=lf, fill=(252, 248, 238))
    sf = fsr(10)
    edge = x + w - (20 if kind else 0)
    d.text((edge - d.textlength(src, font=sf), y + 2), src, font=sf, fill=pal["sub"])
    if kind:
        icon(d, kind, x + w - 8, y + 7, 7, pal["maroon"], pal["sub"])


def lead(d, x, y, w, h, num, region, src, head, deck, kind):
    """Kartu lead #1: ilustrasi kriket besar + papan skor 720/9."""
    pal = PAL
    d.rectangle([x, y, x + w, y + h], fill=pal["panel"], outline=pal["maroon"], width=2)
    chip_row(d, x + 8, y + 6, w - 16, num, region, src, None)
    tw = w - 196
    yy = y + 28
    for ln in wrap(d, head, fb(34), tw):
        d.text((x + 8, yy), ln, font=fb(34), fill=pal["ink"])
        yy += 38
    for ln in wrap(d, deck, fr(15), tw):
        d.text((x + 8, yy), ln, font=fr(15), fill=pal["sub"])
        yy += 18
    # ilustrasi: lapangan kriket, stump, pemukul, papan skor
    ix, iy, iw, ih = x + w - 182, y + 30, 172, h - 40
    d.rectangle([ix, iy, ix + iw, iy + ih], fill=pal["soft"], outline=pal["line"])
    d.ellipse([ix + 10, iy + 8, ix + 30, iy + 28], outline=pal["maroon"], width=2)
    d.rectangle([ix + 78, iy + 8, ix + 164, iy + 56], fill=pal["panel"],
                outline=pal["maroon"], width=2)
    ctext(d, ix + 121, iy + 12, "720/9", fb(22), pal["maroon"])
    ctext(d, ix + 121, iy + 38, "DECLARED", fsr(10), pal["sub"])
    for i in range(3):
        sx = ix + 22 + i * 7
        d.line([sx, iy + 112, sx, iy + 84], fill=pal["ink"], width=3)
    d.line([ix + 22, iy + 84, ix + 36, iy + 84], fill=pal["maroon"], width=2)
    d.line([ix + 54, iy + 114, ix + 78, iy + 72], fill=pal["ink"], width=5)
    d.ellipse([ix + 118, iy + 88, ix + 130, iy + 100], fill=pal["maroon"])
    d.line([ix + 8, iy + 122, ix + iw - 8, iy + 122], fill=pal["line"], width=2)


def mini(d, x, y, w, h, num, region, src, head, deck, kind):
    """Kartu utama ringkas: chip region, ikon, judul besar, fakta, sumber."""
    pal = PAL
    d.rectangle([x, y, x + w, y + h], fill=pal["panel"], outline=pal["line"])
    chip_row(d, x + 7, y + 5, w - 14, num, region, src, kind)
    yy = y + 24
    for ln in wrap(d, head, fb(24), w - 14)[:2]:
        d.text((x + 7, yy), ln, font=fb(24), fill=pal["ink"])
        yy += 27
    for ln in wrap(d, deck, fr(14), w - 14)[:3]:
        d.text((x + 7, yy), ln, font=fr(14), fill=pal["sub"])
        yy += 16


# ----------------------------------------------------------------- page ---
def render(variant):
    global PAL
    PAL = PALETTES[variant]
    pal = PAL
    img = Image.new("RGB", (W, H), pal["bg"])
    d = ImageDraw.Draw(img)
    ink, sub, mar = pal["ink"], pal["sub"], pal["maroon"]

    # kicker jujur
    ctext(d, 512, 4, "40 STORIES · 8 REGIONS · EVERY ONE FROM 23 NOVEMBER 2026",
          fsr(14), mar)
    d.line([16, 21, 1008, 21], fill=mar, width=2)

    # masthead raksasa + tanggal
    if pal["band"]:
        d.rectangle([0, 8, 1024, 92], fill=mar)
        ctext(d, 512, 16, "THE DAILY MERIDIAN", fit_font(d, "THE DAILY MERIDIAN", fk, 64, 980),
              (252, 248, 238))
    else:
        ctext(d, 512, 12, "THE DAILY MERIDIAN", fit_font(d, "THE DAILY MERIDIAN", fk, 64, 980), mar)
    d.text((16, 102), "VOL. I · NO. 327", font=fsr(10), fill=sub)
    rt = "WELLINGTON · LONDON · DELHI"
    d.text((1008 - d.textlength(rt, font=fsr(10)), 102), rt, font=fsr(10), fill=sub)
    ctext(d, 512, 96, "Monday 23 November 2026", fb(30), ink)
    d.line([16, 130, 1008, 130], fill=mar, width=3)
    d.line([16, 134, 1008, 134], fill=pal["line"], width=1)

    # strip angka
    if pal["band"]:
        d.rectangle([0, 136, 1024, 176], fill=mar)
    short_labs = ["INDIA TEST RECORD", "US HOUSE SEATS", "INDIGO SHARE",
                  "GOLD PER OUNCE", "TATA STEEL SALE", "EWING CONTRACT"]
    for i, (val, lab) in enumerate(NUMS):
        bx = 16 + i * 165
        ctext(d, bx + 78, 140, val, fsr(23), (252, 248, 238) if pal["band"] else mar)
        ctext(d, bx + 78, 165, short_labs[i], fsr(10),
              (238, 220, 200) if pal["band"] else sub)

    # kartu-kartu utama
    lead(d, 16, 180, 548, 172, "1", "South Asia", "ObserverVoice · 23 Nov",
         "India Post Record 720/9 at Wellington",
         "India declared at 720 for 9 at Wellington - the highest Test total "
         "ever made in New Zealand, leaving the hosts a mountain to climb.",
         "cricket")
    mini(d, 572, 180, 436, 84, "2", "North America", "BBC · 23 Nov",
         "Democrats Take House 258-173",
         "Democrats won 258 seats to 173 after flipping North Carolina - "
         "biggest House majority since 1992, BBC said.", "ballot")
    mini(d, 572, 268, 436, 84, "3", "Europe", "BBC / AP · 23 Nov",
         "COP31 Ends With No Deal",
         "COP31 closed in Turkiye with no deal; the final draft omitted "
         "fossil fuels, BBC and AP reported.", "globe")
    mini(d, 16, 358, 242, 106, "4", "Europe", "BBC · 23 Nov",
         "Boy, 7, Saved From Kyiv Rubble",
         "Rescuers freed the boy after hours in Kyiv rubble; 6 died, BBC said.", "rescue")
    mini(d, 266, 358, 242, 106, "5", "South East Asia", "JagranJosh · 23 Nov",
         "Indonesia Fire: 7 Found, 50 Lost",
         "7 body bags found in Indonesia; 50 missing, JagranJosh said.", "flame")
    mini(d, 516, 358, 242, 106, "6", "South East Asia", "ICJ ruling · 23 Nov",
         "ICJ: Myanmar Guilty of Genocide",
         "Myanmar's 2017 Rohingya campaign, 700,000 fled, ruled genocide.", "scales")
    mini(d, 766, 358, 242, 106, "7", "Middle East", "AP live · 23 Nov",
         "Tanker Ablaze in Hormuz Strait",
         "Tanker burned as Iran-US war widened; IRGC warned, AP said.", "ship")
    mini(d, 16, 470, 242, 106, "8", "Global", "ObserverVoice · 23 Nov",
         "Gold Slides to $3,538 an Ounce",
         "Down over $2,000 from the 2026 record of $5,595, say reports.", "gold")
    mini(d, 266, 470, 242, 106, "9", "South Asia", "ObserverVoice · 23 Nov",
         "IndiGo Holds 65.9% of the Skies",
         "As SpiceJet pilots sought an audit, IndiGo took 65.9% share.", "plane")
    mini(d, 516, 470, 242, 106, "10", "South Asia", "ObserverVoice · 23 Nov",
         "Tata Steel Sells Pipe Unit",
         "APL Apollo bought the unit for Rs 28,000 crore, reports said.", "steel")
    mini(d, 766, 470, 242, 106, "11", "Europe", "BBC Sport · 23 Nov",
         "Alcaraz Beats Zverev for Crown",
         "Carlos Alcaraz beat Alexander Zverev for his 1st ATP crown.", "trophy")
    mini(d, 16, 582, 325, 106, "12", "North America", "BBC · 23 Nov",
         "Miley Cyrus Marries Maxx Morando",
         "Miley Cyrus married Maxx Morando in California, BBC confirmed on Monday.", "rings")
    mini(d, 349, 582, 325, 106, "13", "Global", "ObserverVoice · 23 Nov",
         "World Chess Title Fight Grips Fans",
         "The World Chess Championship captivated fans as the title match tightened.", "chess")
    mini(d, 682, 582, 325, 106, "14", "North America", "AP wire · 23 Nov",
         "Mets Land Ewing in $95M Deal",
         "New York Mets agreed an 8-year, $95 million deal with A.J. Ewing, AP said.", "baseball")

    # timeline UTC
    d.line([16, 694, 1008, 694], fill=pal["line"])
    for i, (tm, tx) in enumerate(TL):
        bx = 16 + i * 165
        lines = wrap(d, tm + " · " + tx, fr(12), 157)[:2]
        yy = 698
        for ln in lines:
            d.text((bx, yy), ln, font=fr(12), fill=sub)
            yy += 15
    d.line([16, 730, 1008, 730], fill=pal["line"])

    # peta + legenda (kiri bawah)
    d.text((16, 736), "THE DAY ON THE MAP", font=fsr(13), fill=mar)
    dotted_map(d, 16, 754, 336, 92)
    ly = 850
    for ln in wrap(d, "Dotted map: numbered pins mark the 14 main stories; "
                      "dot clusters sketch the continents.", fsr(11), 336):
        d.text((16, ly), ln, font=fsr(11), fill=sub)
        ly += 13
    ly += 3
    regs = list(REGION_COLORS.items())
    for i, (name, colr) in enumerate(regs):
        cx = 16 + (i % 2) * 172
        cy = ly + (i // 2) * 13
        d.rectangle([cx, cy + 2, cx + 10, cy + 12], fill=colr)
        d.text((cx + 14, cy), name, font=fsr(10), fill=sub)

    # ALSO ON (kanan bawah)
    d.text((364, 736), "ALSO ON THE DAY - STORIES 15-40", font=fsr(13), fill=mar)
    for col, briefs in enumerate((BRIEFS_L, BRIEFS_R)):
        bx = 364 + col * 326
        yy = 756
        for b in briefs:
            t = b
            while d.textlength(t, font=fsr(13)) > 318 and " " in t:
                t = t[:t.rfind(" ")]
            d.text((bx, yy), t, font=fsr(13), fill=ink)
            yy += 14

    # DATE CHECK merah
    red = (168, 30, 30)
    d.rectangle([16, 944, 1008, 988], outline=red, width=2)
    d.text((26, 952), "DATE CHECK", font=fsr(13), fill=red)
    d.text((26, 968), "NOT 23 NOV", font=fsr(10), fill=red)
    items = dc.split(" · ")
    for i, it in enumerate(items):
        bx = 150 + (i % 4) * 216
        by = 953 + (i // 4) * 19
        d.text((bx, by), it, font=fr(11), fill=red)

    # footer
    ctext(d, 512, 996,
          "Every story happened, or was first reported, on Monday 23 November "
          "2026. Contested claims are attributed. · Original drawings.",
          fr(11), sub)
    return img


def main():
    variant = sys.argv[1] if len(sys.argv) > 1 else "A"
    out = sys.argv[2] if len(sys.argv) > 2 else os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "entry.png")
    img = render(variant)
    img.save(out, optimize=True)
    print("%s -> %s (%d bytes)" % (variant, out, os.path.getsize(out)))


if __name__ == "__main__":
    main()

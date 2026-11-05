"""Short 2 - 'Find every hidden attachment in 10 seconds' (ZZ_YY)."""
import math, os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from snlib import *
from PIL import Image, ImageDraw, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))

LINES = [
    ("hook",   "Find every hidden attachment in your instance. In ten seconds.",
               "Find every hidden attachment in your instance. In 10 seconds."),
    ("nav",    "In the filter navigator, type sys underscore attachment, dot list. Press enter.",
               "In the filter navigator, type sys_attachment.list and press Enter."),
    ("filter", "Add a condition. Table name. Starts with. Z Z, Y Y. Then run.",
               "Add a condition: Table name, starts with, ZZ_YY. Then Run."),
    ("list",   "That's every attachment hidden from the attachment list, in one place.",
               "That's every attachment hidden from the attachment list, in one place."),
    ("group",  "Group by table name, and you can see exactly which tables are affected.",
               "Group by Table name, and you can see exactly which tables are affected."),
    ("save",   "Save it as a favorite. You'll need it again.",
               "Save it as a favorite. You'll need it again."),
    ("end",    "Want these files back in the attachment list? The business rule fix is in the full video. Follow for more.",
               "Want these files back in the attachment list? The business rule fix is in the full video. Follow for more."),
]

def stopwatch(img, cx, cy, r, frac, color):
    d = ImageDraw.Draw(img)
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(18, 26, 42), outline=WHITE, width=10)
    d.rounded_rectangle([cx - 30, cy - r - 50, cx + 30, cy - r - 10], 8, fill=WHITE)
    if frac > 0:
        d.pieslice([cx - r + 22, cy - r + 22, cx + r - 22, cy + r - 22], -90, -90 + 360 * frac, fill=color)
    ang = math.radians(-90 + 360 * frac)
    d.line([(cx, cy), (cx + (r - 40) * math.cos(ang), cy + (r - 40) * math.sin(ang))], fill=WHITE, width=10)
    d.ellipse([cx - 16, cy - 16, cx + 16, cy + 16], fill=WHITE)

def s_hook(img, t, p):
    d = ImageDraw.Draw(img)
    text_c(d, 250, "FIND EVERY", 100, WHITE, stroke=8)
    text_c(d, 370, "HIDDEN FILE", 100, AMBER, stroke=8)
    stopwatch(img, W // 2, 860, 260, min(1, p * 1.1), ACCENT)
    d = ImageDraw.Draw(img)
    secs = min(10, int(p * 11))
    text_c(d, 1170, f"{secs:02d}s", 90, ACCENT, kind="m", stroke=6)

def s_nav(img, t, p):
    header(img, "STEP 1", "Filter navigator", ACCENT, p)
    shadow_card(img, (90, 560, 990, 1180))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([90, 560, 990, 650], 28, fill=NAVY)
    d.rectangle([90, 620, 990, 650], fill=NAVY)
    d.text((130, 582), "All", font=font(40), fill=WHITE)
    d.rounded_rectangle([130, 690, 950, 790], 16, outline=(140, 170, 255), width=4)
    q = "sys_attachment.list"
    n = int(len(q) * ease(p * 1.8))
    d.text((165, 715), q[:n] + ("|" if int(t * 3) % 2 == 0 and n < len(q) else ""), font=font(46, "m"), fill=INK)
    d.text((170, 850), "Opens the table's list view", font=font(36, "r"), fill=GREY)
    if p > 0.6:
        e = ease((p - 0.6) * 5)
        x0, y0 = 610, 1040
        d.rounded_rectangle([x0, y0, x0 + 300, y0 + 100], 18, fill=(225, 230, 240), outline=(120, 130, 150), width=4)
        d.text((x0 + 50, y0 + 22), "Enter ⏎", font=font(46), fill=INK)
        if e > 0.5:
            ring(img, (x0, y0, x0 + 300, y0 + 100), ACCENT, t)

def s_filter(img, t, p):
    header(img, "STEP 2", "Add the condition", ACCENT, p)
    shadow_card(img, (60, 560, 1020, 1240))
    title_bar(img, (60, 560, 1020, 1240), "Attachments ▸ Filter")
    d = ImageDraw.Draw(img)
    chips = [("Table name", 0.0), ("starts with", 0.25), ("ZZ_YY", 0.5)]
    for i, (c, at) in enumerate(chips):
        e = ease((p - at) * 5)
        if e <= 0:
            continue
        y = 700 + i * 140
        col = AMBER if c == "ZZ_YY" else (140, 170, 255)
        d.rounded_rectangle([110, y, 970, y + 110], 16, outline=col, width=4, fill=(255, 250, 230) if c == "ZZ_YY" else CARD)
        d.text((150, y + 28), c, font=font(48, "m" if c == "ZZ_YY" else "r"), fill=(200, 40, 60) if c == "ZZ_YY" else INK)
        d.text((900, y + 28), "▾", font=font(44), fill=GREY)
    if p > 0.72:
        pressed = p > 0.85
        d.rounded_rectangle([700, 1110, 970, 1205], 18, fill=(30, 130, 80) if pressed else (40, 170, 105))
        d.text((790, 1130), "Run", font=font(46), fill=WHITE)
        cursor(d, 840, 1170, click=ease((p - 0.85) * 6) if pressed else 0)

ROWS = [("outlook_error.png", "ZZ_YYincident"), ("photo.jpg", "ZZ_YYsys_user"),
        ("laptop_quote.pdf", "ZZ_YYsc_req_item"), ("vpn_error.png", "ZZ_YYincident"),
        ("avatar.png", "ZZ_YYsys_user"), ("screenshot.png", "ZZ_YYincident")]

def zz(d, x, y, s, f):
    d.text((x, y), "ZZ_YY", font=f, fill=(220, 40, 60))
    d.text((x + d.textlength("ZZ_YY", font=f), y), s[5:], font=f, fill=INK)

def s_list(img, t, p):
    header(img, "RESULT", "Every hidden file, one list", AMBER, p)
    shadow_card(img, (50, 540, 1030, 1300))
    title_bar(img, (50, 540, 1030, 1300), "sys_attachment")
    d = ImageDraw.Draw(img)
    fm = font(31, "m")
    d.text((80, 650), "File name", font=font(30), fill=GREY)
    d.text((520, 650), "Table name", font=font(30), fill=GREY)
    for i, (a, b) in enumerate(ROWS):
        e = ease((p - i * 0.08) * 6)
        if e <= 0:
            continue
        y = 710 + i * 95
        d.text((80 - 40 * (1 - e), y + 10), a, font=fm, fill=INK)
        zz(d, 520 - 40 * (1 - e), y + 10, b, fm)
        d.line([(70, y + 75), (1010, y + 75)], fill=LINE, width=2)

def s_group(img, t, p):
    header(img, "GROUP BY", "Table name", AMBER, p)
    shadow_card(img, (60, 560, 1020, 1240), fill=(18, 26, 42))
    d = ImageDraw.Draw(img)
    data = [("ZZ_YYincident", 3, ACCENT), ("ZZ_YYsys_user", 2, (140, 170, 255)), ("ZZ_YYsc_req_item", 1, AMBER)]
    fm = font(38, "m")
    for i, (name, n, c) in enumerate(data):
        y = 620 + i * 190
        d.text((110, y), name, font=fm, fill=WHITE)
        e = ease((p - 0.1 - i * 0.12) * 3)
        bw = 760 * n / 3 * e
        d.rounded_rectangle([110, y + 60, 110 + max(bw, 4), y + 130], 14, fill=c)
        if e > 0.95:
            d.text((130 + bw, y + 70), f"({n})", font=font(44), fill=c)
    d.text((110, 1185), "counts from the example list", font=font(28, "r"), fill=GREY)

def s_save(img, t, p):
    header(img, "SAVE IT", "Reuse it anytime", ACCENT, p)
    d = ImageDraw.Draw(img)
    e = ease(p * 3)
    cx, cy, r = W // 2, 780, int(150 * (0.6 + 0.4 * e))
    pts = []
    for k in range(10):
        a = math.radians(-90 + k * 36)
        rr = r if k % 2 == 0 else r * 0.45
        pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
    gl = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(gl).polygon(pts, fill=AMBER + (160,))
    img.alpha_composite(gl.filter(ImageFilter.GaussianBlur(30)))
    d = ImageDraw.Draw(img)
    d.polygon(pts, fill=AMBER)
    shadow_card(img, (60, 1030, 1020, 1250), fill=(18, 26, 42))
    d = ImageDraw.Draw(img)
    d.text((100, 1060), "Or bookmark this URL:", font=font(34, "r"), fill=GREY)
    d.text((100, 1120), "sys_attachment_list.do?", font=font(38, "m"), fill=WHITE)
    d.text((100, 1170), "sysparm_query=table_nameSTARTSWITHZZ_YY", font=font(29, "m"), fill=AMBER)

def s_end(img, t, p):
    end_card(img, t, p, "WANT THEM BACK", "IN ATTACHMENTS?", "Business Rule fix", "(async · after insert)", "▶  Full video on the channel")

SCENES = dict(hook=s_hook, nav=s_nav, filter=s_filter, list=s_list, group=s_group, save=s_save, end=s_end)
print(render(LINES, SCENES, HERE, "short2_find_hidden_attachments"))

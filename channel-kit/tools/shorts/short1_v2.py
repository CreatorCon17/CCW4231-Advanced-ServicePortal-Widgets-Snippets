"""Short 1 - 'Attached... but missing' (ZZ_YY)."""
import math, os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from snlib import *
from PIL import Image, ImageDraw, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))

LINES = [
    ("hook",    "The screenshot is attached. But the incident shows nothing.",
                "The screenshot is attached. But the incident shows nothing."),
    ("portal",  "A user creates an incident from the portal, and attaches a screenshot in the form.",
                "A user creates an incident from the portal and attaches a screenshot in the form."),
    ("inc",     "Open the incident. No attachment. Not even in the activity stream.",
                "Open the incident. No attachment. Not even in the activity stream."),
    ("table",   "Now check the sys attachment table. The file is there, with the table name, Z Z, Y Y incident.",
                "Now check the sys_attachment table. The file is there, with table name ZZ_YYincident."),
    ("notbug",  "This is not a bug. It's platform design.",
                "This is not a bug. It's platform design."),
    ("meaning", "The Z Z, Y Y prefix tells ServiceNow: this file belongs to a variable, or an image field. So keep it out of the attachment list.",
                "The ZZ_YY prefix tells ServiceNow: this file belongs to a variable or an image field. So keep it out of the attachment list."),
    ("end",     "Want it back in the attachment list? The business rule fix is in the full video. Follow for more ServiceNow tips.",
                "Want it back in the attachment list? The business rule fix is in the full video. Follow for more ServiceNow tips."),
]

# ---- scenes ----
def s_hook(img, t, p):
    d = ImageDraw.Draw(img)
    text_c(d, 250, "ATTACHED…", 104, WHITE, stroke=8)
    text_c(d, 380, "BUT MISSING?", 104, RED, stroke=8)
    # file flies toward a card and vanishes
    shadow_card(img, (190, 700, 890, 1200))
    d = ImageDraw.Draw(img)
    d.text((240, 740), "INC0010018", font=font(46), fill=INK)
    d.text((240, 815), "Attachments", font=font(36), fill=INK)
    d.rounded_rectangle([240, 870, 840, 1000], 16, outline=LINE, width=4)
    d.text((300, 915), "No attachments", font=font(36, "r"), fill=GREY)
    d.text((240, 1040), "Activity", font=font(36), fill=INK)
    d.text((240, 1095), "— no files —", font=font(34, "r"), fill=GREY)
    k = ease(p * 1.6)
    alpha = 1 - ease((p - 0.55) * 4)
    if alpha > 0:
        fx, fy = 470 + 40 * (1 - k), 1400 - 480 * k
        layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        file_icon(ImageDraw.Draw(layer), fx, fy, 2.2)
        layer.putalpha(Image.eval(layer.getchannel("A"), lambda v: int(v * alpha)))
        img.alpha_composite(layer)
    if p > 0.6:
        ring(img, (240, 870, 840, 1000), RED, t)

def s_portal(img, t, p):
    header(img, "THE SCENARIO", "Create Incident from the portal", ACCENT, p)
    shadow_card(img, (90, 520, 990, 1330))
    d = ImageDraw.Draw(img)
    d.text((140, 560), "Create Incident", font=font(50), fill=INK)
    d.line([(140, 635), (940, 635)], fill=LINE, width=3)
    d.text((140, 660), "Urgency", font=font(32, "r"), fill=GREY)
    d.rounded_rectangle([140, 705, 940, 775], 12, outline=LINE, width=3)
    d.text((165, 720), "3 - Medium", font=font(34, "r"), fill=INK)
    d.text((140, 800), "Short description", font=font(32, "r"), fill=GREY)
    d.rounded_rectangle([140, 845, 940, 915], 12, outline=LINE, width=3)
    msg = "Unable to log in to Outlook"
    n = int(len(msg) * ease(p * 2.2))
    d.text((165, 860), msg[:n] + ("|" if p < 0.45 and int(t * 3) % 2 == 0 else ""), font=font(34, "r"), fill=INK)
    d.text((140, 940), "Please attach a screenshot of the error", font=font(32, "r"), fill=GREY)
    d.rounded_rectangle([140, 985, 940, 1095], 12, outline=(140, 170, 255), width=3)
    if p > 0.45:
        a = ease((p - 0.45) * 6)
        file_icon(d, 165, 1000 + 10 * (1 - a), 1.1)
        d.text((245, 1018), "outlook_error.png", font=font(34), fill=INK)
        d.text((680, 1022), "✓ uploaded", font=font(30), fill=(30, 160, 90))
    pressed = p > 0.8
    d.rounded_rectangle([640, 1170, 940, 1270], 18, fill=(30, 130, 80) if pressed else (40, 170, 105))
    d.text((715, 1193), "Submit", font=font(42), fill=WHITE)
    cx, cy = (790, 1235) if p > 0.65 else (560 + 300 * ease((p - 0.45) * 5), 1500 - 260 * ease((p - 0.45) * 5))
    cursor(d, cx, cy, click=ease((p - 0.8) * 6) if pressed else 0)

def s_inc(img, t, p):
    header(img, "THE INCIDENT", "…where's the screenshot?", WHITE, p)
    shadow_card(img, (90, 520, 990, 1330))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([90, 520, 990, 610], 28, fill=(52, 64, 84))
    d.rectangle([90, 580, 990, 610], fill=(52, 64, 84))
    d.text((130, 540), "Incident  INC0010018", font=font(40), fill=WHITE)
    rows = [("Short description", "Unable to log in to Outlook"), ("Urgency", "3 - Medium"), ("State", "New")]
    for i, (k, v) in enumerate(rows):
        y = 640 + i * 80
        d.text((130, y), k, font=font(30, "r"), fill=GREY)
        d.text((470, y), v, font=font(32, "r"), fill=INK)
    d.text((130, 900), "Attachments", font=font(36), fill=INK)
    d.rounded_rectangle([130, 950, 950, 1060], 16, outline=LINE, width=4)
    d.text((180, 985), "No attachments", font=font(36, "r"), fill=GREY)
    d.text((130, 1110), "Activity", font=font(36), fill=INK)
    d.rounded_rectangle([130, 1160, 950, 1280], 16, outline=LINE, width=4)
    d.text((180, 1180), "Incident created", font=font(32, "r"), fill=INK)
    d.text((180, 1225), "no files", font=font(30, "r"), fill=GREY)
    if p > 0.25:
        ring(img, (130, 950, 950, 1060), RED, t)
    if p > 0.6:
        ring(img, (130, 1160, 950, 1280), RED, t, alpha=0.9)

def s_table(img, t, p):
    header(img, "sys_attachment", "The file IS here", AMBER, p)
    shadow_card(img, (50, 540, 1030, 1260))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([50, 540, 1030, 630], 28, fill=(52, 64, 84))
    d.rectangle([50, 600, 1030, 630], fill=(52, 64, 84))
    cols = [(80, "File name"), (480, "Table name"), (860, "Sys ID")]
    for x, c in cols:
        d.text((x, 565), c, font=font(32), fill=WHITE)
    rows = [("report.pdf", "incident", "9f3a…"),
            ("outlook_error.png", "ZZ_YYincident", "4c1d…"),
            ("photo.jpg", "ZZ_YYsys_user", "7b2e…"),
            ("invoice.xlsx", "sc_req_item", "a81c…")]
    fm = font(31, "m")
    hl = 1
    for i, (a, b, c) in enumerate(rows):
        y = 660 + i * 140
        if i == hl and p > 0.35:
            d.rounded_rectangle([62, y - 20, 1018, y + 80], 14, fill=(255, 244, 205))
        d.text((80, y + 10), a, font=fm, fill=INK)
        x = 480
        if b.startswith("ZZ_YY"):
            d.text((x, y + 10), "ZZ_YY", font=fm, fill=(220, 40, 60))
            x += d.textlength("ZZ_YY", font=fm)
            d.text((x, y + 10), b[5:], font=fm, fill=INK)
        else:
            d.text((x, y + 10), b, font=fm, fill=INK)
        d.text((860, y + 10), c, font=fm, fill=GREY)
        d.line([(70, y + 100), (1010, y + 100)], fill=LINE, width=2)
    if p > 0.35:
        ring(img, (62, 640, 1018, 740 + 140 * 0 + 0) if False else (62, 780, 1018, 880), AMBER, t)
    if p > 0.6:
        z = ease((p - 0.6) * 4)
        d = ImageDraw.Draw(img)
        text_c(d, 1300, "ZZ_YY + incident", int(64 + 10 * z), AMBER, kind="m", stroke=6)

def s_notbug(img, t, p):
    d = ImageDraw.Draw(img)
    s = ease(p * 3)
    r = int(190 * s)
    cx, cy = W // 2, 800
    if r > 5:
        gl = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        ImageDraw.Draw(gl).ellipse([cx - r * 1.3, cy - r * 1.3, cx + r * 1.3, cy + r * 1.3], fill=ACCENT + (90,))
        img.alpha_composite(gl.filter(ImageFilter.GaussianBlur(40)))
        d = ImageDraw.Draw(img)
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=ACCENT)
        d.line([(cx - r * 0.45, cy + r * 0.02), (cx - r * 0.1, cy + r * 0.38), (cx + r * 0.5, cy - r * 0.35)], fill=(10, 40, 25), width=max(4, int(r * 0.16)), joint="curve")
    text_c(d, 1060, "NOT A BUG", 120, WHITE, stroke=8)
    text_c(d, 1210, "It's platform design", 60, ACCENT)

def s_meaning(img, t, p):
    header(img, "WHAT ZZ_YY MEANS", None, AMBER, p)
    d = ImageDraw.Draw(img)
    boxes = [
        (ACCENT, "table_name = incident", "✓ Shows in Attachments", "Regular attachment (paperclip)"),
        (AMBER, "table_name = ZZ_YYincident", "✗ Hidden from Attachments", "Belongs to a variable / image field"),
    ]
    for i, (c, a, b, sub) in enumerate(boxes):
        e = ease((p - i * 0.3) * 3)
        if e <= 0:
            continue
        y = 450 + i * 420
        x0 = 70 + (1 - e) * (-900 if i == 0 else 900)
        d.rounded_rectangle([x0, y, x0 + 940, y + 360], 28, fill=(18, 26, 42), outline=c, width=6)
        d.text((x0 + 40, y + 40), a, font=font(40, "m"), fill=c)
        d.text((x0 + 40, y + 140), b, font=font(48), fill=WHITE)
        d.text((x0 + 40, y + 240), sub, font=font(36, "r"), fill=GREY)

def s_end(img, t, p):
    end_card(img, t, p, "WANT IT BACK", "IN ATTACHMENTS?", "Business Rule fix", "(async · after insert)", "▶  Full video on the channel")

SCENES = dict(hook=s_hook, portal=s_portal, inc=s_inc, table=s_table, notbug=s_notbug, meaning=s_meaning, end=s_end)
print(render(LINES, SCENES, HERE, "short1_zz_yy_attached_but_missing"))

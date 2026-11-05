"""Short 4 - 'Delete 5 letters = fixed? Don't do it by hand.'"""
import math, os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from snlib import *
from PIL import Image, ImageDraw, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))

LINES = [
    ("hook",    "Delete five letters, and the attachment comes back?",
                "Delete five letters, and the attachment comes back?"),
    ("demo",    "Remove Z Z, Y Y from the table name. Save. Refresh the incident.",
                "Remove ZZ_YY from the table name. Save. Refresh the incident."),
    ("result",  "The file now shows in the attachment list. And the image field still works.",
                "The file now shows in the attachment list. And the image field still works."),
    ("point",   "So the prefix only controls visibility in the attachment list. Nothing else.",
                "So the prefix only controls visibility in the attachment list. Nothing else."),
    ("problem", "But fixing every record by hand? Only admins can, and nobody keeps that up.",
                "But fixing every record by hand? Only admins can, and nobody keeps that up."),
    ("auto",    "Put the same logic in an async business rule, and every new incident is fixed automatically.",
                "Put the same logic in an async Business Rule, and every new incident is fixed automatically."),
    ("end",     "The full business rule is in the long video. Follow for more.",
                "The full Business Rule is in the long video. Follow for more."),
]

def field_box(img, t, value_left, cursor_on=True, y=980):
    d = ImageDraw.Draw(img)
    d.text((140, y - 70), "Table name", font=font(36, "r"), fill=GREY)
    d.rounded_rectangle([130, y, 950, y + 120], 16, outline=(140, 170, 255), width=4, fill=CARD)
    f = font(56, "m")
    x = 170
    if value_left.startswith("ZZ_YY"):
        d.text((x, y + 28), value_left[:5], font=f, fill=(220, 40, 60)); x += d.textlength(value_left[:5], font=f)
        d.text((x, y + 28), value_left[5:], font=f, fill=INK); x += d.textlength(value_left[5:], font=f)
    else:
        pre = value_left[:-8] if value_left.endswith("incident") else ""
        d.text((x, y + 28), pre, font=f, fill=(220, 40, 60)); x += d.textlength(pre, font=f)
        d.text((x, y + 28), "incident", font=f, fill=INK)
    if cursor_on and int(t * 3) % 2 == 0:
        d.line([(170 + d.textlength(value_left[:max(0, len(value_left) - 8)], font=f), y + 22),
                (170 + d.textlength(value_left[:max(0, len(value_left) - 8)], font=f), y + 98)], fill=INK, width=4)

def s_hook(img, t, p):
    d = ImageDraw.Draw(img)
    text_c(d, 250, "DELETE 5 LETTERS", 92, WHITE, stroke=8)
    text_c(d, 365, "= FIXED?", 100, AMBER, stroke=8)
    shadow_card(img, (90, 820, 990, 1200))
    k = 5 - int(min(5, p * 7))
    field_box(img, t, "ZZ_YY"[:k] + "incident")

def s_demo(img, t, p):
    header(img, "THE MANUAL FIX", "sys_attachment record", AMBER, p)
    shadow_card(img, (90, 820, 990, 1300))
    field_box(img, t, "incident", cursor_on=False)
    d = ImageDraw.Draw(img)
    pressed = p > 0.5
    d.rounded_rectangle([640, 1150, 940, 1250], 18, fill=(30, 130, 80) if pressed else (40, 170, 105))
    d.text((735, 1172), "Save", font=font(44), fill=WHITE)
    cursor(d, 800, 1210, click=ease((p - 0.5) * 5) if pressed else 0)

def s_result(img, t, p):
    header(img, "IT'S BACK", None, ACCENT, p)
    def extra(img, d, b):
        x0, y0, x1, y1 = b
        d.text((x0 + 40, y0), "Image field", font=font(36), fill=INK)
        d.rounded_rectangle([x0 + 40, y0 + 55, x0 + 340, y0 + 200], 16, fill=(225, 235, 255))
        file_icon(d, x0 + 160, y0 + 90, 1.1)
        d.text((x0 + 380, y0 + 100), "✓ still works", font=font(44), fill=(30, 150, 90))
    inc_card(img, t, attachments=("outlook_error.png",), ring_att=ACCENT, extra=extra, box=(90, 440, 990, 1320))

def s_point(img, t, p):
    d = ImageDraw.Draw(img)
    text_c(d, 380, "ZZ_YY", 170, AMBER, kind="m", stroke=10)
    text_c(d, 640, "only controls", 70, WHITE)
    text_c(d, 740, "visibility in the", 70, WHITE)
    text_c(d, 840, "attachment list", 70, ACCENT)
    text_c(d, 1030, "Nothing else.", 64, GREY, kind="r", stroke=4)

def s_problem(img, t, p):
    header(img, "BUT…", "every record? by hand?", RED, p)
    for i in range(7):
        e = ease((p - i * 0.07) * 6)
        if e <= 0:
            continue
        x = 110 + (i % 2) * 40 + i * 18
        y = 600 + i * 95
        shadow_card(img, (x, y, x + 780, y + 150))
        d = ImageDraw.Draw(img)
        d.text((x + 40, y + 45), f"INC00100{22 + i}", font=font(44), fill=INK)
        d.text((x + 630, y + 30), "✗", font=font(70), fill=RED)

def s_auto(img, t, p):
    header(img, "AUTOMATE IT", "async Business Rule", ACCENT, p)
    d = ImageDraw.Draw(img)
    cx, cy, r = W // 2, 720, 120
    ang = t * 2
    pts = []
    for k in range(16):
        a = ang + k * math.pi / 8
        rr = r if k % 2 == 0 else r * 0.78
        pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
    d.polygon(pts, fill=ACCENT)
    d.ellipse([cx - 45, cy - 45, cx + 45, cy + 45], fill=(18, 26, 42))
    for i in range(4):
        y = 920 + i * 100
        e = ease((p - 0.2 - i * 0.12) * 5)
        d.rounded_rectangle([150, y, 930, y + 80], 14, fill=(18, 26, 42), outline=ACCENT if e > 0.5 else GREY, width=3)
        d.text((190, y + 18), f"INC00100{30 + i}", font=font(38), fill=WHITE)
        if e > 0.5:
            d.text((820, y + 8), "✓", font=font(56), fill=ACCENT)

def s_end(img, t, p):
    end_card(img, t, p, "GET THE", "BUSINESS RULE", "Full script + demo", "(async · insert)", "▶  Full video on the channel")

SCENES = dict(hook=s_hook, demo=s_demo, result=s_result, point=s_point, problem=s_problem, auto=s_auto, end=s_end)
print(render(LINES, SCENES, HERE, "short4_dont_fix_by_hand"))

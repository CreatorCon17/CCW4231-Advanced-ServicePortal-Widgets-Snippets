"""Short 5 - 'Your cleanup script might be deleting real files' (ZZ_YY trap)."""
import math, os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from snlib import *
from PIL import Image, ImageDraw, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))

FIX = [
    "var table = att.getValue('table_name')",
    "    .replace(/^ZZ_YY/, '');",
    "var rec = new GlideRecord(table);",
    "if (!rec.isValid() ||",
    "    !rec.get(att.getValue('table_sys_id'))) {",
    "  gs.info('Orphan? ' + att.sys_id);",
    "}",
]

LINES = [
    ("hook",  "This cleanup script might be deleting real files.",
              "This cleanup script might be deleting real files."),
    ("how",   "A common cleanup job checks every attachment. If its record doesn't exist, the file gets deleted.",
              "A common cleanup job checks every attachment. If its record doesn't exist, the file gets deleted."),
    ("trap",  "But there's no table called Z Z, Y Y incident. So the lookup fails, and a file that's still in use looks orphaned.",
              "But there's no table called ZZ_YYincident. So the lookup fails, and a file that's still in use looks orphaned."),
    ("fix",   "Strip the Z Z, Y Y prefix before you look up the table. Then check the record.",
              "Strip the ZZ_YY prefix before you look up the table. Then check the record."),
    ("dry",   "And run it as a dry run first. Log, don't delete.",
              "And run it as a dry run first. Log, don't delete."),
    ("end",   "Why Z Z, Y Y exists is in the full video. Follow for more.",
              "Why ZZ_YY exists is in the full video. Follow for more."),
]

def step(d, y, text, col, e):
    if e <= 0:
        return
    x = 130 - (1 - e) * 600
    d.rounded_rectangle([x, y, x + 820, y + 130], 22, fill=(18, 26, 42), outline=col, width=5)
    d.text((x + 40, y + 36), text, font=font(46), fill=WHITE)

def s_hook(img, t, p):
    d = ImageDraw.Draw(img)
    text_c(d, 250, "THIS SCRIPT", 100, WHITE, stroke=8)
    text_c(d, 370, "DELETES REAL FILES", 84, RED, stroke=8)
    # trash can
    cx, cy = W // 2, 900
    shake = math.sin(t * 30) * 6 if p > 0.4 else 0
    d.rounded_rectangle([cx - 150 + shake, cy - 120, cx + 150 + shake, cy + 220], 24, fill=(60, 66, 84), outline=RED, width=6)
    d.rectangle([cx - 190 + shake, cy - 170, cx + 190 + shake, cy - 130], fill=RED)
    d.rectangle([cx - 50 + shake, cy - 200, cx + 50 + shake, cy - 170], fill=RED)
    for k in (-80, 0, 80):
        d.line([(cx + k + shake, cy - 80), (cx + k + shake, cy + 180)], fill=(30, 34, 46), width=12)
    e = ease(p * 2)
    file_icon(d, cx - 60, 560 + 260 * e, 2.2, color=(90, 140, 255))

def s_how(img, t, p):
    header(img, "THE CLEANUP JOB", None, WHITE, p)
    d = ImageDraw.Draw(img)
    step(d, 470, "1. Read each attachment", (140, 170, 255), ease(p * 4))
    step(d, 660, "2. Find its record", (140, 170, 255), ease((p - 0.25) * 4))
    step(d, 850, "3. Not found?", AMBER, ease((p - 0.5) * 4))
    step(d, 1040, "4. Delete the file", RED, ease((p - 0.7) * 4))

def s_trap(img, t, p):
    header(img, "THE TRAP", None, RED, p)
    code_card(img, (40, 430, 1040, 760), ["new GlideRecord('ZZ_YYincident');"], t, title="lookup")
    d = ImageDraw.Draw(img)
    if p > 0.25:
        text_c(d, 820, "✗ table doesn't exist", 60, RED)
    if p > 0.5:
        shadow_card(img, (120, 960, 960, 1290))
        d = ImageDraw.Draw(img)
        file_icon(d, 170, 1020, 1.6)
        d.text((290, 1010), "outlook_error.png", font=font(42), fill=INK)
        d.text((290, 1080), "still used on INC0010018", font=font(34, "r"), fill=GREY)
        d.rounded_rectangle([290, 1150, 760, 1235], 16, fill=(255, 225, 228))
        d.text((315, 1168), "flagged as orphan", font=font(40), fill=(200, 30, 50))

def s_fix(img, t, p):
    header(img, "THE FIX", "Strip the prefix first", ACCENT, p)
    code_card(img, (40, 520, 1040, 1250), FIX, t, size=31, hl={0, 1} if p < 0.55 else {2, 3, 4}, title="cleanup (dry run)")

def s_dry(img, t, p):
    header(img, "DRY RUN FIRST", None, AMBER, p)
    d = ImageDraw.Draw(img)
    for i, (lab, mark, col) in enumerate([("LOG", "✓", ACCENT), ("DELETE", "✗", RED)]):
        e = ease((p - i * 0.3) * 4)
        if e <= 0:
            continue
        y = 560 + i * 380
        shadow_card(img, (140, y, 940, y + 300), fill=(18, 26, 42))
        d = ImageDraw.Draw(img)
        d.rounded_rectangle([140, y, 940, y + 300], 28, outline=col, width=6)
        d.text((220, y + 95), lab, font=font(100), fill=WHITE)
        d.text((780, y + 80), mark, font=font(120), fill=col)

def s_end(img, t, p):
    end_card(img, t, p, "WHY DOES", "ZZ_YY EXIST?", "Full explainer", "(platform design + fix)", "▶  Full video on the channel")

SCENES = dict(hook=s_hook, how=s_how, trap=s_trap, fix=s_fix, dry=s_dry, end=s_end)
print(render(LINES, SCENES, HERE, "short5_cleanup_script_trap"))

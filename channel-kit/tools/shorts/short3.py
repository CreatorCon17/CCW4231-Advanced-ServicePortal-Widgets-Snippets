"""Short 3 - 'Fix hidden attachments automatically' (async Business Rule)."""
import math, os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from snlib import *
from PIL import Image, ImageDraw, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))

CODE = [
    "var att = new GlideRecord('sys_attachment');",
    "var table = current.getTableName();",
    "att.addQuery('table_name', 'ZZ_YY' + table);",
    "att.addQuery('table_sys_id', current.sys_id);",
    "att.query();",
    "while (att.next()) {",
    "  att.setValue('table_name', table);",
    "  att.update();",
    "}",
]

LINES = [
    ("hook",   "Stop fixing hidden attachments by hand. Let a business rule do it.",
               "Stop fixing hidden attachments by hand. Let a business rule do it."),
    ("setup",  "Create a business rule on the incident table. Tick advanced. When: async. On insert.",
               "Create a Business Rule on the incident table. Advanced. When: async. On insert."),
    ("query",  "Query sys attachment for this record, where the table name is Z Z, Y Y, plus the table name.",
               "Query sys_attachment for this record, where table_name is ZZ_YY + the table name."),
    ("loop",   "For every match, set the table name back to the real table, and update.",
               "For every match, set table_name back to the real table, and update."),
    ("while",  "Use while, not if. So an incident with two screenshots gets both fixed.",
               "Use while, not if. So an incident with two screenshots gets both fixed."),
    ("result", "Submit a new incident, and the screenshot shows in the attachment list.",
               "Submit a new incident, and the screenshot shows in the attachment list."),
    ("end",    "Full walkthrough in the long video. Follow for more ServiceNow tips.",
               "Full walkthrough in the long video. Follow for more ServiceNow tips."),
]

def s_hook(img, t, p):
    d = ImageDraw.Draw(img)
    text_c(d, 250, "STOP FIXING", 100, WHITE, stroke=8)
    text_c(d, 370, "BY HAND", 100, RED, stroke=8)
    for i, (label, col, mark) in enumerate([("Manual edit", RED, "✗"), ("Business Rule", ACCENT, "✓")]):
        e = ease((p - i * 0.35) * 3)
        if e <= 0:
            continue
        y = 640 + i * 330
        shadow_card(img, (120, y, 960, y + 260), fill=(18, 26, 42))
        d = ImageDraw.Draw(img)
        d.rounded_rectangle([120, y, 960, y + 260], 28, outline=col, width=6)
        d.text((180, y + 85), label, font=font(64), fill=WHITE)
        d.text((830, y + 70), mark, font=font(100), fill=col)

def s_setup(img, t, p):
    header(img, "STEP 1", "Create the Business Rule", ACCENT, p)
    box = (90, 560, 990, 1300)
    shadow_card(img, box)
    title_bar(img, box, "Business Rule  ·  New")
    d = ImageDraw.Draw(img)
    fields = [("Name", "INC attachment visible"), ("Table", "incident"), ("Advanced", "✓"),
              ("When", "async"), ("Insert", "✓")]
    for i, (k, v) in enumerate(fields):
        e = ease((p - i * 0.12) * 5)
        if e <= 0:
            continue
        y = 690 + i * 115
        d.text((140, y + 18), k, font=font(34, "r"), fill=GREY)
        d.rounded_rectangle([400, y, 940, y + 85], 14, outline=LINE, width=3)
        bold = v in ("incident", "async", "✓")
        d.text((430, y + 18), v, font=font(38 if bold else 34, "b" if bold else "r"),
               fill=(30, 150, 90) if v == "✓" else INK)
        if v in ("async",) and p > 0.7:
            ring(img, (400, y, 940, y + 85), AMBER, t)

def s_query(img, t, p):
    header(img, "STEP 2", "Find the hidden files", AMBER, p)
    code_card(img, (40, 520, 1040, 1330), CODE, t, hl={0, 1, 2, 3, 4}, reveal=0.3 + 0.7 * ease(p * 2), size=31)

def s_loop(img, t, p):
    header(img, "STEP 3", "Point them at the real table", AMBER, p)
    code_card(img, (40, 520, 1040, 1330), CODE, t, hl={5, 6, 7, 8}, size=31)

def s_while(img, t, p):
    header(img, "WHILE, NOT IF", "Fixes every file, not just one", ACCENT, p)
    code_card(img, (40, 520, 1040, 1330), CODE, t, hl={5}, size=31)
    if p > 0.3:
        d = ImageDraw.Draw(img)
        e = ease((p - 0.3) * 4)
        d.rounded_rectangle([290, 1170 - 20 * (1 - e), 790, 1280], 18, fill=(18, 26, 42), outline=ACCENT, width=4)
        d.text((335, 1198), "2 files → 2 fixed", font=font(44), fill=ACCENT)

def s_result(img, t, p):
    header(img, "RESULT", "Visible in Attachments", ACCENT, p)
    inc_card(img, t, attachments=("outlook_error.png",) if p > 0.25 else (), ring_att=ACCENT if p > 0.25 else None)

def s_end(img, t, p):
    end_card(img, t, p, "WANT THE FULL", "WALKTHROUGH?", "Step-by-step demo", "(update set · rule · test)", "▶  Full video on the channel")

SCENES = dict(hook=s_hook, setup=s_setup, query=s_query, loop=s_loop, **{"while": s_while}, result=s_result, end=s_end)
print(render(LINES, SCENES, HERE, "short3_business_rule_fix"))

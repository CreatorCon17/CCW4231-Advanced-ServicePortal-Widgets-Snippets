"""HRSD Ep 1.1 Short: auto-populate Manager & Location with no client script (PPT style, voice 9)."""
import math, os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pptstyle import *
from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))

LINES = [
    ("hook",   "Stop writing client scripts just to fill in the manager field.",
               "Stop writing client scripts just to fill in the manager field."),
    ("default", "First, in the record producer, set the requested for default value to javascript, colon, gs dot get user ID. It fills in the logged-in user.",
               "First, set the Requested for default value to javascript:gs.getUserID(). It fills in the logged-in user."),
    ("auto",   "Then open the manager variable, and go to the auto-populate tab. Dependent question: requested for. Dot walk path: manager.",
               "Then open the Manager variable → Auto-populate tab. Dependent question: Requested for. Dot-walk path: Manager."),
    ("loc",    "Same for location. No client script. No GlideAjax.",
               "Same for Location. No client script. No GlideAjax."),
    ("result", "Now pick a user, and the manager and location fill in by themselves.",
               "Now pick a user, and Manager and Location fill in by themselves."),
    ("catch",  "One catch. It only follows fields on the record you point it at. Employee type lives on the HR profile, not the user record, so that needs a different approach.",
               "One catch: it only follows fields on the record you point it at. Employee type lives on the HR profile, not the user record."),
    ("end",    "The full build is in episode one of the HR leave request series. Follow for more.",
               "The full build is in Episode 1 of the HR Leave Request series. Follow for more."),
]

def s_hook(img, t, p):
    d = ImageDraw.Draw(img)
    text_c(d, 230, "AUTO-FILL THE", 92, NAVY)
    text_c(d, 335, "MANAGER FIELD", 92, NAVY)
    chip_w = d.textlength("NO CLIENT SCRIPT", font=font(52)) + 40
    chip(d, (W - chip_w) / 2, 460, "NO CLIENT SCRIPT", GREEN, size=52)
    card(img, (100, 640, 980, 1020))
    d = ImageDraw.Draw(img)
    d.text((140, 670), "onChange client script", font=font(34, "r"), fill=GREYT)
    code = ["g_form.getReference('requested_for',", "  function (u) {", "    g_form.setValue('manager',", "      u.manager); });"]
    for i, l in enumerate(code):
        d.text((140, 730 + i * 58), l, font=font(34, "m"), fill=INK)
    if p > 0.35:
        e = ease((p - 0.35) * 4)
        lw = 12
        d.line([(120, 1000), (120 + 840 * e, 660 + 0 * e)], fill=RED, width=lw)
        d.line([(120, 660), (120 + 840 * e, 1000 - 0 * e)], fill=RED, width=lw)

def s_default(img, t, p):
    header(img, "STEP 1", "Requested for", p, sub="Variable · Default value")
    card(img, (90, 520, 990, 1250))
    bar(img, (90, 520, 990, 1250), "Variable: requested_for")
    d = ImageDraw.Draw(img)
    field(d, 140, 640, 800, "Type", "Reference")
    field(d, 140, 790, 800, "Reference", "sys_user", value_kind="b", value_color=NAVY)
    val = "javascript:gs.getUserID()"
    n = int(len(val) * ease((p - 0.15) * 2.2))
    field(d, 140, 940, 800, "Default value", val[:n] + ("|" if n < len(val) and int(t * 3) % 2 == 0 else ""), value_kind="m",
          value_color=NAVY, value_size=34, border=AMBER if n else LIGHT)
    if n == len(val):
        ring(img, (140, 984, 940, 1068), t)
        d = ImageDraw.Draw(img)
        d.text((140, 1110), "✓ logged-in user pre-filled", font=tfont("✓", 40), fill=GREEN)

def s_auto(img, t, p):
    header(img, "STEP 2", "Manager variable", p, sub="Auto-populate tab")
    card(img, (90, 520, 990, 1300))
    bar(img, (90, 520, 990, 1300), "Variable: manager")
    d = ImageDraw.Draw(img)
    tx = 140
    for i, tab in enumerate(["Type Specs", "Default Value", "Auto-populate"]):
        f = font(32); w = d.textlength(tab, font=f)
        active = i == 2
        d.rounded_rectangle([tx, 630, tx + w + 36, 690], 10, fill=NAVY if active else LIGHT)
        d.text((tx + 18, 642), tab, font=f, fill=WHITE if active else GREYT)
        tx += w + 50
    e1 = ease((p - 0.25) * 4); e2 = ease((p - 0.55) * 4)
    field(d, 140, 740, 800, "Dependent question", "Requested for" if e1 > 0.5 else "", value_kind="b", value_color=NAVY,
          border=AMBER if e1 > 0.5 else LIGHT)
    field(d, 140, 900, 800, "Dot walk path", "Manager" if e2 > 0.5 else "", value_kind="b", value_color=NAVY,
          border=AMBER if e2 > 0.5 else LIGHT)
    if e2 > 0.5:
        ring(img, (140, 944, 940, 1028), t)
        d = ImageDraw.Draw(img)
        d.text((140, 1080), "Requested for  →  Manager", font=font(44), fill=GREEN)
        d.text((140, 1150), "(read from the sys_user record)", font=font(34, "i"), fill=GREYT)

def s_loc(img, t, p):
    header(img, "STEP 3", "Same for Location", p)
    rows = [("Manager", "Requested for → Manager", GREEN), ("Location", "Requested for → Location", GREEN)]
    for i, (a, b, c) in enumerate(rows):
        e = ease((p - i * 0.25) * 4)
        if e <= 0:
            continue
        y = 470 + i * 230
        x = 90 - (1 - e) * 500
        card(img, (x, y, x + 900, y + 190))
        d = ImageDraw.Draw(img)
        d.rectangle([x, y, x + 16, y + 190], fill=c)
        d.text((x + 50, y + 34), a, font=font(54), fill=NAVY)
        d.text((x + 50, y + 108), b, font=font(40, "r"), fill=GREYT)
    if p > 0.55:
        d = ImageDraw.Draw(img)
        x = 150
        for s_ in ["✗ Client script", "✗ GlideAjax"]:
            x += chip(d, x, 1000, s_, RED, size=44) + 30
        w_ = d.textlength("✓ Config only", font=tfont("✓", 48)) + 40
        chip(d, (W - w_) / 2, 1110, "✓ Config only", GREEN, size=48)

def s_result(img, t, p):
    header(img, "RESULT", "Leave Request form", p, kicker_color=GREEN)
    card(img, (90, 480, 990, 1340))
    bar(img, (90, 480, 990, 1340), "Employee information")
    d = ImageDraw.Draw(img)
    picked = p > 0.3
    fill = ease((p - 0.4) * 4)
    field(d, 140, 600, 800, "Requested for", "Alex Carter" if picked else "Select a user…", value_kind="b" if picked else "i",
          value_color=NAVY if picked else GREYT, border=AMBER if picked and fill < 1 else LIGHT)
    field(d, 140, 760, 800, "Manager", "Sam Patel" if fill > 0.5 else "", value_kind="b", value_color=NAVY,
          border=GREEN if fill > 0.5 else LIGHT)
    field(d, 140, 920, 800, "Location", "London, UK" if fill > 0.5 else "", value_kind="b", value_color=NAVY,
          border=GREEN if fill > 0.5 else LIGHT)
    field(d, 140, 1080, 800, "Employee type", "", border=LIGHT)
    if fill > 0.5:
        ring(img, (140, 804, 940, 1048), t, color=GREEN)
        d = ImageDraw.Draw(img)
        d.text((790, 770), "auto ✓", font=tfont("✓", 34), fill=GREEN)
    if not picked:
        cursor(d, 600 + 200 * ease(p * 3), 760 - 80 * ease(p * 3))
    elif p < 0.45:
        cursor(d, 800, 680, click=ease((p - 0.3) * 6))
    d.text((140, 1230), "Illustrative names", font=font(28, "i"), fill=GREYT)

def s_catch(img, t, p):
    header(img, "ONE CATCH", "Employee type?", p, kicker_color=AMBER, sub="It's not on the user record")
    d = ImageDraw.Draw(img)
    e = ease(p * 3)
    card(img, (90, 540, 520, 960))
    card(img, (560, 540, 990, 960), border=AMBER)
    d = ImageDraw.Draw(img)
    d.text((130, 575), "sys_user", font=font(44, "m"), fill=NAVY)
    for i, f_ in enumerate(["manager ✓", "location ✓", "department ✓"]):
        d.text((130, 660 + i * 80), f_, font=tfont(f_, 40), fill=GREEN)
    d.text((600, 575), "HR profile", font=font(48), fill=NAVY)
    d.text((600, 660), "employee type", font=font(40), fill=INK)
    d.text((600, 740), "lives here", font=font(36, "i"), fill=GREYT)
    if e > 0.5:
        ring(img, (590, 650, 960, 720), t)
        d = ImageDraw.Draw(img)
        text_c(d, 1030, "Auto-populate can't reach it directly", 46, NAVY)
        text_c(d, 1100, "→ different approach, covered in the episode", 40, GREYT, "i")

def s_end(img, t, p):
    end_card(img, t, p, "FULL BUILD IN", "EPISODE 1", "HR Leave Request series", "HR Service · Record Producer · variables")

SCENES = dict(hook=s_hook, default=s_default, auto=s_auto, loc=s_loc, result=s_result, catch=s_catch, end=s_end)
print(render(LINES, SCENES, HERE, "hrsd_ep1_short_autopopulate"))

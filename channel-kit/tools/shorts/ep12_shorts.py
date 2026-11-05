"""HRSD Ep 1.2 Shorts (PPT style, voice 9).
A = Employee type via GlideAjax + Script Include.  B = Leave duration + remaining balance.
Usage: python ep12_shorts.py A|B [preview]"""
import math, os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pptstyle import *
import snlib as S
from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))

def code(img, box, lines, t, hl=(), title="", size=28, reveal=1.0):
    S.code_card(img, box, lines, t, hl=set(hl), size=size, title=title, reveal=reveal)

def illus(d, y=1330):
    d.text((90, y), "Variable / field names illustrative: match your own", font=font(28, "i"), fill=GREYT)

def flow_box(img, d, x, y, w, h, title, sub, color, e=1.0):
    if e <= 0:
        return
    card(img, (x, y, x + w, y + h), border=color)
    d = ImageDraw.Draw(img)
    d.rectangle([x, y, x + 14, y + h], fill=color)
    d.text((x + 40, y + 26), title, font=font(46), fill=NAVY)
    d.text((x + 40, y + 88), sub, font=font(34, "m" if "_" in sub else "r"), fill=GREYT)

# ---------------- SHORT A ----------------
A_LINES = [
    ("hook", "Employee type isn't on the user record. So auto-populate can't fill it.",
             "Employee type isn't on the user record. So auto-populate can't fill it."),
    ("flow", "The fix: an on change client script calls a script include with GlideAjax. The script include reads the HR profile, and sends the value back.",
             "The fix: an onChange client script calls a Script Include with GlideAjax. It reads the HR profile and sends the value back."),
    ("client", "On change of requested for: create the GlideAjax, pass the function name and the user ID, then set employee type from the answer.",
               "onChange of Requested for: create the GlideAjax, pass the function name and the user ID, then set Employee type from the answer."),
    ("si",   "In the script include, read the parameter, look up the HR profile by user, and return the display value.",
             "In the Script Include: read the parameter, look up the HR profile by user, and return the display value."),
    ("gotcha", "Two gotchas. Tick client callable, or the call never reaches the server. And return the display value, or you'll see the back-end value instead.",
               "Two gotchas: tick Client callable, or the call never reaches the server. And return the display value, not the back-end value."),
    ("end",  "Full build in episode one point two of the HR leave request series. Follow for more.",
             "Full build in Episode 1.2 of the HR Leave Request series. Follow for more."),
]
A_CLIENT = [
    "// onChange: requested_for",
    "if (isLoading || !newValue) return;",
    "var ga = new GlideAjax('LeaveRequestHelper');",
    "ga.addParam('sysparm_name', 'getEmployeeType');",
    "ga.addParam('sysparm_user_id', newValue);",
    "ga.getXMLAnswer(function (answer) {",
    "  g_form.setValue('employee_type', answer);",
    "});",
]
A_SI = [
    "// Script Include · Client callable",
    "getEmployeeType: function () {",
    "  var userId =",
    "    this.getParameter('sysparm_user_id');",
    "  var gr = new GlideRecord('sn_hr_core_profile');",
    "  if (gr.get('user', userId))",
    "    return gr.getDisplayValue('employee_type');",
    "  return '';",
    "},",
]

def a_hook(img, t, p):
    d = ImageDraw.Draw(img)
    text_c(d, 220, "EMPLOYEE TYPE?", 100, NAVY)
    w_ = d.textlength("NOT ON THE USER RECORD", font=font(46)) + 40
    chip(d, (W - w_) / 2, 350, "NOT ON THE USER RECORD", AMBER, size=46, fg=NAVY)
    card(img, (90, 520, 520, 980))
    card(img, (560, 520, 990, 980), border=AMBER)
    d = ImageDraw.Draw(img)
    d.text((130, 555), "sys_user", font=font(44, "m"), fill=NAVY)
    for i, f_ in enumerate(["manager ✓", "location ✓", "employee type ✗"]):
        d.text((130, 640 + i * 80), f_, font=tfont(f_, 40), fill=RED if "✗" in f_ else GREEN)
    d.text((600, 555), "HR profile", font=font(48), fill=NAVY)
    d.text((600, 640), "employee type", font=font(42), fill=INK)
    d.text((600, 715), "lives here", font=font(36, "i"), fill=GREYT)
    if p > 0.4:
        ring(img, (590, 630, 960, 700), t)

def a_flow(img, t, p):
    header(img, "THE FIX", "GlideAjax round trip", p)
    d = ImageDraw.Draw(img)
    steps = [("Client script", "onChange · Requested for", NAVY), ("Script Include", "LeaveRequestHelper", GREEN),
             ("HR profile", "sn_hr_core_profile", AMBER)]
    for i, (a, b, c) in enumerate(steps):
        e = ease((p - i * 0.18) * 4)
        y = 480 + i * 260
        flow_box(img, d, 140, y, 800, 170, a, b, c, e)
        d = ImageDraw.Draw(img)
        if i < 2 and e > 0.8:
            d.polygon([(520, y + 185), (560, y + 185), (540, y + 240)], fill=GREYT)
    if p > 0.7:
        d.text((150, 1260), "← employee type comes back as the answer", font=font(38), fill=GREEN)

def a_client(img, t, p):
    header(img, "STEP 1", "Client script", p, sub="onChange · Requested for")
    hl = {2, 3, 4} if p < 0.6 else {5, 6}
    code(img, (40, 520, 1040, 1080), A_CLIENT, t, hl=hl, title="Client script")
    illus(ImageDraw.Draw(img), 1110)

def a_si(img, t, p):
    header(img, "STEP 2", "Script Include", p, sub="LeaveRequestHelper")
    hl = {2, 3} if p < 0.35 else ({4, 5} if p < 0.7 else {6, 7})
    code(img, (40, 520, 1040, 1140), A_SI, t, hl=hl, title="Script Include")
    illus(ImageDraw.Draw(img), 1170)

def a_gotcha(img, t, p):
    header(img, "2 GOTCHAS", "Don't skip these", p, kicker_color=AMBER)
    d = ImageDraw.Draw(img)
    e1 = ease(p * 4); e2 = ease((p - 0.45) * 4)
    if e1 > 0:
        card(img, (90, 470, 990, 800), border=AMBER)
        d = ImageDraw.Draw(img)
        d.text((130, 500), "1  Client callable", font=font(54), fill=NAVY)
        d.rounded_rectangle([130, 600, 180, 650], 8, outline=NAVY, width=4)
        if p > 0.15:
            d.text((138, 594), "✓", font=tfont("✓", 48), fill=GREEN)
        d.text((200, 600), "GlideAjax enabled", font=font(42, "r"), fill=INK)
        d.text((130, 690), "Without it the call never reaches the server", font=font(34, "i"), fill=GREYT)
    if e2 > 0:
        card(img, (90, 850, 990, 1220), border=AMBER)
        d = ImageDraw.Draw(img)
        d.text((130, 880), "2  Display value", font=font(54), fill=NAVY)
        d.text((130, 980), "getValue()", font=font(36, "m"), fill=RED)
        d.text((480, 980), "→ back-end value", font=font(36, "r"), fill=GREYT)
        d.text((130, 1060), "getDisplayValue()", font=font(36, "m"), fill=GREEN)
        d.text((560, 1060), "→ what users see", font=font(36, "r"), fill=GREYT)

def a_end(img, t, p):
    end_card(img, t, p, "FULL BUILD IN", "EPISODE 1.2", "HR Leave Request series", "Client scripts · GlideAjax · Script Include")

A = dict(lines=A_LINES, scenes=dict(hook=a_hook, flow=a_flow, client=a_client, si=a_si, gotcha=a_gotcha, end=a_end),
         base="hrsd_ep12_shortA_employee_type_glideajax")

# ---------------- SHORT B ----------------
B_LINES = [
    ("hook", "Leave days and remaining balance, calculated the moment the dates change.",
             "Leave days and remaining balance, calculated the moment the dates change."),
    ("read", "On change of end date: read the start and end dates. If either is empty, stop.",
             "onChange of End date: read the start and end dates. If either is empty, stop."),
    ("calc", "Subtract the dates, divide by the milliseconds in a day, round up, and add one so both days count.",
             "Subtract the dates, divide by the milliseconds in a day, round up, and add one so both days count."),
    ("bal",  "Then current balance minus those days gives the remaining balance.",
             "Then current balance minus those days gives the remaining balance."),
    ("bug",  "My first test failed. The browser console showed it straight away: a typo in parse int.",
             "My first test failed. The browser console showed it straight away: a typo in parseInt."),
    ("result", "Fixed. Monday to Friday is five days, and twenty five minus five leaves twenty.",
               "Fixed. Monday to Friday is 5 days, and 25 minus 5 leaves 20."),
    ("note", "This counts calendar days for now. Weekends and holidays come later in the series.",
             "This counts calendar days for now. Weekends and holidays come later in the series."),
    ("end",  "Full build in episode one point two. Follow for more.",
             "Full build in Episode 1.2. Follow for more."),
]
B_CODE = [
    "// onChange: end_date",
    "var s = g_form.getValue('start_date');",
    "var e = g_form.getValue('end_date');",
    "if (!s || !e) return;",
    "var ms = new Date(e) - new Date(s);",
    "var days = Math.ceil(",
    "  ms / (1000 * 60 * 60 * 24)) + 1;",
    "g_form.setValue('leave_duration', days);",
    "var bal = parseInt(g_form.getValue(",
    "  'current_balance'), 10) || 0;",
    "g_form.setValue('remaining_balance',",
    "  bal - days);",
]

def form_card(img, t, p, dur, rem, y0=480, highlight=False):
    card(img, (90, y0, 990, y0 + 760))
    bar(img, (90, y0, 990, y0 + 760), "Leave details")
    d = ImageDraw.Draw(img)
    field(d, 130, y0 + 110, 390, "Start date", "Mon 14", value_kind="b", value_color=NAVY)
    field(d, 560, y0 + 110, 390, "End date", "Fri 18" if dur else "", value_kind="b", value_color=NAVY,
          border=AMBER if dur and highlight else LIGHT)
    field(d, 130, y0 + 280, 390, "Leave duration", str(dur) if dur else "", value_kind="b", value_color=GREEN,
          border=GREEN if dur else LIGHT)
    field(d, 560, y0 + 280, 390, "Current balance", "25", value_kind="b", value_color=NAVY)
    field(d, 130, y0 + 450, 820, "Remaining balance", str(rem) if rem is not None else "", value_kind="b",
          value_color=GREEN, border=GREEN if rem is not None else LIGHT)
    d.text((130, y0 + 650), "Illustrative values", font=font(28, "i"), fill=GREYT)

def b_hook(img, t, p):
    d = ImageDraw.Draw(img)
    text_c(d, 210, "LEAVE DAYS", 96, NAVY)
    text_c(d, 310, "CALCULATED LIVE", 96, GREEN)
    e = ease((p - 0.3) * 3)
    form_card(img, t, p, 5 if e > 0.5 else None, 20 if e > 0.5 else None, y0=470, highlight=True)

def b_read(img, t, p):
    header(img, "STEP 1", "Read both dates", p, sub="onChange · End date")
    code(img, (40, 520, 1040, 1250), B_CODE, t, hl={1, 2, 3}, title="Client script", reveal=0.35 + 0.65 * ease(p))
    illus(ImageDraw.Draw(img), 1280)

def b_calc(img, t, p):
    header(img, "STEP 2", "Count the days", p, sub="+1 so both days count")
    code(img, (40, 520, 1040, 1250), B_CODE, t, hl={4, 5, 6, 7}, title="Client script")
    illus(ImageDraw.Draw(img), 1280)

def b_bal(img, t, p):
    header(img, "STEP 3", "Remaining balance", p)
    code(img, (40, 520, 1040, 1250), B_CODE, t, hl={8, 9, 10, 11}, title="Client script")
    illus(ImageDraw.Draw(img), 1280)

def b_bug(img, t, p):
    header(img, "WHEN IT BREAKS", "Check the browser console", p, kicker_color=RED)
    card(img, (60, 500, 1020, 1000), fill=(32, 33, 36), border=(60, 64, 70))
    d = ImageDraw.Draw(img)
    d.text((100, 530), "Console", font=font(36), fill=(200, 200, 205))
    d.line([(60, 590), (1020, 590)], fill=(60, 64, 70), width=2)
    e = ease((p - 0.2) * 4)
    if e > 0:
        d.rectangle([62, 620, 1018, 760], fill=(78, 30, 34))
        d.text((90, 640), "✗", font=tfont("✗", 40), fill=(255, 110, 110))
        d.text((140, 640), "ReferenceError:", font=font(32, "m"), fill=(255, 140, 140))
        d.text((140, 690), "parsInt is not defined", font=font(32, "m"), fill=(255, 140, 140))
    if p > 0.55:
        d.text((90, 820), "Fix:  parsInt  →  parseInt", font=font(38, "m"), fill=(140, 230, 160))
    d = ImageDraw.Draw(img)
    d.text((90, 1040), "Right-click → Inspect → Console", font=font(40), fill=NAVY)
    d.text((90, 1100), "Illustrative error text", font=font(28, "i"), fill=GREYT)

def b_result(img, t, p):
    header(img, "RESULT", "Mon → Fri = 5 days", p, kicker_color=GREEN)
    form_card(img, t, p, 5, 20, y0=470)
    if p > 0.3:
        ring(img, (130, 794, 520, 878), t, color=GREEN)
        ring(img, (130, 964, 950, 1048), t, color=GREEN)

def b_note(img, t, p):
    header(img, "GOOD TO KNOW", "Calendar days, for now", p, kicker_color=AMBER)
    d = ImageDraw.Draw(img)
    days = ["M", "T", "W", "T", "F", "S", "S"]
    for i, dd in enumerate(days):
        x = 110 + i * 125
        weekend = i >= 5
        e = ease((p - i * 0.06) * 5)
        if e <= 0:
            continue
        d.rounded_rectangle([x, 560, x + 105, 680], 16, fill=LIGHT if weekend else WHITE, outline=AMBER if weekend else GREEN, width=4)
        w_ = d.textlength(dd, font=font(56)); d.text((x + (105 - w_) / 2, 585), dd, font=font(56), fill=GREYT if weekend else NAVY)
    if p > 0.5:
        text_c(d, 760, "Fri → Mon counts the weekend too", 46, NAVY)
        text_c(d, 840, "Working days & holidays: later in the series", 40, GREYT, "i")

def b_end(img, t, p):
    end_card(img, t, p, "FULL BUILD IN", "EPISODE 1.2", "HR Leave Request series", "Duration · balance · debugging")

B = dict(lines=B_LINES, scenes=dict(hook=b_hook, read=b_read, calc=b_calc, bal=b_bal, bug=b_bug, result=b_result, note=b_note, end=b_end),
         base="hrsd_ep12_shortB_leave_duration_balance")

if __name__ == "__main__":
    spec = {"A": A, "B": B}[sys.argv[1]]
    here = os.path.join(HERE, sys.argv[1])
    os.makedirs(here, exist_ok=True)
    print(render(spec["lines"], spec["scenes"], here, spec["base"]))

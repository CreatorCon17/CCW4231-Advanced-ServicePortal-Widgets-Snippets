"""HRSD Ep 2 Shorts (PPT style, voice 9).
A = No-manager guard.  B = Ask for Approval: manager pill + rejection rule.  C = HRSD requests, the HRIS records.
Usage: python ep2_shorts.py A|B|C [preview]"""
import math, os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pptstyle import *
import snlib as S
from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))

def illus(d, y):
    d.text((90, y), "Illustrative UI: labels may differ on your release", font=font(28, "i"), fill=GREYT)

def step(img, x, y, w, num, title, sub, color, e=1.0, dim=False, h=150):
    """A Flow Designer-like step row."""
    if e <= 0:
        return
    x += int(40 * (1 - e))
    card(img, (x, y, x + w, y + h), fill=(246, 247, 250) if dim else WHITE, border=color if not dim else LIGHT)
    d = ImageDraw.Draw(img)
    d.rectangle([x, y, x + 12, y + h], fill=color if not dim else LIGHT)
    if num:
        d.ellipse([x + 34, y + 30, x + 94, y + 90], fill=color if not dim else LIGHT)
        nw = d.textlength(num, font=font(36))
        d.text((x + 64 - nw / 2, y + 38), num, font=font(36), fill=WHITE)
        tx = x + 120
    else:
        tx = x + 40
    d.text((tx, y + 26), title, font=font(42), fill=GREYT if dim else NAVY)
    if sub:
        d.text((tx, y + 84), sub, font=font(32, "r"), fill=GREYT)

def pill_chain(img, x, y, parts, p, color=GREEN, size=34):
    """Data pill chain revealed segment by segment."""
    d = ImageDraw.Draw(img)
    n = max(1, int(len(parts) * min(1.0, p) + 0.999))
    for i, s in enumerate(parts[:n]):
        w_ = d.textlength(s, font=font(size)) + 36
        if x + w_ > W - 60:
            x, y = 110, y + size + 46
        d.rounded_rectangle([x, y, x + w_, y + size + 22], 22, fill=color if i == len(parts) - 1 else (232, 240, 234),
                            outline=color, width=3)
        d.text((x + 18, y + 9), s, font=font(size), fill=WHITE if i == len(parts) - 1 else NAVY)
        x += w_ + 12
        if i < len(parts) - 1 and i < n - 1:
            d.text((x - 4, y + 6), "›", font=font(size + 6), fill=GREYT)
            x += 22
    return y

# ======================= SHORT A: no-manager guard =======================
A_LINES = [
    ("hook", "Your leave approval is stuck forever. Because the employee has no manager.",
             "Your leave approval is stuck forever. Because the employee has no manager."),
    ("why", "Contractors, new joiners, data that hasn't synced yet. If the manager is empty, the approval has nowhere to go.",
            "Contractors, new joiners, data that hasn't synced yet. If the manager is empty, the approval has nowhere to go."),
    ("guard", "The fix, in Flow Designer. Before ask for approval, add an if. Requested for, manager, is empty.",
              "The fix, in Flow Designer. Before Ask for Approval, add an If: Requested for › Manager is empty."),
    ("inside", "Inside the if, update the H R case. Assign it to the leave management team, and add a work note saying why. Then, end flow.",
               "Inside the If, update the HR case. Assign it to the Leave Management team, add a work note saying why. Then End Flow."),
    ("result", "Now, no manager means the case goes straight to H R, with the reason. Nothing stuck.",
               "Now, no manager means the case goes straight to HR, with the reason. Nothing stuck."),
    ("end", "Full build in episode two of the H R leave request series. Follow for more.",
            "Full build in Episode 2 of the HR Leave Request series. Follow for more."),
]

def a_hook(img, t, p):
    d = ImageDraw.Draw(img)
    text_c(d, 210, "APPROVAL STUCK?", 104, NAVY)
    w_ = d.textlength("NO MANAGER ON THE USER", font=font(46)) + 40
    chip(d, (W - w_) / 2, 345, "NO MANAGER ON THE USER", AMBER, size=46, fg=NAVY)
    card(img, (90, 520, 990, 1120))
    bar(img, (90, 520, 990, 1120), "Approval · HR Case")
    d = ImageDraw.Draw(img)
    field(d, 140, 640, 800, "Approver", "", border=RED)
    d.text((165, 712), "(empty)", font=font(38, "i"), fill=RED)
    field(d, 140, 820, 800, "State", "")
    dots = "." * (1 + int(t * 3) % 3)
    d.text((165, 892), "Requested · waiting" + dots, font=font(38, "r"), fill=INK)
    d.text((140, 1010), "Day 1 … Day 5 … still waiting", font=font(36, "i"), fill=GREYT)
    if p > 0.35:
        ring(img, (140, 684, 940, 768), t, color=RED)

def a_why(img, t, p):
    header(img, "WHY IT HAPPENS", "No manager on the record", p, kicker_color=AMBER)
    for i, (a, b) in enumerate([("Contractors", "often no manager set"), ("New joiners", "not set up yet"),
                                ("Data not synced", "HR feed hasn't run")]):
        step(img, 110, 470 + i * 200, 860, str(i + 1), a, b, AMBER, ease((p - i * 0.15) * 4))
    d = ImageDraw.Draw(img)
    if p > 0.6:
        text_c(d, 1110, "Manager empty → approval goes nowhere", 46, RED)

def a_guard(img, t, p):
    header(img, "THE FIX", "Flow Designer", p, kicker_color=GREEN)
    step(img, 70, 450, 940, "", "Trigger: HR Case created", "HR Service is Leave Request", NAVY)
    step(img, 70, 640, 940, "1", "If", "", AMBER, ease((p - 0.1) * 4))
    if p > 0.25:
        pill_chain(img, 200, 735, ["Requested for", "Manager"], (p - 0.25) * 3, color=AMBER)
        d = ImageDraw.Draw(img)
        d.text((640, 739), "is empty", font=font(38), fill=RED)
    step(img, 70, 840, 940, "2", "Ask For Approval", "comes after the guard", NAVY, ease((p - 0.4) * 4), dim=True)
    if p > 0.55:
        ring(img, (70, 640, 1010, 790), t)
    illus(ImageDraw.Draw(img), 1040)

def a_inside(img, t, p):
    header(img, "INSIDE THE IF", "Route it, explain it, stop", p, kicker_color=GREEN)
    step(img, 70, 450, 940, "1", "If  Manager is empty", "", AMBER, h=110)
    step(img, 150, 600, 860, "", "Update Record · HR Case", "Assignment group = Leave Management Team", GREEN, ease((p - 0.05) * 4))
    step(img, 150, 790, 860, "", "Work note", "\"No manager on profile — routed to HR\"", GREEN, ease((p - 0.35) * 4))
    if p > 0.7:
        d = ImageDraw.Draw(img)
        chip(d, 150, 985, "END FLOW", RED, size=46)
        d.text((420, 995), "nothing waits on an empty approver", font=font(34, "i"), fill=GREYT)
    illus(ImageDraw.Draw(img), 1110)

def a_result(img, t, p):
    header(img, "RESULT", "Nothing stuck", p, kicker_color=GREEN)
    card(img, (90, 470, 990, 1110))
    bar(img, (90, 470, 990, 1110), "HR Case")
    d = ImageDraw.Draw(img)
    field(d, 140, 590, 800, "Assignment group", "Leave Management Team", value_color=NAVY)
    field(d, 140, 760, 800, "Work notes", "")
    d.text((165, 832), "No manager on profile — routed to HR", font=font(34, "r"), fill=INK)
    d.text((140, 940), "Manual approval by the HR team", font=font(36, "i"), fill=GREYT)
    if p > 0.3:
        ring(img, (140, 634, 940, 718), t, color=GREEN)
    illus(ImageDraw.Draw(img), 1140)

def a_end(img, t, p):
    end_card(img, t, p, "FULL BUILD IN", "EPISODE 2", "HR Leave Request series", "Approval · guard · HR handoff")

A = dict(lines=A_LINES, scenes=dict(hook=a_hook, why=a_why, guard=a_guard, inside=a_inside, result=a_result, end=a_end),
         base="hrsd_ep2_shortA_no_manager_guard")

# ======================= SHORT B: approver = manager + rejection rule =======================
B_LINES = [
    ("hook", "Don't hard-code the approver. Use the requester's manager.",
             "Don't hard-code the approver. Use the requester's manager."),
    ("pill", "In ask for approval, approve when anyone approves. For the approver, use the data pill: trigger, H R case, requested for, manager.",
             "In Ask for Approval: approve when Anyone approves. Approver = data pill: Trigger › HR Case › Requested for › Manager."),
    ("reject", "Then add a rejection rule too. Reject when anyone rejects. ServiceNow's docs recommend it, so the flow doesn't sit waiting.",
               "Then add a rejection rule too: reject when Anyone rejects. ServiceNow docs recommend it, so the flow doesn't sit waiting."),
    ("branch", "After the approval: if approved, assign it to the leave management team. Otherwise, close it as rejected.",
               "After the approval: if Approved, assign to the Leave Management team. Otherwise, close it as rejected."),
    ("journal", "And set the journal field to work notes, so the decision shows up in the case history.",
                "And set the journal field to Work notes, so the decision shows up in the case history."),
    ("end", "Full build in episode two of the H R leave request series. Follow for more.",
            "Full build in Episode 2 of the HR Leave Request series. Follow for more."),
]

def b_hook(img, t, p):
    d = ImageDraw.Draw(img)
    text_c(d, 210, "WHO APPROVES?", 104, NAVY)
    card(img, (90, 420, 990, 700), border=RED)
    d = ImageDraw.Draw(img)
    d.text((140, 455), "✗", font=tfont("✗", 60), fill=RED)
    d.text((220, 455), "Hard-coded user", font=font(54), fill=NAVY)
    d.text((220, 540), "breaks when people change roles", font=font(36, "i"), fill=GREYT)
    e = ease((p - 0.35) * 4)
    if e > 0:
        card(img, (90, 760, 990, 1100), border=GREEN)
        d = ImageDraw.Draw(img)
        d.text((140, 795), "✓", font=tfont("✓", 60), fill=GREEN)
        d.text((220, 795), "Requester's manager", font=font(54), fill=NAVY)
        pill_chain(img, 220, 900, ["Requested for", "Manager"], (p - 0.35) * 3)

def b_pill(img, t, p):
    header(img, "ASK FOR APPROVAL", "Approval rule", p)
    card(img, (60, 470, 1020, 1100))
    d = ImageDraw.Draw(img)
    d.text((110, 510), "Approve when", font=font(34, "r"), fill=GREYT)
    chip(d, 110, 560, "Anyone approves", GREEN, size=40)
    d.text((110, 680), "Users", font=font(34, "r"), fill=GREYT)
    pill_chain(img, 110, 730, ["Trigger", "HR Case Record", "Requested for", "Manager"], p * 1.6)
    if p > 0.65:
        ring(img, (100, 736, 1000, 800), t, color=GREEN)
    illus(ImageDraw.Draw(img), 1130)

def b_reject(img, t, p):
    header(img, "ADD THIS TOO", "Rejection rule", p, kicker_color=AMBER)
    card(img, (60, 470, 1020, 950), border=AMBER)
    d = ImageDraw.Draw(img)
    d.text((110, 510), "Reject when", font=font(34, "r"), fill=GREYT)
    chip(d, 110, 560, "Anyone rejects", RED, size=40)
    d.text((110, 680), "Users", font=font(34, "r"), fill=GREYT)
    pill_chain(img, 110, 730, ["Requested for", "Manager"], 1.0)
    if p > 0.45:
        d = ImageDraw.Draw(img)
        text_c(d, 1000, "Docs: add rejection rules so the", 40, NAVY)
        text_c(d, 1055, "flow doesn't stay in a waiting state", 40, NAVY)
    if p > 0.2:
        ring(img, (108, 566, 420, 622), t)
    illus(ImageDraw.Draw(img), 1140)

def b_branch(img, t, p):
    header(img, "AFTER THE APPROVAL", "Two branches", p)
    step(img, 70, 450, 940, "", "If  Approval State is Approved", "", NAVY, h=110)
    step(img, 150, 590, 860, "", "Update HR Case", "Leave Management Team · Work in Progress", GREEN, ease((p - 0.05) * 4))
    step(img, 70, 790, 940, "", "Else", "", NAVY, ease((p - 0.4) * 4), h=110)
    step(img, 150, 930, 860, "", "Update HR Case", "Closed Incomplete · Rejected by manager", RED, ease((p - 0.5) * 4))
    illus(ImageDraw.Draw(img), 1110)

def b_journal(img, t, p):
    header(img, "AUDIT TRAIL", "Journal field = Work notes", p, kicker_color=GREEN)
    card(img, (90, 470, 990, 1050))
    bar(img, (90, 470, 990, 1050), "HR Case · Activity")
    d = ImageDraw.Draw(img)
    e = ease((p - 0.15) * 4)
    if e > 0:
        d.rounded_rectangle([140, 600, 940, 800], 14, fill=(255, 251, 230), outline=AMBER, width=3)
        d.text((170, 620), "Work notes · Manager", font=font(34), fill=NAVY)
        d.text((170, 680), "Approval: Approved", font=font(40, "r"), fill=INK)
        d.text((170, 740), "comments land on the case", font=font(30, "i"), fill=GREYT)
    if p > 0.5:
        d.text((140, 860), "Who decided, and when: on the record", font=font(38), fill=GREEN)
    illus(ImageDraw.Draw(img), 1080)

def b_end(img, t, p):
    end_card(img, t, p, "FULL BUILD IN", "EPISODE 2", "HR Leave Request series", "Flow Designer approvals")

B = dict(lines=B_LINES, scenes=dict(hook=b_hook, pill=b_pill, reject=b_reject, branch=b_branch, journal=b_journal, end=b_end),
         base="hrsd_ep2_shortB_manager_approval_rejection_rule")

# ======================= SHORT C: HRSD requests, the HRIS records =======================
C_LINES = [
    ("hook", "Stop making H R S D the system of record for leave.",
             "Stop making HRSD the system of record for leave."),
    ("hrsd", "H R S D owns the request, the approval decision, and the audit trail.",
             "HRSD owns the request, the approval decision, and the audit trail."),
    ("hris", "The H R I S, Workday, SAP, or whatever your client runs, owns the leave balance, and payroll.",
             "The HRIS (Workday, SAP, or whatever your client runs) owns the leave balance, and payroll."),
    ("why", "Make H R S D the record, and payroll, finance, and auditors will all fight you.",
            "Make HRSD the record, and payroll, finance, and auditors will all fight you."),
    ("handoff", "So after approval, the leave is recorded in the H R I S, and the H R I S reference comes back to the case.",
                "So after approval, the leave is recorded in the HRIS, and the HRIS reference comes back to the case."),
    ("rule", "H R S D requests. The H R I S records.",
             "HRSD requests. The HRIS records."),
    ("end", "Full build in episode two of the H R leave request series. Follow for more.",
            "Full build in Episode 2 of the HR Leave Request series. Follow for more."),
]

def two_boxes(img, t, hl):
    for i, (x0, title, color, items) in enumerate([(70, "HRSD", NAVY, ["Request", "Approval decision", "Audit trail"]),
                                                   (560, "HRIS", GREEN, ["Leave balance", "Payroll", "Workday · SAP · other"])]):
        on = hl in (i, 2)
        card(img, (x0, 470, x0 + 450, 1090), border=color if on else LIGHT, fill=WHITE if on else (246, 247, 250))
        d = ImageDraw.Draw(img)
        d.rounded_rectangle([x0, 470, x0 + 450, 570], 22, fill=color if on else LIGHT)
        d.rectangle([x0, 530, x0 + 450, 570], fill=color if on else LIGHT)
        w_ = d.textlength(title, font=font(56))
        d.text((x0 + (450 - w_) / 2, 487), title, font=font(56), fill=WHITE if on else GREYT)
        for j, it in enumerate(items):
            d.text((x0 + 40, 620 + j * 120), it, font=font(40 if j < 2 or i == 0 else 34, "b" if on else "r"),
                   fill=INK if on else GREYT)
        if on and hl != 2:
            ring(img, (x0, 470, x0 + 450, 1090), t, color=AMBER)

def c_hook(img, t, p):
    d = ImageDraw.Draw(img)
    text_c(d, 260, "HRSD", 150, NAVY)
    text_c(d, 450, "≠ system of record", 84, RED)
    w_ = d.textlength("FOR LEAVE", font=font(50)) + 40
    chip(d, (W - w_) / 2, 590, "FOR LEAVE", AMBER, size=50, fg=NAVY)
    if p > 0.3:
        card(img, (140, 780, 940, 1080), border=RED)
        d = ImageDraw.Draw(img)
        d.text((190, 820), "HRSD = leave balance", font=font(54), fill=GREYT)
        d.line([(180, 860), (900, 860)], fill=RED, width=8)
        d.text((190, 930), "a common design mistake", font=font(40, "i"), fill=RED)

def c_hrsd(img, t, p):
    header(img, "TWO SYSTEMS", "Two jobs", p)
    two_boxes(img, t, 0)

def c_hris(img, t, p):
    header(img, "TWO SYSTEMS", "Two jobs", p)
    two_boxes(img, t, 1)

def c_why(img, t, p):
    header(img, "WHY NOT HRSD?", "They'll all fight you", p, kicker_color=RED)
    for i, (a, b) in enumerate([("Payroll", "pays from the HRIS balance"), ("Finance", "reports from the HRIS"),
                                ("Auditors", "want one system of record")]):
        step(img, 110, 470 + i * 200, 860, str(i + 1), a, b, RED, ease((p - i * 0.15) * 4))

def c_handoff(img, t, p):
    header(img, "THE HANDOFF", "Each points at the other", p, kicker_color=GREEN)
    d = ImageDraw.Draw(img)
    for x0, title, color in [(70, "HRSD", NAVY), (630, "HRIS", GREEN)]:
        card(img, (x0, 520, x0 + 380, 700), border=color)
        d = ImageDraw.Draw(img)
        w_ = d.textlength(title, font=font(64)); d.text((x0 + (380 - w_) / 2, 572), title, font=font(64), fill=color)
    e1, e2 = ease((p - 0.1) * 3), ease((p - 0.45) * 3)
    if e1 > 0:
        x1 = 460 + int(160 * e1)
        d.line([(460, 750), (x1, 750)], fill=NAVY, width=8)
        d.polygon([(x1, 735), (x1 + 24, 750), (x1, 765)], fill=NAVY)
        d.text((150, 790), "approved leave →", font=font(40), fill=NAVY)
    if e2 > 0:
        x1 = 620 - int(160 * e2)
        d.line([(x1, 900), (620, 900)], fill=GREEN, width=8)
        d.polygon([(x1, 885), (x1 - 24, 900), (x1, 915)], fill=GREEN)
        d.text((480, 940), "← HRIS reference", font=font(40), fill=GREEN)
    if p > 0.75:
        chip(d, 110, 1080, "Episode 2: by hand", AMBER, size=40, fg=NAVY)
        chip(d, 560, 1080, "Episode 3: REST", GREEN, size=40)

def c_rule(img, t, p):
    d = ImageDraw.Draw(img)
    a = ease(p * 4)
    text_c(d, 560 - 30 * (1 - a), "HRSD requests.", 110, NAVY)
    if p > 0.35:
        text_c(d, 740, "The HRIS records.", 110, GREEN)
    if p > 0.6:
        d.rectangle([W / 2 - 160, 930, W / 2 - 10, 942], fill=GREEN)
        d.rectangle([W / 2 + 10, 930, W / 2 + 160, 942], fill=AMBER)

def c_end(img, t, p):
    end_card(img, t, p, "FULL BUILD IN", "EPISODE 2", "HR Leave Request series", "HRSD + HRIS: who owns what")

C = dict(lines=C_LINES, scenes=dict(hook=c_hook, hrsd=c_hrsd, hris=c_hris, why=c_why, handoff=c_handoff, rule=c_rule, end=c_end),
         base="hrsd_ep2_shortC_hrsd_requests_hris_records")

if __name__ == "__main__":
    spec = {"A": A, "B": B, "C": C}[sys.argv[1]]
    here = os.path.join(HERE, sys.argv[1])
    os.makedirs(here, exist_ok=True)
    print(render(spec["lines"], spec["scenes"], here, spec["base"]))

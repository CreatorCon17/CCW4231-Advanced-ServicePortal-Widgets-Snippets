"""Concept Shorts (PPT style, voice 9), 60-75 s each.
1 = Where attachments actually live (table inheritance).  2 = Why a browser can't put files in folders.
3 = Output became input (reading and writing the same set).
Usage: python concept_shorts.py 1|2|3 [preview]"""
import math, os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pptstyle import *
import snlib as S
from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))

def code(img, box, lines, t, hl=(), title="Background script", size=30, reveal=1.0):
    S.code_card(img, box, lines, t, hl=set(hl), size=size, title=title, reveal=reveal)

def note(d, y, s="Illustrative table names: the pattern is what matters"):
    d.text((90, y), s, font=font(28, "i"), fill=GREYT)

def step(img, x, y, w, num, title, sub, color, e=1.0, h=150):
    if e <= 0:
        return
    x += int(40 * (1 - e))
    card(img, (x, y, x + w, y + h), border=color)
    d = ImageDraw.Draw(img)
    d.rectangle([x, y, x + 12, y + h], fill=color)
    tx = x + 40
    if num:
        d.ellipse([x + 34, y + 30, x + 94, y + 90], fill=color)
        nw = d.textlength(num, font=font(36)); d.text((x + 64 - nw / 2, y + 38), num, font=font(36), fill=WHITE)
        tx = x + 120
    d.text((tx, y + 26), title, font=font(42), fill=NAVY)
    if sub:
        d.text((tx, y + 84), sub, font=font(32, "r"), fill=GREYT)

def takeaway(img, t, p, l1, l2, color=GREEN, y=520):
    card(img, (70, y, 1010, y + 430), border=color)
    d = ImageDraw.Draw(img)
    d.rectangle([70, y, 86, y + 430], fill=color)
    a = ease(p * 4)
    text_c(d, y + 90 - 20 * (1 - a), l1, 62, NAVY)
    if p > 0.25:
        text_c(d, y + 190, l2, 62, color)

# ============================ SHORT 1: where attachments live ============================
L1 = [
    ("hook", "Your attachment query returns zero rows. But you can see the files, right there on the record. Here's what's actually happening.",
             "Your attachment query returns zero rows. But you can see the files, right there on the record. Here's what's actually happening."),
    ("setup", "You've got an H R case with three attachments. You write the obvious query. Table name is H R case, and table sys I D is the case.",
              "You've got an HR case with three attachments. You write the obvious query: table_name is hr_case, table_sys_id is the case."),
    ("zero", "Zero rows. No error. And the files are right there.",
             "Zero rows. No error. And the files are right there."),
    ("tree", "Here's the thing. H R case tables are extended. There's a parent table, and specific case types extend it.",
             "Here's the thing. HR case tables are extended. There's a parent table, and specific case types extend it."),
    ("tree2", "When a file is attached, the platform records the table the record actually lives on. The child, not the parent.",
              "When a file is attached, the platform records the table the record actually lives on. The child, not the parent."),
    ("tree3", "So your filter compares the parent name with the child name. It never matches. And because it's a filter, not an error, you get silence.",
              "So your filter compares the parent name with the child name. It never matches. And because it's a filter, not an error, you get silence."),
    ("fix", "The fix. Drop the table name, and query by the record's sys I D.",
            "The fix: drop the table name, and query by the record's sys_id."),
    ("guid", "A sys I D is a generated GUID. Nothing else in the instance will match it. The table name wasn't adding safety. It was only adding a way to fail.",
             "A sys_id is a generated GUID. Nothing else in the instance will match it. The table name wasn't adding safety, only a way to fail."),
    ("catch", "One catch. Files in image or attachment fields are stored with a Z Z, Y Y prefix on the table name. Exclude those, if you only want the files users attached.",
              "One catch: files in image or attachment fields are stored with a ZZ_YY prefix on the table name. Exclude those if you only want the files users attached."),
    ("lesson", "And the lesson is bigger than attachments. Any time you filter by table name on an extended table, ask which table the platform actually wrote. Usually, it's the child.",
               "The lesson is bigger than attachments. Any time you filter by table name on an extended table, ask which table the platform actually wrote. Usually, the child."),
    ("end", "Follow ServiceNow Simplified for more.", "Follow ServiceNow Simplified for more."),
]
Q_BAD = [
    "var ga = new GlideRecord('sys_attachment');",
    "ga.addQuery('table_name', 'hr_case');",
    "ga.addQuery('table_sys_id', caseSysId);",
    "ga.query();",
    "gs.info(ga.getRowCount());   // 0",
]
Q_GOOD = [
    "var ga = new GlideRecord('sys_attachment');",
    "ga.addQuery('table_sys_id', caseSysId);",
    "ga.query();",
]
Q_CATCH = [
    "var ga = new GlideRecord('sys_attachment');",
    "ga.addQuery('table_sys_id', caseSysId);",
    "// skip files stored in image/attachment fields",
    "ga.addQuery('table_name',",
    "            'DOES NOT CONTAIN', 'ZZ_YY');",
    "ga.query();",
]

def tree(img, t, p, stage):
    d = ImageDraw.Draw(img)
    rows = [("task", 0, LIGHT, ""), ("hr_case", 1, NAVY, "← what you queried"), ("hr_case_travel", 2, GREEN, "← record lives here")]
    for i, (name, lvl, color, lab) in enumerate(rows):
        e = ease((p - i * 0.12) * 4) if stage == 0 else 1.0
        if e <= 0:
            continue
        x, y = 110 + lvl * 110, 480 + i * 190
        if lvl:
            d.line([(x - 60, y - 70), (x - 60, y + 60), (x - 4, y + 60)], fill=GREYT, width=5)
        w_ = d.textlength(name, font=font(44, "m")) + 60
        d.rounded_rectangle([x, y + 20, x + w_, y + 100], 16, fill=WHITE, outline=color if color != LIGHT else GREYT, width=4)
        d.text((x + 30, y + 37), name, font=font(44, "m"), fill=NAVY if lvl else GREYT)
        if stage >= 1 and lab:
            d.text((x + w_ + 20, y + 42), lab, font=font(34), fill=color)
    if stage >= 1:
        e = ease(p * 3)
        card(img, (110, 1100, 970, 1260), border=GREEN)
        d = ImageDraw.Draw(img)
        d.text((150, 1125), "sys_attachment.table_name", font=font(34, "m"), fill=GREYT)
        d.text((150, 1180), "= 'hr_case_travel'", font=font(40, "m"), fill=GREEN)
        if stage == 1 and p > 0.4:
            ring(img, (110, 1100, 970, 1260), t, color=GREEN)
    if stage == 2:
        d = ImageDraw.Draw(img)
        if p > 0.15:
            text_c(d, 1290, "'hr_case'  ≠  'hr_case_travel'", 46, RED)
    note(ImageDraw.Draw(img), 1360)

def s1_hook(img, t, p):
    d = ImageDraw.Draw(img)
    text_c(d, 210, "0 ROWS", 140, RED)
    w_ = d.textlength("BUT THE FILES ARE RIGHT THERE", font=font(44)) + 40
    chip(d, (W - w_) / 2, 390, "BUT THE FILES ARE RIGHT THERE", AMBER, size=44, fg=NAVY)
    card(img, (90, 540, 990, 1080))
    bar(img, (90, 540, 990, 1080), "HR case · Attachments (3)")
    d = ImageDraw.Draw(img)
    for i, f_ in enumerate(["ticket.pdf", "invoice.pdf", "receipt.pdf"]):
        y = 670 + i * 120
        d.rounded_rectangle([140, y, 940, y + 90], 14, fill=WHITE, outline=LIGHT, width=3)
        d.rectangle([165, y + 20, 205, y + 70], fill=RED)
        d.text((235, y + 22), f_, font=font(42), fill=INK)

def s1_setup(img, t, p):
    header(img, "THE OBVIOUS QUERY", "Looks right", p)
    code(img, (40, 480, 1040, 1000), Q_BAD[:4], t, hl={1, 2} if p > 0.2 else ())
    note(ImageDraw.Draw(img), 1030)

def s1_zero(img, t, p):
    header(img, "RESULT", "Zero rows. No error.", p, kicker_color=RED)
    code(img, (40, 480, 1040, 1070), Q_BAD, t, hl={4})
    note(ImageDraw.Draw(img), 1100)

def s1_tree(img, t, p):
    header(img, "TABLE INHERITANCE", "Extended tables", p)
    tree(img, t, p, 0)

def s1_tree2(img, t, p):
    header(img, "WHAT GETS STORED", "The child table", p, kicker_color=GREEN)
    tree(img, t, p, 1)

def s1_tree3(img, t, p):
    header(img, "WHY IT'S SILENT", "A filter, not an error", p, kicker_color=RED)
    tree(img, t, p, 2)

def s1_fix(img, t, p):
    header(img, "THE FIX", "Drop the table name", p, kicker_color=GREEN)
    code(img, (40, 480, 1040, 880), Q_GOOD, t, hl={1})
    d = ImageDraw.Draw(img)
    if p > 0.4:
        text_c(d, 930, "3 rows", 80, GREEN)

def s1_guid(img, t, p):
    header(img, "WHY IT'S SAFE", "sys_id is a GUID", p, kicker_color=GREEN)
    takeaway(img, t, p, "sys_id is a GUID.", "The table name adds nothing.", y=480)
    d = ImageDraw.Draw(img)
    d.text((110, 980), "a1b2c3d4e5f60718293a4b5c6d7e8f90", font=font(40, "m"), fill=GREYT)
    d.text((110, 1040), "32 hex characters, generated per record (illustrative)", font=font(30, "i"), fill=GREYT)

def s1_catch(img, t, p):
    header(img, "ONE CATCH", "ZZ_YY field files", p, kicker_color=AMBER)
    code(img, (40, 480, 1040, 1100), Q_CATCH, t, hl={2, 3, 4} if p > 0.25 else (), size=29)
    d = ImageDraw.Draw(img)
    d.text((90, 1130), "Image / attachment-type fields use the ZZ_YY prefix", font=font(32), fill=NAVY)

def s1_lesson(img, t, p):
    header(img, "THE LESSON", "Bigger than attachments", p, kicker_color=GREEN)
    takeaway(img, t, p, "Filtering by table name?", "Which table was written?", y=480)
    d = ImageDraw.Draw(img)
    if p > 0.6:
        text_c(d, 1000, "Usually the child. Not the one you typed.", 44, NAVY)

def s1_end(img, t, p):
    end_card(img, t, p, "CONCEPTS, NOT", "TRICKS", "ServiceNow Simplified", "Table inheritance · sys_attachment")

SPEC1 = dict(lines=L1, base="concept1_where_attachments_live",
             scenes=dict(hook=s1_hook, setup=s1_setup, zero=s1_zero, tree=s1_tree, tree2=s1_tree2, tree3=s1_tree3,
                         fix=s1_fix, guid=s1_guid, catch=s1_catch, lesson=s1_lesson, end=s1_end))

# ============================ SHORT 2: browser folders ============================
L2 = [
    ("hook", "Download each record's files into its own folder. And no zip. You can't build this in a browser. Here's why.",
             "\"Download each record's files into its own folder. And no zip.\" You can't build this in a browser. Here's why."),
    ("req", "Sounds reasonable. Bulk export, one folder per record. Every part is possible, except the folders.",
            "Sounds reasonable. Bulk export, one folder per record. Every part is possible, except the folders."),
    ("bytes", "A web page can't touch your file system. When you click download, the page isn't writing a file. It hands bytes to the browser, and the browser decides.",
              "A web page can't touch your file system. When you click download, the page isn't writing a file. It hands bytes to the browser, and the browser decides."),
    ("name", "Your code doesn't choose the location, or the folder. It can suggest a file name, and even that can be overridden.",
             "Your code doesn't choose the location, or the folder. It can suggest a file name, and even that can be overridden."),
    ("sec", "There's no A P I for, create a folder here. Because letting any website create folders on your disk would be a security problem.",
            "There's no API for \"create a folder here\". Because letting any website create folders on your disk would be a security problem."),
    ("opts", "Inside the browser, you have three options. A zip file, which works everywhere. Flat downloads, with no structure. Or the File System Access A P I.",
             "Inside the browser, you have three options. A zip file, which works everywhere. Flat downloads, no structure. Or the File System Access API."),
    ("opt3", "Only that one makes real folders. And it's Chrome and Edge only. No Firefox, no Safari, no mobile. There's a permission prompt, and I T can switch it off.",
             "Only that one makes real folders. And it's Chrome and Edge only. No Firefox, no Safari, no mobile. There's a permission prompt, and IT can switch it off."),
    ("answer", "Folders, no zip, works for everyone? In a browser, the honest answer is no. Say it in week one. If folders are a must, plan a server side export.",
               "So: folders, no zip, works for everyone? In a browser, the honest answer is no. Say it in week one. If folders are a must, plan a server-side export."),
    ("lesson", "Knowing where a platform's boundary sits is worth more than one more A P I. Scope the story right, instead of finding the problem in U A T.",
               "Knowing where a platform's boundary sits is worth more than one more API. Scope the story right, instead of finding the problem in UAT."),
    ("end", "Follow ServiceNow Simplified for more.", "Follow ServiceNow Simplified for more."),
]

def folder(d, x, y, label, color=AMBER, w=260):
    d.rounded_rectangle([x, y, x + 110, y + 40], 10, fill=color)
    d.rounded_rectangle([x, y + 24, x + w, y + 170], 14, fill=color)
    d.text((x + 24, y + 70), label, font=font(36), fill=NAVY)

def s2_hook(img, t, p):
    d = ImageDraw.Draw(img)
    text_c(d, 200, "FOLDERS. NO ZIP.", 104, NAVY)
    w_ = d.textlength("NOT POSSIBLE IN A BROWSER", font=font(46)) + 40
    chip(d, (W - w_) / 2, 340, "NOT POSSIBLE IN A BROWSER", RED, size=46)
    for i, lab in enumerate(["REC-001", "REC-002", "REC-003"]):
        folder(d, 110 + i * 300, 560, lab)
    if p > 0.3:
        d.line([(100, 540), (980, 760)], fill=RED, width=12)
        d.line([(100, 760), (980, 540)], fill=RED, width=12)
    text_c(d, 870, "Illustrative record numbers", 30, GREYT, "i")

def s2_req(img, t, p):
    header(img, "THE REQUEST", "Sounds reasonable", p)
    for i, (a, ok) in enumerate([("Bulk export", True), ("Files for each record", True), ("No extra step", True), ("One folder per record", False)]):
        e = ease((p - i * 0.12) * 4)
        if e <= 0:
            continue
        y = 470 + i * 170
        card(img, (110, y, 970, y + 130), border=GREEN if ok else RED)
        d = ImageDraw.Draw(img)
        s = "✓" if ok else "✗"
        d.text((150, y + 30), s, font=tfont(s, 64), fill=GREEN if ok else RED)
        d.text((240, y + 36), a, font=font(48), fill=NAVY)

def s2_bytes(img, t, p, name_stage=False):
    if not name_stage:
        header(img, "THE CONCEPT", "Your code hands over bytes", p)
    d = ImageDraw.Draw(img)
    boxes = [(80, "Your code", NAVY), (400, "Browser", GREEN), (720, "Downloads/", AMBER)]
    for i, (x, lab, c) in enumerate(boxes):
        e = 1.0 if name_stage else ease((p - i * 0.2) * 4)
        if e <= 0:
            continue
        card(img, (x, 520, x + 280, 700), border=c)
        d = ImageDraw.Draw(img)
        w_ = d.textlength(lab, font=font(40)); d.text((x + (280 - w_) / 2, 585), lab, font=font(40), fill=c if c != AMBER else NAVY)
        if i < 2 and e > 0.8:
            d.polygon([(x + 290, 595), (x + 320, 610), (x + 290, 625)], fill=GREYT)
    if name_stage or p > 0.55:
        d.text((90, 760), "bytes →", font=font(40), fill=NAVY)
        d.text((420, 760), "decides where →", font=font(40), fill=GREEN)
        d.text((740, 760), "one flat folder", font=font(36, "i"), fill=GREYT)

def s2_name(img, t, p):
    header(img, "WHO DECIDES?", "Not your code", p, kicker_color=AMBER)
    s2_bytes(img, t, p, name_stage=True)
    card(img, (90, 880, 990, 1240))
    d = ImageDraw.Draw(img)
    for i, (a, b, ok) in enumerate([("Location", "browser / user", False), ("Folder", "browser / user", False),
                                    ("File name", "suggest only", True)]):
        y = 910 + i * 105
        s = "✓" if ok else "✗"
        d.text((130, y), s, font=tfont(s, 46), fill=AMBER if ok else RED)
        d.text((200, y), a, font=font(44), fill=NAVY)
        d.text((560, y + 6), b, font=font(38, "r"), fill=GREYT)

def s2_sec(img, t, p):
    header(img, "WHY THERE'S NO API", "Security", p, kicker_color=RED)
    d = ImageDraw.Draw(img)
    card(img, (110, 480, 970, 700), border=RED)
    d = ImageDraw.Draw(img)
    d.text((150, 520), "createFolderHere()", font=font(52, "m"), fill=RED)
    d.line([(140, 560), (720, 560)], fill=RED, width=6)
    d.text((150, 610), "does not exist", font=font(38, "i"), fill=GREYT)
    if p > 0.4:
        text_c(d, 800, "Any website writing folders", 50, NAVY)
        text_c(d, 870, "on your disk = a security hole", 50, NAVY)

def s2_opts(img, t, p, hl=-1):
    header(img, "INSIDE THE BROWSER", "Three options", p)
    opts = [("1", "ZIP file", "works everywhere", GREEN), ("2", "Flat downloads", "no structure at all", AMBER),
            ("3", "File System Access API", "real folders, but…", NAVY)]
    for i, (n, a, b, c) in enumerate(opts):
        e = 1.0 if hl >= 0 else ease((p - i * 0.2) * 4)
        step(img, 70, 470 + i * 190, 940, n, a, b, c, e)
    if hl >= 0:
        ring(img, (70, 470 + hl * 190, 1010, 620 + hl * 190), t)

def s2_opt3(img, t, p):
    header(img, "OPTION 3", "Real folders, big caveats", p, kicker_color=AMBER)
    d = ImageDraw.Draw(img)
    items = [("✓", "Chrome / Edge", GREEN), ("✗", "Firefox", RED), ("✗", "Safari", RED), ("✗", "Mobile", RED),
             ("!", "Permission prompt", AMBER), ("!", "IT can disable it", AMBER)]
    for i, (s, a, c) in enumerate(items):
        e = ease((p - i * 0.08) * 5)
        if e <= 0:
            continue
        col, row = i % 2, i // 2
        x, y = 80 + col * 470, 480 + row * 190
        card(img, (x, y, x + 450, y + 150), border=c)
        d = ImageDraw.Draw(img)
        d.text((x + 30, y + 40), s, font=tfont(s, 60) if s != "!" else font(60), fill=c)
        d.text((x + 100, y + 48), a, font=font(42), fill=NAVY)
    if p > 0.6:
        text_c(d, 1080, "No zip = Chromium only", 60, RED)

def s2_answer(img, t, p):
    header(img, "THE HONEST ANSWER", "Say it in week one", p, kicker_color=RED)
    takeaway(img, t, p, "Folders + no zip + everyone", "= not in a browser", color=RED, y=480)
    d = ImageDraw.Draw(img)
    if p > 0.6:
        chip(d, 170, 1000, "Must have folders? Server-side export", GREEN, size=42)

def s2_lesson(img, t, p):
    header(img, "THE LESSON", "Know the boundary", p, kicker_color=GREEN)
    takeaway(img, t, p, "Know where the boundary is", "before you scope the story", y=480)
    d = ImageDraw.Draw(img)
    if p > 0.5:
        text_c(d, 1000, "Week one, not UAT", 50, NAVY)

def s2_end(img, t, p):
    end_card(img, t, p, "CONCEPTS, NOT", "TRICKS", "ServiceNow Simplified", "Platform boundaries")

SPEC2 = dict(lines=L2, base="concept2_browser_cant_make_folders",
             scenes=dict(hook=s2_hook, req=s2_req, bytes=s2_bytes, name=s2_name, sec=s2_sec, opts=s2_opts,
                         opt3=s2_opt3, answer=s2_answer, lesson=s2_lesson, end=s2_end))

# ============================ SHORT 3: output became input ============================
L3 = [
    ("hook", "This code works the first time. The second time, it's quietly wrong. And it's not a bug in the code.",
             "This code works the first time. The second time, it's quietly wrong. And it's not a bug in the code."),
    ("setup", "You generate a PDF that lists every attachment on a case. Then you attach that PDF to the case, so the user can find it.",
              "You generate a PDF that lists every attachment on a case. Then you attach that PDF to the case, so the user can find it."),
    ("run1", "Run one. Perfect. Three attachments, three rows.", "Run one. Perfect. Three attachments, three rows."),
    ("run2", "Run two. Your PDF lists four attachments. The fourth one is the PDF you generated last time.",
             "Run two. Your PDF lists four attachments. The fourth one is the PDF you generated last time."),
    ("run3", "Run three, it's five. By run ten, the list is mostly old exports.",
             "Run three, it's five. By run ten, the list is mostly old exports."),
    ("loop", "You wrote output into the same set you read from. So your output became input.",
             "You wrote output into the same set you read from. So your output became input."),
    ("trap", "The instinct is to filter by file name. Don't. A user names a real file the same way, and it silently disappears from their list.",
             "The instinct is to filter by file name. Don't. A user names a real file the same way, and it silently disappears."),
    ("fix", "Instead, put the output somewhere your query never looks. For example, attach it to a different record. And add a scheduled clean up, or the files pile up forever.",
            "Instead, put the output somewhere your query never looks, like a different record. And add a scheduled clean-up, or the files pile up forever."),
    ("rule", "The general rule. Any time you read a set, and then write into that same set, your output comes back as input.",
             "The general rule: any time you read a set, and then write into that same set, your output comes back as input."),
    ("shape", "Generated files. Logs written into the table they log. A business rule that updates the record it's watching. Same shape, every time. Ask the question before you build, because it won't show up in your first test.",
              "Generated files. Logs written into the table they log. A business rule updating the record it watches. Same shape. Ask before you build: it won't show up in your first test."),
    ("end", "Follow ServiceNow Simplified for more.", "Follow ServiceNow Simplified for more."),
]

def pdf_list(img, t, x, y, n, new_idx=None, title=None):
    files = ["ticket.pdf", "invoice.pdf", "receipt.pdf"] + [f"export_run{i}.pdf" for i in range(1, 10)]
    card(img, (x, y, x + 900, y + 140 + min(n, 6) * 86))
    d = ImageDraw.Draw(img)
    d.text((x + 40, y + 30), title or f"Supporting Attachments ({n})", font=font(44), fill=NAVY)
    d.line([(x + 40, y + 100), (x + 860, y + 100)], fill=LIGHT, width=3)
    for i, f_ in enumerate(files[:min(n, 6)]):
        own = f_.startswith("export")
        yy = y + 120 + i * 86
        d.text((x + 40, yy), f_, font=font(40, "m"), fill=RED if own else INK)
        if own:
            d.text((x + 520, yy + 4), "← your own output", font=font(34), fill=RED)
    if n > 6:
        d.text((x + 40, y + 120 + 6 * 86 - 20), f"… +{n - 6} more", font=font(34, "i"), fill=GREYT)

def s3_hook(img, t, p):
    d = ImageDraw.Draw(img)
    for i, (lab, c, s) in enumerate([("RUN 1", GREEN, "✓"), ("RUN 2", AMBER, "?"), ("RUN 10", RED, "✗")]):
        e = ease((p - i * 0.18) * 4)
        if e <= 0:
            continue
        y = 300 + i * 260
        card(img, (140, y, 940, y + 200), border=c)
        d = ImageDraw.Draw(img)
        d.text((200, y + 55), lab, font=font(84), fill=NAVY)
        d.text((760, y + 45), s, font=tfont(s, 100) if s != "?" else font(100), fill=c)
    if p > 0.6:
        text_c(d, 1130, "Not a bug in the code", 56, RED)

def s3_setup(img, t, p):
    header(img, "THE SETUP", "Generate, then attach", p)
    for i, (n, a, b, c) in enumerate([("1", "Read the case's attachments", "build an HTML list", NAVY),
                                      ("2", "Convert to PDF", "export.pdf", GREEN),
                                      ("3", "Attach it to the same case", "so the user can find it", AMBER)]):
        step(img, 70, 470 + i * 190, 940, n, a, b, c, ease((p - i * 0.15) * 4))
    if p > 0.7:
        ring(img, (70, 850, 1010, 1000), t)

def s3_run1(img, t, p):
    header(img, "RUN 1", "Perfect", p, kicker_color=GREEN)
    pdf_list(img, t, 90, 470, 3)

def s3_run2(img, t, p):
    header(img, "RUN 2", "Quietly wrong", p, kicker_color=AMBER)
    pdf_list(img, t, 90, 470, 4)
    if p > 0.45:
        ring(img, (120, 845, 980, 915), t, color=RED)

def s3_run3(img, t, p):
    n = 5 if p < 0.45 else 12
    header(img, f"RUN {3 if n == 5 else 10}", "Mostly old exports" if n > 5 else "Five", p, kicker_color=RED)
    pdf_list(img, t, 90, 470, n)

def s3_loop(img, t, p):
    header(img, "THE CONCEPT", "Output became input", p, kicker_color=RED)
    d = ImageDraw.Draw(img)
    cx, cy, r = W / 2, 820, 290
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=LIGHT, width=10)
    a1 = -90 + 360 * min(1, p * 1.4)
    d.arc([cx - r, cy - r, cx + r, cy + r], -90, a1, fill=RED, width=10)
    for ang, lab, c in [(-90, "READ the set", NAVY), (90, "WRITE into the set", RED)]:
        x = cx + r * math.cos(math.radians(ang)); y = cy + r * math.sin(math.radians(ang))
        f = font(42); w_ = d.textlength(lab, font=f)
        d.rounded_rectangle([x - w_ / 2 - 24, y - 40, x + w_ / 2 + 24, y + 40], 20, fill=c)
        d.text((x - w_ / 2, y - 26), lab, font=f, fill=WHITE)
    text_c(d, cy - 40, "case", 70, NAVY)
    text_c(d, cy + 30, "attachments", 50, GREYT)

def s3_trap(img, t, p):
    header(img, "THE TRAP", "Filtering by file name", p, kicker_color=RED)
    code(img, (40, 470, 1040, 760), ["if (name.indexOf('export') == 0) continue;"], t, hl={0}, title="Don't", size=30)
    d = ImageDraw.Draw(img)
    if p > 0.35:
        card(img, (90, 820, 990, 1120), border=RED)
        d = ImageDraw.Draw(img)
        d.text((130, 850), "User uploads:", font=font(38, "r"), fill=GREYT)
        d.text((130, 910), "export_2026_budget.pdf", font=font(42, "m"), fill=INK)
        d.text((130, 1000), "→ silently missing from the list", font=font(40), fill=RED)

def s3_fix(img, t, p):
    header(img, "THE FIX", "Write where you don't read", p, kicker_color=GREEN)
    code(img, (40, 470, 1040, 900), ["var pdf = new",
                                     "  sn_pdfgeneratorutils.PDFGenerationAPI();",
                                     "// attach OUTSIDE the set you read",
                                     "pdf.convertToPDF(html, 'sys_user',",
                                     "  gs.getUserID(), fileName);"], t, hl={2, 3, 4}, title="One option", size=29)
    d = ImageDraw.Draw(img)
    if p > 0.6:
        chip(d, 90, 950, "+ scheduled clean-up", AMBER, size=42, fg=NAVY)
    d.text((90, 1070), "Check the API signature on your release", font=font(28, "i"), fill=GREYT)

def s3_rule(img, t, p):
    header(img, "THE RULE", "Read + write the same set", p, kicker_color=GREEN)
    takeaway(img, t, p, "Read a set, write into it:", "output comes back as input", y=480)

def s3_shape(img, t, p):
    header(img, "SAME SHAPE", "Everywhere", p)
    for i, (n, a, b) in enumerate([("1", "Generated files", "attached where you read"), ("2", "Logging", "into the table you log"),
                                   ("3", "Business rule", "updating the record it watches")]):
        step(img, 70, 470 + i * 190, 940, n, a, b, RED, ease((p - i * 0.12) * 4))
    d = ImageDraw.Draw(img)
    if p > 0.6:
        text_c(d, 1060, "It won't show up in your first test", 46, NAVY)

def s3_end(img, t, p):
    end_card(img, t, p, "CONCEPTS, NOT", "TRICKS", "ServiceNow Simplified", "Design: read vs write sets")

SPEC3 = dict(lines=L3, base="concept3_output_became_input",
             scenes=dict(hook=s3_hook, setup=s3_setup, run1=s3_run1, run2=s3_run2, run3=s3_run3, loop=s3_loop,
                         trap=s3_trap, fix=s3_fix, rule=s3_rule, shape=s3_shape, end=s3_end))

if __name__ == "__main__":
    spec = {"1": SPEC1, "2": SPEC2, "3": SPEC3}[sys.argv[1]]
    here = os.path.join(HERE, "s" + sys.argv[1])
    os.makedirs(here, exist_ok=True)
    print(render(spec["lines"], spec["scenes"], here, spec["base"]))

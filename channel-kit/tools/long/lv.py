"""Long-form 16:9 video: '30 ServiceNow Best Practices'. Usage: python lv.py <part> [preview] | python lv.py all"""
import math, os, subprocess, sys
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import snlib as S
from PIL import Image, ImageDraw, ImageFilter

S.W, S.H = 1920, 1080
S.GAP = 1.2  # breathing room after each point (long-form pacing)
W, H, FPS = S.W, S.H, S.FPS
HERE = os.path.dirname(os.path.abspath(__file__))
font, ease = S.font, S.ease
ACCENT, AMBER, RED, WHITE, GREY, INK, CARD = S.ACCENT, S.AMBER, S.RED, S.WHITE, S.GREY, S.INK, S.CARD
BLUE = (140, 170, 255)

CHAPTERS = [
 dict(key="ch1", name="Server-side scripting",
   vo="Chapter one. Server-side scripting. This is where most performance problems start.",
   tips=[
    ("Write code the next developer can read. Comment why the code exists, not what each line does. Use whitespace and descriptive names. And prefer a simple if else over clever nested ternaries.",
     "READABLE CODE", "for the next developer", "bullets",
     [("Comments", "explain why, not what", ACCENT), ("Whitespace", "group related lines", ACCENT),
      ("Names", "descriptive, not x or gr2", ACCENT), ("if / else", "over nested ternaries", AMBER)]),
    ("Don't repeat yourself. If the same logic appears twice, move it into a function, or a script include. Store a function's result in a variable instead of calling it again. And have functions return a value, so the caller can check what happened.",
     "REUSE IT", "functions & Script Includes", "bullets",
     [("Same logic twice?", "move it into a function", AMBER), ("Used across scripts?", "put it in a Script Include", ACCENT),
      ("Store results", "call once, reuse the variable", ACCENT), ("Return a value", "so callers can check it", ACCENT)]),
    ("Counting records? Get row count loads every matching record and then counts them, which gets slower as the table grows. GlideAggregate asks the database to do the count instead.",
     "COUNT SMART", "GlideAggregate, not getRowCount()", "code2",
     (["var gr = new GlideRecord('incident');", "gr.addActiveQuery();", "gr.query();", "var count = gr.getRowCount();"],
      ["var ga = new GlideAggregate('incident');", "ga.addActiveQuery();", "ga.addAggregate('COUNT');", "ga.query();", "ga.next();",
       "var count = ga.getAggregate('COUNT');"])),
    ("For complex filters, use one encoded query instead of a chain of add query and add or condition calls. It's easier to read, and you can copy it straight from a list filter.",
     "ENCODED QUERIES", "one line instead of a chain", "code2",
     (["var gr = new GlideRecord('incident');", "var qc = gr.addQuery('priority', 1);", "qc.addOrCondition('priority', 2);",
       "gr.addQuery('active', true);", "gr.query();"],
      ["var gr = new GlideRecord('incident');", "gr.addEncodedQuery(", "  'active=true^priority=1^ORpriority=2');", "gr.query();"])),
    ("Let the database do the work. If you only need one record, add set limit one, so the query stops early.",
     "LIMIT IT", "need one record? setLimit(1)", "code2",
     (["gr.addActiveQuery();", "gr.query();", "if (gr.next()) { /* ... */ }"],
      ["gr.addActiveQuery();", "gr.setLimit(1);", "gr.query();", "if (gr.next()) { /* ... */ }"])),
    ("Never hard-code sys IDs. They can differ between instances, and nobody knows what they mean. Store them in a system property, and read it with gs dot get property.",
     "NO HARD-CODED IDs", "use a system property", "code2",
     (["var groupId = '8a5055c9c6112278…';"], ["var groupId = gs.getProperty(", "    'my_app.default_group');"])),
    ("Use get value for logic. A reference field already stores a sys ID, so get value returns it. No dot-walking needed. Use get display value only when you show something to a user, because display values can change, and can depend on the user's language.",
     "VALUE vs DISPLAY", "getValue() for logic", "code2",
     (["var callerId = current.caller_id.sys_id;", "if (current.getDisplayValue('state')", "    == 'Resolved') { /* ... */ }"],
      ["var callerId = current.getValue('caller_id');", "if (current.getValue('state') == '6') {", "  /* ... */", "}"])),
    ("And never use eval. It runs any string as code, which opens the door to injection attacks, and its errors don't give you useful line numbers. Call known functions explicitly instead.",
     "NEVER eval()", "it runs any string as code", "bullets",
     [("eval(string)", "runs any string as code", RED), ("Risk", "injection attacks", RED),
      ("Debugging", "no useful line numbers", AMBER), ("Instead", "call known functions explicitly", ACCENT)]),
   ]),
 dict(key="ch2", name="Client scripts",
   vo="Chapter two. Client scripts. They run in the user's browser, so every extra call is time the user waits.",
   tips=[
    ("For mandatory, visible, or read-only fields, use a UI policy, not a client script. Save client scripts for logic UI policies can't handle. And think about list editing: if the form enforces a rule, make sure list edits can't bypass it.",
     "UI POLICY FIRST", "mandatory · visible · read-only", "bullets",
     [("Mandatory / Visible / Read-only", "UI Policy", ACCENT), ("Complex logic", "Client Script", AMBER),
      ("List editing", "make sure it can't bypass form rules", RED)]),
    ("Client scripts have no condition field, so they run every time. In on change scripts, exit early when the form is loading, when the new value is empty, or when it hasn't actually changed.",
     "GUARD onChange", "exit early", "code1",
     ["function onChange(control, oldValue,", "                  newValue, isLoading) {", "  if (isLoading || newValue === '' ||",
      "      newValue === oldValue) {", "    return;", "  }", "  // your logic here", "}"]),
    ("Use data that's already on the client whenever you can. Need server data at load time? Fill g scratchpad from a display business rule. Need it later? Use asynchronous GlideAjax, and only after checking you really need it. Client-side GlideRecord and get reference are no longer recommended.",
     "CUT SERVER CALLS", "g_scratchpad or async GlideAjax", "code2",
     (["g_form.getReference('caller_id', cb);", "var gr = new GlideRecord('sys_user');"],
      ["// display Business Rule fills it", "var isVip = g_scratchpad.isVip;", "// or only when needed:", "ga.getXMLAnswer(handleAnswer);"])),
    ("When you set a reference field, pass the display value too. Without it, the form makes an extra call to the server just to look it up.",
     "SET DISPLAY VALUE", "on reference fields", "code2",
     (["g_form.setValue('caller_id', userId);"], ["g_form.setValue('caller_id', userId,", "                userName);"])),
    ("Avoid global client scripts. They load on every form. And avoid DOM manipulation, because it breaks when the UI is upgraded. Use the g form API instead. The exception is UI pages and Service Portal widgets, where you own the markup.",
     "NO GLOBAL, NO DOM", "use the g_form API", "bullets",
     [("Global client scripts", "load on every form", RED), ("DOM manipulation", "breaks on UI upgrades", RED),
      ("Use instead", "the g_form API", ACCENT), ("Exception", "UI Pages & Service Portal widgets", AMBER)]),
   ]),
 dict(key="ch3", name="Business rules",
   vo="Chapter three. Business rules. They run on every database operation, so small mistakes multiply fast.",
   tips=[
    ("Pick the right when. Use before to change the current record, after to update other records, async for work that can wait, and display to send data to the form with g scratchpad.",
     "PICK THE RIGHT WHEN", "before · after · async · display", "bullets",
     [("before", "change the current record", ACCENT), ("after", "update other records", BLUE),
      ("async", "work that can wait", AMBER), ("display", "fill g_scratchpad for the form", GREY)]),
    ("Always add a condition. Conditions are checked before the script runs. Without one, the script runs on every single insert or update on the table.",
     "ADD A CONDITION", "or it runs on every save", "bullets",
     [("No condition", "script runs every time", RED), ("State changes to Resolved", "runs only when needed", ACCENT)]),
    ("Don't call current dot update in a business rule. It triggers the business rules again and can create a loop. ServiceNow stops a recursive rule and logs an error, but by then you've lost performance. In a before rule, just set the value. It's saved automatically.",
     "NO current.update()", "it can call itself", "code2",
     (["// after Business Rule", "current.state = 6;", "current.update(); // runs BRs again"],
      ["// before Business Rule", "current.state = 6;", "// saved automatically"])),
    ("If the user doesn't need the result right away, use async instead of after. The user gets control back faster, and the work happens in the background.",
     "ASYNC > AFTER", "when it can wait", "bullets",
     [("after", "user waits for it", AMBER), ("async", "runs in the background", ACCENT), ("Good for", "integrations, other records", GREY)]),
    ("Keep your code inside the function wrapper that advanced business rules give you, so your variables don't leak into other scripts. And put reusable logic in a script include, not a global business rule, which loads on every page.",
     "WRAP & REUSE", "no leaks, no global BRs", "code1",
     ["(function executeRule(current, previous) {", "  // variables stay inside this function", "  new MyUtils().closeChildTasks(current);",
      "})(current, previous);"]),
   ]),
 dict(key="ch4", name="Debugging",
   vo="Chapter four. Debugging. Finding a bug fast matters as much as not writing one.",
   tips=[
    ("gs dot log and gs dot print don't work in scoped apps. Use gs dot info, or gs dot debug. They work in both scoped and global.",
     "gs.info > gs.log", "works in scoped + global", "code2",
     (["gs.log('here');      // global only", "gs.print('x=' + x);  // global only"],
      ["gs.info('MyUtil: x=' + x);", "gs.debug('MyUtil: ' + msg);"])),
    ("Wrap debug messages in a system property check. Then you can turn logging on or off without changing code, and without affecting other users.",
     "SWITCH IT OFF", "with a system property", "code1",
     ["if (gs.getProperty('debug.MyUtil') == 'true') {", "  gs.info('MyUtil: ' + details);", "}"]),
    ("Type debug in the navigator to see every debug module. Debug business rule shows which rules started, finished, or were skipped. Debug security rules shows how ACLs evaluate on each field. And stop debugging turns it all off.",
     "DEBUG MODULES", "type 'debug' in the navigator", "bullets",
     [("Debug Business Rule", "==> started · <== finished · === skipped", ACCENT), ("Debug Security Rules", "ACL results per field", AMBER),
      ("Debug Log", "gs.info / gs.debug output", BLUE), ("Stop Debugging", "turn it all off", RED)]),
    ("On the client side, turn on the JavaScript log and field watcher, and use jslog in your scripts. Check the browser console too. It shows errors that appear nowhere else. And before production, remove leftover alerts and log statements.",
     "CLIENT-SIDE", "JavaScript Log · console", "bullets",
     [("JavaScript Log", "+ jslog() in client scripts", ACCENT), ("Field Watcher", "see what changes a field", ACCENT),
      ("Browser console", "errors that appear nowhere else", AMBER), ("Before production", "remove alert() & leftover logs", RED)]),
   ]),
 dict(key="ch5", name="Logs & queues",
   vo="Chapter five. Logs and queues. Your instance tells you what's wrong, if you know where to look.",
   tips=[
    ("Check System Logs, System Log, All, regularly during development. Every error should be fixed, or documented as a known issue.",
     "SYSTEM LOG", "fix or document every error", "path",
     (["System Logs", "System Log", "All"], [("Error", "fix it", RED), ("Known issue", "document it", AMBER)])),
    ("Download the node log files and search for these messages: slow evaluate, slow business rule, recursive business rule, compiler exception, and extremely large result. Each one points to a script or query worth fixing. A log file that suddenly grows is a warning too.",
     "SEARCH FOR THESE", "in the node log files", "bullets",
     [("Slow evaluate", "", AMBER), ("Slow Business Rule", "", AMBER), ("Recursive Business Rule", "", RED),
      ("Compiler exception", "", RED), ("Extremely large result", "", AMBER), ("Sudden log growth", "", AMBER)]),
    ("Open Slow Queries in System Diagnostics. Sort by total execution time, and use the example column to find the script behind each slow query.",
     "SLOW QUERIES", "find the script behind it", "path",
     (["System Diagnostics", "Slow Queries"], [("Sort", "Total Execution Time", AMBER), ("Read", "the Example column", ACCENT)])),
    ("In the event log, sort by processing duration to find slow events, and group by name to find noisy ones. An event that nothing responds to is just noise. Consider disabling whatever logs it.",
     "NOISY EVENTS", "in the Event Log", "bullets",
     [("Sort", "Processing duration Z→A", AMBER), ("Group by", "Name", BLUE), ("No action?", "stop logging it", ACCENT)]),
   ]),
 dict(key="ch6", name="Update sets & XML",
   vo="Chapter six. Update sets and XML. Code that works in dev only matters if it arrives safely in production.",
   tips=[
    ("Keep a migration document. List the order to apply update sets, plus the plugins to activate, system properties to set, and servers to configure.",
     "WRITE IT DOWN", "a migration document", "bullets",
     [("1", "Update set order", ACCENT), ("2", "Plugins to activate", ACCENT), ("3", "System properties", ACCENT), ("4", "MID & identity servers", ACCENT)]),
    ("Some data isn't captured in update sets, like approval lookup records. Move it as XML, and note that in the update set description, so whoever installs it knows.",
     "DATA STAYS BEHIND", "move it with XML", "bullets",
     [("Not in update sets", "e.g. approval lookups", RED), ("Export / Import", "as XML", AMBER), ("Note it", "in the update set description", ACCENT)]),
    ("Importing XML doesn't run business rules, and doesn't update the instance cache. Plan for anything those rules would normally do.",
     "XML SKIPS RULES", "plan for it", "bullets",
     [("Business Rules", "✗ not run", RED), ("Instance cache", "✗ not updated", RED)]),
    ("An XML export contains only that record. Export a user, and their group memberships and roles don't come with it. Export those separately.",
     "ONE RECORD ONLY", "related records stay behind", "bullets",
     [("User record", "✓ exported", ACCENT), ("Group memberships", "✗ not included", RED), ("Roles", "✗ not included", RED)]),
   ]),
]
TOTAL_TIPS = sum(len(c["tips"]) for c in CHAPTERS)  # 30

# ---------------- drawing helpers ----------------
def text_l(d, x, y, s, size, fill, kind="b", stroke=0, maxw=None):
    f = font(size, kind)
    if maxw and d.textlength(s, font=f) > maxw:
        f = font(size * maxw / d.textlength(s, font=f), kind)
    d.text((x, y), s, font=f, fill=fill, stroke_width=stroke, stroke_fill=(0, 0, 0))

def top_bar(img, label=None, n=0, total=0):
    S.logo_badge(img, 36, 30, 220, pad=12, alpha=0.95)
    d = ImageDraw.Draw(img)
    if label:
        f = font(30)
        w = d.textlength(label, font=f)
        d.text((W - 60 - w, 36), label, font=f, fill=GREY)
    if total:
        x = W - 60 - total * 44
        for i in range(total):
            d.rounded_rectangle([x + i * 44, 84, x + i * 44 + 34, 98], 7, fill=ACCENT if i < n else (70, 80, 105))

def tip_header(img, n, title, sub, p):
    d = ImageDraw.Draw(img)
    a = ease(p * 4)
    d.rounded_rectangle([120, 140, 270, 192], 26, fill=AMBER)
    d.text((148, 146), f"TIP {n}", font=font(34), fill=(20, 24, 36))
    kind = "m" if ("(" in title or "." in title) else "b"
    text_l(d, 300 - 30 * (1 - a), 128, title, 72, WHITE, kind=kind, stroke=5, maxw=1480)
    text_l(d, 122, 220, sub, 40, GREY, maxw=1650)

def code_pair(img, t, p, bad, good):
    lh = int(28 * 1.55)
    h = 100 + max(len(bad), len(good)) * lh + 20
    y0 = 330
    S.code_card(img, (80, y0, 940, y0 + h), bad, t, size=28, title="✗  AVOID")
    ImageDraw.Draw(img).rounded_rectangle([80, y0, 940, y0 + h], 28, outline=RED, width=4)
    e = ease((p - 0.25) * 4)
    if e > 0:
        x = 980 + 40 * (1 - e)
        S.code_card(img, (x, y0, x + 860, y0 + h), good, t, size=28, title="✓  DO THIS")
        ImageDraw.Draw(img).rounded_rectangle([x, y0, x + 860, y0 + h], 28, outline=ACCENT, width=4)

def code_single(img, t, p, lines):
    lh = int(32 * 1.55)
    S.code_card(img, (260, 330, 1660, 330 + 120 + len(lines) * lh), lines, t, size=32, title="✓  DO THIS",
                reveal=0.2 + 0.8 * ease(p * 2))

def bullets(img, t, p, items, y0=330, y1=880):
    d = ImageDraw.Draw(img)
    n = len(items)
    cols = 1 if n <= 3 else 2
    rows = math.ceil(n / cols)
    gap = 24
    h = min(170, (y1 - y0 - gap * (rows - 1)) // rows)
    cw = 1400 if cols == 1 else 820
    x_base = (W - cw) / 2 if cols == 1 else 120
    for i, (a, b, c) in enumerate(items):
        e = ease((p - i * (0.6 / n)) * 5)
        if e <= 0:
            continue
        r, col = (i // cols, i % cols)
        x = x_base + col * (cw + 40) - (1 - e) * 500
        y = y0 + r * (h + gap)
        d.rounded_rectangle([x, y, x + cw, y + h], 24, fill=(18, 26, 42), outline=c, width=4)
        d.rounded_rectangle([x, y, x + 16, y + h], 8, fill=c)
        kind = "m" if a in ("==>", "<==", "===") or "(" in a else "b"
        if b:
            text_l(d, x + 50, y + h / 2 - 54, a, 46, WHITE, kind=kind, maxw=cw - 80)
            text_l(d, x + 50, y + h / 2 + 6, b, 38, c if c != GREY else (200, 205, 215), kind="r", maxw=cw - 80)
        else:
            text_l(d, x + 50, y + h / 2 - 28, a, 50, WHITE, kind=kind, maxw=cw - 80)

def path_scene(img, t, p, crumbs, items):
    d = ImageDraw.Draw(img)
    f = font(42)
    x, y = 120, 330
    for i, c in enumerate(crumbs):
        if ease((p - i * 0.12) * 5) <= 0:
            break
        w = d.textlength(c, font=f)
        d.rounded_rectangle([x, y, x + w + 56, y + 90], 18, fill=CARD)
        d.text((x + 28, y + 20), c, font=f, fill=INK)
        x += w + 56
        if i < len(crumbs) - 1:
            d.text((x + 14, y + 12), "›", font=font(56), fill=AMBER)
            x += 64
    bullets(img, t, max(0, p - 0.3) / 0.7, items, y0=y + 150, y1=880)

def captions(img, segs, t):
    for s in segs:
        if s["start"] <= t < s["start"] + s["dur"]:
            words = s["cap"].split()
            wts = np.array([len(w) + 3 for w in words], float)
            cum = np.cumsum(wts) / wts.sum() * s["dur"]
            wi = min(int(np.searchsorted(cum, t - s["start"])), len(words) - 1)
            c0 = (wi // 6) * 6
            d = ImageDraw.Draw(img)
            f = font(50)
            parts = [(w, AMBER if c0 + j == wi else WHITE) for j, w in enumerate(words[c0:c0 + 6])]
            total = sum(d.textlength(w + " ", font=f) for w, _ in parts)
            if total > W - 200:
                f = font(50 * (W - 200) / total)
                total = sum(d.textlength(w + " ", font=f) for w, _ in parts)
            x = (W - total) / 2
            band = Image.new("RGBA", (W, H), (0, 0, 0, 0))
            ImageDraw.Draw(band).rounded_rectangle([x - 30, 935, x + total + 20, 1015], 20, fill=(0, 0, 0, 150))
            img.alpha_composite(band)
            d = ImageDraw.Draw(img)
            for w, col in parts:
                d.text((x, 945), w, font=f, fill=col, stroke_width=4, stroke_fill=(0, 0, 0))
                x += d.textlength(w + " ", font=f)
            return

# ---------------- parts ----------------
def part_intro():
    lines = [
        ("i_hook", "Most ServiceNow performance problems come from the same few habits.",
                   "Most ServiceNow performance problems come from the same few habits."),
        ("i_list", "In this video, I'll walk you through thirty best practices, across six areas. Server-side scripting, client scripts, business rules, debugging, logs and queues, and update sets.",
                   "In this video: 30 best practices across 6 areas. Server-side scripting, client scripts, business rules, debugging, logs & queues, and update sets."),
        ("i_cta",  "The chapters are in the description, so you can jump straight to what you need. Let's start.",
                   "The chapters are in the description, so you can jump straight to what you need. Let's start."),
    ]
    def hook(img, t, p):
        d = ImageDraw.Draw(img)
        lw = 700
        S.logo_badge(img, (W - lw - 48) / 2, 120, lw, pad=24)
        S.text_c(d, 470, "30 SERVICENOW", 120, WHITE, stroke=8)
        S.text_c(d, 620, "BEST PRACTICES", 120, AMBER, stroke=8)
    def grid(img, t, p, cta=False):
        top_bar(img)
        d = ImageDraw.Draw(img)
        S.text_c(d, 120, "6 AREAS · 30 PRACTICES", 64, WHITE, stroke=5)
        for i, c in enumerate(CHAPTERS):
            e = 1 if cta else ease((p - i * 0.1) * 5)
            if e <= 0:
                continue
            r, col = divmod(i, 3)
            x, y = 130 + col * 570, 270 + r * 300 + 30 * (1 - e)
            d.rounded_rectangle([x, y, x + 530, y + 260], 28, fill=(18, 26, 42), outline=ACCENT, width=4)
            d.text((x + 36, y + 30), f"0{i + 1}", font=font(70, "m"), fill=AMBER)
            text_l(d, x + 36, y + 130, c["name"], 46, WHITE, maxw=460)
            d.text((x + 36, y + 196), f"{len(c['tips'])} practices", font=font(32, "r"), fill=GREY)
        if cta:
            S.text_c(d, 870, "Chapters ↓ in the description", 44, ACCENT, stroke=3)
    return lines, dict(i_hook=hook, i_list=grid, i_cta=lambda img, t, p: grid(img, t, p, True))

def part_chapter(ci):
    ch = CHAPTERS[ci]
    total = len(ch["tips"])
    label = f"CHAPTER {ci + 1} · {ch['name'].upper()}"
    lines = [("title", ch["vo"], ch["vo"])]
    def title(img, t, p):
        top_bar(img)
        d = ImageDraw.Draw(img)
        e = ease(p * 3)
        d.text((140, 250 - 40 * (1 - e)), f"0{ci + 1}", font=font(300, "m"), fill=AMBER)
        text_l(d, 140, 600, ch["name"].upper(), 96, WHITE, stroke=6, maxw=900)
        d.text((140, 730), f"{total} practices", font=font(44, "r"), fill=GREY)
        for i, tip in enumerate(ch["tips"]):
            ee = ease((p - 0.15 - i * 0.07) * 5)
            if ee <= 0:
                continue
            y = 220 + i * (600 // max(total, 5))
            x = 1080 + 60 * (1 - ee)
            d.rounded_rectangle([x, y, x + 720, y + 64], 16, fill=(18, 26, 42), outline=(60, 70, 95), width=2)
            text_l(d, x + 24, y + 12, f"{i + 1}. {tip[1]}", 34, WHITE, kind="m" if "(" in tip[1] or "." in tip[1] else "b", maxw=670)
    scenes = dict(title=title)
    for i, (vo, ttl, sub, kind, payload) in enumerate(ch["tips"]):
        key = f"t{i + 1}"
        lines.append((key, vo, vo))
        def sc(img, t, p, i=i, ttl=ttl, sub=sub, kind=kind, payload=payload):
            top_bar(img, label, i + 1, total)
            tip_header(img, i + 1, ttl, sub, p)
            if kind == "code2":
                code_pair(img, t, p, *payload)
            elif kind == "code1":
                code_single(img, t, p, payload)
            elif kind == "bullets":
                bullets(img, t, p, payload)
            elif kind == "path":
                path_scene(img, t, p, *payload)
        scenes[key] = sc
    return lines, scenes

def part_outro():
    lines = [
        ("o_recap", "So, to recap. Write readable, reusable server code, and let the database do the work. Keep client scripts light. Give business rules conditions, and never call current dot update. Debug with properties, not leftovers. Read your logs. And document every migration.",
                    "To recap: readable, reusable server code; let the database do the work. Keep client scripts light. Business rules need conditions, and no current.update(). Debug with properties, not leftovers. Read your logs. Document every migration."),
        ("o_cta",   "If this helped, subscribe, and check the Shorts playlist for a quick refresher on each chapter. See you in the next one.",
                    "If this helped, subscribe, and check the Shorts playlist for a quick refresher on each chapter. See you in the next one."),
    ]
    recap = ["Readable, reusable server code", "Light client scripts", "BRs with conditions, no current.update()",
             "Debug with properties", "Read your logs", "Document every migration"]
    def rc(img, t, p):
        top_bar(img)
        d = ImageDraw.Draw(img)
        S.text_c(d, 120, "RECAP", 80, AMBER, stroke=6)
        for i, s in enumerate(recap):
            e = ease((p - i * 0.12) * 5)
            if e <= 0:
                continue
            r, col = divmod(i, 2)
            x, y = 140 + col * 840, 280 + r * 200
            d.rounded_rectangle([x, y, x + 800, y + 160], 24, fill=(18, 26, 42), outline=ACCENT, width=4)
            d.text((x + 34, y + 38), "✓", font=font(70), fill=ACCENT)
            text_l(d, x + 130, y + 52, s, 42, WHITE, maxw=640)
    def cta(img, t, p):
        d = ImageDraw.Draw(img)
        lw = 760
        S.logo_badge(img, (W - lw - 48) / 2, 140, lw, pad=24)
        bob = 10 * math.sin(t * 4)
        d.rounded_rectangle([W / 2 - 300, 520 + bob, W / 2 + 300, 640 + bob], 60, fill=(220, 40, 50))
        S.text_c(d, 545 + bob, "SUBSCRIBE", 64, WHITE, stroke=0)
        S.text_c(d, 720, "▶  Best Practices Shorts playlist", 50, ACCENT, stroke=3)
    return lines, dict(o_recap=rc, o_cta=cta)

PARTS = ["intro"] + [c["key"] for c in CHAPTERS] + ["outro"]

def build(name):
    if name == "intro":
        return part_intro()
    if name == "outro":
        return part_outro()
    return part_chapter([c["key"] for c in CHAPTERS].index(name))

def render_part(name, preview=False):
    lines, scenes = build(name)
    here = os.path.join(HERE, "parts", name)
    out = os.path.join(here, "build")
    os.makedirs(out, exist_ok=True)
    segs, total = S.build_audio(lines, out, length_scale=1.0)
    S.write_srt(segs, os.path.join(here, "part.srt"))
    BG = S._bg()

    def scene_at(t):
        cur = segs[0]
        for s in segs:
            if t >= s["start"] - 0.15:
                cur = s
        lt = t - (cur["start"] - 0.15)
        return cur, lt, lt / (cur["dur"] + S.GAP)

    def frame(fi):
        t = fi / FPS
        img = BG.copy()
        s, lt, p = scene_at(t)
        scenes[s["scene"]](img, lt, min(1.0, max(0.0, p)))
        captions(img, segs, t)
        if lt < 0.1:
            img.alpha_composite(Image.new("RGBA", (W, H), (255, 255, 255, int(60 * (1 - lt / 0.1)))))
        return img.convert("RGB")

    if preview:
        for s in segs:
            frame(int((s["start"] + s["dur"] * 0.8) * FPS)).save(os.path.join(out, f"prev_{s['scene']}.png"))
        return
    silent = os.path.join(out, "silent.mp4")
    ff = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
                           "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "medium", "-crf", "19",
                           "-pix_fmt", "yuv420p", silent], stdin=subprocess.PIPE)
    for fi in range(int(total * FPS)):
        ff.stdin.write(frame(fi).tobytes())
    ff.stdin.close(); ff.wait()
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", silent, "-i", os.path.join(out, "vo.wav"),
                    "-i", os.path.join(out, "music.wav"), "-filter_complex",
                    "[1:a]aresample=44100,volume=1.6,asplit=2[v][vs];[2:a]volume=0.8[m];"
                    "[m][vs]sidechaincompress=threshold=0.05:ratio=6:attack=20:release=300[duck];"
                    "[v][duck]amix=inputs=2:normalize=0,volume=2.0,alimiter=limit=0.85:level=false[a]",
                    "-map", "0:v", "-map", "[a]", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-ar", "44100", "-ac", "2",
                    "-shortest", os.path.join(here, "part.mp4")], check=True)

if __name__ == "__main__":
    render_part(sys.argv[1], preview="preview" in sys.argv)

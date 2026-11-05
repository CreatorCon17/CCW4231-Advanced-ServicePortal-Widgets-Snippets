"""ServiceNow Best Practices Shorts series (6 categories). Usage: python bp_shorts.py <1-6> [preview]"""
import math, os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from snlib import *
from PIL import Image, ImageDraw, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))

# Each tip: (vo, caption, title, sub, kind, payload)
#   kind: "code2" -> (bad_lines, good_lines) | "code1" -> lines | "bullets" -> items | "path" -> (crumbs, items)
SPECS = {
 1: dict(
    base="bp1_server_side_scripting", cat="SERVER-SIDE SCRIPTING",
    hook=(("4 SERVER-SIDE", WHITE), ("HABITS", AMBER)),
    hook_vo="Four server-side scripting habits every ServiceNow developer should have.",
    tips=[
      ("One. Counting records? Use GlideAggregate. Get row count pulls every record first, and that gets slower as the table grows.",
       "1. Counting records? Use GlideAggregate. getRowCount() pulls every record first, and gets slower as the table grows.",
       "COUNT SMART", "GlideAggregate, not getRowCount()", "code2",
       (["var gr = new GlideRecord('incident');", "gr.addActiveQuery();", "gr.query();", "var count = gr.getRowCount();"],
        ["var ga = new GlideAggregate('incident');", "ga.addActiveQuery();", "ga.addAggregate('COUNT');", "ga.query();", "ga.next();",
         "var count = ga.getAggregate('COUNT');"])),
      ("Two. Need just one record? Add set limit one, and let the database stop early.",
       "2. Need just one record? Add setLimit(1) and let the database stop early.",
       "LIMIT IT", "Need one record? setLimit(1)", "code2",
       (["gr.addActiveQuery();", "gr.query();", "if (gr.next()) { /* ... */ }"],
        ["gr.addActiveQuery();", "gr.setLimit(1);", "gr.query();", "if (gr.next()) { /* ... */ }"])),
      ("Three. Never hard-code sys IDs. Store them in a system property, and read it with gs dot get property.",
       "3. Never hard-code sys_ids. Store them in a system property and read it with gs.getProperty().",
       "NO HARD-CODED IDs", "Use a system property", "code2",
       (["var groupId = '8a5055c9c6112278…';"],
        ["var groupId = gs.getProperty(", "    'my_app.default_group');"])),
      ("Four. Need a reference field's sys ID? Use get value. Don't dot-walk to the sys ID.",
       "4. Need a reference field's sys_id? Use getValue(). Don't dot-walk to sys_id.",
       "REFERENCE IDs", "getValue(), not dot-walking", "code2",
       (["var callerId = current.caller_id.sys_id;"],
        ["var callerId = current.getValue('caller_id');"])),
    ],
    end=("SAVE THIS", "FOR CODE REVIEW", "1/6 · Server-side scripting", "▶  Next: Client scripts"),
    end_vo="Save this for your next code review. Next up: client scripts. Follow so you don't miss it."),
 2: dict(
    base="bp2_client_scripts", cat="CLIENT SCRIPTS",
    hook=(("SLOW FORMS?", WHITE), ("FIX THESE 4", AMBER)),
    hook_vo="Is your form slow to load? These four client script habits fix most of it.",
    tips=[
      ("One. Making fields mandatory, visible, or read-only? Use a UI policy, not a client script.",
       "1. Making fields mandatory, visible or read-only? Use a UI Policy, not a Client Script.",
       "UI POLICY FIRST", "mandatory · visible · read-only", "bullets",
       [("Mandatory", "UI Policy", ACCENT), ("Visible", "UI Policy", ACCENT), ("Read-only", "UI Policy", ACCENT),
        ("Complex logic", "Client Script", AMBER)]),
      ("Two. In on change scripts, exit early when the form is loading, or when the new value is empty.",
       "2. In onChange scripts, exit early when the form is loading or the new value is empty.",
       "GUARD onChange", "Exit early", "code1",
       ["function onChange(control, oldValue,", "                  newValue, isLoading) {",
        "  if (isLoading || newValue === '') {", "    return;", "  }", "  // your logic here", "}"]),
      ("Three. Need server data? Use g scratchpad from a display business rule, or asynchronous GlideAjax. Client-side GlideRecord and get reference are no longer recommended.",
       "3. Need server data? Use g_scratchpad (display BR) or async GlideAjax. Client GlideRecord and getReference() are no longer recommended.",
       "CUT SERVER CALLS", "g_scratchpad or async GlideAjax", "code2",
       (["g_form.getReference('caller_id', cb);", "var gr = new GlideRecord('sys_user');"],
        ["// display Business Rule fills it", "var isVip = g_scratchpad.isVip;", "// or only when needed:", "ga.getXMLAnswer(handleAnswer);"])),
      ("Four. Setting a reference field? Pass the display value too, or the form makes an extra trip to the server.",
       "4. Setting a reference field? Pass the display value too, or the form makes an extra trip to the server.",
       "SET DISPLAY VALUE", "on reference fields", "code2",
       (["g_form.setValue('caller_id', userId);"],
        ["g_form.setValue('caller_id', userId,", "                userName);"])),
    ],
    end=("SAVE THIS", "FOR CODE REVIEW", "2/6 · Client scripts", "▶  Next: Business rules"),
    end_vo="Save this for your next code review. Next up: business rules. Follow so you don't miss it."),
 3: dict(
    base="bp3_business_rules", cat="BUSINESS RULES",
    hook=(("4 BUSINESS RULE", WHITE), ("MISTAKES", RED)),
    hook_vo="Four business rule mistakes that slow down your instance.",
    tips=[
      ("One. Don't call current dot update in a business rule. It runs the rules again, and can loop. In a before rule, just set the value. It saves automatically.",
       "1. Don't call current.update() in a Business Rule. It runs the rules again and can loop. In a before rule, just set the value. It saves automatically.",
       "NO current.update()", "it can call itself", "code2",
       (["// after Business Rule", "current.state = 6;", "current.update(); // runs BRs again"],
        ["// before Business Rule", "current.state = 6;", "// saved automatically"])),
      ("Two. Always add a condition. Without one, the rule runs on every single save.",
       "2. Always add a condition. Without one, the rule runs on every single save.",
       "ADD A CONDITION", "or it runs on every save", "bullets",
       [("No condition", "runs every time", RED), ("State changes to Resolved", "runs when needed", ACCENT)]),
      ("Three. If the user doesn't need the result right away, use async instead of after. They get control back faster.",
       "3. If the user doesn't need the result right away, use async instead of after. They get control back faster.",
       "ASYNC > AFTER", "when it can wait", "bullets",
       [("after", "user waits", AMBER), ("async", "runs in the background", ACCENT),
        ("Good for", "integrations, other records", GREY)]),
      ("Four. Don't write global business rules. They load everywhere. Put reusable code in a script include. It only loads when it's called.",
       "4. Don't write global Business Rules. They load everywhere. Put reusable code in a Script Include. It loads only when called.",
       "NO GLOBAL BRs", "use a Script Include", "bullets",
       [("Global Business Rule", "loads on every page", RED), ("Script Include", "loads only when called", ACCENT)]),
    ],
    end=("SAVE THIS", "FOR CODE REVIEW", "3/6 · Business rules", "▶  Next: Debugging"),
    end_vo="Save this for your next code review. Next up: debugging. Follow so you don't miss it."),
 4: dict(
    base="bp4_debugging", cat="DEBUGGING",
    hook=(("STILL USING", WHITE), ("gs.log()?", AMBER)),
    hook_vo="Still debugging with gs dot log? Here's a better way.",
    tips=[
      ("One. gs dot log and gs dot print don't work in scoped apps. Use gs dot info, or gs dot debug. They work in both.",
       "1. gs.log() and gs.print() don't work in scoped apps. Use gs.info() or gs.debug(). They work in both.",
       "gs.info > gs.log", "works in scoped + global", "code2",
       (["gs.log('here');      // global only", "gs.print('x=' + x);  // global only"],
        ["gs.info('MyUtil: x=' + x);", "gs.debug('MyUtil: ' + msg);"])),
      ("Two. Wrap debug messages in a system property check. Turn logging on or off without touching the code.",
       "2. Wrap debug messages in a system property check. Turn logging on or off without touching code.",
       "SWITCH IT OFF", "with a system property", "code1",
       ["if (gs.getProperty('debug.MyUtil')", "      == 'true') {", "  gs.info('MyUtil: ' + details);", "}"]),
      ("Three. Debug business rule shows every rule that ran. Started, finished, or skipped, with the condition that failed.",
       "3. Debug Business Rule shows every rule that ran: started, finished, or skipped, with the condition that failed.",
       "DEBUG BR", "see which rules ran", "bullets",
       [("==>", "started", ACCENT), ("<==", "finished", (140, 170, 255)), ("===", "skipped + failed condition", AMBER)]),
      ("Four. Before production, remove leftover log and alert statements, and switch debugging off.",
       "4. Before production, remove leftover log and alert statements, and switch debugging off.",
       "CLEAN UP", "before production", "bullets",
       [("Remove", "leftover gs.log / alert()", RED), ("Stop Debugging", "System Security", AMBER),
        ("Debug properties", "set to false", ACCENT)]),
    ],
    end=("SAVE THIS", "FOR CODE REVIEW", "4/6 · Debugging", "▶  Next: Logs & queues"),
    end_vo="Save this for your next code review. Next up: logs and queues. Follow so you don't miss it."),
 5: dict(
    base="bp5_logs_and_queues", cat="LOGS & QUEUES",
    hook=(("YOUR LOGS ARE", WHITE), ("WARNING YOU", RED)),
    hook_vo="Your logs are warning you. Here's where to look.",
    tips=[
      ("One. Check System Logs, System Log, All, regularly. Every error should be fixed, or documented as a known issue.",
       "1. Check System Logs > System Log > All regularly. Every error: fix it, or document it as a known issue.",
       "SYSTEM LOG", "fix or document every error", "path",
       (["System Logs", "System Log", "All"],
        [("Error", "fix it", RED), ("Known issue", "document it", AMBER)])),
      ("Two. Search your node logs for these messages. Each one points to a script or query that needs fixing.",
       "2. Search your node logs for these messages. Each one points to a script or query that needs fixing.",
       "SEARCH FOR THESE", "in the node log files", "bullets",
       [("Slow evaluate", "", AMBER), ("Slow Business Rule", "", AMBER), ("Recursive Business Rule", "", RED),
        ("Compiler exception", "", RED), ("Extremely large result", "", AMBER)]),
      ("Three. Open Slow Queries in System Diagnostics. Sort by total execution time, and use the example column to find the script behind it.",
       "3. Open System Diagnostics > Slow Queries. Sort by Total Execution Time, and use Example to find the script behind it.",
       "SLOW QUERIES", "find the script behind it", "path",
       (["System Diagnostics", "Slow Queries"],
        [("Sort", "Total Execution Time", AMBER), ("Read", "the Example column", ACCENT)])),
      ("Four. In the event log, sort by processing duration, and group by name. An event that nothing responds to is just noise.",
       "4. In the Event Log, sort by Processing duration and group by Name. An event nothing responds to is just noise.",
       "NOISY EVENTS", "in the Event Log", "bullets",
       [("Sort", "Processing duration Z→A", AMBER), ("Group by", "Name", (140, 170, 255)),
        ("No action?", "stop logging it", ACCENT)]),
    ],
    end=("SAVE THIS", "FOR YOUR NEXT AUDIT", "5/6 · Logs & queues", "▶  Next: Update sets & XML"),
    end_vo="Save this for your next health check. Next up: update sets and XML. Follow so you don't miss it."),
 6: dict(
    base="bp6_update_sets_xml", cat="UPDATE SETS & XML",
    hook=(("WORKED IN DEV,", WHITE), ("BROKE IN TEST?", RED)),
    hook_vo="Your update set worked in dev, but broke in test? Here's why.",
    tips=[
      ("One. Keep a migration document. The order to apply update sets, plus the plugins, properties and servers to set up.",
       "1. Keep a migration document: the order to apply update sets, plus plugins, properties and servers to set up.",
       "WRITE IT DOWN", "a migration document", "bullets",
       [("1", "Update set order", ACCENT), ("2", "Plugins to activate", ACCENT), ("3", "System properties", ACCENT),
        ("4", "MID & identity servers", ACCENT)]),
      ("Two. Some data isn't captured in update sets, like approval lookup records. Move it as XML, and note that in the update set description.",
       "2. Some data isn't captured in update sets, like approval lookup records. Move it as XML, and note it in the update set description.",
       "DATA STAYS BEHIND", "move it with XML", "bullets",
       [("Not in update sets", "e.g. approval lookups", RED), ("Export", "as XML", AMBER), ("Import", "as XML", AMBER),
        ("Note it", "in the update set description", ACCENT)]),
      ("Three. Importing XML doesn't run business rules, and doesn't update the instance cache. Plan for that.",
       "3. Importing XML doesn't run Business Rules and doesn't update the instance cache. Plan for that.",
       "XML SKIPS RULES", "plan for it", "bullets",
       [("Business Rules", "✗ not run", RED), ("Instance cache", "✗ not updated", RED)]),
      ("Four. An XML export has only that record. Export a user, and their groups and roles don't come with it.",
       "4. An XML export has only that record. Export a user, and their groups and roles don't come with it.",
       "ONE RECORD ONLY", "related records stay behind", "bullets",
       [("User record", "✓ exported", ACCENT), ("Group memberships", "✗ not included", RED), ("Roles", "✗ not included", RED)]),
    ],
    end=("SERIES", "COMPLETE", "6/6 · Update sets & XML", "▶  Share it with your team"),
    end_vo="That's the full best practices series. Save it, share it with your team, and follow for more."),
}

# ---------- visual building blocks ----------
def progress(img, n, total):
    d = ImageDraw.Draw(img)
    x = W - 60 - total * 46
    for i in range(total):
        c = ACCENT if i < n else (70, 80, 105)
        d.rounded_rectangle([x + i * 46, 74, x + i * 46 + 34, 92], 9, fill=c)

def cat_chip(img, text, y=170):
    d = ImageDraw.Draw(img)
    f = font(34)
    w = d.textlength(text, font=f)
    d.rounded_rectangle([(W - w) / 2 - 24, y, (W + w) / 2 + 24, y + 58], 29, fill=(30, 40, 62), outline=ACCENT, width=3)
    d.text(((W - w) / 2, y + 10), text, font=f, fill=ACCENT)

def tip_header(img, n, title, sub, p):
    d = ImageDraw.Draw(img)
    a = ease(p * 4)
    d.rounded_rectangle([W / 2 - 80, 170, W / 2 + 80, 225], 27, fill=AMBER)
    text_c(d, 176, f"TIP {n}", 36, (20, 24, 36), stroke=0)
    size = 80 if len(title) <= 15 else int(80 * 15 / len(title))
    text_c(d, 250 - 30 * (1 - a), title, size, WHITE, kind="m" if "(" in title or "." in title else "b", stroke=7)
    text_c(d, 360, sub, 42, GREY, stroke=3)

def code_pair(img, t, p, bad, good):
    lh = int(30 * 1.55)
    hb = 100 + len(bad) * lh + 10
    hg = 100 + len(good) * lh + 10
    y0 = 450
    code_card(img, (40, y0, 1040, y0 + hb), bad, t, size=30, title="✗  AVOID")
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([40, y0, 1040, y0 + hb], 28, outline=RED, width=4)
    e = ease((p - 0.3) * 4)
    if e > 0:
        y1 = y0 + hb + 40 + 20 * (1 - e)
        code_card(img, (40, y1, 1040, y1 + hg), good, t, size=30, title="✓  DO THIS")
        d = ImageDraw.Draw(img)
        d.rounded_rectangle([40, y1, 1040, y1 + hg], 28, outline=ACCENT, width=4)

def code_single(img, t, p, lines):
    lh = int(30 * 1.55)
    code_card(img, (40, 470, 1040, 470 + 110 + len(lines) * lh), lines, t, size=30, title="✓  DO THIS",
              reveal=0.2 + 0.8 * ease(p * 2))

def bullets(img, t, p, items, y0=470):
    d = ImageDraw.Draw(img)
    n = len(items)
    gap = 18
    h = min(160, (1380 - y0 - gap * n) // n)
    for i, (a, b, c) in enumerate(items):
        e = ease((p - i * (0.6 / n)) * 5)
        if e <= 0:
            continue
        y = y0 + i * (h + gap)
        x = 60 - (1 - e) * 700
        d.rounded_rectangle([x, y, x + 960, y + h], 24, fill=(18, 26, 42), outline=c, width=4)
        d.rounded_rectangle([x, y, x + 16, y + h], 8, fill=c)
        ta = font(44 if b else 50, "m" if a in ("==>", "<==", "===") else "b")
        if b:
            d.text((x + 50, y + h / 2 - 50), a, font=ta, fill=WHITE)
            d.text((x + 50, y + h / 2 + 4), b, font=font(38, "r"), fill=c if c != GREY else (200, 205, 215))
        else:
            d.text((x + 50, y + h / 2 - 28), a, font=ta, fill=WHITE)

def path_scene(img, t, p, crumbs, items):
    d = ImageDraw.Draw(img)
    f = font(38)
    x, y = 60, 470
    for i, c in enumerate(crumbs):
        e = ease((p - i * 0.12) * 5)
        if e <= 0:
            break
        w = d.textlength(c, font=f)
        if x + w + 60 > W - 40:
            x, y = 60, y + 100
        d.rounded_rectangle([x, y, x + w + 48, y + 80], 18, fill=CARD)
        d.text((x + 24, y + 18), c, font=f, fill=INK)
        x += w + 48
        if i < len(crumbs) - 1:
            d.text((x + 10, y + 12), "›", font=font(48), fill=AMBER)
            x += 56
    bullets(img, t, max(0, p - 0.3) / 0.7, items, y0=y + 140)

def make(spec):
    lines = [("hook", spec["hook_vo"], spec["hook_vo"])]
    scenes = {}
    total = len(spec["tips"])

    def s_hook(img, t, p):
        d = ImageDraw.Draw(img)
        cat_chip(img, "BEST PRACTICES · " + spec["cat"])
        (l1, c1), (l2, c2) = spec["hook"]
        s1 = 104 if len(l1) <= 14 else int(104 * 14 / len(l1))
        s2 = 104 if len(l2) <= 14 else int(104 * 14 / len(l2))
        text_c(d, 560, l1, s1, c1, kind="m" if "(" in l1 else "b", stroke=8)
        text_c(d, 700, l2, s2, c2, kind="m" if "(" in l2 else "b", stroke=8)
        for i in range(total):
            e = ease((p - 0.2 - i * 0.12) * 5)
            r = 34 * e
            cx = W / 2 + (i - (total - 1) / 2) * 120
            if r > 1:
                d.ellipse([cx - r, 1000 - r, cx + r, 1000 + r], fill=AMBER)
                if e > 0.8:
                    ff = font(36)
                    tw = d.textlength(str(i + 1), font=ff)
                    d.text((cx - tw / 2, 978), str(i + 1), font=ff, fill=(20, 24, 36))
    scenes["hook"] = s_hook

    for i, (vo, cap, title, sub, kind, payload) in enumerate(spec["tips"]):
        key = f"tip{i + 1}"
        lines.append((key, vo, cap))
        def scene(img, t, p, i=i, title=title, sub=sub, kind=kind, payload=payload):
            tip_header(img, i + 1, title, sub, p)
            if kind == "code2":
                code_pair(img, t, p, *payload)
            elif kind == "code1":
                code_single(img, t, p, payload)
            elif kind == "bullets":
                bullets(img, t, p, payload)
            elif kind == "path":
                path_scene(img, t, p, *payload)
            progress(img, i + 1, total)
        scenes[key] = scene

    l1, l2, sub, cta = spec["end"]
    lines.append(("end", spec["end_vo"], spec["end_vo"]))
    def s_end(img, t, p):
        end_card(img, t, p, l1, l2, "Best Practices series", sub, cta)
    scenes["end"] = s_end
    return lines, scenes

if __name__ == "__main__":
    k = int(sys.argv[1])
    spec = SPECS[k]
    here = os.path.join(HERE, f"bp{k}")
    os.makedirs(here, exist_ok=True)
    lines, scenes = make(spec)
    print(render(lines, scenes, here, spec["base"]))

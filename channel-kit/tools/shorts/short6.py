"""Short 6 - 'Interview question: what is ZZ_YY?'"""
import math, os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from snlib import *
from PIL import Image, ImageDraw, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))

LINES = [
    ("hook",  "Interview question. What does Z Z, Y Y mean in ServiceNow?",
              "Interview question: what does ZZ_YY mean in ServiceNow?"),
    ("pause", "Pause, and answer. Three. Two. One.",
              "Pause and answer. 3. 2. 1."),
    ("a1",    "It's a prefix on the table name, in sys attachment.",
              "It's a prefix on the table name in sys_attachment."),
    ("a2",    "It means the file belongs to a variable, or an image field. Not the record itself.",
              "It means the file belongs to a variable or an image field, not the record itself."),
    ("a3",    "That's why it's hidden from the attachment list. By design, not a bug.",
              "That's why it's hidden from the attachment list. By design, not a bug."),
    ("a4",    "Need it visible? An async business rule sets the table name back.",
              "Need it visible? An async Business Rule sets the table name back."),
    ("end",   "Got it right? Comment yes. Follow for more ServiceNow interview questions.",
              "Got it right? Comment YES. Follow for more ServiceNow interview questions."),
]

ANSWERS = [
    ("Prefix on", "sys_attachment.table_name"),
    ("File belongs to a", "variable / image field"),
    ("Hidden from the", "attachment list (by design)"),
    ("Need it visible?", "async Business Rule"),
]

def s_hook(img, t, p):
    d = ImageDraw.Draw(img)
    e = ease(p * 3)
    d.rounded_rectangle([250, 240, 830, 360], 60, fill=AMBER)
    text_c(d, 262, "INTERVIEW Q", 74, (20, 24, 36), stroke=0)
    text_c(d, 560, "What does", 90, WHITE, stroke=8)
    text_c(d, 700, "ZZ_YY", int(150 + 20 * e), AMBER, kind="m", stroke=10)
    text_c(d, 900, "mean in", 90, WHITE, stroke=8)
    text_c(d, 1020, "ServiceNow?", 90, ACCENT, stroke=8)

def s_pause(img, t, p):
    d = ImageDraw.Draw(img)
    text_c(d, 300, "PAUSE & ANSWER", 90, WHITE, stroke=8)
    n = 3 - min(2, int(p * 3.2))
    s = 1 + 0.15 * math.sin(t * 8)
    cx, cy, r = W // 2, 850, int(230 * s)
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=AMBER, width=14)
    f = font(300)
    w = d.textlength(str(n), font=f)
    d.text((cx - w / 2, cy - 190), str(n), font=f, fill=AMBER)

def answers(img, t, p, upto):
    header(img, "THE ANSWER", None, ACCENT, 1.0)
    d = ImageDraw.Draw(img)
    for i, (a, b) in enumerate(ANSWERS[:upto + 1]):
        e = ease(p * 4) if i == upto else 1
        y = 440 + i * 220
        x = 70 - (1 - e) * 900
        cur = i == upto
        d.rounded_rectangle([x, y, x + 940, y + 190], 26, fill=(18, 26, 42), outline=ACCENT if cur else (60, 70, 95), width=5 if cur else 3)
        d.ellipse([x + 30, y + 55, x + 110, y + 135], fill=ACCENT if cur else (60, 70, 95))
        d.text((x + 55, y + 63), str(i + 1), font=font(50), fill=(10, 30, 20) if cur else WHITE)
        d.text((x + 140, y + 32), a, font=font(40, "r"), fill=GREY)
        d.text((x + 140, y + 95), b, font=font(46, "m" if "_" in b or "." in b else "b"), fill=WHITE if cur else (190, 196, 210))

def s_a1(img, t, p): answers(img, t, p, 0)
def s_a2(img, t, p): answers(img, t, p, 1)
def s_a3(img, t, p): answers(img, t, p, 2)
def s_a4(img, t, p): answers(img, t, p, 3)

def s_end(img, t, p):
    end_card(img, t, p, "GOT IT RIGHT?", "COMMENT YES ✓", "Full explainer", "(ZZ_YY + Business Rule fix)", "▶  Full video on the channel")

SCENES = dict(hook=s_hook, pause=s_pause, a1=s_a1, a2=s_a2, a3=s_a3, a4=s_a4, end=s_end)
print(render(LINES, SCENES, HERE, "short6_interview_question"))
